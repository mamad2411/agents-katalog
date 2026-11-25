---
name: kmp-patterns
description: Build Kotlin Multiplatform (KMP) applications — shared business logic across Android, iOS, desktop, and web. Covers project structure, expect/actual declarations, Ktor networking, SQLDelight database, Koin DI, and Compose Multiplatform UI. Use when building KMP apps, sharing code between platforms, or implementing cross-platform features. Trigger on "KMP", "Kotlin Multiplatform", "Compose Multiplatform", "shared module", "expect actual".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Kotlin Multiplatform (KMP) Patterns Skill

Build cross-platform applications sharing business logic.

## Project Structure
```
project/
├── shared/                       → Shared KMP module
│   ├── src/
│   │   ├── commonMain/           → Shared code (all platforms)
│   │   │   └── kotlin/
│   │   │       ├── domain/       → Entities, use cases
│   │   │       ├── data/         → Repositories, DTOs
│   │   │       ├── network/      → Ktor API client
│   │   │       ├── database/     → SQLDelight queries
│   │   │       └── di/           → Koin modules
│   │   ├── androidMain/          → Android-specific implementations
│   │   ├── iosMain/              → iOS-specific implementations
│   │   └── commonTest/           → Shared tests
│   └── build.gradle.kts
├── androidApp/                   → Android application
│   └── src/main/
│       └── kotlin/               → Android UI (Compose)
├── iosApp/                       → iOS application (SwiftUI wrapper)
│   └── iosApp/
│       ├── ContentView.swift
│       └── iOSApp.swift
├── desktopApp/                   → Desktop (optional)
└── build.gradle.kts
```

## Expect/Actual Pattern
```kotlin
// commonMain — declare expected interface
expect class PlatformContext

expect fun getPlatformName(): String

expect class SecureStorage(context: PlatformContext) {
    fun save(key: String, value: String)
    fun get(key: String): String?
    fun delete(key: String)
}

// androidMain — Android implementation
actual typealias PlatformContext = Context

actual fun getPlatformName(): String = "Android ${Build.VERSION.SDK_INT}"

actual class SecureStorage actual constructor(context: PlatformContext) {
    private val prefs = EncryptedSharedPreferences.create(/*...*/)
    actual fun save(key: String, value: String) { prefs.edit().putString(key, value).apply() }
    actual fun get(key: String): String? = prefs.getString(key, null)
    actual fun delete(key: String) { prefs.edit().remove(key).apply() }
}

// iosMain — iOS implementation
actual typealias PlatformContext = Unit

actual fun getPlatformName(): String = UIDevice.currentDevice.systemName

actual class SecureStorage actual constructor(context: PlatformContext) {
    actual fun save(key: String, value: String) { /* Keychain */ }
    actual fun get(key: String): String? { /* Keychain */ }
    actual fun delete(key: String) { /* Keychain */ }
}
```

## Ktor Networking (Shared)
```kotlin
// commonMain
class ApiClient(private val httpClient: HttpClient) {
    suspend fun getUsers(): List<UserDto> =
        httpClient.get("https://api.example.com/users").body()
    
    suspend fun createUser(dto: CreateUserDto): UserDto =
        httpClient.post("https://api.example.com/users") {
            contentType(ContentType.Application.Json)
            setBody(dto)
        }.body()
}

// Shared HttpClient config
val httpClient = HttpClient {
    install(ContentNegotiation) { json(Json { ignoreUnknownKeys = true }) }
    install(Logging) { level = LogLevel.INFO }
    install(Auth) {
        bearer {
            loadTokens { BearerTokens(tokenStorage.getAccessToken(), tokenStorage.getRefreshToken()) }
            refreshTokens { /* refresh logic */ }
        }
    }
}
```

## SQLDelight (Shared Database)
```sql
-- shared/src/commonMain/sqldelight/com/example/db/User.sq
CREATE TABLE User (
    id TEXT NOT NULL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

getAll:
SELECT * FROM User ORDER BY created_at DESC;

getById:
SELECT * FROM User WHERE id = ?;

insert:
INSERT OR REPLACE INTO User (id, email, name) VALUES (?, ?, ?);

deleteById:
DELETE FROM User WHERE id = ?;
```

## Compose Multiplatform UI (Shared)
```kotlin
@Composable
fun UserListScreen(viewModel: UserListViewModel = koinViewModel()) {
    val state by viewModel.state.collectAsState()
    
    when (val s = state) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Error -> ErrorMessage(s.message, onRetry = viewModel::refresh)
        is UiState.Success -> LazyColumn {
            items(s.users) { user -> UserCard(user) }
        }
    }
}
```

## Anti-Patterns

- **Platform code in commonMain** — putting Android/iOS specific code in shared modules; use expect/actual
- **No expect/actual for platform APIs** — directly referencing platform classes instead of abstracting
- **Fat ViewModels** — putting business logic in ViewModels; extract into use cases in domain layer
- **Not testing commonMain** — only testing platform-specific code; shared logic needs comprehensive coverage
- **Mixing DI frameworks** — using Koin in some modules and manual DI in others; be consistent
- **Ignoring Kotlin/Native concurrency** — sharing mutable state across threads without proper isolation

## Checklist

- [ ] Shared business logic in commonMain
- [ ] expect/actual for platform-specific APIs
- [ ] Ktor client in commonMain with platform engines
- [ ] SQLDelight schema for local persistence
- [ ] Koin modules for dependency injection
- [ ] ViewModels use StateFlow for UI state
- [ ] commonTest covers shared logic
- [ ] Platform tests in androidTest/iosTest
