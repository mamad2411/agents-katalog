---
name: kotlin-master
description: Use when writing, reviewing, debugging, or explaining Kotlin, Kotlin/JVM, Android apps, Jetpack Compose UI, Material 3, coroutines, Flow, StateFlow, SharedFlow, ViewModel, lifecycle-aware collection, Room, DataStore, WorkManager, Hilt, Koin, Navigation Compose, type-safe routes, SavedStateHandle, Paging 3, RemoteMediator, Retrofit, Ktor, kotlinx.serialization, OkHttp, Coil, Kotlin Multiplatform, K2 compiler, Kotlin 2.x features, context parameters, context receivers, Gradle Kotlin DSL, build.gradle.kts, libs.versions.toml, version catalogs, KSP, KAPT, Compose compiler plugin, Compose BOM, AGP, minSdk, targetSdk, compileSdk, namespace, applicationId, permissions, ActivityResultContracts, foreground services, edge-to-edge, predictive back, R8, ProGuard, app signing, Play Store release, Android Keystore, Network Security Config, testing, or modern Android architecture choices may affect correctness.
---

# Kotlin Master

Use this skill for modern Kotlin work. For Android, assume Kotlin-first and Compose-first defaults unless the user explicitly asks for legacy Views or Java interop.

## 1. When to use this skill

- Use it any time you write or review Kotlin.
- Use it any time Android, Jetpack Compose, coroutines, Flow, or Gradle Kotlin DSL are involved.
- Use it any time the task mentions `build.gradle.kts`, `libs.versions.toml`, Room, DataStore, Hilt, WorkManager, or Kotlin Multiplatform.
- Use it any time nullability, sealed types, state management, or lifecycle-aware async behavior matters.

## 2. First classify the target

- State the target before giving advice:
  - plain Kotlin/JVM
  - Android app
  - Jetpack Compose screen
  - Kotlin Multiplatform
  - Gradle/build configuration
- Do not blur Kotlin language advice, Android framework rules, and Compose runtime rules together.
- For modern Android, prefer Kotlin + Jetpack Compose + `ViewModel` + `StateFlow` as the default stack.

## 3. Kotlin language rules

- Prefer `val` over `var`.
- Prefer immutable models and read-only collection types at API boundaries.
- Use `data class` for value/state models.
- Use `sealed class` or `sealed interface` for closed result or UI state hierarchies.
- Use `enum class` only for fixed constants, not for rich state with different payloads.
- Use nullable types only when absence is a real state.
- Avoid `!!`. Fix the model, validate the boundary, or use `requireNotNull`, safe calls, and Elvis defaults.
- Keep scope functions readable:
  - `let` for nullable transforms
  - `apply` for object configuration
  - `also` for side effects
  - `run` for compute-and-return
- Do not stack nested scope functions just to look concise.
- Prefer top-level functions only when they are actually cohesive with the package.

## 4. Kotlin version-sensitive rules

- Treat Kotlin version as important. Check whether the project uses Kotlin 1.x, Kotlin 2.0+, or newer Kotlin 2.x before changing compiler or build syntax.
- Kotlin 2.0+ uses the K2 compiler by default in modern tooling.
- Do not suggest old context receivers for new code. Prefer context parameters only when the project Kotlin version supports them and the team intentionally uses them.
- Do not use experimental Kotlin features unless the project already opts into them or the user explicitly asks.
- For Java interop, watch platform types, nullability annotations, SAM conversions, and whether `@JvmStatic`, `@JvmOverloads`, `@JvmInline`, or `@Serializable` is actually needed.

## 5. Coroutines and Flow rules

- Use `suspend` for asynchronous work.
- Use structured concurrency. Prefer `viewModelScope`, `lifecycleScope`, or an injected scope with a real owner.
- Never use `GlobalScope` in app code.
- Re-throw `CancellationException`. Do not hide coroutine cancellation inside broad `catch` blocks.
- Use `StateFlow` for current UI state.
- Use `SharedFlow` for broadcast-like or event-style streams when a single current state value is not the model.
- Use plain `Flow` for reactive data streams that do not need an always-current state holder.
- Use `collectLatest` when stale in-flight work should be cancelled by new values.
- Do not block the main thread. Move I/O and heavy computation out of UI code.

