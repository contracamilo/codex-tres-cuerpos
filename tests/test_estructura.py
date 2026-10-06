import unittest
from tres_cuerpos import PERIODO, simular


class TestEstructura(unittest.TestCase):
    def test_contrato_disponible(self):
        self.assertTrue(callable(simular))
        self.assertGreater(PERIODO, 0)
