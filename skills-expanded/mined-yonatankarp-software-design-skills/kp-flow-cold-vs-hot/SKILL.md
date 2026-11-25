---
name: kp-flow-cold-vs-hot
description: Use when choosing between Flow, SharedFlow, and StateFlow — phrases like "cold flow vs hot flow", "Flow vs SharedFlow vs StateFlow", "replay cache", "should I use StateFlow for this UI state", "events vs state", "Flow re-runs every time", "shared flow buffer", "state flow current value". Defines the three Kotlin stream primitives and the picking criteria.
---

## One-line summary

`Flow` is cold (re-runs per collector), `SharedFlow` is hot and broadcast (no required current value, optional replay), `StateFlow` is hot and conflates (always has a current value). Pick by *what the consumer needs*: a fresh execution, an event stream, or current state.

## When to use this skill

- Designing an API that exposes a stream of values.
- Refactoring callback-based code into a coroutines-friendly stream.
- Confusion between which Flow variant to use for a given use case (UI state, server-sent events, periodic polling, etc.).

## When NOT to use this skill

- A single async value — use `suspend fun` or `Deferred<T>`.
- A bounded list of values that's available all at once — use `List<T>` or `Sequence<T>`.

## Core content

**`Flow<T>` — cold.** Lazy by construction; the producing code runs only when a collector starts collecting, and re-runs from scratch for each new collector. Each collector gets its own independent run.

```kotlin
val temperatures: Flow<Reading> = flow {
    while (true) {
        emit(sensor.read())
        delay(1.seconds)
    }
}
// Collecting twice = two independent sensor-reading loops.
```

Use Flow when:
- The work to produce values is the same per consumer (and you want a fresh run each time).
- The stream represents a query or a transformation pipeline.
- There's no concept of "current value" to share.

**`SharedFlow<T>` — hot, broadcast.** A single producing path; all collectors see the same emissions. Has no required current value. Optionally buffers and replays past emissions to late subscribers.

```kotlin
class NotificationBus {
    private val _events = MutableSharedFlow<Notification>(replay = 0, extraBufferCapacity = 64)
    val events: SharedFlow<Notification> = _events.asSharedFlow()
    suspend fun publish(n: Notification) = _events.emit(n)
}
```

Use SharedFlow when:
- Multiple subscribers must see the same emissions.
- The stream represents *events* (notifications, navigation commands, broadcast updates).
- There's no canonical "current value" — emissions are discrete events.

**`StateFlow<T>` — hot, conflated, with current value.** A specialization of `SharedFlow` where there's always exactly one current value, and duplicate consecutive values are dropped. Collectors immediately receive the current value, then each subsequent update.

```kotlin
class UserState {
    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()
    fun update(newUser: User?) { _user.value = newUser }
}
```

Use StateFlow when:
- There's a meaningful "current value" consumers care about (UI state, connection state, current user).
- Late subscribers should immediately see the current state without waiting for the next update.
- You'd otherwise build a `BehaviorSubject`-style construct (Rx terminology).

**Quick decision table.**

| Use case | Pick |
| -------- | ---- |
| Database query / pagination / HTTP stream | `Flow` (cold) |
| Notifications / one-shot events / commands | `SharedFlow` |
| UI state / connection status / current user | `StateFlow` |
| Single async value | `suspend fun` / `Deferred` |

## Decision heuristics

- Cold Flow if each collector should get its own independent run.
- Hot Flow if all collectors share a single producing path.
- StateFlow if a current value is part of the contract; SharedFlow if emissions are events with no "current".
- Conflation is the default for StateFlow; configure SharedFlow's `replay` and `extraBufferCapacity` deliberately based on real subscriber needs.

## Anti-patterns

- Exposing a `MutableSharedFlow` / `MutableStateFlow` publicly — defeats encapsulation. Expose the read-only `SharedFlow` / `StateFlow` interface; keep the mutable side private.
- Using `Flow` (cold) for events that all subscribers should see — late subscribers miss earlier emissions silently.
- Using `StateFlow` for events — the conflation drops events that happen to have the same value as the current one.
- Manually buffering events in a `MutableList` and exposing it as a "flow" — reinvents `SharedFlow` badly.

## See also

- `kp-flow-operators` — transforming and combining flows.
- `gof-observer` — Flow / SharedFlow / StateFlow are Kotlin's first-class Observer implementations.
- `gof-kotlin-idioms` — Observer section also touches on these.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 7 (Controlling the Data Flow).
- Kotlin coroutines official guide — Flows.
