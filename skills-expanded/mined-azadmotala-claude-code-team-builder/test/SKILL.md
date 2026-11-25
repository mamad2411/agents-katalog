---
name: test
description: Run the TenantFlow test suite. Vitest unit tests and Playwright e2e tests.
---

# Test

Runs the test suite for TenantFlow.

## Usage
- `/test` — run all tests
- `/test --unit` — unit tests only (faster)
- `/test --e2e` — end-to-end tests only

## Workflow

1. **Install/verify dependencies** — `npm install` if package-lock has changed
2. **Unit + integration tests** — `npm run test`
3. **E2E tests** — `npx playwright test` (requires dev server running or staging URL)
4. **Report** — summarize pass/fail counts; if failures, show the failing test names and errors
5. **If failures**: suggest likely causes and fixes before asking user what to do

## Project specifics
- Test framework: Vitest (unit/integration) + Playwright (e2e)
- Test directory: `src/**/*.test.ts` + `e2e/`
- Coverage threshold: 80%
- Critical tests: tenant isolation queries, Stripe webhook handlers, invoice generation
