---
name: qa-generator
description: Workflow para crear Test Cases con pasos numerados Given/When/Then desde planificación o requisitos. Usar para generar QA.generator-test-cases.md.
disable-model-invocation: true
argument-hint: "Documentación con requisitos, suites y nombres de tests. Opcional: 'to <path>' para destino, o 'preview'/'no-save' para chat-only."
user-invocable: true
compatibility: 
  - agents: [QA.generator]
---

## Mapa de pasos

DEBES leer y ejecutar los pasos de la carpeta `steps/` en este orden:

1. `steps/01-analisis-de-entrada.md` — Análisis de Entrada
2. `steps/02-particionado-por-acceptance-criteria.md` — Particionado por Acceptance Criteria
3. `steps/03-diseno-de-pasos-de-test-cases.md` — Diseño de Pasos de Test Cases
4. `steps/04-marcaje-de-provisionales.md` — Marcaje de Provisionales
5. `steps/05-revision-de-trazabilidad.md` — Revisión de Trazabilidad
6. `steps/06-generacion-de-reporte.md` — Generación de Reporte

## Feedback al usuario

- Mientras ejecutas cada paso: salvo que el usuario indique lo contrario, escribe en el chat solo para reportar errores o decisiones pendientes; de lo contrario, mantén silencio.
- Cuando termines cada paso: responde en chat **exactamente una línea seca** con el formato `<nombre-del-paso> OK.`
- Cuando termines de escribir archivos: responde en chat **exactamente una línea seca** con el formato `<nombre-del-workflow> OK; reporte: <ruta a archivos generados>`;
