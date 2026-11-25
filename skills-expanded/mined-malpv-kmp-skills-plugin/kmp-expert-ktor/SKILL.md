---
name: kmp-expert-ktor
description: Wire the Ktor networking layer into a KMP project — dependencies, the shared HttpClient with auth/refresh and secure logging, per-platform engines, and the DTO→domain repository flow with MockEngine tests. Use whenever the user adds networking, consumes a REST API, mentions Ktor, HttpClient, bearer/token refresh, DataSources or DTOs, request logging, or debugs 401s, missing-INTERNET-permission crashes, or empty network logs. Applies the standard, does not just describe it.
---

# Skill: KMP Expert Ktor

This skill provides the definitive engineering standard for structuring the network layer in Kotlin Multiplatform (KMP) projects, ensuring secure transactions, resilience to failures, clean automated testing, and robust error handling following Clean Architecture principles.

> [!NOTE]
> **Placement (architecture-agnostic):** the shared `HttpClient` + plugins are network **infrastructure**; the DTOs, DataSources, and repositories belong to the consuming feature's **data layer**. In a **modular** project (feature + layers) map these to the corresponding modules — see `kmp-modular-architecture`. In a **single-module** project they are packages under `commonMain` (and the platform source sets). This skill does not assume a module layout.

## Workflow

This skill **applies** the standard. Do the steps in order; each points to the section with the full code and its warnings. Do not stop at summarizing.

1. **Dependencies** (§1) — add the catalog entries and the `shared` Gradle wiring. Reconcile against what the project already declares; do not duplicate versions.
2. **Decide auth.** Does the API need a bearer token? **No** → build the client without the `Auth` block. **Yes** → include it (§4), and confirm where refresh tokens are stored: this skill consumes a `TokenStorage` interface, implemented by `kmp-encrypted-storage`. Refresh lives only in the client, never in a feature's DataSource.
3. **HttpClient factory** (§2) — one client, `isDebug` sourced from the build (never hardcoded), `Logger.SIMPLE`.
4. **Per-platform engines** (§3) — OkHttp/Darwin via DI. **Android: declare the `INTERNET` permission** or every request fails at runtime.
5. **Feature data layer** (§5) — DTOs, DataSource, and the repository returning `Flow<ResultState<T>>`. Rethrow `CancellationException`; map transport errors once.
6. **Tests** (§6) — a MockEngine test per DataSource. A compiling client is not a working one — this is where behavior is checked.
7. **Verify by running.** Neither compilation nor the graph proves the calls work: the `INTERNET` permission and `Logger.DEFAULT` both fail only at runtime. Drive one real request and read the log.

---

## Networking Standards

1. **Single Client (Singleton)**: A single `HttpClient` managed by DI and reused across all requests to leverage connection pooling and prevent memory leaks.
2. **Physical Engine Layer**: Selection of the optimal native engine per platform (OkHttp for Android, Darwin for iOS).
3. **Strict Data Mapping**: Network responses use serializable DTOs. Conversion to pure Domain Models (free of `@Serializable` annotations) is performed in the Repository.
4. **Reactive ResultState Pattern**: Network calls are encapsulated and returned to the UI as a `Flow<ResultState<T>>` (featuring `Loading`, `Success`, and `Error` states).
5. **Integrated Security**: Automatic masking of authorization credentials in debug logs and secure token injection.

---

## 1. Dependencies (libs.versions.toml)

```toml
[versions]
ktor = "<version>"

[libraries]
ktor-client-core = { group = "io.ktor", name = "ktor-client-core", version.ref = "ktor" }
ktor-client-content-negotiation = { group = "io.ktor", name = "ktor-client-content-negotiation", version.ref = "ktor" }
ktor-client-logging = { group = "io.ktor", name = "ktor-client-logging", version.ref = "ktor" }
ktor-client-auth = { group = "io.ktor", name = "ktor-client-auth", version.ref = "ktor" }
ktor-serialization-kotlinx-json = { group = "io.ktor", name = "ktor-serialization-kotlinx-json", version.ref = "ktor" }
ktor-client-okhttp = { group = "io.ktor", name = "ktor-client-okhttp", version.ref = "ktor" }
ktor-client-darwin = { group = "io.ktor", name = "ktor-client-darwin", version.ref = "ktor" }
ktor-client-mock = { group = "io.ktor", name = "ktor-client-mock", version.ref = "ktor" }
```

### Gradle Configuration (`shared/build.gradle.kts`):
```kotlin
commonMain.dependencies {
    implementation(libs.ktor.client.core)
    implementation(libs.ktor.client.content.negotiation)
    implementation(libs.ktor.serialization.kotlinx.json)
    implementation(libs.ktor.client.logging)
    implementation(libs.ktor.client.auth)
}
androidMain.dependencies {
    implementation(libs.ktor.client.okhttp)
}
iosMain.dependencies {
    implementation(libs.ktor.client.darwin)
}
commonTest.dependencies {
    implementation(libs.ktor.client.mock)
}
```

