---
description: Playwright test and Page Object conventions (architecture, assertions, locators, reliability, test data)
globs: tests/**/*.ts, pages/**/*.ts
alwaysApply: false
---

# Playwright Test & Page Object Rules

## Architecture
- Use **Page Object Model** for all UI interactions.
- **Page Objects**: encapsulate locators; expose user actions (not raw selectors); avoid assertions except for page readiness.
- Inject Page Objects via **Playwright fixtures**.
- Prefer reusable state (e.g. authenticated session fixture).
- Write test titles that **describe behavior** clearly.
- Prioritize clean, maintainable architecture.

## Assertions
- Use **tolerant assertions** when UI text may vary (e.g. `toContainText`, regex).
- Use **soft assertions** when appropriate so the test can continue and report multiple failures.

## Parametrization
- Avoid copy-paste tests; **extract reusable test data** into fixtures or constants.
- Prefer `test.describe` + parameters or shared fixtures over duplicated specs.

## Locators
- Prefer **accessibility-first** locators (`getByRole`, `getByLabel`, `getByText`, `getByPlaceholder`).
- Avoid CSS selectors tied to styling or layout.

## Reliability
- **Never** use arbitrary `setTimeout` or fixed waits; rely on **Playwright auto-waiting**.
- Ensure tests can run **in parallel** and do **not** depend on execution order.
- Reset or isolate state between tests (e.g. fresh session, clean data).

## Test Data
- **Do not** hardcode credentials or environment values.
- Use **environment variables** for configuration; centralize access (e.g. `test-data/`, config).
- Prefer **deterministic** inputs for stable, repeatable tests.
