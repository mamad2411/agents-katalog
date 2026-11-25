---
name: e2e-web-testing
description: Playwright conventions for reliable end-to-end web tests — user-visible selectors, per-test isolation, storageState auth, waiting discipline, critical-path focus, evidence on failure, and a flaky-test policy. Use when writing or reviewing e2e tests for a React or Next.js web app.
---

# E2E Web Testing (Playwright)

E2E tests exist to prove critical user journeys work in a real browser. They are expensive and, done wrong, flaky — a flaky suite is worse than no suite because the team learns to ignore red. Optimize for reliability and signal, not coverage count.

## Selectors — target what the user sees

Query the accessibility tree, never brittle structure:

- Prefer `getByRole('button', { name: 'Check out' })`, `getByLabel('Email')`, `getByText`, `getByPlaceholder`.
- Use `getByTestId` only when no accessible name exists (add a `data-testid` in that case — it also improves a11y-adjacent stability).
- **Never** use CSS class chains, nth-child, or XPath. They break on every refactor and test nothing a user cares about.

```ts
// good
await page.getByRole('link', { name: 'Cart' }).click();
await expect(page.getByRole('heading', { name: 'Your order' })).toBeVisible();

// bad — brittle, meaningless
await page.locator('.nav > ul > li:nth-child(3) a').click();
```

## Isolation — fresh state per test

Each test starts from a known state and shares nothing with its neighbors:

- Seed data through the **API or DB fixtures**, not by clicking through the UI. UI setup is slow, flaky, and couples unrelated features.
- Create per-test unique data (email with a random suffix, unique SKU) so parallel runs don't collide.
- Tear down or namespace what you create. Never depend on data left by a previous test or a previous run.

## Auth via storageState

Log in once in a setup project, save the authenticated context, and reuse it — do not drive the login form in every test.

```ts
// global setup
await page.getByLabel('Email').fill(user.email);
await page.getByLabel('Password').fill(user.password);
await page.getByRole('button', { name: 'Sign in' }).click();
await page.context().storageState({ path: 'auth/user.json' });

// test file
test.use({ storageState: 'auth/user.json' });
```

Keep separate storageState files per role for the authz matrix.

## Waiting discipline

- Use **web-first assertions** — `expect(locator).toBeVisible()`, `.toHaveText()`, `.toHaveURL()` — which auto-retry until the condition holds or times out.
- **Never** `page.waitForTimeout(ms)` / hard sleeps. A fixed sleep is either too short (flaky) or too long (slow), never right.
- Wait on state, not time: `await expect(spinner).toBeHidden()`, `await page.waitForResponse(...)` for a specific request.
- Assert on outcomes (URL, visible content), not on internal implementation timing.

## Cover the critical paths, not everything

E2E is for journeys that must never break: sign-up/login, checkout/payment, the core create-read flow of the product. Push field-level validation, formatting, and branch logic down to unit/component tests where they run in milliseconds. A focused 30-test suite that always tells the truth beats 400 tests nobody trusts.

## Evidence on failure

Configure the runner to capture proof automatically so a failed CI run is self-explanatory:

```ts
use: { trace: 'on-first-retry', screenshot: 'only-on-failure', video: 'retain-on-failure' }
```

Attach the trace/screenshot to any bug you file (see `bug-report-standards`).

## Parallelism & CI stability

- Tests must be independent enough to run fully parallel (`fullyParallel: true`).
- Pin browser versions in CI; run against a seeded, ephemeral environment.
- Set `retries: 1` in CI to absorb genuine infrastructure blips — but treat a test that only passes on retry as flaky (below), not fixed.
- Keep total wall-clock time visible; a suite that takes 40 minutes stops being run.

## Flaky-test policy

A test that passes and fails on identical code is a defect. When one appears:

1. **Quarantine** it (`test.fixme` / a `@flaky` tag excluded from the gate) so it stops blocking merges.
2. **File a linked fix issue** immediately with the failing trace attached.
3. Fix the root cause (usually a missing web-first assertion or shared state), then un-quarantine.

Never silently delete a flaky test and never `retry` your way to green as a permanent fix — that hides the bug the test was catching.

## Anti-patterns

- CSS/XPath selectors; asserting on class names.
- `waitForTimeout` anywhere.
- Logging in through the UI in every test instead of `storageState`.
- Tests that must run in a specific order or share data.
- Screenshots-off in CI, so failures are undebuggable.
- Deleting flaky tests to make the build green.