---

## 2. HttpClient Configuration and Factory

The HTTP client is initialized in `commonMain` by injecting the platform-specific engine (`HttpClientEngine`).

```kotlin
import io.ktor.client.HttpClient
import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.logging.LogLevel
import io.ktor.client.plugins.logging.Logger
import io.ktor.client.plugins.logging.Logging
import io.ktor.client.plugins.defaultRequest
import io.ktor.http.ContentType
import io.ktor.http.HttpHeaders
import io.ktor.http.contentType
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

fun createHttpClient(
    engine: HttpClientEngine,
    baseUrl: String,
    isDebug: Boolean = false
): HttpClient = HttpClient(engine) {
    
    // 1. Serialization
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
            isLenient = true
            // Important: encodeDefaults = true ensures properties with default
            // values are included in the JSON payload sent to the server.
            encodeDefaults = true
        })
    }

    // 2. Default Request Headers
    defaultRequest {
        url(baseUrl)
        contentType(ContentType.Application.Json)
    }

    // 3. Timeouts
    install(HttpTimeout) {
        connectTimeoutMillis = 15_000L
        requestTimeoutMillis = 30_000L
        socketTimeoutMillis = 15_000L
    }

    // 4. Secure Logging (Prevents authorization token leaks)
    install(Logging) {
        level = if (isDebug) LogLevel.BODY else LogLevel.HEADERS
        logger = Logger.SIMPLE // Not DEFAULT — see the note below
        sanitizeHeader { it.equals(HttpHeaders.Authorization, ignoreCase = true) }
    }

    // 5. Automatic exceptions on non-2xx status codes
    expectSuccess = true
}
```

> [!WARNING]
> **Use `Logger.SIMPLE`, not `Logger.DEFAULT` — on Android `DEFAULT` logs nothing.** `Logger.DEFAULT` resolves to an SLF4J-backed logger on JVM/Android. Android ships no SLF4J binding, so it silently degrades to a no-op: requests run fine and **not a single line reaches logcat**, which reads exactly like "the logging plugin is broken" or "my flag is off". `Logger.SIMPLE` uses `println`, so it works on both platforms — logcat on Android, console on iOS — with no extra dependency.
>
> Debug this by elimination: if `LogLevel.HEADERS` also prints nothing, the problem is the **logger**, not the level or the `isDebug` flag. Only add an SLF4J binding if the project already depends on it for other reasons.

> [!NOTE]
> **`isDebug` and header sanitization.** `sanitizeHeader { ... Authorization ... }` is **unconditional** — the `Authorization` header is masked in logs on every build, debug or release. But `sanitizeHeader` only covers **headers, not bodies**: with `LogLevel.BODY` the response bodies of `auth/login` and `auth/refresh` still print `accessToken`/`refreshToken` in clear text. That is why the level itself is gated on `isDebug` (`BODY` in debug, `HEADERS` in release) — never wire `isDebug = true` (or `LogLevel.BODY`) into a release build or the DI graph unconditionally.
>
> Source the flag from the build's own debug signal, not from a hardcoded literal. The portable, dependency-free way is an `expect/actual` value — do **not** pull in a plugin just for one boolean:
>
> ```kotlin
> // commonMain
> expect val isDebugBuild: Boolean
> // androidMain
> actual val isDebugBuild: Boolean = BuildConfig.DEBUG
> // iosMain — kotlin.native.Platform
> actual val isDebugBuild: Boolean = Platform.isDebugBinary
> ```
>
> Then `createHttpClient(..., isDebug = isDebugBuild)`. If DI is initialized per platform, an equally clean variant is to pass the flag into `initKoin(isDebug)` from each platform entry point (Android already knows `BuildConfig.DEBUG`). Only reach for `BuildKonfig.DEBUG` if the project already uses BuildKonfig for other config. Keep this flag separate from where the app sources its endpoints or secrets.

---

## 3. Platform-Specific Engines

Only the engine changes per platform; the `HttpClient` configuration (section 2) is shared. Provide each engine via DI so the factory stays platform-agnostic. Timeouts are already handled by the `HttpTimeout` plugin in the shared config, so the engines need no extra setup.

### Android Engine (`androidMain` - OkHttp)
```kotlin
import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.engine.okhttp.OkHttp
import org.koin.dsl.module

actual val engineModule = module {
    single<HttpClientEngine> { OkHttp.create() }
}
```

