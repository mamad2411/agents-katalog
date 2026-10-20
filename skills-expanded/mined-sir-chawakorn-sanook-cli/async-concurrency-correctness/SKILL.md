---
name: async-concurrency-correctness
description: Writes and fixes correct async/concurrent code across Python (asyncio), TypeScript (Promises), Rust (tokio), and Go (goroutines/channels), targeting deadlocks, races, cancellation, and backpressure.
when_to_use: User is writing or debugging async/await, event loops, goroutines, tokio tasks, locks, channels, or hits deadlocks, races, leaked tasks, blocked event loops, or unbounded concurrency. NOT for general code tidy-ups (use refactor-cleanup).
---

## When to Use

Reach for this skill when the code touches more than one thing happening at once and correctness depends on *ordering, timing, or shared state*:

- Writing/reviewing `async`/`await`, event loops, `goroutine`+`channel`, `tokio::spawn`, thread pools, locks, queues.
- A symptom points at concurrency: hang/deadlock, intermittent test failure, data race, "works once then stalls", leaked/zombie tasks, OOM under load, event loop "blocked" warnings, requests timing out under concurrency but fine serially.
- Adding parallelism to existing serial code (fan-out, worker pool, pipeline).

Do NOT use for single-threaded refactors, naming, or non-timing-dependent logic bugs — that's `refactor-cleanup`. If a "race" reproduces 100% deterministically serially, it's a logic bug, not a concurrency bug — stop and treat it as one.

First move: **identify the runtime model before writing a line.** The right fix differs per runtime.

| Runtime | Model | Key constraint |
|---|---|---|
| Python asyncio | single-thread cooperative loop | one blocking call freezes *everything*; CPU work needs a process, not a thread (GIL) |
| TypeScript/Node | single-thread microtask queue | sync CPU blocks the loop; `await` in a `for` serializes; unhandled rejection can crash |
| Rust tokio | M:N work-stealing (multi-thread) or current-thread | blocking a worker starves the pool; `!Send` futures can't cross threads |
| Go | M:N goroutine scheduler, preemptive | true parallelism → real data races; nil/closed channel semantics bite |

## Steps

1. **Pin the runtime + executor flavor.** asyncio (`asyncio.run`?) · tokio (`#[tokio::main]` multi-thread vs `flavor = "current_thread"`?) · Go (`GOMAXPROCS`?) · Node (worker_threads in play?). Decisions below depend on this.

