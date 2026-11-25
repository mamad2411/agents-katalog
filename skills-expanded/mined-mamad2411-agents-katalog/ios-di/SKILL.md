---
name: ios-di
description: Project-specific dependency-injection rules — the `CompositionRoot` in the `App` target, constructor injection through protocols, factory methods for view models, the preview/test container, and when a DI library is actually warranted. Load when adding a type that needs dependencies, wiring a repository, setting up previews, or debugging a DI-related crash.
---

# Dependency injection (project delta)

There is no DI framework here to learn — the pattern is plain Swift initializers. This file documents the rules that make that scale, and the places people reach for a shortcut that breaks testability.

## When this applies

**Composition root + constructor injection, no container library.** On an existing app:

- **`swift-dependencies`** (`@Dependency(\.apiClient)`, `DependencyValues`) → keep it. It solves the same problem with per-test overrides; don't unwind it. The "no service locator, no singletons" spirit still applies.
- **Factory / Resolver / Swinject** (`Container.shared.resolve(...)`) → keep it, but the service-locator failure mode is real: flag types that resolve dependencies *inside themselves* rather than receiving them.
- **TCA** → it already uses `swift-dependencies`; skip this skill.
- **Singletons throughout** (`APIClient.shared`, `UserManager.shared`) → say plainly that it blocks testing, but don't refactor the app's wiring as a side effect of an unrelated change.

## The composition root

One type, built once at launch, living in the `App` target — the only place that knows concrete implementations exist:

```swift
struct CompositionRoot {
    let apiClient: APIClient
    let orderRepository: OrderRepository

    static let live: CompositionRoot = {
        let api = URLSessionAPIClient(baseURL: Env.apiBaseURL, keychain: KeychainStoreLive())
        return CompositionRoot(
            apiClient: api,
            orderRepository: LiveOrderRepository(client: api)
        )
    }()
}

extension CompositionRoot {
    func makeOrderDetailViewModel(id: OrderID) -> OrderDetailViewModel {
        OrderDetailViewModel(
            id: id,
            getOrder: GetOrderUseCase(orders: orderRepository),
            submit: SubmitOrderUseCase(orders: orderRepository)
        )
    }
}
```

The scaffolded template is in `.claude/skills/ios-app-skeleton/references/app-target.md`.

## The four rules

1. **`CompositionRoot.live` is the only shared instance in the app.** No other `static let shared`. If you're tempted, you want a factory method on the root instead.
2. **Never pass the root into a view model.** That's a service locator wearing a struct's clothes: the view model's initializer stops declaring what it needs, and tests have to build the whole graph. Give it the specific use cases.
3. **Initializer injection only.** No optional-var-then-assign wiring, no setter injection. If a type can exist in a half-configured state, it will.
4. **Parameters are protocols**, unless the concrete type is already a framework-free `AppCore` value type.

Only a `RootView` constructs a view model, and only from the root:

```swift
struct OrderListRootView: View {
    @State private var model: OrderListViewModel
    init(container: CompositionRoot) {
        _model = State(initialValue: container.makeOrderListViewModel())
    }
}
```

## Previews and tests

A `preview` variant of the root keeps `#Preview` blocks one line long and IO-free:

```swift
extension CompositionRoot {
    static func preview(
        orders: OrderRepository = StubOrderRepository(result: .success(.sample))
    ) -> CompositionRoot {
        CompositionRoot(apiClient: StubAPIClient(), orderRepository: orders)
    }
}

#Preview { OrderListRootView(container: .preview()) }
```

For unit tests, skip the container entirely — construct the view model with stubs directly. If a test needs the whole graph, the type under test has too many dependencies.

## When a DI library is warranted

Consider `swift-dependencies` or `Factory` when the container has grown past ~30 distinct dependencies and is genuinely hard to read, when you want per-test overrides without threading a container through every initializer, or when you're adopting TCA anyway. **Not** merely because the app is growing — the plain pattern scales considerably further than people expect, and it costs nothing at build time.

## Common pitfalls

- **Constructing a view model in a stateless view** — it should receive state and closures. See `swiftui-views`.
- **Stashing services in `EnvironmentValues`** — Environment is for UI concerns (theme, locale, size class). Business services there are hidden global state with extra steps.
- **Forgetting `@MainActor` on a view model** — under Swift 6 strict concurrency this surfaces as a data race, usually far from the cause.
- **A `static let shared` added "just for this one thing"** — it is never just one thing.
