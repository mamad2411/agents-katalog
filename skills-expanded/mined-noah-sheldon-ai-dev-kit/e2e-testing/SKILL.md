---
name: e2e-testing
description: Playwright E2E testing patterns including page object model, fixtures, parallel execution, flaky test prevention, visual regression, API mocking, and cross-browser testing.
origin: AI Dev Kit
disable-model-invocation: false
---

# E2E Testing with Playwright

Comprehensive E2E testing patterns using Playwright. Covers page object model, test fixtures, parallel execution, flaky test prevention, visual regression, API mocking, and cross-browser validation. Use this skill when writing or maintaining E2E tests for web applications.

## When to Use

- Writing new E2E tests for critical user flows
- Converting manual QA scenarios to automated tests
- Debugging flaky E2E tests
- Setting up cross-browser test infrastructure
- Implementing visual regression testing
- Mocking external APIs in end-to-end scenarios
- Establishing E2E testing standards for a project

## Core Concepts

### Critical User Flows

Not every path needs an E2E test. Focus on flows that represent real user journeys:

| Priority | Flow | Example |
|---|---|---|
| P0 | Authentication | Sign up → verify email → log in |
| P0 | Core transaction | Add to cart → checkout → payment confirmation |
| P1 | CRUD operations | Create item → edit → delete → verify removal |
| P1 | Search and filter | Search → apply filter → verify results |
| P2 | Settings and profile | Update profile → save → verify persistence |
| P3 | Edge cases | Session timeout → redirect → re-auth |

P0 and P1 flows should be covered by E2E tests. P2 and P3 are optional based on project scope.

### Page Object Model (POM)

Encapsulate page interactions in reusable, maintainable classes:

```typescript
// tests/pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign In' })
    this.errorMessage = page.getByTestId('login-error')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectLoggedInUser(name: string) {
    await expect(this.page.getByText(name)).toBeVisible()
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message)
  }
}
```

```typescript
// tests/pages/DashboardPage.ts
import { Page, Locator, expect } from '@playwright/test'

export class DashboardPage {
  readonly page: Page
  readonly welcomeHeading: Locator
  readonly createItemButton: Locator
  readonly itemList: Locator

  constructor(page: Page) {
    this.page = page
    this.welcomeHeading = page.getByRole('heading', { name: /welcome/i })
    this.createItemButton = page.getByRole('button', { name: 'Create Item' })
    this.itemList = page.getByTestId('item-list')
  }

  async goto() {
    await this.page.goto('/dashboard')
  }

  async createItem(name: string) {
    await this.createItemButton.click()
    await this.page.getByLabel('Item Name').fill(name)
    await this.page.getByRole('button', { name: 'Save' }).click()
  }

  async expectItemExists(name: string) {
    await expect(this.itemList.getByText(name)).toBeVisible()
  }
}
```

```typescript
// tests/e2e/auth-flow.spec.ts
import { test, expect } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'
import { DashboardPage } from '../pages/DashboardPage'

test.describe('Authentication Flow', () => {
  test('user can log in and access dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const dashboardPage = new DashboardPage(page)

    await loginPage.goto()
    await loginPage.login('alice@example.com', 'correct-password')
    await dashboardPage.expectLoggedInUser('Alice')

    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('invalid credentials show error message', async ({ page }) => {
    const loginPage = new LoginPage(page)

    await loginPage.goto()
    await loginPage.login('alice@example.com', 'wrong-password')
    await loginPage.expectError('Invalid email or password')

    await expect(page).toHaveURL(/\/login/)
  })
})
```

### Test Fixtures

Use Playwright fixtures to set up test state and avoid duplication:

```typescript
// tests/fixtures/auth.ts
import { test as base, Page } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'

type AuthFixtures = {
  loginPage: LoginPage
  authenticatedPage: Page
}

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page)
    await use(loginPage)
  },

  authenticatedPage: async ({ page }, use) => {
    // Auto-login before each test
    await page.goto('/login')
    await page.getByLabel('Email').fill('testuser@example.com')
    await page.getByLabel('Password').fill('testpass123')
    await page.getByRole('button', { name: 'Sign In' }).click()
    await page.waitForURL(/\/dashboard/)
    await use(page)
  },
})

export { expect } from '@playwright/test'
```

