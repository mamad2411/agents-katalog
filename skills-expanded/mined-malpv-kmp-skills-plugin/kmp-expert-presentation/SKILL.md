---
name: kmp-expert-presentation
description: Build the presentation layer of a KMP feature — ViewModels with viewModelScope, a single UiState per screen, session restore with offline handling, and Compose consumption via koinViewModel/collectAsStateWithLifecycle. Use whenever the user builds a screen's logic, mentions ViewModel, UI state, StateFlow, loading/error states, when a UseCase is warranted, wiring a screen to a repository, or logout/session-restore behavior — even if they just say "make the login screen actually log in".
---

# Skill: KMP Expert Presentation

This skill defines the standard for the **presentation layer** in Kotlin Multiplatform: how a screen holds state, how it reaches the domain, and how Compose consumes it. It is the layer that turns a data layer into a working app.

Three skills touch the same screen and must not overlap:

| Skill | Owns | Answers |
|:---|:---|:---|
| `kmp-expert-navigation` | Routes, `Actions` | Where does the screen go? |
| **`kmp-expert-presentation`** | ViewModel, `UiState` | **What does the screen know?** |
| `mobile-design` | Theme, tokens, components | How does the screen look? |

This skill owns state and data flow only. It prescribes no colors, spacing, or component styling — that is `mobile-design`'s job.

> [!NOTE]
> **Placement (architecture-agnostic):** ViewModels and their `UiState` belong to the **presentation** layer, alongside the screens they serve. In a **modular** project (feature + layers) each ViewModel lives in its own feature's presentation package — see `kmp-modular-architecture`. In a **single-module** project they are packages under `commonMain`. This skill does not assume a module layout.

---

## Presentation Standards

1. **Real ViewModels only**: extend `androidx.lifecycle.ViewModel` and use `viewModelScope`. Never hand-roll a `CoroutineScope`.
2. **One state object per screen**: a single `UiState` data class, never a fan of loose `StateFlow`s.
3. **Immutable outward**: expose `StateFlow` via `asStateFlow()`; mutate only through `update { it.copy(...) }`.
4. **No leaking `ResultState` to the UI**: the ViewModel maps transport results into screen state.

---

## 1. Dependencies

```toml
[libraries]
koin-compose-viewmodel = { group = "io.insert-koin", name = "koin-compose-viewmodel", version.ref = "koin" }
androidx-lifecycle-viewmodelCompose = { module = "org.jetbrains.androidx.lifecycle:lifecycle-viewmodel-compose", version.ref = "androidx-lifecycle" }
androidx-lifecycle-runtimeCompose = { module = "org.jetbrains.androidx.lifecycle:lifecycle-runtime-compose", version.ref = "androidx-lifecycle" }
```

---

## 2. The ViewModel

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class LoginUiState(
    val username: String = "",
    val password: String = "",
    val isLoading: Boolean = false,
    val error: String? = null,
    val loggedUser: User? = null
)

