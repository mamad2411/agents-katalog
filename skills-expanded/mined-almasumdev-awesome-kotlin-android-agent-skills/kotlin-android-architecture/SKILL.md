---
name: kotlin-android-architecture
description: Expert guidance on a modern Kotlin-first Android application architecture using Clean Architecture, Gradle module separation, version catalogs, and Hilt DI. Use this when asked about project structure, module layout, or dependency injection.
---

# Kotlin Android Clean Architecture & Modularization

## Instructions

When designing or refactoring a Kotlin Android application, follow **Clean Architecture** principles. Dependencies must flow **inwards** toward pure Kotlin domain code. Kotlin 2.0 (K2), JVM 17, Compose-first.

### 1. High-Level Layers

- **Presentation Layer** (`:app`, `:feature:*:ui`)
  - Responsibility: Render Compose UI and expose ViewModels.
  - Components: `@Composable` screens, `HiltViewModel` classes exposing `StateFlow<UiState>`, and one-shot events via `SharedFlow<UiEvent>`.
  - Dependencies: Domain interfaces only. No Retrofit, no Room here.
- **Domain Layer** (`:core:domain`, `:feature:*:domain`) — pure Kotlin, no Android dependencies
  - Components: UseCases (`class GetArticlesUseCase @Inject constructor(...)`), immutable `data class` entities, repository **interfaces**.
  - Rule: Module-level `plugins { kotlin("jvm") }` only. No `com.android.library`. This is enforceable.
- **Data Layer** (`:core:data`, `:feature:*:data`)
  - Components: Repository **implementations**, Retrofit API services, Room `@Dao`s, DTOs with `@Serializable`, and mappers to domain models.

### 2. Module Graph

```
:app
 └─ depends on feature modules + :core:designsystem + :core:ui
:feature:articles:ui       → :feature:articles:domain, :core:designsystem
:feature:articles:data     → :feature:articles:domain, :core:network, :core:database
:feature:articles:domain   → (pure Kotlin)
:core:network              → Retrofit, OkHttp, kotlinx.serialization
:core:database             → Room
:core:designsystem         → Compose, Material 3 tokens, typography, shapes
```

### 3. Version Catalog (`gradle/libs.versions.toml`)

```toml
[versions]
kotlin = "2.0.21"
agp = "8.7.2"
compose-bom = "2024.10.01"
hilt = "2.52"
room = "2.6.1"
retrofit = "2.11.0"
kotlinx-serialization = "1.7.3"

[libraries]
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version = "2.0.21-1.0.25" }
```

### 4. Dependency Injection with Hilt

```kotlin
@HiltAndroidApp
class MyApp : Application()

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun provideJson(): Json = Json { ignoreUnknownKeys = true; explicitNulls = false }

    @Provides @Singleton
    fun provideRetrofit(client: OkHttpClient, json: Json): Retrofit =
        Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(client)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryBindings {
    @Binds abstract fun bindArticleRepo(impl: ArticleRepositoryImpl): ArticleRepository
}
```

For Koin (alternative): declare modules with `single { ... }` / `viewModel { ... }` and call `startKoin { modules(appModule) }` in `Application.onCreate`.

### 5. Feature Module Template

```kotlin
// feature/articles/ui/build.gradle.kts
plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
}

android { namespace = "com.example.feature.articles.ui"; compileSdk = 35 }

dependencies {
    implementation(projects.feature.articles.domain)
    implementation(projects.core.designsystem)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
    implementation(libs.hilt.android); ksp(libs.hilt.compiler)
}
```

### 6. Rules the Agent Must Enforce
- Domain modules use `kotlin("jvm")`, never `com.android.library`.
- Feature modules do not depend on other feature modules directly — wire across features in `:app` only.
- Every public repository returns **domain models**, never DTOs.
- Every ViewModel exposes a single immutable `UiState` via `StateFlow`, plus a `Channel<UiEvent>` or `SharedFlow<UiEvent>` for navigation/toasts.

## Checklist
- [ ] Domain modules have zero Android dependencies (`./gradlew :core:domain:dependencies | grep androidx` returns nothing).
- [ ] `libs.versions.toml` is the single source of versions; no hard-coded `"x.y.z"` in build scripts.
- [ ] Hilt graph compiles (`./gradlew :app:kspDebugKotlin`).
- [ ] Repositories return domain entities; DTOs live only in `:feature:*:data`.
- [ ] Feature-to-feature imports fail CI (enforced by a module-graph lint or `konsist` rule).
