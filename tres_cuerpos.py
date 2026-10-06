"""Tres masas unitarias en un plano, G=1 e integración RK4."""

import argparse
import csv
from dataclasses import dataclass
import json
import math
from pathlib import Path

PERIODO = 6.32591398
DISTANCIA_MINIMA = 1e-6
MAX_PASOS = 100_000


@dataclass(frozen=True)
class Muestra:
    tiempo: float
    estado: tuple[float, ...]  # x, y, vx, vy para cada cuerpo


def inicial(perturbacion=0.0):
    """Perturba vx de los cuerpos 1 y 3 conservando el momento total."""
    if not math.isfinite(perturbacion):
        raise ValueError("La perturbación debe ser finita")
    return (0.97000436, -0.24308753, 0.466203685 + perturbacion, 0.432365730,
            -0.97000436, 0.24308753, 0.466203685, 0.432365730,
            0.0, 0.0, -0.93240737 - perturbacion, -0.86473146)


def derivada(estado):
    """Velocidades y aceleraciones newtonianas; suma por parejas."""
    if len(estado) != 12 or not all(math.isfinite(v) for v in estado):
        raise ValueError("El estado debe contener 12 números finitos")
    resultado = [0.0] * 12
    for i in range(3):
        resultado[4*i:4*i+2] = estado[4*i+2:4*i+4]
        for j in range(i+1, 3):
            dx = estado[4*j] - estado[4*i]
            dy = estado[4*j+1] - estado[4*i+1]
            distancia = math.hypot(dx, dy)
            if distancia <= DISTANCIA_MINIMA:
                raise ValueError("Cuerpos demasiado próximos: reduce el paso o cambia las condiciones")
            factor = 1.0 / distancia**3
            for eje, componente in enumerate((dx, dy)):
                aceleracion = componente * factor
                resultado[4*i+2+eje] += aceleracion
                resultado[4*j+2+eje] -= aceleracion
    return tuple(resultado)


def paso_rk4(estado, dt):
    """Promedio ponderado de cuatro evaluaciones de la derivada."""
    k1 = derivada(estado)
    k2 = derivada(tuple(y + dt*k/2 for y, k in zip(estado, k1)))
    k3 = derivada(tuple(y + dt*k/2 for y, k in zip(estado, k2)))
    k4 = derivada(tuple(y + dt*k for y, k in zip(estado, k3)))
    siguiente = tuple(y + dt*(a + 2*b + 2*c + d)/6
                      for y, a, b, c, d in zip(estado, k1, k2, k3, k4))
    if not all(math.isfinite(v) for v in siguiente):
        raise ValueError("La integración produjo valores no finitos")
    return siguiente


def simular(duracion=PERIODO, dt=0.002, perturbacion=0.0):
    """Incluye t=0 y el instante final exacto con un último paso menor."""
    if not math.isfinite(duracion) or duracion <= 0:
        raise ValueError("La duración debe ser positiva y finita")
    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("El paso debe ser positivo y finito")
    if dt > duracion:
        raise ValueError("El paso no puede superar la duración")
    cociente = duracion / dt
    if not math.isfinite(cociente) or cociente > MAX_PASOS:
        raise ValueError(f"La simulación admite como máximo {MAX_PASOS} pasos")
    pasos = math.ceil(cociente)
    estado = inicial(perturbacion)
    muestras = [Muestra(0.0, estado)]
    for n in range(1, pasos+1):
        tiempo = min(n*dt, duracion)
        estado = paso_rk4(estado, tiempo - muestras[-1].tiempo)
        muestras.append(Muestra(tiempo, estado))
    return muestras


def invariantes(estado):
    """Energía, momento lineal (px, py) y momento angular escalar."""
    derivada(estado)  # Valida el estado y rechaza singularidades.
    energia = sum((estado[i+2]**2 + estado[i+3]**2)/2 for i in (0, 4, 8))
    for i in range(3):
        for j in range(i+1, 3):
            energia -= 1/math.hypot(estado[4*j]-estado[4*i], estado[4*j+1]-estado[4*i+1])
    px = sum(estado[i+2] for i in (0, 4, 8))
    py = sum(estado[i+3] for i in (0, 4, 8))
    angular = sum(estado[i]*estado[i+3]-estado[i+1]*estado[i+2] for i in (0, 4, 8))
    return energia, px, py, angular


def diagnostico(muestras):
    referencia = invariantes(muestras[0].estado)
    errores = [0.0]*4
    for muestra in muestras:
        valores = invariantes(muestra.estado)
        errores = [max(e, abs(v-r)) for e, v, r in zip(errores, valores, referencia)]
    return {"error_relativo_energia": errores[0]/abs(referencia[0]),
            "error_momento_lineal": math.hypot(errores[1], errores[2]),
            "error_momento_angular": errores[3]}


def exportar_csv(muestras, archivo):
    with Path(archivo).open('w', newline='', encoding='utf-8') as salida:
        escritor = csv.writer(salida)
        escritor.writerow(['t'] + [f'{v}{i}' for i in range(1, 4) for v in ('x', 'y', 'vx', 'vy')])
        escritor.writerows((m.tiempo, *m.estado) for m in muestras)


def exportar_html(original, perturbada, archivo):
    """Animación independiente, limitada a 2001 muestras para la presentación."""
    salto = max(1, math.ceil((len(original)-1)/2000))
    indices = list(range(0, len(original)-1, salto)) + [len(original)-1]
    datos = [[[muestras[i].tiempo, *muestras[i].estado] for i in indices]
             for muestras in (original, perturbada)]
    plantilla = Path(__file__).with_name('animacion.html').read_text(encoding='utf-8')
    Path(archivo).write_text(plantilla.replace('__DATOS__', json.dumps(datos, allow_nan=False)), encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description='El problema de los tres cuerpos: órbita en ocho y perturbación')
    parser.add_argument('--duracion', type=float, default=2*PERIODO)
    parser.add_argument('--dt', type=float, default=0.002)
    parser.add_argument('--perturbacion', type=float, default=0.01)
    parser.add_argument('--salida', type=Path, default=Path('outputs'))
    args = parser.parse_args(argv)
    try:
        original = simular(args.duracion, args.dt)
        perturbada = simular(args.duracion, args.dt, args.perturbacion)
        args.salida.mkdir(parents=True, exist_ok=True)
        exportar_csv(original, args.salida/'original.csv')
        exportar_csv(perturbada, args.salida/'perturbada.csv')
        exportar_html(original, perturbada, args.salida/'orbita.html')
        informe = {'duracion': args.duracion, 'dt': args.dt, 'perturbacion': args.perturbacion,
                   'pasos': len(original)-1, 'original': diagnostico(original),
                   'perturbada': diagnostico(perturbada)}
        (args.salida/'diagnostico.json').write_text(json.dumps(informe, indent=2)+'\n', encoding='utf-8')
    except (ValueError, OverflowError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(informe, indent=2))
    print(f"Abre {(args.salida/'orbita.html').resolve()} en tu navegador")


if __name__ == '__main__':
    main()
