---
name: mobile-ios-native
description: Native iOS development with Swift, SwiftUI, and the modern Apple platforms stack (iOS 16+). Use when building, reviewing, or refactoring iOS apps using SwiftUI, Swift Concurrency (async/await, actors), Observation, SwiftData/Core Data, Combine, and Xcode tooling.
source: self
---

# Mobile iOS Native

Modern, production-grade iOS engineering with Swift and SwiftUI on Apple platforms.

## When to Use

- Building or reviewing native iOS apps (Swift + SwiftUI)
- Migrating from UIKit to SwiftUI, or Combine to Swift Concurrency
- Designing iOS-specific architecture (scenes, lifecycle, background modes)
- Integrating Apple platform APIs (HealthKit, CoreLocation, AVFoundation, WidgetKit, App Intents)
- Reviewing Xcode build settings, code signing, App Store Connect, or TestFlight workflows

## Toolchain Defaults

- Language: Swift 5.10+ (Swift 6 mode where dependencies allow), strict concurrency checking on
- UI: SwiftUI first; UIKit only where SwiftUI gaps exist (use `UIViewRepresentable` bridges)
- Min iOS: 16 (lower only with explicit reason); use availability checks for newer APIs
- Build: Xcode latest stable, Swift Package Manager (SPM) preferred over CocoaPods/Carthage
- State: `@Observable` (Observation framework, iOS 17+), `@State`, `@Binding`, `@Environment`; Combine only for legacy bridges
- Persistence: SwiftData (iOS 17+) or Core Data with NSPersistentCloudKitContainer; Keychain for secrets
- Networking: `URLSession` with `async/await`; `Codable` + JSON; `Sendable` models
- Background: BGTaskScheduler, background URLSession, push-triggered fetch
- Testing: XCTest, Swift Testing (when stable), XCUITest, snapshot tests via SwiftSnapshotTesting

## Architecture Rules

1. Prefer SwiftUI views composed of small, focused subviews; pass state via `@Binding` and environment.
2. Use `@Observable` model classes (or `ObservableObject` pre-iOS 17) as the source of truth; views are derived.
3. Layer the app: `Features` (views + view models) → `Domain` (pure Swift) → `Data` (repositories, services). Keep Domain free of UIKit/SwiftUI imports.
4. Inject dependencies through initializers or `Environment`; avoid singletons except for system-bridged services.
5. Use Swift Concurrency end-to-end: `async`/`await`, `Task`, `TaskGroup`, `AsyncSequence`. Isolate mutable shared state with `actor`s.
6. Mark types `Sendable` where they cross concurrency domains; turn on strict concurrency checking and resolve all warnings.
7. Use `@MainActor` for UI-touching code; never block the main thread with synchronous I/O.

## SwiftUI Rules

- Keep view bodies small; extract subviews to enable better diffing and previews.
- Use `Identifiable` models with stable IDs in `ForEach`; avoid index-based identity.
- Prefer `LazyVStack`/`LazyHStack`/`List` for large collections; use `.id()` and `.task(id:)` carefully.
- Use `.task { }` for async work tied to view lifetime; cancel propagates automatically.
- Animate with `withAnimation` and `matchedGeometryEffect`; respect Reduce Motion.
- Theming: support Dynamic Type, Dark Mode, high-contrast, and SF Symbols variants.
- Accessibility: every actionable element has a label; group related elements; provide rotor/custom actions where appropriate.

## Concurrency & Data

- Use `async let`, `TaskGroup`, and `AsyncStream` instead of `DispatchQueue` callbacks.
- Cancellation is cooperative — check `Task.checkCancellation()` in long loops.
- Repositories return `async throws` functions or `AsyncSequence`; map errors to a domain `Error` enum.
- SwiftData: model context is main-actor isolated; use background contexts for heavy writes.
- Core Data: use `NSPersistentContainer.newBackgroundContext()` and merge changes; never pass `NSManagedObject` across contexts.
- Networking: configure `URLSessionConfiguration` (timeouts, waitsForConnectivity), pin certificates for sensitive endpoints.

## Performance

- Profile with Instruments (Time Profiler, Allocations, Hangs, SwiftUI, Animation Hitches) before optimizing.
- Cold launch budget: < 400ms to first useful frame on iPhone 12 / mid-range device.
- Avoid `@StateObject`/`@Observable` churn; pass minimal state down the tree.
- Use `drawingGroup()` for complex composited views; avoid offscreen passes when not needed.
- Image pipeline: load correctly sized images, prefer `Image(uiImage:)` from a cached `UIImage`, decode off-main when needed.
- Reduce app size: enable bitcode-free distribution, App Thinning, on-demand resources for large assets.
- Watch hangs and disk writes via MetricKit; ship `MXMetricManager` integration in production.

## Security

- Store secrets in Keychain with `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` minimum.
- Use App Transport Security (ATS) with no exceptions; pin certificates for sensitive endpoints.
- Enable Hardened Runtime, App Sandbox, and Data Protection (`NSFileProtectionComplete` where possible).
- Use `LAContext` for biometric gating; require recent authentication for sensitive actions.
- Validate all Universal Links / deep link inputs; reject unexpected schemes.
- Privacy: declare required reason APIs, fill out the Privacy Manifest (`PrivacyInfo.xcprivacy`), and minimize tracked data.

## Testing

- Unit-test domain code with no UI dependencies; use protocol-based fakes injected via initializers.
- Use Swift Testing or XCTest with `async` tests; avoid expectations for async code.
- Snapshot-test critical SwiftUI screens across Dynamic Type sizes and color schemes.
- XCUITest for end-to-end smoke flows; keep them short and deterministic.
- Run tests on multiple device classes (small phone, large phone, iPad) in CI.

## Release & Distribution

- Use Xcode Cloud or Fastlane for automated builds, signing, and TestFlight uploads.
- Manage signing with App Store Connect API keys; never commit `.p12` or provisioning profiles.
- Use phased release on the App Store; monitor crash-free users and MetricKit signals.
- Maintain a Privacy Manifest, App Privacy details, and accurate export compliance.
- Use TestFlight internal/external groups for staged validation before submission.

## Anti-Patterns

- Force-unwrapping (`!`) outside tests or unmistakably safe boundaries
- Using `DispatchQueue.main.async` from inside `async` code instead of `@MainActor`
- Long-lived `Task { }` without storing/cancelling; leaking work after view dismissal
- `ObservableObject` with many `@Published` properties causing whole-view invalidation
- Storing `UIViewController` or `UIView` references in models
- Hard-coding strings for accessibility labels in non-localized form
- Shipping without `Sendable`/strict concurrency warnings resolved
- Disabling ATS or skipping Privacy Manifest entries

## Review Checklist

- [ ] Min iOS, Swift, and Xcode versions are current and aligned
- [ ] SwiftUI views are small, hoist state, and use stable identities
- [ ] Concurrency: `async/await`, `actor` isolation, `Sendable` correctness, `@MainActor` on UI
- [ ] Domain layer is UI-framework free; dependencies injected via init/environment
- [ ] Persistence uses SwiftData/Core Data correctly across contexts
- [ ] Secrets in Keychain; ATS on; Privacy Manifest filled out
- [ ] Accessibility: Dynamic Type, VoiceOver labels, Reduce Motion respected
- [ ] Crash, hang, and launch metrics are monitored (MetricKit + Crashlytics/Sentry)
