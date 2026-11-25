---
name: follow-lib-effect-ts-test-effect
description: Test Effect code — @effect/vitest, Effect.runPromise, TestClock, layer mocking, Exit/Cause assertions
argument-hint: "[scope]"
related:
  - follow-lib-effect-ts
  - run-test
  - resolve-errors
  - improve
---

## Goal

Write tests for Effect programs — `@effect/vitest` integration, `Effect.runPromise`, `TestClock`, `Layer` substitution, `Exit`/`Cause` assertions

## Scope

testing Effect code — `@effect/vitest` (`it.effect`, `it.scoped`, `it.live`), deterministic `TestClock`, Layer-based fakes, `Arbitrary` property testing

## Execute

### 1. Setup

```bash
bun i -D @effect/vitest vitest
```

```ts
import { describe, it } from "@effect/vitest"
// @effect/vitest@0.30+ requires vitest ^3.2 + effect ^3.22
```

### 2. Basic Assertions

```ts
it.effect("returns todos", () =>
  Effect.gen(function* () {
    const result = yield* program
    expect(result).toEqual(expected)
  }))

it.effect("fails with NotFound", () =>
  Effect.gen(function* () {
    const exit = yield* Effect.exit(program)
    expect(Exit.isFailure(exit)).toBe(true)
  }))
```

- `it.effect` — effect test body (TestClock is provided, time ops deterministic)
- `it.live` — real clock when testing against actual timing
- `it.scoped` — tests that need a `Scope` (acquireRelease, scoped fibers)

### 3. TestClock And Time

```ts
yield* TestClock.adjust("5 seconds")   // advance deterministic clock
```

- `TestClock` = the default in `it.effect` — `Effect.sleep`/`timeout`/`retry` schedules can be tested without real waiting
- Timing-sensitive integration uses `it.live`

### 4. Layer Substitution

```ts
const TestLayer = Layer.mergeAll(
  Layer.succeed(TodoRepo, { findAll: () => Effect.succeed(fixtures) }),
  Layer.mock(HttpClient)  // partial mocks
)
it.effect("with fake repo", () => program.pipe(Effect.provide(TestLayer)))
```

- `Layer.succeed(Tag, fakeImpl)` — full replacement; `Layer.mock` — partial + defaults throw
- Platform services: `FileSystem` in-memory layers, `Terminal` capture — see `use-platform`

### 5. Property Testing

- `Arbitrary.make(Schema)` → fast-check generators from schemas — random valid inputs

## Rules

- Every test touching time → `it.effect` + `TestClock` — no `setTimeout`/real sleeps
- Mock via `Layer.succeed`/`Layer.mock` — never `vi.mock` at module level for services
- `Effect.exit`/`Exit.match` assert failures — not try/catch around runPromise
- `it.live` only when testing against real IO/timing

## Expected Outcome

- Tests deterministic via TestClock + Layer fakes
- Failure cases asserted through Exit/Cause — covering expected errors + defects
