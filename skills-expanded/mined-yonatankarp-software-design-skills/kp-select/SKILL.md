---
name: kp-select
description: Use when waiting on whichever of several suspending sources is ready first — phrases like "select expression", "Kotlin select", "race between channels", "pick first to complete", "timeout vs result", "multiplex channels and deferreds", "biased select". Defines the `select { … }` expression as the coroutine equivalent of a non-blocking poll across multiple suspending sources (channels, deferreds, timeouts) — taking whichever clause becomes ready first.
---

## One-line summary

A `select { … }` expression suspends on multiple suspending clauses (channel receives, deferred awaits, timeouts) at once and resumes when the first one becomes ready — coroutine-safe, biased toward declaration order.

## When to use this skill

- Multiplexing across several channels: "wait for input from any of these sources".
- Racing several `Deferred<T>` and acting on the first to finish (other branches naturally lose).
- Implementing a timeout: select between the real operation and an `onTimeout` clause.
- Building a non-blocking poll across channel state without locking up the calling coroutine.

## When NOT to use this skill

- A single source — `await`, `receive`, or `delay` directly. `select` adds ceremony for no benefit.
- "Pick the latest" semantics on a `Flow` → use `flatMapLatest`, not `select`.
- Choosing between alternative algorithms (no timing involved) → `when` on a config flag.

## Core content

```kotlin
suspend fun firstReady(a: ReceiveChannel<Int>, b: ReceiveChannel<Int>): Int = select {
    a.onReceive { it }
    b.onReceive { it }
    onTimeout(5_000) { -1 }
}
```

When any clause becomes ready (a value arrives on `a`, a value arrives on `b`, or 5 seconds elapse), `select` resumes and runs the corresponding lambda. The lambda's return becomes the `select` expression's value.

**Common clauses.**

- **`ch.onReceive { v -> … }`** — receive a value from a channel; the lambda gets the value.
- **`ch.onReceiveCatching { result -> … }`** — channel variant that surfaces close as a value rather than throwing.
- **`def.onAwait { v -> … }`** — await a `Deferred<T>`; the lambda gets the result.
- **`ch.onSend(value) { … }`** — send a value to a channel; the lambda runs if the send succeeded.
- **`onTimeout(d) { … }`** — fire after duration `d` if no other clause is ready.

**Bias.** `select` is *biased* toward the first clause declared when multiple clauses are simultaneously ready. Use deliberately — order your clauses by priority.

**Single-shot.** `select { … }` fires exactly once, then completes. To loop over events from multiple sources, wrap the `select` in a `while (isActive) { … }`.

```kotlin
while (isActive) {
    select<Unit> {
        commands.onReceive { handle(it) }
        ticker.onReceive { tick() }
    }
}
```

## Decision heuristics

- Reach for `select` only when you have ≥2 *suspending* sources to wait on. With one source, the direct call is clearer.
- Use `onTimeout` for soft timeouts where you want a fallback value; for hard timeouts that cancel the entire operation, use `withTimeout` instead.
- Biased ordering means hot sources can starve cold sources. Mix in a random shuffle, a round-robin, or `onTimeout` if starvation matters.

## Anti-patterns

- Using `select` for a single source — adds ceremony with no benefit.
- Heavy work inside `select` clauses — clauses should be tiny dispatchers; do the actual work after `select` returns.
- Mutating shared state in clauses without synchronization — race conditions across clauses.
- Long-running `select` loops without a cancellation check — make sure the loop body honours `isActive` or yields periodically.

## See also

- `kp-channels` — `select` is most useful over channels.
- `kp-launch-vs-async` — `onAwait` lets `select` multiplex over `Deferred<T>`.
- `kp-structured-concurrency` — combining `select` with `coroutineScope` for clean cancellation.

## References

- *Kotlin Coroutines* (Marcin Moskała) — dedicated section on the `select` expression.
- Kotlin coroutines official guide — select expression.
