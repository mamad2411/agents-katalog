---
name: kp-dispatchers
description: Use when choosing which dispatcher to run coroutines on — phrases like "Dispatchers.Default vs IO vs Main", "withContext", "which thread pool", "blocking IO in coroutines", "CPU-bound coroutine", "Unconfined dispatcher", "should I switch dispatchers here". Distinguishes the four built-in dispatchers and the picking criteria.
---

## One-line summary

Pick a dispatcher whose thread-pool characteristics match the work — `Default` for CPU-bound, `IO` for blocking I/O, `Main` for UI updates, `Unconfined` only when you really mean "stay on whatever thread called me".

## When to use this skill

- Designing a suspending function whose work has specific concurrency characteristics (CPU-heavy, blocking I/O, UI-bound).
- Code that mixes blocking calls with coroutines and risks starving a thread pool.
- Switching dispatchers mid-computation with `withContext`.
- Code review wants to verify dispatcher choices are deliberate.

## When NOT to use this skill

- The work is a single `suspend` call to another `suspend` function — usually no dispatcher choice needed.
- The code already runs in a dispatcher-aware framework primitive (`viewModelScope` defaults to `Main.immediate`).

## Core content

**`Dispatchers.Default`** — a thread pool sized for CPU cores (typically `max(2, #cores)`). Use for CPU-bound computation (parsing, transformation, mathematical work). Saturating it is OK — those threads are the right size for the machine.

**`Dispatchers.IO`** — a larger thread pool (default 64+) optimized for blocking I/O. Use when calling JDBC, file I/O, blocking HTTP clients, or any code that calls `Thread.sleep` / blocks. Threads here can sleep without starving CPU work.

**`Dispatchers.Main`** — single-threaded, ties to the UI thread on platforms with one (Android, JavaFX, Swing). Use for UI updates. Calls suspend; doesn't block the UI thread between suspensions. `Main.immediate` skips the dispatch if already on Main.

**`Dispatchers.Unconfined`** — runs on whatever thread invoked the coroutine until the first suspension; afterwards, on whatever thread resumes it. Unpredictable. Use for tests of a coroutine's logic (when the thread doesn't matter) and rarely in production. Soshin warns about it.

**`withContext` for switching.** Inside a suspend function, `withContext(Dispatchers.IO) { … }` runs the block on the IO dispatcher and switches back when done. This is the idiomatic way to write a suspend function whose body needs a specific dispatcher.

```kotlin
suspend fun loadUser(id: UserId): User = withContext(Dispatchers.IO) {
    database.query("SELECT * FROM users WHERE id = ?", id)  // blocking JDBC
}
```

The caller doesn't need to know which dispatcher the function uses — the function picks the right one for its work.

**Custom dispatchers.** For very specific needs (single-threaded queue, work-stealing pool with a custom size), use `Executors.newSingleThreadExecutor().asCoroutineDispatcher()` or similar. Document why a custom dispatcher is needed; built-ins serve most cases.

## Decision heuristics

- CPU-bound (computation, parsing, transforming data in memory) → `Default`.
- Blocking I/O (JDBC, blocking HTTP, file I/O) → `IO`.
- UI updates → `Main`.
- Don't use `Unconfined` in production unless you have a documented reason.
- Always wrap blocking calls in `withContext(Dispatchers.IO)` — otherwise you're starving the dispatcher you're on.

## Anti-patterns

- Running blocking JDBC / blocking HTTP on `Default` — starves the CPU dispatcher, kills throughput.
- `Dispatchers.Unconfined` in production — unpredictable thread, hard-to-reproduce bugs.
- `withContext(Dispatchers.Main)` for non-UI work on a server — pinning to a single thread for no reason.
- Manually switching dispatchers inside `launch`/`async` instead of using `withContext` — extra indirection without benefit.

## See also

- `kp-coroutine-scope` — scope's default dispatcher.
- `kp-launch-vs-async` — `withContext` vs `launch`/`async`.
- `kp-anti-patterns` — Coroutines anti-patterns.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 6 (Threads and Coroutines).
- Kotlin coroutines official guide — coroutine context and dispatchers.
