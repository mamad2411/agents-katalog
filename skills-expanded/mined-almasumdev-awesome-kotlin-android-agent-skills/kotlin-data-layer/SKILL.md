---
name: kotlin-data-layer
description: Expert guidance on building a Kotlin offline-first data layer with Room, Retrofit, Flow-based observables, and the repository pattern. Use this for repositories, caching, and synchronization.
---

# Kotlin Data Layer (Room + Retrofit + Flow, Offline-First)

## Instructions

The data layer's job is to be the **single source of truth** for the app. The UI observes the database; network responses only write to the database.

### 1. Module Shape

```
:feature:articles:data
├── api/        Retrofit services, DTOs, interceptors
├── db/         Room entities, DAOs, TypeConverters
├── mapper/     DTO ↔ Entity ↔ Domain mappers
└── repository/ ArticleRepositoryImpl (implements :domain interface)
```

### 2. Room Entity + DAO

```kotlin
@Entity(tableName = "articles")
data class ArticleEntity(
    @PrimaryKey val id: String,
    val title: String,
    val body: String,
    val publishedAt: Long,
    val isBookmarked: Boolean = false,
)

@Dao
interface ArticleDao {
    @Query("SELECT * FROM articles ORDER BY publishedAt DESC")
    fun observeAll(): Flow<List<ArticleEntity>>

    @Query("SELECT * FROM articles WHERE id = :id")
    fun observeById(id: String): Flow<ArticleEntity?>

    @Upsert
    suspend fun upsertAll(items: List<ArticleEntity>)

    @Query("DELETE FROM articles WHERE id NOT IN (:keepIds)")
    suspend fun deleteStale(keepIds: List<String>)

    @Transaction
    suspend fun replaceAll(items: List<ArticleEntity>) {
        upsertAll(items)
        deleteStale(items.map { it.id })
    }
}
```

### 3. Retrofit Service + DTO

```kotlin
@Serializable
data class ArticleDto(
    val id: String,
    val title: String,
    val body: String,
    @SerialName("published_at") val publishedAt: String,
)

interface ArticleApi {
    @GET("articles")
    suspend fun getArticles(@Query("page") page: Int = 1): List<ArticleDto>
}
```

### 4. Mappers (Extension Functions)

```kotlin
fun ArticleDto.toEntity() = ArticleEntity(
    id = id,
    title = title,
    body = body,
    publishedAt = Instant.parse(publishedAt).toEpochMilliseconds(),
)

fun ArticleEntity.toDomain() = Article(
    id = id,
    title = title,
    body = body,
    publishedAt = Instant.fromEpochMilliseconds(publishedAt),
    isBookmarked = isBookmarked,
)
```

### 5. Offline-First Repository

```kotlin
class ArticleRepositoryImpl @Inject constructor(
    private val api: ArticleApi,
    private val dao: ArticleDao,
    @IoDispatcher private val io: CoroutineDispatcher,
) : ArticleRepository {

    override fun observeArticles(): Flow<List<Article>> =
        dao.observeAll().map { list -> list.map(ArticleEntity::toDomain) }

    override suspend fun refresh(): Result<Unit> = withContext(io) {
        runCatching {
            val fresh = api.getArticles().map(ArticleDto::toEntity)
            dao.replaceAll(fresh)
        }
    }

    override suspend fun toggleBookmark(id: String) = withContext(io) {
        dao.updateBookmark(id, toggle = true)
    }
}
```

Key property: UI subscribes once to `observeArticles()` and reacts to any write — from a pull-to-refresh, a bookmark toggle, or a `WorkManager` sync.

### 6. Error Mapping

Never leak `IOException` or `HttpException` to the domain. Map at the repository boundary:

```kotlin
sealed interface DataError {
    data object Offline : DataError
    data class Server(val code: Int) : DataError
    data class Unknown(val cause: Throwable) : DataError
}

private fun Throwable.toDataError(): DataError = when (this) {
    is UnknownHostException, is SocketTimeoutException -> DataError.Offline
    is HttpException -> DataError.Server(code())
    else -> DataError.Unknown(this)
}
```

### 7. Background Sync with WorkManager

```kotlin
@HiltWorker
class SyncArticlesWorker @AssistedInject constructor(
    @Assisted ctx: Context,
    @Assisted params: WorkerParameters,
    private val repo: ArticleRepository,
) : CoroutineWorker(ctx, params) {
    override suspend fun doWork(): Result =
        repo.refresh().fold(onSuccess = { Result.success() }, onFailure = { Result.retry() })
}
```

Schedule with `PeriodicWorkRequestBuilder<SyncArticlesWorker>(6.hours.toJavaDuration())` and `NetworkType.CONNECTED` constraint.

### 8. DataStore for Preferences

```kotlin
val Context.userPrefs by preferencesDataStore(name = "user_prefs")
object PrefKeys { val DARK = booleanPreferencesKey("dark_mode") }

class SettingsRepository @Inject constructor(@ApplicationContext ctx: Context) {
    private val store = ctx.userPrefs
    val darkMode: Flow<Boolean> = store.data.map { it[PrefKeys.DARK] ?: false }
    suspend fun setDarkMode(enabled: Boolean) { store.edit { it[PrefKeys.DARK] = enabled } }
}
```

## Checklist
- [ ] UI observes Room via `Flow`, never calls Retrofit directly.
- [ ] Writes go Network → Room → UI (one-way).
- [ ] DAOs expose `Flow<T>` for reads and `suspend` for writes.
- [ ] Every multi-step write is `@Transaction`.
- [ ] Errors are mapped to a sealed `DataError` at the repository boundary.
- [ ] Periodic refresh is implemented as a Hilt-aware `CoroutineWorker`.
- [ ] No `SharedPreferences` in new code — use `DataStore`.
