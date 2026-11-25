---
name: kotlin-android-compose
description: Builds Jetpack Compose screens with state hoisting, ViewModels and one-way data flow, so UI stays stateless, previewable and easy to test.
---

# Kotlin Android Compose

State goes down, events go up. Composables that draw take values and lambdas, nothing else.

## Steps

1. Read the module's existing screens, its Gradle version catalog and its DI setup (Hilt, Koin or manual). Match them.
2. Define a `UiState` as a sealed interface or data class: loading, content, error. Define a `UiEvent` or plain methods on the ViewModel for user actions.
3. The ViewModel exposes `StateFlow<UiState>` built with `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), initial)`. One-off effects such as navigation or snackbars go through a `Channel` collected once, or become state that the UI consumes and clears.
4. Write two composables per screen. `FooRoute(viewModel)` collects with `collectAsStateWithLifecycle()` and wires navigation. `FooScreen(state, onEvent)` is stateless and has a `@Preview` for each state.
5. Hoist state to the lowest common parent that reads it. Use `rememberSaveable` for UI-only state that must survive rotation, such as a text field or scroll position.
6. Lists: `LazyColumn` with `key = { it.id }` and `contentType`. Pass immutable or `@Immutable` types, or `kotlinx.collections.immutable` lists, so items skip recomposition.
7. Effects: `LaunchedEffect(key)` only for work tied to a key, never to call ViewModel methods on every composition. Clean up with `DisposableEffect`.
8. Test the ViewModel with a fake repository and `runTest`, and the screen with `createComposeRule` against fixed states.

## Rules

- Never pass a ViewModel into a stateless composable.
- No `GlobalScope`. No `mutableStateOf` inside a ViewModel for data the repository owns.

## Report

Files added, the state model, and test results.
