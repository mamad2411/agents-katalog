---
name: playwright-e2e-spa-auth-navigation
description: Generic Playwright E2E patterns for React SPAs with authentication — fixture setup, login, navigation strategy, afterEach isolation, headless mode, and SPA reload timing.
category: Testing & Debugging
---

# Playwright E2E SPA Authentication & Navigation

Generic Playwright E2E testing patterns for React single-page applications
that require authentication before accessing protected routes.

## When to use

Use this skill when writing or debugging Playwright E2E tests for a React SPA
that:

- Has a login form (email/password) that stores an authentication token in
  `localStorage`.
- Uses protected routes (e.g., React Router `<PrivateRoutes>`) that check for
  the token before rendering.
- Has a post-login workflow that initializes application state (encrypted
  resources, sidebar menu filtering) before navigation is safe.
- Needs to navigate between pages in E2E tests — either via UI clicks or
  direct `page.goto()`.
- Runs tests in headless mode and encounters rendering differences
  (sidebar submenus, auth-visibility gating).

## Composition by Higher-Level Skills

Distribution-unit-specific composer skills (e.g., in an org-private repo) can
selectively compose sections from this base skill, adding repo-specific auth
credentials, card-click flows, `<VerifyComponent>` reload logic, and test-case
patterns.

## Environment & Dependencies

- **Node.js 18+**: Required for Playwright. Verify with `node --version`.
- **@playwright/test ^1.60.0**: Test runner. Verify with `npx playwright --version`.
- **Playwright browser binary**: Chromium (bundled) for headless runs.
  Install with `npx playwright install chromium`.
- **Running dev server**: Playwright `webServer` config in `playwright.config.ts`
  starts the app before tests; alternatively start manually with `npm start`.

***

## 1. Auth Fixture Pattern

Create a custom fixture that provides a clean authenticated page to every
test. The fixture MUST create a fresh browser context per test to guarantee
isolation — no shared cookies, localStorage, or service workers.

### 1.1 Fixture template

```typescript
import { test as base, type Page } from '@playwright/test';

export const test = base.extend<{ authPage: Page }>({
  authPage: async ({ browser, baseURL }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    // Navigate to base URL before clearing storage (avoids SecurityError
    // from about:blank origin)
    if (baseURL) {
      await page.goto(baseURL);
    }
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    await use(page);
    await context.close();
  },
});
```

### 1.2 Fixture guarantees

- A brand-new `Page` in a brand-new `BrowserContext` for every test.
- `localStorage` and `sessionStorage` are empty; cookies are cleared.
- The page starts at the app's `baseURL` (usually `http://localhost:3000`),
  which the SPA redirects to the login page.

**Why not use `storageState`?** If the app stores encrypted per-session
resources (e.g., a `<resource-list>` encrypted with server-side keys) that
expire, pre-seeding `storageState` leads to stale tokens and silent failures.
Always re-authenticate per test.

***

## 2. Login Flow

### 2.1 Login function template

```typescript
async function doLogin(page: Page) {
  await page.getByPlaceholder('Enter your email address').fill('user@example.com');
  await page.getByPlaceholder('Enter your password').fill('correct-password');
  await page.getByRole('button', { name: /Sign In/i }).click();
  await page.waitForURL('**/<post-login-route>**', { timeout: 30_000 });
}
```

**Customise for your app:**

- Replace placeholder text, role matchers, and expected redirect URL.
- If login uses OAuth / SSO, adapt the flow (wait for redirect, handle
  popup, read tokens from URL params).

### 2.2 What the login sets up

After successful login, the app typically writes to `localStorage`:

| Key | Value | Source |
| :--- | :--- | :--- |
| `accessToken` | JWT or opaque token | Login API response |
| `refreshToken` | Long-lived refresh token | Login API response |
| (optional) `<resource-list>` | Encrypted list of accessible resources | Post-login discovery (e.g., card click trigger) |

The `accessToken` alone is usually sufficient for `PrivateRoutes` to allow
navigation. Some routes also require `<resource-list>` (encrypted permissions)
which may be set by a secondary action after login.

### 2.3 Verifying login success

