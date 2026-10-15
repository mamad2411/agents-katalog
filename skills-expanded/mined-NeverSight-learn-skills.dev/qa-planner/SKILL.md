---
name: qa-planner
description: Diseña suites de prueba, cobertura y precondiciones estructurales y entrega el reporte `QA.planner-execution-summary.md`.
disable-model-invocation: true
argument-hint: "documentación con requisitos consolidados, dependencias y gaps. Opcional: 'to <path>' para destino, o 'preview'/'no-save' para chat-only."
compatibility: 
  - agents: [QA.planner]
---

## Mapa de pasos

DEBES leer y ejecutar los pasos de la carpeta `steps/` en este orden:

1. `steps/01-analisis-de-handoff-de-entrada.md` — Análisis de Handoff de Entrada
2. `steps/02-diseno-de-suites.md` — Diseño de Suites
3. `steps/03-modelamiento-de-cobertura.md` — Modelamiento de Cobertura
4. `steps/04-definicion-de-precondiciones.md` — Definición de Precondiciones
5. `steps/05-trazabilidad-estructural.md` — Trazabilidad Estructural
6. `steps/06-generacion-de-handoff-y-reporte.md` — Generación de Reporte

## Feedback al usuario

- Mientras ejecutas cada paso: salvo que el usuario indique lo contrario, escribe en el chat solo para reportar errores o decisiones pendientes; de lo contrario, mantén silencio.
- Cuando termines cada paso: responde en chat **exactamente una línea seca** con el formato `<nombre-del-paso> OK.`
- Cuando termines de escribir archivos: responde en chat **exactamente una línea seca** con el formato `<nombre-del-workflow> OK; reporte: <ruta a archivos generados>`;
