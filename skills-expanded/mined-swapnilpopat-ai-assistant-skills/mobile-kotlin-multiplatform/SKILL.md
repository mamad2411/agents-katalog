---
name: mobile-kotlin-multiplatform
description: Cross-platform mobile development with Kotlin Multiplatform (KMP) and Compose Multiplatform. Use when sharing business logic (and optionally UI) across Android, iOS, desktop, and web while keeping native integration where it matters.
source: self
---

# Mobile Kotlin Multiplatform

Production-grade Kotlin Multiplatform (KMP) and Compose Multiplatform (CMP) engineering for sharing code across Android, iOS, desktop, and web.

## When to Use

- Sharing domain, data, and networking layers across Android and iOS (and optionally desktop/web)
- Adding shared UI with Compose Multiplatform when product needs justify it
- Migrating a Kotlin Android codebase to KMP without rewriting iOS
- Integrating shared Kotlin code into an existing Swift/SwiftUI app

## Toolchain Defaults

- Kotlin: latest stable with K2 compiler; Gradle Kotlin DSL + version catalogs
- KMP targets: `androidTarget()`, `iosArm64()`, `iosSimulatorArm64()`, `iosX64()` (only if needed); add `jvm()`/`wasmJs()` per product
- iOS distribution: XCFramework via `kotlin("multiplatform")` + `XcodeProject`/`SwiftPM` integration (CocoaPods deprecated path — prefer SwiftPM-direct)
- Networking: Ktor Client (multiplatform), kotlinx.serialization
- Persistence: SQLDelight (preferred) or Room KMP where appropriate
- DI: Koin Multiplatform or manual DI; avoid Hilt (Android-only)
- Concurrency: Kotlin Coroutines + Flow with `Dispatchers.IO`/`Dispatchers.Default`; use `Dispatchers.Main` only on UI targets
- Date/time: `kotlinx-datetime`; UUIDs: `kotlin.uuid`
- Logging: `Napier` or `Kermit`
- Settings/secrets: `multiplatform-settings` + platform Keychain/Keystore bridges

## Architecture Rules

1. Default to sharing the **domain** and **data** layers; share UI only when product/team velocity justifies it.
2. Express public API in `commonMain` using only stable, multiplatform-safe types; keep platform code in `androidMain`/`iosMain`.
3. Use `expect`/`actual` sparingly — only for true platform primitives (Keychain, secure storage, biometric, push tokens).
4. Make all shared types `Sendable`-friendly: immutable, no captured Android `Context`, no JVM-only APIs.
5. Surface async APIs as `suspend` functions and `Flow`; wrap them in iOS-friendly facades (see iOS Bridging) so Swift consumers don't see Kotlin-only constructs.
6. Keep the shared module pure Kotlin where possible; pull in Compose only on targets that consume it.

## iOS Bridging Rules

- Generate an XCFramework; integrate via Swift Package Manager (`Package.swift`) for clean dependency management.
- Wrap shared `suspend` functions and `Flow` in Swift-friendly types:
  - Use `SKIE` (or hand-written wrappers) to expose `suspend` as Swift `async/await` and `Flow` as `AsyncSequence`.
  - Avoid leaking `kotlinx.coroutines` types directly to Swift call sites.
- Use `@HiddenFromObjC` / `@ShouldRefineInSwift` to hide raw Kotlin shapes when SKIE refines them.
- Treat the shared framework as a published API: version it, document it, and avoid breaking changes without migration notes.
- Keep iOS-specific glue (DI registration, Keychain `actual`s, push token plumbing) in `iosMain`, not in Swift.

## Compose Multiplatform Rules

- Use only when shared UI delivers clear value (forms, dashboards, internal tools); for highly platform-specific UX, prefer native UI.
- Mirror the Android Compose rules: hoist state, small composables, stable list keys, lifecycle-aware collection.
- Theming: define a shared design system; map to Material 3 on Android and a Cupertino-flavored theme on iOS where possible.
- Respect platform conventions for back navigation, gestures, and typography even with shared UI.
- iOS integration: host Compose in a `UIViewController` via `ComposeUIViewController`; bridge gestures and keyboard handling carefully.

