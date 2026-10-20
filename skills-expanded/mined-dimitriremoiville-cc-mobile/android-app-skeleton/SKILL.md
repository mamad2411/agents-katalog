---
name: android-app-skeleton
description: Load when scaffolding a brand-new Android app from scratch (Kotlin + Jetpack Compose + Hilt + Clean Architecture). Authoritative blueprint used by /init-android-app — placeholder list, feature-flag block, layout, execution order, hard rules, and post-scaffold checklist. File templates live in `references/` and are loaded step-by-step (progressive disclosure).
---

# Android app skeleton

This file is the **procedure**. The actual file templates live in sibling files under `references/` — each execution-order step points at the reference it needs. Read the spine end-to-end first, then load each referenced file when its step runs. Substitute placeholders before writing.

Follow templates verbatim — the whole point of the skeleton is reproducibility. The only acceptable divergence is a documented AGP-version delta (see "Escape hatch: AGP 8.x" in `references/root-files.md`). If you find yourself improvising more than that, stop and surface what you're seeing instead.

**Target floor: AGP 9 / Kotlin 2.2 / JDK 17.** Older toolchains (AGP 8.x) require the deltas listed in the escape-hatch callout. Don't silently retarget — fail loudly if the resolved versions disagree with the floor table.

## Placeholders

| Placeholder | Meaning | Example |
|---|---|---|
| `{{APP_NAME}}` | Gradle project folder name, lowercase kebab or snake | `my_app` |
| `{{APP_CLASS}}` | `Application` subclass name in PascalCase | `MyApp` |
| `{{PACKAGE_ID}}` | applicationId / root package | `com.example.myapp` |
| `{{PACKAGE_PATH}}` | slash form of package id | `com/example/myapp` |
| `{{APP_DISPLAY_NAME}}` | Human-facing name | `My App` |
| `{{API_BASE_URL_DEV}}` | Dev-flavor API base URL (trailing slash required by Retrofit) | `https://api.dev.example.com/` |
| `{{API_BASE_URL_PROD}}` | Prod-flavor API base URL (trailing slash required by Retrofit) | `https://api.example.com/` |

## Feature flags

| Flag | Adds |
|---|---|
| `INCLUDE_ROOM` | Room module + entities/DAO/DB, migration skeleton, schema export |
| `INCLUDE_DATASTORE` | DataStore module + typed prefs |
| `INCLUDE_FIREBASE` | google-services plugin + Crashlytics + Analytics init |

## Layout

Single Gradle module, `:app`. **Feature-first** package layout — each feature is a top-level package containing the layers it actually needs (`ui/`, `domain/`, `data/`). Cross-feature plumbing lives under `core/`. This matches `android-architecture` and is what `/new-feature` and `/add-screen` produce.

```
app/src/main/java/{{PACKAGE_PATH}}/
├── {{APP_CLASS}}.kt                  # Application
├── MainActivity.kt                   # single Activity host
├── core/                             # cross-feature plumbing
│   ├── domain/                       # Outcome, DomainError, analytics interface (framework-free)
│   ├── data/                         # networking + analytics impls (knows frameworks)
│   ├── ui/theme/                     # AppTheme, color schemes
│   └── navigation/                   # AppNavGraph (top-level routes)
├── home/ui/                          # the bottom-nav shell feature (no data/domain — pure UI)
├── feed/                             # tab feature, full feature-first shape
│   ├── data/{repository,di}/
│   ├── domain/{model,repository,usecase}/
│   └── ui/                           # UiState, ViewModel, Screen, Route
└── profile/                          # tab feature, full feature-first shape
    ├── data/{repository,di}/
    ├── domain/{model,repository,usecase}/
    └── ui/                           # UiState, ViewModel, Screen, Route
```

