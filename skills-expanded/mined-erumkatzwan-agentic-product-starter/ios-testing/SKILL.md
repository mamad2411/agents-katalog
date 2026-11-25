---
name: ios-testing
description: Use when writing or fixing unit tests, UI tests or Maestro end-to-end tests in the iOS app (AgenticApp), or when a pull request check is red.
---

# iOS testing

Every story ships with all three layers. Pull requests cannot merge unless all checks are green.

| Layer | Where | Runs | Command |
|---|---|---|---|
| Unit | `AgenticAppTests/` | View models, services, networking, flags | `make test-unit` |
| UI | `AgenticAppUITests/` | Real app on the simulator with fixture data | `make test-ui` |
| End-to-end | `e2e/flows/*.yaml` (Maestro) | Full user journeys on the simulator | `make e2e` |

## Rules

- Unit tests use the test doubles in `AgenticAppTests/TestDoubles.swift` (`MockAPIClient`, `StubItemsRepository`, `StubURLProtocol`). No real network.
- Name tests `test<Behaviour>` and structure them arrange / act / assert.
- UI and end-to-end tests launch with `-uiTesting`, so the app uses `FixtureAPIClient` and `Resources/Fixtures/*.json`.
- Find elements by `accessibilityIdentifier`, never by position or styling.
- Flip feature flags in tests with launch arguments, for example `-FF_settings NO`.
- Coverage gate: logic coverage (views, design system and app wiring excluded) must stay at or above 70%.

## When a check is red

- `iOS lint` – run `make lint` and fix every warning.
- `iOS spelling` – run `make typos`; fix the word or add it to `_typos.toml` if it is a real term.
- `iOS unit tests and coverage` – run `make test-unit`; add tests if coverage dropped.
- `iOS UI tests` / `iOS end-to-end tests` – run locally, then open the `.xcresult` artifact from the failed run.
