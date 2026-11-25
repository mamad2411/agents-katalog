---
name: e2e-flow
description: Author a browser end-to-end (e2e) test for a critical user journey — stable selectors, web-first waits, deterministic data. Full-stack UI flows, not unit tests or service contracts.
---

# e2e-flow

> Test the journey a user actually takes through the running app — the few flows whose breakage is a Sev. Not the whole UI, not every edge; the money paths.

## When to use

- A critical user journey (sign-up, checkout, the core loop) needs protection against full-stack regressions.
- The user asks for browser/e2e/Playwright/Cypress tests of a flow.
- A workflow invokes `polymath-test-automation:e2e-flow`.

This authors *browser, full-stack* flows. It is not unit testing (`polymath-qa:unit-tests`), service-boundary/contract testing (`polymath-qa:integration-contract`), or load testing (`polymath-test-automation:load-test`).

## Inputs

- The journey (the user goal and its happy path), and the 1–2 failure paths worth guarding.
- The app URL / how to launch it, and how to seed deterministic test data.

## Procedure

1. **Pick the journeys** — only the flows whose failure is a serious incident. Resist testing every page.
2. **Stabilise selectors** — prefer role + accessible name or `data-testid`; never brittle CSS/nth-child or visible-text that copy edits will break.
3. **Web-first waits** — assert on state (element visible/enabled, URL, network idle); no fixed `sleep`. Flake starts here.
4. **Deterministic data** — seed/reset per test (API or fixture); never depend on prod-like shared state or test order.
5. **One journey per spec**, with a clear arrange → act → assert; isolate auth/setup into reusable fixtures.
6. **Trace on failure** — capture screenshot/trace/video so a CI failure is debuggable.
7. Output the spec(s) and the run command; note the data seeding and any required services.

## Quality bar

- Every wait is state-based; the suite has no `sleep`/arbitrary timeout.
- Selectors are role/test-id based and survive a copy or layout change.
- Each spec seeds its own data and passes regardless of run order.
- Only critical journeys are covered — the suite stays fast enough to gate a PR.
