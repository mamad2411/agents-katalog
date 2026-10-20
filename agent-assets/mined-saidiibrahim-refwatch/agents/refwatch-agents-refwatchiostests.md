# AGENTS.md

## Scope
Unit tests for the iOS app. Applies to `RefWatchiOSTests/`.

## Run
- `xcodebuild test -project RefWatch.xcodeproj -scheme RefWatchiOS -destination 'platform=iOS Simulator,name=iPhone 15'`

## Guidance
- Focus on iOS‑specific services/adapters and feature view models.
- Use in‑memory persistence and protocol mocks; avoid network.
- Naming: `test<Action>_when<Context>_does<Outcome>()`.

