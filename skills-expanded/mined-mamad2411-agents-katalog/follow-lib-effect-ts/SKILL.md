---
name: follow-lib-effect-ts
description: Development guidelines with Effect-TS 3.22+ for functional programming and type-safe effects
argument-hint: "[scope]"
related:
  - follow-best-practice
  - follow-lang-typescript
  - follow-tool-vitest
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Set the standard for developing with the latest Effect-TS version for functional programming with type safety, error handling, and dependency injection

## Scope

For projects that need functional programming with Effect-TS — pick the workflow by project status:

- First-time setup (no `effect` yet) → `workflows/setup-effect/SKILL.md`
- Migrate an existing codebase (neverthrow/Promise/try-catch) to Effect incrementally → `workflows/migrate-to-effect/SKILL.md`
- If the task does not involve the `effect` package → do not use this skill

- Check the `effect` version in `package.json` before choosing APIs (v3.x vs v4 RC differ)
- Configure `tsconfig.json` for strict mode and Effect types
- Install `effect`, `@effect/platform`, `@effect/vitest`, and related dependencies
- Create the project structure per Effect architecture
- Write code with `Effect.gen`, `Effect.fn`, `Data.TaggedError`, `Context.Tag`, `Effect.Service`, `Layer`, `Schedule`, `Schema`
- Write tests with `vitest` and `@effect/vitest`

## Execute

### Workflows

| Topic | Workflow |
|-------|----------|
| Setup | `workflows/setup-effect/SKILL.md` — install, Effect/Layer/Service basics |
| Migrate | `workflows/migrate-to-effect/SKILL.md` — adopt Effect into neverthrow/promise codebase incrementally |
| Services/DI/Layer | `workflows/define-services/SKILL.md` — `Effect.Service`, `Context.Tag`, Layer composition |
| Errors/retry/Schedule | `workflows/handle-errors/SKILL.md` — `TaggedError`, `catchTag*`, `Cause`/`Exit`, timeout |
| Schema/validation | `workflows/use-schema/SKILL.md` — `Schema.Class`, decode/encode, transforms, branded |
| Concurrency/fibers | `workflows/use-concurrency/SKILL.md` — `Effect.all`, `forEach`, `fork`, race, Deferred/Queue |
| Streams/Sink | `workflows/use-stream/SKILL.md` — `Stream`, `Sink`, `Channel`, backpressure |
| Platform services | `workflows/use-platform/SKILL.md` — `FileSystem`, `HttpClient`, `Command`, runtime layers |
| Testing | `workflows/test-effect/SKILL.md` — `@effect/vitest`, `TestClock`, `Layer.mock`, `Exit` |

### 1. Detect Version And Ecosystem

> Goal: pick the API matching the effect version and the project's package manager

1. Read `package.json` → if `effect` is `3.x` use the v3 API; if `4.x` or `-rc`/`-beta` use the v4 API (see Version Notes in )
2. Detect the package manager from the lockfile (`bun.lock`/`bun.lockb` → `bun`, `pnpm-lock.yaml` → `pnpm`, `package-lock.json` → `npm`), then use the matching command
3. If the project has no `effect` yet → install the latest stable (v3.x) per step 3

### 2. Setup TypeScript Config

> Goal: configure `tsconfig.json` for strict mode and Effect types

1. Verify TypeScript version is `5.4` or newer (`bunx tsc --version`)
2. Edit `tsconfig.json` to include:
   - `strict: true`
   - `noUncheckedIndexedAccess: true`
   - `exactOptionalPropertyTypes: true`
   - `skipLibCheck: true`
   - `module: "ESNext"`/`"Preserve"` + `moduleResolution: "bundler"` or `"nodenext"` per runtime
   - `target: "ES2022"` or newer
3. (optional) Add the Effect LSP plugin in `compilerOptions.plugins`: `{ "name": "@effect/language-service" }` — must be installed per step 3 and the editor configured to use workspace TypeScript; with TypeScript `>= 7.0` use `@effect/tsgo` instead

### 3. Install Effect Packages

> Goal: install Effect-TS dependencies as needed

