import decimal

def resumir_despesas(lancamentos):
    """
    Resumo de despesas por categoria.

    Args:
        lancamentos: Lista de dicionários com informações sobre as despesas.

    Returns:
        Um dicionário contendo o resumo das despesas.
    """
    por_categoria = {}
    total_geral = decimal.Decimal('0.00')
    quantidade_lancamentos = 0

    for lancamento in lancamentos:
        try:
            categoria = lancamento['categoria'].strip()
            valor_str = lancamento['valor'].strip()
            valor = decimal.Decimal(valor_str)

            if valor < 0:
                raise ValueError("Valor da despesa não pode ser negativo.")

            if not isinstance(valor, decimal.Decimal):
                raise ValueError("Valor da despesa deve ser um número decimal.")

            if categoria in por_categoria:
                por_categoria[categoria]['total'] += valor
                por_categoria[categoria]['quantidade'] += 1
            else:
                por_categoria[categoria] = {'total': valor, 'quantidade': 1}

            total_geral += valor
            quantidade_lancamentos += 1

        except (KeyError, ValueError) as e:
            print(f"Lançamento inválido: {lancamento}. Erro: {e}")
            continue # Ignora o lançamento inválido e continua com o próximo

    # Ordena as categorias por total (decrescente) e, em caso de empate, por nome (alfabético)
    categorias_ordenadas = sorted(por_categoria.items(), key=lambda item: (item[1]['total'], item[0]), reverse=True)

    resultado = {
        'total_geral': str(total_geral),
        'quantidade_lancamentos': str(quantidade_lancamentos),
        'por_categoria': categorias_ordenadas
    }

    return resultado

if __name__ == '__main__':
    # Exemplo de uso (para testes rápidos)
    despesas = [
        {'categoria': 'Alimentação', 'valor': '150.50'},
        {'categoria': 'Transporte', 'valor': '75.25'},
        {'categoria': 'Alimentação', 'valor': '25.75'},
        {'categoria': 'Moradia', 'valor': '300.00'},
        {'categoria': 'Transporte', 'valor': '100.00'}
    ]
    resultado = resumir_despesas(despesas)
    print(resultado)
