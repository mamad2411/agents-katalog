---
name: kotlin-android-patterns
description: "Kotlin Android patterns: ViewModel with StateFlow and Compose, a Room entity, DAO, and repository, Hilt modules, Compose recomposition fixes, and WorkManager background sync. Use when writing modern Android app code."
---

# Kotlin Android Patterns

## MVVM: ViewModel + StateFlow + Compose

```kotlin
// UiState
data class ProductListUiState(
    val products: List<Product> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
)

// ViewModel
@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val getProductsUseCase: GetProductsUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(ProductListUiState(isLoading = true))
    val uiState: StateFlow<ProductListUiState> = _uiState.asStateFlow()

    init {
        loadProducts()
    }

    private fun loadProducts() {
        viewModelScope.launch {
            getProductsUseCase()
                .catch { e ->
                    _uiState.update { it.copy(isLoading = false, errorMessage = e.message) }
                }
                .collect { products ->
                    _uiState.update {
                        it.copy(products = products, isLoading = false)
                    }
                }
        }
    }

    fun refresh() {
        _uiState.update { it.copy(isLoading = true, errorMessage = null) }
        loadProducts()
    }
}
```

### Compose UI with collectAsStateWithLifecycle
```kotlin
@Composable
fun ProductListScreen(
    viewModel: ProductListViewModel = hiltViewModel()
) {
    // Stops collection when app is backgrounded — battery efficient
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Box(modifier = Modifier.fillMaxSize()) {
        when {
            uiState.isLoading -> CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            uiState.errorMessage != null -> ErrorMessage(
                message = uiState.errorMessage!!,
                onRetry = viewModel::refresh
            )
            else -> ProductList(products = uiState.products)
        }
    }
}
```

---

## Room: Entity, DAO, Repository

```kotlin
// Entity
@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "title") val title: String,
    @ColumnInfo(name = "price") val price: Double,
    @ColumnInfo(name = "last_updated") val lastUpdated: Long = System.currentTimeMillis()
)

// DAO
@Dao
interface ProductDao {
    @Query("SELECT * FROM products ORDER BY title ASC")
    fun observeAll(): Flow<List<ProductEntity>>

    @Query("SELECT * FROM products WHERE id = :id")
    suspend fun getById(id: String): ProductEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(products: List<ProductEntity>)

    @Query("DELETE FROM products")
    suspend fun deleteAll()

    @Transaction
    suspend fun replaceAll(products: List<ProductEntity>) {
        deleteAll()
        insertAll(products)
    }
}

// Repository
class ProductRepository @Inject constructor(
    private val dao: ProductDao,
    private val api: ProductApi,
) {
    fun observeProducts(): Flow<List<Product>> =
        dao.observeAll()
            .map { entities -> entities.map { it.toDomain() } }
            .flowOn(Dispatchers.IO)

    suspend fun refreshProducts() = withContext(Dispatchers.IO) {
        val products = api.fetchProducts()
        dao.replaceAll(products.map { it.toEntity() })
    }
}
```

---

## Hilt: Module Setup

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient =
        OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor())
            .build()

    @Provides
    @Singleton
    fun provideRetrofit(client: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl(BuildConfig.API_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

    @Provides
    @Singleton
    fun provideProductApi(retrofit: Retrofit): ProductApi =
        retrofit.create(ProductApi::class.java)
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindProductRepository(
        impl: ProductRepositoryImpl
    ): ProductRepository
}
```

---

## Compose: Recomposition Optimization

```kotlin
// Bad: entire screen recomposes when any part of state changes
@Composable
fun Screen(viewModel: MyViewModel = hiltViewModel()) {
    val state = viewModel.uiState.collectAsStateWithLifecycle().value
    HeavyComponent(data = state.someField)
    AnotherComponent(count = state.count)
}

// Good: each component subscribes to only what it needs
@Composable
fun Screen(viewModel: MyViewModel = hiltViewModel()) {
    val someField by remember {
        viewModel.uiState.map { it.someField }
    }.collectAsStateWithLifecycle(initialValue = "")

    val count by remember {
        viewModel.uiState.map { it.count }
    }.collectAsStateWithLifecycle(initialValue = 0)

    HeavyComponent(data = someField)
    AnotherComponent(count = count)
}

// derivedStateOf: compute from observed state, recompose only on derived change
@Composable
fun FilteredList(allItems: List<Item>, query: String) {
    val filtered by remember(allItems) {
        derivedStateOf {
            allItems.filter { it.name.contains(query, ignoreCase = true) }
        }
    }
    LazyColumn { items(filtered) { ItemRow(it) } }
}
```

---

## WorkManager: Background Sync

```kotlin
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val repository: ProductRepository
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        return try {
            repository.refreshProducts()
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) Result.retry() else Result.failure()
        }
    }

    @AssistedFactory
    interface Factory : ChildWorkerFactory
}

// Scheduling
fun scheduleDailySync(context: Context) {
    val constraints = Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .setRequiresBatteryNotLow(true)
        .build()

    val request = PeriodicWorkRequestBuilder<SyncWorker>(1, TimeUnit.DAYS)
        .setConstraints(constraints)
        .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 15, TimeUnit.MINUTES)
        .build()

    WorkManager.getInstance(context).enqueueUniquePeriodicWork(
        "daily_sync",
        ExistingPeriodicWorkPolicy.KEEP, // Don't replace if already scheduled
        request
    )
}
```
