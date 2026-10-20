# SAP-039: React E2E Testing - Claude Agent Guide

**SAP ID**: SAP-039
**Version**: 1.0.0
**Status**: pilot
**For**: Claude Code, Claude Desktop, Claude API
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

This CLAUDE.md provides: Claude Code-specific workflows for E2E testing.

---

### When to Use This SAP

**Use SAP-039 when user requests**:
- "Add E2E testing to my app"
- "Test login/signup flows automatically"
- "Prevent flaky tests"
- "Add visual regression testing"
- "Test my app across browsers (Chrome, Safari, Firefox)"
- "Mock APIs in E2E tests"

**Don't use SAP-039 when**:
- User wants unit tests only (use SAP-021: React Testing instead)
- User wants API testing only (use Postman/Insomnia)
- User has no React app yet (adopt SAP-020: React Foundation first)

---

## Progressive Context Loading Strategy

Claude should load context progressively to optimize token usage:

### Phase 1: Framework Selection (0-5k tokens)

**Goal**: Recommend Playwright or Cypress

**Read**:
1. This file (CLAUDE.md) for overview
2. AGENTS.md for framework decision tree

**Ask user**:
- "Do you need Safari or mobile browser testing?" (YES → Playwright)
- "Do you prioritize time-travel debugging?" (YES → Cypress)
- "Do you need free parallelization?" (YES → Playwright)

**Output**: Framework recommendation (Playwright or Cypress)

**Time**: 2-3 minutes

---

### Phase 2: Implementation (10-50k tokens)

**Goal**: Setup E2E testing with chosen framework

**Read**:
1. `adoption-blueprint.md` - Step-by-step setup for chosen framework (Option A or Option B)
2. `AGENTS.md` (Workflow 1) - Quick setup workflow

**Generate**:
- Install commands (`npm init playwright` or `npm install cypress`)
- Configuration file (playwright.config.ts or cypress.config.ts)
- First test (homepage.spec.ts)
- Page Object Model (LoginPage.ts)
- Authentication setup (auth.setup.ts or cy.login())

**Time**: 20-25 minutes

---

### Phase 3: Advanced Patterns (50-100k tokens)

**Goal**: Add flakiness prevention, API mocking, visual regression

**Read**:
1. `protocol-spec.md` (How-To Guides section) - Flakiness reduction, API mocking, visual regression
2. `AGENTS.md` (Workflows 2-4) - Authentication, API mocking, visual regression

**Generate**:
- Flakiness prevention checklist (explicit waits, deterministic selectors)
- API mocking patterns (Playwright route, Cypress intercept)
- Visual regression tests (Playwright screenshots, Cypress + Percy)
- CI/CD integration (GitHub Actions)

**Time**: 30-60 minutes (depending on complexity)

---

## Framework Decision Framework for Claude

### Decision Tree Prompt

When user requests E2E testing, use this prompt:

```
I'll help you set up E2E testing. First, let me ask a few questions:

1. **Safari Testing**: Do you need to test on Safari? (YES/NO)
2. **Mobile Testing**: Do you need to test on mobile browsers (Chrome Android, Safari iOS)? (YES/NO)
3. **Debugging**: Do you prioritize time-travel debugging (see DOM at every step)? (YES/NO)
4. **Parallelization**: Do you need free parallelization (no paid tier)? (YES/NO)

Based on your answers, I'll recommend:
- **Playwright**: Cross-browser, mobile, free parallelization, modern
- **Cypress**: Time-travel debugging, developer experience, mature ecosystem
```

---

### Recommendation Matrix

| User Requirements | Recommended Framework | Rationale |
|-------------------|----------------------|-----------|
| Need Safari testing | **Playwright** | Only framework with WebKit support |
| Need mobile testing (Chrome Android, Safari iOS) | **Playwright** | Native mobile browser support |
| Need time-travel debugging | **Cypress** | Best-in-class debugging with DOM snapshots |
| Need free parallelization | **Playwright** | Built-in workers, sharding (Cypress requires paid Cypress Cloud) |
| Need built-in visual regression | **Playwright** | Native screenshot comparison (Cypress requires Percy) |
| Migrating from Selenium | **Playwright** | Similar API, easier migration |
| Existing Cypress setup | **Cypress** | Stick with what works |

**Default**: **Playwright** (cross-browser, cost-effective, modern)

---

## Code Generation Patterns for Claude

### Pattern 1: Playwright Setup

