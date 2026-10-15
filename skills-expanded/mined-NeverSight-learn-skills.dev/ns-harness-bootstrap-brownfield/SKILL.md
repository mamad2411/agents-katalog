---
name: ns-harness-bootstrap-brownfield
description: (NS) Onboard an existing codebase into spec-driven planning — map stack, modules, rule adherence, and gaps without modifying code. Use when the user says analyze existing project, brownfield bootstrap, or before first requirements on a repo with code but no requirements. Outputs brownfield-map.md for ns-sdd-requirements-generator. Read-only on source code.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
---

# Bootstrap Brownfield

Architectural discovery for existing products before SDD planning.

Output is **agent-dense** (tables, counts, gap list) — not a human essay. See `references/agent-dense.md`.

## Harness discovery

See `../ns-harness/references/harness-discovery.md`. Load rules from `{harness_root}/rules/*.md`. Read `architecture-rules.md` first. Legacy: `.cursor/rules/*.mdc` only if `{harness_root}` is absent. Compare findings to canonical rules when present — checks are advisory if rules missing. **Do not copy the constitution stack into the map** — link it.

## When to use

- "Analyze the existing project" / "brownfield bootstrap"
- First SDD planning on repo with code but no `requirements.md`
- Before `ns-sdd-requirements-generator` on legacy code

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

Create or update `{product_root}/docs/context/brownfield-map.md` from `references/brownfield-map.template.md` and `references/agent-dense.md`.

Writing rules:

- Tables / one-liners only — no overview paragraphs.
- Stack = pointer to `architecture-rules.md` (+ optional one-line delta).
- Gaps = priority table; Next planning ≤3 bullets.

### Step 5 — Present

Chat summary only (3–5 bullets: date, critical gaps, next skill). Do not paste the map body into chat.

## Critical rules

- **Read-only** — no code changes
- Report only under `{product_root}/docs/context/`
- Pass `brownfield-map.md` to `ns-sdd-requirements-generator` as context
- Update existing map rather than duplicate
- Never duplicate full stack from `architecture-rules.md`

## Related skills

- `ns-harness-architecture-rules` — constitution (stack/layout source of truth)
- `ns-harness-codebase-reverse-spec` — business behavior extraction (deeper than bootstrap)
- `ns-sdd-requirements-generator` — next step after bootstrap
- `ns-sdd-clarify-requirements` — when scope still vague

## References

| File | When |
| ---- | ---- |
| `references/brownfield-map.template.md` | Step 4 skeleton |
| `references/agent-dense.md` | Writing constraints |