2. **Get blocking work off the async path.** Anything that doesn't yield blocks the whole loop/worker:
   - asyncio: wrap sync/CPU/file-I/O in `await asyncio.to_thread(fn, ...)`; for CPU-bound use `loop.run_in_executor(ProcessPoolExecutor(), ...)` (threads won't help under the GIL).
   - tokio: `tokio::task::spawn_blocking(move || ...).await` for blocking syscalls/CPU; never call `std::thread::sleep`, blocking `Mutex` held across `.await`, or sync file I/O on a worker.
   - Node: move CPU work to a `worker_thread`; never a synchronous loop, `fs.readFileSync`, or `JSON.parse` of a huge string on the main thread.
   - Go: blocking is fine (scheduler handles it), but cap goroutines spawned around it (step 5).

3. **Never hold a sync lock across an await/yield point.** This is the #1 async deadlock.
   - asyncio: use `asyncio.Lock` (an `async with`), not `threading.Lock`, around `await`. If you must touch a `threading.Lock`, acquire→mutate→release with *zero* awaits inside.
   - tokio: use `tokio::sync::Mutex` only when the guard must survive `.await`. Otherwise prefer `std::sync::Mutex` and **drop the guard before** `.await` (scope it in a block, or `let v = *guard; drop(guard);`). Holding `std::sync::Mutex` across `.await` is a hang waiting to happen.
   - Go: `sync.Mutex` is fine but never `Lock()` then `<-ch`/another `Lock()` while holding it — order all locks consistently to kill lock-ordering deadlocks.

4. **Make cancellation and shutdown explicit.** Tasks must be reliably stoppable and joined.
   - asyncio: prefer `asyncio.TaskGroup` (3.11+) so a child failure cancels siblings and you `await` them all; use `asyncio.timeout(s)` for deadlines. Every bare `create_task` must be stored and awaited/cancelled — fire-and-forget tasks get GC'd and silently dropped. On shutdown: cancel, then `await asyncio.gather(*tasks, return_exceptions=True)`. Catch `asyncio.CancelledError`, run cleanup, then **re-raise it** — swallowing it breaks cancellation.
   - tokio: pass a `tokio_util::sync::CancellationToken` (or `select!` on a shutdown channel) into long tasks; wrap deadlines in `tokio::time::timeout`. Note a dropped `JoinHandle` does *not* cancel the task — call `.abort()` or use a `JoinSet`. Cancellation drops at the next `.await`, so keep state consistent at every await point.
   - Node: thread an `AbortSignal` into fetch/timers/streams; race work against `AbortSignal.timeout(ms)`.
   - Go: every goroutine takes `ctx context.Context` and returns on `<-ctx.Done()`; pair `context.WithTimeout`/`WithCancel` with a `defer cancel()`. Use a `sync.WaitGroup` to join before exit so you don't leak.

5. **Bound concurrency — never unbounded fan-out.** Spawning one task per input will exhaust memory/sockets/fds.
   - asyncio: gate with `asyncio.Semaphore(N)` around each unit, or process in chunks; `gather` over a *fixed* worker pool, not over N inputs.
   - tokio: `Semaphore::new(N)` + `acquire_owned`, or `buffer_unordered(N)` on a `futures::stream`.
   - Node: pool with `p-limit`/a concurrency cap; an unawaited `array.map(async ...)` fires all at once — wrap in `pLimit` or batch.
   - Go: fixed-size worker pool reading from a jobs channel (`for w := 0; w < N; w++ { go worker() }`), or a buffered semaphore channel `sem := make(chan struct{}, N)`.

6. **Channels/queues must have backpressure.** Bounded by default; unbounded queues just move the OOM downstream and hide the real throughput limit.
   - Go: `make(chan T, N)` (buffered) so producers block when consumers lag; close the channel exactly once, from the *sender* side only; never send on a closed channel. Drain or `select{ case <-ctx.Done(): }` to avoid send-blocked leaks.
   - asyncio: `asyncio.Queue(maxsize=N)`; `await queue.put` blocks the producer under load (that's the point). Use sentinel values or `task_done()`/`join()` to signal completion.
   - Rust: `tokio::sync::mpsc::channel(N)` (bounded), not `unbounded_channel`. `send().await` applies backpressure.

7. **Eliminate shared mutable state or make access correct.** Prefer message-passing/ownership over shared memory. If shared:
   - Make handlers **idempotent** (retries + at-least-once delivery will re-run them).
   - Use atomics for counters (`std::sync::atomic`, Go `atomic`, not bare `i++`); use proper guarded structures for the rest.
   - Go: protect every shared field — a single unguarded write under `-race` is a real bug, not a warning to ignore.

8. **Verify under contention, not just once** (see Verify).

## Common Errors

- **`std::sync::Mutex` guard held across `.await` (Rust):** task parks holding the lock → deadlock. Drop the guard before awaiting, or switch to `tokio::sync::Mutex`.
- **`threading.Lock` instead of `asyncio.Lock` (Python):** blocks the whole loop or deadlocks. Use the async lock around awaits.
- **Fire-and-forget `asyncio.create_task(...)` without keeping a reference:** the task can be garbage-collected mid-flight and exceptions vanish. Store it; await or cancel it; or use `TaskGroup`.
- **Swallowing `CancelledError`:** `except Exception` catches it (it's `BaseException` in 3.8+ but still easy to over-catch) — clean up and re-raise, or cancellation silently no-ops.
- **`await` inside a `for` loop when you meant parallel (JS/Python):** serializes everything. Use `Promise.all`/`asyncio.gather` — but then add a concurrency cap (step 5) so it's not unbounded.
- **`Promise.all` for fan-out with no limit:** opens thousands of connections at once. Cap it.
- **Unhandled promise rejection (Node):** crashes or silently drops the result. Always `.catch`/`try` around detached promises; add `process.on('unhandledRejection')` as a backstop, not a fix.
- **`JoinHandle` dropped expecting cancellation (tokio):** dropping does NOT abort the task — it keeps running detached. Use `.abort()` or a `JoinSet`.
- **Closing a Go channel from the receiver, or twice:** panics. Close once, from the sole sender. Sending on a closed/nil channel panics/blocks forever.
- **`select` with no `default` and no ready case (Go):** blocks forever — a silent deadlock. Add a `ctx.Done()` case.
- **Loop variable captured by goroutine pre-Go 1.22:** all goroutines see the last value. Pass it as an arg or shadow it.
- **Treating `-race` / lint warnings as noise:** a reported race is a real bug. Fix the root cause; never suppress it to make CI green.
- **CPU-bound work in `to_thread`/`spawn_blocking` expecting parallelism (Python):** GIL serializes it. Use processes for CPU.
- **Blocking call sneaking onto a tokio worker** (`reqwest::blocking`, sync `std::fs`, `std::thread::sleep`): starves the runtime. Use async equivalents or `spawn_blocking`.

## Verify

A concurrency fix isn't done until it survives contention. Don't trust a single green run.

1. **Run under the race detector / sanitizer:** Go `go test -race ./...` and `go run -race`; Rust `RUSTFLAGS="-Zsanitizer=thread"` (nightly) or at minimum `cargo test` with `tokio` `--features full` and Loom for lock-free code; Python/Node — add a stress test (below).
2. **Stress test:** run the hot path with N concurrent callers (e.g. 100–1000), repeated 100+ iterations. Flaky pass = unfixed race. In Go run with `-count=100 -race`; in async langs spawn the op `gather`/`Promise.all`/`JoinSet` with a high count and assert invariants every run.
3. **Deadlock check:** add a hard timeout to the test itself (`go test -timeout 30s`, `asyncio.timeout`, jest `testTimeout`) so a hang fails loudly instead of hanging CI.
4. **Leak check:** assert no growth in task/goroutine count after the workload settles — Go `runtime.NumGoroutine()` before/after; asyncio `len(asyncio.all_tasks())`; tokio task count via a `JoinSet`/metrics. Steady-state count must return to baseline.
5. **Backpressure check:** drive producers faster than consumers and confirm bounded memory (queue depth stays ≤ N, RSS flat) instead of unbounded growth.
6. **Cancellation check:** trigger shutdown/timeout mid-flight and assert all tasks stopped, resources released (no leaked connections/fds/locks), and no `CancelledError`/panic escaped.

Show the actual command + output as evidence. "Looks fine" is not verification for concurrency.
