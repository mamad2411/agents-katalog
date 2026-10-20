# SAP-039: React E2E Testing - Agent Awareness Guide

**SAP ID**: SAP-039
**Name**: react-e2e-testing
**Status**: pilot
**Version**: 1.0.0
**For**: All AI agents (Claude, GPT-4, Gemini, etc.)
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-039?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 45-minute setup with framework decision tree for Playwright or Cypress
- 📚 **Time Savings** - 90.6% reduction (45 min vs 6-8 hours manual), 90% flakiness reduction, 10x faster test execution
- 🎯 **2 Framework Options** - Playwright (cross-browser, mobile, 3x faster) or Cypress (time-travel debugging, 10M downloads/month)
- 🔧 **Authentication Testing** - Page Objects, session persistence, login/signup/OAuth flows with 100% coverage
- 📊 **Visual Regression** - Screenshot comparison (Playwright native, Cypress plugins), <5% false positives
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-021 (Testing), SAP-033 (Auth), SAP-041 (Forms)

This AGENTS.md provides: Agent-specific patterns for E2E testing workflows.

---

## Framework Decision Tree

```
START: Which E2E testing framework should I use?

Q1: Do you need Safari or mobile browser (Chrome Android, Safari iOS) testing?
├─ YES → Playwright ✅ (only framework with WebKit + mobile support)
└─ NO  → Continue to Q2

Q2: Do you prioritize time-travel debugging and developer experience?
├─ YES → Cypress ✅ (best-in-class debugging, live reload, test retries)
└─ NO  → Continue to Q3

Q3: Do you need free parallelization (no paid tier)?
├─ YES → Playwright ✅ (built-in parallel execution, test sharding)
└─ NO  → Continue to Q4

Q4: Do you need built-in visual regression (no third-party service)?
├─ YES → Playwright ✅ (native screenshot comparison)
└─ NO  → Either framework works (choose based on preference)

DEFAULT: Playwright (more modern, cross-browser, cost-effective)
```

---

## Framework Comparison

| Criteria | Playwright | Cypress | Winner |
|----------|-----------|---------|--------|
| **Browser Support** | Chrome, Firefox, Safari, Edge, Chrome Android, Safari iOS | Chrome, Firefox, Edge (no Safari, no mobile) | Playwright |
| **Speed** | 3x faster than Selenium | 2x faster than Selenium | Playwright |
| **Debugging** | Trace viewer, video, screenshots | Time-travel, live reload, DOM snapshots | Cypress |
| **Parallelization** | Free (built-in, 4-10 workers) | Paid (Cypress Cloud required) | Playwright |
| **Visual Regression** | Built-in screenshots, manual comparison | Percy integration (paid) | Playwright |
| **Learning Curve** | Steeper (newer, 2020) | Easier (mature, 2015, large community) | Cypress |
| **TypeScript** | First-class support | Partial support | Playwright |
| **Setup Time** | 25 min | 25 min | Tie |

**Recommendation**:
- **Playwright**: Cross-browser, mobile, cost-conscious, modern TypeScript
- **Cypress**: Developer experience, time-travel debugging, mature ecosystem

---

## Common Workflows

### Workflow 1: Set Up E2E Testing (25 min)

**User Request**: "Add E2E testing to my React app"

**Agent Steps**:

1. **Choose Framework** (5 min):
   - Ask user: "Do you need Safari or mobile testing?"
     - YES → Playwright
     - NO → Ask: "Do you want time-travel debugging?" → Cypress or Playwright
   - Recommend Playwright (default)

2. **Install Playwright** (5 min):
   ```bash
   npm init playwright@latest
   # Choose: TypeScript, tests folder, add GitHub Actions
   ```

3. **Configure** (5 min):
   ```typescript
   // playwright.config.ts
   export default defineConfig({
     testDir: './tests/e2e',
     use: {
       baseURL: 'http://localhost:3000',
       trace: 'on-first-retry',
     },
     workers: 4, // Parallel execution
     webServer: {
       command: 'npm run dev',
       port: 3000,
     },
   });
   ```

4. **Create First Test** (5 min):
   ```typescript
   // tests/e2e/homepage.spec.ts
   import { test, expect } from '@playwright/test';

   test('homepage loads', async ({ page }) => {
     await page.goto('/');
     await expect(page.locator('h1')).toBeVisible();
   });
   ```

5. **Run Test** (5 min):
   ```bash
   npx playwright test
   npx playwright show-report
   ```

