# AGENTS.md

## Scope
Instructions for the iOS app. Applies to everything under `RefWatchiOS/`.

## Build & Test
- Build: `xcodebuild -project RefWatch.xcodeproj -scheme RefWatchiOS -destination 'platform=iOS Simulator,name=iPhone 15' build`
- Test (unit+UI if present): `xcodebuild test -project RefWatch.xcodeproj -scheme RefWatchiOS -destination 'platform=iOS Simulator,name=iPhone 15'`
- Run locally: select the scheme, pick an iPhone simulator, `⌘R`.
- Ensure the scheme is Shared.

## Structure & Conventions
- SwiftUI + MVVM, 2‑space indent. One primary type per file.
- App entry under `App/` with `AppRouter` for navigation.
- Core code in `Core/` (DesignSystem/Theme, Platform adapters, Persistence, Diagnostics).
- Features in `Features/` with `FeatureName/{Models,ViewModels,Views}`.
- Use domain/services shared from the watch target via target membership; avoid watch‑only imports.

## Platform Adapters
- Prefer `RefWatchiOS/Core/Platform` adapters (e.g., `IOSHaptics`, `ConnectivityClient`, AI assistant) accessed via protocols. Inject into view models/services. The assistant transport is server-backed; do not reintroduce client-side OpenAI credentials into the app target.

## Config & Secrets
- See `RefWatchiOS/Config/` for `.xcconfig` usage. Never commit real secrets; use `Secrets.example.xcconfig` for placeholders. OpenAI credentials belong to the backend assistant proxy only and should not be added to iOS config files.

## Testing Focus
- Unit tests emphasize iOS‑specific services/adapters and feature view models. UI tests focus on main tab flows.

## Don’ts
- Don’t import `WatchKit` or watch‑only code in iOS sources. Use `#if os(iOS)` and adapters.
