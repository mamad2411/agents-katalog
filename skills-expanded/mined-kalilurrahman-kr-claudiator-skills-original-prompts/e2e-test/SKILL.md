---
name: e2e-test
description: End-to-end testing with Playwright/Cypress for full user flows. Outputs test scenarios, page objects, CI integration, and flake reduction strategies.
argument-hint: [user flows, browser targets, test environment]
allowed-tools: Read, Write, Bash
---

# End-to-End Testing

Design E2E tests that verify complete user journeys through the UI. Not fragile Selenium scripts — modern Playwright/Cypress with auto-waiting, retry logic, and stable selectors.

## Process

1. **Identify critical flows.** Login, checkout, signup, admin tasks.
2. **Choose framework.** Playwright (multi-browser, parallel), Cypress (developer UX).
3. **Design page objects.** Reusable components, stable selectors.
4. **Handle async.** Auto-waiting, explicit waits, network idle.
5. **Manage test data.** Seed DB, API fixtures, cleanup.
6. **Run in CI.** Headless mode, screenshots on failure, video recording.
7. **Reduce flakes.** Retries, deterministic waits, stable selectors.

## Output Format

### E2E Tests: [Application Name]

**Framework:** Playwright  
**Browsers:** Chromium, Firefox, WebKit  
**Flows:** 12 critical paths  
**Execution:** Parallel (4 workers)  
**Duration:** 5 minutes (full suite)  
**Flake Rate:** < 2%

---

## Framework Comparison

| Feature | Playwright | Cypress |
|---------|-----------|---------|
| Multi-browser | ✅ Chrome, Firefox, Safari | ⚠️ Chrome, Firefox, Edge (beta) |
| Speed | Fast (parallel) | Medium |
| Auto-waiting | ✅ | ✅ |
| Network mocking | ✅ | ✅ |
| Screenshots/Video | ✅ | ✅ |
| Real mobile | ✅ Device emulation | ⚠️ Viewport only |
| Learning curve | Medium | Easy |

**Recommendation:** Playwright for flexibility, Cypress for simplicity

---

## Playwright Tests

### Basic Test
```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('https://app.example.com/login');
  
  // Fill form
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  // Verify redirect to dashboard
  await expect(page).toHaveURL(/.*dashboard/);
  await expect(page.locator('h1')).toContainText('Welcome');
});

test('shows error for invalid credentials', async ({ page }) => {
  await page.goto('https://app.example.com/login');
  
  await page.fill('input[name="email"]', 'wrong@example.com');
  await page.fill('input[name="password"]', 'wrong');
  await page.click('button[type="submit"]');
  
  // Error message appears
  await expect(page.locator('.error')).toBeVisible();
  await expect(page.locator('.error')).toContainText('Invalid credentials');
});
```

### Page Object Pattern
```typescript
// pages/LoginPage.ts
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
  
  async getErrorMessage() {
    return await this.page.locator('.error').textContent();
  }
}

// tests/login.spec.ts
test('login with page object', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  
  await expect(page).toHaveURL(/.*dashboard/);
});
```

### Complete E2E Flow
```typescript
test('complete checkout flow', async ({ page }) => {
  // 1. Login
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'buyer@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-button"]');
  
  // 2. Browse products
  await page.goto('/products');
  await page.click('text=Product A');
  
  // 3. Add to cart
  await page.click('[data-testid="add-to-cart"]');
  await expect(page.locator('.cart-count')).toHaveText('1');
  
  // 4. Proceed to checkout
  await page.click('[data-testid="cart-icon"]');
  await page.click('text=Checkout');
  
  // 5. Fill shipping
  await page.fill('[name="address"]', '123 Main St');
  await page.fill('[name="city"]', 'San Francisco');
  await page.selectOption('[name="state"]', 'CA');
  await page.fill('[name="zip"]', '94105');
  await page.click('text=Continue');
  
  // 6. Enter payment (test mode)
  await page.fill('[data-testid="card-number"]', '4242424242424242');
  await page.fill('[data-testid="card-expiry"]', '12/25');
  await page.fill('[data-testid="card-cvc"]', '123');
  
  // 7. Submit order
  await page.click('[data-testid="place-order"]');
  
  // 8. Verify confirmation
  await expect(page.locator('h1')).toContainText('Order Confirmed');
  const orderNumber = await page.locator('[data-testid="order-number"]').textContent();
  expect(orderNumber).toMatch(/^ORD-\d+/);
});
```

---

## Stable Selectors

### Bad (Fragile)
```typescript
await page.click('.btn-primary.mt-4.px-3');  // CSS classes change
await page.click('div > div > button:nth-child(2)');  // DOM structure changes
await page.click('text=Submit');  // Text changes (i18n)
```

### Good (Stable)
```typescript
await page.click('[data-testid="submit-button"]');  // Dedicated test ID
await page.click('button[aria-label="Submit form"]');  // Semantic HTML
await page.click('button:has-text("Submit")');  // Playwright text selector
```

**Add test IDs to components:**
```jsx
<button data-testid="submit-button" className="btn-primary">
  Submit
</button>
```

---

## Auto-Waiting (No Sleep!)

