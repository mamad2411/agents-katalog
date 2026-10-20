# AGENTS.md

## Scope
Platform adapters used by the watch app. Applies to `RefWatchWatchOS/Core/Platform/` and its subfolders (e.g., Haptics, Connectivity).

## Conventions
- Provide protocol‑backed adapters for platform APIs (e.g., `WatchHaptics`).
- Keep adapters lightweight; no business logic—just thin wrappers that conform to protocols in `Core/Protocols/`.
- Guard with `#if os(watchOS)` when types must be visible across targets.
- Expose simple mocks/fakes for tests.

## Usage
- View models/services depend on protocols; inject adapters via initializer/env rather than referencing concrete types.

