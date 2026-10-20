# AGENTS.md

## Scope
UI tests for the iOS app. Applies to `RefWatchiOSUITests/`.

## Run
- `xcodebuild test -project RefWatch.xcodeproj -scheme RefWatchiOS -destination 'platform=iOS Simulator,name=iPhone 15'`

## Guidance
- Cover main tab flows (Matches, Live, Library, Trends, Settings).
- Prefer stable accessibility identifiers. Reset state between tests; avoid network.
- Keep tests fast and robust; avoid sleeping—wait on elements.

