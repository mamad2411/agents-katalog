---
name: android-coroutines-flow
description: |
  Coroutines and Flow patterns for Android/KMP - dispatcher ownership, StateFlow vs SharedFlow, combine/mapLatest/debounce, cancellation, sharing, and collection in ViewModels and Compose. Use this skill whenever writing async code, exposing streams from repositories, transforming Flow, coordinating parallel work, or reviewing coroutine scope usage. Trigger on phrases like "Flow", "StateFlow", "SharedFlow", "coroutines", "dispatcher", "launch", "async", "combine", "mapLatest", "debounce", "retryWhen", or "collectLatest".
---

# Android / KMP Coroutines and Flow

## Core Principles

- Prefer `suspend` for one-shot work and `Flow` for streams over time.
- `ViewModel` owns UI-facing coroutine scopes.
- Repositories expose `Flow` only when data can change over time; otherwise return `suspend` functions.
- Cancellation is expected behavior, not an error.
- Never block the main thread with disk, network, or heavy CPU work.

---

## Choosing the Right API

| Need | Preferred API |
|---|---|
| Single request/response | `suspend fun` |
| Ongoing database observation | `Flow<T>` |
| UI state stream | `StateFlow<T>` |
| One-time events | `Channel` + `receiveAsFlow()` |
| Fire-and-forget parallel child work | `coroutineScope { async { ... } }` |

Do not use `LiveData` in new code.

---

## Dispatcher Ownership

The class doing the blocking work is responsible for moving to the correct dispatcher.

```kotlin
class ImageCompressor(
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend fun compress(bytes: ByteArray): ByteArray = withContext(ioDispatcher) {
        // blocking compression
        bytes
    }
}
```

`ViewModel`s that only use `viewModelScope` should not inject dispatchers. See the **android-testing** skill for test setup with `Dispatchers.setMain(...)`.

---

## Repository Contracts

Use `Flow` only when the caller should keep receiving updates:

```kotlin
interface NoteRepository {
    fun observeNotes(): Flow<List<Note>>
    suspend fun refreshNotes(): EmptyResult<DataError>
    suspend fun getNote(id: String): Result<Note, DataError>
}
```

Bad patterns:
- returning `Flow` for a one-time network request
- launching internal background jobs that the caller cannot control
- collecting a `Flow` inside the repository just to emit into another `Flow`

---

## StateFlow in ViewModels

Expose immutable state only:

```kotlin
private val _state = MutableStateFlow(NoteListState())
val state = _state.asStateFlow()
```

Use `.update { }` for all mutations:

```kotlin
_state.update { it.copy(isLoading = true) }
```

For UI state derived from multiple sources, prefer `combine`:

```kotlin
val state: StateFlow<NoteListState> = combine(
    observeNotes(),
    observeFilter()
) { notes, filter ->
    NoteListState(notes = notes.filter { it.matches(filter) })
}.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5_000),
    initialValue = NoteListState()
)
```

---

## SharedFlow vs Channel

- Use `StateFlow` for persistent UI state.
- Use `Channel` + `receiveAsFlow()` for one-time events such as navigation or snackbars.
- Use `MutableSharedFlow` only when multiple collectors need the same transient stream and replay behavior is intentional.

```kotlin
private val _events = Channel<NoteListEvent>()
val events = _events.receiveAsFlow()
```

Avoid using `StateFlow` for navigation events; it can replay stale events after configuration changes.

---

## Flow Operators That Usually Matter

### `mapLatest`

Cancel previous work when newer input arrives:

```kotlin
searchQuery
    .debounce(300)
    .distinctUntilChanged()
    .mapLatest { query -> repository.search(query) }
```

### `combine`

Join multiple reactive sources into one UI model:

```kotlin
combine(userFlow, settingsFlow) { user, settings ->
    ProfileState(user = user, darkMode = settings.darkMode)
}
```

### `flatMapLatest`

Switch to a new stream when the upstream key changes:

```kotlin
selectedNoteId.flatMapLatest { id -> repository.observeNote(id) }
```

### `catch`

Only recover from upstream exceptions you truly own. Do not swallow `CancellationException`.

```kotlin
flow {
    emit(api.load())
}.catch { throwable ->
    if (throwable is CancellationException) throw throwable
    emit(emptyList())
}
```

---

## Collecting in the ViewModel

Collect long-lived streams in `viewModelScope`:

```kotlin
init {
    repository.observeNotes()
        .onEach { notes ->
            _state.update { it.copy(notes = notes.map { note -> note.toNoteUi() }) }
        }
        .launchIn(viewModelScope)
}
```

Prefer `launchIn(viewModelScope)` for passive observation pipelines and `viewModelScope.launch { flow.collect { ... } }` when you need imperative branching.

---

## Compose Collection

Always collect state in composables with lifecycle awareness:

```kotlin
val state by viewModel.state.collectAsStateWithLifecycle()
```

Do not collect arbitrary flows in deeply nested composables. Keep collection in Root composables and pass plain state down. See the **android-presentation-mvi** skill.

---

## Parallel Work

Use structured concurrency so child work is cancelled with the parent:

```kotlin
suspend fun loadDashboard(): DashboardData = coroutineScope {
    val profile = async { userRepository.getProfile() }
    val stats = async { statsRepository.getStats() }
    DashboardData(
        profile = profile.await(),
        stats = stats.await()
    )
}
```

Use `supervisorScope` only when one child failure should not cancel sibling work.

---

## Retry and Backoff

Prefer explicit retries at boundaries like sync or network refresh:

```kotlin
repository.observeSyncRequests()
    .retryWhen { cause, attempt ->
        cause is IOException && attempt < 3
    }
```

Do not add hidden infinite retries to generic repository functions.

---

## Checklist: Adding Coroutine / Flow Logic

- [ ] Use `suspend` for one-shot work and `Flow` for ongoing streams
- [ ] Move blocking work to the owning dispatcher with `withContext(...)`
- [ ] Expose immutable `StateFlow` from the `ViewModel`
- [ ] Use `Channel` for one-time events
- [ ] Collect UI state with `collectAsStateWithLifecycle()`
- [ ] Never swallow `CancellationException`