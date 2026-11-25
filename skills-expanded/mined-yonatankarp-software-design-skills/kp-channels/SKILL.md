---
name: kp-channels
description: Use when coordinating coroutines through message-passing — phrases like "Channel", "Kotlin Channel", "send/receive", "produce", "consumeEach", "fan-out fan-in", "pipeline of coroutines", "rendezvous channel", "buffered channel", "conflate channel". Defines `Channel<T>` as a coroutine-safe queue for cross-coroutine communication, the four capacity modes, and the common pipeline shapes (fan-out, fan-in, broadcast).
---

## One-line summary

A `Channel<T>` is a coroutine-safe queue used for message-passing between coroutines — the building block for pipelines, fan-out / fan-in, and any coordination that can't be expressed with `Flow` or shared state alone.

## When to use this skill

- Multiple producer coroutines or multiple consumer coroutines that need to coordinate on a stream of values.
- Building a pipeline: stage A produces; stage B transforms; stage C writes. Each stage is its own coroutine connected by channels.
- Fan-out: one producer, many workers (load distribution).
- Fan-in: many producers, one consumer (collecting results).
- When `Flow` is too constrained — `Flow` is single-collector-cold; `Channel` lets multiple coroutines compete for elements.

## When NOT to use this skill

- A single producer and a single consumer with no buffering needs → just use a `Flow` (cold) or `suspend fun`.
- Sharing observable state with multiple subscribers → `StateFlow` / `SharedFlow` (see `kp-flow-cold-vs-hot`).
- Pure transformations on a stream → `Flow` operators (see `kp-flow-operators`).
- Coordination between threads in non-coroutine code → use a `java.util.concurrent` queue.

## Core content

**Send and receive.** `channel.send(x)` suspends until a receiver is ready (rendezvous) or until buffer capacity allows. `channel.receive()` suspends until a value is available. Both are cancellable.

```kotlin
val ch = Channel<Int>()
launch { for (n in 1..5) ch.send(n); ch.close() }
launch { for (n in ch) println(n) }   // for-loop iterates until close
```

**Four capacity modes** (the most consequential design decision):

- **`Channel.RENDEZVOUS` (default, capacity 0)** — every `send` waits for a matching `receive`. Tightest coupling between producer and consumer rates. Use for back-pressure-by-design.
- **`Channel.BUFFERED`** — a fixed-size buffer (default 64). `send` only suspends when the buffer is full. Use when producer should not block on consumer for short bursts.
- **`Channel.CONFLATED`** — buffer of 1; new send replaces pending value. Use when only the latest value matters (UI updates, sensor readings).
- **`Channel.UNLIMITED`** — unbounded buffer. Use *very* sparingly — under sustained mismatch the heap grows without bound. Almost always the wrong default.

**`produce { … }` — single-producer convenience.** Builds a `ReceiveChannel<T>` from a coroutine that emits via `send`:

```kotlin
fun CoroutineScope.numbers(): ReceiveChannel<Int> = produce {
    for (n in 1..10) send(n)
}
```

The channel closes automatically when the produce coroutine completes.

**Fan-out (one producer, many workers).** Many consumers compete for elements from a single channel; each value goes to exactly one consumer.

```kotlin
val tasks = produce { ... }
repeat(4) { workerId -> launch { for (task in tasks) process(workerId, task) } }
```

**Fan-in (many producers, one consumer).** Many producers `send` into a shared channel; one consumer reads.

```kotlin
val results = Channel<Result>()
sources.forEach { src -> launch { results.send(src.compute()) } }
launch { for (r in results) collect(r) }
```

**Closing.** `channel.close()` signals "no more values." Receivers see the channel as closed after draining buffered values. `for (x in channel)` exits cleanly on close. Senders to a closed channel throw `ClosedSendChannelException`.

## Decision heuristics

- Default to `Flow` first. Reach for `Channel` only when you genuinely have *multiple* coroutines as senders or receivers.
- `RENDEZVOUS` is the right default for capacity. Tighter coupling catches mismatched producer/consumer rates early.
- Never use `UNLIMITED` capacity without a hard reason — back-pressure is a feature.
- Always close the channel when production is done; long-lived producers without closers leak coroutines.

## Anti-patterns

- `Channel.UNLIMITED` as a default — heap grows without bound under load.
- Holding a channel reference but never closing it — receivers block forever; the parent coroutine never completes.
- Using channels for single-producer / single-consumer streams when a `Flow` would do — extra ceremony without benefit.
- Sharing a channel with no clear ownership — race conditions on `close()` (closing twice throws).
- Mixing channels with shared mutable state — defeats the message-passing benefit.

## See also

- `kp-select` — multiplexing across multiple channels (or channels + deferreds).
- `kp-actor-pattern` — confining mutable state behind a coroutine via a channel.
- `kp-flow-cold-vs-hot` — when to use `Flow` / `SharedFlow` / `StateFlow` instead of a `Channel`.
- `kp-structured-concurrency` — channels and the scopes that own them.

## References

- *Kotlin Coroutines* (Marcin Moskała) — dedicated chapters on Channels, produce, fan-out/fan-in.
- Kotlin coroutines official guide — channels and asynchronous flow.
