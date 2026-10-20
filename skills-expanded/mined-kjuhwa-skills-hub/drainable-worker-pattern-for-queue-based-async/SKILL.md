---
name: drainable-worker-pattern-for-queue-based-async
description: Use queue-based workers with drain() signals instead of timing-sensitive sleeps for deterministic async test synchronization
category: effect-ts
version: 1.0.0
version_origin: extracted
confidence: high
tags: [effect-ts, testing, async, workers]
source_type: extracted-from-git
source_url: https://github.com/pingdotgg/t3code.git
source_ref: main
source_commit: 9df3c640210fecccb58f7fbc735f81ca0ee011bd
source_project: t3code
imported_at: 2026-04-18
evidence:
  - packages/shared/src/DrainableWorker.ts
  - apps/server/src/orchestration/Layers/ProviderRuntimeIngestion.ts
  - apps/server/src/orchestration/Layers/CheckpointReactor.ts
---

## When to Apply
- You have async work (side effects, external I/O, event processing) that needs to complete before test assertions
- Tests are timing-sensitive and flaky due to `Effect.sleep` or polling loops
- You want to avoid timers and arbitrary delays in test suites
- You're using Effect.ts with a scope-based lifecycle

## Steps
1. Define a work item type `A` representing enqueue payloads
2. Create a processing effect `(item: A) => Effect.Effect<void, E, R>` that consumes items
3. Call `makeDrainableWorker(process)` to fork a worker into your scope
4. Enqueue work via `worker.enqueue(item)` — wrapped atomically with queue state tracking
5. In tests, call `yield* worker.drain()` to block until queue is empty AND current item finishes
6. Assert after drain resolves — all queued work is complete

## Example
```typescript
const worker = yield* makeDrainableWorker((msg: Message) =>
  Effect.gen(function*() {
    yield* processMessage(msg)
  })
)

yield* worker.enqueue({ type: 'turn.start', threadId })
yield* worker.drain()  // blocks until message is fully processed
assert(someState.updated === true)
```

## Counter / Caveats
- Worker is scoped; it stops when scope closes
- Only useful if you can express side effects as Effect — not for external callbacks
- `drain()` is a transaction; concurrent enqueues may race; use in single-threaded test contexts
- Exceptional exits from process() do not drain — handle/report errors explicitly
