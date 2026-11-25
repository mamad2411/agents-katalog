# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

JetUI is a reusable iOS SwiftUI component library (Swift Package) extracted from the TimeProof app. It targets iOS 17+ and is consumed by host apps as a local Swift package dependency.

## Commands

**Build / test the package (terminal):**
```sh
swift build
swift test
# Run a single test class:
swift test --filter JetPaywallExampleContentTests
```

**Fast iteration — skip Firebase re-compilation:**

Firebase (and its Google transitive deps) takes 3–5 min on a cold build but is cached by SwiftPM in `.build/`.
After the first full build succeeds, subsequent `swift build` runs only recompile changed files and are fast (< 30 s).

Strategies to keep builds fast:

```sh
# 1. Only type-check without linking (fastest: ~5–10 s on warm cache)
swift build -Xswiftc -typecheck

# 2. Debug build with explicit arch (avoids universal-binary overhead)
swift build -c debug --arch arm64

# 3. Build only changed targets (SwiftPM does this automatically on warm cache)
swift build

# 4. Run tests without rebuilding unaffected modules
swift test --filter <TestClassName>

# 5. If .build gets corrupted or you need a true clean:
swift package clean          # removes .build — next build is cold again
swift package reset          # also wipes checkouts (re-fetches all deps)

# 6. Pre-warm cache after a clean checkout (do once, then keep .build)
swift build 2>&1 | tail -5
```

**Why Firebase is slow:** FirebaseAnalytics alone pulls in ~15 C++ / ObjC++ modules (abseil, protobuf, GoogleUtilities, etc.) that cannot be parallelised past a certain point. Once compiled into `.build/`, they are never recompiled unless `Package.resolved` changes.

**CI tip:** Cache the `.build/` directory keyed on `Package.resolved` hash to avoid cold builds in CI:
```sh
# GitHub Actions example
- uses: actions/cache@v4
  with:
    path: .build
    key: swiftpm-${{ hashFiles('Package.resolved') }}
    restore-keys: swiftpm-
```

**Regenerate legacy example projects (if needed):**
```sh
xcodegen generate --spec Examples/JetUIPaywallExample/project.yml --project Examples/JetUIPaywallExample
xcodegen generate --spec Examples/JetUIModuleExamples/project.yml --project Examples/JetUIModuleExamples
```

**Open legacy example apps:**
```sh
open Examples/JetUIPaywallExample/JetUIPaywallExample.xcodeproj
open Examples/JetUIModuleExamples/JetUIModuleExamples.xcodeproj
```

> After opening a regenerated project, Xcode may show "An inconsistency was found … will be automatically corrected." — click OK, it is harmless.

## Architecture

### Layer overview

```
Host App (TimeProof, PetPal, …)
    └─ JetUI (Swift Package)
          ├─ Theme/          – Protocol-based theme injection (JetThemeConfig)
          │     └─ Examples/   – ExampleTheme (purple-branded, system fonts)
          ├─ Core/           – Logger, Cache, Diagnostics/MemoryMonitor, Utilities
          │     └─ Examples/   – JetCoreExamples (cache, logger, date)
          ├─ Components/     – Stateless SwiftUI building blocks (Toast, Alert, Glass, …)
          │     └─ Examples/   – JetComponentExamples (toast configs, alert configs, image URLs)
          ├─ Network/        – Moya-backed NetworkCore, Resilience/CircuitBreaker, Account
          │     └─ Examples/   – JetNetworkExamples (ExampleAPIConfig, ExampleAuthSession, error scenarios)
          ├─ Auth/           – Unified auth module (AuthManager + AuthSession + AuthTarget)
          │     ├─ Core/        – AuthManager (lifecycle, Keychain, Apple Sign-In, ECDSA)
          │     │               – AuthSession (token injection into NetworkCore)
          │     ├─ Network/     – AuthTarget (Moya endpoints), AuthModels, LoginResult
          │     └─ Examples/   – JetAuthExamples (state samples, Keychain key reference, Apple Sign-In flow)
          ├─ Analytics/      – Platform-agnostic analytics (JetAnalyticsProvider protocol)
          │     ├─ Firebase/    – FirebaseAnalyticsAdapter (swappable)
          │     └─ Examples/   – JetFirebaseExamples (event samples, user properties)
          ├─ Storage/        – Platform-agnostic cloud storage (JetCloudStorageProvider protocol)
          │     └─ Firebase/   – JetStorageManager/Firebase adapter (swappable)
          ├─ Features/
          │     ├─ Subscription/  – StoreKit 2 full-stack (config → service → VM → views)
          │     │     └─ Examples/   – JetPaywallExampleContent (exampleTimeProofTrial, exampleTimeProofFull)
          │     ├─ Settings/      – Configurable settings page
          │     │     └─ Examples/   – JetSettingsExamples (exampleDark, exampleLight configurations)
          │     └─ Onboarding/    – Paginated onboarding view
          │           └─ Examples/   – JetOnboardingExamples (page presets, dark/light configs)
          ├─ Models/         – Shared value types (JetAppItem)
          │     └─ Examples/   – JetModelsExamples (exampleFeaturedApps, usage notes)
          └─ Extensions/     – UIImage+Jet, View+Jet
                └─ Examples/   – JetExtensionExamples (View + UIImage snippet catalog)
```

