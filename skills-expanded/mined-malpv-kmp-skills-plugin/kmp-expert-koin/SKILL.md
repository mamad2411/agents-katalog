---
name: kmp-expert-koin
description: Structure dependency injection in a Kotlin Multiplatform project with Koin — module organization by feature/layer, constructor DSL (singleOf/viewModelOf), the initKoin entry points and their Swift-friendly overload, and a verify() graph test. Use whenever the user sets up or refactors DI, mentions Koin, modules, initKoin/doInitKoin, viewModelOf, platformModule, threading config into the graph, or a "no definition found"/graph-resolution error.
---

# Skill: KMP Expert Koin

This skill provides the official architectural standard for implementing dependency injection (DI) in Kotlin Multiplatform (KMP) projects, prioritizing Koin's modern constructor binding APIs (v4.0.0+), layered modularity, and testability.

> [!NOTE]
> **Placement (architecture-agnostic):** DI modules mirror the layers/features they wire — one module per layer (data/domain/presentation) or per feature. In a **modular** project (feature + layers) each module declares its own Koin module, aggregated in `:shared` — see `kmp-modular-architecture`. In a **single-module** project the Koin modules are packages under `commonMain`. This skill does not assume a module layout.

## DI Philosophy

1. **Layered Modularity**: Koin modules should reflect the logical structure of Clean Architecture (Data, Domain, Presentation).
2. **Type-Safe & Declarative**: Prefer `singleOf`, `factoryOf`, and `viewModelOf` to reduce boilerplate and automate constructor resolution.
3. **Coding to Interfaces**: Use `bind<Interface>()` to facilitate behavior testing through mocks/fakes.
4. **Controlled Lifecycle**: Koin is initialized from each native platform passing the required context (e.g., `androidContext` on Android, manual `initKoin()` on iOS).

---

## 1. Initial Setup in KMP

### Dependencies (libs.versions.toml)
```toml
[versions]
koin = "<version>"

[libraries]
koin-core = { group = "io.insert-koin", name = "koin-core", version.ref = "koin" }
koin-compose = { group = "io.insert-koin", name = "koin-compose", version.ref = "koin" }
koin-compose-viewmodel = { group = "io.insert-koin", name = "koin-compose-viewmodel", version.ref = "koin" }
koin-android = { group = "io.insert-koin", name = "koin-android", version.ref = "koin" }
```

### Configuration in build.gradle.kts (shared/features module)
```kotlin
commonMain.dependencies {
    implementation(libs.koin.core)
    implementation(libs.koin.compose)
    implementation(libs.koin.compose.viewmodel)
}
androidMain.dependencies {
    implementation(libs.koin.android)
}
```

### Initialization Helper (commonMain/kotlin/di/HelperKoin.kt)
Centralizes Koin configuration for multiplatform consumption.
```kotlin
import org.koin.core.context.startKoin
import org.koin.core.module.Module
import org.koin.dsl.KoinAppDeclaration

fun initKoin(appDeclaration: KoinAppDeclaration = {}) =
    startKoin {
        appDeclaration()
        modules(platformModule(), appModule())
    }

// Necessary overload to invoke from Swift without parameters
fun initKoin() = initKoin {}

expect fun platformModule(): Module
```

