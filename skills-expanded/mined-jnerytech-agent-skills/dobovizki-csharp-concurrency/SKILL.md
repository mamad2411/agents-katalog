---
name: dobovizki-csharp-concurrency
description: "Knowledge base from \"C# Concurrency\" by Nir Dobovizki (Manning, 2025). Use when applying Dobovizki's frameworks for async/await, multithreading, Task/TaskCompletionSource, cancellation, thread-safe collections, deadlocks, ConfigureAwait, or IAsyncEnumerable — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# C# Concurrency
**Author**: Nir Dobovizki (Manning) | **Pages**: ~250 | **Chapters**: 14 | **Generated**: 2026-07-03

## How to Use This Skill

- **Without arguments** — load core frameworks below for reference
- **With a topic** — ask about `ConfigureAwait`, `cancellation`, `thread-safe collections`, `deadlocks`; I read the relevant chapter
- **With chapter** — ask for `ch11`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not in Core Frameworks, I read the relevant chapter file first.

---

## Core Frameworks & Mental Models

**The central insight**: `async` is a *compiler flag* that enables chunk-splitting; `await` *ends the current chunk and returns to the caller*, resuming later. Neither creates a thread. The compiler turns an async method into a state machine (same trick as `yield return`). "There is no magic — the compiler just writes code you could write yourself."

**Task = future event, Task<T> = future value.** A Task is NOT a thread or background op — it signals when one ends. Completed = `RanToCompletion | Canceled | Faulted`. Consume via `await` (best), `ContinueWith`, or `.Result`/`.Wait()` (blocking, deadlock-prone — use only to bridge legacy sync code).

**Async vs threads**: same tools (`Task`, `Task.Run`, `WhenAll`). Async I/O holds *no thread* while waiting; `Task.Run(blocking)` ties up a pool thread per op. For I/O-bound servers, async wins decisively (benchmark: 27 threads flat vs 106 climbing; 2× the connection ceiling).

**Where code after `await` runs** (real rules, in order): (1) task already complete → same thread; (2) thread has a `SynchronizationContext` (UI, ASP.NET Classic) → that context (UI→UI); (3) task has a `TaskScheduler` → that scheduler; (4) else / `ConfigureAwait(false)` → thread pool.

**The run-in-background picker**: `Thread` = long-running/needs thread properties; `ThreadPool.QueueUserWorkItem` = short/legacy; `Task.Run` = short + async-friendly.

