---
name: android-compose-patterns
category: architecture
description: Use when building native Android with Jetpack Compose - stateless composables, state hoisting, ViewModel-owned state, edge-to-edge, predictive back, adaptive layout, atomic components, and Material theming over hardcoded values
tech_stack: Kotlin
source: android/skills (Apache-2.0), skydoves/android-testing-skills (Apache-2.0), adapted
---
# Jetpack Compose Patterns

## Overview

Native Android (Jetpack Compose) is chosen when a task needs deep Android integration or the app is already native (see native-vs-flutter-decision). Same discipline as Flutter/SwiftUI: small stateless composables, state hoisted out, reusable atomic components.

**Core principle:** Composables are stateless functions of state. State is hoisted to a `ViewModel`; composables emit events upward.

## Rules

- **Stateless composables + state hoisting.** A composable takes its state as parameters and exposes callbacks (`onXxx`) — it does not own app state. The screen-level composable connects a `ViewModel` to the stateless UI.
- **`ViewModel` owns state and logic**, exposed as `StateFlow`/`UiState`; the composable collects it with `collectAsStateWithLifecycle()`. Networking/business rules live in the ViewModel + repository, never in the composable.
- **Model UI state as a sealed hierarchy:** `Loading | Data | Empty | Error` — `when` over it renders every branch. No happy-path-only screens.
- **Atomic components:** shared library of reusable composables (atoms → molecules → organisms). Reuse before building; grep before adding.
- **Material theme, not hardcoded values:** `MaterialTheme.colorScheme` / `typography` / a spacing tokens object (`MaterialTheme.spacing`, see `mobile-design-system-foundation`) — never scattered `Color(0xFF...)` and magic `dp`. Support dark theme + dynamic color.
- **`remember`/`derivedStateOf`** to avoid recomputation; **hoist** `remember`ed state only when it's genuinely local (scroll, text field).
- **`@Preview`** reusable composables in their key states, and across the matrix (see below).

## Edge-to-edge (enforced from targetSdk 35)

- Call `enableEdgeToEdge()` before `setContent` in the activity — the opt-out is gone at targetSdk 35+.
- Consume insets at the `Scaffold`: use its `innerPadding` and `Modifier.consumeWindowInsets(innerPadding)` on the content so a nested scrollable doesn't double-apply it.
- IME padding: apply `Modifier.imePadding()` once, at the container that should move with the keyboard — applying it a second time further down the tree produces extra empty space.
- `android:windowSoftInputMode="adjustResize"` in the manifest for screens with text input.
- `NavigationSuiteScaffold` does **not** automatically propagate its padding to the content slot — apply insets explicitly inside it, don't assume it's handled.

## Predictive back (default at targetSdk 36)

- `onBackPressed()` / `OnBackPressedCallback` without `isEnabled` toggling is not called the same way once predictive back is the default — use `BackHandler` (simple) or `PredictiveBackHandler` (custom transition) in Compose, or Navigation 3's built-in handling.
- Verify back navigation in this run rather than assuming the old override still fires.

## Adaptive layout

- `currentWindowAdaptiveInfo().windowSizeClass` to branch layout by available width/height — never by `Configuration.orientation` or a hardcoded device check.
- `NavigationSuiteScaffold` switches a bottom nav bar to a nav rail automatically at the window-size-class breakpoint — prefer it over hand-rolling the switch.
- `GridCells.Adaptive(minWidth)` for grids that should reflow by available width.
- Android 16 (opt-out via `PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY`) and Android 17/API 37 (no opt-out) ignore `screenOrientation`/`resizeableActivity` restrictions on screens ≥600dp — design every screen to work in both orientations and at tablet width; don't rely on an orientation lock to avoid building the wider layout.

## Previews and tests across the matrix

- `@PreviewScreenSizes`, `@PreviewFontScale`, `@PreviewLightDark`, or a custom multi-preview with `Devices.PHONE`/`Devices.TABLET` — see `mobile-visual-self-review` for the full size/text-scale/dark matrix.
- `DeviceConfigurationOverride(ForcedSize(...) then FontScale(...) then DarkMode(...))` for instrumented matrix tests.
- `rule.enableAccessibilityChecks()` on an API 34+ device/emulator before UI-mutating test actions (inconclusive on Robolectric — say so if that's all you ran); see `mobile-accessibility`.
- "Run screenshot tests but do not update reference images" to "fix" a failure — a changed golden is a visual regression until a human confirms it's intended.

## Semantics

- `contentDescription` on every `Image`/`Icon` that carries meaning; `null` explicitly for a purely decorative one.
- `Modifier.semantics(mergeDescendants = true)` on a composite row so a screen reader announces it once.
- Touch targets ≥48dp — `Modifier.size`/`minimumInteractiveComponentSize()`.

## Worked Example

```kotlin
// ViewModel owns state + logic (unit-testable, no Compose)
class TaskListViewModel(private val repo: TaskRepository) : ViewModel() {
    private val _state = MutableStateFlow<UiState<List<Task>>>(UiState.Loading)
    val state: StateFlow<UiState<List<Task>>> = _state
    fun load() = viewModelScope.launch {
        _state.value = UiState.Loading
        _state.value = try {
            val items = repo.list()
            if (items.isEmpty()) UiState.Empty else UiState.Data(items)
        } catch (e: CancellationException) {
            throw e                              // never swallow cancellation
        } catch (e: Exception) {
            UiState.Error(e)
        }
    }
}

// stateless composable renders state, emits events
@Composable
fun TaskListScreen(state: UiState<List<Task>>, onRetry: () -> Unit) = when (state) {
    is UiState.Loading -> AppSpinner()
    is UiState.Error   -> AppErrorView(message = state.cause.message, onRetry = onRetry)
    is UiState.Data    -> TaskList(tasks = state.value)
    is UiState.Empty   -> EmptyView()
}
```

The fix from the previous version: `runCatching { }` wrapped around a suspend call inside `viewModelScope.launch` catches `CancellationException` along with real errors, which breaks structured concurrency (a cancelled screen keeps "loading" instead of stopping) — use `try/catch` and rethrow `CancellationException` explicitly. The `Empty` branch is now actually emitted when the list comes back empty, not just declared and never reached.

## Testing

- Unit-test the `ViewModel` with a fake/mockk repository and a test dispatcher — no Compose.
- Compose UI tests (`createComposeRule`) assert visible behavior and clicks. Test-first.

## Common Mistakes

- A composable holding app state or calling the repository.
- Business logic in the composable instead of the ViewModel.
- Hardcoded colors/dp instead of `MaterialTheme` + tokens.
- Collecting flows without `collectAsStateWithLifecycle` (leaks/waste).
- Only the data branch rendered — `Empty` declared but never emitted.
- `runCatching` around a suspend call, swallowing `CancellationException`.
- Assuming edge-to-edge/predictive back still behave like targetSdk <35/<36 after a target bump.

## Red Flags

- A `@Composable` that imports a repository or Retrofit service.
- `Color(0xFF...)`/magic `dp` outside the theme.
- No error/empty branch in the `when`.
- `enableEdgeToEdge()` missing from a new or recently targetSdk-bumped activity.
- A screen that only renders correctly in one orientation.
