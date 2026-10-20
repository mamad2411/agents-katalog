# AGENTS.md

## Scope
UI tests for the watch app. Applies to `RefWatchWatchOSUITests/`.

## Run
- `xcodebuild test -project RefWatch.xcodeproj -scheme "RefWatch Watch App" -destination 'platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)'`

## Guidance
- Cover critical match flows (kickoff → events → full time) and timer face switching.
- Prefer stable identifiers and visible text over coordinates.
- Keep runs reliable; minimize flakiness by avoiding real network and by resetting state between tests.

