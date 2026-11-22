import unittest
from despesas import resumir_despesas

class TestResumirDespesas(unittest.TestCase):

    def test_lista_vazia(self):
        resultado = resumir_despesas([])
        self.assertEqual(resultado['total_geral'], '0.00')
        self.assertEqual(resultado['quantidade_lancamentos'], 0)
        self.assertEqual(len(resultado['por_categoria']), 0)

    def test_lancamentos_normais(self):
        despesas = [
            {'categoria': 'Alimentação', 'valor': '150.50'},
            {'categoria': 'Moradia', 'valor': '800.00'},
            {'categoria': 'Alimentação', 'valor': '75.25'},
            {'categoria': 'Transporte', 'valor': '100.75'},
            {'categoria': 'Moradia', 'valor': '900.00'}
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['total_geral'], '1926.50')
        self.assertEqual(resultado['quantidade_lancamentos'], 5)
        self.assertEqual(resultado['por_categoria'][0]['categoria'], 'Moradia')
        self.assertEqual(resultado['por_categoria'][0]['total'], '1700.00')
        self.assertEqual(resultado['por_categoria'][0]['quantidade'], 2)
        self.assertEqual(resultado['por_categoria'][1]['categoria'], 'Alimentação')
        self.assertEqual(resultado['por_categoria'][1]['total'], '225.75')
        self.assertEqual(resultado['por_categoria'][1]['quantidade'], 2)
        self.assertEqual(resultado['por_categoria'][2]['categoria'], 'Transporte')
        self.assertEqual(resultado['por_categoria'][2]['total'], '100.75')
        self.assertEqual(resultado['por_categoria'][2]['quantidade'], 1)

    def test_lancamentos_com_espacos(self):
        despesas = [
            {'categoria': '  Alimentação  ', 'valor': '150.50'},
            {'categoria': 'Moradia', 'valor': '800.00'}
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['total_geral'], '950.50')
        self.assertEqual(resultado['quantidade_lancamentos'], 2)

    def test_lancamentos_invalidos(self):
        despesas = [
            {'categoria': 'Alimentação', 'valor': '-150.50'},  # Valor negativo
            {'categoria': 'Moradia', 'valor': '800.00'},
            {'categoria': 'Transporte', 'valor': 'abc'}  # Valor não numérico
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['total_geral'], '800.00')
        self.assertEqual(resultado['quantidade_lancamentos'], 2)

    def test_empate_em_categoria(self):
        despesas = [
            {'categoria': 'Alimentação', 'valor': '100.00'},
            {'categoria': 'Alimentação', 'valor': '50.00'},
            {'categoria': 'Moradia', 'valor': '200.00'}
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['total_geral'], '350.00')
        self.assertEqual(resultado['quantidade_lancamentos'], 3)
        self.assertEqual(resultado['por_categoria'][0]['categoria'], 'Alimentação')
        self.assertEqual(resultado['por_categoria'][0]['total'], '150.00')
        self.assertEqual(resultado['por_categoria'][0]['quantidade'], 2)
        self.assertEqual(resultado['por_categoria'][1]['categoria'], 'Moradia')
        self.assertEqual(resultado['por_categoria'][1]['total'], '200.00')
        self.assertEqual(resultado['por_categoria'][1]['quantidade'], 1)


if __name__ == '__main__':
    unittest.main()
