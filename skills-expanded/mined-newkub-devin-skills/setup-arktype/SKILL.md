---
name: follow-lib-arktype-setup-arktype
description: Install ArkType, type() syntax basics and scope config, ready to use
argument-hint: "[scope]"
related:
  - follow-lib-arktype
  - follow-lib-zod
  - follow-lang-typescript
  - learn
  - resolve-errors
---

## Goal

Install ArkType and configure TypeScript/editor so `type()` syntax and `scope()` work correctly — first-time setup only

## Scope

- Use when the project has no ArkType yet or needs a fresh setup (if it exists already → verify only)
- Covers: install, `tsconfig.json`, editor settings, `type()` basics, `scope()` config
- Does not cover advanced patterns — see the parent `SKILL.md` and `references/`

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. Read `package.json` — if absent → stop and report; if `arktype` is already there → skip to verify
2. Confirm TypeScript `>= 5.1` (`bunx tsc --version`)
3. Confirm `"type": "module"` or a runtime that supports ESM — ArkType requires ESM
4. If unsure about a requirement → run `/learn-from-web` to check the official docs (arktype.io)

### 2. Install

> Goal: install arktype as a runtime dependency

1. Run `bun add arktype` (or the package manager matching the lockfile)
2. Confirm `arktype` is in `dependencies` (never put it in devDependencies — it's used at runtime)
3. If you need regex types, install `arkregex` additionally (optional)

### 3. Configure TypeScript And Editor

> Goal: tsconfig and editor support the string-embedded type syntax

1. Enable `strict: true` (or at minimum `strictNullChecks: true`) in `tsconfig.json`
2. Enable `exactOptionalPropertyTypes: true` and `skipLibCheck: true`
3. Add to `.vscode/settings.json`: `"editor.quickSuggestions": { "strings": "on" }` and exclude `"^(node:)?os$"` from auto-import (to avoid clashing with the Node `os` module)
4. Run `/follow-lang-typescript` if the base config isn't ready

### 4. Define First Types

> Goal: create schemas with `type()` basics

1. `import { type } from "arktype"` then define primitives: `type("string")`, `type("number")`
2. Object: `type({ name: "string", "age?": "number" })` — optional via `"key?"`
3. Union/intersection: `"string | number"`, `"a & b"` or `.or()`/`.and()`
4. Validate: `Schema(data)` returns the output or `ArkErrors`; `.assert(data)` throws; `.allows(data)` returns a boolean
5. Infer the type: `typeof Schema.t` — never write a duplicate TS type separately

### 5. Configure Scope

> Goal: grouped type definitions that reference each other with `scope()`

1. Use `scope({ User: {...}, Post: { author: "User" } })` for types that refer to each other within one scope
2. Export with `scope.export()` then use `scope.type()` for scoped definitions
3. Use `configure()` from `arktype/config` for global options when necessary
4. Organize scopes by domain/feature — never put every type in one global scope

### 6. Verify

> Goal: smoke check that the setup really works

1. Run `bunx tsc --noEmit` until it passes
2. Run a smoke test: parse real data through the `type()` you created — get the output or `ArkErrors` correctly
3. If verification fails → run `/resolve-errors` max 3 rounds, then stop and report; if it passes → `/suggest-next-action`

## Rules

- Idempotent — if setup already exists, only verify; never reinstall/overwrite the existing config
- `arktype` is always a runtime dependency
- Use type inference (`typeof Schema.t`) instead of manual type definitions
- Write the minimal config first, then add options — if unsure → check the official docs

## Expected Outcome

- `arktype` installed as a runtime dep, tsconfig + editor ready
- `type()` and `scope()` usable — validation passes the smoke test
- Typecheck passes, ready to use the advanced patterns from the parent `SKILL.md`
