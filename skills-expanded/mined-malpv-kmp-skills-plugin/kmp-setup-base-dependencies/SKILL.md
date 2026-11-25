---
name: kmp-setup-base-dependencies
description: Set up the dependency catalog and base Gradle config for a KMP project — a capability-grouped libs.versions.toml, the root/shared/androidApp build files, and dynamic Android SDK versions. Use whenever the user bootstraps a KMP project, adds a library or plugin, edits libs.versions.toml or the version catalog, aligns coupled versions (kotlin/ksp/compose/agp), or hits a plugin-resolution / "version does not exist" / IDE-can't-resolve-stdlib error. Apply this before the capability skills (ktor, room, koin...).
---

# Skill: KMP Setup Base Dependencies

This skill delivers two things for a Kotlin Multiplatform (KMP) / Compose Multiplatform (CMP) project:

1. **A centralized version catalog (`gradle/libs.versions.toml`) grouped by capability** — one vetted place for all versions and coordinates, so you never hunt for compatible versions again.
2. **A minimal, correct base project** (`settings.gradle.kts`, root `build.gradle.kts`, `:shared`, `:androidApp`) that wires **only the core**. Every extra capability (networking, database, images, Firebase...) is added deliberately, on demand.

The deep setup of each capability lives in its **sibling skill** (`kmp-expert-ktor`, `kmp-expert-room`, `kmp-expert-koin`, `kmp-expert-navigation`). This skill only provides the catalog entries and where they wire.

## How to Use This Skill

- **Infer capabilities from the task; ask only the ambiguous ones.** "Consume a REST API and store data locally" clearly implies networking + persistence — do not ask. Capabilities that cannot be inferred (Firebase, Crashlytics, analytics) should be confirmed with the user before wiring.
- **Wire only the capability groups you need.** The base project is core-only. Adding a capability means: add its catalog group, then apply the additive block from section 3.
- **Do not dump the whole catalog into the build files.** The catalog is a menu, not a shopping list.
- **Applying over an existing / wizard project:** the project already ships its own versions. Replace the ones this catalog covers with the catalog's vetted set and **delete the project's duplicates** — never keep half and mix. Mixing coupled versions (`kotlin` / `compose`) is what triggers the compile-error / version-guessing loop this catalog exists to prevent.

> [!WARNING]
> **A plugin that fails to resolve is a wrong version, not a wrong toolchain. Never downgrade `agp` or `kotlin` to make a plugin resolve.** This is the single most destructive failure mode when applying this skill. Downgrading `kotlin` cascades into `ksp` and `compose`; downgrading `agp` breaks the `androidLibrary {}` KMP DSL and drags the project back to the legacy `android {}` + `androidTarget()` pattern — an afternoon of damage to fix a one-line version typo.
>
> When a plugin does not resolve, **verify the version exists** before changing anything else:
>
> ```bash
> curl -s -o /dev/null -w "%{http_code}" \
>   https://repo1.maven.org/maven2/com/google/devtools/ksp/com.google.devtools.ksp.gradle.plugin/<version>/
> # 404 = the version does not exist. Fix the version. Do not touch agp/kotlin.
> ```
>
> **Never build the `ksp` version from `kotlin`.** KSP2 has its own version number (`2.3.2`); the `<kotlin>-<ksp>` format (`2.1.20-1.0.31`) is KSP1 and is obsolete. Prefixing the project's Kotlin version produces an artifact that does not exist — which then reads as "Kotlin is too new" and triggers the downgrade spiral. Take the KSP version from its own release list and verify it resolves.

> [!WARNING]
> **Pin `kotlin` to what the IDE supports, not to the newest release.** A Kotlin version newer than the IDE's bundled Kotlin plugin builds perfectly from Gradle while the editor fails to analyze the project at all: the tell-tale symptom is **stdlib** symbols reported as unresolved — `emptyList`, `setOf`, `CancellationException` — across every file. That is not broken code. It is the IDE unable to resolve the source sets.
>
> Diagnose it by the same rule as any other red herring: **if `./gradlew assembleDebug` produces an APK, the code is fine.** Reach for the IDE's supported Kotlin version instead of downgrading `agp`, rewriting module DSLs, or chasing the errors file by file. The `kotlin` version pinned here is chosen for that reason — bumping it to the latest release is a regression in usability even when it compiles.

## When to Use

- Bootstrapping a new KMP project with a clean, centralized dependency setup.
- Centralizing Android SDK, compile/target versions dynamically from the catalog.
- Establishing base dependencies without version conflicts.

---

## Capability Map

