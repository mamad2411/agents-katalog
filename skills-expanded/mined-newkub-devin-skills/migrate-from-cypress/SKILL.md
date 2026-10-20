---
name: follow-tool-playwright-migrate-from-cypress
description: Migrate an E2E suite from Cypress to Playwright — API mapping, page objects, verify
argument-hint: "[scope]"
related:
  - follow-tool-playwright
  - use-astgrep
  - migration-with-astgrep
  - run-test
  - update-tests
---

## Goal

Migrate the E2E test suite from Cypress to Playwright safely — the suite must be green on Playwright before removing Cypress

## Scope

- Migrate `cypress` → `@playwright/test` covering specs, commands, fixtures, intercepts, config
- Not covered: first-time setup (`workflows/setup-playwright`), component testing with no clear equivalent yet

## Execute

### 1. Plan And Inventory

> Goal: map the affected points before editing

1. Run `/plan` — write the rollback path (the Cypress suite must be green before starting)
2. Run `scan-codebase` to find Cypress usage: `cypress.config.*`, `cypress/e2e/**`, `cy.*` calls, custom commands in `cypress/support/`, `cy.intercept`, fixtures
3. Group specs: simple assertions, auth flows, API intercepts, file upload/download — each group maps differently
4. Read the official migration docs — check Playwright docs when unsure about an API equivalent

### 2. Setup Playwright Alongside

> Goal: install Playwright while Cypress stays in place

1. Follow `workflows/setup-playwright` — install, browsers, config
2. Set `testDir` separate from `cypress/` (e.g. `e2e/`) — both frameworks can run side by side during migration
3. Map config: `baseUrl` → `use.baseURL`, `viewportWidth/Height` → `use.viewport`, `defaultCommandTimeout` → `timeout`/`expect.timeout`, `video`/`screenshotOnRunFailure` → `video`/`screenshot` options

### 3. Map APIs

> Goal: convert `cy.*` to Playwright APIs group by group

1. Navigation/actions: `cy.visit(url)` → `await page.goto(url)`, `cy.get(sel).click()` → `await page.locator(sel).click()` or `getByRole`, `cy.get().type()` → `locator.fill()`
2. Assertions: `cy.get().should('be.visible')` → `await expect(locator).toBeVisible()`, `.should('have.text')` → `toHaveText()`, `.should('have.attr')` → `toHaveAttribute()` — use auto-waiting web-first assertions
3. Network: `cy.intercept()` → `page.route()` or `context.route()`
4. State: `cy.clearCookies()`/`localStorage` → context methods or `storageState` config
5. Custom commands → Playwright fixtures (`test.extend()`) or page object methods — never create global commands
6. Use `/use-astgrep`/`/migration-with-astgrep` for bulk rename patterns — one commit per pattern

### 4. Extract Page Objects

> Goal: structure locators/actions for maintainability

1. Convert Cypress custom commands and repeated selectors into Page Object classes
2. Convert selectors to locators: `getByRole` > `getByText`/`getByLabel` > `getByTestId` > CSS
3. Don't copy `.should('exist')` chains verbatim — Playwright locators are lazy and auto-wait

### 5. Verify And Cleanup

> Goal: suite green on Playwright, then remove Cypress

1. Run `bunx playwright test` — migrated specs must all be green; compare coverage against the original Cypress suite
2. Use `--last-failed` to re-run only failures; run `/run-test` (e2e) for the final confirmation
3. Once green: delete `cypress`, `cypress.config.*`, the `cypress/` dir, eslint plugins — in a separate commit
4. Run `/deep-review-codebase` to check for leftover `cy.` → then `/report-before-after` and `/ship`

## Rules

- Never mix migration with feature work — one commit per step
- The Cypress suite must be green before migrating — it is the reference behavior
- Never use `page.waitForTimeout()` in place of Cypress auto-retry — use web-first assertions
- Every migrated spec must assert the equivalent of before — never weaken assertions to pass
- Specs relying on Cypress-only features (e.g. component testing) → a clear TODO list, don't force them

## Expected Outcome

- The E2E suite runs green on Playwright with coverage equivalent to before
- Cypress dependencies/config removed in a separate commit
- Locators/page objects follow Playwright best practices