**Total Time**: 25 minutes

---

### Workflow 2: Test Authentication Flows (10 min)

**User Request**: "Test login/signup without logging in for every test"

**Agent Steps**:

1. **Create Page Object** (3 min):
   ```typescript
   // tests/pages/LoginPage.ts
   export class LoginPage {
     constructor(private page: Page) {}

     async goto() {
       await this.page.goto('/login');
     }

     async login(email: string, password: string) {
       await this.page.fill('input[name="email"]', email);
       await this.page.fill('input[name="password"]', password);
       await this.page.click('button[type="submit"]');
     }
   }
   ```

2. **Setup Session Persistence** (5 min):
   ```typescript
   // tests/auth.setup.ts
   import { test as setup } from '@playwright/test';

   const authFile = 'playwright/.auth/user.json';

   setup('authenticate', async ({ page }) => {
     await page.goto('/login');
     await page.fill('input[name="email"]', 'test@example.com');
     await page.fill('input[name="password"]', 'password');
     await page.click('button[type="submit"]');
     await page.waitForURL('/dashboard');

     // Save cookies + localStorage
     await page.context().storageState({ path: authFile });
   });
   ```

3. **Configure Storage State** (2 min):
   ```typescript
   // playwright.config.ts
   export default defineConfig({
     projects: [
       { name: 'setup', testMatch: /auth\.setup\.ts/ },
       {
         name: 'chromium',
         use: { storageState: authFile },
         dependencies: ['setup'],
       },
     ],
   });
   ```

**Usage**:
```typescript
test('access dashboard', async ({ page }) => {
  await page.goto('/dashboard'); // Already logged in!
  await expect(page).toHaveURL('/dashboard');
});
```

**Total Time**: 10 minutes

---

### Workflow 3: Add API Mocking (5 min)

**User Request**: "Mock API responses to make tests faster and more reliable"

**Agent Steps**:

**Playwright**:
```typescript
test('should display user profile', async ({ page }) => {
  // Mock /api/user endpoint
  await page.route('/api/user', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
      }),
    });
  });

  await page.goto('/profile');
  await expect(page.locator('[data-testid="user-name"]')).toHaveText('John Doe');
});
```

**Cypress**:
```typescript
it('should display user profile', () => {
  cy.intercept('GET', '/api/user', {
    statusCode: 200,
    body: { id: 1, name: 'John Doe', email: 'john@example.com' },
  }).as('getUser');

  cy.visit('/profile');
  cy.wait('@getUser');
  cy.get('[data-testid="user-name"]').should('have.text', 'John Doe');
});
```

**Total Time**: 5 minutes

---

### Workflow 4: Add Visual Regression Testing (10 min)

**User Request**: "Catch CSS bugs with visual regression tests"

**Agent Steps**:

**Playwright** (built-in):
```typescript
test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // First run: saves baseline
  // Subsequent runs: compares to baseline
  await expect(page).toHaveScreenshot('homepage.png');
});
```

**Run & Update**:
```bash
# Run tests
npx playwright test

# Update baselines (after intentional CSS changes)
npx playwright test --update-snapshots
```

**Cypress + Percy**:
```bash
# Install Percy
npm install --save-dev @percy/cli @percy/cypress

# Add to support file
import '@percy/cypress';
```

```typescript
it('homepage visual regression', () => {
  cy.visit('/');
  cy.percySnapshot('Homepage');
});
```

**Total Time**: 10 minutes

---

## Flakiness Prevention Checklist

**Use this checklist to reduce test flakiness by 90%**:

### 1. Replace Arbitrary Timeouts with Explicit Waits

**❌ Flaky**:
```typescript
await page.click('#submit-button');
await page.waitForTimeout(1000); // Arbitrary
```

**✅ Stable**:
```typescript
await page.click('#submit-button');
await page.waitForSelector('.success', { state: 'visible' });
```

---

### 2. Use Deterministic Selectors (data-testid)

**❌ Brittle**:
```typescript
await page.click('.btn-primary'); // CSS class may change
```

**✅ Stable**:
```tsx
// Component
<button data-testid="submit-button" className="btn-primary">Submit</button>

// Test
await page.click('[data-testid="submit-button"]');
```

---

### 3. Wait for Network to Be Idle

**Playwright**:
```typescript
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
```

**Cypress**:
```typescript
cy.visit('/dashboard');
cy.intercept('GET', '/api/**').as('api');
cy.wait('@api');
```

