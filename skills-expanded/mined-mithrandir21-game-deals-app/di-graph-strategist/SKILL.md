---
name: di-graph-strategist
description: Plan or fix dependency-injection graphs for Android/KMP — Hilt or Koin setup, scoping decisions, multi-module DI, KMP-friendly DI patterns, and splitting god-modules into bounded contexts. Use whenever the user asks about "Hilt setup", "Koin setup", "scoping", "@Singleton vs @ActivityScoped", "dependency injection", "DI module organization", "Hilt across modules", "Koin in KMP", or has a DI graph that's grown unwieldy. Also use for "this should be injected but it isn't" type questions.
---

# DI Graph Strategist

Dependency injection earns its complexity when it gives you clear boundaries, swap-in fakes for tests, and obvious scopes. It becomes a tax when modules are too granular, scopes are wrong, or the framework is fighting the codebase. This skill helps you keep DI doing its job.

## When to use

Triggers: "Hilt", "Koin", "DI", "@Singleton", "@ActivityScoped", "@Provides", "module", "scoping", "qualifier", "multi-module DI", "KMP DI", "@AssistedInject", "circular dependency".

For "add a binding for X", just add it. Use this skill when the question is structural.

## Process

### Phase 1: Pick or confirm the framework

If the project already uses one, match it. Otherwise:

| Project shape | Pick |
|---|---|
| Pure Android, Java/Kotlin mix possible, large team | Hilt — opinionated, codegen, compile-time safety |
| Android + small KMP shared module, Kotlin-only | Hilt on Android side, manual wiring in shared. Or Koin everywhere. |
| KMP-heavy, want one DI across platforms | Koin |
| Small app, prefer simplicity | Koin or hand-rolled |

Don't mix DI frameworks in one module. Mixing across modules is fine.

### Phase 2: Lay out the modules

Each Gradle module should own its own DI module:

```
:feature:onboarding
└── di/OnboardingModule.kt   // binds OnboardingRepository, OnboardingApi, etc.

:data:user
└── di/UserDataModule.kt     // binds UserRepository, UserDao, UserApi

:core:network
└── di/NetworkModule.kt      // binds OkHttp, Retrofit, common interceptors
```

Rules:
- A module exposes interfaces, binds implementations.
- Cross-module dependencies go through interfaces in `:api` modules or `:core`.
- Avoid one giant `AppModule` in `:app`. It becomes a god object.

**Hilt: `@InstallIn` choices**

| Component | Lifetime | Use for |
|---|---|---|
| `SingletonComponent` | App | Repos, network clients, DB |
| `ActivityRetainedComponent` | Activity, survives config change | Things shared between an Activity and its ViewModels |
| `ViewModelComponent` | ViewModel | Per-ViewModel dependencies |
| `ActivityComponent` | Activity, dies on rotation | Rarely used |
| `FragmentComponent` | Fragment | Rarely used |
| `ServiceComponent` | Service | Per-service dependencies |

Default to `SingletonComponent` for repos and shared services. Reach for narrower scopes only when you have a reason.

**Koin: modules and scopes**

```kotlin
val userModule = module {
    single<UserRepository> { UserRepositoryImpl(get(), get()) }
    factory { UserMapper() }
}

val featureModule = module {
    viewModel { OnboardingViewModel(get()) }
    scope<OnboardingActivity> {
        scoped { OnboardingNavigator() }
    }
}
```

Koin's `scope` lets you tie objects to lifecycles you control. Use sparingly.

### Phase 3: Decide what to inject and what not to

Inject:
- Dependencies that the consumer doesn't construct itself.
- Things with non-trivial lifetimes (repos, clients, daos).
- Things you want to swap in tests (interfaces).

Don't inject:
- Pure functions or stateless helpers — just import them.
- `data class` models — construct directly.
- Small per-call values — pass as parameters.

If a class has more than ~6 constructor parameters, it's probably doing too much. DI didn't cause that; it just exposed it.

### Phase 4: Common patterns