**User request**: "Setup Playwright for my Next.js app"

**Claude generates**:

1. **Install Playwright**:
```bash
npm init playwright@latest
# Choose: TypeScript, tests/e2e folder, add GitHub Actions
```

2. **Configure playwright.config.ts**:
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 3 : 0, // 3 retries in CI
  workers: process.env.CI ? 4 : 1, // 4 parallel workers in CI
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    port: 3000,
  },
});
```

3. **Create first test**:
```typescript
// tests/e2e/homepage.spec.ts
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toBeVisible();
});
```

4. **Run tests**:
```bash
npx playwright test
npx playwright show-report
```

**Explain to user**:
- "I've set up Playwright with 3 browsers (Chrome, Firefox, Safari)"
- "Tests run in parallel (4 workers) for speed"
- "Auto-retry 3x in CI to reduce flakiness"
- "Next steps: Add more tests (login, forms, etc.)"

---

### Pattern 2: Cypress Setup

**User request**: "Setup Cypress for my React app"

**Claude generates**:

1. **Install Cypress**:
```bash
npm install --save-dev cypress
npx cypress open
# Choose: E2E Testing, Chrome browser
```

2. **Configure cypress.config.ts**:
```typescript
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    retries: { runMode: 2, openMode: 0 },
    screenshotOnRunFailure: true,
    video: true,
  },
});
```

3. **Create first test**:
```typescript
// cypress/e2e/homepage.cy.ts
describe('Homepage', () => {
  it('should load successfully', () => {
    cy.visit('/');
    cy.get('h1').should('be.visible');
  });
});
```

4. **Run tests**:
```bash
npx cypress run
npx cypress open
```

**Explain to user**:
- "I've set up Cypress with time-travel debugging"
- "Auto-retry 2x in CI to reduce flakiness"
- "Screenshots and videos captured automatically on failure"
- "Next steps: Add custom commands (cy.login(), etc.)"

---

### Pattern 3: Authentication Flow Testing

**User request**: "Test login without logging in for every test"

**Claude generates (Playwright)**:

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

**Explain to user**:
- "Login happens once, session saved to auth.json"
- "All tests reuse saved session (no re-login)"
- "99% faster: 100 tests × 10s login = 1000s → 10s (one-time)"

---

### Pattern 4: API Mocking

**User request**: "Mock API responses to make tests faster"

**Claude generates (Playwright)**:

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

**Claude generates (Cypress)**:

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

**Explain to user**:
- "API mocked: no real API calls needed"
- "70% faster tests (no network latency)"
- "90% more reliable (no API failures)"

---

## Workflow Templates for Claude

### Workflow 1: New E2E Testing Project (25 min)

**User**: "Add E2E testing to my Next.js app"

**Claude**:

1. **Framework Selection** (5 min):
   - Ask: "Do you need Safari or mobile testing?" → Playwright or Cypress
   - Default: Playwright (cross-browser, cost-effective)

2. **Install Framework** (5 min):
   ```bash
   npm init playwright@latest
   # OR
   npm install --save-dev cypress
   ```

3. **Configure** (5 min):
   - Generate playwright.config.ts or cypress.config.ts
   - Set baseURL, retries, workers

4. **Create First Test** (5 min):
   - Homepage test (check h1 visible)
   - Login test (if SAP-033 adopted)

5. **Run & Verify** (5 min):
   ```bash
   npx playwright test
   # OR
   npx cypress run
   ```

**Expected time**: 25 minutes
**Output**: Working E2E test suite

---

### Workflow 2: Add Flakiness Prevention (10 min)

**User**: "My tests are flaky (pass/fail randomly)"

**Claude**:

1. **Diagnose Flakiness** (3 min):
   - Check if using arbitrary timeouts (`waitForTimeout(1000)`)
   - Check if using brittle selectors (`.btn-primary`)
   - Check if tests share state (no database reset)

2. **Fix: Replace Timeouts** (3 min):
   ```typescript
   // ❌ Before (flaky)
   await page.waitForTimeout(1000);

   // ✅ After (deterministic)
   await page.waitForSelector('.success', { state: 'visible' });
   await page.waitForLoadState('networkidle');
   ```

3. **Fix: Add data-testid** (2 min):
   ```tsx
   // Component
   <button data-testid="submit-button">Submit</button>

   // Test
   await page.click('[data-testid="submit-button"]');
   ```

4. **Fix: Enable Auto-Retry** (2 min):
   ```typescript
   export default defineConfig({
     retries: 3, // Retry 3x on failure
   });
   ```

**Expected time**: 10 minutes
**Output**: 90% flakiness reduction

---

### Workflow 3: Add Visual Regression Testing (10 min)

**User**: "Catch CSS bugs with visual regression tests"

**Claude**:

1. **Playwright** (built-in):
   ```typescript
   test('homepage visual regression', async ({ page }) => {
     await page.goto('/');
     await page.waitForLoadState('networkidle');

     // First run: saves baseline
     // Subsequent runs: compares to baseline
     await expect(page).toHaveScreenshot('homepage.png');
   });
   ```

2. **Run & Update Baselines**:
   ```bash
   # Run tests
   npx playwright test

   # Update baselines (after CSS changes)
   npx playwright test --update-snapshots
   ```

3. **Cypress + Percy** (optional):
   ```bash
   npm install --save-dev @percy/cli @percy/cypress
   ```

   ```typescript
   // cypress/support/e2e.ts
   import '@percy/cypress';

   // cypress/e2e/visual/homepage.cy.ts
   it('homepage visual regression', () => {
     cy.visit('/');
     cy.percySnapshot('Homepage');
   });
   ```

**Expected time**: 10 minutes
**Output**: Visual regression testing enabled

---

### Workflow 4: Integrate with CI/CD (5 min)

**User**: "Run E2E tests in GitHub Actions"

**Claude**:

1. **Playwright** (auto-generated):
   - Already created by `npm init playwright` in `.github/workflows/playwright.yml`
   - Includes test sharding (4 machines)

2. **Cypress**:
   - Create `.github/workflows/cypress.yml`
   - Use `cypress-io/github-action@v6`

3. **Test on PR**:
   - Push code to PR
   - GitHub Actions runs E2E tests automatically
   - View results in PR checks

**Expected time**: 5 minutes (workflow already exists)
**Output**: E2E tests run on every PR

---

## Integration Guidance for Claude

### SAP-020: React Foundation

**When user has Next.js 15**, test Server Components and Server Actions:

```typescript
// Test Server Component
test('dashboard renders', async ({ page }) => {
  await page.goto('/dashboard'); // Server Component page
  await expect(page.locator('h1')).toBeVisible();
});