**The lock rules for easy multithreading** (Ch 7):
1. Lock **all** shared access (reads too — memory reordering means order isn't trustworthy otherwise).
2. Same **lock order** everywhere (*lock hierarchy*) — the #1 deadlock cure.
3. Never call **foreign code** (events/delegates) while holding a lock.
4. Hold for the **entire operation** — *composing thread-safe ops is NOT thread-safe*.
5. …but hold as **briefly** as possible (else *synchronization* → *starvation*).
6. No thread **priority** or **processor affinity** changes.
Rules 4↔5 conflict: **prefer longer locks** — race conditions (wrong results) are worse than synchronization (slow). Lock a **private object**, never `lock(this)`.

**Cancellation** (`CancellationToken`): just a thread-safe, abuse-resistant flag — cooperative, not preemptive. Source triggers (`Cancel`, `CancelAfter` for timeouts, `CreateLinkedTokenSource` to combine); token only checks (`ThrowIfCancellationRequested`). Check inside long inner loops or cancellation lags. `Thread.Abort` is gone.

**TaskCompletionSource**: create and manually complete a Task (`TrySetResult`/`TrySetException`/`TrySetCanceled` — prefer `Try*`, `Set*` races). For awaitable events, background init, async data structures. `RunContinuationsAsynchronously` when completing under a lock.

**ConfigureAwait(false)**: makes `await` ignore the context → thread pool. **Library code only** (every await); **avoid in application/UI code**. Not a blanket deadlock cure — the async/blocking deadlock is best fixed with `await` instead of `.Result`. No-op on already-completed tasks; to leave a context on purpose use `Task.Run`.

**Thread-safe collections** — three families: **concurrent** (safe mutation; interface fuses check+act: `GetOrAdd`, `TryUpdate`, `TryDequeue`), **immutable** (safe by never changing — but the *reference variable* still needs sync; `ImmutableInterlocked`), **frozen** (build-once, read-hot). `BlockingCollection<T>` = own-thread producer/consumer; `Channel<T>` = async equivalent.

**Exceptions in async**: pre-first-`await` throws normally; post-`await` faults the Task. `await` throws only the *first* inner of `AggregateException`. A **forgotten `await` silently loses the exception**. `async void` → catch everything inside.

**Async iteration**: `IAsyncEnumerable<T>` + `await foreach` = async `IEnumerable`/`foreach`; `async` iterators combine `await` + `yield return` (yield outside `try`). Cancel via `.WithCancellation` + `[EnumeratorCancellation]`.

**ValueTask<T>**: return from often-synchronous hot methods to skip the Task allocation on the fast path.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-async-and-multithreading.md) | Async Programming and Multithreading | pizzeria metaphor, blocking vs nonblocking, multicore |
| [ch02](chapters/ch02-compiler-rewrites-your-code.md) | The Compiler Rewrites Your Code | closure hoisting, yield-return state machine, coroutines |
| [ch03](chapters/ch03-async-await-keywords.md) | The async and await Keywords | Task/Task\<T\>, async/await transform, async void, ValueTask |
| [ch04](chapters/ch04-multithreading-basics.md) | Multithreading Basics | Thread/ThreadPool/Task.Run, lock, deadlock, atomicity |
| [ch05](chapters/ch05-async-await-and-multithreading.md) | async/await and Multithreading | where-await-runs, lock+await, UI marshaling |
| [ch06](chapters/ch06-when-to-use-async-await.md) | When to Use async/await | decision list, contagion, cost, server benchmark |
| [ch07](chapters/ch07-classic-multithreading-pitfalls.md) | Classic Multithreading Pitfalls | the lock rules, memory reordering, race/synchronization/starvation |
| [ch08](chapters/ch08-processing-sequence-in-background.md) | Processing a Sequence in the Background | Parallel class, work queue, persistent queues |
| [ch09](chapters/ch09-canceling-background-tasks.md) | Canceling Background Tasks | CancellationToken, timeouts, linked tokens |
| [ch10](chapters/ch10-await-your-own-events.md) | Await Your Own Events | TaskCompletionSource, RunContinuationsAsynchronously, FromAsync |
| [ch11](chapters/ch11-controlling-which-thread.md) | Controlling Which Thread Code Runs | SynchronizationContext, ConfigureAwait, deadlock, Task.Yield, TaskScheduler |
| [ch12](chapters/ch12-exceptions-and-async-await.md) | Exceptions and async/await | stashed exceptions, AggregateException, lost exception, async void |
| [ch13](chapters/ch13-thread-safe-collections.md) | Thread-Safe Collections | concurrent / immutable / frozen, Channel\<T\>, ImmutableInterlocked |
| [ch14](chapters/ch14-generating-collections-asynchronously.md) | Generating Collections Asynchronously | IAsyncEnumerable, await foreach, async yield return, WithCancellation |

## Topic Index

- **AggregateException** → ch03, ch12
- **async void** → ch03, ch12
- **atomic operations** → ch04, ch07
- **await foreach / IAsyncEnumerable** → ch14
- **BlockingCollection** → ch08, ch13
- **cancellation / CancellationToken** → ch09, ch14
- **Channel\<T\>** → ch13, ch14
- **compiler transform / state machine** → ch02, ch03
- **concurrent collections** → ch13
- **ConfigureAwait(false)** → ch11
- **deadlock** → ch04, ch07, ch11
- **frozen collections** → ch13
- **immutable collections / ImmutableInterlocked** → ch13
- **Interlocked** → ch04
- **lock / lock hierarchy** → ch04, ch07
- **memory reordering / memory model** → ch07
- **Parallel class** → ch08
- **partial updates** → ch07
- **persistent / work queue** → ch08
- **race condition / synchronization / starvation** → ch07
- **SynchronizationContext** → ch11
- **Task / Task\<T\>** → ch03
- **TaskCompletionSource** → ch10
- **Task.Run / thread pool** → ch04
- **TaskScheduler / Task.Yield** → ch11
- **Thread class / thread settings** → ch04
- **UI thread** → ch04, ch05, ch11
- **ValueTask** → ch03
- **volatile** → ch07
- **where code runs after await** → ch05, ch11
- **yield return** → ch02, ch14

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — decision rules, pickers, "never do" list

---

## Scope & Limits

Covers the book's content: .NET async/await, multithreading primitives, thread-safe collections, and the async-await feature through .NET 8/9. Focused on C#/.NET. For hands-on work in your codebase, combine with project-specific tools; for topics beyond the book, check related skills or ask directly.
