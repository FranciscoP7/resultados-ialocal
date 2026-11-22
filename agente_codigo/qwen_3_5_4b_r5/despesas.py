from decimal import Decimal, InvalidOperation
from collections import defaultdict


def resumir_despesas(lancamentos):
    """
    Resumir despesas de uma lista de lançamentos.
    
    Args:
        lancamentos: Lista de dicionários com 'categoria' e 'valor'
        
    Returns:
        Dicionário com 'total_geral', 'quantidade_lancamentos' e 'por_categoria'
        
    Raises:
        ValueError: Se houver lançamentos inválidos
    """
    if not isinstance(lancamentos, list):
        raise ValueError("A entrada deve ser uma lista")
    
    categorias = defaultdict(lambda: {"total": Decimal("0"), "quantidade": 0})
    total_geral = Decimal("0")
    quantidade_lancamentos = 0
    
    for lancamento in lancamentos:
        if not isinstance(lancamento, dict):
            raise ValueError("Cada elemento deve ser um dicionário")
        
        categoria = lancamento.get("categoria")
        valor_str = lancamento.get("valor")
        
        if categoria is None or categoria == "":
            raise ValueError("Categoria não pode ser vazia")
        
        if not isinstance(valor_str, str):
            raise ValueError("Valor deve ser uma string")
        
        try:
            valor = Decimal(valor_str)
        except InvalidOperation:
            raise ValueError(f"Valor '{valor_str}' não é numérico")
        
        if valor < 0:
            raise ValueError(f"Valor não pode ser negativo: {valor}")
        
        categoria_normalizada = categoria.strip()
        if not categoria_normalizada:
            raise ValueError(f"Categoria '{categoria}' é vazia após remoção de espaços")
        
        categorias[categoria_normalizada]["total"] += valor
        categorias[categoria_normalizada]["quantidade"] += 1
        total_geral += valor
        quantidade_lancamentos += 1
    
    # Ordenar por maior gasto (decrescente), depois alfabético
    por_categoria = sorted(
        categorias.items(),
        key=lambda x: (-x[1]["total"], x[0])
    )
    
    resultado = {
        "total_geral": str(total_geral.quantize(Decimal("0.01"))),
        "quantidade_lancamentos": quantidade_lancamentos,
        "por_categoria": [
            {
                "categoria": cat,
                "total": str(data["total"].quantize(Decimal("0.01"))),
                "quantidade": data["quantidade"]
            }
            for cat, data in por_categoria
        ]
    }
    
    return resultado
