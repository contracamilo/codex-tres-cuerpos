# Flujo de trabajo con Codex

Este documento propone un proceso para incorporar Codex al desarrollo de software en un equipo profesional. La simulación de tres cuerpos sirve como ejemplo de los entregables y las comprobaciones de cada etapa. No es un registro de aprobaciones ni acredita que un equipo haya realizado todas las etapas descritas.

## 1. Definición del problema

La persona responsable de la tarea describe la necesidad, el resultado esperado y las restricciones. Codex puede ayudar a aclarar requisitos y detectar ambigüedades antes de modificar código.

En este proyecto, el objetivo es reproducir numéricamente una órbita en ocho y compararla con una variante perturbada. El alcance incluye la simulación, la exportación de datos y una animación local. Quedan fuera una solución analítica general, la relatividad y el tratamiento de colisiones físicas.

**Entregable:** [enunciado y criterios de aceptación](PROBLEMA.md), con una definición explícita de qué significa completar la tarea.

## 2. Investigación y planificación

Codex examina el proyecto, sus instrucciones y las fuentes relevantes. A partir de ese contexto, propone un plan que identifica los archivos afectados, las decisiones técnicas, los riesgos y las comprobaciones necesarias.

Para esta simulación, el plan de referencia es:

1. Verificar las ecuaciones, las condiciones iniciales y su fuente.
2. Implementar las fuerzas por parejas y el integrador RK4.
3. Incorporar validación de entradas y diagnósticos físicos.
4. Generar CSV y una animación HTML autocontenida.
5. Comprobar conservación, retorno aproximado y convergencia.
6. Documentar la ejecución y preparar una PR revisable.

Las restricciones son Python 3.11 o superior y solo la biblioteca estándar. Los principales riesgos son el error numérico, los encuentros cercanos y una interpretación incorrecta de la comparación entre trayectorias.

**Punto de revisión:** la persona responsable contrasta el plan con el alcance y resuelve las decisiones que afecten a arquitectura, dependencias o criterios de aceptación antes de implementar.

**Referencias:** [matemáticas y límites del método en la rama de la demo](https://github.com/contracamilo/codex-tres-cuerpos/blob/codex/solucion-tres-cuerpos/docs/MATEMATICAS.md) e [instrucciones del proyecto](../AGENTS.md).

## 3. Preparación del entorno

El equipo establece la rama de trabajo, los comandos de comprobación y los límites de acceso. Codex trabaja con los archivos y herramientas necesarios para la tarea, conforme a las políticas del proyecto.

En esta demo, `main` conserva el enunciado y el contrato inicial. La implementación se desarrolla en `codex/solucion-tres-cuerpos`. GitHub Actions ejecuta las comprobaciones en Python 3.11 y 3.14.

**Entregable:** un punto de partida reproducible y una rama que permita revisar los cambios de forma independiente.

## 4. Implementación incremental

Codex ejecuta el encargo dentro del alcance acordado. La persona responsable puede dirigir el trabajo, aclarar requisitos y revisar resultados parciales. Si aparece una decisión que cambia el alcance, el equipo actualiza el plan y los criterios de aceptación.

La implementación debe mantener una relación clara entre requisitos y cambios: el cálculo de fuerzas responde al modelo físico, RK4 al método de integración y los archivos exportados al resultado que necesita el usuario.

**Entregables:** código, pruebas y documentación coherentes con el enunciado. El [encargo reproducible](PROMPT.md) recoge el objetivo, las restricciones y las evidencias esperadas.

## 5. Verificación y evidencias

Codex ejecuta las comprobaciones disponibles y comunica qué ha verificado, los resultados y las limitaciones. El equipo evalúa esas evidencias frente a los criterios de aceptación.

| Aspecto | Evidencia en esta demo |
|---|---|
| Fuerzas gravitatorias | Contraste con un caso analítico sencillo |
| Conservación física | Energía, momentos y centro de masas durante la simulación |
| Órbita en ocho | Retorno aproximado tras el periodo de referencia |
| Precisión del integrador | Convergencia al reducir el paso temporal |
| Uso desde consola | Exportación de archivos y tratamiento de entradas inválidas |
| Resultado visual | Revisión de la animación y sus controles en el navegador |
| Reproducibilidad | Ejecución automática de tests en dos versiones de Python |

Comando de comprobación:

```bash
python3 -m unittest discover -s tests -v
```

La ejecución local de referencia superó los 12 tests en Python 3.14.4. Para la demo por defecto, con 6326 pasos y `dt=0.002`, el máximo error relativo de energía observado fue aproximadamente `2.31e-12` en la órbita original y `3.29e-12` en la perturbada. Estos resultados corresponden a esa ejecución y no garantizan precisión para cualquier parámetro.

Los tests y la inspección visual aportan evidencias complementarias. La animación por sí sola no valida la física ni demuestra caos.

## 6. Pull request y revisión humana

Codex prepara una PR que explica el problema, el comportamiento resultante, las decisiones relevantes y las comprobaciones realizadas. El equipo revisa el código y las evidencias, solicita ajustes cuando sea necesario y decide si el cambio cumple los criterios de aceptación.

La revisión debe considerar especialmente la corrección del modelo, las tolerancias de los tests, los límites de RK4 y la claridad de los mensajes de error. Los checks automáticos apoyan la revisión; la responsabilidad de aceptar el cambio corresponde al equipo.

**Entregable:** una PR con cambios acotados y evidencia suficiente para tomar una decisión. La PR de esta demo permanece abierta para revisión.

## 7. Integración y seguimiento

En un proyecto profesional, la integración se realiza conforme a las reglas del repositorio: revisiones requeridas, checks y políticas de publicación. Tras integrar, el equipo verifica el comportamiento en el entorno de destino y registra cualquier trabajo pendiente.

Esta demo termina en la PR abierta. No representa una aprobación del equipo, una integración en `main` ni un despliegue en producción.

## Responsabilidades

La persona responsable define la necesidad y valida el alcance. Codex ayuda a investigar, planificar, implementar y reunir evidencias. Quienes revisan evalúan el resultado y autorizan su integración según el proceso del equipo.

El objetivo es incorporar la asistencia de Codex a un proceso trazable, con requisitos claros y resultados comprobables.
