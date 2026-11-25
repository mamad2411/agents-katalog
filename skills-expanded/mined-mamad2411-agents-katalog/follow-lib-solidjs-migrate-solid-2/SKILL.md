---
name: follow-lib-solidjs-migrate-solid-2
description: Migrate Solid 1.x → 2.0 — breaking changes, API surface check, incremental migration steps
argument-hint: "[scope]"
related:
  - follow-lib-solidjs
  - run-typecheck
  - run-test
  - resolve-errors
---

## Goal

Migrate a Solid 1.x codebase → Solid 2.0 — detect usage of changed APIs, apply breaking changes, verify

## Scope

major version upgrade — do it when the project is on `solid-js` 1.x and needs to move to 2.x; **always check the latest official migration guide first** — v2 was at RC stage when this skill was written, APIs may change

## Execute

### 1. Check Current State

```bash
bun pm ls solid-js            # or npm ls solid-js
```

- `solid-js@^1.x` → this migration path; `@2.x`/`-rc` → use the new APIs directly
- **Fetch the official migration guide first**: https://docs.solidjs.com/ — RC stage = APIs still moving; check the latest source, don't guess from this skill

### 2. Audit API Usage

> Goal: inventory patterns that may change

```bash
# grep hot spots
rg "createEffect|createMemo|createResource|createStore|produce|reconcile|createContext|lazy\(|Suspense|ErrorBoundary" src/ -l
```

- Group them: signals/stores/resources/context/SSR/lifecycle — compare against the breaking-changes list from the official guide
- Related package deps: `@solidjs/router`, `@solidjs/meta`, `@solid-primitives/*`, `solid-start` — check each one's compat version

### 3. Upgrade Incrementally

1. `bun add solid-js@<target>` — RC: pin the exact version, no caret
2. Upgrade the ecosystem packages together (router/meta/testing-library — peer deps must match)
3. Apply breaking changes per the guide — do one primitive family at a time, fix errors group by group
4. `bunx tsc --noEmit` after each batch — type errors reveal missed API changes

### 4. Verify

1. `bunx tsc --noEmit` clean
2. `/run-test` — component + store tests all pass
3. `/run-dev` — smoke critical routes; reactivity regressions (stale UI, missing updates)
4. fail → `/resolve-errors` max 3 rounds → report remaining blockers

## Rules

- **RC version = pin exact** — never use `^` on a prerelease
- The official migration guide = source of truth — this skill gives the workflow only; see the docs for API details
- Migrate per-family (signals → stores → resources → SSR) — don't upgrade a large codebase all at once
- Ecosystem packages must upgrade together — mixed major versions collide on peer deps

## Expected Outcome

- `solid-js` 2.x + compat ecosystem installed
- Breaking changes applied, typecheck + tests + dev server pass
