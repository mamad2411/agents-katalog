---
name: qa-e2e
description: >
  A skill that writes and **always executes** Playwright E2E tests based on test cases and the implemented application.
  It writes E2E test code based on user scenarios, executes the tests, verifies results, and generates bug reports.
  Use this skill when E2E testing, Playwright testing, or integration testing is requested.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## ⛔⛔⛔ Top Priority Principle: Tests Must Be Executed After Writing ⛔⛔⛔

> **⚠️ Warning**: Writing test code without executing it and then terminating is **strictly prohibited**.

### Mandatory Execution Order (Never Skip Any Step)

```
1. Verify/configure test environment ────────────── ✅ Required
           │
           ▼
2. Write test code (GWT format) ─────────────────── ✅ Required
           │
           ▼
3. ⛔ Execute tests (npx playwright test) ────────── ✅ Required (Do not skip!)
           │
           ▼
4. Analyze test results ─────────────────────────── ✅ Required
           │
           ├── All passed ──▶ Report success and finish
           │
           └── Failures ──▶ Proceed to step 5
           │
           ▼
5. Generate bug report ─────────────────────────── ✅ Required on failure
           │
           ▼
6. Request bug fix (call be-main/fe-main) ──────── ✅ Required on failure
```

### ⛔ Strictly Prohibited Actions

1. **Writing test code only and reporting "Done"**
2. **Skipping test execution**
3. **Ignoring test failures and moving on**
4. **Telling the user to "run it later"**

### Workflow Termination Conditions

| Situation | Can Terminate? |
|-----------|---------------|
| Test code only written | ⛔ **Prohibited** - Must be executed |
| All tests pass after execution | ✅ Can terminate |
| Test failures after execution | ⛔ **Prohibited** - Bug report must be generated |
| Bug report generation complete | ✅ Can terminate (fixes are handled by other skills) |

---

## ⚠️ Core Principle: Test Against Real Servers

> **No mocking**: E2E tests must use real servers and databases.
> - No API mocking, MSW, or fake responses
> - Real backend server must be running
> - Use a test-dedicated database
> - Ensure consistent test environment through test data seeding

# QA E2E Test Developer

Write Playwright E2E tests based on test cases and report bugs.
Test the full stack in a **real server environment**.

## Workflow

### 1. Verify Input Documents

Receive the following documents as input:
- Test case document
- Executable application URL
- (Optional) Wireframe/design spec

```
Example input:
- "Write E2E tests based on docs/test-cases/account-test-cases.md"
- "Write E2E tests for the login flow"
```

### 2. Project Analysis

1. Understand existing E2E test structure
2. Check Playwright configuration
3. Review test utilities/helpers
4. Check environment variables/test data

### 3. Configure Test Environment (Real Server)

#### ⛔ Server Startup Method: Always Use Background Servers

> **⚠️ Mandatory Principle**: Do not start servers using Playwright's `webServer` option or Docker Compose.
> Due to memory issues, servers must **always be started in the background beforehand**, then only tests are executed.

```
⛔ Prohibited: Starting server via Playwright webServer option
⛔ Prohibited: Starting server via Docker Compose
⛔ Prohibited: Spawning server processes in globalSetup

✅ Required: Start servers in the background beforehand
✅ Required: Verify server is running via health check
✅ Required: No webServer config in playwright.config.ts
```

#### 3.1 Pre-start Servers (Required Before Testing)

```bash
# 1. Start backend server (separate terminal or background)
cd backend && npm run start:dev &
# → Listening at http://localhost:4000

# 2. Start frontend server (separate terminal or background)
cd frontend && npm run dev &
# → Listening at http://localhost:3000

# 3. Verify server status
curl -s http://localhost:4000/api/health  # Backend health check
curl -s http://localhost:3000             # Frontend check
```

> **When running as agent**: Use the Bash tool to check if server processes are running.
> If not running, start the servers first with `run_in_background: true`.

#### 3.2 Project Structure

```
e2e/
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   └── users/
│       └── profile.spec.ts
├── fixtures/
│   ├── auth.fixture.ts
│   └── test-data.ts
├── pages/
│   ├── login.page.ts
│   └── signup.page.ts
├── utils/
│   ├── helpers.ts
│   └── api-client.ts         # API client for testing
└── playwright.config.ts
```

### 4. Playwright Configuration (Assumes Background Server)

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  // Timeout settings for real server usage
  timeout: 60000,
  expect: {
    timeout: 10000,
  },

  use: {
    // ⚠️ Use URL of already-running server
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 15000,
    navigationTimeout: 30000,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // ⛔ Do not use webServer - prevents memory issues
  // Servers must always be started in the background before running tests
  // Backend: cd backend && npm run start:dev (localhost:4000)
  // Frontend: cd frontend && npm run dev (localhost:3000)
});
```

> **⛔ Important**: Do not use the `webServer` option. Due to memory issues, servers must always be started in the background beforehand.

### 5. Test Data (Seeded Real Data)

```typescript
// e2e/fixtures/test-data.ts
// ⚠️ This data is created in the real DB by seed-database.ts

