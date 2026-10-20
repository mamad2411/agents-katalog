---
name: mobile-android-native
description: Native Android development with Kotlin and Jetpack Compose. Use when building, reviewing, or refactoring Android apps targeting modern Android (API 24+), including Compose UI, Architecture Components, coroutines/Flow, Hilt DI, Room, WorkManager, and Material 3.
source: self
---

# Mobile Android Native

Modern, production-grade Android engineering with Kotlin, Jetpack Compose, and the AndroidX/Jetpack stack.

## When to Use

- Building or reviewing native Android apps (Kotlin + Jetpack Compose)
- Migrating from XML Views to Compose, or LiveData/RxJava to Coroutines/Flow
- Designing Android-specific architecture (lifecycle, process death, configuration changes)
- Integrating background work, notifications, deep links, or platform APIs (camera, location, BLE)
- Reviewing Gradle, R8/ProGuard, baseline profiles, or app size/startup performance

## Toolchain Defaults

- Language: Kotlin (latest stable), `jvmTarget = 17`
- UI: Jetpack Compose + Material 3 (`androidx.compose.material3`)
- Min SDK: 24 (lower only with explicit reason); Target/Compile SDK: latest stable
- Build: AGP latest stable, Gradle Kotlin DSL, version catalogs (`libs.versions.toml`)
- DI: Hilt; Async: Coroutines + Flow; Persistence: Room; Network: Retrofit + OkHttp + kotlinx.serialization
- Navigation: Jetpack Navigation Compose (or Compose Navigation 3 / Decompose where justified)
- Background: WorkManager for deferrable work; Foreground Services only when required
- Image loading: Coil; JSON: kotlinx.serialization (avoid Gson)
- Testing: JUnit5/Kotest, MockK, Turbine, Compose UI Test, Espresso, Robolectric, Macrobenchmark

## Architecture Rules

1. Single-activity app; screens are `@Composable` functions hosted by a NavHost.
2. Use unidirectional data flow: `ViewModel` exposes `StateFlow<UiState>`; UI sends events upward.
3. Layer the app: `ui` → `domain` (use cases, pure Kotlin) → `data` (repositories, sources). No Android types in `domain`.
4. Survive configuration changes and process death via `ViewModel` + `SavedStateHandle`. Do not store UI state in singletons.
5. Scope coroutines correctly: `viewModelScope` for UI work, `WorkManager` for background, `lifecycleScope` only in UI layer.
6. Inject dispatchers (`@IoDispatcher`, `@DefaultDispatcher`) — never hard-code `Dispatchers.IO` in business logic.
7. Treat `Context` like a scoped resource; never hold `Activity`/`View` references in `ViewModel` or singletons.

## Compose Rules

- Hoist state: composables receive state and lambdas; they do not own mutable business state.
- Read state at the lowest level that needs it to keep recomposition scopes small.
- Use `remember`, `rememberSaveable`, and `derivedStateOf` deliberately; avoid recreating heavy objects per recomposition.
- Prefer `LazyColumn`/`LazyRow` with stable `key`s and `contentType` for heterogeneous lists.
- Use `Modifier` order intentionally; pass `Modifier` as first optional param and don't capture it in closures.
- Avoid `MutableState` of large collections; use immutable lists or `SnapshotStateList` only when needed.
- Side effects: `LaunchedEffect`, `DisposableEffect`, `produceState`, `snapshotFlow` — never launch coroutines from composition directly.
- Theming via Material 3 `MaterialTheme` with dynamic color on Android 12+; respect dark theme and large fonts.

## Concurrency & Data

- Cold streams (`Flow`) for data; `StateFlow`/`SharedFlow` for hot UI state and events.
- Collect with `collectAsStateWithLifecycle()` in Compose to avoid wasted work in background.
- Cancellation is cooperative: respect `ensureActive()` and structured concurrency boundaries.
- Room: suspend DAOs and `Flow` queries; never run DB work on `Dispatchers.Main`.
- Network: Retrofit suspend functions; map errors to a sealed `Result`/`DomainError` at the repository boundary.

## Performance

- Measure first with Macrobenchmark, Android Studio Profiler, and `systrace`/Perfetto.
- Ship a Baseline Profile and (when valuable) a Startup Profile; keep them updated in CI.
- Cold start budget: < 500ms TTID on mid-range devices; defer non-critical init out of `Application.onCreate`.
- Enable R8 full mode and resource shrinking for release builds; verify with APK Analyzer.
- Avoid jank: keep frames < 16ms (or < 8ms on 120Hz); use `reportFullyDrawn()` for accurate startup metrics.
- Image pipeline: request correctly sized images, use Coil's memory and disk caches, avoid bitmap allocations on the main thread.

## Security

- Never log PII or secrets; strip with R8 rules in release.
- Use EncryptedSharedPreferences / DataStore with Tink for at-rest secrets; Keystore-backed keys.
- Network: TLS only, certificate pinning for sensitive endpoints, `cleartextTrafficPermitted="false"`.
- Validate all deep link inputs; require `android:exported` to be explicit.
- Follow least-privilege permissions; request runtime permissions just-in-time with rationale.
- Avoid `WebView` JavaScript bridges; if required, restrict with allowlists and disable file access.

## Testing

- Unit-test ViewModels and use cases with `runTest`, fake repositories, and Turbine for Flows.
- Compose UI tests with `createComposeRule()`; prefer semantic matchers (`onNodeWithContentDescription`).
- Use Hilt test modules to swap dependencies; avoid Robolectric for pure-Kotlin logic.
- Add Macrobenchmark tests for startup and key user journeys; gate regressions in CI.

## Release & Distribution

- Publish as Android App Bundle (`.aab`); enable Play Asset Delivery for large assets.
- Sign with Play App Signing; keep upload key in a secure secret store.
- Use Play Console internal/closed/open tracks; staged rollouts with halt thresholds.
- Track crashes (Crashlytics or Sentry), ANRs, and Play vitals; tie alerts to release tracks.

## Anti-Patterns

- AsyncTask, Loaders, or Handler-based threading in new code
- LiveData in new Compose screens (prefer `StateFlow` + `collectAsStateWithLifecycle`)
- `GlobalScope.launch` or hard-coded `Dispatchers.IO` inside use cases
- Holding `Context`, `Activity`, or `View` in singletons or ViewModels
- Storing tokens in plain `SharedPreferences`
- Building release APKs without R8/shrinking, or without a baseline profile when feasible
- Putting business logic inside composables or fragments
- Using `runBlocking` outside tests or `main()` entry points

## Review Checklist

- [ ] Min/Target SDK and AGP/Kotlin/Compose versions are aligned and current
- [ ] Single-activity + Compose Navigation; no leaked `Context`
- [ ] UDF: `ViewModel` exposes immutable `UiState`; events go up
- [ ] Coroutines use injected dispatchers and structured scopes
- [ ] Lists use stable keys, `contentType`, and `collectAsStateWithLifecycle`
- [ ] Release build is R8-shrunk with a baseline profile
- [ ] Permissions are minimized, runtime-requested, and rationale-backed
- [ ] Crash, ANR, and startup metrics are monitored with alerts