| Capability | When to include | Catalog group | Wires in | Sibling skill |
|---|---|---|---|---|
| Core (KMP + Compose + Android) | Always | Core | `:shared` + `:androidApp` | — |
| DI (Koin) | Recommended default | Koin | `:shared` | `kmp-expert-koin` |
| Networking (Ktor) | Talks to an HTTP/REST API | Ktor | `:shared` | `kmp-expert-ktor` |
| Persistence (Room) | Local relational DB | Room | `:shared` | `kmp-expert-room` |
| Images (Coil) | Loads remote images | Coil | `:shared` | — |
| Navigation | Multi-screen type-safe nav | Navigation | `:shared` | `kmp-expert-navigation` |
| Permissions | Runtime permissions | Permissions | `:shared` | — |
| Date/Time | Cross-platform date/time | Utils | `:shared` | — |
| Firebase / Crashlytics | Google/Firebase services | Firebase | `:androidApp` only | — |

---

## 1. Version Catalog (`gradle/libs.versions.toml`)

Centralized catalog grouped by capability. The base project only needs the **Core** and **Koin** groups. Keep (or drop) the optional groups depending on what the project actually uses.

> [!NOTE]
> Adjust Kotlin, KSP, and Compose Multiplatform versions per their compatibility matrix. KSP must match the installed Kotlin version.

```toml
# gradle/libs.versions.toml

[versions]
# --- CORE (always) ---
agp = "9.0.1"                       # Android Gradle Plugin (version of the com.android.* plugins)
kotlin = "2.3.21"
compose-multiplatform = "1.11.0"
material3 = "1.11.0-alpha07"
coroutines = "1.10.1"
serialization = "1.8.0"
androidx-activity = "1.13.0"
# Android SDK centralization
android-compileSdk = "36"
android-minSdk = "29"
android-targetSdk = "36"

# --- DI: Koin (recommended) ---
koin = "4.1.0"
koinCompose = "4.1.0"

# --- Networking: Ktor (optional) ---
ktor = "3.2.3"

# --- Persistence: Room (optional) ---
ksp = "2.3.2"                       # KSP2 has its own version number — never build it from `kotlin`. See note below.
room = "2.7.2"
sqlite = "2.5.2"

# --- Images: Coil (optional) ---
coil = "3.3.0"

# --- Navigation (optional) ---
navigationCompose = "2.9.1"

# --- Permissions (optional) ---
permissions = "0.19.1"

# --- Utils: Date/Time (optional) ---
kotlinDateTime = "0.7.1"

# --- Firebase (optional, requires google-services.json) ---
googleServices = "4.4.3"
crashlytics = "3.0.5"

[libraries]
# --- CORE ---
compose-ui = { module = "org.jetbrains.compose.ui:ui", version.ref = "compose-multiplatform" }
compose-foundation = { module = "org.jetbrains.compose.foundation:foundation", version.ref = "compose-multiplatform" }
compose-material3 = { module = "org.jetbrains.compose.material3:material3", version.ref = "material3" }
compose-runtime = { module = "org.jetbrains.compose.runtime:runtime", version.ref = "compose-multiplatform" }
compose-resources = { module = "org.jetbrains.compose.components:components-resources", version.ref = "compose-multiplatform" }
compose-ui-tooling = { module = "org.jetbrains.compose.ui:ui-tooling", version.ref = "compose-multiplatform" }
compose-ui-tooling-preview = { module = "org.jetbrains.compose.ui:ui-tooling-preview", version.ref = "compose-multiplatform" }
coroutines = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
androidx-activity-compose = { module = "androidx.activity:activity-compose", version.ref = "androidx-activity" }
kotlin-test = { module = "org.jetbrains.kotlin:kotlin-test", version.ref = "kotlin" }

# --- DI: Koin ---
koin-core = { module = "io.insert-koin:koin-core", version.ref = "koin" }
koin-compose = { module = "io.insert-koin:koin-compose", version.ref = "koinCompose" }
koin-compose-viewmodel = { module = "io.insert-koin:koin-compose-viewmodel", version.ref = "koinCompose" }
koin-android = { module = "io.insert-koin:koin-android", version.ref = "koin" }

# --- Networking: Ktor ---
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-client-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
ktor-client-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-logging = { module = "io.ktor:ktor-client-logging", version.ref = "ktor" }
kotlin-serialization = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }

# --- Persistence: Room ---
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
sqlite-bundled = { module = "androidx.sqlite:sqlite-bundled", version.ref = "sqlite" }

# --- Images: Coil ---
coil-compose = { module = "io.coil-kt.coil3:coil-compose", version.ref = "coil" }

# --- Navigation ---
navigation-compose = { module = "org.jetbrains.androidx.navigation:navigation-compose", version.ref = "navigationCompose" }

# --- Permissions ---
moko-permissions = { group = "dev.icerock.moko", name = "permissions", version.ref = "permissions" }

# --- Utils: Date/Time ---
kotlin-date-time = { module = "org.jetbrains.kotlinx:kotlinx-datetime", version.ref = "kotlinDateTime" }

[plugins]
# --- CORE (declared in the ROOT build.gradle.kts with apply false) ---
androidApplication = { id = "com.android.application", version.ref = "agp" }
androidMultiplatformLibrary = { id = "com.android.kotlin.multiplatform.library", version.ref = "agp" }
kotlinMultiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
composeMultiplatform = { id = "org.jetbrains.compose", version.ref = "compose-multiplatform" }
composeCompiler = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }

# --- Persistence: Room (applied ONLY in :shared) ---
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
room = { id = "androidx.room", version.ref = "room" }

# --- Firebase (applied ONLY in :androidApp) ---
googleServices = { id = "com.google.gms.google-services", version.ref = "googleServices" }
firebaseCrashlytics = { id = "com.google.firebase.crashlytics", version.ref = "crashlytics" }
```

