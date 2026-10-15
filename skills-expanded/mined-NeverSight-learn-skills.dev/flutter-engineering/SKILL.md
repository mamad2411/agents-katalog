---
name: flutter-engineering
description: Ensures HeyEddi Flutter projects have the right engineering stack — Flutter (Riverpod, go_router, Material 3), FastAPI backend, or Firebase tooling. Audits gaps, scaffolds as needed, runs flutter test/analyze, documents local dev servers. Use when frontend is Flutter or before design/feature work on a HeyEddi mobile/web app.
paths:
  - "pubspec.yaml"
  - "lib/**"
  - "pyproject.toml"
  - "backend/**"
  - "firebase.json"
  - "openapi.json"
  - ".heyeddi/**"
---

# Flutter Engineering

Baseline **Flutter engineering** for HeyEddi apps. Detects which stacks apply and adds the correct tooling — Vue projects should use `@project-engineering` instead.

## Subagents (default)

Delegate scaffold/audit/test scripts to **Task** `shell`; repo discovery to `explore`. Main chat picks stack from audit JSON. See `reference/subagents.md`.

## Stacks

| Stack | When | Tooling added |
|-------|------|----------------|
| **Flutter** | Mobile / web frontend | `pubspec.yaml`, Riverpod, go_router, Material 3, widget tests |
| **FastAPI** | REST API backend | `backend/`, pytest, `openapi.json`, uvicorn on **8090** |
| **Firebase** | Firestore / Auth | `firebase.json`, rules, emulators |

Declare intent in `.heyeddi/stack.json`:

```json
{
  "frontend": "flutter",
  "backends": ["fastapi"],
  "web_port": 8085,
  "api_port": 8090
}
```

Or `"backends": ["firebase"]` or `["fastapi", "firebase"]`.

## Workflow

1. **`audit_scaffold`** — per-layer JSON (flutter / fastapi / firebase).
2. **`scaffold_stack --stack auto`** — fills gaps (`flutter`, `fastapi`, `firebase`, or `full`).
3. **`ensure_flutter`** + **`ensure_python`** (via `@project-engineering`) as needed.
4. **`dev_server_info`** — Flutter web `:8085`, API `:8090`, Firebase emulators `:4000`.
5. Implement features (`@design-handoff-flutter`, `@flutter-patterns`, `@dart-type-bridger`).
6. **`run_tests`** + **`run_backend_tests`** + **`verify_build`**.

## Local dev servers

| Stack | Command | URL |
|-------|---------|-----|
| Flutter web | `flutter run -d web-server --web-port=8085 --web-hostname=127.0.0.1` | http://127.0.0.1:8085 |
| Flutter mobile | `flutter run` | device / emulator |
| FastAPI | `cd backend && poetry run uvicorn app.main:app --reload --port 8090` | http://127.0.0.1:8090/docs |
| Firebase | `firebase emulators:start` | http://localhost:4000 |

Set `FLUTTER_WEB_URL` (or `DEV_SERVER_URL`) for `@visual-auditor` when auditing Flutter web.

## References

- `reference/dev-server.md` — Flutter web + mobile
- `reference/fastapi-client.md` — Dio + OpenAPI types
- `reference/firebase-client.md` — firebase_core + Firestore
- `reference/design-handoff.md` — chain `@design-handoff-flutter`

## Related skills

- `@dart-type-bridger` — OpenAPI / Firestore → Dart models
- `@flutter-patterns` — repositories, Riverpod providers, auth
- `@design-handoff-flutter` — screenshot → Material widgets
- `@project-engineering` — shared FastAPI/Firebase scaffolds (invoked by `scaffold_stack`)
