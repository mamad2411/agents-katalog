---
name: kp-structured-concurrency
description: Use when designing the cancellation, failure, and lifetime relationships between multiple coroutines — phrases like "structured concurrency", "supervisorScope", "coroutineScope", "parent-child cancellation", "SupervisorJob", "one failure shouldn't cancel siblings", "await all", "first failure cancels the rest". Defines structured concurrency as the discipline of nesting coroutines under explicit scopes whose lifetimes form a tree.
---

## One-line summary

Nest coroutines under explicit scopes whose lifetimes form a tree — making cancellation, failure propagation, and resource cleanup predictable and automatic.

## When to use this skill

- Multiple concurrent operations need to coordinate: combine results, propagate cancellation, or isolate failures.
- A function spawns child coroutines and must not return until all children complete.
- Sibling failure should NOT cancel its siblings (use `supervisorScope`).
- Sibling failure SHOULD cancel its siblings ("fail fast"; use `coroutineScope`).

## When NOT to use this skill

- A single suspend call to a single suspend function — no concurrency to structure.
- Truly independent fire-and-forget work whose failure has no consequence for the rest of the program — though even then, scoping is usually worth it.

## Core content

**`coroutineScope { … }` — fail-fast group.** Runs its block within a new scope as a child of the calling scope. Suspends until *all* children complete. If any child fails, the rest are cancelled and the failure rethrows to the caller.

```kotlin
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val user = async { userRepo.find(currentUserId) }
    val orders = async { ordersRepo.recentFor(currentUserId) }
    val notifications = async { notifRepo.unread() }
    Dashboard(user.await(), orders.await(), notifications.await())
}
// If ordersRepo throws, user and notifications fetch are cancelled and
// the exception propagates to the caller. No leaked coroutines.
```

**`supervisorScope { … }` — isolated children.** Same shape as `coroutineScope`, but a child's failure does NOT cancel its siblings. Use when each child is independent and one failure shouldn't kill the others.

```kotlin
suspend fun fanOut(notifications: List<Notification>) = supervisorScope {
    notifications.forEach { n ->
        launch {
            try { send(n) } catch (e: Exception) { log.warn("failed: $n", e) }
        }
    }
}
// One bad notification doesn't cancel the rest.
```

**`SupervisorJob` for long-lived scopes.** When constructing a long-lived `CoroutineScope` (e.g., for a manager class), pass a `SupervisorJob()` so that a single child's failure doesn't tear down the whole scope.

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
```

**Cancellation propagates downward.** Cancelling a parent cancels all its children. Children check cancellation at suspension points (most coroutine library functions are cancellable). Long-running CPU work without suspension points should call `ensureActive()` or `yield()` periodically to remain cancellable.

**Cleanup with `finally` and `NonCancellable`.** Cleanup work that must run even on cancellation goes in a `finally` block. If the cleanup itself suspends, wrap it in `withContext(NonCancellable) { … }` so cancellation doesn't immediately re-cancel the cleanup.

## Decision heuristics

- Fail-fast (one failure cancels siblings, propagates up) → `coroutineScope`.
- Isolated (siblings independent, log/skip failures) → `supervisorScope` or `SupervisorJob` on a custom scope.
- For an HTTP request handler whose work must complete or fail atomically → `coroutineScope`.
- For a background fan-out where each task is independent (notifications, refreshes) → `supervisorScope`.
- Periodic CPU-bound work → call `ensureActive()` so cancellation works.

## Anti-patterns

- Using `GlobalScope` to spawn children — defeats structured concurrency; children are not tied to any meaningful lifetime.
- Manually creating a `Job`, passing it around, and forgetting to cancel it — leaks coroutines.
- Catching `CancellationException` and swallowing it — breaks cancellation propagation. If you catch it, rethrow it.
- Running uninterruptible CPU work in a coroutine without `ensureActive()` — cancellation requests are ignored until the work completes.

## See also

- `kp-coroutine-scope` — the building block; structured concurrency is about how scopes nest.
- `kp-launch-vs-async` — `async` is the natural fit inside `coroutineScope` for parallel results.
- `kp-dispatchers` — what threads the scoped work runs on.
- `kp-anti-patterns` — Coroutines-related anti-patterns including `GlobalScope` and swallowing `CancellationException`.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 8 (Designing for Concurrency).
- Roman Elizarov, "Structured concurrency" (Medium, 2018) — foundational article.
- Kotlin coroutines official guide — coroutine context, structured concurrency, and exception handling.
