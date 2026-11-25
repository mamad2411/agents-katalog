---
name: ios-architecture
description: Use when adding or changing a screen, feature, route, service or dependency in the iOS app (AgenticApp) (apps/ios). Explains the layers, where code goes and the checklist for a new feature.
---

# iOS architecture

MVVM with a composition root, a router and protocol-based services. SwiftUI + Observation, iOS 17+.

## Layers (folder = layer)

| Folder | Holds | May depend on |
|---|---|---|
| `AgenticApp/App` | App entry, `AppContainer` (composition root), `RootView`, environments | everything |
| `AgenticApp/Features/<Name>` | `<Name>View` + `<Name>ViewModel` | Core, DesignSystem |
| `AgenticApp/Core/Networking` | `APIClient`, `Endpoint`, `Endpoints` | Foundation only |
| `AgenticApp/Core/FeatureFlags` | `FeatureFlag`, `FeatureFlagService`, `FeatureGate` | Networking |
| `AgenticApp/Core/Navigation` | `Route`, `Router` | Models |
| `AgenticApp/Core/Auth` | `SessionStore` (who is signed in), `TokenStore` (Keychain) | Services |
| `AgenticApp/Core/Services` | Repositories, `AuthService`, push | Networking |
| `AgenticApp/DesignSystem` | `Theme` tokens and `DS*` components | SwiftUI only |

## Rules

- Views are thin: layout and bindings only. Logic lives in an `@MainActor @Observable` view model.
- View models depend on protocols (`ItemsRepository`, `AuthService`), never on `URLSession` or concrete clients.
- Only `AppContainer` creates concrete implementations.
- `RootView` shows the sign-in flow when signed out and the app when signed in; screens read the user from `SessionStore`.
- Navigate only through `Router` (`router.push(.route)`, `pop()`, `popToRoot()`). Add new screens as a `Route` case and map it in `RootView`.
- Every tappable or asserted element gets an `accessibilityIdentifier` named `<screen>.<element>`.
- No force unwrapping, no hard-coded colors or fonts, no `print`.

## Checklist: new feature or screen

1. Add `AgenticApp/Features/<Name>/<Name>View.swift` and `<Name>ViewModel.swift`.
2. If it needs data: add an endpoint (see `ios-rest-api`), a repository protocol + implementation in `Core/Services`, wire it in `AppContainer`.
3. Add a `Route` case and map it in `RootView`.
4. Add a `FeatureFlag` if it should be switchable (see `ios-feature-flags`).
5. Style only with `Theme` tokens and `DS*` components (see `ios-design-system`).
6. Tests: view-model unit tests, a UI test for the navigation, a Maestro flow for the user journey (see `ios-testing`).
7. Run `make ci` before opening the pull request.
