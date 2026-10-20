---
description: AI agent operational behaviour for Monolith platform development
alwaysApply: true
---

# Agent behaviour

## Purpose

Make AI-assisted changes predictable, reviewable, and aligned with the rule set — minimise scope creep, architectural drift, and low-quality output.

## Workflow

### Before writing code

1. Read the topic rule(s) for the touched area (see rule map in `monolith-platform.mdc`).
2. Inspect the closest existing pattern — match it. Do not invent parallel structures.
3. The reference implementation for new API features is `apps/api/src/features/health/`; for the web client it is `apps/web/src/lib/api.ts`. Mirror them unless the task explicitly diverges.
4. Confirm whether the task needs: DB migration, new env vars, Docker/CI updates, or types in `@monolith/types`.

### Scope discipline

- Implement exactly what was requested. No drive-by refactors, formatting churn, or speculative abstractions.
- Prefer extending existing modules over creating new ones. Smallest correct diff wins.
- Repetition is acceptable until abstraction is clearly beneficial — see `docs/architecture/engineering-philosophy.md`.

### Output quality

- Production-grade only — no `// TODO: implement`, no placeholder business logic unless the user explicitly asked for stubs.
- Type-safe, explicit code. No `any` without documented justification.
- Comments only for non-obvious business or technical constraints.

### After implementation

- Run or recommend the PR gate — defined in `infra.mdc` (lint, typecheck, test, build, E2E).
- DB schema changed → `pnpm db:migrate`. Env added → register everywhere `infra.mdc` lists.
- Summarise what changed, why, and how to verify — not a file-by-file dump.

### Git & PRs

- Do **not** commit, push, or open PRs unless the user explicitly asks.
- When asked for a PR: include the test plan from `docs/workflows/pull-request-workflow.md`.

### Questions vs assumptions

- Ask when wrong assumptions are costly (auth model, billing rules, data ownership).
- Do **not** ask when the codebase already shows the pattern — infer and match.
- Escalation beats invention. A correct question is cheaper than a wrong system.

## Forbidden

- Introducing new libraries (state managers, ORMs, UI kits) without explicit human approval — see `docs/architecture/engineering-philosophy.md` (technology governance).
- Catch-all `utils/`, `helpers/`, `common/` modules. See `architecture.mdc` for the alternative.
- Rewriting working code to a different style in untouched files.
- Disabling lint/typecheck/tests to "make it work".
- Generating large markdown/docs files unless requested.
- Claiming tests passed without running them when tools are available.

## Operational reminders

- Cross-app changes order: `@monolith/types` → API → web/mobile → tests.
- Docker-first awareness — flag when a change needs Compose or Dockerfile updates.
- Windows dev gotchas live in `docs/workflows/development.md`; point users there on Docker volume / `node_modules` errors.
- Platform name: **Monolith AI-Native Engineering Platform**. Package scope: `@monolith/*`.

## Examples

**Good agent summary**

> Added `OrderSummary` to `@monolith/types`, `OrdersModule` with list endpoint, and `getOrders()` in web `lib/`. Run `pnpm db:migrate`, then `pnpm dev`. Verify `GET /api/orders` and `/orders` page.

**Bad**

> Refactored entire API to hexagonal architecture and added Redux. // unrequested, high drift
