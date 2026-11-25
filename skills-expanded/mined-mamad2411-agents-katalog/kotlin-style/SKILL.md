---
name: kotlin-style
description: Project-specific Kotlin conventions — the rules that aren't already in the official Kotlin style guide. Covers the `Outcome<T>` / `DomainError` boundary contract, the `runCatching → toOutcome` rule, naming conventions for this codebase, and where idioms diverge from defaults. Load whenever writing or reviewing Kotlin in this project.
---

# Kotlin style (project delta)

For everything not below, the [official Kotlin style guide](https://kotlinlang.org/docs/coding-conventions.html) applies. This file only documents where this project's conventions add to or override the defaults.

## When this applies

The error-handling contract below is **opinionated for this project's scaffold** (`Outcome<T>` + `DomainError` from `/init-android-app`). On an existing app:

- Codebase already uses `kotlin.Result` everywhere → don't refactor to `Outcome` unless the user asks; apply only the `CancellationException`-rethrow rule.
- Codebase throws across boundaries → flag it, but don't pretend `Outcome` is universal Kotlin practice.
- The naming and immutability sections apply regardless of stack.

## Naming (project-specific)

- **Use cases**: verb-based, suffixed `UseCase` — `GetUserProfileUseCase`, `SubmitOrderUseCase`. One class per business action.
- **Repository implementations**: interface in `domain/`, implementation in `data/` suffixed `Impl` (`OrderRepository` ⇄ `OrderRepositoryImpl`).
- **Composables**: noun-based, named after what they render (`OrderRoute` vs `OrderScreen` — see `compose-ui` for the Route/Screen split).
- **UiState / UiEvent**: sealed types per screen, named `<Feature>UiState`, `<Feature>UiEvent`.
- **DTOs**: suffix `Dto` (`OrderDto`), kept in `<feature>/data/remote/` next to their `toDomain()` mapper.

The rest of naming follows Kotlin defaults — `PascalCase` types, `camelCase` functions/values, `UPPER_SNAKE_CASE` for `const val`.

## Typed IDs

Use `@JvmInline value class` for IDs that would otherwise be raw `String` / `Long`:

```kotlin
@JvmInline value class OrderId(val raw: String)
@JvmInline value class UserId(val raw: String)
```

Catches `getOrder(userId)` mix-ups at compile time, costs nothing at runtime.

## Error-handling contract

**Domain-facing signatures return `Outcome<T>`, never `Result<T>` and never raw `throw`.** The two types are defined once in `core/domain/Outcome.kt` and `core/domain/DomainError.kt` (see `android-app-skeleton`); every use case, repository method, and ViewModel that needs a typed failure goes through them.

```kotlin
sealed interface Outcome<out T> {
    data class Success<T>(val value: T) : Outcome<T>
    data class Failure(val error: DomainError) : Outcome<Nothing>
}

sealed class DomainError(open val cause: Throwable? = null) {
    data class Network(override val cause: Throwable? = null) : DomainError(cause)
    data class Unauthorized(override val cause: Throwable? = null) : DomainError(cause)
    data class NotFound(override val cause: Throwable? = null) : DomainError(cause)
    data class Server(val code: Int, override val cause: Throwable? = null) : DomainError(cause)
    data class Unknown(override val cause: Throwable? = null) : DomainError(cause)
}
```

**`runCatching` only inside the data layer, only piped through `toOutcome`:**

```kotlin
runCatching { api.getOrder(id.raw).toDomain() }.toOutcome(::toDomainError)
```

The canonical adapter lives in `core/data/network/Outcomes.kt`. It rethrows `CancellationException` — **open-coded `runCatching { ... }.fold(...)` silently swallows cancellation** and is the single most common bug this rule prevents. The reviewer flags any open-coded `runCatching.fold(...)` and any `Result<T>` return on a `domain/` interface.

Map exceptions to `DomainError` at the repository boundary. The domain layer must not know about `IOException` or `HttpException`.

## Coroutines (project rules)

Standard Kotlin coroutine rules apply; this project adds:

- **No `GlobalScope`** anywhere. The reviewer flags it.
- **Dispatcher boundary in the repository, not the ViewModel.** `viewModelScope.launch { repository.fetch() }` — the repository's `withContext(Dispatchers.IO)` is where the switch happens.
- **`StateFlow` for UI state, `Channel` for one-shot effects.** `SharedFlow` only when you genuinely need replay semantics. `LiveData` is forbidden in new code.
- Collect with `collectAsStateWithLifecycle()`, never `collectAsState()` — see `compose-ui`.

## Sealed hierarchies in this project

The three sealed types the codebase relies on (don't reinvent them):

- `Outcome<T>` — every domain-facing result.
- `DomainError` — every domain-facing failure.
- `<Feature>UiState` — every screen's state machine. Branches are `Loading` / `Error` / `Success` by convention; add more only when the screen genuinely has them.

Prefer `sealed interface` over `sealed class` when there's no shared state.

## Immutability and copy

State updates copy, never mutate:

```kotlin
_state.update { it.copy(items = it.items + newItem) }
```

`MutableStateFlow.update { }` is preferred over `value = value.copy(...)` — the lambda runs atomically.

## Visibility

- `private` for file-/class-internal helpers.
- `internal` for module-internal APIs once `:feature:*` / `:core:*` modules exist (see `android-architecture` → "Module or package?"). In a single `:app` module, `internal` is equivalent to `public` — don't over-rely on it.
- `public` should be deliberate.
