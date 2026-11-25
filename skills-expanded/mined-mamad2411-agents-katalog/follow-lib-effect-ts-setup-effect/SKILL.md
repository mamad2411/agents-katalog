---
name: follow-lib-effect-ts-setup-effect
description: Install Effect-TS, tsconfig and the basics (Effect/Layer/Service), ready to use
argument-hint: "[runtime]"
related:
  - follow-lib-effect-ts
  - follow-lang-typescript
  - follow-tool-vitest
  - learn
  - resolve-errors
---

## Goal

Install Effect-TS and configure TypeScript/project structure so `Effect`, `Layer`, `Service` are written correctly — first-time setup only

## Scope

- Use when the project has no `effect` yet or needs a fresh setup (if it exists already → verify only)
- Covers: install, `tsconfig.json`, project structure, Effect/Layer/Service basics
- Does not cover migrating an existing codebase — do `workflows/migrate-to-effect/SKILL.md` instead

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. Read `package.json` — if `effect` is already there → skip to verify; if the version is v4 RC → read the Version Notes in [../../references/effect-ts.md](../../references/effect-ts.md)
2. Confirm TypeScript `>= 5.4` (`bunx tsc --version`)
3. Detect the package manager from the lockfile and use the matching command

### 2. Configure TypeScript

> Goal: tsconfig supports Effect types

1. Set `strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true`, `skipLibCheck: true`
2. `target: "ES2022"`+, `moduleResolution: "bundler"` or `"nodenext"` per runtime
3. Do `/follow-lang-typescript` if the base config isn't ready

### 3. Install Packages

> Goal: install effect and the platform packages per runtime

1. Run `bun add effect` — a runtime dependency, never with `-D`
2. `bun add @effect/platform` + `@effect/platform-bun` (Bun) or `@effect/platform-node` (Node) per runtime
3. `bun add -D vitest @effect/vitest` for tests — check the peer `vitest ^3.2` first (setup: `/follow-tool-vitest`)
4. `Schema` lives in core `effect` — don't install `@effect/schema` separately (legacy)
5. (optional) `bun add -D @effect/language-service` + add `{ "name": "@effect/language-service" }` to `tsconfig.compilerOptions.plugins` for editor diagnostics; TypeScript `>= 7` uses `@effect/tsgo` instead

### 4. Create Structure And Basics

> Goal: folder structure and basic patterns

1. Create `src/app` (composition root), `src/domain` (pure logic), `src/services` (services+layers), `src/adapters`, `src/config`, `src/types`, `src/utils`, `test/unit`, `test/integration`
2. Effect basics: `Effect.gen` + `yield*` for composition, `pipe` for chaining, `Effect.fn` for named functions
3. Errors: `Data.TaggedError` for expected errors, then catch with `Effect.catchTag`/`catchTags`
4. DI: `Effect.Service` (v3.9+) for a service with its default layer, or `Context.Tag` + `Layer.succeed`/`Layer.effect` for manual
5. Config: `Config.string`/`Config.redacted` for env — never read `process.env` directly in services
6. Run only at the boundary: `Effect.runPromise`/`BunRuntime.runMain` at the entry point only — see [../../references/patterns.md](../../references/patterns.md)

### 5. Verify

> Goal: typecheck and the smoke effect pass

1. Run `bunx tsc --noEmit` until it passes
2. Write a small smoke effect (service + layer + run at the entry) and run it to get output
3. If tests exist → `bunx vitest run` passes (use `it.effect` from `@effect/vitest`)
4. If verification fails → run `/resolve-errors` max 3 rounds, then stop and report; if it passes → `/suggest-next-action`

## Rules

- Idempotent — if setup already exists, only verify; never reinstall/overwrite the existing config
- `effect` is a runtime dep; import namespace: `import { Effect, Layer, Context } from "effect"`
- Run (`Effect.run*`) only at the application boundary — never in service/library code
- Check the version in `package.json` before choosing an API (v3 vs v4 RC differ) — if unsure → do `/learn` from the official docs (effect.website)

- Use `/follow-lib-effect-ts` for the full reference, patterns and version notes

## Expected Outcome

- `effect` + platform packages installed per the peer constraints
- `tsconfig.json` strict-ready, structure following the Effect architecture
- Service/Layer basics work, typecheck + smoke test pass
