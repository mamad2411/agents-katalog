---
name: compose-ui
description: Project-specific Compose conventions — the Route/Screen split, `UiState` / `UiEvent` shape, Figma-MCP-to-`MaterialTheme` translation, and the hard-nos this project enforces. Load whenever writing or editing any `@Composable` in this codebase. Navigation destinations and route plumbing live in `navigation-compose` — load that one for any nav-graph or typed-route work.
---

# Compose UI (project delta)

For Compose fundamentals — state hoisting, `Modifier` ordering, `LazyColumn` keys, `@Preview`, recomposition hygiene, `derivedStateOf`, stability — read the [official Compose state guide](https://developer.android.com/develop/ui/compose/state) and Google's published [`android/skills/jetpack-compose/*`](https://github.com/android/skills/tree/main/jetpack-compose) skills (adaptive layouts, theming, View-to-Compose migration). This file documents only where this project's conventions add to or override those defaults.

## When this applies

Jetpack Compose only. On an existing app:

- **View-based UI** (`res/layout/*.xml`, `findViewById`, `binding.`, `Fragment` setup) → don't push Compose patterns. The Route/Screen split, `collectAsStateWithLifecycle`, `Modifier`-first conventions are Compose-only.
- **Mixed Compose + View** (`ComposeView` inside an XML layout, or Compose host fragments) → apply this skill to the `@Composable` parts only; let the View parts follow their own conventions.

## Pulling design specs from Figma

The plugin declares Figma's official MCP server (`.mcp.json` → `figma`, `https://mcp.figma.com/mcp`, OAuth — no API key in the plugin). If the user supplies a Figma URL when asking for a screen or component, pull layout / typography / color / spacing details from the file before generating Compose code. First call triggers a browser OAuth prompt; nothing to configure beyond that.

Map Figma tokens onto `MaterialTheme.colorScheme` / `typography` / `shapes`. Don't paste raw hex/px values into composables — translate to the theme.

## Route + Screen split (project rule)

Every screen is **two functions**: a stateful **Route** that owns the ViewModel, and a stateless **Screen** that renders state and surfaces callbacks. The Route is the only place `hiltViewModel()` is called; everything below the Screen receives state + lambdas as parameters.

```kotlin
@Composable
fun OrderRoute(
    onBack: () -> Unit,
    onCheckout: (OrderId) -> Unit,
    viewModel: OrderViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) { is OrderEvent.Checkout -> onCheckout(event.id) }
        }
    }
    OrderScreen(state = state, onBack = onBack, onAction = viewModel::onAction)
}

@Composable
fun OrderScreen(
    state: OrderUiState,
    onBack: () -> Unit,
    onAction: (OrderAction) -> Unit,
    modifier: Modifier = Modifier,
) { /* pure UI — no Hilt, no ViewModel reference */ }
```

The Screen is what `@Preview` and Compose UI tests drive — no Hilt setup required. The Route's job is wiring; the Screen's job is rendering.

## UiState and UiEvent shape

State is always a **sealed type** with explicit `Loading` / `Error` / `Success` branches by default:

```kotlin
sealed interface OrderUiState {
    data object Loading : OrderUiState
    data class Error(val message: String) : OrderUiState
    data class Success(val order: Order) : OrderUiState
}
```

One-off effects (navigation, snackbars, toasts) are **not** state — they're events emitted through a `Channel<UiEvent>` and collected once in the Route:

```kotlin
sealed interface OrderEvent {
    data class Checkout(val id: OrderId) : OrderEvent
    data class ShowError(val message: String) : OrderEvent
}
```

`StateFlow` for state, `Channel` for events. `SharedFlow` only when you actually need replay.

## Theming

- Colors come from `MaterialTheme.colorScheme.*`. **No hex literals in `@Composable` code** — they live in the theme files only.
- Typography tokens are defined in `Type.kt` and consumed as `MaterialTheme.typography.bodyLarge` etc.
- Shapes as `MaterialTheme.shapes.medium` etc.

When extracting from Figma, define the token in the theme, then reference it from composables.

## Accessibility

The full accessibility checklist lives in the `android-accessibility` skill. The minimum the reviewer flags here:

- Every `Icon` without adjacent text gets a `contentDescription` (or `null`, explicit).
- Interactive elements ≥ 48dp tap target.

## Hard nos

- **No `LiveData`** in new code — use `StateFlow`.
- **No `collectAsState()`** for ViewModel state — `collectAsStateWithLifecycle()` only.
- **No `hiltViewModel()` outside the Route.** Never inside a child composable, never passed down as a parameter.
- **No network or DB calls inside a `@Composable`** or any `LaunchedEffect` that reaches around the ViewModel.
- **No hex literals in composables.** Always go through `MaterialTheme.*` (see Theming).
- **No `@Composable` longer than ~60-80 lines.** Extract children when concerns mix (layout + stateful behaviour + event handling) or nesting exceeds 3 levels. Lines alone aren't the rule; readability is.