## 6. Modern Android and Compose rules

- For modern Android, prefer Jetpack Compose over XML/View patterns unless legacy code requires otherwise.
- Keep composables pure, cheap, and side-effect free except through Compose effect APIs.
- Do not run network, database, or repository writes directly inside a composable body.
- Let `ViewModel` own screen state and expose immutable UI state.
- Model screen state explicitly with immutable `data class` or sealed UI state types.
- Use unidirectional data flow: state down, events up.
- Collect flows in Compose with `collectAsStateWithLifecycle()` on Android.
- Hoist state when a composable should be reusable or testable.
- Use:
  - `remember` for composition-local caching
  - `rememberSaveable` for state that should survive recreation
  - `derivedStateOf` for derived UI state that would otherwise recompose too often
- In `LazyColumn` and related lazy containers, provide stable keys.
- Do not write to state after reading it in the same composable path in a way that creates recomposition loops.
- Prefer Material 3 when the project is using modern Jetpack Compose UI unless the design system says otherwise.

## 7. Architecture defaults

- Default to UI layer + data layer.
- Add a domain/use-case layer only when business logic is complex, reused, or worth isolating.
- Keep repositories as the source of truth boundary between local and remote data.
- For offline-first Android apps, prefer local persistence as the observable source of truth and sync remote data through the repository.
- Prefer Room for structured local data.
- Prefer DataStore over SharedPreferences for new preference storage.
- Prefer WorkManager for guaranteed deferrable background work.
- Hilt is the safest Android default for DI. If the project already uses Koin or manual DI, follow the existing pattern unless there is a real reason to change it.
- For list-heavy or network-paged screens, prefer Paging 3 and use `RemoteMediator` only when the app truly needs coordinated network-plus-database paging.

## 8. Gradle and build rules

- Prefer Gradle Kotlin DSL (`build.gradle.kts`) for modern Kotlin and Android projects.
- Prefer version catalogs in `libs.versions.toml` instead of scattering version strings across modules.
- Do not paste Groovy DSL snippets into Kotlin DSL.
- For modern Kotlin Gradle configuration, prefer `compilerOptions {}` over stale `kotlinOptions {}` guidance.
- Be explicit about whether advice is for:
  - Android Gradle Plugin
  - Kotlin Gradle plugin
  - Compose compiler/plugin
  - plain Gradle
- Do not guess version compatibility across Kotlin, AGP, Compose, and libraries. Verify when version-specific behavior matters.

## 9. Compose build setup rules

- For Kotlin 2.0+, use the Compose Compiler Gradle plugin: `org.jetbrains.kotlin.plugin.compose`.
- Do not add old `androidx.compose.compiler:compiler` manually for Kotlin 2.0+ projects.
- Prefer the Compose BOM for Compose library versions.
- Keep Kotlin plugin, Compose compiler plugin, AGP, Gradle, and JDK compatibility aligned.

## 10. Code generation rules

- Prefer KSP for Room and other Kotlin-native processors when supported.
- Use KAPT only when the dependency still requires it.
- Do not mix `kapt` and `ksp` for the same processor without a reason.
- If Hilt, Room, or other generated code fails, check whether the project is using KSP or KAPT before changing dependencies.

## 11. Android build, platform, and release rules

- Check `compileSdk`, `targetSdk`, `minSdk`, AGP, Gradle, Kotlin, JDK, and Compose compiler setup before giving version-sensitive fixes.
- For Android 15 and 16+, account for edge-to-edge, predictive back, foreground service limits, notification and runtime permissions, and large-screen behavior changes.
- For Android 16/API 36+, do not assume the app can opt out of edge-to-edge.
- Prefer Activity Result APIs and `ActivityResultContracts` for permission and external activity flows.
- Be careful with foreground service types, background work limits, exact alarms, and health or runtime permission changes.
- Use `applicationId` for app identity and `namespace` for generated code and package namespace. Do not confuse them.
- Enable R8 and release minification unless there is a strong reason not to.
- Never hardcode secrets. Use build-time injection, backend-owned secrets, Android Keystore, and Network Security Config where appropriate.

