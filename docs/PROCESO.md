# Proceso con Codex

Resumen de las acciones realizadas en esta conversación, no una transcripción.

1. El usuario indicó una carpeta vacía y pidió un repo GitHub y una PR mediante `gh`.
2. Tras una primera propuesta sencilla, pidió un problema matemático más complejo. Se eligió la simulación del problema de los tres cuerpos.
3. Codex consultó la publicación original de la órbita en ocho para fijar las condiciones iniciales y el periodo.
4. Codex creó el enunciado, el prompt, el contrato del simulador y el workflow de tests.
5. Se ejecutó `git init -b main`. Un permiso adicional para `.git` permitió completar la inicialización.
6. La base se guarda en un commit y se publica con `gh repo create contracamilo/codex-tres-cuerpos --public --source=. --remote=origin --push`.

La implementación, las pruebas y la documentación de la solución se añadirán en una rama independiente y una PR abierta.
