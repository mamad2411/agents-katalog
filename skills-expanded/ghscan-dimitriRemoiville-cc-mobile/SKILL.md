---
name: kmm-architecture
description: How MVVM + Clean Architecture is applied in this Kotlin Multiplatform codebase — source-set placement, `expect`/`actual` vs. interface injection, layer boundaries inside `commonMain`, and how ViewModels reach both Android and iOS. Load when designing a feature, deciding where code belongs, or reviewing layer boundaries in the shared module.
---

# KMM architecture

## The three layers, inside `commonMain`

```
presentation  — ViewModels, UiState/UiEvent/UiAction.  (Runs on both platforms)
      ↓
   domain     — Pure Kotlin. Models, repository interfaces, use cases.
      ↑
    data      — Repository implementations. Ktor clients, SQLDelight DAOs, mappers.
```

**Dependency rule:** `presentation → domain ← data`. Same as the native Android and iOS setups. The domain layer imports only `Foundation`-equivalent Kotlin + coroutines + kotlinx-* (serialization, datetime).

## Source-set decision tree

When adding code, ask:
1. Does it compile on both JVM and Native with only `kotlinx-*` dependencies? → **`commonMain`**.
2. Does it need a JVM-only library (OkHttp, Room, Android Context)? → **`androidMain`**.
3. Does it need an Apple framework (`Foundation`, `UIKit`, `Security` for Keychain)? → **`iosMain`**.
4. Does a single narrow operation differ per platform (like getting a `HttpClient` engine)? → `expect`/`actual`.
5. Does a wider surface differ per platform (a `KeyValueStore`, a `CryptoProvider`)? → **interface in `commonMain`**, implementations in platform source sets, bound via Koin.

Prefer the higher-numbered options only when the lower ones don't fit. `commonMain`-first.

## `expect` / `actual` vs. interface + Koin

**Use `expect` / `actual`** when:
- The surface is small (one or two functions).
- There's no reasonable common implementation.
- The caller wouldn't benefit from swapping the implementation (it's truly platform-fixed).

```kotlin
// commonMain
internal expect fun platformHttpEngine(): HttpClientEngine

// androidMain
internal actual fun platformHttpEngine(): HttpClientEngine = OkHttp.create()

// iosMain
internal actual fun platformHttpEngine(): HttpClientEngine = Darwin.create()
```

**Use an interface + Koin** when:
- The surface has multiple methods.
- Tests need to substitute a fake.
- The abstraction is useful even within a single platform (e.g. a `KeyValueStore` with in-memory, file-backed, and encrypted variants).

```kotlin
// commonMain/domain
interface KeyValueStore {
    suspend fun getString(key: String): String?
    suspend fun putString(key: String, value: String)
    suspend fun remove(key: String)
}

// androidMain
class DataStoreKeyValueStore(private val dataStore: DataStore<Preferences>) : KeyValueStore { ... }

// iosMain
class NSUserDefaultsKeyValueStore : KeyValueStore { ... }
```

## What goes where

| Layer | `commonMain` | `androidMain` | `iosMain` |
|---|---|---|---|
| Domain models | ✓ | | |
| Use cases | ✓ | | |
| Repository interfaces | ✓ | | |
| Repository impls | ✓ (when using `HttpClient` + SQLDelight) | Android-specific impls only | iOS-specific impls only |
| DTOs (`@Serializable`) | ✓ | | |
| Mappers | ✓ | | |
| Ktor `HttpClient` config | ✓ | Platform engine (OkHttp) | Platform engine (Darwin) |
| SQLDelight schema | ✓ | `SqlDriver` (Android driver) | `SqlDriver` (Native driver) |
| ViewModels | ✓ | | |
| Koin modules | core modules common; platform-specific as needed | `androidModule` (binds `Context`, `SharedPreferences`, etc.) | `iosModule` (binds Darwin-specific impls) |
| Navigation | | ✓ (Navigation-Compose) | ✓ (`NavigationStack` in Swift) |
| UI | | ✓ (Jetpack Compose) | ✓ (SwiftUI) |

## Feature skeleton (for a new feature called `orders`)

```
shared/src/commonMain/kotlin/com/example/app/feature/orders/
├── domain/
│   ├── model/Order.kt
│   ├── model/OrderId.kt            # value class
│   ├── repository/OrderRepository.kt
│   └── usecase/GetOrderUseCase.kt
├── data/
│   ├── remote/OrderApi.kt
│   ├── remote/OrderDto.kt
│   ├── mapper/OrderMapper.kt
│   ├── repository/OrderRepositoryImpl.kt
│   └── di/orderDataModule.kt
└── presentation/orders/
    ├── OrderUiState.kt
    ├── OrderUiEvent.kt
    ├── OrderAction.kt
    └── OrderViewModel.kt

shared/src/commonTest/kotlin/com/example/app/feature/orders/
├── domain/usecase/GetOrderUseCaseTest.kt
├── data/mapper/OrderMapperTest.kt
├── data/repository/OrderRepositoryImplTest.kt   # uses Ktor MockEngine
└── presentation/OrderViewModelTest.kt
```

## ViewModel reaches for both platforms

A shared ViewModel extends `androidx.lifecycle.ViewModel` (multiplatform-ready):

```kotlin
class OrderViewModel(
    private val getOrder: GetOrderUseCase,
) : ViewModel() {
    private val _state = MutableStateFlow<OrderUiState>(OrderUiState.Loading)
    val state: StateFlow<OrderUiState> = _state.asStateFlow()

    private val _events = Channel<OrderUiEvent>(Channel.BUFFERED)
    val events: Flow<OrderUiEvent> = _events.receiveAsFlow()

    fun onAction(action: OrderAction) { ... }
}
```

- **Android** collects `state` in a Composable via `viewModel.state.collectAsStateWithLifecycle()` and sends actions with `viewModel::onAction`.
- **iOS** wraps the ViewModel in a `@Observable` Swift class that subscribes to `state` and exposes Swift-friendly properties. See `kmm-ios-interop` skill.

## Layer checklist for a new feature

- [ ] Domain model in `commonMain/.../domain/model/`
- [ ] Repository interface in `commonMain/.../domain/repository/`
- [ ] Use case(s) in `commonMain/.../domain/usecase/` (if warranted)
- [ ] DTO + mapper in `commonMain/.../data/`
- [ ] Ktor API wrapper in `commonMain/.../data/remote/`
- [ ] RepositoryImpl in `commonMain/.../data/repository/`
- [ ] Koin module in `commonMain/.../data/di/`, registered at the root
- [ ] UiState / UiAction / UiEvent in `commonMain/.../presentation/<feature>/`
- [ ] ViewModel in `commonMain/.../presentation/<feature>/`
- [ ] Platform-specific impls only if truly necessary (and bound via Koin)
- [ ] Tests in `commonTest/` for use cases, mappers, repository (with MockEngine), ViewModel
- [ ] Android UI consuming `:shared` (in `../android/`)
- [ ] iOS UI consuming the framework (in `../ios/`)