> [!IMPORTANT]
> The plugin group comments are not decoration — they encode **where each plugin is applied**. Core plugins go in the root `apply false` block. `ksp`/`room` are applied only in `:shared`. `google-services`/`firebase-crashlytics` are applied only in `:androidApp`. See section 2 and 3.

---

## 2. Base Project (core only)

The base wires **only the core**. Everything else is added via section 3.

### `settings.gradle.kts`

`projects.shared` (type-safe project accessor) requires enabling the feature preview:

```kotlin
rootProject.name = "YourApp"
enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

include(":androidApp")
include(":shared")
```

### Root `build.gradle.kts`

Declare the core plugins once with `apply false` so subprojects share a single classloader.

```kotlin
// build.gradle.kts (root)
plugins {
    alias(libs.plugins.androidApplication) apply false
    alias(libs.plugins.androidMultiplatformLibrary) apply false
    alias(libs.plugins.composeMultiplatform) apply false
    alias(libs.plugins.composeCompiler) apply false
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.serialization) apply false

    // Do NOT add single-module plugins here, even if they exist in the catalog.
    // They are applied in THEIR module, never in the root:
    //   ksp, room                             -> in :shared (only if you use Room)
    //   google-services, firebase-crashlytics -> in :androidApp (only if you use Firebase)
}
```

> [!WARNING]
> **Do not dump every catalog plugin into the root `apply false` block.** The most common mistake when applying this skill is adding `ksp`, `room`, `google-services`, and `firebase-crashlytics` there just because they are defined in the catalog. **They do not belong in the root.** The root declares only the plugins that multiple modules apply (the KMP/Compose/Android core + `serialization`).

```kotlin
// WRONG — the root must NOT list single-module plugins
plugins {
    // ...the six core plugins...
    alias(libs.plugins.ksp) apply false                  // belongs to :shared
    alias(libs.plugins.room) apply false                 // belongs to :shared
    alias(libs.plugins.googleServices) apply false      // belongs to :androidApp
    alias(libs.plugins.firebaseCrashlytics) apply false // belongs to :androidApp
}

// RIGHT — the root carries only the core; ksp/room are applied in :shared,
// google-services/firebase-crashlytics in :androidApp (see section 3).
```

### A. Shared KMP library (`shared/build.gradle.kts`)

The shared module holds the common code, the Android target (`androidLibrary` DSL — **not** `androidTarget`), and the iOS framework export. Below is the **core-only** wiring; add optional groups from section 3.

```kotlin
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidMultiplatformLibrary)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
    alias(libs.plugins.serialization)
    // Room only (see section 3): alias(libs.plugins.ksp) + alias(libs.plugins.room)
}

kotlin {
    // iOS targets + framework export
    listOf(
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "Shared"
            isStatic = true
        }
    }

    // With the KMP library plugin, the Android config lives inside kotlin { androidLibrary { } }
    androidLibrary {
        namespace = "your.package.name.shared"
        compileSdk = libs.versions.android.compileSdk.get().toInt()
        minSdk = libs.versions.android.minSdk.get().toInt()

        compilerOptions {
            jvmTarget = JvmTarget.JVM_17
        }
        androidResources {
            enable = true // required for Compose Multiplatform Res.string / Res.drawable
        }
        withHostTest {
            isIncludeAndroidResources = true
        }
    }

    sourceSets {
        commonMain.dependencies {
            // Core UI
            implementation(libs.compose.ui)
            implementation(libs.compose.foundation)
            implementation(libs.compose.material3)
            implementation(libs.compose.runtime)
            implementation(libs.compose.resources)

            // Core: coroutines
            implementation(libs.coroutines)

            // DI (recommended)
            implementation(libs.koin.core)
            implementation(libs.koin.compose)
            implementation(libs.koin.compose.viewmodel)

            // Optional capabilities (networking, DB, images, nav, permissions) -> section 3
        }
        androidMain.dependencies {
            implementation(libs.compose.ui.tooling.preview)
            implementation(libs.koin.android)
        }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
        }
    }
}
```

