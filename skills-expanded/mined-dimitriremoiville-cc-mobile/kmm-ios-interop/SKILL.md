---
name: kmm-ios-interop
description: How the shared Kotlin module is consumed from Swift in the iOS app — what API shapes translate well, what to avoid, how to wrap `StateFlow` and `Flow` for SwiftUI, how to bridge suspend functions and sealed hierarchies, and how to make the framework pleasant to use. Load whenever writing or reviewing a public API that iOS will call.
---

# iOS interop

The shared module becomes a Swift framework (XCFramework, CocoaPods, or SPM artifact). Kotlin-to-ObjC/Swift translation is mostly predictable but has sharp edges. Design public APIs with Swift in mind.

## What translates well

- `data class` → Swift `class` with an initializer and `component1()`/`component2()`-style synthetic Swift APIs you usually ignore. `copy(...)` becomes `doCopy(...)`.
- `sealed class` / `sealed interface` → a Kotlin base class with nested classes; checked in Swift with `if let x = value as? Base.Success`.
- `enum class` → Swift enum-like, but you still access cases as `Base.Something`.
- `suspend fun` → Swift `async` function. Exception types appear as `throws`.
- `interface` → Swift `protocol`-ish. Callers implement it; single-abstract-method interfaces become closures in some Kotlin→Swift bridging plugins.
- `Flow<T>` (cold) and `StateFlow<T>` → exposed as Kotlin types. Consume via a helper that bridges to `AsyncSequence`.

## What's rough

- **`inline` functions** — they don't translate at all. Don't put `inline` on anything `public` if iOS needs to call it.
- **Default arguments** — Kotlin's defaults don't translate. Every iOS call site must supply every parameter. Keep defaults private-only, or provide overloads.
- **Sealed hierarchies with generics** — anything deeper than `Result<T>` gets unreadable quickly in Swift.
- **`@JvmStatic` / `@JvmOverloads`** — irrelevant on iOS; don't rely on them for API shape.
- **`Nothing`-typed returns or `Unit` parameters** — show up awkwardly in Swift. Prefer `Void`-returning functions or explicit types.
- **Generics on companion objects** — often fail to be exposed.
- **`typealias`** — translates but loses the alias name; callers see the underlying type.

## Making APIs Swift-friendly

### Use value classes with care

`@JvmInline value class OrderId(val raw: String)` translates to Swift as a class wrapper, not a value type. It's fine — just document the pattern so iOS folks know what `OrderId(raw: "42")` means.

### Don't rely on Kotlin default arguments

```kotlin
// bad — iOS must supply every arg
suspend fun listOrders(cursor: String? = null, limit: Int = 20): PagedResult<Order>

// better — provide overloads that iOS sees
suspend fun listOrders(): PagedResult<Order> = listOrders(null, 20)
suspend fun listOrders(cursor: String?): PagedResult<Order> = listOrders(cursor, 20)
suspend fun listOrders(cursor: String?, limit: Int): PagedResult<Order>
```

### Keep sealed hierarchies flat

```kotlin
// friendly in Swift
sealed interface OrderUiState {
    data object Loading : OrderUiState
    data class Success(val order: Order) : OrderUiState
    data class Error(val message: String) : OrderUiState
}

// confusing in Swift — generics on sealed
sealed interface Outcome<out T> {
    data class Success<T>(val value: T) : Outcome<T>
    data class Failure<T>(val error: DomainError) : Outcome<T>
}
// Prefer Result<T> with kotlin.Result semantics or a concrete per-type sealed result.
```

### Make exception expectations explicit

Kotlin's `throws` is inferred. For Swift, annotate:

```kotlin
@Throws(DomainError::class, CancellationException::class)
suspend fun submit(draft: OrderDraft): Order
```

Swift sees `func submit(draft:) async throws -> Order` with the right throwing behaviour.

## Consuming Flow / StateFlow from Swift

Kotlin `Flow` shows up in Swift as a type the caller has to `collect` manually. Bridge it to `AsyncSequence`:

```swift
// Swift helper (in iosApp/)
extension Kotlinx_coroutines_coreFlow {
    func asAsyncThrowingStream<T>(_ type: T.Type) -> AsyncThrowingStream<T, Error> {
        AsyncThrowingStream { continuation in
            let job = SwiftFlowCollector(flow: self) { value in
                guard let typed = value as? T else { return }
                continuation.yield(typed)
            }
            continuation.onTermination = { _ in job.cancel() }
        }
    }
}
```

Consume from a `@Observable` Swift wrapper:

```swift
@Observable @MainActor
final class OrderViewModelObservable {
    private(set) var state: OrderUiState = OrderUiState.Loading()
    private let shared: OrderViewModel
    private var stateTask: Task<Void, Never>?

    init(shared: OrderViewModel) {
        self.shared = shared
        self.stateTask = Task { [weak self] in
            for await value in shared.state.asAsyncThrowingStream(OrderUiState.self) {
                self?.state = value
            }
        }
    }

    deinit { stateTask?.cancel() }

    func onAction(_ action: OrderAction) { shared.onAction(action: action) }
}
```

## Bridging helpers to expose from `commonMain`

Expose factory functions from `commonMain` so Swift doesn't have to touch Koin directly:

```kotlin
// commonMain
fun makeOrderViewModel(orderId: String): OrderViewModel =
    get<OrderViewModel> { parametersOf(OrderId(orderId)) }
```

Swift calls `AppKoinKt.makeOrderViewModel(orderId: "42")`.

## SwiftUI view consuming the shared VM

```swift
struct OrderRootView: View {
    @State private var model: OrderViewModelObservable

    init(id: String) {
        let shared = AppKoinKt.makeOrderViewModel(orderId: id)
        _model = State(initialValue: OrderViewModelObservable(shared: shared))
    }

    var body: some View {
        OrderView(
            state: model.state,
            onAction: model.onAction
        )
    }
}
```

The SwiftUI side stays idiomatic — `@Observable` + a plain stateless view. The KMM ViewModel is an implementation detail behind the Swift wrapper.

## Reviewer checklist for public Kotlin API

Before exposing a new type or function from `commonMain`, confirm:
- [ ] No `inline` modifier.
- [ ] No default arguments (or provide overloads).
- [ ] Sealed hierarchies are shallow and non-generic.
- [ ] `@Throws` annotation on `suspend` functions that throw.
- [ ] `value class` usage is documented.
- [ ] No `internal` types leaking through public signatures.
- [ ] Swift folks have a bridging helper for any `Flow`/`StateFlow` surface.

## Common pitfalls

- **Kotlin exception mid-`suspend`** that isn't a `DomainError` — Swift sees `KotlinException`. Map platform exceptions in the repository so the public suspend surface throws domain types only.
- **Cancellation** — Swift `Task` cancellation propagates via `CancellationException` in Kotlin. Never swallow it in `runCatching`.
- **Collection types** — `List<T>` comes through as `NSArray<T>`. Prefer concrete element types; avoid `List<Any>`.
- **`Unit` return types** — fine, but calling `.get()` on a `Deferred<Unit>` returns `()` in Swift. Don't design public APIs around `Deferred`; use `suspend fun` directly.