1. Run `bun add effect` for the core library (latest stable `3.22.2`, verified 2026-09-16) — `effect` is a runtime dependency, never add `-D`
2. `Schema` is included in core `effect` since v3.x (no separate `@effect/schema` install needed)
3. Run `bun add @effect/platform` if you need platform abstractions (`FileSystem`, `Path`, `HttpClient`, `Terminal`)
4. Run `bun add @effect/platform-bun` for the Bun runtime or `bun add @effect/platform-node` for Node.js
5. Run `bun add -D vitest@^3.2 @effect/vitest` for testing — `@effect/vitest@0.30.0` requires peer `vitest ^3.2.0`; if the project uses vitest 4/5, check peers first
6. Run `bun add -D tstyche` for type-level tests (optional)
7. Run `bun add @effect/cli` when building a CLI app, or `bun add @effect/experimental` for experimental APIs (optional)
8. (optional) Run `bun add -D @effect/language-service` for the editor LSP plugin — Effect diagnostics/quickfixes such as `floatingEffect`, `missingStarInYieldEffectGen`, `missingEffectContext`, `runEffectInsideEffect`; in a monorepo install at the root + configure in the root `tsconfig.json`; with TypeScript `>= 7.0` use `@effect/tsgo` instead

### 4. Create Project Structure

> Goal: create the folder structure per Effect architecture

1. Use `exec` to run the OS-specific command — Windows PowerShell:
   `New-Item -ItemType Directory -Force -Path src/app,src/domain,src/services,src/adapters,src/config,src/types,src/utils,test/unit,test/integration`
   or POSIX shell: `mkdir -p src/app src/domain src/services src/adapters src/config src/types src/utils test/unit test/integration`
2. Create `src/app/` for the composition root (entry point, `MainLayer`, `runMain`)
3. Create `src/domain/` for pure business logic, domain schemas, and errors
4. Create `src/services/` for service interfaces (`Tag`/`Effect.Service`) and implementations (`Layer`)
5. Create `src/adapters/` for external library wrappers
6. Create `src/config/` for runtime config with the `Config` module
7. Create `src/types/` for shared types
8. Create `src/utils/` for pure helpers
9. Create `test/unit/` for unit tests and `test/integration/` for integration tests
10. Place the entry point at `src/index.ts` or `src/app/main.ts`, then run with `Effect.runPromise`/`BunRuntime.runMain` only at the edge

### 5. Implement Effect Patterns

> Goal: write code following standard Effect patterns — full examples in  and 

1. Use `Effect.gen` + `yield*` for effect composition and `pipe` for chaining
2. Use `Effect.fn`/`Effect.fnUntraced` for named, traceable functions
3. Use `Data.TaggedError` or `Schema.TaggedError` for type-safe errors, then catch with `Effect.catchTag`/`Effect.catchTags`/`Effect.match`
4. Use `Effect.Service` (v3.9+) for services with a default layer, or `Context.Tag`/`Context.GenericTag` + `Layer.succeed`/`Layer.effect`/`Layer.scoped` for manual DI
5. Use the `Config` module (`Config.string`, `Config.number`, `Config.redacted`) for env config
6. Use `Schedule` + `Effect.retry`/`Effect.timeout` for resilience
7. Use `Effect.acquireRelease`/`Effect.scoped`/`Layer.scoped` for resource safety
8. Use `Effect.all`/`Effect.forEach` (with `concurrency` set) for concurrency and `Effect.fork` + `Fiber` for background work
9. Use `Schema` from core `effect` for data validation and `Option`/`Either` for domain values
10. Use `Stream`/`Sink` when data is streaming
11. Run effects only at the boundary: `Effect.runPromise`, `Effect.runSync`, `Effect.runFork`, `ManagedRuntime`, or `BunRuntime.runMain`
12. Add observability with `Effect.log`, `Effect.withSpan`, `Logger`, `Metric` as needed

### 6. Write Tests

> Goal: write tests with vitest and @effect/vitest — details in 

1. Use `it.effect` from `@effect/vitest` for Effect-based tests (gets `TestContext` automatically)
2. Use `it.live` when you need the live clock/environment and `it.scoped` when the test needs a `Scope`
3. Use `it.layer` to share a `Layer` across tests
4. Use `Layer.mock` (v3.17+) for partial implementations, or `Layer.succeed` + `Effect.provide` for test layers
5. Use `TestClock` to control time in tests that use `Schedule`/`Effect.sleep`
6. Assert failures with `Effect.exit` + `Exit` instead of try/catch
7. Use `tstyche` for type-level assertions (optional)
8. Run `bunx vitest run` to execute tests

