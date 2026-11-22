import unittest
from despesas import resumir_despesas

class TestResumirDespesas(unittest.TestCase):

    def test_lista_vazia(self):
        resultado = resumir_despesas([])
        self.assertEqual(resultado['total_geral'], '0.00')
        self.assertEqual(resultado['quantidade_lancamentos'], '0')
        self.assertEqual(resultado['por_categoria'], [])

    def test_lancamentos_validos(self):
        despesas = [
            {'categoria': 'Alimentação', 'valor': '150.50'},
            {'categoria': 'Transporte', 'valor': '75.25'},
            {'categoria': 'Alimentação', 'valor': '25.75'},
            {'categoria': 'Moradia', 'valor': '300.00'},
            {'categoria': 'Transporte', 'valor': '100.00'}
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['total_geral'], '601.50')
        self.assertEqual(resultado['quantidade_lancamentos'], '5')
        self.assertEqual(resultado['por_categoria'][0]['categoria'], 'Alimentação')
        self.assertEqual(resultado['por_categoria'][0]['total'], '176.25')
        self.assertEqual(resultado['por_categoria'][0]['quantidade'], '2')
        self.assertEqual(resultado['por_categoria'][1]['categoria'], 'Transporte')
        self.assertEqual(resultado['por_categoria'][1]['total'], '175.25')
        self.assertEqual(resultado['por_categoria'][1]['quantidade'], '2')
        self.assertEqual(resultado['por_categoria'][2]['categoria'], 'Moradia')
        self.assertEqual(resultado['por_categoria'][2]['total'], '300.00')
        self.assertEqual(resultado['por_categoria'][2]['quantidade'], '1')

    def test_lancamentos_invalidos(self):
        despesas = [
            {'categoria': 'Alimentação', 'valor': '-150.50'},  # Valor negativo
            {'categoria': 'Transporte', 'valor': 'abc'},  # Valor não numérico
            {'categoria': 'Moradia', 'valor': '300.00'},
            {'categoria': 'Transporte', 'valor': '100.00'}
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['total_geral'], '400.00')
        self.assertEqual(resultado['quantidade_lancamentos'], '4')

    def test_empate_categorias(self):
        despesas = [
            {'categoria': 'Alimentação', 'valor': '100.00'},
            {'categoria': 'Transporte', 'valor': '100.00'}
        ]
        resultado = resumir_despesas(despesas)
        self.assertEqual(resultado['por_categoria'][0]['categoria'], 'Alimentação')
        self.assertEqual(resultado['por_categoria'][0]['total'], '100.00')
        self.assertEqual(resultado['por_categoria'][0]['quantidade'], '1')
        self.assertEqual(resultado['por_categoria'][1]['categoria'], 'Transporte')
        self.assertEqual(resultado['por_categoria'][1]['total'], '100.00')
        self.assertEqual(resultado['por_categoria'][1]['quantidade'], '1')

if __name__ == '__main__':
    unittest.main()