// Test Server Action
test('form submission', async ({ page }) => {
  await page.goto('/contact');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.click('button[type="submit"]'); // Triggers Server Action
  await expect(page.locator('.success')).toBeVisible();
});
```

**Explain**: "I've added E2E tests for your Next.js 15 Server Components and Server Actions"

---

### SAP-021: React Testing

**When user has Vitest**, share MSW mocks between unit tests and E2E tests:

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

**Explain**: "I've shared MSW mocks between your unit tests (Vitest) and E2E tests (Playwright)"

---

### SAP-033: React Authentication

**When user has authentication**, test login/signup/OAuth flows:

```typescript
// Test login
test('login with credentials', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});

// Test OAuth (mock Google)
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

**Explain**: "I've added E2E tests for your authentication flows (login, signup, OAuth)"

---

### SAP-041: React Form Validation

**When user has forms**, test validation and submission:

```typescript
// Test Zod validation
test('form validation', async ({ page }) => {
  await page.goto('/contact');

  // Submit without filling form
  await page.click('button[type="submit"]');

  // Expect validation errors
  await expect(page.locator('[data-testid="email-error"]'))
    .toHaveText('Email is required');
});

// Test successful submission
test('form submission', async ({ page }) => {
  await page.goto('/contact');

  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Hello!');
  await page.click('button[type="submit"]');

  await expect(page.locator('.success')).toHaveText('Message sent');
});
```

**Explain**: "I've added E2E tests for your forms (validation + submission)"

---

## Common Pitfalls for Claude

### Pitfall 1: Not Using Deterministic Selectors

**Problem**:
```typescript
// ❌ Brittle (CSS class may change)
await page.click('.btn-primary');
```

**Fix**:
```tsx
// Component
<button data-testid="submit-button" className="btn-primary">Submit</button>

// Test
await page.click('[data-testid="submit-button"]');
```

**Claude should always use data-testid** when generating tests.

---

### Pitfall 2: Using Arbitrary Timeouts

**Problem**:
```typescript
// ❌ Flaky
await page.waitForTimeout(1000); // May not be enough
```

