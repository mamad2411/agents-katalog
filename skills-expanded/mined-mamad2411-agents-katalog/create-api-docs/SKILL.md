---
name: create-api-docs
description: Generate API documentation for the selected scope from routes, handlers, schemas, resolvers, or formal specifications. | Genera documentación de API para el alcance seleccionado a partir de rutas, handlers, esquemas, resolvers o especificaciones formales.
license: MIT
---

# Create API Docs

## Responsibilities

- identify the API surface
- group endpoints or operations by domain
- describe auth, request/response shapes, and error behavior when evidenced
- avoid speculating about undocumented contracts

## Required Inputs

- the selected `{scope}` and API boundaries
- route definitions, handlers, schemas, resolvers, specs, or validators inside the scope
- scope analysis and terminology used by related docs
- endpoint rules that constrain grouping and evidence handling

## Expected Output

Produce a **Document Generation Artifact** for the API reference containing at least:

- `targetPath`: `{scope}/docs/api-reference.md`
- `documentType`: `api-reference`
- `sourcesInspected`
- `confidenceNote`
- `openQuestions` or `needsConfirmation` when applicable

The generated document must include only evidenced endpoints or operations, marking incomplete payload, versioning, auth, or error details as `Needs confirmation` when needed.

## Rules

- Prefer route definitions, schemas, resolvers, OpenAPI specs, and validators.
- Use `Needs confirmation` for incomplete payload or error details.
- Keep endpoint grouping aligned with the repository structure.
- Include `Sources Inspected`.
- Remove endpoints or operations that are no longer evidenced in the selected scope.

## References

Use the shared document sub-skill contract in [../../references/contracts/document-subskill.md](../../references/contracts/document-subskill.md), the shared handoff contract in [../../references/contracts/sub-skill-handoffs.md](../../references/contracts/sub-skill-handoffs.md), the shared template at [../../references/templates/api-reference.md](../../references/templates/api-reference.md), the shared conventions at [../../references/templates/common.md](../../references/templates/common.md), [references/endpoint-rules.md](references/endpoint-rules.md), and the local specialization note in `references/local-specialization.md`.
