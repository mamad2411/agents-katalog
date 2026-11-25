---
name: tuck-bit-es
description: "TuckBit es una habilidad portátil para agentes de programación. Ayuda a elegir el contexto, las herramientas y la verificación adecuados sin sacrificar la corrección."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: es
---

# TuckBit — Español

> El núcleo de la habilidad está traducido; las referencias técnicas conservan temporalmente el inglés y requieren revisión comunitaria.

Optimiza los resultados correctos y verificados por recurso utilizado, no solo el número de tokens.

Cuatro capacidades básicas: registro, contexto, verificación y presupuesto. Orquestación y métricas son opcionales.

## Método de trabajo

Empieza por la solicitud exacta del usuario, las instrucciones disponibles y las herramientas autorizadas. Conserva todas las condiciones, aprobaciones y pruebas obligatorias.

1. Define el objetivo, los límites, los riesgos y cuándo detenerte; evita planes largos para tareas triviales.
2. Busca el código, los documentos y las herramientas relevantes más específicos; amplía la búsqueda solo cuando sea necesario.
3. Prefiere la búsqueda nativa de herramientas; los metadatos son pistas, nunca permisos de ejecución.
4. Para tareas pequeñas usa un agente; distribuye solo trabajos independientes con responsables y criterios claros.
5. Ejecuta pruebas específicas y después todas las verificaciones obligatorias sobre la revisión final.
6. Entrega un resumen verificable de cambios, pruebas, riesgos y bloqueos. Guarda puntos de control y detente en vez de consultar sin fin.

## Consulta solo la referencia pertinente

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## Límites obligatorios

No omitas comprobaciones de seguridad, reduzcas la calidad, inventes resultados, leas credenciales, ignores aprobaciones ni ejecutes acciones destructivas sin permiso. El anfitrión controla los permisos.

**Vista previa para desarrolladores. La instalación no demuestra la activación del agente ni garantiza un ahorro de tokens.**
