---
name: follow-lib-effect-ts-use-concurrency
description: Effect concurrency — Effect.all, forEach, fibers, racing, interruption, Deferred/Queue coordination
argument-hint: "[scope]"
related:
  - follow-lib-effect-ts
  - run-test
  - resolve-errors
---

## Goal

Use Effect's concurrency primitives fully — parallel composition, fibers, racing, interruption, fiber-local coordination

## Scope

concurrent execution — `Effect.all`/`Effect.forEach`, `Effect.fork`, `Fiber`, `Effect.race`, `Deferred`/`Queue`/`Semaphore`, interruption semantics

## Execute

### 1. Parallel Composition

```ts
Effect.all([a, b, c])                          // tuple → tuple result
Effect.all({ a, b, c })                        // record → record
Effect.forEach(items, fn, { concurrency: 4 })  // bounded parallel map
Effect.all(tasks, { concurrency: "unbounded", mode: "either" })
```

- `Effect.forEach` + `concurrency` = the workhorse for batch IO
- Options: `{ concurrency: N }`, `{ batching: true }`, `{ discard: true }` (fire-and-collect-unit)
- `mode: "either"` = first success wins; `"validate"` = collect errors

### 2. Fibers

```ts
const fiber = yield* Effect.fork(work)
yield* Fiber.join(fiber)                        // wait + get result
yield* Fiber.interrupt(fiber)                   // cooperative cancel
Effect.forkDaemon(fireAndForget)                // survives parent
```

- Fiber = lightweight thread, cooperative cancellation — interruption doesn't leave state dangling
- `Effect.scoped`/`forkIn(scope)` ties the fiber lifetime to a scope

### 3. Racing And Timeouts

- `Effect.race(a, b)` — loser interrupted
- `Effect.raceAll`, `Effect.timeout`, `Effect.timeoutFail`
- `Effect.disconnect` for uninterruptible regions (critical cleanup)

### 4. Coordination Primitives

- `Deferred.make` — one-shot async value (a cancel-safe promise)
- `Queue.bounded/unbounded` — producer/consumer
- `Effect.makeSemaphore(n).withPermits` — bounded resource access
- `Ref.make` — atomic mutable state; `Ref.Synchronized` for effectful updates

## Rules

- Always bound `concurrency` when working over collections — unbounded over thousands of items = resource exhaustion
- Fire-and-forget uses `forkDaemon`/`forkScoped` explicitly — a plain `fork` ties to the parent
- Interruption is cooperative — long CPU loops need `Effect.yieldNow` to add cancel points
- Don't use raw Promise.all inside Effect — you lose interruption + the error channel

## Expected Outcome

- Parallel work bounded + cancel-safe
- Fiber lifetimes clear, coordination via Deferred/Queue/Ref
