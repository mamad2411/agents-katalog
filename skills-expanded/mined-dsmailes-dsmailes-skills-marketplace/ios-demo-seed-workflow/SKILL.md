---
name: ios-demo-seed-workflow
description: Use when adding, reviewing, or planning debug-only believable demo data workflows for iOS apps. Applies to Swift, SwiftUI, SwiftData, Core Data, SQLite, TCA, App Store screenshot preparation, design review builds, onboarding demos, UI regression screenshots, simulator boot scripts, launch arguments such as --demo-seed, and Swift model based fixture registries. Use when the user asks to boot an iOS app with seeded data, create demo seed models, make screenshot fixtures, or add portable simulator demo profiles.
---

# iOS Demo Seed Workflow

## Mission

Add a portable, debug-only path that boots an iOS app with believable local data from Swift seed models. Optimize for screenshots, design review, onboarding demos, widget previews, and UI QA without touching private user data or release behavior.

## Default Workflow

1. Inspect the app's persistence boundary, launch setup, project/scheme, bundle id, and existing test patterns.
2. Create a narrow implementation plan or dev-team tickets when the host project uses tickets.
3. Add a Swift seed protocol and explicit registry.
4. Add debug-only startup wiring that imports a selected seed from `--demo-seed`.
5. Add two or three seed models with realistic states, not exhaustive fake data.
6. Add a simulator boot script based on `scripts/boot-demo-template.sh`.
7. If the user needs App Store screenshots, add the capture step from `references/app-store-screenshot-capture.md`.
8. Verify with focused tests, a build, and one real simulator boot when practical.

## Core Rules

- Keep demo seeding behind `#if DEBUG`, simulator-only build settings, or an equivalent non-release guard.
- Never seed from real private user data.
- Prefer Swift seed models over loose JSON when the app already has strong local model APIs.
- Use an explicit registry keyed by stable seed names; do not rely on runtime type-name reflection.
- Clear or isolate only the demo/debug store before inserting seeded data.
- Generate data through app-owned factories and persistence APIs where possible.
- Unknown seed names should fail clearly or no-op safely; they should not crash release users.
- Keep seed content believable, sparse, and useful for visual QA.

## Implementation Shape

Use this adaptable pattern:

```swift
#if DEBUG
protocol DemoSeedModel {
    static var demoSeedName: String { get }
    static func makeDemoData(now: Date) -> DemoSeedPayload
}

enum DemoSeedRegistry {
    static var seeds: [String: any DemoSeedModel.Type] {
        [
            AppStoreScreenshotSeed.demoSeedName: AppStoreScreenshotSeed.self,
            OnboardingDemoSeed.demoSeedName: OnboardingDemoSeed.self
        ]
    }
}
#endif
```

Adapt `DemoSeedPayload` to the target app. For simple apps it can be `[FeedItem]`; for broader apps it can include model objects, user defaults, widget snapshots, onboarding state, and files.

## Persistence Selection

- **SwiftData**: read `references/swiftdata-seed-pattern.md`.
- **Core Data**: use a debug context/container and import via normal managed object construction.
- **SQLite/GRDB/SQLiteData**: seed through migrations or repository APIs, not string-built SQL unless the project already does that safely.
- **TCA apps**: seed at app startup or dependency boundary, then let features load normally.
- **Widgets/App Groups**: write shared snapshots after app data is inserted.

## Seed Profiles

Prefer a small set of named profiles:

- `app-store-screenshots`: polished, varied, representative.
- `onboarding-demo`: shows first-run or guided states.
- `quiet-day`: sparse feed or empty-ish state.
- `edge-cases`: long text, missing media, disabled sources, error/empty states.

Use stable identifiers and relative dates from `now` so screenshots stay fresh.

## Boot Script

Copy and adapt `scripts/boot-demo-template.sh` into the target app. Keep these parameters explicit:

- scheme
- project/workspace
- bundle id
- product app path
- default simulator name
- supported seed names

Do not hide build failures. The script should reject unknown seeds before building.

## App Store Screenshots

When asked to generate App Store screenshots, add `scripts/capture-app-store-screenshots.sh` from `scripts/capture-app-store-screenshots-template.sh` after the seeded boot script works. Read `references/app-store-screenshot-capture.md` first.

Default to raw simulator screenshots suitable for App Store Connect. Do not add marketing frames, captions, device mockups, or overlays unless the user explicitly asks for composed marketing screenshots.

## Verification

Minimum checks:

```sh
bash -n scripts/boot-demo.sh
xcodebuild test -project App.xcodeproj -scheme App -destination 'platform=iOS Simulator,name=iPhone 17' -only-testing:AppTests/DemoSeedTests
xcodebuild -project App.xcodeproj -scheme App -destination 'generic/platform=iOS Simulator' build
scripts/boot-demo.sh quiet-day
```

Adjust commands for the host project. If simulator or Xcode cache access is sandboxed, request escalation rather than weakening verification.

## References

Read only what is needed:

- `references/swiftdata-seed-pattern.md` for SwiftData model/container code.
- `references/dev-team-ticket-slices.md` when the repo uses ticketed dev-team workflow.
- `references/app-store-screenshot-capture.md` when capturing App Store screenshots from seeded simulator states.
 
