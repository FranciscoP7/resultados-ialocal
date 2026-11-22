import glob
import os
import re

RESP_DIR = r"C:\Experimento_LLM\resultados\respostas_txt"
OUT_FILE = r"C:\Experimento_LLM\resultados\auditoria_e_apendice_d.txt"

arquivos = sorted(glob.glob(os.path.join(RESP_DIR, "*.txt")))

if not arquivos:
    print("Nenhum arquivo encontrado em:", RESP_DIR)
    raise SystemExit

print(f"{'ARQUIVO':<58} | {'PALAVRAS':<8} | {'VERIFICAÇÃO OBJETIVA'}")
print("-" * 105)

with open(OUT_FILE, "w", encoding="utf-8") as f_out:
    f_out.write("=== CONSOLIDAÇÃO DE RESPOSTAS E AUDITORIA OBJETIVA ===\n\n")

    for arq in arquivos:
        nome = os.path.basename(arq)
        with open(arq, "r", encoding="utf-8") as f:
            texto = f.read().strip()

        palavras = len(texto.split())
        if "P1_Hardware" in nome:
            status = "OK (<=200 palavras)" if palavras <= 200 else f"EXCEDEU ({palavras} palavras)"
        elif "P2_Sensores" in nome:
            ok_10 = bool(re.search(r"\b10\b", texto))
            ok_20 = bool(re.search(r"\b20\b", texto))
            ok_16 = bool(re.search(r"\b16\b", texto))
            status = "OK (10, 20, 16)" if (ok_10 and ok_20 and ok_16) else "VERIFICAR CÁLCULO"
        elif "P4_Nota" in nome:
            ok_tot = any(v in texto for v in ("1113.70", "1113,70", "1.113,70", "1.113.70"))
            status = "OK (Total 1113,70)" if ok_tot else "VERIFICAR TOTAL"
        elif "P4_Cena" in nome:
            status = "Conferir objetos com cena.jpg"
        else:
            status = "-"

        print(f"{nome:<58} | {palavras:<8} | {status}")

        if "_R1.txt" in nome:
            f_out.write(f"{'='*80}\nARQUIVO: {nome} | Palavras: {palavras} | Auditoria: {status}\n{'='*80}\n")
            f_out.write(texto + "\n\n")

print(f"\nArquivo consolidado salvo em: {OUT_FILE}")
