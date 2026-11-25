---
name: android-testing
description: Use when writing or fixing unit tests, Compose UI tests or Maestro end-to-end tests in the Android app (AgenticApp), or when a pull request check is red.
---

# Android testing

Every story ships with all three layers. Pull requests cannot merge unless all checks are green.

| Layer | Where | Runs | Command |
|---|---|---|---|
| Unit | `app/src/test/` | View models, services, networking, flags (JVM, no emulator) | `make test-unit` |
| UI | `app/src/androidTest/` | Real app on the emulator with fixture data (Compose UI test) | `make test-ui` |
| End-to-end | `e2e/flows/*.yaml` (Maestro) | Full user journeys on the emulator | `make e2e` |

## Rules

- Unit tests use the test doubles in `app/src/test/.../TestDoubles.kt` (`FakeApiClient`, `FakeAuthService`, `FakeItemsRepository`, `FakePush`). No real network: `ApiClientTest` fakes HTTP with an OkHttp interceptor.
- Use `runTest` for suspend functions. Name tests by behaviour (`signInSavesTheToken…`) and structure them arrange / act / assert.
- UI and end-to-end tests launch with the extra `uiTesting=true`, so the app uses `FixtureApiClient` and `assets/fixtures/*.json`.
- Find elements by test tag (`onNodeWithTag`, Maestro `id:`), never by position or styling. Tags are exposed as resource IDs, so Maestro uses the same IDs as on iOS.
- Wait with `waitUntilAtLeastOneExists`, never `Thread.sleep`.
- Flip feature flags in tests with launch extras, for example `launch("FF_settings" to false)`.
- Coverage gate: logic coverage (screens, design system and Android glue excluded, see `scripts/check-coverage.py`) must stay at or above 70%.

## When a check is red

- `Android lint` – run `make lint`; fix every ktlint and Android Lint warning. `ktlint -F` fixes formatting.
- `Android spelling` – run `make typos`; fix the word or add it to `_typos.toml` if it is a real term.
- `Android unit tests and coverage` – run `make test-unit`; add tests if coverage dropped. The HTML report is in the job's artifacts.
- `Android UI tests` / `Android end-to-end tests` – run locally on an emulator, then open the test report artifact from the failed run.