Each new feature added later mirrors `feed/` and `profile/` — `<feature>/{ui,domain,data}/` with only the layers it needs. The shell feature (`home/`) knows about its tab features; tab features don't know about each other. Feed and Profile in the scaffold each ship the full three-layer shape so the result lines up with what `/new-feature` and `/add-screen` produce — no special-casing the first two tabs.

Why feature-first inside a single module?
- **Code locality.** Everything for a screen — UI, state, repository, mapping — lives next to itself. New contributors find code by feature name, not by guessing which `data/` subfolder.
- **Refactor pressure.** When a feature outgrows the package, promoting it to a `:feature:<name>` Gradle module is mechanical. Layer-first packages don't promote cleanly.
- **Single-module tax stays low.** No extra `build.gradle.kts`, no `project(":core:*")` wiring, no slower first build until you actually want module-level isolation. See `android-architecture/SKILL.md` → "Module or package?".

## Reference files

Templates live alongside this spine. Load each one when its step runs:

| File | Contains | Loaded at step |
|---|---|---|
| [`references/root-files.md`](references/root-files.md) | `settings.gradle.kts`, root `build.gradle.kts`, `gradle.properties`, daemon JVM, `libs.versions.toml`, compatibility-traps table, AGP-8.x escape hatch | 2 |
| [`references/app-module.md`](references/app-module.md) | `app/build.gradle.kts`, proguard, manifest, strings, themes, `{{APP_CLASS}}`, `MainActivity`, `AppTheme`, `AppNavGraph`, `HomeViewModel`, `HomeScreen` | 3, 4, 7, 8 |
| [`references/core-domain.md`](references/core-domain.md) | `Outcome`, `DomainError`, `OutcomeMapTest`, `AnalyticsTracker` interface, `AnalyticsEvent` sealed taxonomy | 5 |
| [`references/core-data.md`](references/core-data.md) | `SampleApi`, `Outcomes.kt` (`toOutcome`/`toDomainError`), `RemoteDataSource`, `NetworkModule`, `NoopAnalyticsTracker`, `FirebaseAnalyticsTracker`, `AnalyticsModule` (both variants), canonical screen-viewed pattern | 6 |
| [`references/feed-feature.md`](references/feed-feature.md) | Feed feature in full three-layer shape — model, repository (interface + impl), use case, DI module, `FeedUiState`, `FeedRoute`, `FeedViewModel`, `FeedScreen` + previews | 8 |
| [`references/profile-feature.md`](references/profile-feature.md) | Profile feature in full three-layer shape, including `AsyncImage` (Coil 3) wiring | 8 |
| [`references/tests.md`](references/tests.md) | `FeedViewModelTest`, `ProfileViewModelTest`, `FeedScreenTest`, `ProfileScreenTest` | 9 |
| [`references/optional-room.md`](references/optional-room.md) | `INCLUDE_ROOM`: `AppDatabase`, `SampleEntity`, `SampleDao`, `PersistenceModule`, schema-export Gradle snippet | 6 (only if flag on) |
| [`references/optional-datastore.md`](references/optional-datastore.md) | `INCLUDE_DATASTORE`: `AppPreferences`, `DataStoreModule` | 6 (only if flag on) |
| [`references/optional-firebase.md`](references/optional-firebase.md) | `INCLUDE_FIREBASE`: Firebase auto-init notes, per-flavor `google-services.json` drop | 11 (only if flag on) |

When the procedure below names a file, the bracketed reference tells you where its template lives.

## Execution order