> [!NOTE]
> **Why two overloads, and why Swift calls it `doInitKoin`.** Kotlin **default arguments do not cross to Obj-C/Swift**, so Swift cannot omit the `KoinAppDeclaration` lambda — that is the only reason the parameterless overload exists. Do **not** write a Kotlin function literally named `doInitKoin`: the `do` prefix is generated automatically by Kotlin/Native, because `init*` collides with Objective-C's `init` method family. The Kotlin `initKoin()` is what Swift sees as `HelperKoinKt.doInitKoin()`.
>
> To pass config into the graph (for example a debug flag), thread it as a **parameter** rather than hardcoding it in a module — each platform entry point supplies it, and Kotlin resolves the overloads because it prefers the candidate without defaults:
>
> ```kotlin
> fun initKoin(isDebug: Boolean, appDeclaration: KoinAppDeclaration = {}) =
>     startKoin {
>         appDeclaration()
>         modules(platformModule(), networkModule(isDebug))  // module as a function
>     }
>
> fun initKoin(isDebug: Boolean) = initKoin(isDebug) {}   // Swift: doInitKoin(isDebug:)
> ```
>
> Android supplies it from `BuildConfig.DEBUG`, which requires enabling the feature explicitly — AGP does not generate `BuildConfig` by default:
>
> ```kotlin
> // androidApp/build.gradle.kts
> android {
>     buildFeatures { buildConfig = true }
> }
>
> // Application class — no import needed when the package matches the android namespace
> initKoin(isDebug = BuildConfig.DEBUG) { androidContext(this@MainApplication) }
> ```
>
> Swift resolves it with `#if DEBUG`, keeping a single call site:
>
> ```swift
> init() {
>     #if DEBUG
>     let isDebug = true
>     #else
>     let isDebug = false
>     #endif
>
>     HelperKoinKt.doInitKoin(isDebug: isDebug)
> }
> ```
>
> Verify the exposed signature in the generated header — it carries the `swift_name` attribute:
>
> ```objc
> + (…)doInitKoinIsDebug:(BOOL)isDebug __attribute__((swift_name("doInitKoin(isDebug:)")));
> ```

### Platform-Specific Implementation

#### Android (`androidMain`)
```kotlin
import org.koin.dsl.module
import org.koin.core.module.Module

actual fun platformModule(): Module = module {
    // Inject native Android dependencies that require Context (Room, EncryptedSharedPreferences)
}

// Initialization in Android Application class (MyApp.kt) or MainActivity
initKoin { 
    androidContext(this@MyApp) 
}
```

#### iOS Configuration

1. **Kotlin Platform-Specific Module** (`iosMain`):
```kotlin
import org.koin.dsl.module
import org.koin.core.module.Module

actual fun platformModule(): Module = module {
    // Inject native iOS implementations (Keychain wrapper, etc.)
}
```

2. **Swift Entry Point Integration** (`iosApp.swift`):
Initialize Koin within the `init()` constructor of your SwiftUI `App` structure.
```swift
import SwiftUI
import Shared

@main
struct ComposeApp: App {
    init() {
        HelperKoinKt.doInitKoin()
    }

    var body: some Scene {
        WindowGroup {
            ContentView().ignoresSafeArea(.all)
        }
    }
}
```

---

## 2. Layered Organization (Clean Architecture)

This section defines **how each layer is bound** — it does not prescribe how many module files a feature must have. Use the binding idiom that matches each layer, then group those bindings to fit the feature's actual size.

> [!NOTE]
> **Module granularity follows feature size, not a fixed template.**
> - **Default: one module per feature.** A single `authModule` holding the feature's data, domain, and presentation bindings is the right shape for most features. Reach for this first.
> - **Split by layer** (`dataModule` / `domainModule` / `viewModelModule` + aggregator) only once a feature grows enough that one file stops being readable, or when a layer must be included on its own — for example reusing `dataModule` in a test graph.
> - Do **not** create four files to hold two bindings. Ceremony that outnumbers the code it organizes is cost without payoff.
> - Declare a layer's module **only if that layer exists**. A feature with no presentation layer has no `viewModelModule` — do not invent UseCases or ViewModels to fill in the template.

### Default: one module per feature

```kotlin
import org.koin.core.module.dsl.viewModelOf // NOT org.koin.compose.viewmodel.dsl — deprecated in Koin 4.1
import org.koin.core.module.dsl.bind
import org.koin.core.module.dsl.factoryOf
import org.koin.core.module.dsl.singleOf
import org.koin.dsl.module

val authModule = module {
    // Data — DataSources and Repositories as singletons.
    // Bind the domain interface to its implementation.
    singleOf(::AuthRemoteDataSource)
    singleOf(::AuthRepositoryImpl) { bind<AuthRepository>() }

    // Domain — UseCases as factories: a new instance per execution flow.
    factoryOf(::LoginUseCase)

    // Presentation — ViewModels bound to the Composable lifecycle.
    viewModelOf(::LoginViewModel)
}
```

