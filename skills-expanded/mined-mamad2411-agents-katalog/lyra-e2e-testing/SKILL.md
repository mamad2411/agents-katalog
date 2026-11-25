---
name: lyra-e2e-testing
description: "End-to-end testing discipline for Playwright, Cypress, Selenium, and WebdriverIO. Use when writing, reviewing, or debugging browser tests."
compatibility: "Playwright recommended. Principles apply to Cypress, Selenium, WebdriverIO. Pairs with lyra-tdd (unit layer) and lyra-ci-cd (pipeline)."
---

# lyra-e2e-testing

## What it does

End-to-end tests verify user journeys through a real browser — login, checkout, the things a unit test cannot reach. This skill keeps that layer thin: accessible locators over test IDs, auto-waiting over sleeps, per-test data over shared state, sharding with merged reports over slow serial runs. It targets Playwright but the rules transfer to Cypress, Selenium, and WebdriverIO. Reach for it when writing, reviewing, or debugging browser tests, wiring e2e into CI, or eliminating flakiness. It assumes `lyra-tdd` covers the unit layer and `lyra-ci-cd` owns the pipeline graph.

## The rules

### 1. Test the journey, not the component tree

E2E covers only what unit and integration tests cannot — user journeys, cross-system integration, real-browser rendering. Target roughly 70% unit, 20% integration, 10% e2e; retesting unit behavior at the browser burns CI minutes for zero new confidence.

```typescript
// bad:  verifies math a unit test already covers
test("cart total", async ({ page }) => {
  await page.goto("/cart");
  await expect(page.getByText("Total: $6")).toBeVisible();
});
// good: a journey only a real browser can verify
test("user checks out a 2-item cart", async ({ page }) => {
  await page.getByRole("button", { name: /add .*widget.* to cart/i }).click();
  await page.getByRole("button", { name: /checkout/i }).click();
  await expect(
    page.getByRole("heading", { name: /order confirmed/i }),
  ).toBeVisible();
});
```

### 2. Reach for accessible locators first; reserve test IDs for last-resort cases

`getByRole`, `getByLabel`, and `getByText` mirror how users and assistive tech find elements, survive refactors, and surface a11y gaps as test failures. Use `getByTestId` only when no accessible query works — a third-party widget with no role — with a comment saying why; raw CSS and XPath couple tests to markup no user reads.

```typescript
// bad:  await page.locator('[data-testid="login-submit"]').click()
// good: await page.getByLabel(/email/i).fill('user@example.com')
//       await page.getByLabel(/password/i).fill('hunter2')
//       await page.getByRole('button', { name: /sign in/i }).click()
```

### 3. Assert what the user sees, never DOM structure or class names

Assert text, visibility, role, and state — not class names, store shape, or internal attributes. A behavior-preserving refactor must not break a test; if it does, the test was coupled to implementation.

```typescript
// bad:  await expect(page.locator('.nav-item.is-selected')).toHaveClass(/is-selected/)
// good: await expect(page.getByRole('link', { name: /dashboard/i })).toHaveAttribute('aria-current', 'page')
```

### 4. No sleeps — let locators auto-wait and assertions retry

`waitForTimeout` manufactures flakiness and slow suites; Playwright locators auto-wait, and `expect(locator).toBeVisible()` retries until timeout. Wait for a specific condition — a visible element, a network response — never for a clock.

```typescript
// bad:  await page.waitForTimeout(2000)
//       await page.getByRole('button', { name: /submit/i }).click()
// good: await page.getByRole('button', { name: /submit/i }).click()
//       await expect(page.getByRole('alert', { name: /saved/i })).toBeVisible()
```

### 5. Retries are a safety net, not a fix

CI may set `retries: 2` to absorb environmental flake, but a test that needs retries to pass is in debt. Track flake rate; anything above 2% gets reproduced with `--repeat-each=20 --workers=1`, root-caused, and fixed — or quarantined with `test.fixme` and an issue link.

```typescript
// bad:  test('flaky checkout', async ({ page }) => { /* retried 3x in CI, never fixed */ })
// good: test('checkout flow', async ({ page }) => {
//         test.fixme(true, 'Flaky ~15% — race on inventory refresh, issue #511')
//         /* ... */
//       })
```

