# Proceso con Codex

Resumen de las acciones realizadas en esta conversación, no una transcripción.

1. El usuario indicó una carpeta vacía y pidió un repo GitHub y una PR mediante `gh`.
2. Tras una primera propuesta sencilla, pidió un problema matemático más complejo. Se eligió la simulación del problema de los tres cuerpos.
3. Codex consultó la publicación original de la órbita en ocho para fijar las condiciones iniciales y el periodo.
4. Codex creó el enunciado, el prompt, el contrato del simulador y el workflow de tests.
5. Se ejecutó `git init -b main`. Un permiso adicional para `.git` permitió completar la inicialización.
6. La base se guarda en un commit y se publica con `gh repo create contracamilo/codex-tres-cuerpos --public --source=. --remote=origin --push`.

La implementación, las pruebas y la documentación de la solución se añadirán en una rama independiente y una PR abierta.

## Implementación en la rama

- Rama: `codex/solucion-tres-cuerpos`.
- Codex implementó las fuerzas newtonianas, RK4, la exportación CSV, la animación y los diagnósticos.
- Añadió tests de física, convergencia, validación y consola.
- La ejecución local en Python 3.14.4 superó los 12 tests.
- La demo por defecto realizó 6326 pasos por simulación. Error relativo máximo de energía observado: aproximadamente 2.31e-12 en la original y 3.29e-12 en la perturbada. Son resultados de esta ejecución, no garantías para cualquier parámetro.
- Los commits de esta demo no llevan firma GPG: la configuración global solicitaba un recurso fuera del entorno permitido y se desactivó la firma solo en cada comando de commit, sin cambiar la configuración global.

Comandos para publicar la solución:

```bash
git push -u origin codex/solucion-tres-cuerpos
gh pr create --base main --head codex/solucion-tres-cuerpos --title "Simular el problema de los tres cuerpos con RK4 y una animación" --body-file /ruta/al/texto-de-la-pr.md
```

La PR queda abierta para que el equipo pueda revisar la implementación antes de integrarla.