### B. Android application module (`androidApp/build.gradle.kts`)

A thin `com.android.application` module that depends on `:shared`. It owns the `applicationId`, versioning, and Android entry point — it must **not** apply `kotlin.multiplatform`.

```kotlin
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
    // Firebase only (see section 3): alias(libs.plugins.googleServices) + alias(libs.plugins.firebaseCrashlytics)
}

kotlin {
    compilerOptions {
        jvmTarget = JvmTarget.JVM_17
    }
}

dependencies {
    implementation(projects.shared)

    implementation(libs.androidx.activity.compose)
    implementation(libs.compose.ui.tooling.preview)
    debugImplementation(libs.compose.ui.tooling)
}

android {
    namespace = "your.package.name"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        applicationId = "your.package.name"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = libs.versions.android.targetSdk.get().toInt()
        versionCode = 1
        versionName = "1.0"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
```

---

## 3. Adding a Capability (additive blocks)

Add only the blocks for capabilities the project actually uses. Each block lists what to add and points to the sibling skill for the real implementation.

### Networking — Ktor

Add to `shared/build.gradle.kts`:

```kotlin
commonMain.dependencies {
    implementation(libs.ktor.client.core)
    implementation(libs.ktor.client.negotiation)
    implementation(libs.ktor.logging)
    implementation(libs.kotlin.serialization)
}
androidMain.dependencies {
    implementation(libs.ktor.client.okhttp)
}
iosMain.dependencies {
    implementation(libs.ktor.client.darwin)
}
```

Deep setup (client factory, bearer auth + refresh, caching, MockEngine testing): **`kmp-expert-ktor`**.

### Persistence — Room

Apply the plugins in `:shared` only:

```kotlin
plugins {
    // ...core plugins...
    alias(libs.plugins.ksp)
    alias(libs.plugins.room)
}
```

Add the dependencies and KSP wiring:

```kotlin
commonMain.dependencies {
    implementation(libs.room.runtime)
    implementation(libs.sqlite.bundled)
}

room {
    schemaDirectory("$projectDir/schemas")
}

dependencies {
    add("kspAndroid", libs.room.compiler)
    add("kspIosX64", libs.room.compiler)
    add("kspIosArm64", libs.room.compiler)
    add("kspIosSimulatorArm64", libs.room.compiler)
}
```

Deep setup (entities, DAOs, `@ConstructedBy`, platform builders): **`kmp-expert-room`**.

### Images — Coil

```kotlin
commonMain.dependencies {
    implementation(libs.coil.compose)
}
```

### Navigation

```kotlin
commonMain.dependencies {
    implementation(libs.navigation.compose)
}
```

Deep setup (type-safe destinations, `Actions` controller): **`kmp-expert-navigation`**.

### Permissions

```kotlin
commonMain.dependencies {
    implementation(libs.moko.permissions)
}
```

### Date/Time

```kotlin
commonMain.dependencies {
    implementation(libs.kotlin.date.time)
}
```

### Firebase / Crashlytics (`:androidApp` only)

Apply the plugins in `androidApp/build.gradle.kts` only — never in the root or in `:shared`:

```kotlin
plugins {
    // ...androidApp plugins...
    alias(libs.plugins.googleServices)
    alias(libs.plugins.firebaseCrashlytics)
}
```

> [!IMPORTANT]
> Firebase requires a `google-services.json` file in the `androidApp` module root (`androidApp/google-services.json`). Do not enable these plugins without it.

---

## Verification

1. Gradle sync with no dependency errors.
2. `./gradlew :shared:assemble :androidApp:assembleDebug` builds cleanly.
3. `./gradlew :shared:linkDebugFrameworkIosSimulatorArm64` links the iOS framework (catches Kotlin/Native issues).
4. If Room was added, a clean build runs KSP without errors.

---

## Best Practices

1. **Catalog is a menu, not a shopping list.** Wire only the capability groups the project needs; the base is core-only.
2. **Root `apply false` = shared-across-modules plugins only.** Single-module plugins are applied in their module (`ksp`/`room` in `:shared`, Firebase in `:androidApp`).
3. **Avoid magic values.** Consume SDK versions via `libs.versions.android.*.get().toInt()`; never hardcode them per module.
4. **camelCase plugin keys.** Prefer catalog keys without dashes for plugins (`androidMultiplatformLibrary`, not `android-multiplatform-library`) to avoid confusing type-safe accessors.
5. **Defer capability depth to the sibling skills.** This skill sets versions and base wiring; `kmp-expert-*` skills implement each capability.
