---
name: follow-lib-zod-setup-zod
description: Install Zod — version detect (v3/v4), install, tsconfig, import patterns
argument-hint: "[version]"
related:
  - follow-lib-zod
  - run-typecheck
  - resolve-errors
---

## Goal

Install Zod — detect/install the version (v3 vs v4), import patterns, tsconfig requirements

## Scope

Setup only — the v3→v4 upgrade is done by the `migrate-zod-v4` workflow; schema authoring → `define-schemas`

## Execute

### 1. Detect Version

```bash
bun pm ls zod     # or npm ls zod
```

- `zod@3.x` → classic API; `zod@4.x` → new API (dual-published subpath `zod/v4` during the v3.25+ transition)
- Fresh install → latest v4 (stable since 2025)

### 2. Install

```bash
bun add zod          # runtime dep — not -D
```

- v4 install notes: `zod@latest` = the v4 line; pin `zod@4` explicitly in package.json
- Peer ecosystem: `@hookform/resolvers`, `zod-to-json-schema` compat — check v4 support per package

### 3. Import Patterns

```ts
import { z } from 'zod'
// v4 explicit: import { z } from 'zod/v4' (in the v3.25+ dual-publish) or 'zod' when v4 is installed
// v4 sub-packages: 'zod/mini' (tree-shakable core), 'zod/locales' (error locales)
```

- The `zod/v4` subpath in v3.25+ — a transition path to try v4 without upgrading
- `zod/mini` — functional API for bundle-sensitive apps

### 4. TSConfig Requirements

- `strict: true` — Zod type inference requires strict mode
- TypeScript `>= 5.5` for v4 (v3 needs 4.5+)
- No special JSX/module config needed

### 5. Verify

1. `bunx tsc --noEmit` clean
2. Smoke test: `z.string().parse('x')` in a unit test
3. fail → `/resolve-errors` max 3 rounds

## Rules

- `zod` is a runtime dependency — never `-D`
- v4 = the new default — v3 only for legacy codebases (upgrade → `migrate-zod-v4`)
- One import style across the project — the `z` namespace is canonical
- Check ecosystem lib compat (hookform resolvers, trpc, orpc) against v4 before upgrading

## Expected Outcome

- `zod` installed at the right version, imports ready, typecheck passing
