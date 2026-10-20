# AGENTS.md

## Scope
Instructions for the watchOS app. Applies to everything under `RefWatchWatchOS/`.

## Build & Test
- Build: `xcodebuild -project RefWatch.xcodeproj -scheme "RefWatch Watch App" -destination 'platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)' build`
- Test (unit+UI if present): `xcodebuild test -project RefWatch.xcodeproj -scheme "RefWatch Watch App" -destination 'platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)'`
- Run locally: select the scheme, pick a watch simulator, `⌘R`.
- Ensure the scheme is Shared (Product → Scheme → Manage Schemes…).

## Structure & Conventions
- SwiftUI + MVVM, 2‑space indent. One primary type per file.
- Core code in `Core/` (Components, Platform adapters, Protocols, Services).
- Features in `Features/FeatureName/{Views,Models,ViewModels}`.
- Shared domain/services live here and are target‑shared with iOS as needed. Guard platform code with `#if os(watchOS)`.

## Timer Faces
- Timer faces live under `Core/Components/TimerFaces/`. Default style is `standard` and is persisted via `@AppStorage("timer_face_style")`.
- Use `TimerFaceFactory` to render a face from `TimerFaceStyle`. Do not switch on style in views directly.

## Platform Adapters
- Use adapters in `Core/Platform/` (e.g., `WatchHaptics`, connectivity). Depend on protocols from `Core/Protocols/`; inject adapters into view models/services.

## Testing Focus
- Prioritize ViewModel and Service tests. UI tests cover key flows. Naming: `test<Action>_when<Context>_does<Outcome>()`.

## Don’ts
- Don’t import iOS‑only frameworks here. Don’t bypass adapters to call platform APIs in features.

