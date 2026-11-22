from decimal import Decimal
import re

def resumir_despesas(lancamentos):
    """
    Resumo de despesas por categoria.

    Args:
        lancamentos: Lista de dicionários com informações de despesas.

    Returns:
        Um dicionário contendo o resumo das despesas.
    """
    total_geral = Decimal('0.00')
    por_categoria = []

    for lancamento in lancamentos:
        try:
            categoria = re.sub(r'^\s+|\s+$', '', lancamento['categoria']) # Remove espaços em branco
            valor_str = lancamento['valor']
            valor = Decimal(valor_str)

            if valor < 0:
                raise ValueError("Valor da despesa não pode ser negativo.")

            total_geral += valor

            # Verifica se a categoria já existe
            categoria_exists = False
            for cat in por_categoria:
                if cat['categoria'] == categoria:
                    cat['total'] += valor
                    cat['quantidade'] += 1
                    categoria_exists = True
                    break

            if not categoria_exists:
                por_categoria.append({'categoria': categoria, 'total': valor, 'quantidade': 1})

        except (KeyError, ValueError) as e:
            print(f"Lançamento inválido: {lancamento}. Erro: {e}")
            # Lidar com o erro de forma apropriada (ex: registrar, ignorar, etc.)
            continue

    # Ordena por total (decrescente) e, em caso de empate, por categoria (alfabética)
    por_categoria.sort(key=lambda x: (-x['total'], x['categoria']))

    return {
        'total_geral': str(total_geral),
        'quantidade_lancamentos': len(lancamentos),
        'por_categoria': por_categoria
    }

if __name__ == '__main__':
    # Exemplo de uso
    despesas = [
        {'categoria': 'Alimentação', 'valor': '150.50'},
        {'categoria': 'Moradia', 'valor': '800.00'},
        {'categoria': 'Alimentação', 'valor': '75.25'},
        {'categoria': 'Transporte', 'valor': '100.75'},
        {'categoria': 'Moradia', 'valor': '900.00'}
    ]
    resumo = resumir_despesas(despesas)
    print(resumo)