## 12. Navigation rules

- Prefer type-safe Navigation Compose routes when the project supports them.
- Do not pass large objects through navigation arguments. Pass IDs and reload from the data layer.
- Use `SavedStateHandle` for process-death-safe ViewModel arguments and state that belongs in business logic.
- Keep navigation events at screen or route boundaries, not buried inside leaf composables.

## 13. Persistence rules

- Use Room migrations for schema changes. Do not casually use destructive migration in production guidance.
- Keep Room entities separate from domain models when the app is non-trivial.
- Use transactions for multi-step database writes.
- DataStore must be a singleton per file and process. Do not create multiple DataStore instances for the same file.
- Keep DataStore and Room access in the data layer, not inside composables.
- If the stack uses Retrofit, Ktor, OkHttp, kotlinx.serialization, or Coil, keep serialization, networking, caching, and image loading choices consistent with the existing project.

## 14. Security and release rules

- Never hardcode API keys or secrets in source code.
- Do not store tokens or passwords in plain DataStore, SharedPreferences, or Room.
- Use Android Keystore or other vetted storage patterns for sensitive secrets.
- Use Network Security Config deliberately; avoid allowing cleartext traffic in release guidance.
- Include app signing, Play App Signing, privacy policy, permissions review, and release build verification in production advice.

## 15. Testing and quality rules

- Test coroutines with `runTest`.
- Use `MainDispatcherRule`, `StandardTestDispatcher`, and `UnconfinedTestDispatcher` intentionally.
- Prefer fake repositories over mocking every dependency boundary.
- Use Turbine for Flow testing when available.
- Test Flow behavior directly instead of only testing final UI snapshots.
- For Compose UI, use semantics-driven UI tests.
- Use Robolectric for JVM Android tests when it fits the test boundary better than instrumentation.
- Use Macrobenchmark and Baseline Profile tests for startup or performance-sensitive apps.
- Keep mutable implementation details private and public state immutable.
- Prefer explicit loading, empty, success, and error states over boolean flag soup.

## 16. Performance and platform rules

- Keep expensive transforms out of composable bodies.
- Cache derived UI work with `remember` or compute it in the `ViewModel`.
- Use Baseline Profiles for startup-sensitive Android apps.
- Use lifecycle-aware collection to avoid leaks and wasted background work.
- Avoid passing `Activity` or `View` context into long-lived singletons or `ViewModel`s.
- Ask for Android permissions late and only when genuinely needed.

## 17. AI mistake checklist

Before giving Kotlin or Android guidance, check for these failures:

- Java/XML/View-era Android patterns suggested for a Compose-first task
- business logic or network access placed inside composables
- old or experimental Kotlin syntax suggested without checking the Kotlin version
- `GlobalScope` used instead of structured scopes
- `!!` used to silence nullability problems
- `MutableStateFlow` exposed publicly instead of `StateFlow`
- `collect` or `collectAsState` used without lifecycle awareness on Android when `collectAsStateWithLifecycle()` is the safer default
- `SharedPreferences` suggested as the default for new code
- Groovy Gradle syntax pasted into `build.gradle.kts`
- old Compose compiler setup suggested for Kotlin 2.0+ projects
- KAPT added blindly when KSP is the right fit
- versions hardcoded everywhere instead of using `libs.versions.toml`
- `applicationId` and `namespace` confused
- Room destructive migration suggested casually
- large navigation arguments passed instead of IDs plus reload
- loading/error/empty states ignored
- missing lazy list keys or expensive recomposition work in Compose
- edge-to-edge, predictive back, foreground service, or permission changes ignored on modern Android
- release/security guidance given without R8, signing, or secret-storage checks
- broad exception handling that swallows `CancellationException`

## 18. Output style for future agents

- State the target stack first.
- If the answer is Android-specific, say so explicitly.
- If the answer is Compose-specific, say so explicitly.
- Prefer copyable Kotlin examples over abstract explanation.
- Separate language advice from framework advice.
- When version-sensitive behavior matters, name the exact Kotlin, Android, or Gradle surface that needs verification.
