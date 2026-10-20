---
name: write-playwright-e2e
description: Designs and stabilizes Playwright end-to-end tests — Page Object Model, role/data-testid selectors, cross-browser, network mocking, visual regression; used when adding or de-flaking browser tests.
when_to_use: When the user wants end-to-end/browser tests, mentions Playwright, Page Object Model, flaky E2E tests, cross-browser testing, or testing real user flows in a browser.
---

## File layout

Save the skill at `skills/write-playwright-e2e/SKILL.md` with this frontmatter, then the body below verbatim:

```yaml
---
name: write-playwright-e2e
description: Designs and stabilizes Playwright end-to-end tests — Page Object Model, role/data-testid selectors, cross-browser, network mocking, visual regression; used when adding or de-flaking browser tests.
when_to_use: When the user wants end-to-end/browser tests, mentions Playwright, Page Object Model, flaky E2E tests, cross-browser testing, or testing real user flows in a browser.
---
```

---

## When to Use

- Adding a new browser test for a real user flow (login, checkout, search→result, form submit).
- A flow spans pages/redirects/auth and can't be covered by a unit or integration test.
- An existing E2E test is **flaky** (passes locally, fails in CI, or fails ~1 in N runs) and needs de-flaking.
- The user explicitly names Playwright, Page Object Model, cross-browser, or visual regression.

Skip — and reach for `write-tests` (unit/integration) instead — when the logic under test is a pure function, a parser, an API handler, or anything you can drive without a real DOM. E2E is the slowest, most brittle tier; only put a flow here when the value *is* the browser+network+rendering integration. One or two E2E tests per critical flow, not one per assertion.

## Steps

