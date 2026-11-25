---
name: kp-anti-patterns
description: Use when reviewing Kotlin code for language-specific anti-patterns — phrases like "kotlin anti-patterns", "!! abuse", "lateinit overuse", "smart cast bypass", "scope function misuse", "GlobalScope abuse", "runBlocking in production", "java-flavored kotlin", "kotlin code smells". Catalogs the most common Kotlin-specific code smells with symptoms, why each is wrong, and the fix.
---

## One-line summary

A reference catalog of Kotlin-specific anti-patterns — language and Coroutines smells that aren't about design patterns but about misusing Kotlin's features.

## When to use this skill

- Code review on Kotlin code, especially code by developers transitioning from Java.
- Spotting smells during refactoring.
- Onboarding teammates to the team's Kotlin conventions.
- Suspecting a specific pattern of misuse (`!!`, `lateinit`, scope functions, Coroutines).

## When NOT to use this skill

- Domain-modeling smells → `ddd-anti-patterns`.
- Design-pattern misuse → `gof-review` and the per-pattern skills.
- General code quality issues that aren't Kotlin-specific (long methods, poor naming) — handled by general code review, not this catalog.

## Core content

**Null-safety smells.**

- **`!!` operator abuse.** Force-unwrap an `Optional<T>?` because "I know it's not null". Wrong because: silent bugs become NullPointerExceptions in production, defeats Kotlin's null safety. Fix: handle the null case explicitly (`?.`, `?:`, `let`), or fix the type to be non-nullable upstream.
- **`lateinit var` for everything that's declared late.** Wrong when: the field has a sensible default, or when it's not actually populated before use. Fix: use a nullable type with `?.` or `lazy { … }` if it should be initialized on first access. `lateinit` is for DI lifecycle; not for "I haven't decided when to initialize this".
- **Platform types treated as non-null.** Calling a Java API that returns `String` (no annotation), assuming non-null, getting NPE at runtime. Fix: assume nullable unless the Java API has `@NonNull` annotations.

**Smart cast smells.**

- **Explicit `as` cast where smart cast would do.** Wrong because: `as` throws on mismatch; smart casts are guaranteed correct because the compiler tracks the type. Fix: structure code so `is` checks let the compiler smart-cast for you.
- **Smart cast bypass via `var`.** Smart casts don't work across mutating boundaries. `var s: String? = …; if (s != null) { val len = s.length }` fails because `s` could change between check and use. Fix: assign to `val` after the null check.

**Scope-function misuse.**

- **`apply` where the return value is wanted.** `apply` returns the receiver; `let`/`run` return the lambda result. Mixing them up returns the wrong value.
- **`with(x) { … }` where method-chain style would read better.** Style — pick one.
- **Nested scope functions of different kinds.** `obj.let { … }.also { … }.apply { … }` is unreadable. Pick one style, name intermediate variables.

**Coroutines smells.**

- **`GlobalScope.launch { … }`** — coroutine leaks; no lifetime tied to anything. Fix: use an appropriate scope (`viewModelScope`, `lifecycleScope`, a manager-owned scope). See `kp-coroutine-scope`.
- **`runBlocking` in production HTTP handler / server code** — blocks a request worker thread. Fix: use `suspend fun` all the way down; let the framework's coroutine runner orchestrate.
- **Catching `CancellationException` and swallowing it** — breaks cancellation propagation. Fix: if you must catch, rethrow.
- **Blocking I/O on `Dispatchers.Default`** — starves the CPU dispatcher. Fix: `withContext(Dispatchers.IO) { … }` around the blocking call.
- **`async { compute() }.await()` immediately** — no parallelism; just call `compute()`. See `kp-launch-vs-async`.
- **Mutable shared state across coroutines without synchronization** — same race conditions as in any concurrent code. Fix: use confinement (single dispatcher), `Mutex`, or actor-style isolation.

**Java-flavored Kotlin smells.**

- **Singleton with `getInstance()` + private constructor** when `object Foo { }` would do. See `gof-singleton`, `gof-kotlin-idioms`.
- **Strategy as `interface Strategy { fun execute() }` + concrete classes** when `(Input) -> Output` function type would do.
- **`data class` for entities** where identity-only equality is needed. `data class` compares all fields. Use a regular `class` with overridden `equals` for entities.
- **Long telescoping `Builder`** when named arguments + default values would do. See `gof-builder`, `gof-kotlin-idioms`.

**DSL smells.**

- **DSL without `@DslMarker`** — outer scope leaks into inner scopes; subtle bugs from accidentally-resolved unqualified names. See `kp-type-safe-builders`.

## Decision heuristics

- Severity scales with reach: a `!!` in a hot path is worse than the same in a one-off script.
- Pattern-name the smell so the fix is referenceable (e.g., "Coroutines: GlobalScope abuse — see kp-coroutine-scope").
- Don't grep for `!!` literally — it appears in legitimate contexts (test fixtures, where the alternative is clutter). Look at the *kind* of code.
- Some "anti-patterns" are *acceptable* with comments explaining why — flag-only, don't auto-reject.

## Anti-patterns about catching anti-patterns

- Treating every `!!` as a defect — sometimes it's the right answer (compile-time invariant the compiler can't see).
- Renaming a smell rather than fixing it.
- Reviewing only for these smells while missing larger design problems.

## See also

- `kp-coroutine-scope`, `kp-launch-vs-async`, `kp-dispatchers`, `kp-structured-concurrency` — Coroutines smells map to these.
- `kp-type-safe-builders` — DSL smells.
- `gof-singleton`, `gof-kotlin-idioms` — Java-flavored Kotlin smells.
- `ddd-anti-patterns` — domain-modeling smells (orthogonal).

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 9 (Idioms and Anti-Patterns).
- Kotlin language docs — null safety, smart casts, scope functions.
- Kotlin coroutines official guide — common pitfalls.
