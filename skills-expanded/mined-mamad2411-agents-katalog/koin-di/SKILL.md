---
name: koin-di
description: How Koin is wired up and used in this KMM project — common modules, platform-specific modules, ViewModel binding for both Android and iOS, and testing. Load when adding a new injectable, creating a Koin module, wiring a repository, writing DI-aware tests, or debugging a Koin error.
---

# Koin (KMP-friendly DI)

Koin is the DI framework here because Hilt is Android-only. Koin runs on every Kotlin Multiplatform target and has a clean DSL.

## Where modules live

Colocate modules with the code they bind.

```
shared/src/commonMain/kotlin/com/example/app/
├── di/
│   └── AppKoin.kt              # initKoin(...) root entry point
├── feature/orders/data/di/orderDataModule.kt
├── feature/orders/presentation/di/orderPresentationModule.kt
└── core/network/networkModule.kt
```

Platform-specific modules:
```
shared/src/androidMain/kotlin/com/example/app/di/AndroidModule.kt
shared/src/iosMain/kotlin/com/example/app/di/IosModule.kt
```

## Root initialization

Platform-specific bindings are carried by an `expect val platformModule` whose `actual` definitions live under `androidMain/` and `iosMain/`. `initKoin` always loads both the shared modules **and** the platform module — no caller-of-`initKoin` has to remember to pass it.

```kotlin
// commonMain/di/AppKoin.kt
fun initKoin(extra: KoinAppDeclaration = {}): KoinApplication =
    startKoin {
        extra()
        modules(
            coreModule,
            networkModule,
            orderDataModule,
            orderPresentationModule,
            platformModule,
        )
    }

expect val platformModule: Module
```

Each platform's entry point calls `initKoin`:

- **Android**: in `Application.onCreate()`:
  ```kotlin
  class App : Application() {
      override fun onCreate() {
          super.onCreate()
          initKoin {
              androidContext(this@App)
          }
      }
  }
  ```

- **iOS**: exposed as a helper function called from Swift:
  ```kotlin
  // commonMain
  fun initKoinForIos() = initKoin()
  ```
  Swift calls `AppKoinKt.initKoinForIos()` at app launch.

The `KoinAppDeclaration` block (`extra { … }`) is the seam for per-platform extras that can't go in `platformModule` — the most common one is `androidContext(this@App)` on Android.

## Defining bindings

```kotlin
val orderDataModule = module {
    // Retrofit-like: single API client
    single { OrderApi(get()) }

    // Repository — single interface → single impl
    single<OrderRepository> { OrderRepositoryImpl(get(), get(named("io"))) }

    // Use cases — factory (a new instance per injection is fine)
    factory { GetOrderUseCase(get()) }
    factory { SubmitOrderUseCase(get(), get()) }
}

val orderPresentationModule = module {
    // ViewModel — one per consumer
    factory { (orderId: OrderId) -> OrderViewModel(get(), get()) }
}
```

`factory { (orderId: OrderId) -> ... }` enables `koinViewModel { parametersOf(orderId) }` on Android.

## Qualifiers (named instances)

When you need more than one instance of the same type:

```kotlin
val coreModule = module {
    single<CoroutineDispatcher>(named("io")) { Dispatchers.IO }
    single<CoroutineDispatcher>(named("default")) { Dispatchers.Default }
}

class Repo(private val io: CoroutineDispatcher) { ... }

val module = module {
    single { Repo(get(named("io"))) }
}
```

## ViewModels

**Android** uses the `koinViewModel()` composable (from `koin-androidx-compose`):

```kotlin
@Composable
fun OrderRoute(id: OrderId) {
    val viewModel: OrderViewModel = koinViewModel { parametersOf(id) }
    // ...
}
```

**iOS** calls a `commonMain` factory function, or injects directly from the Koin graph via a helper:

```kotlin
// commonMain
fun makeOrderViewModel(id: OrderId): OrderViewModel = get<OrderViewModel> { parametersOf(id) }
```

…exposed to Swift as `AppKoinKt.makeOrderViewModel(id: ...)`. From Swift, wrap in an `@Observable` adapter (see `kmm-ios-interop` skill).

## Platform modules

`platformModule` is `expect`/`actual`: one declaration in `commonMain`, one implementation per target. `commonMain` code depends on the shared interfaces, never the per-platform types.

```kotlin
// commonMain
expect val platformModule: Module

// androidMain
actual val platformModule: Module = module {
    single<HttpClientEngine> { OkHttp.create() }
    single<KeyValueStore> { DataStoreKeyValueStore(androidContext().preferencesDataStore) }
}

// iosMain
actual val platformModule: Module = module {
    single<HttpClientEngine> { Darwin.create() }
    single<KeyValueStore> { NSUserDefaultsKeyValueStore() }
}
```

## Testing

Don't boot Koin for unit tests — just construct the class manually with fakes:

```kotlin
class GetOrderUseCaseTest {
    private val repo = FakeOrderRepository()
    private val useCase = GetOrderUseCase(repo)

    @Test
    fun test() = runTest { ... }
}
```

For integration tests that need a full graph, create a test module and call `startKoin { modules(testModule) }` in `@BeforeTest` and `stopKoin()` in `@AfterTest`.

## Common errors and fixes

- **`NoBeanDefFoundException`** — the type isn't bound. Check the module's registered and the binding's there. For generics, the type must match exactly (`List<Order>` ≠ `List<*>`).
- **`KoinAppAlreadyStartedException`** — you called `startKoin` twice. Guard with `if (KoinPlatformTools.defaultContext().getOrNull() == null)`.
- **ViewModel dependency not found** — missing `factory { … }` for the VM, or the `parametersOf(...)` at the call site is missing an argument the factory expects.
- **Works on Android, fails on iOS (or vice versa)** — `platformModule`'s `actual` is missing a binding, or a new shared dependency needs a platform implementation. Check both `androidMain` and `iosMain` actuals.
