---
name: appium-mobile-bank
description: >-
  Create or update the Appium/WebdriverIO mobile-web automation suite for the
  Vulnerable Bank application — real Chrome on Android and Safari on iOS, not
  Playwright emulation. Use when editing files under mobile/, running
  test:mobile:android/ios, or porting Playwright page objects to WebdriverIO.
---

# Appium Mobile-Web Automation — Vulnerable Bank

Drives real mobile browser engines (Chrome/Android via UiAutomator2, Safari/iOS via XCUITest) against the same Flask app the Playwright suite tests. No native app — mobile web only.

Separate framework from Playwright (WebdriverIO/Mocha). Mirrors Playwright conventions where the protocol allows. Playwright detail: `.cursor/skills/playwright-vulnerable-bank/SKILL.md`.

## Project Layout

```
mobile/
  wdio.conf.ts            Base config — not run directly
  wdio.android.conf.ts    Android/Chrome + Appium service
  wdio.ios.conf.ts        iOS/Safari + Appium service
  tsconfig.json           Separate from repo root (WDIO types must not leak into Playwright)
  pages/
    mobile-helper-base.ts
    mobile-page-manager.ts
    login.page.ts, dashboard.page.ts, money-transfer.page.ts
  fixtures/
    mobile-auth.ts        Port of helpers/auth-bootstrap.ts + credentials.ts
  specs/
    *.mobile.spec.ts
```

Conventions from Playwright suite:
- No barrel/`index.ts` files.
- Locators inside page-object methods, not constructor fields.
- One `MobilePageManager` owns all page objects.
- Reuse `test-data/users.json` via `helpers/credentials.ts`.

## Locator Priority (WebdriverIO)

Mirror Playwright's selector philosophy — semantic/accessible first, same DOM so selectors should match 1:1. Check `pages/<feature>.page.ts` first.

| Priority | Strategy | Playwright equivalent |
|----------|----------|----------------------|
| P1 | ARIA / role | `getByRole()`, `getByLabel()` |
| P2 | `data-testid` | `getByTestId()` — dev-set, stable |
| P2 | Text match | `getByText()`, `getByPlaceholder()` |
| P3 | ID / name attr | shallow attribute selectors |
| P4 | CSS class | avoid — changes across releases |
| P5 | XPath | avoid — especially deeply nested |

Use chaining/filtering for context instead of long compound selectors. Keep selectors descriptive and stable across releases.

```ts
const input = $('input[name="username"]');
await input.waitForDisplayed({ timeout: 5000 });
await input.setValue('testuser');
```

Mirror Playwright locators 1:1 — check `pages/<feature>.page.ts` before writing mobile selectors.

**Mobile-specific:** viewport may hide elements (off-canvas menu) — use `isDisplayed()` and `openMenu()`-style methods (`mobile/pages/dashboard.page.ts`) before interacting.

## Assertions (expect-webdriverio)

Use `expect-webdriverio` matchers — they retry until timeout, mirroring Playwright auto-wait:

```ts
await expect($('h1')).toBeDisplayed();
await expect(browser).toHaveUrl(/\/dashboard/);
await expect($('#balance')).toHaveText(expect.stringMatching(/\d+/));
```

Avoid one-shot checks (`const visible = await el.isDisplayed(); expect(visible).toBe(true)`) when a matcher exists.

## Test Isolation

**Per-test** (`mobile/wdio.conf.ts` hooks):
- `beforeEach`/`afterEach`: clear localStorage, sessionStorage, cookies.

**Global** (`mobile/global-teardown.ts` via `onComplete`):
- Admin auth, delete test users by prefix; preserve admin account.

## What Differs from Playwright

| Playwright | WebdriverIO |
|------------|-------------|
| `Page` constructor arg | `browser`/`$`/`$$` globals |
| `request.newContext()` + cookies | `fetch` + `browser.setCookies`/`browser.execute` |
| `@playwright/test` expect | `expect-webdriverio` matchers |
| Schema + SecurityReporter | Out of scope — add API/OWASP coverage in Playwright suite |

No `networkidle` equivalent — `waitForLoad()` polls URL + heading + `#balance` with `waitForDisplayed`/`waitUntil`.

## Adding a New Spec

1. Check/create page object in `mobile/pages/` extending `MobileHelperBase` — same locators as Playwright sibling.
2. Register in `mobile/pages/mobile-page-manager.ts`.
3. Add `mobile/specs/<feature>.mobile.spec.ts`; use `ensureDashboardAuthenticated` in `beforeEach` for post-login flows.
4. Run locally on booted emulator/simulator before assuming CI parity.

## Running

```bash
npm run test:mobile:android   # ANDROID_HOME + booted AVD with Chrome
npm run test:mobile:ios       # macOS, Xcode, booted iOS Simulator
```

Both write to shared `allure-results/` — `npm run allure:report` shows Playwright + mobile together.
