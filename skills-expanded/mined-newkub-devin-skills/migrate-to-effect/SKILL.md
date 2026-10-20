---
name: follow-lib-effect-ts-migrate-to-effect
description: Migrate a neverthrow/promise codebase to Effect incrementally
argument-hint: "[module-or-scope]"
related:
  - follow-lib-effect-ts
  - plan
  - scan-codebase
  - run-typecheck
  - run-test
  - report-before-after
---

## Goal

Adopt Effect-TS into a codebase using neverthrow/Promise/try-catch incrementally — one module at a time, coexisting, rollback-able

## Scope

- Use when the project already has `effect` installed (if not → do `workflows/setup-effect/SKILL.md` first) and old error handling/async patterns must move to Effect
- Covers: pattern mapping (Result → Effect, Promise → Effect.tryPromise), interop, incremental adoption
- Doesn't force a rewrite of the whole codebase — old boundaries keep working during the migrate

## Execute

### 1. Plan And Map Impact

> Goal: pick the scope and the migration order

1. Do `/plan` — identify the modules to migrate, dependency order (leaf modules first, entry point last)
2. Do `/scan-codebase` to find the old patterns: `Result`/`ResultAsync` (neverthrow), `try/catch` + `await`, `Promise` chains, custom error types
3. Write the rollback path — migrate in a separate commit per module so each module can be reverted
4. Never mix migration with feature work in one commit

### 2. Establish Interop Boundary

> Goal: old code and Effect work side by side during the migrate

1. Wrap calls at the boundary: `Effect.tryPromise(() => promiseFn())` for Promise-based code, `Effect.try` for sync throws
2. neverthrow interop: `Result` → `Effect.succeed`/`Effect.fail`; `ResultAsync` → `Effect.tryPromise` + match — write one shared adapter helper
3. Expose Effect services back as Promises with `Effect.runPromise` when old callers aren't migrated yet
4. Put adapters in `src/adapters/` — never scatter interop code across the codebase

### 3. Migrate Modules Incrementally

> Goal: move one module at a time in leaf → root order

1. Errors: custom error classes/`Err` → `Data.TaggedError`; catch with `Effect.catchTag`/`catchTags`/`match`
2. Async: `try/catch` + `await` → `Effect.gen` + `yield*` + `Effect.tryPromise`; `ResultAsync` → `Effect` directly
3. Dependencies: constructor injection/factory params → `Effect.Service`/`Context.Tag` + `Layer`
4. Env/config: `process.env` reads → the `Config` module
5. Resources: `try/finally` cleanup → `Effect.acquireRelease`/`Scope`/`Layer.scoped`
6. Retries/timeouts: manual retry loops → `Schedule` + `Effect.retry`/`Effect.timeout`

### 4. Verify Each Step

> Goal: every migrated module typechecks and its tests pass

1. Run `bunx tsc --noEmit` after each module (do `/run-typecheck`)
2. Run that module's tests (do `/run-test`) — add `it.effect` tests for the new behavior
3. Assert error paths with `Effect.exit` + `Exit` instead of try/catch in tests
4. Runtime smoke at the entry point — confirm old callers still work through the interop boundary

### 5. Complete And Report

> Goal: summarize coverage and remaining work

1. Check `Effect.run*` remains only at the entry point — none in service code
2. If the migration isn't complete → list TODOs per module with reasons
3. Done → `/report-before-after` then `/ship`

## Rules

- Always incremental — one module at a time, separate commits, per-piece rollback
- Interop only at the boundary — never mix Promise/Result inside Effect internals or the other way
- Expected errors = `Data.TaggedError` in the error channel; leave bugs as defects (die)
- If unsure about an API/pattern → check the official docs (effect.website) or `/follow-lib-effect-ts` for the full reference

## Expected Outcome

- Migrated modules use `Effect.gen`, `Data.TaggedError`, `Layer` correctly
- Old code keeps working through the interop boundary during the migrate
- Typecheck + tests pass at every commit — rollback works per module
