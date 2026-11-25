---
name: kp-actor-pattern
description: Use when confining mutable state behind a single coroutine that receives messages via a channel — phrases like "actor pattern", "actor model", "confine state to one coroutine", "single-threaded state via channel", "Mutex vs actor", "serialize access to state". Defines the actor pattern in Kotlin coroutines as a coroutine that owns mutable state and accepts mutation requests as messages, eliminating shared-state concurrency without explicit locks.
---

## One-line summary

Hide mutable state inside one coroutine; let the outside world send it messages on a channel. The coroutine processes one message at a time, so the state is implicitly single-threaded — no locks needed.

## When to use this skill

- Coordinating concurrent updates to a small piece of state (counters, caches, in-memory aggregates, session state).
- Replacing a `Mutex` + `var` setup when the operations on the state are clearly enumerable as a small set of message types.
- Modeling a stateful service whose state evolves through a stream of commands (`AddItem`, `RemoveItem`, `Clear`, …).
- When `StateFlow` isn't quite right because the state needs *commands*, not just observation.

## When NOT to use this skill

- The state is observed by many consumers but rarely updated → `StateFlow` is simpler.
- Operations are independent enough that no coordination is needed → no actor required.
- The state is genuinely complex with many invariants → consider whether a proper data structure with internal locking would be clearer.

## Core content

The shape:

```kotlin
sealed interface CounterMsg {
    data class Add(val n: Int) : CounterMsg
    data class Get(val reply: CompletableDeferred<Int>) : CounterMsg
}

fun CoroutineScope.counterActor(): SendChannel<CounterMsg> {
    val ch = Channel<CounterMsg>()
    launch {
        var count = 0
        for (msg in ch) when (msg) {
            is CounterMsg.Add -> count += msg.n
            is CounterMsg.Get -> msg.reply.complete(count)
        }
    }
    return ch
}

// Usage:
val actor = scope.counterActor()
actor.send(CounterMsg.Add(3))
val reply = CompletableDeferred<Int>()
actor.send(CounterMsg.Get(reply))
println(reply.await())   // 3
```

Three parts:
1. **A sealed message type.** Each variant is one operation the actor supports. Sealed-class enables exhaustive `when` — the compiler enforces every message gets handled.
2. **A coroutine owning the state.** Declared as a `var` (or any mutable structure) *inside* the launched coroutine. Outside code has no reference to it.
3. **An external channel.** Senders ship messages; the actor's `for (msg in ch)` loop processes them one at a time.

**Replies via `CompletableDeferred`.** For query messages, the sender includes a `CompletableDeferred<T>` that the actor completes; the sender then `await()`s. Avoids leaking a return channel.

**Why this works.** The actor's coroutine processes one message at a time. Within the actor, the state is single-threaded — no race conditions, no locks, no `volatile`. Concurrency happens at the message boundary, not inside.

**The deprecated `actor { … }` coroutine builder.** Kotlin once shipped an `actor { … }` builder; it's been deprecated. Build the pattern by hand as shown above — it's not much more code.

## Decision heuristics

- Actor is the right tool when you can enumerate the operations on state as a finite, named set (a sealed message hierarchy).
- For "read often, write rarely" state shared across many readers → `StateFlow`, not actor.
- For "many writers, occasional reader" → actor.
- Keep the message vocabulary small. If the sealed hierarchy grows past ~6 variants, reconsider the design.
- Use `Channel.UNLIMITED` only if you're certain the actor can keep up; otherwise prefer `BUFFERED` so back-pressure is visible.

## Anti-patterns

- Exposing the internal state via a "give me the reference" message — defeats confinement; callers now have shared-state access.
- Letting the actor block on long external operations — other messages pile up. Spawn child coroutines for the slow part, keep the actor's main loop snappy.
- Unbounded-capacity channels under sustained load — heap blows up.
- Two actors talking back and forth synchronously — easy path to deadlock. Design message flows acyclically when possible.

## See also

- `kp-channels` — the message-passing primitive actors use.
- `kp-sealed-when` — the message type is a sealed hierarchy with exhaustive `when`.
- `kp-select` — useful when an actor needs to wait on multiple sources (commands plus timers, for example).
- `kp-flow-cold-vs-hot` — when shared *observable* state is the real need, `StateFlow` beats actor.
- `gof-state` — actor often hosts a state machine internally.

## References

- *Kotlin Coroutines* (Marcin Moskała) — actor pattern chapter.
- Kotlin coroutines official guide — shared mutable state and concurrency, "actors" subsection.