> [!WARNING]
> **Android requires the `INTERNET` permission — declare it or every request fails at runtime.** This is not a compile error and not a Ktor error: the app builds, DI resolves, the request fires, and the engine dies inside DNS resolution with `java.lang.SecurityException: Permission denied (missing INTERNET permission?)`. Add it to the app's `AndroidManifest.xml`:
>
> ```xml
> <manifest xmlns:android="http://schemas.android.com/apk/res/android">
>     <uses-permission android:name="android.permission.INTERNET" />
>     <application ... />
> </manifest>
> ```
>
> Declaring it in the **app** module keeps every permission visible in one auditable place. A library module can declare it instead and let manifest merging propagate it, but then the app's permission list no longer tells the whole story — prefer the app manifest unless you have a reason not to. iOS needs no equivalent: outbound HTTPS requires no entitlement.
>
> If the API is served over plain `http://`, Android also blocks it by default from API 28 onward (cleartext traffic). Fix the endpoint to HTTPS rather than enabling `android:usesCleartextTraffic`.

### iOS Engine (`iosMain` - Darwin)
```kotlin
import io.ktor.client.engine.HttpClientEngine
import io.ktor.client.engine.darwin.Darwin
import org.koin.dsl.module

actual val engineModule = module {
    single<HttpClientEngine> { Darwin.create() }
}
```

---

## 4. Token Authentication (Bearer Auto-Refresh)

Ktor's `Auth` plugin intercepts outgoing requests, appending the bearer token, and automatically coordinates token refresh mechanics if the server returns a `401 Unauthorized` status.

```kotlin
import io.ktor.client.plugins.auth.Auth
import io.ktor.client.plugins.auth.providers.bearer
import io.ktor.client.plugins.auth.providers.BearerTokens
import io.ktor.client.request.post
import io.ktor.client.request.setBody

// In the HttpClient configuration:
install(Auth) {
    bearer {
        loadTokens {
            val session = tokenStorage.getTokens() ?: return@loadTokens null
            BearerTokens(session.accessToken, session.refreshToken)
        }
        
        refreshTokens {
            val refresh = oldTokens?.refreshToken ?: return@refreshTokens null
            try {
                // markAsRefreshTokenRequest() prevents this token refresh call
                // from going through this same interceptor, avoiding infinite loops.
                markAsRefreshTokenRequest() 
                
                val response = client.post("auth/refresh") {
                    setBody(RefreshRequestDto(refresh))
                }.body<TokenResponseDto>()
                
                tokenStorage.saveTokens(response.accessToken, response.refreshToken)
                BearerTokens(response.accessToken, response.refreshToken)
            } catch (e: Exception) {
                // Logout / expire session if the refresh token call fails
                onSessionExpired()
                null
            }
        }
        
        // Attach the token proactively. loadTokens returns null before login,
        // so nothing is attached to login/public pre-auth calls. See the note below.
        sendWithoutRequest { true }
    }
}
```

> [!NOTE]
> **Refresh lives only here.** Token refresh is handled exclusively by the `Auth` plugin in the network infrastructure. `RefreshRequestDto` / `TokenResponseDto` belong to this network layer — a feature's `RemoteDataSource` must **not** expose a `refresh()` method or duplicate these DTOs. Features do login / logout / data calls; refresh is transparent and automatic on `401`.
>
> **`TokenStorage` is an interface** the network layer owns; bind its implementation via DI. For persistence across launches, implement it with the **`kmp-encrypted-storage`** skill (Keychain / EncryptedSharedPreferences); an in-memory implementation is fine only as a temporary placeholder. `baseUrl` is a plain `String` supplied by DI — keep this layer agnostic of where it comes from.

> [!NOTE]
> **`sendWithoutRequest`: prefer `{ true }`.** It decides whether to attach the token **proactively** (without waiting for a `401` challenge — which many APIs never send, so the reactive default silently fails to attach). For a client scoped to a single API host (`defaultRequest { url(baseUrl) }`), `{ true }` is the robust, generic default: `loadTokens` returns `null` before login, so nothing leaks to login/public pre-auth calls. Matching literal path names is **fragile** (it breaks if your auth endpoints are named differently) and is only needed to withhold an *existing* token from specific endpoints — e.g. a client that spans multiple hosts.

```kotlin
// WRONG — inverted: attaches the token ONLY to login/public, and makes protected calls
// wait for a 401 challenge that many APIs never send (so auth silently fails)
sendWithoutRequest { req -> req.url.pathSegments.any { it == "login" || it == "public" } }

// RIGHT — single-host client: attach proactively; loadTokens guards the pre-login case
sendWithoutRequest { true }

// VARIANT — only to withhold an existing token from specific endpoints (e.g. multi-host client)
sendWithoutRequest { req -> req.url.pathSegments.none { it in listOf("login", "register") } }
```

---

## 5. DataSource, Mapping, and Repository Flow