1. Create directory `{{APP_NAME}}/` with Gradle wrapper.
2. Write `settings.gradle.kts`, root `build.gradle.kts`, `gradle.properties`, `gradle/libs.versions.toml` — templates in `references/root-files.md`.
3. Write `app/build.gradle.kts` (single module — it carries all runtime deps) — template in `references/app-module.md`.
4. Write `AndroidManifest.xml`, `strings.xml` (with tab labels), themes, launcher icons — templates in `references/app-module.md`.
5. Write `core/domain/` — `Outcome`, `DomainError`, **`analytics/AnalyticsTracker` interface + `AnalyticsEvent` sealed taxonomy** (always emitted; the analytics interface is part of the domain so use cases / VMs depend on the abstraction even when Firebase is absent). Templates in `references/core-domain.md`.
6. Write `core/data/` — sample API + `RemoteDataSource`, **`Outcomes.kt` (canonical `Result<T>.toOutcome(...)` adapter + `toDomainError(...)` mapper)**, **`network/di/NetworkModule.kt` (Hilt providers for `OkHttpClient`, `Json`, `Retrofit`, `SampleApi` — DEBUG-gated logging; one source of truth for the HTTP stack so Coil reuses the same client)**, **`analytics/` module wiring `AnalyticsTracker` to `NoopAnalyticsTracker` (always) or `FirebaseAnalyticsTracker` (`INCLUDE_FIREBASE`)**. Add `core/data/persistence/` (template in `references/optional-room.md`) + `core/data/datastore/` (template in `references/optional-datastore.md`) — each with their own DI modules — behind their flags. Core-data templates in `references/core-data.md`.
7. Write `core/ui/theme/AppTheme.kt` and `core/navigation/AppNavGraph.kt` (top-level nav with `Home` as start destination) — templates in `references/app-module.md`.
8. Write the features — `{{APP_CLASS}}` Application (Hilt + `SingletonImageLoader.Factory` for Coil), `MainActivity`, **`home/ui/{HomeScreen,HomeViewModel}.kt` (bottom NavigationBar + nested NavHost; VM fires `AnalyticsEvent.HomeViewed` from `init { }`)** — templates in `references/app-module.md`. Then the two demo tabs in their full feature-first shape: `feed/{data,domain,ui}/` (`references/feed-feature.md`) and `profile/{data,domain,ui}/` (`references/profile-feature.md`). Each tab ships a `RepositoryImpl` (stub data wrapped in `Outcome.Success`), a domain `Repository` interface + `UseCase`, a Hilt `<Feature>DataModule` binding the impl, and `UiState` / `ViewModel` / `Screen` / `Route` under `ui/`. ViewModels expose user actions as discrete public functions (`fun retry()`, `fun submit(...)`), matching Google's [Now in Android](https://github.com/android/nowinandroid); escalate to a sealed `<Screen>Action.kt` only when a screen has ≥5 distinct interactions.
9. Write `:app` tests — `core/domain/OutcomeMapTest.kt` (template in `references/core-domain.md`), `feed/ui/FeedViewModelTest.kt` and `profile/ui/ProfileViewModelTest.kt` (each mocks `AnalyticsTracker` + the feature use case and verifies the `init { }` analytics event fires), plus the Compose UI tests `feed/ui/FeedScreenTest.kt` and `profile/ui/ProfileScreenTest.kt` under `app/src/androidTest/`. Templates for VM + screen tests in `references/tests.md`. The androidTest pair anchors the Route + Screen split: each test drives the **stateless** `<Feature>Screen` directly, not the Route — no Hilt setup needed.
10. **Compile + assemble + run unit tests.** Run `:app:compileDebugKotlin`, then **`:app:assembleDevDebug`** (the full assemble — this is the gate that catches missing Gradle plugins, unresolved deps, manifest merger errors), then `:app:testDebugUnitTest`. `compileDebugKotlin` alone is not sufficient. The Compose UI tests run via `:app:connectedDebugAndroidTest` when an emulator/device is attached; if none is available, leave them ready-to-run rather than blocking the scaffold.
11. Emit manual setup notes (signing, flavor stubs, Firebase files). See "Post-scaffold manual steps" below; if `INCLUDE_FIREBASE`, also see `references/optional-firebase.md`.

---

## Hard rules

