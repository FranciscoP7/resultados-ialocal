from decimal import Decimal, InvalidOperation

def resumir_despesas(lancamentos):
    if not lancamentos:
        return {
            'total_geral': '0.00',
            'quantidade_lancamentos': 0,
            'por_categoria': []
        }

    categorias = {}
    total_geral = Decimal('0.00')

    for lancamento in lancamentos:
        if not lancamento.get('categoria') or not lancamento.get('valor'):
            raise ValueError("Categorias vazias ou valores não fornecidos")

        categoria = lancamento['categoria'].strip()
        valor_str = lancamento['valor'].replace(',', '.')

        try:
            valor = Decimal(valor_str)
        except InvalidOperation:
            raise ValueError("Valores não numéricos")

        if valor < 0:
            raise ValueError("Valores negativos não são permitidos")

        if categoria not in categorias:
            categorias[categoria] = {
                'total': Decimal('0.00'),
                'quantidade': 0
            }

        categorias[categoria]['total'] += valor
        categorias[categoria]['quantidade'] += 1
        total_geral += valor

    por_categoria = [
        {
            'categoria': categoria,
            'total': str(categorias[categoria]['total'].quantize(Decimal('0.00'))),
            'quantidade': categorias[categoria]['quantidade']
        }
        for categoria in sorted(categorias, key=lambda x: (-categorias[x]['total'], x))
    ]

    return {
        'total_geral': str(total_geral.quantize(Decimal('0.00'))),
        'quantidade_lancamentos': len(lancamentos),
        'por_categoria': por_categoria
    }
