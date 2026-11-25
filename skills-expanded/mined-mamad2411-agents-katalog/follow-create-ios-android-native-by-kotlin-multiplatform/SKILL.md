---
name: follow-create-ios-android-native-by-kotlin-multiplatform
description: Build one native iOS+Android app with Kotlin Multiplatform and Compose Multiplatform
argument-hint: "[project-name]"
related:
  - follow-create-web
  - follow-lang-kotlin
  - deep-review-codebase
  - follow-create-mobile
  - follow-create-mobile-cross-with-capacitor
  - ask-me
---

## Goal

Build a native mobile app for iOS and Android from a single Kotlin codebase using Kotlin Multiplatform (KMP) and Compose Multiplatform per best practices — business logic, networking, storage, and UI are maximally shared through the `shared` module

## Scope

- Use to create a new iOS+Android app that needs native performance + shared Kotlin code (instead of maintaining separate Swift+Kotlin teams)
- Covers setup, project structure (KMP modules), Compose Multiplatform UI, expect/actual, build, test, and deploy to both stores
- Use Android Studio as the primary IDE (Xcode is required for the iOS target — macOS only)

- Packages: Kotlin, KMP plugin, Compose Multiplatform, AGP, Gradle — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file, per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest KMP, Compose Multiplatform, Kotlin, and AGP versions and breaking changes, then run `/deep-review-codebase` to summarize the tech stack
2. Record the rationale for choosing KMP over separate native codebases or Capacitor for future reference

### 2. Gather Requirements

> Goal: understand the app scope

1. Collect project name, package name (e.g. `com.example.app`), min SDK (Android), and deployment target (iOS)
2. Define features, screens, and navigation pattern
3. Define shared vs platform-specific code: networking (Ktor), storage (SQLDelight/DataStore), DI (Koin)
4. Decide between shared UI (Compose Multiplatform on both platforms) or shared logic only (iOS uses SwiftUI wrapping the `shared` module)
5. If anything is unclear → use `/ask-me`

### 3. Verify Environment

> Goal: check the environment before building

1. Verify the latest Android Studio version that supports KMP (check with `/deep-research` — minimum Otter 2025.2.1)
2. Verify JDK 21 or newer and the Kotlin Multiplatform plugin in Android Studio
3. For the iOS target: verify Xcode >= 26.0 (macOS only — Windows can build Android/desktop targets only)
4. Verify `kdoctor` (`brew install kdoctor` or `scoop install kdoctor`) — run `kdoctor` to confirm the environment is complete

### 4. Create Project

> Goal: create the KMP project with the right template

1. Use the Kotlin Multiplatform Wizard (`kmp.jetbrains.com`) or Android Studio > New Project > Kotlin Multiplatform App
2. Choose shared UI (Compose Multiplatform) or shared logic only per step 2.4
3. Set the package name and minimum versions: Android minSdk >= 24, iOS >= 15
4. Configure Gradle to use Kotlin DSL (`build.gradle.kts`) + a version catalog (`libs.versions.toml`)

### 5. Configure Modules

> Goal: organize module structure per KMP conventions

1. Standard structure:
   ```text
   shared/          # KMP module — commonMain, androidMain, iosMain
   androidApp/      # Android entry (Jetpack Compose host)
   iosApp/          # Xcode project — SwiftUI host or Compose Multiplatform view
   ```