## Concurrency & Data

- Coroutines: structured scopes only; never use `GlobalScope`. Inject dispatchers behind a `DispatcherProvider`.
- SQLDelight: define schemas in `.sq` files; generate typed queries; use `asFlow()` + `mapToList()` for reactive reads.
- Ktor: configure engine per platform (`Darwin` on iOS, `OkHttp` on Android); install `ContentNegotiation`, `Logging`, `HttpTimeout`, retry/backoff.
- Errors: map to a sealed `DomainError` in `commonMain`; never expose `Throwable` to consumers.
- Caching: in-memory + SQLDelight + ETag/`If-Modified-Since` where the API supports it.

## Build & Tooling

- Use a single `libs.versions.toml`; pin Kotlin, Compose Multiplatform, AGP, and Ktor versions explicitly.
- Configure hierarchical source sets (`appleMain`, `iosMain`) using the default hierarchy template.
- Enable `-Xexpect-actual-classes` only with intent; prefer interface-based abstractions.
- CI must build all targets and produce the XCFramework artifact; cache `~/.gradle` and Konan dependencies.
- Treat warnings as errors in `commonMain`; allow stricter compiler flags as the codebase matures.

## Testing

- Run `commonTest` on all targets; use `kotlinx-coroutines-test` and `Turbine` for Flows.
- Use `kotlin.test` assertions for portability; platform-specific tests live in `androidUnitTest`/`iosTest`.
- Mock with interfaces and hand-rolled fakes; MockK is JVM-only and not suitable for `commonTest`.
- Smoke-test the published XCFramework from a small Swift sample app in CI to catch ABI breaks.

## Performance

- Measure on each platform with platform-native tools (Android Profiler, Xcode Instruments).
- Watch out for Kotlin/Native memory model surprises — modern KMP uses the new memory model by default; verify it is enabled.
- Avoid large object graphs crossing the Kotlin↔Swift bridge in hot paths; batch or stream instead.
- Lazy-init expensive shared services; share singletons through DI rather than `object` declarations holding state.

## Security

- Secrets and tokens: store via platform Keychain (iOS) and EncryptedSharedPreferences/Keystore (Android) behind an `expect`/`actual` interface.
- TLS: pin certificates in Ktor's engine configuration when needed; do not disable certificate validation, ever.
- Strip logs from release builds (Napier/Kermit log gating).
- Treat the XCFramework like any other binary dependency: scan, sign, and verify checksums.

## Anti-Patterns

- Sharing UI prematurely before product needs justify it
- Exposing raw `kotlinx.coroutines` `Job`/`Flow` types to Swift without wrappers
- Putting Android `Context` or JVM-only types in `commonMain`
- Using `runBlocking` to bridge async APIs to Swift (use SKIE/async wrappers)
- Heavy use of `expect`/`actual` for things better solved with interfaces
- Skipping CI builds on iOS targets (regressions land silently)
- Treating the shared module as internal — it is a public API for two app teams

## Review Checklist

- [ ] Kotlin, AGP, Compose Multiplatform, and Ktor versions are pinned and current
- [ ] `commonMain` has no platform-specific imports; `expect`/`actual` is justified
- [ ] iOS framework is delivered as an XCFramework via SwiftPM with Swift-friendly async/Flow wrappers
- [ ] Coroutines use injected dispatchers; no `GlobalScope` or `runBlocking` outside tests
- [ ] Persistence (SQLDelight) and networking (Ktor) configured per platform with timeouts and retries
- [ ] Shared module API is versioned and documented; CI builds all targets including iOS
- [ ] Secrets stored via platform-secure storage behind a shared interface
