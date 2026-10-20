# Kotlin Conventions

Conventions for Android apps and Kotlin Multiplatform (KMP) targets built with Jetpack Compose and
Coroutines. Applies to any feature the framework targets at Android or shared Kotlin layers.

## Architecture
ALWAYS follow Clean Architecture layers: Domain → UseCase → Repository → DataSource.
NEVER let domain entities import Android framework classes (`Context`, `Activity`, etc.).
ALWAYS define repository interfaces in the use-case layer, implement in the data layer.
ALWAYS use constructor injection — no service locators or manual `getInstance()` calls outside DI modules.
NEVER use `GlobalScope` — always use a `CoroutineScope` tied to a lifecycle or ViewModel.
ALWAYS use `StateFlow` / `SharedFlow` for UI state — never raw mutable state exposed from ViewModel.

## Project Tooling
- **Build system**: Gradle with Kotlin DSL (`build.gradle.kts`) — no Groovy DSL for new projects.
- **Complexity enforcement**: [`detekt`](https://detekt.dev/) — `ComplexMethod` rule capped at `6`
  (enforces the framework-wide `< 7` cyclomatic complexity budget). Add `detekt.yml` at the repo
  root; treat detekt failures as CI build failures.
- **Formatter / linter**: [`ktlint`](https://pinterest.github.io/ktlint/) — consistent Kotlin
  formatting (Google style guide subset). Run as a Gradle task or pre-commit hook.
- **Static analysis**: detekt (complexity + code smells) + Android Lint (resource and API issues).
- **Build variants**: use Gradle product flavors only when the apps genuinely differ in behavior;
  avoid flavor soup for environment config — use `BuildConfig` fields backed by CI env vars instead.

## File Naming
PascalCase for classes and files; camelCase for functions, properties, and variables; one public
top-level declaration per file; filename matches the public declaration name.

| Purpose | Suffix | Example |
|---|---|---|
| Domain model | `Model.kt` | `UserModel.kt` |
| ViewModel | `ViewModel.kt` | `UserProfileViewModel.kt` |
| Repository interface | `Repository.kt` | `UserRepository.kt` |
| Repository impl | `RepositoryImpl.kt` | `UserRepositoryImpl.kt` |
| Use case | `UseCase.kt` | `FetchUserUseCase.kt` |
| Compose screen | `Screen.kt` | `UserProfileScreen.kt` |
| Data source | `DataSource.kt` | `UserRemoteDataSource.kt` |
| Unit test | `Test.kt` | `UserProfileViewModelTest.kt` |

## Frameworks
- **UI layer**: Jetpack Compose — primary and modern default. XML layouts only for legacy feature
  areas or views not yet expressible in Compose; never mix them in the same screen without a clear
  `AndroidView` boundary.
- **Async**: Kotlin Coroutines + Flow — all async work. Prefer `suspend fun` for one-shot operations,
  `Flow<T>` for streams, `StateFlow<T>` for observable UI state.
- **Dependency injection**: [Hilt](https://dagger.dev/hilt/) for Android apps (Dagger-backed,
  first-party Google support). [Koin](https://insert-koin.io/) for Kotlin Multiplatform targets
  where Hilt isn't available. Constructor injection always — no field injection except where
  Android lifecycle genuinely forces it (legacy `Activity`/`Fragment` injection only).
- **Networking**: [Ktor](https://ktor.io/) for KMP or [Retrofit](https://square.github.io/retrofit/)
  for Android-only; never use raw `HttpURLConnection`.
- **Local persistence**: Room for SQL; DataStore (Proto or Preferences) for lightweight key-value;
  never SharedPreferences for new code.

## Testing & QA Tooling
- **Unit testing framework**: JUnit 5 (`junit-jupiter`) — same framework default as the Java
  conventions (`java-conventions.md`).
- **Mocking**: [`MockK`](https://mockk.io/) — the Kotlin-idiomatic mocking library (`mockk<T>()`,
  `coEvery`, `coVerify`). Prefer MockK over Mockito for any Kotlin codebase; Mockito lacks suspend
  function support without the `mockito-kotlin` bridge.
- **Coroutine testing**: `kotlinx-coroutines-test` — `runTest {}`, `TestCoroutineScheduler`,
  `UnconfinedTestDispatcher`. Never use `runBlocking` in tests — use `runTest`.
- **Android UI testing**: [Espresso](https://developer.android.com/training/testing/espresso) for
  View-based UI; [Compose UI Test](https://developer.android.com/jetpack/compose/testing) for
  Compose screens (`composeTestRule.onNodeWithText(...).performClick()`).
- **Snapshot testing**: [Paparazzi](https://github.com/cashapp/paparazzi) — records and diffs
  Compose and View screenshots without a device or emulator. Pair with visual-qa-engineer.
- **Fake / synthetic data**: [`Faker`](https://github.com/serpro69/kotlin-faker) (`io.github.serpro69:kotlin-faker`)
  — Kotlin-idiomatic wrapper over the Faker pattern, consistent with the Java DataFaker pick in
  `java-conventions.md`. Pair with hand-written builder functions for domain-object construction.
- **Factories**: hand-written `build*()` factory functions or `Builder` classes per domain type —
  same preference as Go conventions. [InstancioKotlin](https://www.instancio.org/kotlin/) is an
  option for large object graphs.
- **Mutation testing** (ADR-008 clause 2): PIT (`pitest`), through its Gradle plugin — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: Android Macrobenchmark for app startup and scroll jank; k6 for any
  backend service the Android app calls.
- **Reporting**: JUnit XML output via `junit-platform-reporting`; feed into CI reporting aggregator
  (same pipeline as `java-conventions.md`).

## Quick Reference

```kotlin
// Complexity: < 7 — enforce with detekt ComplexMethod capped at 6
// File naming: PascalCase classes/files, camelCase functions/props, one public decl per file
// Architecture: Domain / UseCase / Repository / DataSource — no Android imports in domain
// Async: Coroutines + Flow; StateFlow for UI state; runTest in tests (never runBlocking)
// DI: Hilt (Android) or Koin (KMP); constructor injection always
// UI: Jetpack Compose; XML layouts legacy only
// Mocking: MockK (not Mockito)
// Snapshot: Paparazzi
// Complexity tool: detekt ComplexMethod capped at 6
```

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
