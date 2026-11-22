import csv
from collections import defaultdict
import statistics

ARQ_ENTRADA = r"C:\Experimento_LLM\resultados\metricas_brutas.csv"
ARQ_SAIDA = r"C:\Experimento_LLM\resultados\resumo_estatistico.csv"

grupos = defaultdict(lambda: {
    "tempo_total": [],
    "tempo_carga": [],
    "tokens_saida": [],
    "tps": [],
    "vram": [],
    "alocacao": set()
})

with open(ARQ_ENTRADA, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        chave = (row["Modelo"], row["Tarefa"])
        grupos[chave]["tempo_total"].append(float(row["Tempo_Total_s"]))
        grupos[chave]["tempo_carga"].append(float(row["Tempo_Carga_s"]))
        grupos[chave]["tokens_saida"].append(int(row["Tokens_Saida"]))
        grupos[chave]["tps"].append(float(row["Tokens_Por_Segundo"]))
        grupos[chave]["vram"].append(int(row["VRAM_Usada_MB"]))
        # Extrai a parte de % GPU/CPU do status do ollama ps
        partes = row["Status_Ollama_PS"].split()
        proc = " ".join(p for p in partes if "%" in p or p in ("GPU", "CPU"))
        grupos[chave]["alocacao"].add(proc if proc else row["Status_Ollama_PS"])

def stats(valores):
    media = statistics.mean(valores)
    mediana = statistics.median(valores)
    dp = statistics.stdev(valores) if len(valores) > 1 else 0.0
    return round(media, 2), round(mediana, 2), round(dp, 2)

with open(ARQ_SAIDA, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out, delimiter=";")
    writer.writerow([
        "Modelo", "Tarefa", "N_Execucoes",
        "TPS_Media", "TPS_Mediana", "TPS_DesvioPadrao",
        "TempoTotal_Media_s", "TempoTotal_Mediana_s", "TempoTotal_DP_s",
        "TempoCarga_Media_s", "TokensSaida_Media",
        "VRAM_Media_MB", "VRAM_Pico_MB", "Alocacao_Hardware"
    ])

    print(f"{'MODELO':<45} | {'TAREFA':<12} | {'TPS (Med/Méd)':<15} | {'TEMPO (Med)':<11} | {'VRAM (MB)':<10} | {'HARDWARE'}")
    print("-" * 115)

    for (modelo, tarefa), dados in grupos.items():
        tps_med, tps_mediana, tps_dp = stats(dados["tps"])
        tt_med, tt_mediana, tt_dp = stats(dados["tempo_total"])
        tc_med, _, _ = stats(dados["tempo_carga"])
        tok_med, _, _ = stats(dados["tokens_saida"])
        vram_med = round(statistics.mean(dados["vram"]))
        vram_pico = max(dados["vram"])
        aloc = " / ".join(sorted(dados["alocacao"]))

        writer.writerow([
            modelo, tarefa, len(dados["tps"]),
            tps_med, tps_mediana, tps_dp,
            tt_med, tt_mediana, tt_dp,
            tc_med, tok_med,
            vram_med, vram_pico, aloc
        ])

        nome_curto = modelo.split("/")[-1]
        print(f"{nome_curto:<45} | {tarefa:<12} | {tps_mediana:>6} / {tps_med:<6} | {tt_mediana:>9} s | {vram_pico:>10} | {aloc}")

print(f"\nResumo salvo em: {ARQ_SAIDA}")
