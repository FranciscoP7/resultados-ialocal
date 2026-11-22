import unittest
from decimal import Decimal
from despesas import resumir_despesas


class TestResumirDespesas(unittest.TestCase):
    
    def test_casos_normais(self):
        """Teste com casos normais de entrada"""
        lancamentos = [
            {"categoria": "Alimentação", "valor": "50.00"},
            {"categoria": "Alimentação", "valor": "30.50"},
            {"categoria": "Transporte", "valor": "20.00"},
            {"categoria": "Transporte", "valor": "15.50"},
            {"categoria": "Lazer", "valor": "100.00"},
        ]
        
        resultado = resumir_despesas(lancamentos)
        
        self.assertEqual(resultado["total_geral"], "226.00")
        self.assertEqual(resultado["quantidade_lancamentos"], 5)
        
        self.assertEqual(len(resultado["por_categoria"]), 3)
        
        # Verificar ordem (maior gasto primeiro)
        categorias = resultado["por_categoria"]
        self.assertEqual(categorias[0]["categoria"], "Lazer")
        self.assertEqual(categorias[0]["total"], "100.00")
        self.assertEqual(categorias[0]["quantidade"], 1)
        
        self.assertEqual(categorias[1]["categoria"], "Alimentação")
        self.assertEqual(categorias[1]["total"], "80.50")
        self.assertEqual(categorias[1]["quantidade"], 2)
        
        self.assertEqual(categorias[2]["categoria"], "Transporte")
        self.assertEqual(categorias[2]["total"], "35.50")
        self.assertEqual(categorias[2]["quantidade"], 2)
    
    def test_lista_vazia(self):
        """Teste com lista vazia"""
        resultado = resumir_despesas([])
        
        self.assertEqual(resultado["total_geral"], "0.00")
        self.assertEqual(resultado["quantidade_lancamentos"], 0)
        self.assertEqual(len(resultado["por_categoria"]), 0)
    
    def test_espacos_em_categorias(self):
        """Teste com categorias que têm espaços extras"""
        lancamentos = [
            {"categoria": "  Alimentação  ", "valor": "50.00"},
            {"categoria": "Alimentação", "valor": "30.00"},
            {"categoria": "  Transporte", "valor": "20.00"},
        ]
        
        resultado = resumir_despesas(lancamentos)
        
        self.assertEqual(resultado["total_geral"], "100.00")
        self.assertEqual(resultado["quantidade_lancamentos"], 3)
        
        # Verificar que categorias foram normalizadas
        categorias = resultado["por_categoria"]
        self.assertEqual(categorias[0]["categoria"], "Alimentação")
        self.assertEqual(categorias[0]["total"], "80.00")
        self.assertEqual(categorias[0]["quantidade"], 2)
    
    def test_valores_invalidos(self):
        """Teste com valores inválidos"""
        lancamentos = [
            {"categoria": "Alimentação", "valor": "abc"},
            {"categoria": "", "valor": "50.00"},
            {"categoria": "Transporte", "valor": "-10.00"},
        ]
        
        with self.assertRaises(ValueError) as context:
            resumir_despesas(lancamentos)
        
        self.assertIn("não é numérico", str(context.exception))
    
    def test_empate_ordenacao_alfabetica(self):
        """Teste com empate no valor (ordem alfabética)"""
        lancamentos = [
            {"categoria": "Banana", "valor": "50.00"},
            {"categoria": "Abacaxi", "valor": "50.00"},
            {"categoria": "Uva", "valor": "50.00"},
        ]
        
        resultado = resumir_despesas(lancamentos)
        
        categorias = resultado["por_categoria"]
        
        # Verificar ordem alfabética em caso de empate
        self.assertEqual(categorias[0]["categoria"], "Abacaxi")
        self.assertEqual(categorias[1]["categoria"], "Banana")
        self.assertEqual(categorias[2]["categoria"], "Uva")
    
    def test_decimal_precisao(self):
        """Teste com valores decimais complexos"""
        lancamentos = [
            {"categoria": "Teste", "valor": "10.123456"},
            {"categoria": "Teste", "valor": "20.987654"},
        ]
        
        resultado = resumir_despesas(lancamentos)
        
        self.assertEqual(resultado["total_geral"], "31.11")
        self.assertEqual(resultado["por_categoria"][0]["total"], "31.11")
    
    def test_entrada_invalida_nao_lista(self):
        """Teste com entrada inválida (não lista)"""
        with self.assertRaises(ValueError):
            resumir_despesas("não é uma lista")
    
    def test_entrada_invalida_elemento_nao_dict(self):
        """Teste com elemento que não é dicionário"""
        lancamentos = [
            {"categoria": "Teste", "valor": "50.00"},
            "não é um dicionário",
        ]
        
        with self.assertRaises(ValueError):
            resumir_despesas(lancamentos)


if __name__ == "__main__":
    unittest.main()