### Key architectural decisions (v3.0)

**Auth is one module.** `Auth/Core/` owns the login-state lifecycle (Keychain, Apple Sign-In, ECDSA signing). `Auth/Network/` owns the Moya HTTP layer (endpoints + request/response models). The previous split between `Network/Auth/` and `Auth/` is gone.

**Analytics & Storage are protocol-first.** `JetAnalyticsProvider` and `JetCloudStorageProvider` are thin protocols in `Analytics/` and `Storage/`. Firebase implementations live under `Analytics/Firebase/` and `Storage/Firebase/` and are registered at app startup via `JetAnalytics.shared.register(…)` / `JetCloudStorage.shared.register(…)`. Swapping backends (e.g. Amplitude, Cloudflare R2) requires only a new adapter.

**CircuitBreaker belongs to Network.** `Network/Resilience/CircuitBreaker.swift` protects outbound API calls. `Core/Diagnostics/MemoryMonitor.swift` handles in-process diagnostics — these are distinct concerns.


### Theme system

Host apps inject a `JetThemeConfig` implementation at startup; internal code accesses it via `JetUI.theme`. The protocol hierarchy is:

```
JetThemeConfig
  ├─ colors:  JetColorPalette   (brandPrimary, backgroundPrimary, textPrimary, …)
  ├─ fonts:   JetTypography     (displayXXL … footnote)
  └─ layout:  JetLayoutConfig
                ├─ spacing: JetSpacing  (xs/s/m/l/xl/xxl)
                ├─ radius:  JetRadius   (small/medium/large/pill)
                └─ icons:   JetIcons
```

`DefaultTheme` is used when no custom theme is provided. `AppColor` and `AppFont` are convenience accessors that delegate to `JetUI.theme`.

### Subscription module

The public entry point is `JetPaywall` (`Features/Subscription/Views/JetPaywall.swift`). It dispatches to either `JetPaywallView` (`.list` style) or `JetTrialPaywallView` (`.timeline` style) based on a `JetPaywallStyle` enum.

Content is separated from style via `JetPaywallContent`. Example presets live in `JetPaywallContent+Presets` (used by both tests and example apps).

The subscription stack:
- `JetSubscriptionConfig` — product IDs, group ID, app identifier
- `JetStoreService` — StoreKit 2 fetch/purchase, calls backend `bindSubscription` internally
- `JetSubscriptionManager` — observable `isPro` state, wraps `JetTransactionObserver`
- `JetPaywallViewModel` — drives both paywall views; host app configures it via `JetUI.configureSubscription(_:)`

### Network layer

`NetworkCore` wraps Moya. Callers use `NetworkCore.shared.api(_:_:)`. Auth tokens are managed by `AuthSession` and injected via `NetworkCore.shared.authSession`. `AccountService` handles subscription backend binding.

### Naming convention

All public types are prefixed with `Jet` (e.g., `JetToastView`, `JetStoreService`). File names match type names.

## Example Apps

| App | Purpose |
|---|---|
| `JetUIExampleApp` | **Primary example app** — two tabs: (1) Module catalog with interactive example for every module (Auth, Components, Core, Extensions, Features, Firebase, Models, Network, Resources, Theme); (2) Paywall tab for testing StoreKit 2 layouts. Use this for all module development. |
| `JetUIPaywallExample` | Legacy Paywall-only example. Retained for StoreKit Configuration file testing with real price rows. |
| `JetUIModuleExamples` | Legacy module catalog. Superseded by `JetUIExampleApp`. |

**Open / regenerate the primary example app:**
```sh
# Regenerate after editing project.yml
xcodegen generate --spec Examples/JetUIExampleApp/project.yml --project Examples/JetUIExampleApp

# Open in Xcode
open Examples/JetUIExampleApp/JetUIExampleApp.xcodeproj
```

## App Startup Configuration

```swift
// Typical host-app init()
JetUI.configureTheme(MyAppTheme())
JetUI.configureLogger(subsystem: Bundle.main.bundleIdentifier!)
JetUI.configureAnalytics(enabled: true)
JetUI.configureAuth(MyAPIConfig())
JetUI.configureAccount(baseURL: apiURL, tokenProvider: { AuthManager.shared.token })
JetUI.configureSubscription(
    JetSubscriptionConfig(
        productIds: [...],
        proProductIds: [...],
        groupId: "...",
        appIdentifier: "..."
    )
)
```