- **Feature-first packaging.** Each feature is a top-level package containing only the layers it needs (`<feature>/{ui,domain,data}/`). Cross-feature plumbing lives under `core/`. Don't grow a global `ui/`, `domain/`, or `data/` next to features — that's the layer-first shape this scaffold deliberately avoids.
- **No `kapt`.** KSP only (Hilt 2.48+, Room 2.6+ all support KSP).
- **No string routes.** Navigation Compose 2.8+ typed destinations via `@Serializable` + `kotlinx-serialization` plugin.
- **Keep `core/domain/` and `<feature>/domain/` Android-free.** No `android.*` imports, no Compose, no Retrofit, no Room — only Kotlin stdlib + coroutines. Enforced by review until/unless you extract `:core:domain` / `:feature:<name>:domain` (a `kotlin.jvm` module would enforce it mechanically).
- **`ui/` consumes `domain/` interfaces, never `data/` types.** Repository implementations stay behind interfaces declared in `domain/`. Cross the boundary through use cases, not by reaching into `data/` directly.
- **One `Outcomes.kt` adapter, one `toDomainError(...)` mapper.** Every `runCatching { ... }` boundary call goes through `Result<T>.toOutcome(::toDomainError)`. Open-coding `runCatching { ... }.fold(...)` swallows `CancellationException` and silently breaks coroutine cancellation — see `core/data/network/Outcomes.kt` (in `references/core-data.md`) for the canonical implementation.
- **Compose BOM is the single source of truth** for Compose versions. Never pin individual Compose libs.
- **Apply `kotlin.compose` (the standalone Gradle plugin) on every module with `buildFeatures.compose = true`.** The plugin alias lives in the catalog as `kotlin-compose` and rides the `kotlin` version ref. Without the alias, the Kotlin compiler aborts with `Compose Compiler is required, but not applied`. Don't pin Compose Compiler separately.
- **Version catalog is the single source of truth** for all versions. Never inline `"2.1.0"` in a module `build.gradle.kts`.
- **Hilt on the Application**, on every `Activity` / `ViewModel` / Service that needs injection. Don't sprinkle `EntryPoint` unless you truly have a non-Hilt consumer.
- **`exportSchema = true`** is mandatory for Room once the app ships. The `schemas/` directory goes into version control.

## Signing-config inputs

The `app/build.gradle.kts` template (`references/app-module.md`) wires the release signing config to a root-level `keystore.properties` file. Commit a *redacted* `keystore.properties.example` so contributors know the shape; gitignore the real one.

### `keystore.properties.example`

```properties
# Copy to keystore.properties (gitignored) and fill in real values.
# Path is resolved relative to the repository root.
storeFile=release.keystore
storePassword=changeme
keyAlias=release
keyPassword=changeme
```

### `.gitignore` additions (root)

```
keystore.properties
*.keystore
/app/src/*/google-services.json
```

## Post-scaffold manual steps

Emit a block the command prints to the user:

```
Scaffold complete. Next steps:

☐ Generate a release keystore and copy keystore.properties.example → keystore.properties (gitignored).
   keytool -genkey -v -keystore release.keystore -alias release -keyalg RSA -keysize 2048 -validity 10000
   The signing config in app/build.gradle.kts auto-wires once keystore.properties exists.

☐ [if Firebase] drop google-services.json into app/src/dev/ and app/src/prod/.
   The build-time guard skips processGoogleServices per-variant until the JSON
   arrives, AND FirebaseAnalyticsTracker no-ops at runtime if FirebaseApp isn't
   initialized — so the project compiles, installs, AND launches from the moment
   you finish scaffolding. Events start flowing as soon as the JSON lands.

☐ [if Room] confirm app/schemas/ is populated after ./gradlew :app:kspDevDebugKotlin.
☐ Replace the Feed and Profile tab placeholders with your first real features
   (each tab is a typed `HomeRoute` destination under `ui/home/`).

Build and run:
  ./gradlew :app:installDevDebug
  ./gradlew :app:testDebugUnitTest
```