2. `shared/build.gradle.kts`: set `kotlin { androidTarget(); iosX64(); iosArm64(); iosSimulatorArm64() }` and the `commonMain`/`androidMain`/`iosMain` source sets
3. Enable the Compose Multiplatform plugins `org.jetbrains.compose` + `org.jetbrains.kotlin.plugin.compose` (the Compose Compiler ships with Kotlin since 2.0 — don't set an extension version yourself)
4. Use `libs.versions.toml` for the version catalog

### 6. Setup Shared Architecture

> Goal: structure the shared module per Clean Architecture

1. Keep in `commonMain`: `data/` (repositories, DTOs, Ktor client), `domain/` (use cases, models, repository interfaces), `presentation/` (ViewModels, screens)
2. Keep only platform implementations in `androidMain`/`iosMain` via `expect`/`actual` (e.g. `expect fun platform(): String`)
3. Use `follow-lang-kotlin` for conventions
4. Networking → `io.ktor:ktor-client-*` (engine: `darwin` on iOS, `okhttp`/`cio` on Android)
5. Storage → `app.cash.sqldelight` (SQL) or `androidx.datastore` via a multiplatform adapter
6. DI → `io.insert-koin:koin-core` (KMP-ready)

### 7. Implement Shared UI

> Goal: build the UI with Compose Multiplatform in commonMain

1. Create `App.kt` in `commonMain` — the shared composable entry
2. Use Material 3 components from `org.jetbrains.compose.material3` (KMP)
3. Navigation → `org.jetbrains.androidx.navigation:navigation-compose` (Navigation 3 multiplatform)
4. Resources → the `compose-multiplatform` resources API (`Res.drawable`, `Res.string`) under `commonMain/composeResources`
5. Android host: `MainActivity` calls `setContent { App() }`; iOS host: `ComposeViewController()` or SwiftUI + shared ViewModels

### 8. Platform-Specific Wiring

> Goal: wire the shared module into the host apps correctly

1. iOS: use `ComposeUIViewController { App() }` in `MainViewController.kt` (iosMain), or export `shared` as a framework for SwiftUI to call via `SharedModuleKt`/`skie`
2. Android: `MainActivity` in `androidApp` calls `App()` from `shared` directly
3. Use `expect`/`actual` for platform APIs: file system, keychain/keystore, notifications, permissions
4. Set iOS capabilities/signing in the Xcode project (push, app groups, keychain sharing)

### 9. Testing And Build

> Goal: verify correctness and produce release builds

1. Unit tests in `commonTest` with `kotlin.test`; platform tests in `androidTest`/`iosTest`
2. Run `./gradlew :shared:testDebugUnitTest` (Android side) and run iOS tests through Xcode
3. Android release: `./gradlew :androidApp:assembleRelease` → AAB → Play Console/`fastlane supply`
4. iOS release: archive through Xcode → App Store Connect/TestFlight (Xcode >= 26 only since Apr 2026)
5. Never commit keystore/provisioning secrets — use env vars

### 10. Validate And Ship

> Goal: check quality before delivery

1. Run `/deep-review-codebase` to check UI/UX and architecture
2. Run `/run-test` for the test suite
3. Run `/follow-lang-kotlin` to verify conventions
4. Run `/ship`

## Rules

### 1. Kotlin Multiplatform

- Shared code lives in `commonMain` only — platform code via `expect`/`actual` only when necessary
- Use KMP-compatible libraries only (Ktor, SQLDelight, Koin, Kotlinx.*) — JVM-only libs must never be in `commonMain`
- Use Compose Multiplatform for shared UI — if iOS needs SwiftUI, share only `domain`/`data` + ViewModels

### 2. Architecture

- Use Clean Architecture — `domain` must not depend on platform/framework
- ViewModels use `androidx.lifecycle` multiplatform (KMP-ready)
- Repository pattern for the data layer

### 3. Security

- Never hardcode secrets — use Keychain on iOS and Keystore/EncryptedSharedPreferences on Android via `expect`/`actual`
- HTTPS only; ATS compliance on iOS, `usesCleartextTraffic="false"` on Android

### 4. Build

- Android: minSdk >= 24, targetSdk/compileSdk >= 36
- iOS: deployment target >= 15; Xcode >= 26 (App Store Connect requirement)
- Use a version catalog; the latest Gradle wrapper supported by AGP/Kotlin (check the matrix with `/deep-research`)

- Use /follow-create-web if needed
- Use /follow-create-mobile-cross-with-capacitor if the requirements fit a web stack better than native

## Expected Outcome

- The KMP project runs on both iOS and Android from a shared Kotlin codebase
- Clear Clean Architecture; maximal shared logic/UI, with platform code isolated in the right places
- Tests, navigation, DI, storage, and networking complete
- Release builds ready for the Play Store and App Store
