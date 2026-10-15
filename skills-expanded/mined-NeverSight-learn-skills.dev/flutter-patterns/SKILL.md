---
name: flutter-patterns
description: Provides FastAPI Dio and Firebase client patterns for Flutter — repositories, Riverpod providers, auth. Context-first skill; use when writing or reviewing Dart data layers for HeyEddi Flutter apps.
paths:
  - "lib/**"
  - "pubspec.yaml"
---

# Flutter Patterns

## When to use

- Writing auth, API, or Firestore repositories
- Choosing FastAPI JWT vs Firebase client patterns
- Reviewing provider error handling and token refresh

## Instructions

1. Read `context/fastapi-dio.md` for REST + JWT projects.
2. Read `context/firebase-client.md` for Firebase/Firestore projects.
3. Read `context/riverpod.md` for provider conventions.
4. Optional: `python scripts/validate_provider.py --path lib/providers/users_provider.dart`

## Notes

- Prefer context docs over improvising interceptors or security rules.
- Widgets stay thin; repositories + providers own I/O.
