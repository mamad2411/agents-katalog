---
name: android-kmp-viewmodel
description: |
  Sharing ViewModel logic across Android and iOS in KMP — CommonViewModel base, StateFlow in shared code, platform wrappers for iOS consumption. Use when building shared presentation logic, moving ViewModel to commonMain, or exposing Flow to Swift. Trigger on: "shared ViewModel", "KMP ViewModel", "commonMain ViewModel", "StateFlow iOS", "KMP presentation".
---

# KMP ViewModel

## Strategy

Keep `ViewModel` class on Android (it owns `viewModelScope`). Move all **state logic** to a platform-agnostic `Presenter` or `CommonViewModel` in `commonMain` that takes an explicit `CoroutineScope`.

## CommonViewModel (`commonMain`)

```kotlin
// commonMain — core:domain or feature module
abstract class CommonViewModel {
    private val viewModelScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    protected fun launch(block: suspend CoroutineScope.() -> Unit): Job =
        viewModelScope.launch(block = block)

    open fun onCleared() {
        viewModelScope.cancel()
    }
}
```

## Android ViewModel wraps it

```kotlin
// androidMain
class TaskListViewModel(
    private val getTasks: GetTasksUseCase,
) : ViewModel() {

    private val _state = MutableStateFlow(TaskListState())
    val state: StateFlow<TaskListState> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            getTasks().collect { tasks ->
                _state.update { it.copy(tasks = tasks) }
            }
        }
    }
}
```

## iOS Swift wrapper (StateFlow → Combine)

```kotlin
// iosMain — thin wrapper so Swift can observe
class TaskListIosViewModel(
    private val getTasks: GetTasksUseCase,
) : CommonViewModel() {

    private val _state = MutableStateFlow(TaskListState())
    val state: StateFlow<TaskListState> = _state.asStateFlow()

    init {
        launch {
            getTasks().collect { tasks ->
                _state.update { it.copy(tasks = tasks) }
            }
        }
    }
}
```

```swift
// Swift — consume the StateFlow via a helper
let vm = TaskListIosViewModel(getTasks: ...)
let publisher = vm.state.toPublisher() // use KMP-NativeCoroutines or manual wrapper
```

## Recommended library

[KMP-NativeCoroutines](https://github.com/rickclephas/KMP-NativeCoroutines) generates Swift async/await wrappers for `StateFlow` and `Flow` automatically.

```kotlin
// commonMain
import com.rickclephas.kmp.nativecoroutines.NativeCoroutinesState

abstract class CommonViewModel {
    @NativeCoroutinesState
    abstract val state: StateFlow<*>
}
```

## Checklist

- [ ] `CommonViewModel` in `commonMain`, no Android imports
- [ ] Android `ViewModel` delegates to shared logic or shares `StateFlow`
- [ ] iOS wrapper calls `onCleared()` in `deinit`
- [ ] No `LiveData` in shared code — `StateFlow` only
- [ ] Use KMP-NativeCoroutines or equivalent for Swift consumption