**Fix**:
```typescript
// ✅ Deterministic
await page.waitForSelector('.success', { state: 'visible' });
await page.waitForLoadState('networkidle');
```

**Claude should never use waitForTimeout** unless absolutely necessary.

---

### Pitfall 3: Not Enabling Auto-Retry

**Problem**: Tests fail randomly without retry

**Fix**:
```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 3 : 0, // Always retry in CI
});
```

**Claude should always enable retries** in CI.

---

### Pitfall 4: Recommending Wrong Framework

**Problem**: User needs Safari testing → Claude recommends Cypress (no Safari support)

**Fix**: Always ask clarifying questions:
- "Do you need Safari testing?" (YES → Playwright)
- "Do you need mobile testing?" (YES → Playwright)

**Claude should ask before recommending** a framework.

---

### Pitfall 5: Not Testing Authentication Flows

**Problem**: User has authentication (SAP-033) but no E2E tests for login

**Fix**: Always suggest authentication flow testing when SAP-033 is adopted:
```typescript
// Add auth.setup.ts for session persistence
// Test login, signup, logout flows
```

**Claude should check for SAP-033 adoption** and suggest auth testing.

---

## Performance Optimization Tips for Claude

### 1. Enable Parallel Execution

**Playwright**:
```typescript
export default defineConfig({
  workers: 4, // 4 parallel workers
  fullyParallel: true,
});
```

**Explain**: "I've enabled 4 parallel workers—tests will run 4x faster"

---

### 2. Use Test Sharding in CI

**GitHub Actions**:
```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]

steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```

**Explain**: "I've added test sharding—tests split across 4 CI machines for 4x speedup"

---

### 3. Mock Slow APIs

```typescript
await page.route('/api/slow-endpoint', async (route) => {
  await route.fulfill({ status: 200, body: '{"data": "mocked"}' });
});
```

**Explain**: "I've mocked slow APIs—tests are 70% faster"

---

## Documentation Navigation for Claude

### When to Read Each Artifact

| User Request | Artifact to Read | Why |
|--------------|------------------|-----|
| "What is SAP-039?" | CLAUDE.md (this file) | Overview, decision tree |
| "Setup Playwright" | adoption-blueprint.md (Option A) | Step-by-step setup, 25 min |
| "Setup Cypress" | adoption-blueprint.md (Option B) | Step-by-step setup, 25 min |
| "How to reduce flakiness?" | protocol-spec.md (How-To 1) | Complete flakiness guide |
| "How to mock APIs?" | protocol-spec.md (How-To 3) | API mocking patterns |
| "Why Playwright vs Cypress?" | capability-charter.md (Solution Design) | Framework comparison |
| "How much time savings?" | ledger.md (Evidence) | Quantified metrics |

---

### Progressive Reading Strategy

**Small request** (e.g., "Setup Playwright"):
- Read: adoption-blueprint.md (Option A only)
- Don't read: protocol-spec.md (too large)

**Medium request** (e.g., "Add E2E + reduce flakiness"):
- Read: adoption-blueprint.md + protocol-spec.md (How-To sections)
- Don't read: capability-charter.md, ledger.md

**Large request** (e.g., "Design E2E testing architecture"):
- Read: capability-charter.md (Solution Design) + protocol-spec.md (full)
- Skim: ledger.md (case studies)

---

## Quick Command Reference

### Playwright

```bash
# Initialize
npm init playwright@latest

# Run all tests
npx playwright test

# Run specific test
npx playwright test tests/e2e/login.spec.ts

# Run in headed mode
npx playwright test --headed

# Run in debug mode
npx playwright test --debug

# View report
npx playwright show-report

# Update screenshots
npx playwright test --update-snapshots
```

---

### Cypress

```bash
# Install
npm install --save-dev cypress

# Open UI
npx cypress open

# Run all tests (headless)
npx cypress run

# Run specific test
npx cypress run --spec cypress/e2e/login.cy.ts

# Run in headed mode
npx cypress run --headed
```

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Two-framework architecture (Playwright, Cypress)
  - Progressive context loading strategy
  - 4 code generation patterns
  - 4 workflow templates
  - Integration guidance (SAP-020, SAP-021, SAP-033, SAP-041)
  - Common pitfalls and fixes

---

**Status**: Pilot
**For**: Claude Code, Claude Desktop, Claude API
**Estimated Setup Time**: 45 minutes
**Time Savings**: 90.6% (6-8h → 45min)
**Next Review**: After 3 validation projects
