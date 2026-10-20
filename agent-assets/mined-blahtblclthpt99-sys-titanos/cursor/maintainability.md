---
description: Maintainability — modules, interfaces, shared UI, docs, onboarding
alwaysApply: true
---

# MAINTAINABILITY

Code must be easy for the next developer to find, change, and extend without tribal knowledge.

## Architecture

| Layer | Owns | Must not |
|---|---|---|
| `src/pages` | Routes, composition | Business rules, raw SQL |
| `src/components/{domain,shared,ui}` | UI | Direct Supabase in deep leaves when an `*Api` exists |
| `src/lib/{feature\|*Api}` | Feature services | Page markup |
| `src/api` | Auth/entities/functions client | Product UI |
| `api/functions` + `api/_lib` | Server endpoints / helpers | Client-only assumptions |
| `shared/` | Pure dual-runtime engines | React, DOM |
| `supabase/migrations` | Schema / RLS / indexes | App business prose |

## Rules

1. **Modular** — new domains get a folder (`lib/<feature>/`) + public `index.js` (+ optional `MODULE.md`).
2. **Reusable services** — prefer `*Api.js` / `api/_lib` / `shared/*` over copy-paste in pages.
3. **Shared UI** — list/detail pages use `PageShell` + `PageHeader` + Empty/Loader/Error; export via `ExportMenu`.
4. **Separation** — money/tax/GPS rules live in engines/docs, not JSX.
5. **Interfaces** — export public contracts from barrels; document shapes in `interfaces.js` / JSDoc.
6. **Feature isolation** — Driver Hub UI talks to `@/lib/driverOs` and `@/lib/driverActivity`, not random deep files (except temporary migration).
7. **Documentation** — update `ARCHITECTURE.md` / feature `MODULE.md` when boundaries change.
8. **Onboarding** — `docs/ONBOARDING.md` stays accurate (env, migrations, test/lint/build, where to put code).

## Definition of done

Incomplete if a feature ships only as a god page with no service boundary, skips shared chrome, leaves no map for the next contributor, or fails the FINAL OBJECTIVE ship gate (`.cursor/rules/final-objective.mdc`).
