---
name: coroutines-patterns
description: Kotlin Coroutines patterns for Android development with StateFlow, SharedFlow, suspend functions, and structured concurrency. Use when implementing async operations, managing streams of data, handling view model lifecycle, or implementing repository patterns with coroutines.
---

# Coroutines Patterns

Best practices cho Kotlin Coroutines trong Android development.

## StateFlow Patterns

### StateFlow trong ViewModel

```kotlin
@HiltViewModel
class FeatureViewModel @Inject constructor(
    private val repository: FeatureRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(FeatureUiState())
    val uiState: StateFlow<FeatureUiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            
            try {
                val data = repository.getData()
                _uiState.update { 
                    it.copy(data = data, isLoading = false) 
                }
            } catch (e: Exception) {
                _uiState.update { 
                    it.copy(error = e.message, isLoading = false) 
                }
            }
        }
    }
}
```

### State Updates

```kotlinn// Atomic update với copy
_uiState.update { currentState ->
    currentState.copy(
        items = newItems,
        isLoading = false
    )
}

// Conditional update
_uiState.update { state ->
    if (state.selectedId == id) {
        state.copy(selectedId = "")
    } else {
        state.copy(selectedId = id)
    }
}
```

## SharedFlow cho Events

### One-time Events

```kotlin
class FeatureViewModel : ViewModel() {

    private val _events = MutableSharedFlow<FeatureEvent>()
    val events = _events.asSharedFlow()

    fun navigateToDetail(id: String) {
        viewModelScope.launch {
            _events.emit(FeatureEvent.NavigateToDetail(id))
        }
    }
}
```

### Event Sealed Class

```kotlinnsealed class FeatureEvent {
    data class ShowMessage(val message: String) : FeatureEvent()
    data class NavigateToDetail(val id: String) : FeatureEvent()
    data object NavigateBack : FeatureEvent()
}
```

## Repository Pattern

### Suspend Functions

```kotlin
interface UserRepository {
    suspend fun getUser(id: String): User
    suspend fun saveUser(user: User)
    suspend fun deleteUser(id: String)
}

class UserRepositoryImpl @Inject constructor(
    private val api: UserApi,
    private val dao: UserDao
) : UserRepository {

    override suspend fun getUser(id: String): User {
        // Try cache first
        val cached = dao.getUser(id)
        if (cached != null) return cached.toDomain()
        
        // Fetch from network
        val remote = api.getUser(id)
        dao.insert(remote.toEntity())
        return remote.toDomain()
    }
}
```

### Flow Streams

```kotlinninterface DataRepository {
    fun getDataStream(): Flow<List<DataItem>>
    fun getItemById(id: String): Flow<DataItem?>
}

class DataRepositoryImpl @Inject constructor(
    private val dao: DataDao
) : DataRepository {

    override fun getDataStream(): Flow<List<DataItem>> {
        return dao.getAll()
            .map { entities -> entities.map { it.toDomain() } }
            .flowOn(Dispatchers.IO)
    }
}
```

## ViewModelScope

### Launch Patterns

```kotlinn// Basic launch
viewModelScope.launch {
    // Coroutine code
}

// With exception handling
viewModelScope.launch {
    try {
        val result = repository.fetchData()
        handleSuccess(result)
    } catch (e: IOException) {
        handleNetworkError(e)
    } catch (e: Exception) {
        handleGenericError(e)
    }
}

// Multiple parallel requests
viewModelScope.launch {
    val deferred1 = async { repository.getUser() }
    val deferred2 = async { repository.getSettings() }
    
    val user = deferred1.await()
    val settings = deferred2.await()
    
    _uiState.update { 
        it.copy(user = user, settings = settings) 
    }
}
```

## Error Handling

### Result Wrapper

```kotlinnsealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}

// Repository
suspend fun <T> safeApiCall(
    apiCall: suspend () -> T
): Result<T> {
    return try {
        Result.Success(apiCall())
    } catch (e: Exception) {
        Result.Error(e)
    }
}

// ViewModel
fun loadData() {
    viewModelScope.launch {
        _uiState.update { it.copy(isLoading = true) }
        
        when (val result = repository.getData()) {
            is Result.Success -> {
                _uiState.update { 
                    it.copy(data = result.data, isLoading = false) 
                }
            }
            is Result.Error -> {
                _uiState.update { 
                    it.copy(error = result.exception.message, isLoading = false) 
                }
            }
            is Result.Loading -> { /* already loading */ }
        }
    }
}
```

### Retry Mechanism

```kotlinnsuspend fun <T> retryWithExponentialBackoff(
    times: Int = 3,
    initialDelay: Long = 100,
    maxDelay: Long = 1000,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(times - 1) {
        try {
            return block()
        } catch (e: Exception) {
            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelay)
        }
    }
    return block() // Last attempt
}
```

## Structured Concurrency

### Supervisor Job

```kotlinn// Khi cần child coroutines chạy độc lập
viewModelScope.launch(SupervisorJob()) {
    launch { fetchUsers() } // Failure không ảnh hưởng
    launch { fetchSettings() } // vẫn chạy nếu fetchUsers fail
}
```

### CoroutineScope Custom

```kotlinnclass FeatureManager @Inject constructor(
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher
) {
    private val scope = CoroutineScope(SupervisorJob() + ioDispatcher)

    fun startWork() {
        scope.launch {
            // Background work
        }
    }

    fun cleanup() {
        scope.cancel()
    }
}
```

## Flow Operators

### Common Patterns

```kotlinn// Debounce search
searchQueryFlow
    .debounce(300)
    .filter { it.isNotBlank() }
    .flatMapLatest { query ->
        repository.search(query)
    }
    .catch { e -> 
        emit(emptyList()) 
    }
    .collect { results ->
        updateResults(results)
    }

// Combine multiple flows
combine(
    userFlow,
    settingsFlow,
    notificationsFlow
) { user, settings, notifications ->
    DashboardData(user, settings, notifications)
}
    .flowOn(Dispatchers.Default)
    .catch { e ->
        handleError(e)
    }
```

## Cancellation

### Cooperative Cancellation

```kotlinnsuspend fun longRunningWork() {
    repeat(100) { i ->
        ensureActive() // Check cancellation
        doWork(i)
        yield() // Cooperative point
    }
}

// Cancellable repository call
suspend fun fetchData(): Data {
    return withContext(Dispatchers.IO) {
        ensureActive()
        api.fetchData()
    }
}
```

## Dispatchers

### Best Practices

```kotlinn// IO operations
viewModelScope.launch(Dispatchers.IO) {
    repository.saveToDatabase(data)
}

// Computation
viewModelScope.launch(Dispatchers.Default) {
    processLargeDataset(data)
}

// Main thread (UI updates)
viewModelScope.launch(Dispatchers.Main) {
    _uiState.update { it.copy(isLoading = false) }
}

// Inject dispatchers (testability)
class Repository @Inject constructor(
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher
) {
    suspend fun save(data: Data) = withContext(ioDispatcher) {
        dao.insert(data)
    }
}
```

## Testing Coroutines

### Test Dispatchers

```kotlinn@ExperimentalCoroutinesApi
class ViewModelTest {
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    @Test
    fun `load data updates state`() = runTest {
        val viewModel = FeatureViewModel(repository)
        
        viewModel.loadData()
        
        assertEquals(
            FeatureUiState(data = testData, isLoading = false),
            viewModel.uiState.value
        )
    }
}
```

## Common Patterns

### Throttle vs Debounce

```kotlinn// Debounce - wait for pause
searchFlow
    .debounce(300)
    .collect { query -> search(query) }

// Sample - take latest every interval
locationFlow
    .sample(1000)
    .collect { location -> updateMap(location) }

// Throttle - limit rate
dataFlow
    .buffer(Channel.CONFLATED)
    .collect { data -> process(data) }
```

## References

- [references/coroutines-testing.md](references/coroutines-testing.md) - Testing patterns
- [references/flow-operators.md](references/flow-operators.md) - Flow transformation patterns