### Scaling up: split by layer

Once the feature justifies it, promote each layer to its own module in the feature's `di/` package and aggregate them. The bindings are unchanged — only their grouping is:

```kotlin
val dataModule = module {
    singleOf(::AuthRemoteDataSource)
    singleOf(::AuthRepositoryImpl) { bind<AuthRepository>() }
}

val domainModule = module {
    factoryOf(::LoginUseCase)
}

val viewModelModule = module {
    viewModelOf(::LoginViewModel)
}

// Feature aggregator — the single entry point the app graph includes
val authModule = module {
    includes(dataModule, domainModule, viewModelModule)
}
```

> [!TIP]
> **Name the module after the feature, not the layer it started with.** A feature module named `authNetworkModule` that also binds repositories and UseCases has a name that lies about its scope. Use `authModule` — the aggregating name stays accurate as the feature grows, so the module never needs renaming when a layer is added.

---

## Best Practices

- **Use `singleOf`**: For unique instances persisted in memory (API clients, Repositories, Databases).
- **Use `factoryOf`**: For stateless classes or classes that should be recreated (Use Cases, Presenters).
- **Use `viewModelOf`**: To bind your ViewModels to the Composable lifecycle natively.
- **Avoid manual `get()` in constructors**: Let Koin's constructor binding functions (`singleOf(::MyClass)`) auto-detect and inject required parameters implicitly.
- **Inject Coroutine Dispatchers**: Do not use `Dispatchers.IO` directly in network or database code. Inject `CoroutineDispatcher` to make it easily mockable in unit tests:
  ```kotlin
  single<CoroutineDispatcher> { Dispatchers.IO }
  ```

---

## 3. Graph Verification Test

Koin resolves dependencies at **runtime**: a compiling project proves nothing about the graph. A missing binding surfaces as a crash on app start, not as a compile error — and `singleOf(::X)` makes this more important, not less, since constructor params are matched by type with no compile-time check.

`verify()` walks every constructor by reflection and fails if a type has no binding. It **does not instantiate anything**, so it needs no emulator and no real `Context` — which is what makes it viable for graphs holding Android-only engines (`EncryptedSharedPreferences`, Room). It traverses `includes(...)`, so a single test covers a composed graph.

```kotlin
// Dependency: io.insert-koin:koin-test
// Placement: verify() uses reflection — it is JVM-only. It cannot live in commonTest;
// put it in the JVM/Android host test source set (androidHostTest, androidUnitTest, or jvmTest).

class KoinGraphTest {

    @OptIn(KoinExperimentalAPI::class)
    @Test
    fun koin_graph_resolves_every_dependency() {
        val graph = module {
            includes(platformModule(), securityModule, networkModule(isDebug = false), authModule)
        }
        // Types supplied at runtime rather than by a module (androidContext) go in extraTypes.
        graph.verify(extraTypes = listOf(Context::class))
    }
}
```

> [!TIP]
> **Prove the test has teeth.** A module that only holds `includes(...)` declares no definitions of its own — if the assertion were vacuous it would pass while verifying nothing. Confirm it fails before trusting it: drop one module from the list and check the test reports `MissingKoinDefinitionException`, then restore it.

> [!NOTE]
> **`verify()` vs `checkModules()`.** `checkModules()` actually **instantiates** every definition, so it needs a real runtime and will fail on platform engines that require an Android `Context`. Prefer `verify()` for graph-shape validation in host tests; reserve `checkModules()` for instrumented tests where a real context exists.

---

## References

- [Koin Official Documentation](https://insert-koin.io/)
- [Koin Compose ViewModel in KMP](https://insert-koin.io/docs/reference/koin-compose/viewmodel)