After `click()`, wait for the URL to settle on an authenticated route:

```typescript
await page.waitForURL('**/<post-login-route>**', { timeout: 30_000 });
```

Confirm the token exists:

```typescript
const token = await page.evaluate(() => localStorage.getItem('accessToken'));
expect(token).toBeTruthy();
```

***

## 3. Navigation Strategies

Two approaches exist for navigating within the SPA during E2E tests:

| Strategy | When to use | Risks |
| :--- | :--- | :--- |
| **UI click-through** | When the app must initialize React state (sidebar menus, context providers) before the route renders safely | Slower; sub-menus may not expand in headless mode |
| **Direct `page.goto(url)`** | When auth tokens + resource list are already in `localStorage` and the route is not state-dependent | Navigation can be interrupted by SPA redirects if required state is missing |

### 3.1 Decision rule

Use `page.goto()` ONLY after the full auth state (`accessToken` +
`<resource-list>` + any encrypted permission blobs) is confirmed present in
`localStorage`. If the route guards depend on React state (selected menu
item, expanded folder), use UI click-through.

### 3.2 UI click-through pattern

```typescript
// Traverse sidebar hierarchy
await page.getByText('<Section>').click();
await page.getByText('<SubSection>').click();
await page.getByText('<SubPage>', { exact: true }).click();
await page.getByText('<TargetPage>', { exact: true }).click();
await page.waitForURL('**/<page-route>', { timeout: 15_000 });
```

**Headless consideration:** Sidebar sub-menus are often hidden via CSS
(`display: none`) until their parent is clicked. In headless mode the CSS
transition may not fire identically — add `waitForTimeout(500)` between
nested clicks or prefer direct `page.goto()` when the auth state is stable.

### 3.3 Direct page.goto pattern

```typescript
await page.goto('/<section>/<sub-section>/<page-route>', { timeout: 30_000 });
await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
```

**Prerequisites:**

1. `accessToken` is set in `localStorage` (login completed).
2. `<resource-list>` (or equivalent permission blob) is set in `localStorage`
   (post-login resource discovery completed).
3. The SPA has fully initialized at least once (React components mounted,
   `PrivateRoutes` rendered) — typically after a page load or reload.

If `page.goto()` triggers a redirect to the dashboard, it means one of the
prerequisites is missing or expired. Debug by checking `localStorage`
contents before the goto:

```typescript
const ls = await page.evaluate(() => ({ ...localStorage }));
console.log('localStorage before goto:', JSON.stringify(ls));
```

***

## 4. AfterEach Isolation

### 4.1 Problem

The `test.afterEach` hook runs after every test. If it navigates to the
app's base URL (to access localStorage for clearing), it can trigger
client-side redirects that interfere with the next test's navigation.
The next test's `page.goto()` may be interrupted by a redirect generated
by the clean-up navigation.

### 4.2 Clean pattern

```typescript
test.afterEach(async ({ authPage }) => {
  // The authPage fixture already creates a fresh context for each test.
  // Do NOT navigate to baseURL here — it may trigger SPA redirects.
  // Just clear cookies and storage on the existing page.
  await authPage.context().clearCookies();
  await authPage.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });
});
```

**Key rule:** Never `page.goto(baseURL)` inside `afterEach` for an SPA.
The fixture already creates a fresh context with clean storage. The only
purpose of the afterEach is to clear cross-context persistent state
(cookies) as a safety net — not to re-initialize the SPA.

### 4.3 Why this matters for sequential tests

Without this fix, the first test passes but subsequent tests fail with:

```text
page.goto: Navigation to "http://localhost:3000/private/route"
  is interrupted by another navigation to "http://localhost:3000/<dashboard-route>/default"
```

The interruption is the SPA's `PrivateRoutes` redirect caused by the
afterEach navigation loading the app and React clearing the token.

***

## 5. Headless Mode Considerations

Playwright's headless (bundled Chromium) differs from headed (system Chrome)
in several ways that affect E2E tests:

### 5.1 Sidebar / sub-menu rendering

