---
name: composable-patterns
description: Provides FastAPI JWT and Firebase client composable patterns for consistent auth and data layers. Context-first skill — use when writing or reviewing Vue composables for API access.
paths:
  - "**/composables/**"
  - "**/use*.ts"
---


# Composable Patterns

## When to use

- Writing `useAuth`, `useApi`, or Firestore data composables
- Choosing between FastAPI JWT vs Firebase client patterns
- Reviewing composable error handling and token refresh

## Instructions

1. Read `context/fastapi-jwt.md` for REST + JWT projects.
2. Read `context/firebase-client.md` for Firebase/Firestore projects.
3. Optional: `python scripts/validate_composable.py --path src/composables/useX.ts`

## Notes

- Prefer context docs over improvising interceptors or security rules.
