---
name: test-ui-qsf
description: QSF project conventions for the Playwright E2E suite. Use when working in the QSF playwright-tests directory (authFixtures, ___ping-* handles, data-test-label test IDs, .auth storage states) — not for generic Playwright advice.
---

# QSF Playwright E2E Conventions

Project-specific conventions for the QSF Playwright suite. For generic Playwright
best practices (locators, auto-waiting, POM, anti-patterns), follow the `test-ui`
skill — this skill only adds what is QSF-specific.

## Commands

- `source ./bin/load_env.sh && bunx playwright test` — run all tests headless
- `source ./bin/load_env.sh && bunx playwright test --project=regression-tests` —
  skip auth-setup
- `bun run test` / `bunx playwright test --ui` — interactive UI mode
- `bunx playwright test --reporter=list` — verbose terminal output
- `bunx playwright test --grep '@smoke'` — run tagged tests
- `bunx playwright show-trace <trace.zip>` — inspect failure traces

## Test IDs

`getByTestId` resolves to the **`data-test-label`** attribute (set via
`testIdAttribute` in `playwright.config.ts`):

```typescript
page.getByTestId("no-handles-available-indicator");
page.getByTestId("open-filter-section-button");
```

## Fixtures (Auth Pattern)

The project extends Playwright's `test` with pre-authenticated user fixtures via
storage state files in `playwright-tests/.auth/`.

```typescript
// fixtures/authFixtures.ts
const authFiles = {
  guest: "guest_storage_state.json",
  testView: "test_view_storage_state.json",
  testNoRights: "test_no_rights_storage_state.json",
  // ... more users
};

const baseFixtures = Object.fromEntries(
  Object.entries(authFiles).map(([key, fileName]) => [
    key,
    async ({ browser }: { browser: Browser }, use: (page: Page) => Promise<void>) => {
      const storageState = path.join(__dirname, "../.auth", fileName);
      const context = await browser.newContext({ storageState });
      const page = await context.newPage();
      try {
        await use(page);
      } finally {
        await context.close();
      }
    },
  ]),
);

export const test = baseTest.extend(baseFixtures);
export const expect = test.expect;
```

### Fixture Usage

```typescript
// Tests import from authFixtures, NOT from @playwright/test
import { test, expect } from "../../fixtures/authFixtures";

test("user sees their handles", async ({ guest }) => {
  await guest.goto("/"); // `guest` is a pre-authenticated Page — no login needed
});

test("restricted user cannot access admin", async ({ testNoRights }) => {
  await testNoRights.goto("/admin");
});
```

## File Organization

```text
playwright-tests/
├── .auth/              # Storage state JSON files (gitignored in CI)
├── enums/              # Constants: handle names, error messages, labels
├── fixtures/           # authFixtures.ts — extended test/expect
├── pageObjects/        # POM classes (BasePage, LoginPage, ...)
│   └── components/     # Reusable: Navigation, FileUpload, FormElements
├── setup/              # auth.setup.ts, cleanup.ts
└── tests/              # Spec files grouped by feature (handle/, ping-files/, ...)
```

## Page Objects

Pages extend `BasePage` (`pageObjects/BasePage.ts`), which composes
`Navigation`, `FilterSection`, and `IdleModal`. Specialized pages (e.g.
`AppsDetailPage`) add components like `FileUpload` and `Iwa`. Keep
`FormElements.ts` under 300 lines — split by element type when it grows.

## Enums & Constants

Store UI labels, error messages, and handle identifiers in
`playwright-tests/enums/`. **Never hard-code** them in tests.

```typescript
// enums/handles.ts
export const HandleNames = { PING_FILES: '___ping-files-en', ... };
export const HandleIds = { PING_FILES: 'qsf-handle-ping-files', ... };

// enums/errors.ts
export const Errors = { FILE_TOO_LARGE: 'produced an error while processing', ... };

// enums/elementLabels.ts
export const Buttons = { SUBMIT: 'Submit', UPLOAD: 'Upload files', ... };
```

## Typical Test Pattern

```typescript
import { test, expect } from "../../fixtures/authFixtures";
import { AppsDetailPage } from "../../pageObjects/AppsDetailPage";
import { MyAppsPage } from "../../pageObjects/MyAppsPage";
import { HandleNames } from "../../enums/handles";

test.describe("Feature Area", () => {
  test.beforeEach(async ({ guest }) => {
    const myAppsPage = new MyAppsPage(guest);
    await guest.goto("/");
    await myAppsPage.navigation.openHandle(HandleNames.PING_FILES);
  });

  test("describes expected behavior", async ({ guest }) => {
    const appsDetailPage = new AppsDetailPage(guest);
    await appsDetailPage.doSomething();
    await appsDetailPage.assertSomething(expected);
  });
});
```

When `beforeEach` navigation + upload + dashboard assertion is duplicated across
describe blocks, extract a shared helper (e.g.
`setupDashboardForTestcase(guest, handleName, testcase)`).

## Environment-Aware Tests

```typescript
import { isOpenAmEnv } from "../../src/utils/environment";

test.skip(isOpenAmEnv, "This test is only for Keycloak environments");
```

Env is loaded via `source ./bin/load_env.sh`; the `ENVIRONMENT` variable controls
the target URL (default: `test`).

## Configuration Highlights (`playwright.config.ts`)

```typescript
export default defineConfig({
  testDir: "./playwright-tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.TEST_HANDLE ? 0 : 1,
  workers: process.env.CI ? 1 : 5,
  globalTimeout: 30 * 60 * 1000,
  timeout: 60000,
  expect: { timeout: 10000 },
  use: {
    ignoreHTTPSErrors: true,
    testIdAttribute: "data-test-label",
    baseURL: envUrl,
    trace: "on-first-retry",
  },
  projects: [
    { name: "auth-setup", testMatch: "**/setup/auth.setup.ts" },
    {
      name: "regression-tests",
      testMatch: ["**/tests/*.spec.ts", "**/tests/**/*.spec.ts"],
      dependencies: process.env.CI ? ["auth-setup"] : [],
      use: { trace: "retain-on-failure", headless: true },
    },
  ],
});
```

## QSF Checklist

- [ ] `test`/`expect` imported from `authFixtures`, not `@playwright/test`
- [ ] Named user fixtures (`guest`, `testView`, `testNoRights`) used for auth
- [ ] Browser context closed after each fixture via `context.close()`
- [ ] Handle names, errors, and labels imported from `enums/`
- [ ] `getByTestId` values match `data-test-label` attributes
- [ ] `test.skip(isOpenAmEnv, ...)` used for environment-specific tests
- [ ] Env loaded via `source ./bin/load_env.sh` before running
- [ ] Generic rules from the `test-ui` skill also satisfied
