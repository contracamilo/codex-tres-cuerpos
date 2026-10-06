# Codex: tres cuerpos: el problema de los tres cuerpos

**Tres cuerpos, una ley de gravedad. ¿Podemos reproducir una órbita en forma de ocho?**

Demo de Codex desde una carpeta vacía hasta una pull request con Python, pruebas y una animación.

## Punto de partida

Esta rama `main` contiene el reto y el contrato del simulador. La implementación permanece en una PR abierta para que los asistentes puedan revisar el cambio.

1. Lee [el problema](docs/PROBLEMA.md).
2. Consulta [el encargo reproducible](docs/PROMPT.md).
3. En **Pull requests**, abre la solución y revisa **Files changed** y **Checks**.
4. Sigue las instrucciones de ejecución del README de la PR.
5. Consulta [el proceso](docs/PROCESO.md) para ver cómo se preparó la demo.

Requisito: Python 3.11 o superior. Sin dependencias externas.

```bash
python3 -m unittest discover -s tests -v
```

La comprobación inicial solo verifica que existe el contrato. Todavía no valida la física.
