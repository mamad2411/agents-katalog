---
name: qa-documentation
description: Extrae, normaliza y entrega requisitos QA consolidados en un analysis-report markdown.
disable-model-invocation: true
argument-hint: "solicitud QA y fuentes de requisitos. Opcional: 'to <path>' para destino, o 'preview'/'no-save' para chat-only."
compatibility: 
  - agents: [QA.documentation]
---

## Mapa de pasos

DEBES leer y ejecutar los pasos de `steps/` en este orden:

1. `steps/01-extraccion-de-requisitos.md` — Extracción de Requisitos
2. `steps/02-identificacion-de-gaps.md` — Identificación de Gaps
3. `steps/03-particionado-por-area.md` — Particionado por Área
4. `steps/04-normalizacion-y-estructuracion.md` — Normalización y Estructuración
5. `steps/05-generacion-de-reporte.md` — Generación de Reporte

## Feedback al usuario

- Mientras ejecutas cada paso: salvo que el usuario indique lo contrario, escribe en el chat solo para reportar errores o decisiones pendientes; de lo contrario, mantén silencio.
- Cuando termines cada paso: responde en chat **exactamente una línea seca** con el formato `<nombre-del-paso> OK.`
- Cuando termines de escribir archivos: responde en chat **exactamente una línea seca** con el formato `<nombre-del-workflow> OK; reporte: <ruta a archivos generados>`;