class LoginViewModel(
    private val repository: AuthRepository
) : ViewModel() {

    private val _state = MutableStateFlow(LoginUiState())
    val state: StateFlow<LoginUiState> = _state.asStateFlow()

    fun onUsernameChanged(value: String) {
        _state.update { it.copy(username = value, error = null) }
    }

    fun login() {
        val current = _state.value
        if (current.username.isBlank() || current.password.isBlank()) {
            _state.update { it.copy(error = "Username and password are required") }
            return
        }

        viewModelScope.launch {
            repository.login(current.username.trim(), current.password).collect { result ->
                when (result) {
                    is ResultState.Loading -> _state.update { it.copy(isLoading = true, error = null) }
                    is ResultState.Success -> _state.update { it.copy(isLoading = false, loggedUser = result.data) }
                    is ResultState.Error -> _state.update {
                        it.copy(isLoading = false, error = result.customMessage ?: "Unexpected error")
                    }
                }
            }
        }
    }
}
```

> [!WARNING]
> **Never hand-roll a `CoroutineScope` in a ViewModel.** A class that does not extend `ViewModel` has no lifecycle, so nothing ever calls `onCleared()` and the scope is **never cancelled** — every in-flight request outlives the screen. This leaks quietly: no crash, no log, just coroutines accumulating on every navigation.
>
> ```kotlin
> // WRONG — no lifecycle, scope never cancelled, leaks on every screen exit
> class ChecklistViewModel(private val repository: DashboardRepository) {
>     private val viewModelScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
> }
>
> // RIGHT — viewModelScope is cancelled automatically in onCleared()
> class ChecklistViewModel(private val repository: DashboardRepository) : ViewModel()
> ```

> [!WARNING]
> **One `UiState`, not many `StateFlow`s — and never public mutable fields.** Loose flows cannot be updated atomically: a screen recomposes between two `.value` assignments and renders a state that never logically existed (for example `isLoading = false` while the list is still empty). Public `var` fields are worse — invisible to Compose, so mutating them recomposes nothing.
>
> ```kotlin
> // WRONG — no atomic update, and mutable state Compose cannot observe
> private val _evaluationsState = MutableStateFlow<ResultState<List<DomEvaluation>>>(ResultState.Loading)
> val evaluationsState: StateFlow<...> = _evaluationsState  // exposed without asStateFlow(): castable back to Mutable
> private val _currentIndex = MutableStateFlow(0)
> var activeEvaluationName: String = ""                     // Compose never sees this change
>
> // RIGHT — a single atomic state object
> data class ChecklistUiState(
>     val evaluations: List<DomEvaluation> = emptyList(),
>     val currentIndex: Int = 0,
>     val activeEvaluationName: String = "",
>     val isLoading: Boolean = false,
>     val error: String? = null
> )
> private val _state = MutableStateFlow(ChecklistUiState())
> val state: StateFlow<ChecklistUiState> = _state.asStateFlow()
> ```
>
> Always publish with `asStateFlow()`. Exposing the `MutableStateFlow` typed as `StateFlow` still lets any caller cast it back and write to it.

---

## 3. When a UseCase Earns Its Place

A UseCase is justified only when it holds logic that is **not a single repository call**: orchestrating several repositories, applying a business rule, or transforming data. When it only forwards, it is an indirection layer to read and maintain for nothing.

```kotlin
// WRONG — pure delegation, adds a file and a hop, changes nothing
class GetProductsUseCase(private val repository: ProductRepository) {
    operator fun invoke() = repository.getProducts()
}

// RIGHT — the ViewModel talks to the repository directly
class DashboardViewModel(private val repository: ProductRepository) : ViewModel()

// RIGHT — a UseCase that orchestrates and owns a rule the repository does not
class CheckoutUseCase(
    private val cart: CartRepository,
    private val payments: PaymentRepository
) {
    suspend operator fun invoke(): CheckoutResult { /* multi-repository rule */ }
}
```

> [!WARNING]
> **A UseCase does not prevent duplicated rules — it creates a place to duplicate them.** If a rule lives in the UseCase, the ViewModel must not re-check it:
>
> ```kotlin
> // WRONG — the same rule enforced in both layers; they drift the day one changes
> class LoginUseCase(private val repository: AuthRepository) {
>     suspend operator fun invoke(email: String, password: String): LoginResult {
>         if (email.isBlank() || password.isBlank()) return LoginResult.Failure("Fields required")
>         return repository.login(email.trim(), password)
>     }
> }
> class LoginViewModel(private val loginUseCase: LoginUseCase) : ViewModel() {
>     fun login() {
>         if (state.value.email.isBlank()) { /* the very same check, again */ }
>     }
> }
> ```
>
> Pick one owner per rule. Input validation for form fields belongs to the ViewModel; domain rules belong below it.

---

## 4. Consuming State from Compose

Screens take navigation callbacks (see `kmp-expert-navigation`) and resolve their own ViewModel through Koin.

```kotlin
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import org.koin.compose.viewmodel.koinViewModel

@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit,
    modifier: Modifier = Modifier,
    viewModel: LoginViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    // One-shot navigation reacting to a state change, keyed so it fires once.
    LaunchedEffect(state.loggedUser) {
        if (state.loggedUser != null) onLoginSuccess()
    }

    when {
        state.isLoading -> LoadingContent()
        state.error != null -> ErrorContent(message = state.error, onRetry = viewModel::login)
        else -> LoginForm(state = state, onLogin = viewModel::login)
    }
}
```

Use `collectAsStateWithLifecycle()`, not `collectAsState()`: it stops collecting when the screen leaves the foreground.

### Route arguments

A route argument comes from navigation, not from the DI graph, so it is passed at the call site:

```kotlin
// DI — the argument is a parameter, not a binding
viewModel { params -> DetailViewModel(productId = params.get(), repository = get()) }

