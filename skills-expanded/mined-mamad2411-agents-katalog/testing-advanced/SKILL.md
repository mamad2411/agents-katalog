---
name: testing-advanced
version: "1.0.0"
description: |
  Advanced testing: E2E with Playwright/Cypress, property-based testing,
  mutation testing, contract testing, and CI/CD pipelines.

  Use when: (1) E2E tests with Playwright/Cypress, (2) Property-based testing
  with fast-check, (3) Mutation testing, (4) Contract testing with Pact,
  (5) CI/CD test pipelines, (6) Flaky test management.

  Auto-detects: playwright.config.*, cypress.config.*, e2e/, pact, fast-check,
  stryker, mutation in package.json
related:
  - testing
  - devops
  - api-design
---

# Testing Advanced Skill

E2E, property-based, mutation, and CI/CD testing patterns.

## E2E with Playwright

```bash
npx playwright test           # Run all
npx playwright test --ui      # UI mode
npx playwright test --debug   # Debug mode
npx playwright codegen        # Generate tests
```

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async expectLoggedIn() {
    await expect(this.page).toHaveURL('/dashboard');
  }
}

// tests/auth.spec.ts
test('should login successfully', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');
  await loginPage.login('user@test.com', 'password');
  await loginPage.expectLoggedIn();
});
```

### Visual Regression

```typescript
test('should match screenshot', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100,
  });
});
```

## Cypress Configuration

```typescript
// cypress.config.ts
export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.ts',
    specPattern: 'cypress/e2e/**/*.cy.ts',
  },
  retries: { runMode: 2, openMode: 0 },
});
```

## Property-Based Testing

```typescript
import fc from 'fast-check';

describe('string operations', () => {
  it('reverse(reverse(s)) === s', () => {
    fc.assert(
      fc.property(fc.string(), (s) => {
        return reverse(reverse(s)) === s;
      })
    );
  });

  it('sort is idempotent', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted = sort(arr);
        return JSON.stringify(sort(sorted)) === JSON.stringify(sorted);
      })
    );
  });
});
```

## Mutation Testing (Stryker)

```json
// stryker.conf.json
{
  "mutate": ["src/**/*.ts", "!src/**/*.spec.ts"],
  "testRunner": "jest",
  "reporters": ["html", "clear-text"],
  "thresholds": { "high": 80, "low": 60, "break": 50 }
}
```

```bash
npx stryker run
```

## Contract Testing (Pact)

```typescript
// Consumer test
const provider = new Pact({
  consumer: 'FrontendApp',
  provider: 'UserService',
});

describe('User API', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('should get user', async () => {
    await provider.addInteraction({
      state: 'user exists',
      uponReceiving: 'get user request',
      withRequest: { method: 'GET', path: '/users/1' },
      willRespondWith: {
        status: 200,
        body: { id: 1, name: 'John' },
      },
    });

    const user = await getUser(1);
    expect(user.name).toBe('John');
  });
});
```

## CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }

      - run: npm ci
      - run: npm run test:cov

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4

      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Flaky Test Management

```typescript
// Retry configuration
test.describe.configure({ retries: 2 });

// Wait for stability
await expect(element).toBeVisible({ timeout: 10000 });

// Avoid timing issues
await page.waitForLoadState('networkidle');
```

## F5 Quality Gates

| Gate | Requirement |
|------|-------------|
| G3 | E2E critical paths verified |
| G4 | Contract tests pass |
| G5 | Production smoke tests |