export const testUsers = {
  // Seeded standard user
  standard: {
    email: 'test@example.com',
    password: 'Test1234!',
    name: 'Test User',
  },
  // Seeded admin
  admin: {
    email: 'admin@example.com',
    password: 'Test1234!',
    name: 'Admin',
  },
  // Non-existent user (for failure tests)
  nonExistent: {
    email: 'nonexistent@example.com',
    password: 'password123',
  },
  // For new user creation tests
  newUser: {
    email: `new-${Date.now()}@example.com`,
    password: 'NewUser1234!',
    name: 'New User',
  },
};
```

### 6. Page Object Model

```typescript
// e2e/pages/login.page.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly signupLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Log In' });
    this.errorMessage = page.getByRole('alert');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot Password' });
    this.signupLink = page.getByRole('link', { name: 'Sign Up' });
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectErrorMessage(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }

  async expectRedirectToDashboard() {
    await expect(this.page).toHaveURL('/dashboard');
  }
}
```

### 7. Test Code (Given-When-Then Format)

E2E test code is written in **Given-When-Then** format to ensure readability and clarity of intent.
Tests use **real seeded data**.

```typescript
// e2e/tests/auth/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/login.page';
import { testUsers } from '../../fixtures/test-data';

test.describe('Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  // TC-AUTH-P-001: Normal login (seeded user from real DB)
  test('Login succeeds with valid credentials', async () => {
    // Given: The user is on the login page
    // Given: A test user has been seeded in the DB (handled in global-setup)

    // When: The user logs in with seeded user credentials
    await loginPage.login(testUsers.standard.email, testUsers.standard.password);

    // Then: The user is redirected to the dashboard page
    await loginPage.expectRedirectToDashboard();
  });

  // TC-AUTH-N-001: Wrong password
  test('Login fails with wrong password', async () => {
    // Given: The user is on the login page

    // When: The user attempts to log in with a seeded email and wrong password
    await loginPage.login(testUsers.standard.email, 'wrongpassword');

    // Then: An error message is displayed
    await loginPage.expectErrorMessage('Email or password does not match');
  });

  // TC-AUTH-N-002: Non-existent email
  test('Login fails with non-existent email', async () => {
    // Given: The user is on the login page

    // When: The user attempts to log in with an email that does not exist in the DB
    await loginPage.login(testUsers.nonExistent.email, testUsers.nonExistent.password);

    // Then: An error message is displayed
    await loginPage.expectErrorMessage('Email or password does not match');
  });

  // TC-AUTH-B-001: Email format validation
  test('Error is displayed when invalid email format is entered', async ({ page }) => {
    // Given: The user is on the login page

    // When: The user enters an invalid email format and submits
    await loginPage.emailInput.fill('invalid-email');
    await loginPage.passwordInput.fill('password123');
    await loginPage.submitButton.click();

    // Then: An email format error message is displayed
    await expect(page.getByText('Please enter a valid email')).toBeVisible();
  });
});
```

### 8. Sign-up Test (Real DB Record)

```typescript
// e2e/tests/auth/signup.spec.ts
import { test, expect } from '@playwright/test';
import { SignupPage } from '../../pages/signup.page';
import { testUsers } from '../../fixtures/test-data';

test.describe('Sign Up', () => {
  let signupPage: SignupPage;

  test.beforeEach(async ({ page }) => {
    signupPage = new SignupPage(page);
    await signupPage.goto();
  });

  // TC-SIGNUP-P-001: Normal sign-up (creates user in real DB)
  test('Sign-up succeeds with valid information', async () => {
    // Given: The user is on the sign-up page
    const newUser = {
      email: `e2e-test-${Date.now()}@example.com`,
      password: 'NewUser1234!',
      name: 'New User',
    };

    // When: The user enters valid information and attempts to sign up
    await signupPage.signup(newUser.email, newUser.password, newUser.name);

    // Then: Sign-up succeeds and the user is redirected to the login page
    await expect(signupPage.page).toHaveURL('/login');
    await expect(signupPage.page.getByText('Sign-up is complete')).toBeVisible();
  });

  // TC-SIGNUP-N-001: Already existing email (conflicts with seeded user)
  test('Sign-up fails with already existing email', async () => {
    // Given: The user is on the sign-up page
    // Given: A user with this email already exists in the DB (seeded)

    // When: The user attempts to sign up with an already existing email
    await signupPage.signup(
      testUsers.standard.email,  // Already seeded email
      'NewPassword1234!',
      'Duplicate User'
    );

    // Then: An error message is displayed
    await expect(signupPage.errorMessage).toContainText('This email is already registered');
  });
});
```

### 9. Fixture Usage (Real Authentication)

```typescript
// e2e/fixtures/auth.fixture.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { testUsers } from './test-data';

