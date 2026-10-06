# Matemáticas de la simulación

## Modelo

Cada cuerpo tiene posición `r_i = (x_i, y_i)` y velocidad `v_i`. Usamos masas unitarias y G = 1. La gravedad da:

`dr_i/dt = v_i`

`dv_i/dt = suma_j≠i (r_j - r_i) / ||r_j - r_i||³`

El estado reúne 12 valores: x, y, vx y vy de cada uno de los tres cuerpos. La función `derivada` devuelve sus tasas de cambio. Calculamos las fuerzas por parejas y aplicamos contribuciones opuestas, siguiendo la tercera ley de Newton.

## Integración RK4

Para avanzar el estado y un paso h:

```
k1 = f(y)
k2 = f(y + h*k1/2)
k3 = f(y + h*k2/2)
k4 = f(y + h*k3)
y_siguiente = y + h*(k1 + 2*k2 + 2*k3 + k4)/6
```

En una trayectoria suficientemente suave y un intervalo fijo, el error global es de orden h⁴. Reducir h a la mitad debería disminuirlo aproximadamente por un factor 16. El test compara pasos 0.02 y 0.01 contra una referencia numérica con paso 0.00125 durante una unidad de tiempo. Esta referencia también tiene error y no constituye una solución exacta.

## Conservación física

```
E = suma_i ||v_i||²/2 - suma_i<j 1/||r_i-r_j||
P = suma_i v_i
L = suma_i (x_i*vy_i - y_i*vx_i)
```

El informe calcula el máximo cambio respecto al estado inicial en todas las muestras de cada simulación. El error energético se divide por |E_inicial|. Para P se informa una cota conservadora que combina los máximos cambios de sus dos componentes. RK4 no conserva estos valores exactamente.

## Órbita en ocho

Las condiciones y el periodo aproximado vienen de la figura 1 del artículo citado en el enunciado. Verificamos que el estado regresa aproximadamente al punto de partida tras 6.32591398 unidades de tiempo. Las constantes publicadas están redondeadas: no se debe exigir coincidencia exacta.

## Perturbación

Cambiamos vx del cuerpo 1 en +δ y vx del cuerpo 3 en -δ. Conservamos el momento lineal inicial, pero cambiamos la energía y el momento angular. Esto permite comparar trayectorias cercanas sin añadir una traslación neta del centro de masas.

La separación observada no prueba por sí sola caos. Tampoco presentamos esta órbita especial como representativa de todas las configuraciones de tres cuerpos.
