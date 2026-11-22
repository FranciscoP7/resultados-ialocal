import base64
from collections import Counter
import csv
import json
import os
import subprocess
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
BASE_DIR = r"C:\Experimento_LLM"

MODELOS = [
    "hf.co/ggml-org/gemma-3-4b-it-GGUF:Q4_K_M",
    "hf.co/ggml-org/Qwen3.5-4B-GGUF:Q4_K_M",
    "hf.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M",
    "qwen3-vl:4b",
]

TAREFAS = [
    {"id": "P1_Hardware", "prompt": "p1_hardware.txt", "imagem": None, "multimodal": False},
    {"id": "P2_Sensores", "prompt": "p2_sensores.txt", "imagem": None, "multimodal": False},
    {"id": "P4_Cena", "prompt": "p4_visao_cena.txt", "imagem": "cena.jpg", "multimodal": True},
    {"id": "P4_Nota", "prompt": "p4_visao_nota.txt", "imagem": "nota_comercial.png", "multimodal": True},
]

def obter_vram_mb():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            text=True
        )
        return int(out.strip().splitlines()[0])
    except Exception:
        return -1

def obter_divisao_processamento():
    try:
        out = subprocess.check_output(["ollama", "ps"], text=True)
        linhas = [l.strip() for l in out.strip().splitlines() if l.strip()]
        return linhas[-1] if len(linhas) > 1 else "N/A"
    except Exception:
        return "Erro"

def carregar_imagem_b64(nome_arquivo):
    caminho = os.path.join(BASE_DIR, "imagens", nome_arquivo)
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def consultar_ollama(modelo, texto_prompt, img_b64=None):
    payload = {
        "model": modelo,
        "prompt": texto_prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "seed": 42,
            "num_ctx": 8192
        }
    }
    if img_b64:
        payload["images"] = [img_b64]

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    inicio = time.perf_counter()
    with urllib.request.urlopen(req, timeout=300) as resp:
        dados = json.loads(resp.read().decode("utf-8"))
    tempo_parede = time.perf_counter() - inicio
    return dados, tempo_parede

def carregar_concluidos(csv_path):
    contagem = Counter()
    if not os.path.exists(csv_path):
        return contagem
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                contagem[(row[0], row[1])] += 1
    return contagem

def main():
    csv_path = os.path.join(BASE_DIR, "resultados", "metricas_brutas.csv")
    respostas_dir = os.path.join(BASE_DIR, "resultados", "respostas_txt")
    os.makedirs(respostas_dir, exist_ok=True)

    concluidos = carregar_concluidos(csv_path)
    arquivo_existe = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0

    with open(csv_path, "a", newline="", encoding="utf-8") as f_csv:
        writer = csv.writer(f_csv, delimiter=";")
        if not arquivo_existe:
            writer.writerow([
                "Modelo", "Tarefa", "Rodada", "Tempo_Total_s", "Tempo_Carga_s",
                "Tokens_Entrada", "Tokens_Saida", "Tokens_Por_Segundo",
                "VRAM_Usada_MB", "Status_Ollama_PS"
            ])

        for modelo in MODELOS:
            nome_limpo = modelo.replace("/", "_").replace(":", "_")
            for tarefa in TAREFAS:
                if tarefa["multimodal"] and "Coder" in modelo:
                    continue

                if concluidos[(modelo, tarefa["id"])] >= 5:
                    print(f"[PULANDO] {modelo} | {tarefa['id']} (já concluído)")
                    continue

                with open(os.path.join(BASE_DIR, "prompts", tarefa["prompt"]), encoding="utf-8") as fp:
                    prompt_txt = fp.read()

                img_b64 = carregar_imagem_b64(tarefa["imagem"]) if tarefa["imagem"] else None

                for rodada in range(0, 6):
                    tipo = "AQUECIMENTO" if rodada == 0 else f"Execução {rodada}/5"
                    print(f"[{modelo}] {tarefa['id']} -> {tipo}...")

                    dados, tempo_parede = consultar_ollama(modelo, prompt_txt, img_b64)
                    vram = obter_vram_mb()
                    ps_info = obter_divisao_processamento()

                    if rodada == 0:
                        continue

                    load_s = dados.get("load_duration", 0) / 1e9
                    eval_count = dados.get("eval_count", 0)
                    eval_dur_s = dados.get("eval_duration", 1) / 1e9
                    prompt_tokens = dados.get("prompt_eval_count", 0)
                    tps = round(eval_count / eval_dur_s, 2) if eval_dur_s > 0 else 0

                    writer.writerow([
                        modelo, tarefa["id"], rodada, round(tempo_parede, 3),
                        round(load_s, 3), prompt_tokens, eval_count, tps, vram, ps_info
                    ])
                    f_csv.flush()

                    arq_resp = f"{nome_limpo}_{tarefa['id']}_R{rodada}.txt"
                    with open(os.path.join(respostas_dir, arq_resp), "w", encoding="utf-8") as fr:
                        fr.write(dados.get("response", ""))

    print("\nColeta concluída! Dados salvos em C:\\Experimento_LLM\\resultados\\metricas_brutas.csv")

if __name__ == "__main__":
    main()
