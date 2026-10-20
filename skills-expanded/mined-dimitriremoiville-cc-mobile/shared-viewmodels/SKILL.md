---
name: shared-viewmodels
description: How shared ViewModels are written in this KMM project — extending `androidx.lifecycle.ViewModel` (multiplatform), exposing `StateFlow<UiState>` + `Channel<UiEvent>`, handling actions, and being consumed from Jetpack Compose and SwiftUI. Load whenever writing or reviewing a shared ViewModel.
---

# Shared ViewModels

## The contract

A shared ViewModel exposes three things:
- `state: StateFlow<UiState>` — the current UI state (always has a value).
- `events: Flow<UiEvent>` — one-off effects (navigation, snackbars, toasts) via a `Channel`.
- `onAction(action: UiAction)` — the single entry point for UI interactions.

That's it. Everything else is private.

## Canonical shape

```kotlin
class OrderViewModel(
    private val getOrder: GetOrderUseCase,
    private val submit: SubmitOrderUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow<OrderUiState>(OrderUiState.Loading)
    val state: StateFlow<OrderUiState> = _state.asStateFlow()

    private val _events = Channel<OrderUiEvent>(Channel.BUFFERED)
    val events: Flow<OrderUiEvent> = _events.receiveAsFlow()

    fun onAction(action: OrderAction) {
        when (action) {
            is OrderAction.Load -> load(action.id)
            OrderAction.Retry -> load(currentId)
            is OrderAction.Submit -> submit(action.draft)
        }
    }

    private fun load(id: OrderId) {
        viewModelScope.launch {
            _state.value = OrderUiState.Loading
            getOrder(id).fold(
                onSuccess = { _state.value = OrderUiState.Success(it) },
                onFailure = { error ->
                    _state.value = OrderUiState.Error(error.message.orEmpty())
                    _events.send(OrderUiEvent.ShowToast("Couldn't load order"))
                }
            )
        }
    }
}
```

Rules:
- `private val _state`, `public val state`. Same for events.
- No `setX` / `getX` — outside code drives change via `onAction`.
- `viewModelScope` is provided by `androidx.lifecycle:lifecycle-viewmodel` on both platforms.
- Actions are sealed — `when` without `else` gets exhaustiveness for free.

## UiState, UiEvent, UiAction

```kotlin
sealed interface OrderUiState {
    data object Loading : OrderUiState
    data class Success(val order: Order) : OrderUiState
    data class Error(val message: String) : OrderUiState
}

sealed interface OrderUiEvent {
    data class ShowToast(val message: String) : OrderUiEvent
    data class NavigateToCheckout(val id: OrderId) : OrderUiEvent
}

sealed interface OrderAction {
    data class Load(val id: OrderId) : OrderAction
    data class Submit(val draft: OrderDraft) : OrderAction
    data object Retry : OrderAction
}
```

## Consuming from Jetpack Compose (Android)

```kotlin
@Composable
fun OrderRoute(
    id: OrderId,
    onCheckout: (OrderId) -> Unit,
    viewModel: OrderViewModel = koinViewModel { parametersOf(id) },
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is OrderUiEvent.NavigateToCheckout -> onCheckout(event.id)
                is OrderUiEvent.ShowToast -> { /* show snackbar */ }
            }
        }
    }
    OrderScreen(
        state = state,
        onAction = viewModel::onAction,
    )
}
```

## Consuming from SwiftUI (iOS)

The shared ViewModel is wrapped by a small Swift `@Observable` class that translates state and forwards actions. See the `kmm-ios-interop` skill for the full pattern — a sketch:

```swift
@Observable @MainActor
final class OrderViewModelObservable {
    private(set) var state: OrderUiState = .loading
    private let shared: OrderViewModel
    private var stateTask: Task<Void, Never>?

    init(shared: OrderViewModel) {
        self.shared = shared
        self.stateTask = Task { [weak self] in
            for await value in shared.state.asAsyncSequence() {
                self?.state = value
            }
        }
    }

    deinit { stateTask?.cancel() }

    func onAction(_ action: OrderAction) { shared.onAction(action: action) }
}
```

`asAsyncSequence()` is a small helper in `iosMain` or a Swift extension that bridges `StateFlow` → `AsyncSequence` via `collect`.

## Initial state, not `null`

`StateFlow` always has a value. Don't use `MutableStateFlow<UiState?>(null)` — pick a sensible initial state (`Loading` is usually right).

## Errors

Use `DomainError` values, not thrown exceptions, to shape UI state. Map platform errors at the repository; by the time they reach the VM, they're domain types.

## Testing

Test the ViewModel like any other class. `runTest { }` + injected `TestDispatcher` + Turbine-less assertions on `state.value` after `advanceUntilIdle()`.

```kotlin
@Test
fun loadTransitionsFromLoadingToSuccess() = runTest(dispatcher) {
    val vm = OrderViewModel(FakeGetOrderUseCase(Result.success(ORDER)))
    vm.onAction(OrderAction.Load(OrderId("42")))
    advanceUntilIdle()
    assertIs<OrderUiState.Success>(vm.state.value)
}
```

## Hard nos

- No Android imports in `presentation/` inside `commonMain` (other than `androidx.lifecycle:lifecycle-viewmodel`'s multiplatform API).
- No `LiveData`.
- No business logic in the ViewModel — delegate to use cases.
- No direct repository calls from a ViewModel when a use case would carry real logic.
- No `@Serializable` on UiState; UiState is internal to the app, not wire format.
