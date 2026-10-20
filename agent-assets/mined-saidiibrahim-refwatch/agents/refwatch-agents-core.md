# AGENTS.md

## Scope
Cross‑cutting watchOS building blocks under `Core/`: Components, Platform, Protocols, Services.

## Modules
- Components: Reusable SwiftUI views (buttons, inputs, selections, timer faces). No business logic.
- Platform: Adapters to platform APIs (haptics, connectivity). Must conform to protocols.
- Protocols: Contracts for timers, live activity, etc. No implementation.
- Services: Pure logic (formatting, live activity state, match lifecycle). No SwiftUI or platform calls.

## Conventions
- Protocol‑first. Views depend on view models; view models/services depend on protocols.
- Keep components stateless where possible; pass data via bindings or model objects.
- Separate watch‑only code with `#if os(watchOS)` when sharing headers with iOS.

## Testing
- Unit test services and protocol‑backed logic. Provide simple mocks for platform adapters.

