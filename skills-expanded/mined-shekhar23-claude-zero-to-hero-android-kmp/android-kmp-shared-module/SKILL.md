---
name: android-kmp-shared-module
description: |
  KMP shared module setup — expect/actual, commonMain/androidMain/iosMain source sets, what belongs in shared vs platform. Use when adding KMP support, creating a shared module, splitting Android code for multiplatform, or working with expect/actual declarations. Trigger on: "KMP", "multiplatform", "shared module", "commonMain", "expect/actual", "iOS shared", "kotlin multiplatform".
---

# KMP Shared Module

## Gradle setup (`build.gradle.kts`)

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
}

kotlin {
    androidTarget {
        compilations.all { kotlinOptions { jvmTarget = "11" } }
    }
    iosX64(); iosArm64(); iosSimulatorArm64()

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.ktor.client.core)
        }
        androidMain.dependencies {
            implementation(libs.ktor.client.okhttp)
        }
        iosMain.dependencies {
            implementation(libs.ktor.client.darwin)
        }
    }
}

android {
    namespace = "com.example.shared"
    compileSdk = libs.versions.compileSdk.get().toInt()
}
```

## What belongs in `commonMain`

| Put in shared | Keep platform-specific |
|---|---|
| Domain models | Android `Context` usage |
| Repository interfaces | Room / SQLDelight Android config |
| Use cases | Compose UI |
| Ktor HTTP client calls | Android permissions |
| `kotlinx.serialization` DTOs | Platform file paths |
| `kotlinx.coroutines` flows | Firebase (Android only) |
| Feature flag interfaces | Play Billing |

## expect / actual pattern

```kotlin
// commonMain
expect class PlatformInfo() {
    val name: String
}

// androidMain
actual class PlatformInfo actual constructor() {
    actual val name: String = "Android ${android.os.Build.VERSION.SDK_INT}"
}

// iosMain
actual class PlatformInfo actual constructor() {
    actual val name: String = UIDevice.currentDevice.systemName()
}
```

## Repository interface in shared, impl per platform

```kotlin
// commonMain — core:domain
interface TaskRepository {
    fun getTasks(): Flow<List<Task>>
    suspend fun syncTasks(): EmptyResult<DataError>
}

// androidMain — core:data (Android module)
class TaskRepositoryImpl(
    private val dao: TaskDao,         // Room — Android only
    private val api: TaskApi,
) : TaskRepository { ... }
```

## Checklist

- [ ] No `android.*` imports in `commonMain`
- [ ] `expect`/`actual` only for truly platform-divergent behaviour
- [ ] Coroutines and serialization come from KMP-compatible artifacts
- [ ] Ktor engine injected per platform (OkHttp / Darwin)
- [ ] Domain models are plain Kotlin data classes — no Android annotations