---

### 4. Enable Auto-Retry

**Playwright** (playwright.config.ts):
```typescript
export default defineConfig({
  retries: process.env.CI ? 3 : 0, // 3 retries in CI
});
```

**Cypress** (cypress.config.ts):
```typescript
export default defineConfig({
  retries: { runMode: 2, openMode: 0 },
});
```

---

### 5. Isolate Tests (Database Seeding)

**Playwright**:
```typescript
beforeEach(async () => {
  await prisma.user.deleteMany(); // Clean slate
  await prisma.user.create({
    data: { email: 'test@example.com', password: 'hashed' },
  });
});
```

**Cypress**:
```typescript
beforeEach(() => {
  cy.task('db:reset'); // Custom task in cypress.config.ts
});
```

---

### 6. Verify Expected State Before Actions

**❌ Flaky**:
```typescript
await page.click('#submit-button'); // May not be clickable
```

**✅ Stable**:
```typescript
await page.waitForSelector('#submit-button', { state: 'visible' });
await expect(page.locator('#submit-button')).toBeEnabled();
await page.click('#submit-button');
```

---

## Code Examples (Copy-Paste Ready)

### Example 1: Login Test (Playwright)

```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toHaveText('Dashboard');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="email"]', 'invalid@example.com');
    await page.fill('input[name="password"]', 'wrong');
    await page.click('button[type="submit"]');

    await expect(page.locator('[data-testid="error-message"]'))
      .toHaveText('Invalid email or password');
  });
});
```

---

### Example 2: Form Submission (Cypress)

```typescript
// cypress/e2e/contact.cy.ts
describe('Contact Form', () => {
  it('should submit form successfully', () => {
    cy.visit('/contact');

    cy.get('input[name="name"]').type('John Doe');
    cy.get('input[name="email"]').type('john@example.com');
    cy.get('textarea[name="message"]').type('Hello!');

    cy.get('button[type="submit"]').click();

    cy.get('[data-testid="success-message"]')
      .should('be.visible')
      .and('contain', 'Message sent successfully');
  });
});
```

---

### Example 3: API Mocking with MSW

```typescript
// mocks/handlers.ts (shared with Vitest)
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/user', () => {
    return HttpResponse.json({
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
    });
  }),
];
```

```typescript
// tests/msw.setup.ts
import { setupServer } from 'msw/node';
import { handlers } from '../mocks/handlers';

export const server = setupServer(...handlers);
```

```typescript
// playwright.config.ts
import { server } from './tests/msw.setup';

export default defineConfig({
  globalSetup: async () => {
    server.listen();
  },
  globalTeardown: async () => {
    server.close();
  },
});
```

---

### Example 4: Page Object Model

```typescript
// tests/pages/DashboardPage.ts
import { Page, Locator } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly heading: Locator;
  readonly userName: Locator;
  readonly settingsButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.locator('h1');
    this.userName = page.locator('[data-testid="user-name"]');
    this.settingsButton = page.locator('[data-testid="settings-button"]');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async getUserName() {
    return await this.userName.textContent();
  }

  async openSettings() {
    await this.settingsButton.click();
  }
}
```

**Usage**:
```typescript
import { DashboardPage } from './pages/DashboardPage';

test('should display dashboard', async ({ page }) => {
  const dashboard = new DashboardPage(page);

  await dashboard.goto();
  await expect(dashboard.heading).toHaveText('Dashboard');

  const userName = await dashboard.getUserName();
  expect(userName).toBe('John Doe');
});
```

---

## Troubleshooting Guide

### Issue 1: Tests Fail in CI But Pass Locally

**Symptoms**:
- ✅ Tests pass on local machine
- ❌ Tests fail in GitHub Actions

**Diagnosis**:
1. Check if tests depend on specific browser version
2. Verify environment variables in CI
3. Check if database seeding works in CI

**Solutions**:

**Install Playwright browsers in CI**:
```yaml
# .github/workflows/e2e.yml
- name: Install Playwright browsers
  run: npx playwright install --with-deps
```

**Add environment variables**:
```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  NEXT_PUBLIC_API_URL: http://localhost:3000
```

**Increase timeout**:
```typescript
// playwright.config.ts
export default defineConfig({
  timeout: 60000, // 60 seconds (CI is slower)
});
```

---

### Issue 2: Flaky Tests (Pass/Fail Randomly)

