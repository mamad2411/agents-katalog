---
name: backend-type-bridger
description: Syncs FastAPI OpenAPI schema to TypeScript types and reads Firestore schema hints. Use when writing Vue composables against FastAPI or Firebase backends.
paths:
  - "**/composables/**"
  - "**/api/**"
  - "openapi.json"
---


# Backend Type Bridger

## When to use

- Frontend agent needs accurate API payload shapes
- `openapi.json` or FastAPI server available locally
- Firestore rules or schema file exists for Firebase projects

## Instructions

1. FastAPI: `python scripts/sync_openapi.py --project-root <root>` — writes `src/types/api.ts` from `openapi.json` or `--url`
2. Firebase: `python scripts/fetch_firestore_schema.py --project-root <root>`
3. Import generated types in composables — never guess field names. Refine generated interfaces if OpenAPI uses `$ref` heavily.
