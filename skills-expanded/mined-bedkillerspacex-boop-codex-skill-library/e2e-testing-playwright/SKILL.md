---
name: e2e-testing-playwright
description: >
  Playwright end-to-end testing strategy: critical journeys, stable selectors,
  fixtures, isolation, web-first assertions, trace/video on failure, and CI
  discipline. Use when Playwright, e2e tests, end-to-end, browser tests, page
  object, locator strategy, or flaky UI suites. Complements
  integration-test-strategy and unit-testing-style; not for pure unit matrices
  or Pact contracts alone.
---

# E2E Testing with Playwright

## Scope And Authorization

- **In scope:** apps and environments you own or have written permission to test (dev/stage/ephemeral previews).
- **Out of scope:** hammering production with destructive journeys, scraping third-party sites, or storing real customer PII in test artifacts.
- Prefer dedicated test accounts, seeded data, and non-prod base URLs.
- Redact auth cookies, tokens, and personal data from traces, videos, and CI logs.
- Pair implementation changes with `code-quality-standards`.

## When To Use

- Adding or repairing Playwright suites for critical user journeys (login, checkout, admin, multi-step forms).
- Reducing flake: racey clicks, brittle CSS selectors, shared mutable state, network timing.
- Wiring Playwright into CI with shards, retries only where justified, and failure artifacts.
- Choosing locators, fixtures, Page Object / fixture patterns, and API setup vs full UI setup.
- Debugging with `trace.zip`, screenshots, video, and headed/debug mode.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Unit/component tests only | `unit-testing-style` |
| Service/API contract tests | `integration-test-strategy` or Pact-related skills |
| Visual regression program | visual/snapshot tooling skill if catalogued |
| Accessibility audit depth | `accessibility-a11y-checklist` |
| Implementation quality baseline | `code-quality-standards` |
| Load/perf under concurrent users | performance/load testing skill |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Journey selection | Cover money/security paths first; skip pure cosmetic smoke if budget is tight |
| Selectors | Prefer `getByRole`, `getByLabel`, `getByTestId`; avoid nth/CSS hierarchy |
| Isolation | Fresh storage state or context per suite; no order-dependent suites |
| Assertions | Web-first (`expect(locator).toBeVisible()`) not fixed `sleep` |
| Data | Seed via API/DB helpers; never rely on leftover UI state from prior tests |
| CI | Shard by file; upload trace on first retry failure; pin browser versions |

## Workflow

### 1. Confirm scope and success criteria

1. List critical journeys (happy path + one authz-negative per sensitive action).
2. Name environments, base URLs, and whether tests may mutate shared stage data.
3. Define green criteria: suite duration budget, max flake rate, required browsers.

### 2. Inventory current Playwright setup

1. Read `playwright.config.ts` (or `.js`): projects, retries, workers, `trace`/`video`/`screenshot`, `baseURL`, `storageState`.
2. Inventory specs under `tests/` / `e2e/`; note shared fixtures and global setup/teardown.
3. Check CI job: install browsers, cache, shard count, artifact retention.

### 3. Baseline flake and coverage

1. Run the suite twice locally or in CI; record intermittent failures and wall time.
2. Tag tests that hit live third parties (OAuth, payments sandboxes) vs fully mocked.
3. Capture one failing `trace.zip` for a known flake as a reference.

### 4. Stabilize selectors and structure

1. Prefer role/label locators; add stable `data-testid` only where semantics are weak.
2. Encapsulate pages in fixtures or thin page modules; keep assertions in the test.
3. Replace `page.waitForTimeout` with auto-waiting assertions or `waitForURL` / network idle only when necessary.
4. Use `test.step` for readable traces on multi-step journeys.

```ts
// Prefer role-based locators + web-first expect
import { test, expect } from '@playwright/test';

test('user can complete checkout', async ({ page }) => {
  await page.goto('/cart');
  await page.getByRole('button', { name: 'Checkout' }).click();
  await expect(page.getByRole('heading', { name: 'Payment' })).toBeVisible();
  await page.getByLabel('Card number').fill('4242424242424242');
  await page.getByRole('button', { name: 'Pay' }).click();
  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

### 5. Isolate state and auth

1. Use `storageState` for a pre-authenticated user when login is not under test.
2. Create data via API in `beforeEach` / fixture; delete or use unique IDs per worker.
3. Parallel-safe: no shared email/username without a worker index suffix.
4. Mock or stub third-party iframes when the contract is out of scope.

```ts
// playwright.config.ts (excerpt)
export default defineConfig({
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 4 : undefined,
  use: {
    baseURL: process.env.BASE_URL ?? 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

### 6. Verify with evidence

```bash
# Install browsers once (CI cache after)
npx playwright install --with-deps chromium

# Run suite
npx playwright test

# Single file, headed debug
npx playwright test tests/checkout.spec.ts --debug

# Show last HTML report
npx playwright show-report

# Open a failure trace
npx playwright show-trace test-results/**/trace.zip
```

1. Confirm retries are not hiding systematic bugs (investigate any test that needs retry often).
2. Confirm CI uploads `blob`/`html` report and traces for failed shards.
3. Gate merge only on owned app URLs; never point default config at production.

### 7. CI hardening and handoff

1. Start app + dependencies in CI (compose, preview deploy, or webServer in config).
2. Shard: `npx playwright test --shard=${SHARD}/${TOTAL}`.
3. Document how to reproduce a failure from a PR artifact.
4. Apply `code-quality-standards` to shared fixtures and helpers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Selectors | `getByRole('button', { name: 'Save' })` | `.css-x7 > div:nth-child(3)` |
| Waiting | `await expect(row).toBeVisible()` | `await page.waitForTimeout(5000)` |
| Auth | Dedicated test user + storageState | Shared admin password in repo |
| Isolation | Unique email per worker | All workers edit the same row |
| CI | Trace on first retry + artifacts | Silent flake with retries=3 forever |
| Scope | Stage/ephemeral | Unbounded prod traffic as “e2e” |

## Output Checklist

- [ ] Critical journeys listed with owner and env
- [ ] Config: baseURL, trace/screenshot/video, parallel settings reviewed
- [ ] Selectors favor roles/labels/testids; no sleep-based waits
- [ ] Auth and data isolation are parallel-safe
- [ ] Suite run with evidence (report/trace) and flake notes
- [ ] CI shards, browser install, and artifact upload documented
- [ ] Secrets/PII redacted from traces and logs
- [ ] `code-quality-standards` applied to helpers/fixtures
- [ ] Residual flake risks and next review noted

## Rules

- Authorized environments only; do not treat production as a free load generator.
- Prefer deterministic setup (API seed) over long UI prerequisites.
- Keep retries low; fix root causes of flake.
- Never commit real customer data or long-lived production credentials into test state.
- Focus this skill on Playwright e2e; route pure unit/contract work elsewhere.
- Redact tokens and cookies from shared failure artifacts.
