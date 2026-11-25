---
name: compose-state-management
description: Expert guidance on managing state in Jetpack Compose using ViewModel, StateFlow, remember/rememberSaveable, state hoisting, and unidirectional data flow. Use this when implementing screens or refactoring stateful composables.
---

# Compose State Management (ViewModel + StateFlow + UDF)

## Instructions

Follow **Unidirectional Data Flow (UDF)**: state flows down from a single source of truth (`ViewModel`), events flow up.

### 1. UiState as a Single Immutable Class

```kotlin
@Immutable
data class ArticlesUiState(
    val isLoading: Boolean = false,
    val articles: ImmutableList<Article> = persistentListOf(),
    val error: String? = null,
)
```

Use `kotlinx.collections.immutable` (`ImmutableList`, `PersistentList`) so Compose treats list fields as stable and skips unnecessary recompositions.

### 2. ViewModel Exposes StateFlow

```kotlin
@HiltViewModel
class ArticlesViewModel @Inject constructor(
    private val getArticles: GetArticlesUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow(ArticlesUiState(isLoading = true))
    val state: StateFlow<ArticlesUiState> = _state.asStateFlow()

    private val _events = Channel<ArticlesEvent>(Channel.BUFFERED)
    val events = _events.receiveAsFlow()

    init { load() }

    fun onAction(action: ArticlesAction) = when (action) {
        ArticlesAction.Refresh -> load()
        is ArticlesAction.Open  -> viewModelScope.launch { _events.send(ArticlesEvent.Navigate(action.id)) }
    }

    private fun load() = viewModelScope.launch {
        _state.update { it.copy(isLoading = true, error = null) }
        runCatching { getArticles() }
            .onSuccess { list -> _state.update { it.copy(isLoading = false, articles = list.toPersistentList()) } }
            .onFailure { e -> _state.update { it.copy(isLoading = false, error = e.message) } }
    }
}

sealed interface ArticlesAction {
    data object Refresh : ArticlesAction
    data class Open(val id: String) : ArticlesAction
}

sealed interface ArticlesEvent {
    data class Navigate(val id: String) : ArticlesEvent
}
```

### 3. Collecting in Composables (Lifecycle-Aware)

```kotlin
@Composable
fun ArticlesRoute(vm: ArticlesViewModel = hiltViewModel(), onOpen: (String) -> Unit) {
    val state by vm.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        vm.events.collect { e ->
            when (e) { is ArticlesEvent.Navigate -> onOpen(e.id) }
        }
    }

    ArticlesScreen(state = state, onAction = vm::onAction)
}
```

Always use `collectAsStateWithLifecycle()` (from `lifecycle-runtime-compose`) — never raw `collectAsState()` for `Flow`s that stay hot, to avoid work while the UI is stopped.

### 4. State Hoisting

Composables render state and raise events. They should not own business state.

```kotlin
@Composable
fun ArticlesScreen(state: ArticlesUiState, onAction: (ArticlesAction) -> Unit) {
    when {
        state.isLoading -> LoadingIndicator()
        state.error != null -> ErrorView(state.error, onRetry = { onAction(ArticlesAction.Refresh) })
        else -> ArticleList(state.articles, onClick = { onAction(ArticlesAction.Open(it.id)) })
    }
}
```

### 5. `remember` vs `rememberSaveable`

- `remember { mutableStateOf(...) }` — ephemeral UI state lost across config changes. Use for scroll position on a short-lived screen, hover state, etc.
- `rememberSaveable { mutableStateOf(...) }` — survives config change and process death. Use for search text fields, dialog open/closed flags.
- For complex saved state use a custom `Saver`:

```kotlin
val FilterSaver = Saver<Filter, List<String>>(
    save = { listOf(it.query, it.category) },
    restore = { Filter(query = it[0], category = it[1]) },
)
val filter = rememberSaveable(saver = FilterSaver) { Filter("", "all") }
```

### 6. Derived and Produced State

```kotlin
val canSubmit by remember(state.articles) {
    derivedStateOf { state.articles.isNotEmpty() && !state.isLoading }
}

val temperature by produceState(initialValue = 0f, key1 = sensorId) {
    sensorFlow(sensorId).collect { value = it }
}
```

`derivedStateOf` prevents recomposition when the derived value is unchanged even though inputs changed.

### 7. Anti-Patterns
- Do not hold `Context`, `View`, or `NavController` in `ViewModel`.
- Do not mutate `MutableStateFlow.value` from the UI thread directly from a composable body; route through `onAction`.
- Do not expose `MutableStateFlow` publicly — always `.asStateFlow()`.
- Do not use `LiveData` in new Compose code (see `livedata-to-flow` skill for migration).

## Checklist
- [ ] ViewModel exposes a single immutable `UiState` via `StateFlow`.
- [ ] UI collects with `collectAsStateWithLifecycle()`.
- [ ] One-shot events use `Channel`/`SharedFlow`, not `StateFlow`.
- [ ] No `Context` or Android framework types stored in ViewModel fields.
- [ ] `rememberSaveable` is used for any state that must survive config change.
- [ ] List fields use `ImmutableList` / `persistentListOf()` for stability.
