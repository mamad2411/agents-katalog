# Repository Guidelines

## Project Overview
macOS menu bar utility that opens a terminal in the active IDE's project directory. Supports JetBrains IDEs, VS Code, Cursor, Antigravity, and Xcode. Pure SwiftPM app — no Xcode project.

## Project Structure
- `Sources/Shellporter`: Swift 6.2 menu bar app (resolver pipeline, terminal launcher, hotkey system, config, UI). Keep changes small; reuse existing helpers.
- `Tests/ShellporterTests`: Swift Testing (`@Test`, `#expect`) — not XCTest. Mirror new logic with focused tests.
- `Scripts`: build/package helpers (`compile_and_run.sh`, `package_app.sh`, `sign-and-notarize.sh`, `make_appcast.sh`).
- `docs`: release notes and process docs.

## Build, Test, Run
- Dev loop: `./Scripts/compile_and_run.sh --dev` - kills old dev instance, builds, packages `Shellporter Dev.app`, relaunches.
- With tests: `./Scripts/compile_and_run.sh --dev --test`
- Quick build/test: `swift build` / `swift test`
- Universal release: `./Scripts/compile_and_run.sh --release-universal`
- Signing setup: `./Scripts/setup_dev_signing.sh`

## Coding Style
- **Swift 6.2 strict concurrency.** `@MainActor` where needed; background work via `withCheckedContinuation` + `DispatchQueue`. `@unchecked Sendable` only where a dispatch queue provides thread safety.
- Dependency injection via constructor for testability.
- All UI strings go through `AppStrings.swift`, backed by `Localizable.strings` via `Bundle.module`.

## Testing Guidelines
- Use Swift Testing framework (`import Testing`, `@Test`, `#expect`). Tests touching `@MainActor` types: `@Test @MainActor`.
- Always run `swift test` before handoff.
- After code changes affecting the app, rebuild and relaunch the dev app with `./Scripts/compile_and_run.sh --dev` to validate.

## Release Flow
1. Bump `version.env` (MARKETING_VERSION + BUILD_NUMBER)
2. Update `CHANGELOG.md`
3. `swift test`
4. `./Scripts/sign-and-notarize.sh` (requires `.env` with Apple credentials, Sparkle key)
5. GitHub release + upload zip
6. `./Scripts/make_appcast.sh <zip>` to update `appcast.xml`
7. Commit and push `appcast.xml`

## Agent Notes
- Use SwiftPM and provided scripts; avoid adding dependencies without confirmation.
- After any code edit, rebuild with `./Scripts/compile_and_run.sh --dev` before validating behavior.
- Prefer modern SwiftUI/Observation macros (`@Observable`, `@State`, `@Bindable`); avoid `ObservableObject`/`@ObservedObject`/`@StateObject`.