```typescript
// tests/e2e/item-management.spec.ts
import { test, expect } from '../fixtures/auth'

test.describe('Item Management', () => {
  test('create and verify item', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/dashboard')
    await authenticatedPage.getByRole('button', { name: 'Create Item' }).click()
    await authenticatedPage.getByLabel('Item Name').fill('Test Widget')
    await authenticatedPage.getByRole('button', { name: 'Save' }).click()

    await expect(authenticatedPage.getByTestId('item-list').getByText('Test Widget')).toBeVisible()
  })
})
```

## Flaky Test Prevention

### Root Causes and Solutions

| Cause | Symptom | Fix |
|---|---|---|
| Timing issues | Element not found intermittently | Use `waitFor` assertions, not `sleep()` |
| Shared state | Tests pass/fail depending on order | Isolate data per test, clean up after |
| Network variability | API timeouts, slow responses | Mock external APIs, set generous timeouts |
| Animation/transitions | Element visible but not clickable | Wait for animation to complete or disable in test mode |
| Dynamic content | IDs/text change between runs | Use stable selectors (`data-testid`, roles) |

### Anti-Pattern vs. Correct Pattern

```typescript
// BAD: Fixed sleep — timing dependent
await page.click('button')
await page.waitForTimeout(2000) // Flaky on slow CI
await expect(page.getByText('Success')).toBeVisible()

// GOOD: Wait for the actual state change
await page.click('button')
await expect(page.getByText('Success')).toBeVisible({ timeout: 10000 })
```

```typescript
// BAD: Brittle CSS selector
await page.click('.css-1a2b3c')

// GOOD: Semantic selector with data-testid
await page.click('[data-testid="submit-button"]')

// GOOD: Role-based selector (preferred)
await page.click('role=button[name="Submit"]')
```

### Retry and Trace Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  timeout: 30_000,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## API Mocking

Mock external APIs to ensure deterministic, fast E2E tests:

```typescript
// tests/e2e/payment-flow.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Payment Flow', () => {
  test('successful payment completes order', async ({ page }) => {
    // Mock Stripe API
    await page.route('**/api/stripe/create-payment-intent', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          clientSecret: 'pi_test_secret_123',
          id: 'pi_123',
        }),
      })
    })

    // Mock order confirmation webhook
    await page.route('**/api/webhooks/stripe', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ received: true }),
      })
    })

    await page.goto('/checkout')
    await page.fill('[data-testid="card-number"]', '4242424242424242')
    await page.fill('[data-testid="card-expiry"]', '12/30')
    await page.fill('[data-testid="card-cvc"]', '123')
    await page.click('[data-testid="pay-button"]')

    await expect(page.getByText('Payment Successful')).toBeVisible()
    await expect(page).toHaveURL(/\/order-confirmation/)
  })

  test('failed payment shows error', async ({ page }) => {
    await page.route('**/api/stripe/create-payment-intent', async (route) => {
      await route.fulfill({
        status: 402,
        body: JSON.stringify({ error: { message: 'Card declined' } }),
      })
    })

    await page.goto('/checkout')
    await page.click('[data-testid="pay-button"]')
    await expect(page.getByText('Card declined')).toBeVisible()
  })
})
```

## Visual Regression Testing

Capture and compare screenshots to detect unintended UI changes:

```typescript
// tests/e2e/visual-regression.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Visual Regression', () => {
  test('login page matches baseline', async ({ page }) => {
    await page.goto('/login')
    await expect(page).toHaveScreenshot('login-page.png', {
      maxDiffPixels: 100,
      fullPage: true,
    })
  })

  test('dashboard layout is stable', async ({ page }) => {
    await page.goto('/dashboard')
    // Wait for all async content to load
    await page.waitForSelector('[data-testid="item-list"]')
    await expect(page).toHaveScreenshot('dashboard-layout.png', {
      maxDiffPixels: 200,
    })
  })

  test('mobile login page matches baseline', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/login')
    await expect(page).toHaveScreenshot('login-mobile.png', {
      maxDiffPixels: 100,
      fullPage: true,
    })
  })
})
```

