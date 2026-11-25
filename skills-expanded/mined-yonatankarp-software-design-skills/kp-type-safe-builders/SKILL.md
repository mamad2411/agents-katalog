---
name: kp-type-safe-builders
description: Use when building a type-safe DSL in Kotlin — phrases like "type-safe builder", "Kotlin DSL", "lambda with receiver", "@DslMarker", "html builder", "HTML DSL", "build a configuration DSL", "Gradle Kotlin DSL style", "Jetpack Compose style". Defines Kotlin's lambda-with-receiver mechanism as the foundation for HTML-style DSLs, and explains the @DslMarker annotation that prevents nested scope confusion.
---

## One-line summary

Build a fluent, type-safe DSL using lambdas with receivers — letting callers write `html { head { title("hi") } }` while the compiler enforces what's valid inside each block.

## When to use this skill

- Configuration that reads better as a recipe than as constructor arguments: Gradle build scripts, Compose UI trees, Ktor routing.
- Domain-specific construction that benefits from a structural shape (HTML, SVG, query builders).
- Test fixtures and seed data where readability matters.

## When NOT to use this skill

- Construction would be just as clear with named arguments + default values — a DSL adds learning cost; reach for it only when the structural shape genuinely helps.
- The "DSL" is one level deep and has no nested scopes — that's just a function with a builder parameter, not really a DSL.
- The grammar you're inventing is complex enough to deserve a real parser — a DSL hides the complexity instead of solving it.

## Core content

**Lambda with receiver.** A function whose last parameter is `T.() -> Unit` makes `T`'s methods and properties available as if you were inside `T`:

```kotlin
fun html(block: HtmlBuilder.() -> Unit): Html {
    val b = HtmlBuilder()
    b.block()    // inside `block`, methods of HtmlBuilder are in scope
    return b.build()
}
```

Inside `html { … }`, `this` *is* an `HtmlBuilder`, so methods like `head`, `body`, `div` are unqualified calls.

**Nesting.** Each builder method takes its own lambda with receiver, creating a typed scope inside it:

```kotlin
fun HtmlBuilder.body(block: BodyBuilder.() -> Unit) {
    val b = BodyBuilder()
    b.block()
    bodies.add(b.build())
}
```

The grammar of the DSL is captured by the type system — `head` is valid inside `html { }` but not inside `body { }`.

**`@DslMarker` — prevent scope leakage.** Without `@DslMarker`, nested DSLs implicitly let you reach outer scopes. This can cause confusing bugs ("why did `title` work inside `body`?"). Annotating the builders with a `@DslMarker` annotation tells the compiler to restrict each scope to its own receiver:

```kotlin
@DslMarker
annotation class HtmlDsl

@HtmlDsl class HtmlBuilder { ... }
@HtmlDsl class HeadBuilder { ... }
@HtmlDsl class BodyBuilder { ... }
```

Now inside `body { … }`, you cannot accidentally call `head`'s methods — the compiler enforces that the implicit receiver of an unqualified call must be the innermost `@HtmlDsl` scope.

**Build → return → use.** The builder typically accumulates state internally and produces an immutable result at the end (`build()` returns the finished tree). The DSL itself is mutable inside the block, immutable outside.

```kotlin
class HtmlBuilder {
    private val children = mutableListOf<Element>()
    fun head(block: HeadBuilder.() -> Unit) { children.add(HeadBuilder().apply(block).build()) }
    fun body(block: BodyBuilder.() -> Unit) { children.add(BodyBuilder().apply(block).build()) }
    fun build(): Html = Html(children.toList())
}
```

## Decision heuristics

- DSL pays off when the grammar has structure (nested scopes, sequences with rules) AND callers will use it often enough to learn its idioms.
- Always use `@DslMarker` to keep scopes from accidentally leaking.
- Make the result of `build()` immutable; DSLs are mutable inside their block and frozen outside.
- A DSL with 30 builder types is over-engineered; start with 2–4 levels.

## Anti-patterns

- DSL without `@DslMarker` — outer scope leaks into inner scopes; you can call `html`'s methods inside `body`, leading to subtle bugs.
- "DSL" that's really a fluent setter chain (`builder.foo().bar().build()`) — no nested scopes, no type-safe grammar. Use named arguments instead.
- DSL whose builder holds the result and is reused across calls — produces stale state and concurrency bugs.
- DSLs with side effects in the build block (logging, IO) — make construction unpredictable.

## See also

- `gof-builder` — classical Builder; DSL builders are the Kotlin-idiomatic specialization.
- `kp-higher-order-functions` — lambda-with-receiver is the foundation.
- `gof-kotlin-idioms` — the Builder section shows a small DSL example.

## References

- *Kotlin Design Patterns and Best Practices* (Alexey Soshin), Ch. 5 (Introducing Functional Programming) and Ch. 9 (Idioms and Anti-Patterns) for `@DslMarker` discussion.
- Kotlin language docs — type-safe builders.
