---
name: gof-kotlin-idioms
description: Use when implementing a GoF design pattern in Kotlin — phrases like "kotlin strategy", "kotlin singleton with object", "kotlin observer with flow", "by delegation for decorator", "sealed class state machine", "kotlin builder vs named arguments", "data class copy as prototype", "how do I express this pattern in kotlin idiomatically". Maps each of the seventeen GoF patterns (HFDP's thirteen plus Builder, Prototype, Bridge, Visitor) to its idiomatic Kotlin construct AND flags where a Kotlin language feature (object, sealed class, function types, by-delegation, default arguments, named arguments, data class copy, extension functions, scope functions) supersedes the pattern entirely.
---

## One-line summary

Translate each GoF pattern into idiomatic Kotlin — and, for several patterns, explain when a Kotlin language feature replaces the pattern outright.

## When to use this skill

- A GoF pattern has been chosen (via `gof-identify`) and the target language is Kotlin.
- The user wants idiomatic Kotlin code, not Java-flavored Kotlin.
- A code review asks "is this Kotlin pattern usage idiomatic?".

## When NOT to use this skill

- The target language is not Kotlin.
- The user is still picking a pattern → route to `gof-identify`.
- Framework-specific patterns (Spring, Arrow) — out of scope; future adapter plugins.

## Core content

For each pattern: the idiomatic Kotlin construct, and a note when the language supersedes the pattern.

**Strategy.** Use a function type, not an interface.

```kotlin
class Sorter(private val compare: (Item, Item) -> Int) {
    fun sort(items: List<Item>): List<Item> = items.sortedWith(Comparator(compare))
}
// Usage:
Sorter { a, b -> a.price.compareTo(b.price) }
```

The interface-based Strategy is rarely needed in Kotlin. If you have multiple closely-related operations, group them in a `sealed interface` so `when` is exhaustive.

**Observer.** Use `Flow` / `SharedFlow` / `StateFlow`. Rolling your own observer list is almost never the right move.

```kotlin
class WeatherStation {
    private val _readings = MutableSharedFlow<Reading>()
    val readings: SharedFlow<Reading> = _readings.asSharedFlow()
    suspend fun publish(r: Reading) = _readings.emit(r)
}
// Observer:
weatherStation.readings.collect { display.show(it) }
```

Choosing the variant:

- **`StateFlow<T>`** — *always has a current value*, conflates duplicates. Use for *state* a consumer always needs the latest of (UI state, current user, current connection status). Read with `.value`; observe with `.collect`.
- **`SharedFlow<T>`** — *no required current value*, can replay N past emissions, can buffer. Use for *events* — emit-and-listeners-react (notifications, navigation commands, one-shot signals). Configure `replay` and `extraBufferCapacity` deliberately.
- **`Flow<T>`** (cold) — re-runs its emitter for each collector. Use for *pull-driven* streams (a query, a paged fetch). Each `.collect` starts a fresh execution.
- **`Deferred<T>`** (`async { … }.await()`) — one-shot async value. Not really Observer; it's the Future/Promise analogue.

**Decorator.** Use class delegation with `by`.

```kotlin
interface Coffee { fun cost(): BigDecimal; fun description(): String }

class MilkDecorator(coffee: Coffee) : Coffee by coffee {
    override fun cost() = coffee.cost() + 0.5.toBigDecimal()
    override fun description() = coffee.description() + ", milk"
}
```

`by coffee` forwards every method to the wrapped instance; you override only what you change. Without `by`, you'd have to forward every method manually.

**Caveat — `is` checks don't see through `by`.** A decorator implements the *interface*, not the wrapped *concrete class*. So `loggedRepo is DefaultRepository` returns `false` even though `loggedRepo` wraps a `DefaultRepository`. If you find yourself doing `is` checks against concrete wrapped types, the abstraction has leaked; restructure or treat the chain through the interface. (Soshin Ch. 3 covers this caveat explicitly.)

**Factory.** Use a `companion object` factory method on the type, or a top-level function.

```kotlin
class Pizza private constructor(...) {
    companion object {
        fun of(style: Style): Pizza = when (style) {
            Style.NY -> Pizza(...)
            Style.CHICAGO -> Pizza(...)
        }
    }
}
```

For Factory Method / Abstract Factory, the same pattern applies — replace the abstract method with a `sealed interface PizzaFactory` and exhaustive `when` matching at the call site.

**Singleton.** Use `object`. That's it. No double-checked locking, no `getInstance()`, no boilerplate.

```kotlin
object Logger { fun log(msg: String) { ... } }
// Usage:
Logger.log("hello")
```

`object` is thread-safe by language guarantee. For testable code, prefer dependency injection — define an interface and inject a singleton-scoped bean from your DI container. Classical Singleton via `class` + `companion object` + `getInstance()` is almost never warranted.

**Command.** Use a function type (`() -> Unit` or `suspend () -> Result<X>`) or a `sealed interface` of command types when you need pattern-matching on the command.

```kotlin
sealed interface Command {
    data class Send(val to: Recipient, val body: String) : Command
    data class Cancel(val id: SendId) : Command
}

fun execute(cmd: Command) = when (cmd) {
    is Command.Send -> ...
    is Command.Cancel -> ...
}
```

For undo/redo, each command carries its own `undo()` — keep both as part of the sealed interface or as a dedicated `Undoable` interface.

**Adapter.** For a single method, use an extension function — no class needed.

```kotlin
fun OldApi.modernized(): NewApi.Response =
    NewApi.Response(this.legacyResult, mapStatus(this.code))
```

For multiple methods, a wrapper class is fine. For ACL between bounded contexts, follow `ddd-context-mapping`.

**Facade.** Top-level functions or a small class. Kotlin's lack of ceremony makes facades cheap — but the discipline (keep it stateless, keep it narrow) still applies.

**Template Method.** A function that takes the varying steps as lambda parameters often replaces a subclass-based template.

```kotlin
fun brew(
    boil: () -> Water,
    flavor: (Water) -> Beverage,
    addCondiments: (Beverage) -> Beverage = { it }
): Beverage = addCondiments(flavor(boil()))
```

Subclass-based template is fine when the steps share state across calls; otherwise prefer functions.

**Iterator.** Implement `Iterator<T>` and/or `Iterable<T>` directly. Use the `iterator { ... }` builder with `yield` for lazy iteration.

```kotlin
fun rangeOfFibs(n: Int): Sequence<Int> = sequence {
    var a = 0; var b = 1
    repeat(n) { yield(a); val t = a + b; a = b; b = t }
}
```

`Sequence<T>` is Kotlin's lazy stream type. Use it instead of writing your own iterator for any transform / filter pipeline.

**Composite.** Sealed-class hierarchies + exhaustive `when` give compile-time-checked Composites.

```kotlin
sealed interface MenuComponent { fun price(): BigDecimal }
data class MenuItem(val name: String, val price: BigDecimal) : MenuComponent {
    override fun price() = price
}
data class Menu(val items: List<MenuComponent>) : MenuComponent {
    override fun price() = items.sumOf { it.price() }
}
```

Sealed-class Composites are safer than the transparent-vs-safe debate suggests: every operation is declared on the sealed parent; `when` enforces exhaustiveness.

**State.** Same pattern as Composite — a `sealed class` per state, with the context delegating to the current state.

```kotlin
sealed class OrderState {
    object Draft : OrderState()
    data class Placed(val at: Instant) : OrderState()
    object Cancelled : OrderState()
}

class Order(var state: OrderState = OrderState.Draft) {
    fun place() {
        state = when (state) {
            OrderState.Draft -> OrderState.Placed(Instant.now())
            else -> throw IllegalStateException("Cannot place from $state")
        }
    }
}
```

Compile-time exhaustiveness checking from `when` over sealed types eliminates a whole category of "forgot to handle this state" bugs.

**Proxy.** Use `by lazy` for virtual proxies (lazy initialization of expensive fields). Use generated stubs (gRPC, Retrofit, OpenAPI codegen) for remote proxies. Hand-written proxies are rare in Kotlin.

```kotlin
class ImageHolder(private val path: String) {
    val pixels: BufferedImage by lazy { ImageIO.read(File(path)) }
}
```

For protection proxies, prefer authorization at a controller / boundary layer over an in-process proxy that can be bypassed.

**Builder.** Default to *named arguments + default values* on a `data class` or constructor. Only reach for an explicit Builder when construction is genuinely staged (intermediate validation, type-state) or when a DSL builder reads better.

```kotlin
// Named args + defaults beat a classic Builder for most cases:
data class HttpRequest(
    val url: String,
    val method: HttpMethod = HttpMethod.GET,
    val headers: Map<String, String> = emptyMap(),
    val body: ByteArray? = null,
    val timeout: Duration = 30.seconds,
)
val req = HttpRequest(url = "/api", method = HttpMethod.POST, body = bytes)

// DSL builder when assembly reads better as a recipe:
val page = html {
    head { title("Hello") }
    body { p("World") }
}
```

For DSL builders, use a function whose last parameter is a lambda with receiver (`html(block: HtmlBuilder.() -> Unit)`); the receiver makes the builder methods in-scope inside the lambda.

**Prototype.** Use `data class.copy(...)`. That's Prototype as a language feature — no `clone()` interface, no registry boilerplate.

```kotlin
val baseRequest = HttpRequest(url = "/users")
val authedRequest = baseRequest.copy(headers = baseRequest.headers + auth)
```

Caveat: `copy()` is *shallow*. Nested mutable collections (`MutableList`, `MutableMap`) inside a `data class` are shared with the copy. For deep clones, use immutable nested types (`List`, `Map`) or copy explicitly.

**Bridge.** Plain composition via a constructor parameter. No abstract class needed; Kotlin's lack of constructor ceremony makes Bridge a few lines.

```kotlin
interface Renderer { fun render(shape: Shape) }
class Circle(val r: Double, private val renderer: Renderer): Shape {
    override fun draw() = renderer.render(this)
}
class VectorRenderer: Renderer { override fun render(s: Shape) { … } }
class RasterRenderer: Renderer { override fun render(s: Shape) { … } }
```

Inject the `Renderer` via constructor (or DI) so abstraction and implementation evolve independently.

**Visitor.** In Kotlin, almost always prefer `sealed` + exhaustive `when` over the Visitor pattern.

```kotlin
sealed class Shape
data class Circle(val r: Double): Shape()
data class Square(val side: Double): Shape()

fun area(s: Shape): Double = when (s) {
    is Circle -> Math.PI * s.r * s.r
    is Square -> s.side * s.side
}   // compiler enforces that every Shape variant is handled
```

Adding a new operation is a new function — no `accept(visitor)` ceremony. Adding a new element type is "loud" — the compiler flags every `when` that needs updating. That's usually the *better* trade-off than the classical Visitor's silent-default-no-op risk.

Use classical Visitor only when the hierarchy is genuinely open-ended (you really can't make it `sealed`), or when visitors need to carry rich state across visits.

## Scope functions (cross-cutting idiom)

Several patterns above lean on Kotlin's scope functions (`let`, `run`, `apply`, `also`, `with`). Quick reference:

- **`apply { … }`** — configure a receiver, return the receiver. Builder-like: `User().apply { name = "x"; email = "y" }`.
- **`also { … }`** — side-effect on a receiver (logging, debugging), return the receiver. `obj.also { log.debug(it) }`.
- **`let { … }`** — transform the receiver (passed as `it`), return the lambda's result. Common with nullable safe-calls: `nullable?.let { use(it) }`.
- **`run { … }`** — like `let` but receiver is `this`. Use when you want `this`-style access to the receiver and a transformed result.
- **`with(x) { … }`** — `run` as a top-level function; receiver passed in. Use when you don't want method-chain style.

Pick the scope function whose *receiver style* (`this` vs `it`) and *return value* (receiver vs lambda result) match what the code is doing. Misusing them is one of Soshin's listed anti-patterns.

## Decision heuristics

- Default to *language features over patterns* in Kotlin. The pattern is a hint about intent; the language usually provides a cleaner expression.
- Prefer immutability. Most patterns are easier to reason about when the wrapped / composed types are immutable.
- Use `sealed interface` for marker / variant hierarchies (Composite, State, Command). Use `sealed class` only when shared state is needed.
- Use `data class` for value-like wrappers (Command parameters, observer events). Use a regular `class` when identity matters or the type owns mutable state.
- Don't reach for class-based pattern implementations when a top-level function or extension function does the same job.

## Anti-patterns

- Java-flavored Kotlin: writing classical Singleton with private constructors and `getInstance()` when `object` exists; writing Strategy with an interface and concrete classes when a function type would do.
- Sealed-class hierarchies for things that don't have a closed variant set (use an open interface instead).
- `by` delegation that adds *behavior* without overriding any method — pointless wrapper.
- Stateful `object` declarations — global mutable state, even with `object`'s thread-safety, is still global mutable state.
- Using `lateinit var` to fake immutability — `lateinit` is a DI workaround, not a pattern tool.

## See also

- All thirteen `gof-*` pattern skills (the underlying concepts).
- `gof-identify` — picks the pattern; this skill renders it.
- `ddd-kotlin-idioms` — sister adapter for DDD patterns; overlapping idioms (sealed classes, value classes, immutable data).

## References

- Kotlin language docs on `object`, `data class`, `value class` (`@JvmInline`), `sealed class` / `sealed interface`, class delegation (`by`), coroutines / `Flow` / `SharedFlow` / `StateFlow`, and scope functions.
- *Head First Design Patterns* (2nd ed) — the underlying GoF patterns. The Kotlin renderings here often differ substantially from the book's Java examples; that's the point of an idiom adapter.
- *Kotlin Design Patterns and Best Practices* (Alexey Soshin) — primary source for the Kotlin-flavored treatment of every pattern, the `by`-delegation `is`-check caveat, and the scope-function discipline. Highly recommended companion reading.
