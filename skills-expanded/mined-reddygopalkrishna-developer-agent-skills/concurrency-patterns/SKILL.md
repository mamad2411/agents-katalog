---
name: concurrency-patterns
description: Finds and fixes race conditions, lost updates, deadlocks and async bugs using atomic operations, optimistic or pessimistic locking, database constraints and race detectors. Use when code runs in threads, async tasks, goroutines, background workers or multiple service instances, when duplicates or double charges appear, when a test fails only under load, or when reviewing check-then-act logic. Not for designing distributed workflows (see resilience-patterns and event-driven-architecture).
license: MIT
---

# Concurrency Patterns

Most concurrency bugs come from shared mutable state that more than one actor (thread, task, process, request, service instance) touches without a single owner. Remove the sharing first, make what remains atomic second, and prove the fix with a race detector or a stress test. "It passed when I ran it" proves nothing.

## When to use

- Duplicate rows, double charges, double emails, lost updates, counters that drift.
- Deadlocks, hangs, or timeouts that appear only under load.
- Tests that fail intermittently and pass on rerun (see test-strategy for flaky tests in general).
- Writing threaded, async, or worker-queue code, or code that runs on several instances at once.
- Reviewing "check, then act" logic: `if not exists: create`, `if balance >= x: withdraw`.

Single-threaded runtimes are not exempt. Node.js and Python asyncio interleave at every `await`, and two instances of any service race on the same database rows.

## Workflow

1. **List the shared state.** Every piece of mutable state reachable by two concurrent actors: fields, globals, in-memory caches, database rows, files, queues, external resources (a payment provider). Count every instance of the service, not just threads in one process.
2. **Write the invariant for each** in one sentence: "a balance never goes negative", "one active subscription per user", "each job is processed once".
3. **Find the race shapes** using the table below. Pay most attention to code that reads a value, decides, then writes.
4. **Choose a strategy** using the strategy table. Prefer the highest row that works.
5. **Implement with bounded waits.** Every lock acquisition and every wait has a timeout.
6. **Reproduce, then fix.** Write a test that runs the operation concurrently and fails before the fix. Run the race detector where one exists. Then apply the fix and rerun many times.
7. **Review every async boundary.** After each `await`/suspension point, assume other code ran and the state you read before may have changed.

## Race shapes

| Shape | Example | Fix |
| --- | --- | --- |
| Check-then-act | `if not user_exists(email): create_user(email)` | Unique constraint plus handling the duplicate error, or an atomic upsert |
| Read-modify-write | `b = get_balance(); set_balance(b - 10)` | Atomic statement (`UPDATE ... SET balance = balance - 10 WHERE id = ? AND balance >= 10`), atomic increment, or optimistic version check |
| Lazy initialization | `if client is None: client = connect()` | The language's once primitive or a lock around init (Go `sync.Once`, C# `Lazy<T>`, Java holder-class idiom) |
| Iterating while mutating | One thread iterates a list/map while another modifies it | Concurrent collection, copy-on-write snapshot, or one lock for both |
| Lost update between users | Two people edit the same record; the last save silently wins | Optimistic concurrency with a version or ETag; return 409 or 412 on conflict |
| Duplicate processing | Two workers take the same job; a retry re-runs a finished job | `FOR UPDATE SKIP LOCKED`, idempotency keys, unique constraint on processed message IDs |
| Publishing before ready | Another thread sees a half-built object or a flag set before data is written | Build fully, then publish through a thread-safe handoff (queue, atomic reference, lock) |

## Choosing a strategy

| Strategy | Use when | Cost |
| --- | --- | --- |
| Eliminate sharing: immutability, confinement to one owner, message passing / actors, partitioning by key | Design time; the most robust choice | Restructuring |
| Database constraint or single atomic statement | The invariant is about persisted data | Must handle the constraint error |
| Optimistic concurrency (version column, compare-and-swap, `If-Match`) | Conflicts are rare; user-facing edits | Retry loop or conflict UX |
| Pessimistic lock (mutex, `SELECT ... FOR UPDATE`, advisory lock) | Conflicts are common and the critical section is short | Contention, deadlock risk |
| Distributed lock (Redis, etcd, ZooKeeper, database advisory lock) | Cross-process coordination with no row to lock | Hard to get right: leases expire while a holder is paused, so the resource must check a fencing token. Prefer constraints and idempotency |

## Database-level patterns

- **Atomic conditional update**, then check the affected row count:

  ```sql
  UPDATE accounts SET balance = balance - 10
  WHERE id = 42 AND balance >= 10;   -- 0 rows affected = insufficient funds
  ```

- **Optimistic concurrency** with a version column:

  ```sql
  UPDATE documents SET body = :body, version = version + 1
  WHERE id = :id AND version = :expected_version;   -- 0 rows = someone else saved first
  ```

  ORMs support this directly (JPA `@Version`, EF Core concurrency tokens, Rails `lock_version`).

