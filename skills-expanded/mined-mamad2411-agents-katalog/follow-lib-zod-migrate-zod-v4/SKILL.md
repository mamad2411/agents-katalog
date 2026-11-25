---
name: follow-lib-zod-migrate-zod-v4
description: migrate Zod v3 → v4 — breaking changes, import path, API renames
argument-hint: "[scope]"
related:
  - follow-lib-zod
  - plan
  - scan-codebase
  - use-astgrep
  - deep-review-codebase
  - run-typecheck
---

## Goal

Migrate the codebase from Zod v3 to v4 safely — import paths, API renames, error handling changes — with a rollback path and full verification

## Scope

- Use when the project is on `zod@3.x` and wants to move to v4, or to use the `zod/v4` subpath side by side
- Covers: import changes, deprecated APIs, error object changes, verification
- Full v4 API details live in the parent `SKILL.md` and the official migration guide (zod.dev)

## Execute

### 1. Plan And Map Impact

> Goal: identify every affected point before editing

1. Do `/plan` — read `package.json` to confirm the current version, write the rollback path (revert commit + pin `zod@3`)
2. Do `/scan-codebase` for all import sites: `from "zod"`, `from "zod/v3"`, `zod/v4`
3. Find usage of changed APIs: `.format()`, `.flatten()`, `.merge()`, `.strict()`, `.passthrough()`, `z.string().email()`, `error.errors`, the `message` option
4. Check dependent libraries (e.g. `zod-to-json-schema`, form libs) for v4 support — if a blocker → stop and report

### 2. Upgrade Package And Imports

> Goal: change the version and import paths correctly

1. Run `bun add zod@latest` (v4.x) — or for a gradual migration: `zod@3.x` offers the `zod/v4` subpath as a temporary bridge
2. v4 code uses the normal `import * as z from "zod"`; old code still on v3 switches temporarily to `import * as z from "zod/v3"`
3. Use a codemod if available (`zod` has an official codemod — see the official docs) or do `/use-astgrep` for rename patterns
4. Separate commits: package upgrade / import changes / API renames — so it's bisectable

### 3. Fix API Renames

> Goal: fix the breaking changes group by group

1. Error handling: `error.errors` → `error.issues`; `.format()`/`.flatten()` → `z.treeifyError()`; the `message` param → `error` param
2. Schema methods: `.merge()` → `A.extend(B.shape)` or spread; `.strict()` → `z.strictObject()`; `.passthrough()` → `z.looseObject()`
3. String formats: `z.string().email()` → `z.email()`, `.uuid()` → `z.uuid()`, `.url()` → `z.url()`
4. Removed types: `ZodEffects` was removed — refactor code that relied on internal types (`._zod` is internal, never use it)
5. The `safeParse` error in v4 no longer extends `Error` — fix spots checking `instanceof Error`

### 4. Verify

> Goal: typecheck, tests, and runtime smoke all pass

1. Run `bunx tsc --noEmit` (do `/run-typecheck`) — type errors reveal the missed spots
2. Run tests (do `/run-test`) — especially schema validation tests and error-shape assertions
3. Do `/deep-review-codebase` — no v3 APIs left
4. Runtime smoke: parse real input through the changed schemas — check the error output shape
5. If stuck → build a TODO list; done → `/report-before-after` then `/ship`

## Rules

- Never mix migration with feature work in one commit — one commit per step
- The `zod/v3` subpath is fine as a bridge during migration, but there must be a plan to remove it
- Check dependent libraries before upgrading — a lib still requiring v3 is a blocker
- If any API is uncertain → check the official docs (zod.dev migration guide)

## Expected Outcome

- `zod` is v4 in `package.json` with no v3 imports left (or only bridged ones with a removal plan)
- Typecheck, tests, and runtime smoke pass
- No deprecated APIs — ready for `/ship`
