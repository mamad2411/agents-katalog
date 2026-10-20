---
name: ktor-multiplatform
description: Networking patterns for this KMM project — Ktor Client in `commonMain`, platform engines (OkHttp on Android, Darwin on iOS), kotlinx.serialization, repository integration, and error mapping. Load whenever writing or editing an API call, engine configuration, or serializer.
---

# Ktor Client (multiplatform)

## The pipeline

```
domain.Repository       # domain types only
      ↓
data.RepositoryImpl     # calls HttpClient, maps DTOs, returns Result<Domain>
      ↓
data.remote.*Api        # small wrapper around HttpClient + endpoints
      ↓
HttpClient (Ktor)       # shared in commonMain, platform engine injected
      ↓
engine: OkHttp (Android) | Darwin (iOS)
```

Errors are mapped to domain errors at the **repository boundary**. Nothing above the data layer sees `io.ktor.client.plugins.*` exceptions.

## HttpClient setup (in `commonMain`)

```kotlin
fun buildHttpClient(
    baseUrl: String,
    engine: HttpClientEngine,
    authTokenProvider: AuthTokenProvider,
): HttpClient = HttpClient(engine) {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
            explicitNulls = false
            coerceInputValues = true
        })
    }
    install(DefaultRequest) {
        url(baseUrl)
        header(HttpHeaders.Accept, "application/json")
    }
    install(HttpTimeout) {
        connectTimeoutMillis = 10_000
        requestTimeoutMillis = 30_000
    }
    install(Auth) {
        bearer {
            loadTokens { authTokenProvider.current()?.let { BearerTokens(it, it) } }
            refreshTokens { authTokenProvider.refresh().let { BearerTokens(it, it) } }
        }
    }
    if (isDebug()) {
        install(Logging) { level = LogLevel.BODY }   // debug only
    }
}
```

- The **engine** (OkHttp / Darwin) is injected — don't reference an engine type in `commonMain`. Provide it via Koin (see below).
- `ContentNegotiation` + `kotlinx.serialization` is the only JSON pathway. No manual `Json.decodeFromString` in repositories.
- `Logging` only in debug. `isDebug()` is an `expect fun` or a build-time flag.

## Per-platform engine (via Koin)

```kotlin
// androidMain
val androidKtorModule = module {
    single<HttpClientEngine> { OkHttp.create() }
}

// iosMain
val iosKtorModule = module {
    single<HttpClientEngine> { Darwin.create() }
}

// commonMain
val networkModule = module {
    single {
        buildHttpClient(
            baseUrl = get<AppConfig>().apiBaseUrl,
            engine = get(),
            authTokenProvider = get(),
        )
    }
}
```

## API wrappers

Keep them thin and focused:

```kotlin
class OrderApi(private val http: HttpClient) {
    suspend fun get(id: String): OrderDto = http.get("orders/$id").body()
    suspend fun list(cursor: String?): PagedDto<OrderDto> =
        http.get("orders") { cursor?.let { parameter("cursor", it) } }.body()
    suspend fun create(body: CreateOrderRequest): OrderDto =
        http.post("orders") {
            contentType(ContentType.Application.Json)
            setBody(body)
        }.body()
}
```

Every endpoint method is `suspend`. Responses are deserialized by `ContentNegotiation`.

## DTOs

```kotlin
@Serializable
data class OrderDto(
    val id: String,
    val items: List<OrderItemDto>,
    @SerialName("total_cents") val totalCents: Long,
    @SerialName("created_at") val createdAt: String,
)
```

Rules:
- DTOs in `commonMain/.../data/remote/`, never leaking upward.
- `@Serializable` + `@SerialName` for snake_case boundary.
- Nullability reflects the wire, not the domain.

## Mappers

```kotlin
fun OrderDto.toDomain(): Order = Order(
    id = OrderId(id),
    items = items.map(OrderItemDto::toDomain),
    total = Money.fromCents(totalCents),
    createdAt = Instant.parse(createdAt),
)
```

One-way. Extension functions on the DTO or free functions; pick one style per project.

## Repository

```kotlin
class OrderRepositoryImpl(
    private val api: OrderApi,
    private val io: CoroutineDispatcher,
) : OrderRepository {
    override suspend fun getOrder(id: OrderId): Result<Order> = withContext(io) {
        runCatching { api.get(id.raw).toDomain() }
            .mapError(::toDomainError)
    }
}

private fun toDomainError(t: Throwable): DomainError = when (t) {
    is ClientRequestException -> when (t.response.status.value) {
        401 -> DomainError.Unauthorized
        404 -> DomainError.NotFound
        else -> DomainError.Unknown(t.response.status.value.toString())
    }
    is ServerResponseException -> DomainError.Server
    is HttpRequestTimeoutException, is ConnectTimeoutException -> DomainError.Timeout
    is IOException -> DomainError.Network                  // JVM
    is kotlin.coroutines.cancellation.CancellationException -> throw t
    else -> DomainError.Unknown(t.message.orEmpty())
}

inline fun <T> Result<T>.mapError(transform: (Throwable) -> DomainError): Result<T> =
    fold(onSuccess = { Result.success(it) }, onFailure = { Result.failure(transform(it)) })
```

- **Always rethrow `CancellationException`.** `runCatching` doesn't by default.
- Map `ClientRequestException` / `ServerResponseException` before generic catches.

## Testing with MockEngine

See `.claude/skills/kmm-testing/SKILL.md`. `MockEngine` is multiplatform-friendly; use it in `commonTest`.

## Common pitfalls

- **Referencing `OkHttp` or `Darwin` types in `commonMain`.** Inject the engine as `HttpClientEngine`.
- **Creating an `HttpClient` per request.** It's a singleton — expensive to build.
- **`Logging` plugin in release.** Guard with `isDebug()`.
- **Swallowing `CancellationException`** via `runCatching`. Rethrow it.
- **Using `try { client.get(...).body() } catch (e: Exception)`** without specific catches — always differentiate `ClientRequestException`, `ServerResponseException`, and timeouts.
