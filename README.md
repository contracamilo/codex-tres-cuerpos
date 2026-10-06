# Codex: tres cuerpos: el problema de los tres cuerpos

**Tres cuerpos, una ley de gravedad. ¿Podemos reproducir una órbita en forma de ocho?**

Demo preparada con Codex desde una carpeta vacía hasta una PR revisable. Python calcula las trayectorias y genera una animación local con la órbita original y una variante perturbada.

## Ejecución rápida

Python 3.11 o superior. Solo biblioteca estándar: no hay que instalar paquetes.

```bash
git clone https://github.com/contracamilo/codex-tres-cuerpos.git
cd codex-tres-cuerpos
git switch codex/solucion-tres-cuerpos
python3 -m unittest discover -s tests -v
python3 tres_cuerpos.py
```

Abre `outputs/orbita.html` en cualquier navegador moderno. Puedes pausar, reiniciar o mover el control de tiempo. Las dos vistas comparten escala. El archivo funciona sin conexión y sin servidor.

La ejecución por defecto integra dos periodos aproximados con `dt=0.002`, y cambia `vx` en 0.01 para el primer cuerpo y -0.01 para el tercero. Así conserva el momento lineal inicial. La perturbación sí cambia la energía y el momento angular iniciales: el informe compara cada simulación con sus propios valores iniciales.

```bash
python3 tres_cuerpos.py --duracion 20 --dt 0.002 --perturbacion 0.03
python3 tres_cuerpos.py --help
```

Los archivos se escriben en `outputs/` (ignorado por Git). Puedes elegir otro directorio con `--salida`. Repetir la ejecución en el mismo directorio reemplaza esos archivos.

| Archivo | Contenido |
|---|---|
| `orbita.html` | Animación autocontenida, hasta 2001 instantes |
| `original.csv` | Tiempo, posiciones y velocidades de la órbita original |
| `perturbada.csv` | Datos de la órbita perturbada |
| `diagnostico.json` | Parámetros y errores de conservación |

## Cómo revisar la demo en GitHub

`main` conserva el contrato inicial. La rama `codex/solucion-tres-cuerpos` incorpora la implementación. Abre la PR en **Pull requests**:

- **Commits** muestra la evolución de la solución.
- **Files changed** permite revisar la física, el integrador, los tests y la documentación.
- **Checks** ejecuta los tests en Python 3.11 y 3.14.

Consulta [el enunciado](docs/PROBLEMA.md), [el prompt](docs/PROMPT.md), [las matemáticas](docs/MATEMATICAS.md), [el proceso](docs/PROCESO.md).

## Verificación y límites

Los tests contrastan las fuerzas con un caso analítico sencillo, verifican el retorno aproximado tras un periodo, la conservación de energía y momentos, y la convergencia de RK4. También prueban entradas inválidas y exportación desde la consola.

La animación representa una aproximación numérica, no una solución analítica general. La órbita en ocho es un caso especial. Una perturbación no garantiza caos en el intervalo mostrado. RK4 con paso fijo puede perder precisión en encuentros cercanos y tiempos largos; el umbral de proximidad detiene evaluaciones singulares, pero no detecta todas las colisiones entre pasos. No se usa suavizado de la gravedad.

Límite práctico: 100 000 pasos por simulación. El tamaño y la escala de los números deben ser razonables para la aritmética de coma flotante.

## Fuente matemática

Alain Chenciner y Richard Montgomery, *A remarkable periodic solution of the three-body problem in the case of equal masses*, Annals of Mathematics 152 (2000), 881–901. Figura 1: condiciones iniciales calculadas por Carles Simó.

[Publicación original](https://www.maths.tcd.ie/EMIS/journals/Annals/152_3/chencine.pdf)
