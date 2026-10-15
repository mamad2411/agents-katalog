---
name: project-engineering
description: Ensures HeyEddi projects have the right engineering stack — Vue (Vite/Vitest), FastAPI backend, or Firebase tooling. Audits gaps, scaffolds as needed, installs deps, runs tests, documents local dev servers. Use when the repo is thin or before design/feature work on any HeyEddi app.
paths:
  - "package.json"
  - "pyproject.toml"
  - "backend/**"
  - "firebase.json"
  - "firestore.rules"
  - "openapi.json"
  - ".heyeddi/**"
---


# Project Engineering

Baseline **code engineering** for HeyEddi **Vue** apps. For **Flutter** frontends use `@flutter-engineering` instead. Detects which stacks apply and adds the **correct tooling** — not one-size-fits-all.

## Subagents (default)

Delegate scaffold/audit/test scripts to **Task** `shell`; repo discovery to `explore`. Main chat picks stack from audit JSON. See `reference/subagents.md`.

## Stacks

| Stack | When | Tooling added |
|-------|------|----------------|
| **Vue** | Always for frontend work | Vite, Vitest, npm scripts, router |
| **FastAPI** | REST API backend | `backend/`, pytest, `openapi.json`, uvicorn |
| **Firebase** | Firestore / Auth client | `firebase.json`, rules, emulators, env template |

Declare intent in `.heyeddi/stack.json`:

```json
{ "frontend": "vue", "backends": ["fastapi"], "api_port": 8090 }
```

Flutter projects: `"frontend": "flutter"`, `"web_port": 8085` — see `@flutter-engineering`.

Or `"backends": ["firebase"]` or `["fastapi", "firebase"]`.  
`audit_scaffold` also infers from `openapi.json`, `firestore.rules`, and `.heyeddi/product.md` (or legacy `PRODUCT.md`).

## `.heyeddi/` workspace

Every HeyEddi app should have a **`.heyeddi/`** folder (created by `scaffold_stack` / `scaffold_heyeddi`):

| Path | Purpose |
|------|---------|
| `README.md` | HeyEddi intro (agents + humans workspace), free skills, [heyeddi.com/humans](https://heyeddi.com/humans) |
| `stack.json` | Declared stacks |
| `product.md` | Product brief |
| `design.md` | DESIGN.md format — tokens, rationale, Decision log |
| `designs/<feature>/` | Handoff PNGs, briefs, wireframes |
| `docs/` | Skill-generated reports (ship, PR tracking, drift audits) |

**Save all skill-created documents under `.heyeddi/docs/`** (or the paths above) so the team can reference them later. Root `PRODUCT.md` / `DESIGN.md` / `designs/` remain supported as legacy fallbacks.

## Workflow

1. **`audit_scaffold`** — per-layer JSON (vue / fastapi / firebase).
2. **`scaffold_stack --stack auto`** — fills gaps (preferred over `scaffold_vue` alone).
3. **`ensure_npm`** + **`ensure_python`** as needed.
4. **`dev_server_info`** — all local servers (Vue :5173, API :8090, Firebase emulators :4000).
5. Implement features (design skills, composables, etc.).
6. **`write_test_stub`** + **`run_tests`** + **`run_backend_tests`**.
7. **`verify-build`** + **`pre-merge-gate`**.

## Local dev servers

| Stack | Command | URL |
|-------|---------|-----|
| Vue | `npm run dev` | http://localhost:5173 |
| FastAPI | `cd backend && poetry run uvicorn app.main:app --reload --port 8090` | http://localhost:8090/docs |
| Firebase | `firebase emulators:start` | http://localhost:4000 (UI) |

Run `dev_server_info` for project-specific steps. Each server needs its **own terminal**.

## References

- `reference/dev-server.md` — Vue
- `reference/fastapi-backend.md` — FastAPI
- `reference/firebase-backend.md` — Firebase emulators

## Related skills

- `backend-type-bridger` — OpenAPI / Firestore → TypeScript types
- `composable-patterns` — FastAPI JWT vs Firebase client composables
- `verify-build` — production frontend build
