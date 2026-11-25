---
name: lang-kotlin
description: Kotlin engineering, structured concurrency, coroutine cancellation, sound null-safety without !!, and immutable data collections.
---

# Kotlin Coroutines & Sound Null-Safety Contract

## 1. Null-Safety Discipline
- The not-null assertion operator (`!!`) is strictly prohibited in production code. Use `?:`, `let`, or explicit exception throwing.
- Leverage smart casts and exhaustive `when` expressions over `sealed class`/`sealed interface`.

## 2. Coroutines & Structured Concurrency
- Never launch unmanaged coroutines in `GlobalScope`.
- Ensure cancellation cooperativeness by calling `yield()` or checking `ensureActive()` in compute loops.
