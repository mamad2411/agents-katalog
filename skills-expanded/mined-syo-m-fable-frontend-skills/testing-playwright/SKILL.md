---
name: testing-playwright
description: Playwright E2E conventions — locators, web-first assertions, isolation, network stubbing, flake prevention. Use when writing or fixing E2E tests or playwright.config. 日本語の依頼例:「E2Eテスト書いて」「Playwright」「ブラウザテスト」「ユーザー操作の通しテスト」「テストが不安定/flaky」。
---

# Playwright

E2E tests cover critical user journeys end-to-end (signup, checkout, the money paths) — not every permutation. Component-level behavior belongs in Storybook/Vitest.

## Locators — user-facing only

- Priority (same list as `testing-vitest`): `getByRole(…, { name })` > `getByLabel` > `getByText` > `getByTestId` (last resort). Reaching for `getByPlaceholder` is a smell — the input probably lacks a label (see `a11y`); fix the markup instead.
- Never CSS/XPath selectors tied to DOM structure or generated class names (`.css-x91kb`) — they encode implementation, not behavior.
- Scope with `locator.filter()` / chaining instead of `nth()` indexes when possible.

## Web-first assertions — the anti-flake core

- `await expect(locator).toBeVisible() / toHaveText() / toHaveCount()` — these auto-retry until timeout. Use them for ALL state checks.
- **Banned:** `page.waitForTimeout()`, `expect(await locator.isVisible())` (no retry), manual polling loops. A hard wait is always a hidden race.
- Wait for meaning, not mechanics: assert the UI state you need next, rather than `waitForLoadState('networkidle')`.

## Isolation & auth

- Every test independent: own data, no ordering, parallel-safe. A test must pass alone via `--repeat-each=2` and with the full suite sharded.
- Auth once per worker via a setup project + `storageState`, not a UI login in every test. Test the login flow itself in exactly one spec.
- `storageState` files contain live session tokens: keep them in `playwright/.auth/` and **gitignore that directory**; authenticate only dedicated, ephemeral test accounts — never real users or production credentials.
- Create test data via API/seed scripts in fixtures, not by clicking through the UI; clean up in the fixture teardown.

## Fixtures over Page Objects

- Encode app-specific setup as custom fixtures (`test.extend`) — authenticated page, seeded user, feature flags.
- Keep page helpers lightweight: functions/classes wrapping *actions* (`checkout.fillShipping(data)`), not assertion museums. Assertions live in tests.

## Network

- True E2E (against real backend) for the few critical paths; `page.route()` stubbing for hard-to-trigger states (server errors, empty lists, slow responses).
- Never stub the thing the test exists to verify.

## Config

- `webServer` block to build+serve the app — tests own their server lifecycle, locally and in CI.
- CI: `retries: 2`, `trace: 'on-first-retry'`, `forbidOnly: true`, sharding for speed. Local: 0 retries so flake is loud.
- A retried-pass is a flake report, not a success — fix the cause (usually a missing web-first assertion before an action).
- `toHaveScreenshot` assertions follow the `visual-regression` skill (own project, fixture data, determinism rules) — they don't belong in functional E2E specs.
- Cover the browsers users use (chromium minimum; add webkit/firefox per project requirements) — but don't 3x the matrix for stubbed-network tests.

## A11y gate

- `@axe-core/playwright` scan on each key page/state in a dedicated spec; fail on serious/critical violations.