In headed mode, CSS transitions and hover states may make sub-menus visible
even without explicit `click()`. In headless mode, use `display: block/none`
strictly as governed by React state — there is no "ambient" rendering.

**Fix:** Always click the parent menu item to expand sub-menus before
clicking children:

```typescript
await page.getByText('<Section>').click();
await page.waitForTimeout(300); // allow React state update
await page.getByText('<SubSection>').click();
```

### 5.2 window.location.reload() timing

After a client-side navigation (React Router), the URL may match
`waitForURL` BEFORE the promised `window.location.reload()` fires.
This creates a race condition where `page.goto()` is interrupted by the
pending reload.

**Fix:** After `waitForURL`, wait for the reload to complete by checking
`document.readyState`:

```typescript
await page.waitForURL('**/<dashboard-route>/**', { timeout: 30_000 });
// <VerifyComponent>-like: client nav + window.location.reload()
await page.waitForFunction(
  () => document.readyState === 'complete',
  { timeout: 30_000 }
);
```

### 5.3 Viewport / font rendering

Headless mode uses a default viewport of 1280×720. Text and CSS media
queries behave identically to headed mode when `headless: true` is set
on Chromium. Mobile viewport testing uses `page.setViewportSize()`:

```typescript
await page.setViewportSize({ width: 375, height: 812 });
```

### 5.4 Debugging headless failures

Capture screenshots at each phase to compare against headed runs:

```typescript
const SS = (name: string) => `scratch/screenshots/${name}.png`;
await page.screenshot({ path: SS('after-login'), fullPage: true });
await page.screenshot({ path: SS('after-nav'), fullPage: true });
```

Also dump the visible text to understand what rendered:

```typescript
const text = await page.evaluate(() => document.body.innerText.substring(0, 500));
console.log('Page text:', JSON.stringify(text));
```

***

## 6. SPA Reload Pattern (`<VerifyComponent>`-like)

Some SPA flows involve a sequence of:

1. A UI action (e.g., card click) that fetches encrypted permissions and
   navigates to a "verify" route.
2. A process on the verify route that reads the permissions, filters menus,
   and calls `window.location.reload()` to restart the app with full auth
   state.

This pattern is common in "application chooser" / "workspace selector"
workflows.

### 6.1 Waiting for the reload to complete

The reload happens as TWO navigation events:

| Step | Navigation type | URL |
| :--- | :--- | :--- |
| 1 | Client-side (React Router `navigate()`) | `/<dashboard-route>/default` |
| 2 | Full page reload (`window.location.reload()`) | `/<dashboard-route>/default` (same URL) |

`waitForURL('**/<dashboard-route>/**')` resolves on Step 1. The reload in Step 2
happens in the next event-loop tick. To wait for the reload to finish, use
`waitForFunction` checking `document.readyState` — it will cycle through
`'loading'` → `'interactive'` → `'complete'` again after the reload.

```typescript
async function navigateThroughCardToDashboard(page: Page) {
  await page.getByText('Card Title').click();
  // Step 1: client-side nav
  await page.waitForURL('**/<dashboard-route>/**', { timeout: 30_000 });
  // Step 2: wait for the reload
  await page.waitForFunction(
    () => document.readyState === 'complete',
    { timeout: 30_000 }
  );
}
```

### 6.2 State after reload

After the reload, `localStorage` contains:

- `accessToken` (persisted from login)
- `<resource-list>` (encrypted permissions, set during the card-click flow)

The application restarts fresh with all auth state, making `page.goto()`
safe for subsequent navigation.

***

## 7. Related Skills

- [`mrt-configuration-debug`](../mrt-configuration-debug/SKILL.md) — Verify MRT features
  in E2E tests (adds MRT-specific selectors, filter/sort/pagination patterns)
- [`mrt-component-test-strategy`](../mrt-component-test-strategy/SKILL.md) — Unit-test MRT
  components with Jest+RTL (complementary: E2E vs unit coverage)
- [`table-persistence-implementation`](../table-persistence-implementation/SKILL.md) —
  `useTablePersistence` hook and localStorage persistence patterns
- [`project-structure`](../project-structure/SKILL.md) — Project scaffolding
  for the repo under test