### 7. Validate

> Goal: typecheck and tests pass before delivery

1. Run `bunx tsc --noEmit` until it passes
2. Run `bunx vitest run` until it passes
3. Verify no `Effect.run*` exists in library/service code (allowed only at the entry point)

## Rules

### 1. TypeScript Configuration

- Follow `/follow-lang-typescript` for the base config (strict mode, moduleResolution)

- TypeScript `5.4` or newer is required
- Must have `strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true`
- Use `moduleResolution: "bundler"` or `"nodenext"` per runtime

### 2. Imports And Dependencies

- Import by namespace from one package: `import { Effect, Schema, Layer, Context, Schedule } from "effect"`
- If using subpath imports like `import * as Effect from "effect/Effect"`, pick one style and keep it consistent across the project
- `effect` is a runtime dependency (`bun add effect`, not `-D`)
- Standalone `@effect/schema` is legacy — use `Schema` from `effect` only
- `@effect/vitest@0.30.0` requires peers `vitest ^3.2.0` and `effect ^3.22.0` — pin vitest to match before installing (setup: `/follow-tool-vitest`)

### 3. Code Patterns

- `Effect.gen` for composition; never `yield*` a non-yieldable value (`Effect`, `Option`, `Either`, `TaggedError`)
- `Data.TaggedError`/`Schema.TaggedError` for expected errors; defects (bugs) stay die in `Cause`
- `Effect.Service` (v3.9+) is the recommended way to define services; `Context.Tag`/`GenericTag` + `Layer` when you want manual control
- `Schedule` + `Effect.retry` for resilience; `Effect.timeout` for deadlines
- `Effect.acquireRelease`/`Scope`/`Layer.scoped` for resources that need cleanup
- Run (`Effect.run*`) only at the application boundary
- Requirements only through the `R` channel/Layer — never import singletons/globals directly in Effect code
- Validate external data with `Schema` — no `as T` casts at the boundary

### 4. Project Structure

- `app/` <-- domain, services, types, config (only the composition root runs effects)
- `domain/` <-- types, utils (pure, no side effects)
- `services/` <-- types, config, adapters
- `adapters/` <-- external libs only
- `types/`, `utils/` <-- no internal dependencies

### 5. Testing

- Use `vitest` + `@effect/vitest` (`it.effect`, `it.live`, `it.scoped`, `it.layer`) for Effect tests
- Use `TestClock`/`TestContext` instead of real timers and `Layer.mock` for mocks
- Use `tstyche` for type-level tests (optional)

### 6. Version Notes

- Latest stable (verified 2026-09-16): `effect@3.22.2`, `@effect/platform@0.97.2`, `@effect/platform-bun@0.91.2`, `@effect/platform-node@0.108.2`, `@effect/vitest@0.30.0`
- Effect v4 RC: `effect@rc` (`4.0.0-rc.115`, verified 2026-09-16) with major breaking changes: package consolidation (`effect/unstable/*`), `Context.Service` replaces `Context.Tag`/`Context.GenericTag`/`Effect.Service`, `Yieldable` types require `.asEffect()`, `Layer`/`Runtime` APIs changed
- TypeScript latest: `7.0.2` (native/tsgo) — `effect` requires at least `5.4`; check compatibility with the project toolchain before use; editor LSP: `@effect/language-service` supports TS `< 7` only, with TS `>= 7` use `@effect/tsgo`
- Always check the version in `package.json` before choosing APIs

- Use /follow-best-practice if needed
- Use /use-my-packages-on-registry if needed
- Use /setup-cicd if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- TypeScript config sets strict mode for Effect
- Effect libraries install successfully within peer constraints
- Project structure follows Effect architecture and dependency rules
- Code uses `Effect.gen`, `Effect.fn`, `Data.TaggedError`, `Effect.Service`/`Context.Tag`, `Layer`, `Schedule`, `Schema`
- Tests pass with `vitest` + `@effect/vitest`
- `bunx tsc --noEmit` and `bunx vitest run` all pass
