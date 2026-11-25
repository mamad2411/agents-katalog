# AGENTS.md — splitio_client_side package

## Purpose

**Public SDK entry point + CS-layer wiring** — The package end users install. Owns `SplitFactory`, `SplitClient`, `SplitManager`, and the DI composition root (`DependencyContainer`) that assembles all `splitio_commons` subdomains into a working SDK instance. Maps to spec §3.3 and §7.

## Key Files

- `lib/splitio_client_side.dart` — Public library export (re-exports all user-facing types)
- `lib/src/internal/split_factory.dart` — `SplitFactory`: creates SDK instances, wires all layers
- `lib/src/internal/dependency_container.dart` — DI composition root (LOC-exemption: approved)
- `lib/src/internal/split_manager.dart` — `SplitManager`: flag listing / metadata queries
- `lib/src/internal/user_consent.dart` — User consent state management
- `lib/src/client/split_client.dart` — `SplitClient`: per-key evaluation + track + lifecycle

## Testing

- **Run tests**: `cd packages/splitio_client_side && dart test`
- **Integration tests**: `cd packages/e2e && dart test` (authoritative end-to-end coverage)
- **Focus**: Wiring correctness, public API contract, factory lifecycle

## Dependencies

- **Internal**: `splitio_commons` (all subdomains via single package dep)
- **External**: None (kept thin intentionally)

## Public API (spec §7 — do NOT change casually)

- `SplitFactory.create(config)` / `.destroy()`
- `SplitClient.getTreatment(flag, [opts])` / `.getTreatments(flags, [opts])` / `.track(...)` / `.ready()` / `.destroy()`
- `SplitManager.splits()` / `.split(name)` / `.names()`
- `SplitClientConfig` / `SplitView`
- `SplitClient.whenReady()` / `whenTimeout()` / `whenUpdated()` (readiness lifecycle)

## Important Patterns

- **Composition root**: `DependencyContainer` is the only place that knows about all subdomains
- **Thin public layer**: No business logic here — delegates everything to `splitio_commons`
- **Factory pattern**: `SplitFactory` constructs and owns the SDK lifetime

## DOs

- Keep this package thin — logic belongs in `splitio_commons`
- Re-export all user-facing types so users only import `splitio_client_side`
- Maintain semver carefully — this is the user-facing contract

## DON'Ts

- Don't change the public API without spec sign-off and user approval (spec §7)
- Don't add business logic here — delegate to `splitio_commons` subdomains
- Don't expose internal implementation details in the public export
