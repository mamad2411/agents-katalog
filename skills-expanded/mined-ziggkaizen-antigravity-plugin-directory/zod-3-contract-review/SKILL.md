---
name: zod-3-contract-review
description: Reviews Zod 3 schema/API/DTO alignment, schema drift, shared validation source-of-truth structure, dependency compatibility, and migration risks. Use for frontend-backend contract reviews, DTO drift, schema refactoring, generated client checks, or Zod 3 to Zod 4 readiness analysis.
license: MIT
compatibility: Requires Node.js for bundled helper scripts. Intended for TypeScript or JavaScript projects using Zod 3.
---

# Zod 3 Contract Review Skill

## When to Use

Use this skill when reviewing schema changes, shared validation package changes, frontend/backend DTO drift, contract-generation output, OpenAPI alignment, dependency compatibility, or migration readiness.

## First Checks

1. Confirm whether Zod schemas, DTOs, OpenAPI, generated clients, or framework metadata are the source of truth.
2. Identify all consumers of the schema change.
3. Run helper scripts with `--help` before using them:
   - `scripts/scan-zod-compatibility.mjs --help`
   - `scripts/scan-contract-drift.mjs --help`
   - `scripts/zod-3-schema-change-review.mjs --help`
   - `scripts/zod-3-contract-drift-guard.mjs --help`

## Review Priorities

- Shared schemas live in a deliberate source-of-truth location.
- Frontend validation accepts the same shape that backend validation accepts.
- Backend DTOs, API responses, and Zod schemas describe the same fields and optionality.
- Transforms and preprocessors do not obscure the input/output contract.
- Version compatibility is explicit and tested.
- Schema changes include consumer updates, tests, and documentation where needed.

## Workflow References

- `workflows/contract-review-workflow.md`: Use for schema/API/DTO review.
- `workflows/contract-drift-check-workflow.md`: Use when checking drift between DTOs and schemas.

## Resources and Examples

- `resources/contract-review-checklist.md`: Contract review checklist.
- `resources/source-of-truth-layouts.md`: Common validation package layouts.
- `examples/contract-alignment.example.ts`: Example of schema-derived DTO alignment.