// Screen
@Composable
fun DetailScreen(
    productId: Int,
    onBack: () -> Unit,
    viewModel: DetailViewModel = koinViewModel { parametersOf(productId) }
)
```

> [!NOTE]
> **Type the route argument to match the domain.** A `Detail(productId: String)` route feeding a domain whose `Product.id` is an `Int` forces a conversion at the boundary and fails at runtime on bad input. Model the route argument as the domain type.

---

## 5. Session State and Navigation Gating

Restoring a session on start is the canonical case where presentation drives navigation.

```kotlin
sealed interface SessionState {
    data object Checking : SessionState
    data class Authenticated(val user: User) : SessionState
    data object Unauthenticated : SessionState
}

class SessionViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _state = MutableStateFlow<SessionState>(SessionState.Checking)
    val state: StateFlow<SessionState> = _state.asStateFlow()

    init { restoreSession() }

    fun restoreSession() {
        // Skip the network entirely on first launch: nothing is stored yet.
        if (!repository.hasStoredSession()) {
            _state.value = SessionState.Unauthenticated
            return
        }
        viewModelScope.launch {
            repository.getCurrentUser().collect { result ->
                _state.value = when (result) {
                    is ResultState.Loading -> SessionState.Checking
                    is ResultState.Success -> SessionState.Authenticated(result.data)
                    is ResultState.Error -> SessionState.Unauthenticated
                }
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            repository.logout().collect { result ->
                if (result is ResultState.Success) _state.value = SessionState.Unauthenticated
            }
        }
    }
}
```

```kotlin
@Composable
fun AppNavigation(sessionViewModel: SessionViewModel = koinViewModel()) {
    val session by sessionViewModel.state.collectAsStateWithLifecycle()

    // Compose the NavHost only once the session resolves.
    if (session is SessionState.Checking) {
        LoadingContent()
        return
    }

    NavHost(
        navController = navController,
        startDestination = if (session is SessionState.Authenticated) Destinations.Dashboard else Destinations.Login
    ) { /* ... */ }
}
```

> [!WARNING]
> **`startDestination` is captured once.** `NavHost` reads it on first composition and ignores later changes. Composing the `NavHost` while the session is still `Checking` pins the app to the login screen even after the session resolves. Gate the `NavHost` behind the resolved state, as above.

> [!WARNING]
> **Wire logout to actually clear the session.** A `logout()` on the repository that clears tokens is worthless if nothing calls it — a screen whose logout button only navigates leaves the tokens in encrypted storage, and the next launch silently restores the session. This defect passes compilation, DI verification, and every test.
>
> ```kotlin
> // WRONG — navigates away; the session survives
> onLogout = actions::logout
>
> // RIGHT — clear the session, then navigate
> onLogout = {
>     sessionViewModel.logout()
>     actions.logout()
> }
> ```

---

## 6. DI Registration

Bind ViewModels in the feature module (see `kmp-expert-koin` for module granularity):

```kotlin
// The ViewModel DSL lives in org.koin.core.module.dsl as of Koin 4.1.
// org.koin.compose.viewmodel.dsl.viewModelOf is deprecated — it still compiles, with a warning.
// The koinViewModel() Composable is unaffected: it stays in org.koin.compose.viewmodel.
import org.koin.core.module.dsl.bind
import org.koin.core.module.dsl.singleOf
import org.koin.core.module.dsl.viewModelOf

val authModule = module {
    // Data
    singleOf(::AuthRemoteDataSource)
    singleOf(::AuthRepositoryImpl) { bind<AuthRepository>() }

    // Presentation
    viewModelOf(::LoginViewModel)
    viewModelOf(::SessionViewModel)
}
```

> [!NOTE]
> **`viewModelOf` is verifiable; `viewModel { ... }` is not.** Koin's `verify()` only introspects constructor-reference definitions. A ViewModel bound through a lambda (as parameterized ones must be) is skipped by graph verification — its dependencies are checked only at runtime. Prefer `viewModelOf` wherever the ViewModel takes no runtime parameter.

---

## Verification

A compiling project with a green DI graph proves nothing about the presentation layer. Verify by running the flow:

- The screen renders **real data**, not placeholder literals. Hardcoded sample content is the signature of a UI wired to nothing — if the data layer exists and the screen never calls it, the feature does not work regardless of what compiles.
- Loading, error, and retry states each render.
- Session restore survives an app restart; logout does not.

---

## References

- [Koin Compose ViewModel in KMP](https://insert-koin.io/docs/reference/koin-compose/viewmodel)
- [Jetpack Lifecycle ViewModel in KMP](https://www.jetbrains.com/help/kotlin-multiplatform-dev/compose-viewmodel.html)
