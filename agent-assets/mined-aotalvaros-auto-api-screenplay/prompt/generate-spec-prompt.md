---
name: generate-spec
description: Genera una especificación técnica ASDD para un nuevo feature. Usa este comando con el nombre e descripción del feature.
argument-hint: "<nombre-feature>: <descripción del requerimiento>"
agent: Spec Generator
tools:
  - edit/createFile
  - read/readFile
  - search/listDirectory
  - search
---

Genera una especificación técnica completa en `.github/specs/` para el siguiente requerimiento.

**Feature**: ${input:featureName:nombre del feature en kebab-case}
**Requerimiento**: ${input:requirement:descripción del requerimiento — o "ver requirements" para cargar desde .github/requirements/}

## Pasos a seguir:

1. **Si el requerimiento no se proporcionó**, busca en `.github/requirements/${input:featureName}.md`. Si existe, úsalo como fuente.
2. Lee el stack: `.github/instructions/backend.instructions.md`.
3. Explora el código existente para identificar patrones, modelos y rutas relacionadas.
4. Genera la spec usando la plantilla en `.github/skills/generate-spec/spec-template.md`.
5. Guarda el archivo como `.github/specs/${input:featureName}.spec.md` con estado `DRAFT`.
6. Confirma la creación con un resumen de la spec al usuario.

## La spec debe cubrir:
- Historias de usuario con criterios de aceptación en Gherkin
- Modelos de datos (Pydantic + MongoDB)
- Endpoints de API con request/response y errores
- Diseño Frontend (páginas, componentes, hooks, servicios)
- Plan de pruebas (backlog de tasks Backend + Frontend + QA)
