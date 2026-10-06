import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tres_cuerpos import (PERIODO, derivada, diagnostico, inicial,
                           invariantes, simular)


class TestFisica(unittest.TestCase):
    def test_fuerzas_contra_caso_analitico(self):
        estado = (-1., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.)
        d = derivada(estado)
        self.assertAlmostEqual(d[2], 1.25)
        self.assertAlmostEqual(d[6], 0.0)
        self.assertAlmostEqual(d[10], -1.25)
        self.assertTrue(all(d[i] == 0 for i in (3, 7, 11)))

    def test_energia_inicial_y_momento(self):
        e, px, py, angular = invariantes(inicial())
        self.assertAlmostEqual(e, -1.287, delta=0.001)
        self.assertAlmostEqual(px, 0.0)
        self.assertAlmostEqual(py, 0.0)
        self.assertAlmostEqual(angular, 0.0)
        self.assertAlmostEqual(invariantes(inicial(0.01))[1], 0.0)

    def test_conservacion_durante_un_periodo(self):
        muestras = simular()
        errores = diagnostico(muestras)
        self.assertLess(errores['error_relativo_energia'], 1e-8)
        self.assertLess(errores['error_momento_lineal'], 1e-12)
        self.assertLess(errores['error_momento_angular'], 1e-8)
        for m in muestras:
            self.assertLess(abs(sum(m.estado[i] for i in (0, 4, 8))), 1e-11)
            self.assertLess(abs(sum(m.estado[i] for i in (1, 5, 9))), 1e-11)

    def test_retorno_tras_un_periodo(self):
        final = simular()[-1].estado
        self.assertLess(max(abs(a-b) for a, b in zip(final, inicial())), 1e-6)

    def test_convergencia_rk4_con_referencia_mas_fina(self):
        referencia = simular(1.0, 0.00125)[-1].estado
        gruesa = simular(1.0, 0.02)[-1].estado
        fina = simular(1.0, 0.01)[-1].estado
        error_gruesa = math.dist(gruesa, referencia)
        error_fina = math.dist(fina, referencia)
        self.assertGreater(error_gruesa/error_fina, 12)
        self.assertLess(error_gruesa/error_fina, 20)

    def test_perturbacion_cambia_trayectoria(self):
        self.assertGreater(math.dist(simular(1)[-1].estado,
                                     simular(1, perturbacion=0.01)[-1].estado), 0.001)

    def test_instante_final_y_paso_incompleto(self):
        muestras = simular(0.1, 0.03)
        self.assertEqual(len(muestras), 5)
        self.assertEqual(muestras[0].tiempo, 0)
        self.assertEqual(muestras[-1].tiempo, 0.1)
        self.assertTrue(all(a.tiempo < b.tiempo for a, b in zip(muestras, muestras[1:])))

    def test_parametros_invalidos(self):
        for parametros in ({'dt': 0}, {'dt': -1}, {'dt': float('nan')},
                           {'duracion': 0}, {'duracion': float('inf')},
                           {'perturbacion': float('nan')}, {'dt': 10},
                           {'dt': 1e-10}):
            with self.subTest(parametros=parametros), self.assertRaises(ValueError):
                simular(**parametros)

    def test_colision_y_estado_invalido(self):
        for estado in ((0.,)*12, (0.,)*11, (float('nan'),)*12):
            with self.subTest(estado=estado), self.assertRaises(ValueError):
                derivada(estado)


class TestConsola(unittest.TestCase):
    def test_exportacion_completa(self):
        with tempfile.TemporaryDirectory() as temporal:
            resultado = subprocess.run([sys.executable, 'tres_cuerpos.py', '--duracion', '0.1',
                                        '--dt', '0.01', '--salida', temporal],
                                       capture_output=True, text=True)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            ruta = Path(temporal)
            self.assertEqual(len((ruta/'original.csv').read_text().splitlines()), 12)
            self.assertEqual(len((ruta/'perturbada.csv').read_text().splitlines()), 12)
            html = (ruta/'orbita.html').read_text()
            self.assertNotIn('__DATOS__', html)
            self.assertNotIn('src="http', html)
            self.assertIn('const datos=[', html)
            informe = json.loads((ruta/'diagnostico.json').read_text())
            self.assertEqual(informe['pasos'], 10)
            self.assertLess(informe['original']['error_relativo_energia'], 1e-8)

    def test_error_de_consola_sin_traza(self):
        resultado = subprocess.run([sys.executable, 'tres_cuerpos.py', '--dt', '-1'],
                                   capture_output=True, text=True)
        self.assertEqual(resultado.returncode, 2)
        self.assertIn('El paso debe ser positivo', resultado.stderr)
        self.assertNotIn('Traceback', resultado.stderr)


if __name__ == '__main__':
    unittest.main()