- **Pessimistic lock** inside a short transaction: `SELECT ... FROM accounts WHERE id = 42 FOR UPDATE`. Never make network calls or wait for user input while holding it.
- **Work queues**: `SELECT id FROM jobs WHERE status = 'ready' ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED` lets many workers take different jobs without blocking each other (PostgreSQL 9.5+, MySQL 8.0+).
- **Unique constraints are the last line of defense.** Combine with `INSERT ... ON CONFLICT DO NOTHING` (PostgreSQL) or `INSERT ... ON DUPLICATE KEY UPDATE` (MySQL) for idempotent inserts.
- **Isolation levels**: defaults differ (PostgreSQL uses Read Committed, MySQL InnoDB uses Repeatable Read). Neither prevents a lost update when the read-modify-write happens in application code. `SERIALIZABLE` prevents these anomalies but transactions can fail with serialization errors (SQLSTATE `40001`), and the whole transaction must be retried.
- **Advisory locks** (PostgreSQL `pg_advisory_xact_lock(key)`) coordinate work that has no natural row, and are released when the transaction ends.

## Deadlocks

- Acquire multiple locks in one global order (for example by ascending ID) everywhere in the code.
- Keep critical sections short. No I/O, RPC, logging to remote sinks, or callbacks into unknown code while holding a lock.
- Use timeouts: `tryLock(timeout)` style APIs, PostgreSQL `lock_timeout`, MySQL `innodb_lock_wait_timeout`.
- Databases detect deadlocks and abort one transaction. Catch that error and retry the transaction a bounded number of times with backoff.
- Async deadlocks look different: blocking on async code from sync code (C# `.Result`), awaiting while holding a non-async lock, or goroutines waiting on each other's channels. See the language reference.

## Async rules for every ecosystem

- Every `await` is a point where other tasks run. Re-check state after it instead of trusting values read before it.
- Never block the event loop or a shared thread pool with synchronous I/O or long CPU work. Move it to a worker thread or process.
- Every spawned task is awaited, joined, or owned by a supervisor that logs its errors. No silent fire-and-forget.
- Bound fan-out. `Promise.all` over 10,000 items starts 10,000 requests at once; use a semaphore or worker pool.
- Propagate cancellation and deadlines (`AbortSignal`, `context.Context`, `CancellationToken`, asyncio timeouts) so abandoned work stops.

Read [references/language-pitfalls.md](references/language-pitfalls.md) when working in JavaScript/TypeScript, Python, Java/Kotlin, C#/.NET, Go or Rust; it lists the specific traps and primitives for each.

## Testing concurrent code

- **Race detectors**: Go `go test -race ./...`; ThreadSanitizer (`-fsanitize=thread`) for C, C++ and other LLVM-based toolchains that support it. They only report races that actually happen during the run, so pair them with stress tests.
- **Stress tests**: start N actors behind a barrier or latch so they hit the critical section at the same moment (`CountDownLatch`, `Barrier`, `Promise.all`, `asyncio.gather`), repeat many times, then assert the invariant (total balance unchanged, exactly one row created). In Go: `go test -race -count=500 -run TestTransfer ./...`.
- **Systematic or model-checking tools** explore interleavings deterministically: jcstress (Java), loom (Rust), Coyote (.NET). Go also has `testing/synctest` for code that uses time and goroutines (generally available since Go 1.25; Go 1.24 had only an experimental API behind `GOEXPERIMENT=synctest`); check the `go` directive in `go.mod`.
- **Database races need real transactions.** Test with two real connections against a real database (for example in a container), not with mocks.
- Keep the failing stress test as a regression test, with an iteration count that runs in CI in reasonable time.

## Anti-patterns

- **Fixing a race with `sleep`.** It only changes the timing; the race remains.
- **One global lock around everything.** It serializes the system and hides the real invariant.
- **Check-then-act in application code with no database constraint behind it.**
- **Holding a lock across I/O or `await`.**
- **"It's single-threaded, so no races."** Interleaving at `await` and multiple instances still race.
- **Double-checked locking without correct memory semantics** (in Java the field must be `volatile`).
- **Distributed locks treated as perfect mutual exclusion** without lease handling or fencing tokens.
- **Unbounded retries on deadlock or serialization errors.**
- **Background tasks whose exceptions are never observed.**

## Done when

- Shared state and invariants are listed, and each is protected by a named mechanism (constraint, atomic statement, version check, lock, single owner).
- A concurrent test reproduced the bug before the fix and passes repeatedly after it; the race detector (where available) is clean.
- Every lock has a timeout and a consistent acquisition order; no I/O happens under a lock.
- Every background task is awaited or supervised, and its errors reach logs or metrics.
- Invariants on persisted data are enforced by the database, not only by application code.

## References

- [references/language-pitfalls.md](references/language-pitfalls.md) — read for the language you are working in: traps, primitives, and tooling.
