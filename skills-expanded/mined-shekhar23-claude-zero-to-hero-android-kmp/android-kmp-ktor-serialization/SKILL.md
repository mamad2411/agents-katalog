---
name: android-kmp-ktor-serialization
description: |
  Ktor HTTP client + kotlinx.serialization for shared KMP networking — client setup in commonMain, platform engines, request/response helpers, typed errors. Use when building a shared network layer, adding API calls to KMP, or serializing JSON in commonMain. Trigger on: "Ktor KMP", "shared networking", "kotlinx.serialization KMP", "multiplatform HTTP", "commonMain API".
---

# KMP Ktor + kotlinx.serialization

## Dependency setup

```toml
# libs.versions.toml
[versions]
ktor = "2.3.12"
serialization = "1.7.3"

[libraries]
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-serialization-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }
ktor-client-logging = { module = "io.ktor:ktor-client-logging", version.ref = "ktor" }
ktor-client-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-client-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
kotlinx-serialization-json = { module = "org.jetbrains.kotlinx:kotlinx-serialization-json", version.ref = "serialization" }
```

## HttpClient factory (`commonMain`)

```kotlin
// core:data — commonMain
fun createHttpClient(engine: HttpClientEngine): HttpClient = HttpClient(engine) {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
            isLenient = true
        })
    }
    install(Logging) {
        level = LogLevel.HEADERS
    }
    defaultRequest {
        url("https://api.example.com/v1/")
        contentType(ContentType.Application.Json)
    }
}
```

## Platform engine injection

```kotlin
// androidMain
fun provideHttpClient(): HttpClient = createHttpClient(OkHttp.create())

// iosMain
fun provideHttpClient(): HttpClient = createHttpClient(Darwin.create())
```

## DTO + serialization

```kotlin
// commonMain
@Serializable
data class TaskDto(
    val id: String,
    val title: String,
    @SerialName("due_at") val dueAt: String?,
    val priority: String,
)
```

## Safe API call helper

```kotlin
// commonMain — core:data
suspend inline fun <reified T> safeApiCall(
    call: () -> T
): Result<T, DataError.Network> = try {
    Result.Success(call())
} catch (e: RedirectResponseException) {
    Result.Error(DataError.Network.SERVER_ERROR)
} catch (e: ClientRequestException) {
    if (e.response.status == HttpStatusCode.Unauthorized)
        Result.Error(DataError.Network.UNAUTHORIZED)
    else
        Result.Error(DataError.Network.SERVER_ERROR)
} catch (e: ServerResponseException) {
    Result.Error(DataError.Network.SERVER_ERROR)
} catch (e: Exception) {
    Result.Error(DataError.Network.UNKNOWN)
}
```

## Usage in a remote data source

```kotlin
// commonMain
class TaskRemoteDataSource(private val client: HttpClient) {
    suspend fun getTasks(): Result<List<TaskDto>, DataError.Network> = safeApiCall {
        client.get("tasks").body<List<TaskDto>>()
    }
}
```

## Checklist

- [ ] `createHttpClient` in `commonMain`, engine injected per platform
- [ ] All DTOs annotated with `@Serializable`
- [ ] `safeApiCall` wraps every request — no raw `try/catch` at call sites
- [ ] `ignoreUnknownKeys = true` on all Json instances
- [ ] Token injection via `defaultRequest` or a dedicated plugin
