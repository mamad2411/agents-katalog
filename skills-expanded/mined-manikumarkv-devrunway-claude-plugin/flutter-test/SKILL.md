---
name: flutter-test
description: Flutter testing standards — the harness first (pumpApp, ProviderContainer, hand-written fakes, seeded config, in-memory cache), substituting at the service interface rather than the transport, which test type belongs to which layer, the four screen states with a retry that re-fetches, golden tests with loaded fonts and frozen time on one platform, consumer-driven contract tests against a committed schema, integration journeys, performance budgets, and a coverage ratchet. Load when writing or reviewing tests, fakes, fixtures, goldens, or integration journeys.
user-invocable: false
stack: testing/flutter-test
paths:
  - "**/test/**/*.dart"
  - "**/integration_test/**/*.dart"
  - "**/*_test.dart"
---

Full standards in [flutter-test.md](flutter-test.md). Always-on summary:

**Scope:** *how* things are tested. *What* is tested belongs to the layer that owns it — the service contract is `api-style/dio`, provider lifetime and `AsyncValue` are `state/riverpod`, the four screen states are `frontend/flutter-ui`, model shape is `language/dart-models`.

**Build the harness before the first test.** Apps end up untested because nothing was substitutable, not from indifference — the first test costing a day is the actual cause.
- `test/support/harness.dart` exposes `pumpApp` — wraps the widget under test in `ProviderScope` + the app theme + the `AppLocalizations` delegates, and takes an `overrides` list — and `createContainer`, a `ProviderContainer` seeded with a test config, an in-memory cache and fake services, registered with `addTearDown(container.dispose)`.
- Fakes are hand-written classes implementing the service contract, under `test/support/fakes/`. They record their calls and the `CancelToken` they were handed.
- Delete the generated `widget_test.dart` counter scaffold on the first commit. It tests Flutter, not the app, and its presence says the suite was never started.

**Substitute at the service interface, never at the transport.** A test that stubs raw HTTP responses is coupled to the wire format and breaks on refactors that changed no behaviour. Override the service provider with a fake that implements the contract.

**Test type per layer:**

| Subject | Test | Must cover |
|---|---|---|
| Model | unit | round-trip, missing optional fields, unknown enum value, malformed payload |
| Notifier | `ProviderContainer` | state transitions, the error path, disposal cancelling in-flight work |
| Screen | widget | loading, error **with a retry that re-fetches**, empty, data, semantics |
| Design-system component | golden | light, dark, 200% text scale (`TextScaler.linear(2.0)`) |
| User journey | integration | a handful, seeded and torn down |

**Goldens:** load fonts explicitly (`loadAppFonts()` from `flutter_test_config.dart`) or text renders as boxes in CI. Freeze clock, randomness, images and animations. Generate *and* verify inside one container image — font rasterization differs between macOS and Linux. Zero pixel difference: a golden matches the committed image exactly or it fails; softening the comparison hides exactly the regressions goldens exist to catch. Diffs are reviewed as images.

**Journeys:** a handful, not thirty. Dedicated environment, data seeded in `setUp` and destroyed in `tearDown`, never production. Wait on a condition (`pumpUntil`), never on a duration — a sleep is a flake with a timer. Flakes are quarantined with an owner, then fixed or deleted. Runs on merge and nightly, never in the PR gate.

**Contract:** the schema is versioned and committed under `contract/` (a spec fetched at build time makes builds unreproducible); models are generated from it where it is published; a scheduled job diffs committed against deployed; fixtures come from the spec's own examples; unknown fields are ignored and unknown enum values fall back — with a test proving both.

**Perf budgets:** profile mode, physical device, one pinned baseline device. Absolute ceilings *and* per-PR deltas — a slow creep never breaches a ceiling until it is too late to bisect. On merge and nightly, not in the gate.

**Coverage:** reported on every PR against a floor that only rises. An absolute target argued up front never gets set; a ratchet works from wherever you are.

**Related:** `state/riverpod`, `api-style/dio`, `frontend/flutter-ui`, `language/dart-models`, `ci/flutter-release`.
