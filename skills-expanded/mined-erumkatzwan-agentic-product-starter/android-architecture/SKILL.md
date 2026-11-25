---
name: android-architecture
description: Use when adding or changing a screen, feature, route, service or dependency in the Android app (AgenticApp) (apps/android). Explains the layers, where code goes and the checklist for a new feature.
---

# Android architecture

MVVM with a composition root, a router and interface-based services. Kotlin, Jetpack Compose, Material 3, Navigation 3. Same layers and names as the iOS app, so a story reads the same on both platforms.

## Layers (package = layer, under `app/src/main/kotlin/com/agentic/app`)

| Package | Holds | May depend on |
|---|---|---|
| root (`com.agentic.app`) | `MainActivity`, `AppViewModel`, `AppContainer` (composition root), `RootScreen`, `AppEnvironment`, `LaunchOptions` | everything |
| `features/<name>` | `<Name>Screen` (composable) + `<Name>ViewModel` | core, designsystem |
| `core/network` | `ApiClient`, `Endpoint`, `Endpoints`, `FixtureApiClient` | kotlinx.serialization, OkHttp |
| `core/flags` | `FeatureFlag`, `FeatureFlagService`, `FeatureGate` | network |
| `core/navigation` | `Route`, `Router` | models |
| `core/auth` | `SessionStore` (who is signed in), `TokenStore` (Android Keystore) | services |
| `core/services` | Repositories, `AuthService`, push | network |
| `designsystem` | `AppTheme` tokens and `DS*` components | Compose only |

Per-environment values (API URL, environment name) live in `app/src/<flavor>/kotlin/.../FlavorConfig.kt`, the Android counterpart of the iOS `Config/*.xcconfig`.

## Rules

- Screens are thin: layout and callbacks only. Logic lives in a `ViewModel` that holds Compose state (`mutableStateOf`) and exposes `suspend` functions. Screens call them with `rememberCoroutineScope().launch { … }`.
- View models depend on interfaces (`ItemsRepository`, `AuthService`), never on OkHttp or concrete clients.
- Only `AppContainer` creates concrete implementations. No DI framework; add one (Hilt, Koin, Metro) only through an ADR.
- `RootScreen` shows the sign-in flow when signed out and the app when signed in; screens read the user from `SessionStore`.
- Navigate only through `Router` (`router.push(Route.X)`, `pop()`, `popToRoot()`). Add new screens as a `Route` and map them in `RootScreen`'s `entryProvider`. Create view models there with `viewModel { … }`, so they are scoped to the navigation entry.
- Every tappable or asserted element gets a `Modifier.testTag("<screen>.<element>")`, using the same names as the iOS accessibility identifiers.
- No `!!`, no hard-coded colours, font sizes or paddings, no `println`/`Log` left in features.

## Checklist: new feature or screen

1. Add `features/<name>/<Name>Screen.kt` and `<Name>ViewModel.kt`.
2. If it needs data: add an endpoint (see `android-rest-api`), a repository interface + implementation in `core/services`, wire it in `AppContainer`.
3. Add a `Route` and map it in `RootScreen`.
4. Add a `FeatureFlag` if it should be switchable (see `android-feature-flags`).
5. Style only with `AppTheme` tokens and `DS*` components (see `android-design-system`).
6. Tests: view-model unit tests, a UI test for the navigation, a Maestro flow for the user journey (see `android-testing`).
7. Build the same story on iOS (and web if it applies) with the same names, flags and fixtures.
8. Run `make ci` before opening the pull request.

## Google's Android skills

For deeper platform questions use the official skills in this folder: `navigation-3`, `edge-to-edge`, `jetpack-compose-performance`, `testing-setup`, `agp-9-upgrade`, `r8-analyzer`, `restore-credentials`, `android-permissions-security`, `android-intent-security`. This skill wins when they disagree, because it describes how this app is built.