```typescript
// ❌ Bad: Explicit sleep
await page.click('button');
await page.waitForTimeout(2000);  // Fragile!
await expect(page.locator('.result')).toBeVisible();

// ✅ Good: Auto-waiting
await page.click('button');
await expect(page.locator('.result')).toBeVisible();  // Waits automatically

// ✅ Good: Wait for network
await page.click('button');
await page.waitForResponse(resp => resp.url().includes('/api/submit'));
await expect(page.locator('.result')).toBeVisible();
```

---

## Network Interception

### Mock API Responses
```typescript
test('shows products from mocked API', async ({ page }) => {
  // Intercept API call
  await page.route('**/api/products', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        products: [
          { id: 1, name: 'Test Product', price: 10.00 }
        ]
      })
    });
  });
  
  await page.goto('/products');
  await expect(page.locator('.product-name')).toHaveText('Test Product');
});
```

### Wait for API Call
```typescript
test('waits for data to load', async ({ page }) => {
  await page.goto('/dashboard');
  
  // Wait for specific API response
  const responsePromise = page.waitForResponse(
    resp => resp.url().includes('/api/stats') && resp.status() === 200
  );
  
  const response = await responsePromise;
  const data = await response.json();
  
  expect(data.total_users).toBeGreaterThan(0);
});
```

---

## Authentication State

```typescript
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  await page.waitForURL('**/dashboard');
  
  // Save auth state
  await page.context().storageState({ path: 'auth.json' });
});

// playwright.config.ts
export default {
  use: {
    storageState: 'auth.json'  // Reuse for all tests
  }
};

// tests/dashboard.spec.ts
test('access dashboard as logged in user', async ({ page }) => {
  // Already authenticated!
  await page.goto('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

---

## Test Data Management

### API-Based Setup
```typescript
test.beforeEach(async ({ request }) => {
  // Create test user via API
  await request.post('/api/test/users', {
    data: {
      email: 'test@example.com',
      password: 'password123'
    }
  });
  
  // Create test products
  await request.post('/api/test/products', {
    data: {
      products: [
        { name: 'Product A', price: 10.00 },
        { name: 'Product B', price: 20.00 }
      ]
    }
  });
});

test.afterEach(async ({ request }) => {
  // Cleanup
  await request.delete('/api/test/reset');
});
```

### Database Seeding
```typescript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

test.beforeAll(async () => {
  // Reset and seed test database
  await execAsync('npm run db:reset:test');
  await execAsync('npm run db:seed:test');
});
```

---

## Screenshot & Video on Failure

```typescript
// playwright.config.ts
export default {
  use: {
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure'
  }
};

// Manual screenshot
test('important flow', async ({ page }) => {
  await page.goto('/checkout');
  await page.screenshot({ path: 'checkout.png', fullPage: true });
});
```

---

## Parallel Execution

```typescript
// playwright.config.ts
export default {
  workers: process.env.CI ? 4 : 2,  // 4 workers in CI
  fullyParallel: true
};

// Run tests
npx playwright test --workers=4
```

---

## Flake Reduction

### Retry Failed Tests
```typescript
// playwright.config.ts
export default {
  retries: process.env.CI ? 2 : 0  // Retry 2x in CI
};
```

### Test Isolation
```typescript
test.describe.configure({ mode: 'parallel' });  // Isolate tests

test.beforeEach(async ({ page, context }) => {
  // Clear cookies/storage
  await context.clearCookies();
  await context.clearPermissions();
});
```

### Deterministic Waits
```typescript
// ❌ Race condition
await page.click('button');
const text = await page.locator('.result').textContent();

// ✅ Wait for stable state
await page.click('button');
await page.waitForLoadState('networkidle');
const text = await page.locator('.result').textContent();
```

---

## CI Integration

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npx playwright test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Visual Regression Testing

```typescript
test('homepage looks correct', async ({ page }) => {
  await page.goto('/');
  
  // Compare screenshot to baseline
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100  // Allow minor differences
  });
});

// Update baselines
npx playwright test --update-snapshots
```

---

## Mobile Testing

```typescript
// playwright.config.ts
import { devices } from '@playwright/test';

export default {
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'iphone', use: { ...devices['iPhone 13'] } },
    { name: 'pixel', use: { ...devices['Pixel 5'] } }
  ]
};

// Test mobile-specific behavior
test('mobile menu works', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'Mobile only');
  
  await page.goto('/');
  await page.click('[data-testid="mobile-menu-button"]');
  await expect(page.locator('nav')).toBeVisible();
});
```

## Rules

- E2E tests verify critical user flows only — 10-20 tests, not 1000.
- Use stable selectors (data-testid) not CSS classes or DOM structure.
- No explicit waits (sleep) — use auto-waiting and network idle.
- Run in CI on every PR — catch regressions before production.
- Screenshot/video on failure for debugging — essential for CI failures.
- Parallel execution reduces runtime 4x — 20min → 5min.
- Retry flaky tests 2x in CI — reduces false negatives.
- Page object pattern for reusability — avoid duplicating selectors.
- API-based test data setup faster than UI — seed via /api/test endpoints.
- Flake rate must be < 5% — fix or disable flaky tests, don't ignore.
