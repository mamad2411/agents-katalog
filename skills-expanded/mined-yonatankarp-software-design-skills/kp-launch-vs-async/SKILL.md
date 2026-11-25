---
name: kp-launch-vs-async
description: Use when choosing between launch and async in Kotlin coroutines — phrases like "launch vs async", "fire and forget", "awaitable", "parallel decomposition", "should I use launch or async here", "what does Deferred mean", "why is my async result ignored". Distinguishes launch (fire-and-forget, returns Job) from async (parallel computation, returns Deferred<T>) and the misuses of each.
---

## One-line summary

`launch` is fire-and-forget — it returns a `Job` you don't usually await. `async` is parallel computation — it returns a `Deferred<T>` whose `.await()` gives you the result. Use `launch` for side effects; use `async` for parallel decomposition where you need every result.

## When to use this skill

- Starting concurrent work and unsure which builder to pick.
- Code that returns `Job` where it should return `Deferred<T>`, or vice versa.
- Code review wants to know "is this `async` actually being used for parallel decomposition, or is it a mis-applied `launch`?".

## When NOT to use this skill

- Sequential, non-concurrent work — no builder needed; just call the `suspend` function.
- Switching to a different dispatcher for a single call — use `withContext`, not `launch` or `async`.

## Core content

**`launch` — fire-and-forget side effects.**

```kotlin
scope.launch {
    // side-effect work; no return value
    repository.save(order)
}
```

Returns a `Job`. The `Job` can be cancelled (`job.cancel()`) and joined (`job.join()`), but it does not carry a value. Use `launch` when the body produces a *side effect* (writes, network calls, notifications) and the caller doesn't need to consume a return value.

**`async` — parallel computation with a result.**

```kotlin
val a = scope.async { computeOne() }
val b = scope.async { computeTwo() }
val combined = a.await() + b.await()
```

Returns a `Deferred<T>`. Calling `.await()` suspends until the result is ready. Use `async` when you need a *return value* AND you want to start the computation early so it runs in parallel with other work.

**Single-async is almost always wrong.** `val x = scope.async { compute() }.await()` is just an awkward way to write `val x = compute()` — no parallelism is achieved. Reach for `async` only when there are multiple results to compute in parallel.

**Exception handling differs.** A `launch` block's failure propagates to the parent scope and crashes other coroutines (unless the scope uses a `SupervisorJob`). An `async` block's failure is also captured in the returned `Deferred`; `.await()` rethrows it. As long as the `async` is a *child* of a regular `Job`, the failure still propagates to the parent — it is not silently lost. The failure becomes truly unobservable only when the `Deferred` is a root coroutine or sits under a `SupervisorJob` *and* nobody awaits it. The practical risk: you intended supervision (or were on a `GlobalScope`-like context) and forgot to `.await()`.

**`withContext` is not `launch`.** `withContext(Dispatchers.IO) { … }` switches to a different dispatcher for a block and returns its result, but does *not* run concurrently with anything. It's not a launcher; it's a context switch.

## Decision heuristics

- "Does the result of this work matter to the caller?" Yes → `async`. No → `launch`.
- "Am I running multiple things in parallel?" Yes → multiple `async` + `awaitAll`. No → don't use `async`.
- "Do I just need to switch to a different thread for a moment?" → `withContext`.

## Anti-patterns

- `async { … }.await()` immediately on the same line — no parallelism, just `launch`-shaped overhead. Either call the `suspend` function directly or use `withContext` for a thread switch.
- `launch` where the caller actually wanted a return value — the Job carries no value; the result is silently lost.
- Root or supervised `async` whose `Deferred` is never awaited — failure is never observed by the caller and the result is discarded (under a regular parent `Job`, the failure still propagates up).
- Mixing `async` and `launch` in the same parallel-decomposition — pick one style: usually `async` for all branches and `awaitAll(jobs)`.

## See also

- `kp-coroutine-scope` — every `launch`/`async` needs a scope.
- `kp-structured-concurrency` — `coroutineScope` and `supervisorScope` for combining results.
- `kp-dispatchers` — `withContext` for context switches.
- `kp-anti-patterns` — Coroutines-related anti-patterns.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 6 (Threads and Coroutines).
- Kotlin coroutines official guide — composing suspending functions.
