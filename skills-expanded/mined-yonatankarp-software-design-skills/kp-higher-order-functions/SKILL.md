---
name: kp-higher-order-functions
description: Use when designing APIs that take or return functions in Kotlin — phrases like "higher-order function", "function type", "function as parameter", "function as return value", "inline function", "reified type parameter", "lambda with receiver", "function composition", "curry". Covers Kotlin's first-class function types, their idiomatic uses, and the inline/crossinline/noinline knobs that affect performance and control flow.
---

## One-line summary

Treat functions as first-class values — pass them as parameters, return them, store them, compose them — and understand Kotlin's `inline` machinery for keeping the cost negligible.

## When to use this skill

- Designing an API that takes a function parameter (the canonical case: `list.map { … }`, `withResource { … }`).
- Returning a function from another function (currying, partial application, function factories).
- Wrapping work with a setup/teardown function that takes the work as a lambda (`use { … }`, `runBlocking { … }`).
- Anywhere a small interface with one method would otherwise be required — a Kotlin function type usually beats it.

## When NOT to use this skill

- The function takes many parameters with names that matter — a regular function or a data class is more readable than a `(A, B, C, D) -> R`.
- The "function" carries state — that's not a function, that's an object; design it as such.
- The function must be exposed across a module boundary in a way that prevents `inline` — `inline` only works for callers in the same compilation, so cross-module APIs may want to be regular functions.

## Core content

**Function types.** `(Int) -> String` is a type. So is `suspend (User) -> Result<Order>`. So is `Item.(Int) -> Item` (a function type with receiver — the basis of type-safe DSL builders).

**Passing a function.**

```kotlin
fun List<Item>.filterPrice(predicate: (BigDecimal) -> Boolean): List<Item> =
    filter { predicate(it.price) }

items.filterPrice { it > 100.toBigDecimal() }
```

**Returning a function.**

```kotlin
fun discountFor(loyalty: LoyaltyLevel): (BigDecimal) -> BigDecimal = when (loyalty) {
    GOLD   -> { price -> price * 0.9.toBigDecimal() }
    SILVER -> { price -> price * 0.95.toBigDecimal() }
    NONE   -> { price -> price }
}
```

**`inline` for performance.** Kotlin compiles lambdas to anonymous-class instances by default — each invocation allocates. Marking a function `inline` substitutes its body (and the lambda's body) at the call site, removing the allocation. Use for *very hot* paths or when the lambda captures variables that would otherwise force boxing.

```kotlin
inline fun <T> measureTimeMillis(block: () -> T): Pair<T, Long> {
    val start = System.currentTimeMillis()
    val result = block()
    return result to (System.currentTimeMillis() - start)
}
```

`inline` allows the lambda to use `return` (non-local return — returns from the enclosing function, not the lambda). `crossinline` forbids non-local returns (when you pass the lambda into another context that can't safely return). `noinline` opts a specific parameter out of inlining.

**Reified type parameters.** `inline` enables `reified` — the type parameter is known at runtime because the call site is inlined.

```kotlin
inline fun <reified T> Any.asOrNull(): T? = this as? T
```

## Decision heuristics

- Prefer function types over single-method interfaces (avoids the boilerplate of declaring an interface that exists only to wrap a function).
- Use `inline` for higher-order functions on hot paths or that take lambdas the caller writes often. Don't inline large functions — it inflates bytecode.
- Function types with receiver are the foundation of DSL builders — see `kp-type-safe-builders`.

## Anti-patterns

- Inlining everything reflexively — `inline` inflates bytecode and only helps when the lambda would have allocated; for cold-path functions it's noise.
- Overusing function composition (`f compose g compose h compose …`) when a named function would read better — composition is great for one or two steps, hard to debug at five.
- Functions returning functions returning functions — at three levels of nesting, the type is unreadable. Use named types or refactor.

## See also

- `gof-strategy` — in Kotlin, Strategy *is* a function-typed parameter most of the time.
- `gof-command` — when the command's `execute` has no state, a function type beats the Command interface.
- `kp-type-safe-builders` — lambdas with receiver are the foundation.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 5 (Introducing Functional Programming).
- Kotlin language docs on function types, `inline`, `crossinline`, `noinline`, and reified type parameters.
