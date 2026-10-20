---
name: network-layer-architect
description: Design or refactor the network layer for Android or KMP — Retrofit or Ktor setup, OkHttp tuning, interceptors, retry/backoff strategies, caching, error envelopes, offline-first patterns, and auth token handling. Use whenever the user asks to "set up networking", "review the network layer", "add an interceptor", "implement retry logic", "handle 401s", "add offline support", or mentions Retrofit/Ktor/OkHttp configuration. Especially useful for greenfield modules or when reorganizing a tangled networking layer.
---

# Network Layer Architect

A well-shaped network layer hides HTTP from the rest of the app, returns domain types, handles auth and retry centrally, and is testable without spinning up a server. This skill helps you build or refactor toward that.

## When to use

Triggers: "network setup", "Retrofit config", "Ktor client", "OkHttp", "interceptor", "401 refresh", "offline-first", "retry policy", "API error handling", "MockWebServer", "WebSocket".

For a one-off bug fix in an existing endpoint, just fix it. Use this for layer-shaped work.

## Process

### Phase 1: Pick the client

If the project already uses one, match it. Otherwise:

| Use | Pick |
|---|---|
| Android only, REST/JSON, mature ecosystem | Retrofit + OkHttp |
| KMP (shared with iOS), modern Kotlin idioms | Ktor Client |
| Heavy WebSocket / streaming | Ktor (Android or KMP) |
| Existing OkHttp pipeline you want to keep | Ktor with OkHttp engine, or stay on Retrofit |

### Phase 2: Layer the design

Aim for this shape regardless of client:

```
ViewModel
    ↓
Repository (returns domain types, hides HTTP)
    ↓
ApiService (Retrofit interface / Ktor client wrapper)
    ↓
HttpClient (OkHttp / Ktor engine, with interceptors)
```

Rules:
- ViewModels never see `Response`, `Call`, `HttpException`, or DTOs.
- Repositories translate HTTP → domain `Result<T>` or sealed `Outcome` types.
- DTOs (`data class FooResponse(...)`) live in `:data` and never leak past the repository.

### Phase 3: Configure the client

**OkHttp / Retrofit**

```kotlin
val client = OkHttpClient.Builder()
    .connectTimeout(15.seconds.toJavaDuration())
    .readTimeout(30.seconds.toJavaDuration())
    .callTimeout(60.seconds.toJavaDuration())
    .addInterceptor(authInterceptor)
    .addInterceptor(loggingInterceptor)   // last in chain, after auth
    .build()

val retrofit = Retrofit.Builder()
    .baseUrl(BASE_URL)
    .client(client)
    .addConverterFactory(MoshiConverterFactory.create(moshi))
    .build()
```

**Ktor**

```kotlin
HttpClient(OkHttp) {
    install(ContentNegotiation) { json(json) }
    install(HttpTimeout) {
        connectTimeoutMillis = 15_000
        requestTimeoutMillis = 60_000
    }
    install(Logging) { level = LogLevel.HEADERS }
    install(Auth) { bearer { loadTokens { ... }; refreshTokens { ... } } }
    defaultRequest { url(BASE_URL) }
}
```

### Phase 4: Build the interceptor stack

Order matters. From outer to inner:

1. **Logging** — innermost so it sees the final request with auth applied. (Actually OkHttp logs run in registration order, so register logging *last* to see the fully-processed request.)
2. **Auth** — adds `Authorization` header. On 401, refreshes the token and retries the request once.
3. **Telemetry** — records request/response metrics, send to analytics on failure.
4. **Retry** — see Phase 5.
5. **Cache** (if used) — handles ETag and If-Modified-Since.

**Auth interceptor sketch (OkHttp)**

```kotlin
class AuthInterceptor(
    private val tokens: TokenStore,
    private val refresh: TokenRefresher,
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokens.access
        val response = chain.proceed(chain.request().withAuth(token))
        if (response.code == 401 && tokens.refresh != null) {
            response.close()
            val new = refresh.refresh() ?: return chain.proceed(chain.request())
            return chain.proceed(chain.request().withAuth(new.access))
        }
        return response
    }
}
```

Watch for:
- Thread safety on the token store. Use a mutex; refresh should be single-flight.
- Don't refresh on the refresh-token endpoint itself (infinite loop).

### Phase 5: Retry and backoff

Most failures are not worth retrying — 4xx are client errors. Retry only on:

- Network errors (`IOException`).
- 5xx server errors.
- Specific transient codes (429 with Retry-After, 503).

Use exponential backoff with jitter:

```kotlin
retry(maxAttempts = 3) { attempt ->
    val baseDelay = 200L * (1 shl (attempt - 1))   // 200, 400, 800
    val jitter = Random.nextLong(0, baseDelay / 2)
    delay(baseDelay + jitter)
}
```

In Ktor, `HttpRequestRetry` plugin handles this. In OkHttp, write a small interceptor or use `Flow.retry`.

### Phase 6: Error handling

Return sealed types from repositories, not exceptions:

```kotlin
sealed interface NetResult<out T> {
    data class Success<T>(val data: T) : NetResult<T>
    data class HttpError(val code: Int, val body: ErrorBody?) : NetResult<Nothing>
    data object NetworkError : NetResult<Nothing>
    data class Unknown(val cause: Throwable) : NetResult<Nothing>
}
```

Map `HttpException`, `IOException`, etc. inside the repository. ViewModels pattern-match.

For typed error envelopes (`{ "error": { "code": "...", "message": "..." } }`), parse them in the repository and surface as part of `HttpError`.

### Phase 7: Caching strategy

Pick the right tool for each case:

- **HTTP cache** (OkHttp `Cache` with proper headers): cheap, works for GETs where the server cooperates.
- **Database as source of truth**: Room/SQLDelight holds data, network refreshes it. UI observes the database via Flow.
- **In-memory cache**: for ephemeral data not worth persisting.

Offline-first: UI always reads from DB. Network is a refresher. This is more code but the only pattern that handles partial connectivity well.

### Phase 8: Test

- Use MockWebServer (OkHttp) or MockEngine (Ktor) for unit tests of the layer.
- Test auth refresh paths explicitly — easy to get wrong.
- Test the error mapping: a 401 returns `HttpError(401)`, a `SocketTimeoutException` returns `NetworkError`.
- For integration tests, hit a staging environment but keep the suite small and quarantine-tagged.

## Output

A network layer or refactor plan including:

1. Client and library choice with rationale.
2. Layer diagram (HttpClient → ApiService → Repository → ViewModel).
3. Interceptor stack with order.
4. Error envelope and result type.
5. Retry policy.
6. Caching strategy.
7. Test setup outline.

## Common pitfalls

- **Leaking DTOs to ViewModels.** Couples UI to API shape; every API change breaks UI.
- **Catching `Exception` in repositories.** Hides real bugs. Catch the specific exceptions you can handle.
- **Retrying 4xx errors.** Wastes resources, may trigger rate limits.
- **Auth refresh deadlock.** Two concurrent 401s both try to refresh; one wins, the other uses the now-invalid second response. Single-flight with a mutex.
- **MockWebServer not reset between tests.** Tests pollute each other. Reset in `@After`.
- **OkHttp logging at `BODY` level in production.** Logs every request body, including auth tokens.