type AuthFixtures = {
  loginPage: LoginPage;
  authenticatedPage: LoginPage;
  adminPage: LoginPage;
};

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);
  },

  // Authenticated as standard user (real login)
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    // ⚠️ Sends actual login request to the real server
    await loginPage.login(testUsers.standard.email, testUsers.standard.password);
    await expect(page).toHaveURL('/dashboard');
    await use(loginPage);
  },

  // Authenticated as admin (real login)
  adminPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    // ⚠️ Sends actual admin login request to the real server
    await loginPage.login(testUsers.admin.email, testUsers.admin.password);
    await expect(page).toHaveURL('/dashboard');
    await use(loginPage);
  },
});

// Usage example
test('Authenticated user can view profile', async ({ authenticatedPage, page }) => {
  // Given: The user is logged in (real login completed in fixture)
  await page.goto('/profile');

  // Then: The profile page is displayed
  await expect(page.getByText(testUsers.standard.name)).toBeVisible();
});

test('Admin can view user list', async ({ adminPage, page }) => {
  // Given: The admin is logged in
  await page.goto('/admin/users');

  // Then: The user list is displayed
  await expect(page.getByRole('table')).toBeVisible();
});
```

### 10. ⛔ Test Execution (Required - Do Not Skip!)

> **⛔ Warning**: Skipping this step means the skill execution is considered **failed**.
> After writing test code, you must execute the tests and verify the results.

#### 10.1 Test Execution (Background Server Environment)

```bash
# 1. ⛔ Verify servers are already running (required!)
curl -s http://localhost:4000/api/health  # Backend
curl -s http://localhost:3000             # Frontend

# If servers are not running, start them in the background
# cd backend && npm run start:dev &
# cd frontend && npm run dev &

# 2. Run migrations (if needed)
cd backend && npx typeorm migration:run -d src/data-source.ts

# ⛔ 3. Execute tests! (Do not skip!)
cd frontend && npx playwright test

# ⚠️ Runs without webServer option - uses already-running servers
```

#### 10.2 ⛔ Analyze Test Results (Required)

After test execution, you **must** analyze the results:

```bash
# Execute tests and check results
npx playwright test 2>&1 | tee test-results.log

# Or generate JSON report
npx playwright test --reporter=json > test-results.json
```

**Result Analysis Checklist:**

| Check Item | Action |
|-----------|--------|
| All tests pass | ✅ Write success report and finish |
| Some tests fail | ⛔ Bug report generation required (proceed to step 11) |
| Test environment error | Resolve environment issue and re-run |
| Timeout occurred | Adjust timeout settings or check server status |

#### 10.3 Report on Success

If all tests pass, output the following:

```markdown
## ✅ E2E Test Results: Success

**Execution Time**: 2024-01-15 14:30:00
**Total Tests**: 15
**Passed**: 15
**Failed**: 0
**Skipped**: 0

### Test Summary
- auth/login.spec.ts: 5/5 passed ✅
- auth/signup.spec.ts: 4/4 passed ✅
- users/profile.spec.ts: 6/6 passed ✅

> All E2E tests passed. You may proceed to the next step.
```

#### NPM Scripts

```json
// package.json
{
  "scripts": {
    "e2e": "playwright test",
    "e2e:ui": "playwright test --ui",
    "e2e:debug": "playwright test --debug",
    "e2e:headed": "playwright test --headed",

    "e2e:setup": "docker-compose -f e2e/docker-compose.e2e.yml up -d --wait",
    "e2e:teardown": "docker-compose -f e2e/docker-compose.e2e.yml down -v",
    "e2e:seed": "ts-node e2e/setup/seed-database.ts",
    "e2e:reset": "ts-node e2e/setup/reset-database.ts",

    "e2e:ci": "playwright test --reporter=github"
  }
}
```

#### CI/CD Pipeline Example

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests
        run: npm run e2e:ci
        env:
          CI: true
          BASE_URL: http://localhost:3000

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### 11. ⛔ Bug Report Generation (Required on Test Failure!)

> **⛔ Warning**: Terminating without generating a bug report when tests have failed is **prohibited**.

When tests fail, you **must** generate a bug report document:

```markdown
# Bug Report

## BUG-001: Login Error Message Not Displayed

**Severity**: High
**Date Found**: 2024-01-15
**Version Found**: v1.2.0
**Related TC**: TC-AUTH-N-001

