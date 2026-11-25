---
name: bootstrap-brownfield
description: (NS) Onboard an existing codebase into spec-driven planning — map stack, modules, rule adherence, and gaps without modifying code. Use when the user says analyze existing project, brownfield bootstrap, or before first requirements on a repo with code but no requirements. Outputs brownfield-map.md for requirements-generator. Read-only on source code.
depends:
  - nextstage-harness
---

# Bootstrap Brownfield

Architectural discovery for existing products before SDD planning.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md`. Load rules from `{harness_root}/rules/*.md`. Read `architecture-rules.md` first. Legacy: `.cursor/rules/*.mdc` only if `{harness_root}` is absent. Compare findings to canonical rules when present — checks are advisory if rules missing.

## When to use

- "Analyze the existing project" / "brownfield bootstrap"
- First SDD planning on repo with code but no `requirements.md`
- Before `requirements-generator` on legacy code

## Workflow

### Step 1 — Structure detection

Under `{product_root}` (and repo root if legacy layout — document inconsistency):

**Backend signals:** `composer.json`, `artisan`, modular `app/Modules/`, `docker-compose.yml`, `.env.example`

**Frontend signals:** `package.json`, `tsconfig.json`, `src/modules/`, `cypress/`, bundler config

**Layout:** monorepo `backend/` + `frontend/` vs single app

### Step 2 — Module mapping

List domains:

- Backend: modules, controllers, models, migrations per module
- Frontend: pages, stores, services per module

### Step 3 — Rule adherence (optional)

Compare to harness rules when they exist — backend module layout, multitenancy, frontend patterns, tests. Mark ✅ / ⚠️ / ❌ per row.

Use stack-agnostic checks when no harness rules.

### Step 4 — Report

Create or update `{product_root}/docs/context/brownfield-map.md`:

```markdown
# Architectural map — brownfield bootstrap

**Date:** {date}

## Identified stack

- Backend: ...
- Frontend: ...
- Database, cache, queues, E2E tooling

## Backend modules

| Module | Controllers | Models | Migrations | Tests |

## Frontend modules

| Module | Pages | Stores | E2E |

## Rule adherence

{tables when rules exist}

## Gaps (priority)

1. Critical ...
2. Medium ...

## Recommendations for next planning

- ...
```

### Step 5 — Present

Summarize 3–5 bullets, highlight critical gaps, ask whether to start version planning or review gaps.

## Critical rules

- **Read-only** — no code changes
- Report only under `{product_root}/docs/context/`
- Pass `brownfield-map.md` to `requirements-generator` as context
- Update existing map rather than duplicate

## Related skills

- `codebase-reverse-spec` — business behavior extraction (deeper than bootstrap)
- `requirements-generator` — next step after bootstrap
- `clarify-requirements` — when scope still vague
