---
name: dart-type-bridger
description: Syncs FastAPI OpenAPI schema to Dart model stubs and reads Firestore schema hints for Flutter projects. Use when writing Flutter repositories against FastAPI or Firebase backends.
paths:
  - "lib/models/**"
  - "lib/repositories/**"
  - "openapi.json"
---

# Dart Type Bridger

## When to use

- Flutter agent needs accurate API payload shapes
- `openapi.json` or FastAPI server available locally
- Firestore rules or schema file exists for Firebase projects

## Instructions

1. FastAPI: `python scripts/sync_openapi.py --project-root <root>`
2. Firebase: `python scripts/fetch_firestore_schema.py --project-root <root>`
3. Import generated models in repositories — never guess field names.