Update baselines after intentional UI changes:

```bash
# Update visual baselines
npx playwright test --update-snapshots

# Run visual tests only
npx playwright test visual-regression --project=chromium
```

## Cross-Browser Testing

Run the same test suite across multiple browsers:

```bash
# Install all browsers
npx playwright install

# Run all browser projects
npx playwright test --project=chromium --project=firefox --project=webkit

# Run only mobile browsers
npx playwright test --project=mobile-chrome --project=mobile-safari

# Run with HTML report
npx playwright test --reporter=html
npx playwright show-report
```

### Browser-Specific Quirks to Watch For

| Issue | Chromium | Firefox | WebKit |
|---|---|---|---|
| Date input format | `yyyy-MM-dd` | `MM/dd/yyyy` | `dd/MM/yyyy` |
| File upload behavior | Native dialog | Native dialog | May need `setInputFiles` |
| CSS support | Full | Full | Minor gaps in older versions |
| Cookie handling | Third-party blocked by default | User-configurable | ITP restrictions |

Test date inputs with explicit format handling:

```typescript
// Handle date inputs across browsers
async function fillDateInput(page, selector: string, date: Date) {
  const formatted = date.toISOString().split('T')[0] // yyyy-MM-dd
  await page.fill(selector, formatted)
  // Verify the browser accepted the value
  const actual = await page.inputValue(selector)
  expect(actual).toBe(formatted)
}
```

## E2E Test Organization

```
project/
├── tests/
│   ├── e2e/
│   │   ├── auth-flow.spec.ts        # Login, signup, password reset
│   │   ├── item-management.spec.ts  # CRUD operations
│   │   ├── payment-flow.spec.ts     # Checkout, Stripe mock
│   │   └── visual-regression.spec.ts # Screenshot baselines
│   ├── fixtures/
│   │   └── auth.ts                  # Shared authentication fixtures
│   ├── pages/
│   │   ├── LoginPage.ts             # Page object for /login
│   │   └── DashboardPage.ts         # Page object for /dashboard
│   └── playwright.config.ts         # Browser projects, timeouts
```

## CI/CD Integration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # Daily smoke test

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium
      - name: Run E2E tests
        run: npx playwright test --project=chromium
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---|---|---|
| Testing every single page | Slow, high maintenance | Cover critical flows, unit test the rest |
| `waitForTimeout(5000)` everywhere | Flaky on variable load times | Wait for specific selectors/state |
| Hardcoded credentials in tests | Security risk, not portable | Use env vars + fixtures for auth |
| Tests sharing state | Order dependency, cascading failures | Each test creates its own data |
| No cleanup after tests | Database grows, tests slow down | Use transaction rollback or per-test schemas |
| Screenshot tests on dynamic content | Every run differs | Mock dates, random values, or use `maxDiffPixels` |

## Best Practices

1. **Test critical flows only** — E2E tests are expensive; unit tests are cheap
2. **Use Page Object Model** — keeps tests readable and maintainable
3. **Mock external APIs** — deterministic results, no network dependency
4. **Wait for state, not time** — `expect(locator).toBeVisible()` not `waitForTimeout()`
5. **Use semantic selectors** — `getByRole()`, `getByTestId()`, not CSS classes
6. **Parallelize aggressively** — `fullyParallel: true`, independent test data
7. **Capture traces on failure** — `trace: 'on-first-retry'` for debugging
8. **Run daily in CI** — catch regressions before they reach production
9. **Keep tests under 30 seconds each** — slow tests indicate wrong abstraction
10. **Review flaky tests weekly** — fix or delete, never ignore

## Success Metrics

- [ ] All P0 and P1 critical flows covered by E2E tests
- [ ] Flaky test rate < 2% (failures per run)
- [ ] E2E suite completes in under 10 minutes
- [ ] Visual regression baselines updated after intentional UI changes
- [ ] Cross-browser tests pass on Chromium, Firefox, WebKit
- [ ] No hardcoded credentials or secrets in test files
- [ ] Test results visible in CI/CD pipeline with artifact upload on failure

---

**Remember:** E2E tests are your last line of automated defense. They should be reliable, fast, and focused on what matters to real users.