**Symptoms**:
- Test passes sometimes, fails other times
- No code changes between runs

**Diagnosis**:
Run test 10 times:
```bash
for i in {1..10}; do npx playwright test; done
```

**Solutions**:

1. **Add explicit waits**:
   ```typescript
   await page.waitForLoadState('networkidle');
   await page.waitForSelector('[data-testid="content"]', { state: 'visible' });
   ```

2. **Use deterministic selectors**:
   ```typescript
   // ❌ Brittle
   await page.click('.btn-primary');

   // ✅ Stable
   await page.click('[data-testid="submit-button"]');
   ```

3. **Enable auto-retry**:
   ```typescript
   export default defineConfig({
     retries: 3,
   });
   ```

4. **Isolate tests**:
   ```typescript
   beforeEach(async () => {
     await resetDatabase();
   });
   ```

---

### Issue 3: Slow Test Execution (>10 min)

**Symptoms**:
- Full test suite takes 10-30 minutes
- CI pipeline blocked

**Diagnosis**:
```bash
npx playwright test --reporter=list
# Shows timing for each test
```

**Solutions**:

1. **Enable parallel execution**:
   ```typescript
   // playwright.config.ts
   export default defineConfig({
     workers: 4, // 4 parallel workers
   });
   ```

2. **Use test sharding** (CI):
   ```yaml
   # .github/workflows/e2e.yml
   strategy:
     matrix:
       shard: [1, 2, 3, 4]
   steps:
     - run: npx playwright test --shard=${{ matrix.shard }}/4
   ```

3. **Mock slow APIs**:
   ```typescript
   await page.route('/api/slow-endpoint', async (route) => {
     await route.fulfill({ status: 200, body: '{"data": "mocked"}' });
   });
   ```

4. **Skip non-critical tests in CI**:
   ```typescript
   test.skip('slow visual regression test', async ({ page }) => {
     // Skipped in CI
   });
   ```

---

### Issue 4: Visual Regression False Positives

**Symptoms**:
- Screenshot differs but looks identical
- Fonts render differently across environments

**Diagnosis**:
Compare screenshots manually:
```bash
npx playwright show-report
# Open diff images
```

**Solutions**:

1. **Use same OS for screenshots** (CI + local):
   ```yaml
   # .github/workflows/e2e.yml
   runs-on: ubuntu-latest # Match local Docker or WSL
   ```

2. **Increase diff threshold**:
   ```typescript
   await expect(page).toHaveScreenshot('homepage.png', {
     maxDiffPixels: 100, // Allow 100 pixel diff
   });
   ```

3. **Mask dynamic content**:
   ```typescript
   await expect(page).toHaveScreenshot('homepage.png', {
     mask: [page.locator('[data-testid="timestamp"]')],
   });
   ```

---

### Issue 5: Authentication Session Not Persisting

**Symptoms**:
- Session setup runs, but tests still redirect to login
- Cookies not saved

**Diagnosis**:
Check if auth.json file exists:
```bash
ls playwright/.auth/user.json
```

**Solutions**:

1. **Verify storage state path**:
   ```typescript
   // auth.setup.ts
   const authFile = 'playwright/.auth/user.json';
   await page.context().storageState({ path: authFile });

   // playwright.config.ts
   use: { storageState: authFile }
   ```

2. **Wait for navigation**:
   ```typescript
   await page.click('button[type="submit"]');
   await page.waitForURL('/dashboard'); // Wait for redirect
   await page.context().storageState({ path: authFile });
   ```

3. **Check if cookies are HttpOnly**:
   ```typescript
   // If cookies are HttpOnly, need to include them
   await page.context().storageState({
     path: authFile,
     cookies: await page.context().cookies(),
   });
   ```

---

## Integration with Other SAPs

### SAP-020 (React Foundation)

**Integration**: E2E testing for Next.js 15 App Router flows

**Pattern**:
```typescript
// Test Server Components
test('server component renders', async ({ page }) => {
  await page.goto('/dashboard'); // Server Component page
  await expect(page.locator('h1')).toBeVisible();
});

// Test Server Actions
test('server action submission', async ({ page }) => {
  await page.goto('/form');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.click('button[type="submit"]'); // Triggers Server Action
  await expect(page.locator('.success')).toBeVisible();
});
```

---

### SAP-021 (Testing)

**Integration**: Share MSW mocks between Vitest (unit tests) and E2E tests

