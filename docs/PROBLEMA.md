# El problema de los tres cuerpos

## Reto

Simular tres masas iguales que se atraen por gravedad en un plano. Reproducir la órbita periódica en forma de ocho y comparar con una perturbación de las velocidades iniciales.

Unidades normalizadas: G = 1 y cada masa = 1.

Para cada cuerpo i:

`aceleración_i = suma((posición_j - posición_i) / distancia_ij³)` para j distinto de i.

Integra posiciones y velocidades con Runge-Kutta de cuarto orden (RK4), usando un paso temporal configurable.

## Condiciones iniciales

| Cuerpo | x | y | vx | vy |
|---|---:|---:|---:|---:|
| 1 | 0.97000436 | -0.24308753 | 0.466203685 | 0.432365730 |
| 2 | -0.97000436 | 0.24308753 | 0.466203685 | 0.432365730 |
| 3 | 0 | 0 | -0.93240737 | -0.86473146 |

Periodo aproximado: 6.32591398 unidades de tiempo.

Fuente: Chenciner y Montgomery, *Annals of Mathematics* 152 (2000), figura 1. Condiciones calculadas por Carles Simó.
https://www.maths.tcd.ie/EMIS/journals/Annals/152_3/chencine.pdf

## Criterios de aceptación

- Simulación reproducible en Python sin dependencias externas.
- Exportación CSV y animación HTML autocontenida que abra sin servidor.
- Comparación visual de la órbita original y una perturbación configurable.
- Informe del error relativo de energía y de los momentos lineal y angular.
- Tests de fuerza, conservación, retorno aproximado tras un periodo y convergencia al reducir el paso.
- Errores claros para entradas inválidas y cuerpos demasiado próximos.
- Comando de demo sencillo y documentación del razonamiento.

## Límites

Es una aproximación numérica de un caso particular, no una solución analítica general. La órbita en ocho es una solución especial: variar sus condiciones no garantiza caos ni separación espectacular en cualquier intervalo. RK4 no conserva energía exactamente. El paso fijo no es adecuado para encuentros muy cercanos o simulaciones arbitrariamente largas. Las masas son puntos, sin relatividad ni colisiones físicas.