### 6. No shared state — each test seeds and cleans its own data via an API factory

Every test runs in a clean context, seeds through the API (never the UI of a previous test), and cleans up in `afterEach`. Hardcoded `"test-user-1"` collides across workers and branches, so factory output should carry a unique suffix.

```typescript
// bad:  test('create item', ...)        // leaves data behind
//       test('list shows 1 item', ...)   // depends on the first having run
// good: test('list shows created item', async ({ apiFactory, page }) => {
//         const item = await apiFactory.create({ name: `widget-${crypto.randomUUID()}` })
//         await page.goto('/items')
//         await expect(page.getByRole('listitem', { name: item.name })).toBeVisible()
//       }) // apiFactory fixture deletes everything it created in afterEach
```

### 7. No `expect(true)`, no swallowed failures, no smoke tests in the merge gate

A test whose only assertion is `expect(true)` is not a test, and a `try/catch` that swallows failures manufactures green. A test that loads a page and asserts nothing observable is smoke — keep it if you want, but exclude it from the merge gate.

```typescript
// bad:  test('checkout works', async ({ page }) => {
//         try { await page.getByRole('button', { name: /pay/i }).click() } catch {}
//         expect(true).toBe(true)
//       })
// good: test('checkout shows confirmation', async ({ page }) => {
//         await page.getByRole('button', { name: /pay/i }).click()
//         await expect(page.getByRole('heading', { name: /order confirmed/i })).toBeVisible()
//       })
```

### 8. One journey per test; split at journey boundaries

Each test exercises one user behavior with a clear pass/fail. A test that logs in, browses, adds to cart, checks out, and reviews is five tests stitched into one — when it fails you cannot tell which step broke.

```typescript
// bad:  test('full shopping experience', async ({ page }) => { /* 200 lines */ })
// good: test.describe('checkout', () => {
//         test('adds item to cart', async ({ page }) => { /* ... */ })
//         test('completes payment', async ({ page }) => { /* ... */ })
//       })
```

### 9. Page Objects for shared flows, obeying the same locator rules

Build a Page Object when three or more tests repeat the same flow (login, navigation, a multi-step form); one-off locators stay inline. A Page Object that hides `[data-testid]` behind a friendly name has not fixed the coupling — it has renamed it.

```typescript
// bad:  class CartPage {
//         readonly checkoutBtn = this.page.locator('[data-testid="cart-checkout-v2"]')
//       }
// good: class CartPage {
//         readonly checkoutBtn = this.page.getByRole('button', { name: /checkout/i })
//         async checkout() { await this.checkoutBtn.click() }
//       }
```

### 10. `fullyParallel` by default; serial is an exception with a comment

`fullyParallel: true` is the default. A test that cannot run in parallel is breaking rule 6 — fix the isolation, do not disable parallelism. `test.describe.serial` is allowed with a comment, never as a habit.

```typescript
// bad:  test.describe.configure({ mode: 'serial' }) // no reason given
// good: // serial: legacy shared DB fixture cannot reset between tests — migrating, issue #640
//       test.describe.configure({ mode: 'serial' })
```

### 11. Shard across runners, then merge the reports

For suites over five minutes, shard with `--shard=i/n`, upload each shard's blob report, and run a final job that merges them into one verdict and one HTML report. Sharding without merging yields N partial reports instead of an answer.

```yaml
strategy:
  matrix:
    shardIndex: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shardIndex }}/4
  - uses: actions/upload-artifact@v4
    if: always()
    with: { name: blob-report-${{ matrix.shardIndex }}, path: blob-report }
merge:
  needs: [shard]
  steps:
    - uses: actions/download-artifact@v4
    - run: npx playwright merge-reports --reporter html ./all-blob-reports
```

### 12. Capture screenshot, video, and trace on every failure

Configure once in `playwright.config`. A failed test without a trace is debug-by-guessing; the minutes saved by disabling capture are the hours lost debugging.

```typescript
use: {
  trace: 'on-first-retry',
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

_Part of the [skill collection](../README.md)._