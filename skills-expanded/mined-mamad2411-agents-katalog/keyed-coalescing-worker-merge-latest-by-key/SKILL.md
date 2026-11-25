---
name: keyed-coalescing-worker-merge-latest-by-key
description: Reduce queue backpressure by coalescing multiple updates to the same key into a single merged work item
category: effect-ts
version: 1.0.0
version_origin: extracted
confidence: high
tags: [effect-ts, workers, coalescing, optimization]
source_type: extracted-from-git
source_url: https://github.com/pingdotgg/t3code.git
source_ref: main
source_commit: 9df3c640210fecccb58f7fbc735f81ca0ee011bd
source_project: t3code
imported_at: 2026-04-18
evidence:
  - packages/shared/src/KeyedCoalescingWorker.ts
---

## When to Apply
- Multiple callers enqueue updates for the same entity (thread, file, checkpoint, etc.) in quick succession
- Each update is idempotent or can be merged into a single final state
- Queue backlog grows faster than processing, causing lag or memory pressure
- You want `drainKey(k)` to block only until that key's work is done, not all keys

## Steps
1. Define key type `K` (e.g., `ThreadId`) and value type `V` (e.g., `{ turn, state }`)
2. Implement a merge function `(current: V, next: V) => V` — usually returns `next` or merges fields
3. Define a process effect `(key: K, value: V) => Effect.Effect<void>`
4. Create worker via `makeKeyedCoalescingWorker({ merge, process })`
5. Enqueue multiple updates for same key: `yield* worker.enqueue(key, value1)`, then `enqueue(key, value2)`
6. Only one queue item per key is tracked; if key already queued, merge and replace instead of adding
7. Call `yield* worker.drainKey(k)` to block until that key has no active, queued, or pending work

## Example
```typescript
const worker = yield* makeKeyedCoalescingWorker({
  merge: (curr, next) => ({ ...curr, ...next }),  // shallow merge latest
  process: (threadId, state) => updateThreadState(threadId, state)
})

yield* worker.enqueue(threadId, { newMessage: msg1 })
yield* worker.enqueue(threadId, { newMessage: msg2 })  // merges, not queued separately
yield* worker.drainKey(threadId)  // waits for single merged update to complete
```

## Counter / Caveats
- Merge must be associative for correctness; arbitrary side-effecting merges are error-prone
- If multiple keys are active, `drainKey(k)` only waits for that key; other keys continue
- Failed process() does not mark key clean; key re-queues if updates still pending
- Useful for state updates but risky for commands with strict ordering requirements