### Steps to Reproduce
1. Navigate to the login page (`/login`)
2. Enter a valid email
3. Enter a wrong password
4. Click the login button

### Expected Result
- Error message "Email or password does not match" is displayed

### Actual Result
- No error message is displayed
- Only the login button becomes disabled

### Screenshot
![Error Screenshot](./screenshots/bug-001.png)

### Environment
- Browser: Chrome 120
- OS: macOS 14.0
- Screen Size: 1920x1080

### Attachments
- Trace file: `trace-bug-001.zip`
- Video: `video-bug-001.webm`
```

### 11. File Output

```
e2e/
├── tests/{backlog-keyword}/{feature}.spec.ts
├── pages/{page-name}.page.ts
├── fixtures/{feature-name}.fixture.ts
├── utils/
│   └── api-client.ts         # API client for testing
└── playwright.config.ts

docs/{backlog-keyword}/
└── bug-reports/
    └── {bug-id}-report.md
```

> **Directory Rule**: All artifacts are stored under the backlog-keyword directory.

## Playwright Patterns

### Element Selector Priority

1. `getByRole()` - Accessibility role
2. `getByLabel()` - Label text
3. `getByPlaceholder()` - placeholder
4. `getByText()` - Text content
5. `getByTestId()` - data-testid (last resort)

```typescript
// Good
page.getByRole('button', { name: 'Save' });
page.getByLabel('Email');

// Avoid
page.locator('#submit-btn');
page.locator('.login-form button');
```

### Wait Strategy

```typescript
// Auto-wait (recommended)
await page.getByRole('button').click(); // Automatically waits until clickable

// Explicit wait
await page.waitForURL('/dashboard');
await expect(element).toBeVisible();
await expect(page.getByText('Success')).toBeVisible({ timeout: 10000 });

// Network wait
await page.waitForResponse('/api/users');
await page.waitForLoadState('networkidle');
```

### Screenshots/Videos

```typescript
// Screenshot during test
await page.screenshot({ path: 'screenshot.png' });
await page.screenshot({ path: 'full.png', fullPage: true });

// Element screenshot
await element.screenshot({ path: 'element.png' });

// Auto-capture in config
// playwright.config.ts
use: {
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
  trace: 'on-first-retry',
}
```

## Real Server Testing Principles

### 1. No Mocking
- ❌ Do not use MSW (Mock Service Worker)
- ❌ Do not mock API responses
- ❌ Do not intercept APIs with `page.route()`
- ✅ Use real responses from the real server

### 2. Test Data Management
- Prepare consistent data through seeding before tests
- Reset data after tests if needed
- Isolate data between tests (use unique emails)

### 3. Environment Separation
- Use a test-dedicated database (when possible)
- Never use the production database
- Start local development servers in the background beforehand

### 4. Test Stability
- Set timeouts considering real server response times
- Verify service readiness via health checks
- Handle transient failures with retry logic

### 5. CI/CD Integration
- Start services beforehand in GitHub Actions, then run tests
- Save artifacts on test failure (screenshots, traces)
- Be careful about database isolation during parallel execution

## ⛔ Skill Completion Checklist (Must Verify Before Finishing)

> **⚠️ Warning**: Failing to complete all items below means the skill execution has **failed**.

### Required Checklist

- [ ] 1. Test environment configuration complete (playwright.config.ts, fixtures, etc.)
- [ ] 2. Page Object Model written
- [ ] 3. E2E test code written (GWT format)
- [ ] **4. ⛔ Tests executed** (`npx playwright test` was run)
- [ ] **5. ⛔ Test results verified** (pass/fail status confirmed)
- [ ] 6. (On failure) Bug report generated

### Required Output on Completion

```markdown
## E2E Test Results Report

**Execution Time**: {timestamp}
**Test Environment**: {baseURL}

### Results Summary
- Total Tests: {total}
- Passed: {passed} ✅
- Failed: {failed} ❌
- Skipped: {skipped} ⏭️

### Executed Test List
| File | Test Count | Result |
|------|-----------|--------|
| auth/login.spec.ts | 5 | ✅ Passed |
| auth/signup.spec.ts | 4 | ❌ 1 failed |

### (On Failure) Generated Bug Reports
- docs/{backlog}/bug-reports/BUG-001-report.md
- docs/{backlog}/bug-reports/BUG-002-report.md
```

> **⛔ Prohibited**: Reporting only "Test code has been written" without the above report and terminating

## References

- Playwright Patterns Guide: [references/playwright-patterns.md](references/playwright-patterns.md)
- Bug Report Template: [references/bug-report-template.md](references/bug-report-template.md)
- Docker Compose Test Environment: [references/docker-e2e-setup.md](references/docker-e2e-setup.md)
