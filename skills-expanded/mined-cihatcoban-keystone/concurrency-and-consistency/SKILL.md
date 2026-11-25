---
name: concurrency-and-consistency
description: Handles shared mutable state correctly - races, locks, transaction isolation, lost updates, async correctness. Triggers - two requests update the same row and lose data, race condition, which isolation level, deadlock, optimistic locking, test fails intermittently under load, double submit.
---

# Concurrency and Consistency

Concurrency bugs are the most expensive class of defect: they pass every test,
survive review, appear under load, and cannot be reproduced on demand. They are
not found by care — they are prevented by design. "We'll be careful with this
shared state" is not a strategy.

## First: eliminate rather than manage

Ranked by reliability:

1. **No shared mutable state.** Immutable values, pure functions, message
   passing. A race requires shared mutability; remove one and the class of bug
   is gone.
2. **Confine ownership.** One owner (one thread, one actor, one partition key)
   for each piece of mutable state. Others send messages, never reach in.
3. **Let the database arbitrate.** A unique constraint, conditional update or
   atomic counter is correct under concurrency for free. Application-level
   coordination is the fallback, not the default.
4. **Lock, carefully.** Last resort — locks introduce deadlock, priority
   inversion and contention.

## The canonical bug: read-modify-write

```text
  T1: read balance (100) ─────────┐
  T2: read balance (100) ───┐     │
  T2: write 100 - 30 = 70 ──┘     │
  T1: write 100 - 50 = 50 ────────┘     → the 30 withdrawal vanished
```

Every "the count is slightly wrong" bug is this. Three correct fixes:

| Fix | Form | Best for |
|---|---|---|
| Atomic operation | `UPDATE accounts SET balance = balance - 30 WHERE id = ? AND balance >= 30` | Simple arithmetic; always prefer this |
| Optimistic lock | `UPDATE ... WHERE id = ? AND version = ?` → 0 rows means conflict, retry | Low contention, long think-time (user editing a form) |
| Pessimistic lock | `SELECT ... FOR UPDATE` inside a transaction | High contention, short critical section |

Check the affected row count. An optimistic update that silently updates zero
rows and returns success is worse than the original bug.

## Isolation levels: what they do not prevent

| Level | Prevents | Still possible |
|---|---|---|
| Read committed (common default) | Dirty reads | Non-repeatable reads, phantoms, **lost updates** |
| Repeatable read / snapshot | + non-repeatable reads | Phantoms (engine-dependent), write skew |
| Serializable | All of the above | Nothing — but expect conflicts and retries |

Two consequences engineers routinely miss:

- **Read committed does not protect a read-modify-write.** Most application
  defaults sit here. Your `SELECT` then `UPDATE` is unsafe unless you use one
  of the three fixes above.
- **Write skew** survives snapshot isolation: two transactions read an
  overlapping set, each checks an invariant that holds for its own view, both
  write, and the invariant is now violated (the classic "at least one doctor
  on call" bug). Snapshot isolation will not save you; serializable, an explicit
  lock, or materializing the conflict will.

Whatever level you choose, **serialization failures are normal** — the
application must catch and retry them.

## Locking rules

- **Order locks consistently.** Deadlock requires a cycle; a global ordering
  (always by ascending id) makes cycles impossible.
- **Hold locks briefly, never across I/O.** A lock held during an HTTP call
  converts a slow dependency into a system-wide stall.
- **Set a lock timeout.** Waiting forever is not resilience.
- **Distributed locks are advisory, not guarantees.** A lease can expire while
  the holder still believes it holds it (GC pause, network partition). Use a
  fencing token that the resource validates, or design the protected operation
  to be idempotent so a double execution is harmless.

## Async and parallel code

- Do not mix blocking calls into an async runtime. One blocking call in an
  event loop stalls every other task on it.
- Unbounded concurrency (`spawn` per item over a large list) exhausts
  connections, memory or the downstream service. Bound it with a semaphore or
  worker pool.
- Cancellation must be propagated; an orphaned task holding a connection is a
  leak that only appears under load.
- Fire-and-forget hides failures. Either await the result or send it somewhere
  that is monitored.
- Async does not make code parallel, and it does not remove races — it changes
  where the interleaving points are.

## Idempotency at the entry point

Users double-click and mobile clients retry. The HTTP layer needs the same
protection as the data layer: an idempotency key or a natural unique
constraint, not a disabled button.

## Testing

- Deterministic first: unit-test the conflict path directly (simulate a version
  mismatch, assert the retry happens and converges).
- Concurrency test: N parallel workers against one row; assert the invariant
  holds and the final value is exact. Run it in CI — this catches the common
  cases cheaply.
- An intermittent test failure is a **report of a real race**, in the test or
  the code. Never retry it into green; quarantine and investigate. Retrying
  flaky tests is how races reach production.

## Exit checklist

- [ ] No read-modify-write without an atomic operation, version check or lock
- [ ] Affected row counts are checked on conditional updates
- [ ] Isolation level is chosen explicitly and its gaps are known
- [ ] Serialization failures are caught and retried at a sensible layer
- [ ] Locks: consistent ordering, timeouts, never held across I/O
- [ ] Distributed locks use fencing or the operation is idempotent
- [ ] Concurrency is bounded everywhere tasks are spawned
- [ ] A parallel test exercises the contended path
