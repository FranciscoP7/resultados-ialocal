import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Experimento_LLM"
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
IMAGENS_DIR = os.path.join(BASE_DIR, "imagens")

os.makedirs(PROMPTS_DIR, exist_ok=True)
os.makedirs(IMAGENS_DIR, exist_ok=True)

prompts = {
    "p1_hardware.txt": """Explique as diferenças entre memória RAM, memória VRAM e armazenamento SSD no contexto da execução local de grandes modelos de linguagem (LLMs).
Para cada componente, apresente:
1. Sua principal função no computador.
2. Como participa do carregamento e da execução de um modelo de IA.
3. Quais problemas podem ocorrer quando sua capacidade é insuficiente.
Ao final, explique por que a memória compartilhada do sistema não deve ser considerada equivalente à memória VRAM dedicada.
Utilize linguagem clara e tecnicamente correta, sem ultrapassar 200 palavras. Não invente especificações de hardware que não foram fornecidas.""",

    "p2_sensores.txt": """Um laboratório recebeu 46 sensores que precisam ser distribuídos integralmente entre três caixas: A, B e C.
Sabe-se que:
1. A caixa B deve conter o dobro da quantidade de sensores da caixa A.
2. A caixa C deve conter seis sensores a mais do que a caixa A.
3. Todos os 46 sensores devem ser distribuídos, sem sobras.
Determine quantos sensores devem ser colocados em cada caixa.
Apresente as equações utilizadas, o resultado final e uma verificação que demonstre que todas as condições foram atendidas.
Não utilize informações externas nem acrescente condições que não estejam descritas no problema.""",

    "p3_programacao.txt": """Atue como um desenvolvedor Python experiente.
Crie dois arquivos neste diretório: 'despesas.py' e 'test_despesas.py'.

No arquivo 'despesas.py', desenvolva uma função chamada resumir_despesas(lancamentos) utilizando Python 3.11 ou superior e exclusivamente bibliotecas da própria linguagem.
A função deverá receber uma lista de dicionários, cada um contendo:
- categoria: nome da categoria da despesa.
- valor: valor monetário representado como uma string decimal, utilizando ponto como separador.

Requisitos funcionais:
1. Agrupar os lançamentos por categoria, desconsiderando espaços no início e no final dos nomes.
2. Calcular o valor total gasto em cada categoria.
3. Informar a quantidade de lançamentos de cada categoria.
4. Calcular o total geral de todas as despesas.
5. Ordenar as categorias pelo maior gasto, em ordem decrescente. Em caso de empate, utilizar ordem alfabética.
6. Utilizar Decimal para evitar imprecisões em cálculos monetários.
7. Rejeitar registros inválidos, categorias vazias, valores não numéricos ou negativos, gerando ValueError.
8. Para uma lista vazia, retornar um resultado válido com total igual a zero e nenhuma categoria.

Formato esperado do retorno:
Um dicionário contendo 'total_geral', 'quantidade_lancamentos' e 'por_categoria' (lista de dicionários com 'categoria', 'total' e 'quantidade'). Os valores monetários devem ser strings com duas casas decimais.

No arquivo 'test_despesas.py', desenvolva testes automatizados utilizando unittest cobrindo casos normais, lista vazia, valores inválidos e situações de empate.""",

    "p4_visao_cena.txt": """Analise cuidadosamente a imagem anexada.
Descreva detalhadamente os objetos visíveis na cena, informando suas cores predominantes, quantidades e relações espaciais (esquerda, direita, centro, primeiro plano ou fundo).
Não invente informações nem deduza elementos que não estejam claramente visíveis na imagem.""",

    "p4_visao_nota.txt": """Analise cuidadosamente a imagem anexada.
Você recebeu a imagem de um documento comercial contendo uma tabela de produtos, quantidades e preços unitários.
Execute as seguintes tarefas:
1. Identifique e transcreva todos os produtos apresentados.
2. Extraia a quantidade e o preço unitário de cada produto.
3. Calcule o subtotal de cada item, multiplicando a quantidade pelo preço unitário.
4. Calcule o valor total de todos os produtos.
5. Verifique se os cálculos estão matematicamente corretos.
Organize os resultados em uma tabela com as colunas: Produto, Quantidade, Preço unitário e Subtotal, e apresente o total geral ao final.
Não invente informações que não estejam visíveis na imagem."""
}

for nome, conteudo in prompts.items():
    with open(os.path.join(PROMPTS_DIR, nome), "w", encoding="utf-8") as f:
        f.write(conteudo.strip())

# Gera a imagem padronizada nota_comercial.png
img = Image.new("RGB", (900, 420), "white")
draw = ImageDraw.Draw(img)
try:
    fonte_titulo = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
    fonte_texto = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
except Exception:
    fonte_titulo = fonte_texto = ImageFont.load_default()

draw.text((40, 30), "ORÇAMENTO COMERCIAL Nº 2026-084", fill="black", font=fonte_titulo)
draw.line([(40, 70), (860, 70)], fill="black", width=2)

linhas = [
    ("Produto", "Qtd", "Preço Unitário (R$)", "Subtotal (R$)"),
    ("Teclado Mecânico USB", "2", "245.50", "491.00"),
    ("Mouse Óptico Sem Fio", "3", "89.90", "269.70"),
    ("Cabo HDMI 2.1 (2 metros)", "4", "42.00", "168.00"),
    ("Suporte Articulado Monitor", "1", "185.00", "185.00"),
]

y = 90
for i, (prod, qtd, unit, sub) in enumerate(linhas):
    f_atual = fonte_titulo if i == 0 else fonte_texto
    draw.text((40, y), prod, fill="black", font=f_atual)
    draw.text((420, y), qtd, fill="black", font=f_atual)
    draw.text((520, y), unit, fill="black", font=f_atual)
    draw.text((730, y), sub, fill="black", font=f_atual)
    y += 45
    if i == 0:
        draw.line([(40, y - 10), (860, y - 10)], fill="black", width=1)

draw.line([(40, y + 5), (860, y + 5)], fill="black", width=2)
draw.text((520, y + 20), "TOTAL GERAL: R$ 1113.70", fill="black", font=fonte_titulo)

img.save(os.path.join(IMAGENS_DIR, "nota_comercial.png"))
print("Prompts e nota_comercial.png criados com sucesso!")