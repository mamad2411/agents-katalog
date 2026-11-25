---
name: e2e-test-design
description: Chooses the few user journeys that deserve end-to-end coverage and writes stable browser tests with resilient locators and no fixed waits.
---

# E2E test design

Cover the journeys that matter with a handful of dependable tests. Everything else belongs in faster layers.

## Steps

1. Choose journeys. Ask what failing would cost: signup and login, checkout or payment, the core create-and-save action, permission boundaries. Aim for 5 to 15 tests. Skip anything a unit or API test can cover.
2. Check the existing tool and config (Playwright, Cypress, WebdriverIO) and follow it. Do not introduce a second runner.
3. Write each test as one user story with a single outcome. Name it for the result: "a returning customer can pay with a saved card".
4. Locators: prefer role and accessible name (`getByRole("button", { name: "Pay" })`), then label or text, then a dedicated `data-testid`. Never use generated class names or long CSS paths.
5. Waiting: rely on the tool's auto-wait and assert on the visible outcome (`expect(...).toBeVisible()`). No `sleep` or fixed timeouts. Wait for a specific network response only when the UI shows nothing.
6. Data: create it per test through the API or a seed helper, with unique values, and clean up. Never depend on another test having run first. Log in through a saved session state, not the UI, except in the login test itself.
7. External services: stub payment, email and analytics at the network layer; keep one thin test against the real sandbox if needed.
8. Run each new test 10 times, and in parallel, before committing. Enable traces and screenshots on failure, and retries only in CI.

## Rules

- One test, one journey; no logic branches inside tests.
- Do not assert on pixel details or copy that changes often.

## Report

Journeys chosen and rejected with reasons, tests written, flake check results, and run time.
