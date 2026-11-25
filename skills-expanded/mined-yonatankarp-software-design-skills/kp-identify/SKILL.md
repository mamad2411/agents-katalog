---
name: kp-identify
description: Use when the user has a Kotlin-specific design problem and is asking which Kotlin pattern (Coroutines / Flow / sealed-when / DSL / etc.) fits — phrases like "what's the right kotlin pattern for this", "should I use launch or async", "Flow or SharedFlow", "is this a sealed class job or an interface", "DSL or just a function". Diagnostic mode that routes to the relevant Kotlin-pattern skill or rules patterns out.
---

## One-line summary

Diagnose which Kotlin-specific pattern fits a stated problem — or route to a GoF pattern, a language feature, or a simpler alternative when no Kotlin-specific pattern applies.

## When to use this skill

- The user has a design problem and isn't sure which Kotlin idiom or pattern to reach for.
- Confusion between similar Kotlin primitives (`launch` vs `async`, `Flow` vs `SharedFlow`, `sealed class` vs `enum`).
- Code review wants to know "is there a Kotlin-idiomatic pattern for this?".

## When NOT to use this skill

- The user already knows the pattern → go directly to it (e.g., `kp-coroutine-scope`).
- The problem is a classical GoF design problem → route to `gof-identify`.
- The problem is domain modeling → route to `ddd-design`.

## Core content

Walk the problem through these diagnostic questions, in this order:

**1. Is it a closed set of variants where the compiler should enforce exhaustiveness?**
- Yes → `kp-sealed-when`. Examples: status types, result types, command types, expression trees, AST nodes.

**2. Is it about concurrency?**
- *I want to do work concurrently / off the main thread* → start with `kp-coroutine-scope` (lifecycle ownership), then `kp-launch-vs-async` (which primitive), then `kp-dispatchers` (which thread pool).
- *I have multiple concurrent operations and need to handle their cancellation / failure* → `kp-structured-concurrency`.
- *I need coroutines to coordinate by passing messages (pipeline, fan-out, fan-in)* → `kp-channels`.
- *I need to wait on whichever of several suspending sources is ready first (channels, deferreds, timeouts)* → `kp-select`.
- *I want to confine mutable state behind a single coroutine, mutated via messages* → `kp-actor-pattern`.
- *I'm wrapping a callback-based API as a `suspend fun` (one-shot)* → `kp-callback-bridging`.
- *I'm writing tests for coroutine code (need virtual time, deterministic dispatch)* → `kp-testing-coroutines`.

**3. Is it about a stream of values over time?**
- *Latest value matters, observable state* → `StateFlow` (see `kp-flow-cold-vs-hot`).
- *Events, no required current value, possibly buffered* → `SharedFlow` (see `kp-flow-cold-vs-hot`).
- *Cold pull-style stream, re-runs per collector* → `Flow` (see `kp-flow-cold-vs-hot`).
- *Transforming / combining / debouncing streams* → `kp-flow-operators`.
- *Many-shot callback emitting events* → `kp-callback-bridging` (`callbackFlow`).

**4. Is it a configuration / construction problem that reads better as a recipe?**
- *Type-safe DSL (HTML, Gradle config, builder API)* → `kp-type-safe-builders`.
- *Just an object with many parameters* → use named arguments + default values; not a DSL.
- *Classical Builder needed (staged construction, type-state)* → `gof-builder`.

**5. Is it about behavior that varies?**
- *Algorithm varies at runtime* → `gof-strategy` (function type in Kotlin).
- *Behavior varies with object state* → `gof-state` (sealed class in Kotlin — see `kp-sealed-when`).
- *Adding operations over a hierarchy without modifying it* → `gof-visitor` (sealed + when in Kotlin).

**6. Is the code smelly in a Kotlin-specific way?**
- Excessive `!!`, abuse of `lateinit`, scope functions used incorrectly, `runBlocking` in production, `GlobalScope` everywhere → audit via `kp-anti-patterns`.

**7. Higher-order functions / functions as first-class values?**
- *Passing functions as parameters or returning them* → `kp-higher-order-functions`.

**8. None of the above?**
- The problem may not need a Kotlin-specific pattern. Most often: a plain function, a `data class`, a top-level constant, or a GoF pattern (route to `gof-identify`).

## Decision heuristics

- Always prefer the *simplest construct that solves the problem*. Coroutines and Flow are powerful but have learning-curve costs — use them when concurrency or streams are genuinely the problem.
- A sealed class is often the cleanest answer when "the variants are known and finite".
- For event-style coupling between two parts of the same process, `SharedFlow` is the right reach 9/10 times in 2026 Kotlin.

## Anti-patterns

- Reaching for Coroutines when a single suspending function would do.
- Reaching for `Flow` when a `List` or `Sequence` would do.
- Building a DSL when named arguments + default values would suffice.
- Sealed classes used for things that aren't actually a closed variant set.

## See also

- All ten `kp-*` pattern skills in this plugin.
- `gof-identify` — for classical GoF problems.
- `ddd-design` — for domain modeling problems.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin) — primary source for the Kotlin-specific patterns this skill routes to.
- Kotlin official docs on coroutines, Flow, sealed classes, type-safe builders.