1. **Bootstrap once if Playwright is absent.** Check `package.json` devDeps for `@playwright/test`. If missing: `npm init playwright@latest` (or `npm i -D @playwright/test && npx playwright install --with-deps`). Confirm a `playwright.config.ts` exists; tests live in `e2e/` or `tests/` (match the repo's existing convention — never invent a parallel folder). Add an npm script `"test:e2e": "playwright test"` if none exists.

2. **Set config invariants before writing any test.** In `playwright.config.ts`:
   - `use.baseURL` → so tests call `page.goto('/path')`, never hardcoded hosts.
   - `webServer: { command, url, reuseExistingServer: !process.env.CI }` → Playwright boots/awaits the app itself; no manual "start the server first".
   - `use.trace: 'on-first-retry'`, `screenshot: 'only-on-failure'`, `video: 'retain-on-failure'` → failure forensics without bloating green runs.
   - `expect.timeout` left at default (5s); raise per-assertion only where justified, never globally to mask slowness.
   - `forbidOnly: !!process.env.CI` → a stray `.only` fails CI instead of silently shrinking the suite.

3. **Write one user scenario per `test`, arrange→act→assert.** Name it after the behavior (`'user can reset password from the login page'`), not the implementation. Use `test.describe` to group a feature, `test.beforeEach` for shared navigation/setup. One scenario = one reason to fail; don't chain five unrelated flows into a mega-test where failure 1 hides 2–5.

4. **Select by role/label first, `data-testid` only as fallback — never brittle CSS/text.** Priority order:
   - `page.getByRole('button', { name: 'Submit' })`, `getByLabel`, `getByPlaceholder`, `getByText` for stable user-visible content → these mirror what a user/assistive-tech sees and survive refactors.
   - `page.getByTestId('cart-total')` when there's no accessible handle. If the element lacks one, **add a `data-testid` to the app source** rather than reaching for `.css > .selectors:nth-child(3)`.
   - Banned: deep CSS/XPath chains, `nth-child`, class names from a CSS framework, and matching on copy that translates/changes. These are the #1 source of false failures.

5. **Lean entirely on auto-waiting + web-first assertions — zero manual sleeps.** Every locator action (`click`, `fill`) auto-waits for actionability; every `expect(locator)` retries until the timeout. Write `await expect(page.getByRole('alert')).toBeVisible()`, `toHaveText`, `toHaveURL`, `toBeEnabled`. **Never** `page.waitForTimeout(ms)` / `sleep` — it's either flaky (too short) or slow (too long). To wait on the network, await the round-trip explicitly: `await page.waitForResponse(r => r.url().includes('/api/x') && r.ok())` or `Promise.all([waitForResponse(...), button.click()])`.

6. **Extract reusable flows into Page Objects.** One class per page/major component under `e2e/pages/` (e.g. `LoginPage`). The class takes `page` in its constructor, exposes locators as readonly fields and **intent methods** (`async login(user, pass)`), and returns the next Page Object when navigation crosses pages. Tests then read as prose: `await new LoginPage(page).login(...)`. Assertions stay in the test, not buried in the POM. Promote a flow to a POM the moment a second test needs it — don't copy-paste selectors.

7. **Isolate from the real backend with network interception + fixtures.** For deterministic tests, mock at the network edge: `await page.route('**/api/orders', route => route.fulfill({ json: fixture }))`. Keep payloads in `e2e/fixtures/*.json`. Seed auth via storage state — log in once in a setup project, save `storageState`, and reuse it (`use.storageState`) so most tests skip the login UI. Decide explicitly per suite: mock (fast, deterministic, no env deps) vs. hit a seeded test backend (higher fidelity). Don't half-do it — a test that mocks some calls and lets others hit prod is the worst of both.

8. **Cover cross-browser + viewport via `projects`, not duplicated tests.** Define `projects` for `chromium`, `firefox`, `webkit`, plus mobile via `devices['Pixel 5']` / `devices['iPhone 13']`. The same test file runs across all of them. Gate genuinely engine-specific behavior with `test.skip(browserName === 'webkit', 'reason')` — sparingly, with a written reason. For responsive breakpoints, set `viewport` per project rather than resizing mid-test.

9. **(Optional) Add visual regression where pixels are the contract.** `await expect(page).toHaveScreenshot('checkout.png')` for layout-critical surfaces. Mask dynamic regions (`mask: [page.getByTestId('timestamp')]`), disable animations (`animations: 'disabled'`), and pin a fixed viewport. Generate baselines with `--update-snapshots`, **commit them**, and review the baseline image like code. Use sparingly — snapshots are high-maintenance; don't snapshot pages full of live/random data.

10. **De-flake methodically — retries are a last resort, not a fix.** When a test flakes, run `playwright test --repeat-each=20 <file>` (or `--retries=0` to surface it) to reproduce, then open the **trace** (`npx playwright show-trace`) to see the exact failing step. Root causes, in order of likelihood: a manual sleep masking a real wait; asserting before the network settled; a non-deterministic selector (text/index); shared mutable state between tests; an animation/transition mid-action. Fix the cause. Only after that, set `retries: 2` in CI config as a safety net for genuine infra blips — never to paper over a known race.

11. **Run green across all projects before declaring done.** `npm run test:e2e` (all browsers). Run the new/changed file `--repeat-each=10` to prove non-flakiness. Confirm CI runs headless. Report: which flows are covered, which browsers, and any deliberately skipped engine.

## Common Errors

- **`waitForTimeout` / arbitrary sleeps.** The single biggest cause of flake *and* slowness. There is always a condition to await instead (`expect().toBeVisible`, `waitForResponse`, `waitForURL`). Treat any sleep in an E2E test as a bug.
- **Race on click→assert without awaiting the trigger's effect.** Clicking submit then immediately asserting the next page fails intermittently because navigation/fetch is in flight. Either use a web-first assertion (which retries) or `Promise.all([page.waitForURL('**/success'), submit.click()])`.
- **Brittle selectors.** `nth-child`, framework class names, and copy-text break on the next refactor/translation and produce false failures that erode trust in the suite. Role/label/testid only.
- **Forgetting `await`.** Every Playwright call is async. A missing `await` makes assertions pass vacuously (the promise is truthy) — a test that can never fail. Enable `@typescript-eslint/no-floating-promises` to catch these.
- **`reuseExistingServer` left on in CI**, or no `webServer` block at all → tests race a not-yet-ready app and fail on the first `goto`. Let Playwright own server lifecycle and await `url`.
- **Tests depending on order / shared state.** Each test must set up and tear down its own data; Playwright runs files in parallel and order isn't guaranteed. Cross-test coupling produces "passes alone, fails in suite."
- **Cross-origin `page.route` misses.** A glob like `/api/*` won't match an absolute `https://api.example.com/...`. Use `**/api/**` and verify the route actually fired (route handlers that never match silently fall through to the real network).
- **Uncommitted or machine-specific snapshot baselines.** Visual diffs fail in CI when baselines aren't committed, or were generated on a different OS/font stack. Generate in (or matching) the CI environment and commit them.
- **Global timeout inflation to "fix" flake.** Bumping `expect.timeout` to 30s hides a race and makes every failure take 30s. Fix the wait condition; keep timeouts tight.

## Verify

The work is done when:

- Each test covers exactly one user scenario, named for behavior, structured arrange→act→assert.
- Zero `waitForTimeout`/`sleep`; all waits are web-first assertions or explicit `waitFor*` conditions.
- Selectors are role/label-based, with `data-testid` only as a documented fallback — no positional CSS/XPath or copy-text matching.
- Reused flows live in Page Objects (`e2e/pages/`); duplicated selector blocks have been extracted.
- The suite is deterministic: network mocked via `page.route` + committed fixtures, or pointed at a seeded backend — chosen explicitly, applied consistently.
- `playwright.config.ts` sets `baseURL`, `webServer` (with `reuseExistingServer: !CI`), trace/screenshot/video on failure, and `forbidOnly` in CI.
- Cross-browser coverage exists via `projects` (chromium/firefox/webkit + at least one mobile device) on the same test files.
- New/changed tests pass `--repeat-each=10` with no flake, and the full `npm run test:e2e` is green headless. Any retries are documented as an infra safety net, not a race patch.
- (If used) visual snapshots are masked/animation-disabled, viewport-pinned, and the baselines are committed.
