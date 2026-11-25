---
name: kp-coroutine-scope
description: Use when working with Kotlin coroutine lifecycle and scope ownership — phrases like "CoroutineScope", "where should I launch this coroutine", "GlobalScope considered harmful", "viewModelScope", "lifecycleScope", "coroutine leaks", "who cancels these coroutines". Defines CoroutineScope as the owner of a coroutine's lifecycle — and the discipline of attaching every coroutine to a scope whose cancellation matches the work's natural lifetime.
---

## One-line summary

Every coroutine belongs to a `CoroutineScope`. The scope owns the coroutine's lifecycle — when the scope is cancelled, the coroutine is cancelled. Choosing the right scope is the most common Coroutines design decision.

## When to use this skill

- Launching a coroutine and unsure which scope to attach it to.
- Coroutines outliving their useful work (running after the screen closes, the request returns, the test finishes) — a scope-ownership problem.
- Code that uses `GlobalScope` — almost always wrong; this skill explains the alternatives.
- Test setup that leaks coroutines into other tests.

## When NOT to use this skill

- A single `suspend` function called directly from another `suspend` function — no `launch` needed.
- The work is a one-shot transform that does not need to outlive the call — use `withContext` instead of `launch`.

## Core content

**Scopes are lifecycle anchors.** A `CoroutineScope` is created with a `Job` (or `SupervisorJob`) and a `CoroutineContext`. When the job is cancelled, every coroutine launched from the scope is cancelled. Structured concurrency depends on this.

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
scope.launch { … }       // runs until scope is cancelled or finishes
scope.cancel()           // cancels every coroutine launched from this scope
```

**Common pre-built scopes.**

- **`viewModelScope`** (Android ViewModel) — cancelled when the ViewModel is cleared. Use for UI-related work that should die with the screen.
- **`lifecycleScope`** (Android Lifecycle) — cancelled when the lifecycle owner is destroyed.
- **`runBlocking { … }`** — creates a scope that blocks the calling thread until all coroutines complete. Useful in `main()` and tests; never use in production server code.
- **`coroutineScope { … }`** — runs a block within the *current* scope, propagating cancellation. The block returns after all child coroutines complete. This is the *structured concurrency* primitive.
- **`supervisorScope { … }`** — like `coroutineScope` but children's failures don't cancel siblings.

**`GlobalScope` is almost always wrong.** It has no lifetime, so coroutines launched in it outlive everything. Use it only for true application-wide background work that genuinely should outlive every component (rare in practice). Most code that reaches for `GlobalScope` would be served better by a scope tied to the work's natural lifetime.

**Custom scope.** When no pre-built scope fits, create one tied to the lifetime of the component that owns the work:

```kotlin
class CartManager {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    fun start() { scope.launch { … } }
    fun stop() { scope.cancel() }
}
```

The component that owns the scope is responsible for cancelling it.

## Decision heuristics

- Match the scope's lifetime to the work's natural lifetime. Work that should die with the screen → `viewModelScope` / `lifecycleScope`. Work that should die with a component → a scope the component owns.
- If you're tempted to use `GlobalScope`, stop and ask "what is the actual lifetime?" Usually there's a better answer.
- For one-shot work that finishes before returning, use `withContext { … }`, not `launch { … }`.
- Never use `runBlocking` inside a coroutine or a Web request handler — blocks the thread, defeats the point.

## Anti-patterns

- `GlobalScope.launch { … }` for work that has a natural shorter lifetime — coroutine leaks, work continues after it's no longer needed, results silently discarded.
- Creating a `CoroutineScope` but never cancelling it — same as `GlobalScope` in practice.
- `runBlocking` in production server code — blocks an HTTP worker thread.
- Mixing scopes by manually constructing `Job` and passing it around — leads to "who owns the job" confusion. Let scopes own their jobs.

## See also

- `kp-launch-vs-async` — once you have a scope, which builder to use.
- `kp-structured-concurrency` — `coroutineScope` and `supervisorScope` for nested scopes.
- `kp-dispatchers` — picking the right dispatcher within a scope.
- `kp-anti-patterns` — Coroutines-related anti-patterns and how to spot them.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 6, 8 (Threads and Coroutines; Designing for Concurrency).
- Roman Elizarov's "Structured concurrency" (Medium, foundational article).
