# AGENTS.md

## Scope
Guidance for the Swift Package `RefWatchCore`. Applies to everything under `RefWatchCore/`.

## Build & Test
- Build: `swift build --package-path RefWatchCore`
- Test: `swift test --package-path RefWatchCore`
- Targets: platform‑agnostic. Do not import UI frameworks or platform SDKs here.

## Responsibilities
- Owns domain models, protocols, core services, and view models shared by iOS and watchOS.
- No SwiftUI, UIKit, or WatchKit. Isolate platform integration behind protocols.

## Conventions
- Public API is minimal and protocol‑first; prefer value semantics where possible.
- Files are single‑purpose; naming matches type names. 2‑space indent.
- Thread‑safety: services must be deterministic and testable; document any async behavior.
- Avoid global singletons; inject dependencies via initializers.

## Testing
- Cover services and view models with XCTest in `RefWatchCore/Tests`. Use in‑memory fakes/mocks for persistence or connectivity.
- Naming: `test<Action>_when<Context>_does<Outcome>()`.

