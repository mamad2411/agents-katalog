---
name: kp-sealed-when
description: Use when modeling a closed set of related types in Kotlin — phrases like "sealed class", "sealed interface", "ADT", "algebraic data type", "exhaustive when", "compile-time pattern matching", "Result type", "I have N variants and want the compiler to make me handle every one". Defines Kotlin's sealed hierarchies + exhaustive `when` as the language's pattern-matching primitive — the foundation for state machines, result types, command types, AST nodes, and many GoF substitutes.
---

## One-line summary

Combine a `sealed class` or `sealed interface` (closed variant set) with an exhaustive `when` expression — getting compile-time-checked pattern matching that the compiler refuses to compile when a variant is unhandled.

## When to use this skill

- Modeling a closed, finite set of variants: order status, parser results, command types, AST/expression nodes, network response shapes.
- Replacing `enum` when variants need to carry different data (an enum is a set of singletons; a sealed hierarchy is variants-with-payload).
- Implementing GoF State, Visitor, or Command patterns in idiomatic Kotlin.
- Wherever you have a "type code + switch" pattern in older code — sealed + when is the structural fix.

## When NOT to use this skill

- The set is genuinely open-ended (third parties or downstream modules can add new variants) — use an open interface instead.
- The variants share no behavior or data — they might not belong as a hierarchy at all. Consider whether the discriminator is the wrong abstraction.
- A simple `enum` suffices because the variants are pure tags with no payload.

## Core content

Two key Kotlin language features cooperating:

**Sealed types.** A `sealed class` or `sealed interface` declares a closed set of direct subtypes — declared in the same package and the same module as the parent (with source-set constraints in multiplatform projects). Subtypes can be top-level or nested inside other named classes, interfaces, or objects within that package. The compiler knows the full set.

```kotlin
sealed interface Result<out T> {
    data class Success<T>(val value: T) : Result<T>
    data class Failure(val error: DomainError) : Result<Nothing>
    object Pending : Result<Nothing>
}
```

**Exhaustive `when`.** When `when` is used as an *expression* (its value is assigned or returned), the compiler requires every variant to be handled. Forgetting one is a compile error.

```kotlin
fun render(r: Result<User>): String = when (r) {
    is Result.Success -> "Welcome, ${r.value.name}"
    is Result.Failure -> "Error: ${r.error.message}"
    Result.Pending    -> "Loading…"
}
// Add a new variant and this when stops compiling until you handle it.
```

The compiler's exhaustiveness check is the pattern's main value. It eliminates a whole category of "forgot to handle this case" bugs that hide in `if`/`else if`/`else` chains and `switch` statements.

**`sealed class` vs `sealed interface`.** Prefer `sealed interface` unless you need shared state or a common constructor in the parent. Sealed interfaces allow a variant to implement multiple sealed hierarchies, which can be useful for cross-cutting state.

**`data object` (Kotlin 1.9+)** is the right choice for stateless variants — gives sensible `toString`/`equals` and signals intent. Older code uses plain `object`.

## Decision heuristics

- Closed variant set + variants carry different data → sealed hierarchy.
- Closed set of pure tags, no payload → `enum class`.
- Open set (extensible by consumers) → open interface.
- Want compile-time exhaustiveness — both expression *and* statement forms over sealed types, enums, and `Boolean` are checked exhaustively since Kotlin 1.7. Older codebases (pre-1.7) only enforced it for expression form, so you may still see "make the when an expression" advice in legacy guidance.

## Anti-patterns

- `else` branches in `when` over sealed types — silently swallows new variants the compiler would have flagged.
- Sealed hierarchy with one subtype — single variant means no exhaustiveness benefit; reconsider whether you need the hierarchy at all.
- Sealed hierarchy where downstream modules need to add variants — defeats "closed". Open it up.
- Relying on non-exhaustive `when` over a sealed type. Since Kotlin 1.7 the compiler enforces exhaustiveness in both expression and statement form for sealed types, enums, and `Boolean`. Avoid `else` branches when you want the compiler to flag newly added variants.

## See also

- `gof-state` — sealed + when is the idiomatic Kotlin implementation of State.
- `gof-visitor` — sealed + when usually replaces Visitor in Kotlin.
- `gof-command` — sealed-interface Commands with exhaustive `when` for dispatch.
- `gof-kotlin-idioms` — pattern-by-pattern guidance that often reaches for sealed + when.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 5 (Pattern matching).
- Kotlin language docs on `sealed class` / `sealed interface` and `when` expressions.