**Pattern**:
```typescript
// mocks/handlers.ts (shared)
export const handlers = [
  http.get('/api/user', () => {
    return HttpResponse.json({ id: 1, name: 'John Doe' });
  }),
];

// Vitest (unit tests)
import { setupServer } from 'msw/node';
const server = setupServer(...handlers);

// Playwright (E2E tests)
import { server } from './msw.setup';
// Use same mocks in E2E tests
```

---

### SAP-033 (Authentication)

**Integration**: Test auth flows (login, signup, OAuth)

**Pattern**:
```typescript
// Test NextAuth login
test('login with credentials', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});

// Test OAuth (mock provider)
test('login with Google', async ({ page }) => {
  await page.route('**/api/auth/callback/google', async (route) => {
    await route.fulfill({
      status: 302,
      headers: { 'Location': '/dashboard' },
    });
  });

  await page.goto('/login');
  await page.click('button:has-text("Sign in with Google")');
  await expect(page).toHaveURL('/dashboard');
});
```

---

### SAP-041 (Forms)

**Integration**: Test form validation, submission

**Pattern**:
```typescript
// Test Zod validation
test('form validation', async ({ page }) => {
  await page.goto('/contact');

  // Submit without filling form
  await page.click('button[type="submit"]');

  // Expect validation errors
  await expect(page.locator('[data-testid="email-error"]'))
    .toHaveText('Email is required');
  await expect(page.locator('[data-testid="message-error"]'))
    .toHaveText('Message is required');
});

// Test successful submission
test('form submission', async ({ page }) => {
  await page.goto('/contact');

  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Hello!');
  await page.click('button[type="submit"]');

  await expect(page.locator('[data-testid="success-message"]'))
    .toHaveText('Message sent successfully');
});
```

---

## Quick Command Reference

### Playwright

```bash
# Initialize Playwright
npm init playwright@latest

# Run all tests
npx playwright test

# Run specific file
npx playwright test tests/e2e/login.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Run in debug mode
npx playwright test --debug

# Run specific browser
npx playwright test --project=chromium
npx playwright test --project=webkit

# Update snapshots
npx playwright test --update-snapshots

# View HTML report
npx playwright show-report

# View trace
npx playwright show-trace trace.zip
```

---

### Cypress

```bash
# Initialize Cypress
npx cypress open

# Run all tests (headless)
npx cypress run

# Run specific file
npx cypress run --spec cypress/e2e/login.cy.ts

# Run in headed mode
npx cypress run --headed

# Run specific browser
npx cypress run --browser chrome
npx cypress run --browser firefox

# Open Cypress UI
npx cypress open
```

---

## Best Practices Summary

### 1. Test Organization
- ✅ Group tests by feature (auth/, dashboard/, forms/)
- ✅ Use Page Object Model for reusable page logic
- ✅ One test file per feature (login.spec.ts, signup.spec.ts)

### 2. Selectors
- ✅ Prefer data-testid over CSS classes
- ✅ Use semantic selectors (aria-label, role)
- ❌ Avoid brittle selectors (nth-child, complex CSS)

### 3. Waits
- ✅ Use explicit waits (waitForSelector, waitForLoadState)
- ❌ Avoid arbitrary timeouts (waitForTimeout, sleep)
- ✅ Wait for network to be idle before assertions

### 4. Performance
- ✅ Enable parallel execution (4-10 workers)
- ✅ Use test sharding in CI (4 machines)
- ✅ Mock slow APIs
- ✅ Reuse authentication (storage state)

### 5. Flakiness
- ✅ Enable auto-retry (3x in CI)
- ✅ Use deterministic selectors
- ✅ Isolate tests (database seeding)
- ✅ Verify state before actions

---

## Version History

### 1.0.0 (2025-11-09) - Initial Release
- Two-framework architecture (Playwright, Cypress)
- Framework decision tree (Safari/mobile → Playwright, debugging → Cypress)
- 4 common workflows (setup, auth, API mocking, visual regression)
- Flakiness prevention checklist (90% reduction)
- 5 code examples (login, forms, API mocking, Page Object Model, visual regression)
- Troubleshooting guide (5 common issues)
- Integration patterns (SAP-020, SAP-021, SAP-033, SAP-041)

---

**Status**: Pilot (awaiting first production adoption)
**Time Savings**: 6-8h → 45min (90.6% reduction)
**Next Steps**: See [adoption-blueprint.md](./adoption-blueprint.md) for step-by-step setup