### A. Data Layer: DTOs and RemoteDataSource
The DataSource only handles the network transaction and returns the structured DTO.
```kotlin
import io.ktor.client.call.body
import io.ktor.client.request.get
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ItemDto(
    @SerialName("id") val id: String,
    @SerialName("title") val title: String,
    @SerialName("desc") val desc: String? = null
)

class RemoteDataSource(private val httpClient: HttpClient) {
    suspend fun getItems(): List<ItemDto> {
        return httpClient.get("items").body()
    }
}
```

### B. Domain Layer: ResultState and Pure Model
```kotlin
sealed class ResultState<out T> {
    data class Success<T>(val data: T) : ResultState<T>()
    data class Error(val error: Throwable, val customMessage: String?) : ResultState<Nothing>()
    data object Loading : ResultState<Nothing>()
}

data class ItemModel(val id: String, val title: String)

// Mapper: Converts DTO to Domain Model
fun ItemDto.toDomain() = ItemModel(id = id, title = title)
```

### C. Repository Layer: Coordination and Error Handling
The repository wraps network calls into reactive streams, catches Ktor-specific exceptions, and maps them to domain-level errors to avoid leaking network implementation details to the presentation layer.
```kotlin
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import io.ktor.client.plugins.ClientRequestException
import io.ktor.client.plugins.ServerResponseException
import io.ktor.client.plugins.HttpRequestTimeoutException
import kotlinx.io.IOException
import kotlin.coroutines.cancellation.CancellationException

class ItemRepositoryImpl(private val dataSource: RemoteDataSource) : ItemRepository {
    override fun fetchItems(): Flow<ResultState<List<ItemModel>>> = flow {
        emit(ResultState.Loading)
        try {
            val dtos = dataSource.getItems()
            emit(ResultState.Success(dtos.map { it.toDomain() }))
        } catch (e: CancellationException) {
            throw e // never swallow cancellation — it breaks structured concurrency
        } catch (e: ClientRequestException) { // 4xx
            emit(ResultState.Error(e, "Client error: ${e.response.status.value}"))
        } catch (e: ServerResponseException) { // 5xx
            emit(ResultState.Error(e, "Server error: ${e.response.status.value}"))
        } catch (e: HttpRequestTimeoutException) {
            emit(ResultState.Error(e, "Request timeout"))
        } catch (e: IOException) { // No internet connection
            emit(ResultState.Error(e, "No internet connection"))
        } catch (e: Exception) {
            emit(ResultState.Error(e, "An unexpected error occurred"))
        }
    }
}
```

---

## 6. Unit Testing with MockEngine

Injecting the `HttpClientEngine` allows you to mock the network layer at runtime without sending real HTTP requests.

```kotlin
import io.ktor.client.engine.mock.MockEngine
import io.ktor.client.engine.mock.respond
import io.ktor.http.HttpStatusCode
import io.ktor.http.headersOf
import io.ktor.http.HttpHeaders
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs

class UserRepositoryTest {

    @Test
    fun `fetchItems returns success and deserializes correctly`() = runTest {
        // 1. Mock Engine Setup
        val mockEngine = MockEngine { request ->
            assertEquals("/items", request.url.encodedPath)
            respond(
                content = """[{"id":"1","title":"Kotlin"}]""",
                status = HttpStatusCode.OK,
                headers = headersOf(HttpHeaders.ContentType, "application/json")
            )
        }
        
        // 2. HttpClient instantiation using the Mock Engine
        val testClient = createHttpClient(mockEngine, baseUrl = "https://api.test.com/", isDebug = true)
        val dataSource = RemoteDataSource(testClient)
        val repository = ItemRepositoryImpl(dataSource)
        
        // 3. Verification
        repository.fetchItems().collect { state ->
            if (state is ResultState.Success) {
                assertEquals(1, state.data.size)
                assertEquals("Kotlin", state.data.first().title)
            }
        }
    }
}
```

---

## Correct vs. Incorrect Patterns

*   **Incorrect**: Creating a new instance of `HttpClient` inside a suspend function. This causes thread leaks and keeps sockets open unnecessarily.
*   **Correct**: Instantiating `HttpClient` only once as a singleton and supplying it via DI to DataSources.
*   **Incorrect**: Attempting manual token refresh logic by intercepting calls inside repository try/catch blocks.
*   **Correct**: Using Ktor's native `Auth` plugin and the `markAsRefreshTokenRequest()` directive to let the framework orchestrate retry requests.
*   **Incorrect**: Leaking Ktor-specific exceptions (`ClientRequestException`, `RedirectResponseException`) directly to ViewModels in the presentation layer.
*   **Correct**: Catching exceptions inside the Repository and mapping them to decoupled domain-specific error types.