**Qualifiers for multiple implementations of one interface**

```kotlin
// Hilt
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class Authenticated
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class Anonymous

@Provides @Authenticated
fun authedClient(...): OkHttpClient = ...

@Provides @Anonymous
fun anonClient(...): OkHttpClient = ...
```

```kotlin
// Koin
single<OkHttpClient>(named("authenticated")) { ... }
single<OkHttpClient>(named("anonymous")) { ... }
```

**Assisted injection** — when an object needs both injected and runtime parameters:

```kotlin
// Hilt
class DocumentEditor @AssistedInject constructor(
    private val repo: DocumentRepository,
    @Assisted private val documentId: String,
)

@AssistedFactory interface Factory {
    fun create(documentId: String): DocumentEditor
}
```

ViewModels with parameters use `SavedStateHandle` + Hilt's `@HiltViewModel`, or assisted injection.

**Lazy injection** to break init-time work:

```kotlin
class Foo @Inject constructor(
    private val heavy: Lazy<HeavyDependency>,   // dagger.Lazy
)
```

Used to delay construction of an expensive dependency until first access.

### Phase 5: KMP DI

Hilt is Android-only. For KMP shared code, options:

**Option A: Manual wiring in shared, Hilt on Android**

```kotlin
// commonMain
class SharedGraph(
    private val httpClient: HttpClient,
    private val database: Database,
) {
    val userRepository: UserRepository by lazy { UserRepositoryImpl(httpClient, database) }
}
```

Android side: provide `SharedGraph` from Hilt, access its properties.
iOS side: construct `SharedGraph` in Swift, pass to Swift-side wiring.

**Option B: Koin everywhere**

```kotlin
// commonMain
val sharedModule = module {
    single<UserRepository> { UserRepositoryImpl(get(), get()) }
}

// androidMain or shared startKoin
startKoin { modules(sharedModule, androidModule) }
```

iOS: same `startKoin` call from Swift, resolve via `KoinJavaComponent` or generated helpers.

Pick one and stick with it. Mixing inside the shared module is painful.

### Phase 6: Diagnose existing graph issues

If the graph is already a mess, look for:

- **God modules** — one `AppModule.kt` with 30+ `@Provides`. Split by domain.
- **Wrong scopes** — `@Singleton` on something that should be per-screen (holds Activity state), or vice versa. Symptom: leaks or stale state.
- **Circular dependencies** — Hilt/Koin will complain. Usually a sign of poor layer boundaries. Fix by extracting a third type both depend on.
- **`@Provides` returning concrete types instead of interfaces** — couples the graph; harder to swap in tests.
- **Direct Hilt usage in commonMain** — won't compile. Push the binding to `androidMain` or use the manual graph pattern.

### Phase 7: Test the graph

- For Hilt, the build itself validates the graph. If it compiles, it resolves.
- Write at least one Hilt test (`@HiltAndroidTest`) that confirms key bindings exist with the expected scopes.
- For Koin, `checkModules()` in a unit test validates all bindings resolve.

## Output

For a setup or refactor:

1. **Framework choice** (with reason if not obvious).
2. **Module layout** — one DI module per Gradle module.
3. **Scope policy** — defaults and exceptions.
4. **KMP strategy** if applicable.
5. **Migration steps** if reorganizing an existing graph.

## Common pitfalls

- **Scoping everything as `@Singleton`.** Hides lifecycle bugs; objects holding view state survive too long.
- **Scoping ViewModels manually.** `@HiltViewModel` and Koin's `viewModel { }` already handle this. Don't double-wrap.
- **`@Provides` and `@Binds` in the same module.** Hilt allows it but it makes the module noisier. Pick one style per module.
- **Injecting `Context` everywhere.** Inject `@ApplicationContext` specifically. Anything that needs an `Activity` context shouldn't be a Singleton.
- **Custom Hilt components.** Almost never needed. Defaults cover ~95% of cases.
- **Putting the whole graph in `:app`.** Defeats modularization; `:app` rebuilds on every DI change.
