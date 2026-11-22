import unittest
from despesas import resumir_despesas

class TestResumirDespesas(unittest.TestCase):
    def test_caso_normal(self):
        lancamentos = [
            {'categoria': 'Alimentos', 'valor': '10.50'},
            {'categoria': 'Alimentos', 'valor': '20.00'},
            {'categoria': 'Transporte', 'valor': '15.75'},
            {'categoria': 'Alimentos', 'valor': '5.25'}
        ]
        resultado = resumir_despesas(lancamentos)
        self.assertEqual(resultado, {
            'total_geral': '41.50',
            'quantidade_lancamentos': 4,
            'por_categoria': [
                {'categoria': 'Alimentos', 'total': '36.00', 'quantidade': 3},
                {'categoria': 'Transporte', 'total': '15.75', 'quantidade': 1}
            ]
        })

    def test_lista_vazia(self):
        lancamentos = []
        resultado = resumir_despesas(lancamentos)
        self.assertEqual(resultado, {
            'total_geral': '0.00',
            'quantidade_lancamentos': 0,
            'por_categoria': []
        })

    def test_valores_inválidos(self):
        lancamentos = [
            {'categoria': 'Alimentos', 'valor': 'abc'},
            {'categoria': '', 'valor': '10.00'},
            {'categoria': 'Alimentos', 'valor': '-5.00'}
        ]
        with self.assertRaises(ValueError):
            resumir_despesas(lancamentos)

    def test_empate(self):
        lancamentos = [
            {'categoria': 'Alimentos', 'valor': '10.00'},
            {'categoria': 'Alimentos', 'valor': '10.00'},
            {'categoria': 'Transporte', 'valor': '10.00'},
            {'categoria': 'Alimentos', 'valor': '10.00'}
        ]
        resultado = resumir_despesas(lancamentos)
        self.assertEqual(resultado, {
            'total_geral': '40.00',
            'quantidade_lancamentos': 4,
            'por_categoria': [
                {'categoria': 'Alimentos', 'total': '40.00', 'quantidade': 4},
                {'categoria': 'Transporte', 'total': '10.00', 'quantidade': 1}
            ]
        })

if __name__ == '__main__':
    unittest.main()
