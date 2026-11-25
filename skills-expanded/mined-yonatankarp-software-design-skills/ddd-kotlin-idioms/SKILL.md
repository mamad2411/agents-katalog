---
name: ddd-kotlin-idioms
description: Use when implementing a DDD pattern in Kotlin — phrases like "kotlin entity", "kotlin value class for ID", "kotlin data class for value object", "sealed class for domain status", "how do I express this aggregate in kotlin", "idiomatic kotlin DDD". Maps each pattern decision from ddd-core to the right Kotlin construct (data class / value class / sealed class / object / Result / require). Framework-agnostic — no Spring or Arrow opinions here.
---

## One-line summary

Translate DDD pattern decisions into idiomatic Kotlin using stdlib only — no framework opinions.

## When to use this skill

- A DDD pattern has been chosen (typically via `ddd-implement`) and the target language is Kotlin.
- The user wants idiomatic code, not pseudocode.
- A code review on Kotlin DDD code asks "what is the right Kotlin construct for this pattern?".

## When NOT to use this skill

- The target language is not Kotlin.
- The user is still deciding the pattern — route to a `ddd-core` pattern skill first.
- The user wants framework-specific scaffolding (Spring annotations, Arrow `Either`) — those are out of scope here and will live in future adapter plugins (`ddd-kotlin-spring`, `ddd-kotlin-arrow`).

## Core content

The mapping. For each DDD pattern, the idiomatic Kotlin construct and the trade-off that motivates the choice.

**Value object — wrap of a single primitive.**

```kotlin
@JvmInline
value class CustomerId(val raw: UUID)
```

Use Kotlin's `@JvmInline value class` for zero-allocation typed IDs and other single-field wraps. Caveat: prior to Kotlin 1.9, value classes could not have an `init {}` block; for *validated* single-field wraps, use a `data class` or a private constructor with a validating companion factory.

**Value object — composite, multi-field.**

```kotlin
data class Money(val amount: BigDecimal, val currency: Currency) {
    init {
        require(amount.scale() <= currency.defaultFractionDigits) {
            "amount scale exceeds ${currency.defaultFractionDigits} for ${currency.currencyCode}"
        }
    }
    fun add(other: Money): Money {
        require(currency == other.currency) { "cannot add $currency and ${other.currency}" }
        return Money(amount + other.amount, currency)
    }
}
```

`data class` is the right choice — equal-by-attribute, immutable by default (use `val`), copy-on-modify via `copy()`. Put invariants in the `init` block.

**Entity.**

```kotlin
class Customer(val id: CustomerId, name: String) {
    var name: String = name
        private set

    fun rename(to: String) {
        require(to.isNotBlank())
        this.name = to
    }

    override fun equals(other: Any?) = other is Customer && other.id == id
    override fun hashCode() = id.hashCode()
}
```

A *regular* `class`, not `data class`. Override `equals`/`hashCode` to compare by identity (the `id`) only. `data class` would compare all fields, which makes two `Customer` instances with the same name (but different IDs) equal — wrong.

**Aggregate root.** An entity that exposes only commands. Internals stay `private`; queries return immutable views.

```kotlin
class Order(val id: OrderId, val customerId: CustomerId) {
    private val _items = mutableListOf<LineItem>()
    val items: List<LineItem> get() = _items.toList()

    fun addItem(productId: ProductId, quantity: Int) {
        check(items.none { it.productId == productId }) { "product already in order" }
        _items.add(LineItem(productId, quantity))
    }
}
```

Note `customerId: CustomerId` — a *reference by ID* to the `Customer` aggregate, not a `Customer` object reference.

**Domain event.**

```kotlin
sealed interface OrderEvent {
    data class Placed(val orderId: OrderId, val at: Instant) : OrderEvent
    data class Cancelled(val orderId: OrderId, val reason: String, val at: Instant) : OrderEvent
}
```

Past-tense names. `sealed interface` is preferred over `sealed class` for marker hierarchies; the variants are `data class`es because they are value objects.

**Status / state machine.**

```kotlin
sealed class OrderStatus {
    data object Draft : OrderStatus()
    data class Placed(val at: Instant) : OrderStatus()
    data object Cancelled : OrderStatus()
}
```

`sealed` enables exhaustive `when`. Use `data object` (Kotlin 1.9+) for stateless variants so `toString` and `equals` are sensible.

**Result / fallible operation.**

```kotlin
fun place(order: Order): Result<Order> = runCatching { /* domain logic */ }
```

Use `kotlin.Result` for now. (A future `ddd-kotlin-arrow` plugin would substitute Arrow's `Either<DomainError, Order>` with named error types.)

**Invariants.**

- `require(...)` for constructor preconditions — throws `IllegalArgumentException`.
- `check(...)` for state-invariant checks during operations — throws `IllegalStateException`.

For domain-specific exceptions, define your own: `class OrderAlreadyPlacedException(...) : IllegalStateException(...)`.

**Repository interface.**

```kotlin
interface OrderRepository {
    fun save(order: Order)
    fun findById(id: OrderId): Order?
}
```

The interface lives in the domain module. Implementations live in an infrastructure module and are wired by the application bootstrap.

**Factory — preferred form.**

```kotlin
class Order private constructor(/* ... */) {
    companion object {
        fun place(customerId: CustomerId, items: List<LineItem>): Order { /* invariant checks, then return Order */ }
    }
}
```

Private constructor + a named companion factory expresses the domain verb (`place`) and prevents arbitrary callers from constructing invalid `Order` instances.

## Decision heuristics

- Use `data class` only when *all* properties participate in identity (value objects). Use a regular `class` with an overridden `equals` for entities so identity is by ID alone.
- Prefer `sealed interface` over `sealed class` unless the hierarchy needs to share state.
- For typed IDs and single-primitive wraps with no validation, prefer `@JvmInline value class`. Otherwise prefer `data class`.
- Prefer immutability everywhere except inside an entity that owns mutable state — and even then, only mutate via methods that maintain invariants.

## Anti-patterns

- Using `data class` for entities — equality includes mutable fields, breaks identity semantics.
- Putting JPA annotations (`@Entity`, `@Column`) on a domain entity that lives in a pure-domain module — couples the domain to the persistence framework.
- Throwing bare `IllegalArgumentException` everywhere instead of defining domain-meaningful exceptions.
- Abusing `lateinit var` to fake immutability — `lateinit` is a workaround for DI lifecycle, not a domain modeling tool.
- Using `JpaRepository<Order, UUID>` *as* the domain repository — exposes every CRUD method and ties the domain to JPA.

## See also

- `ddd-entity`, `ddd-value-object`, `ddd-aggregate`, `ddd-domain-event`, `ddd-repository`, `ddd-factory` — the patterns this skill realizes.
- `ddd-implement` — the entry-point that routes here for Kotlin code generation.

## References

- Kotlin language docs on `data class`, `value class` (`@JvmInline`), `sealed class` / `sealed interface`, and `Result`.
- Evans, *Domain-Driven Design* (2003), Chs 5–6, for the underlying patterns.
