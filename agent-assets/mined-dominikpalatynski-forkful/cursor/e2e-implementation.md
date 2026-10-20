---
alwaysApply: false
---
# E2E Test Implementation Rule - Playwright Best Practices

## Your Role
You are an expert Playwright test engineer implementing e2e tests for React applications following industry best practices.

## Core Principles

### 1. ALWAYS use data-testid for complex/dynamic elements
```typescript
// In React components
<button data-testid="submit-order-btn">Submit</button>
<div data-testid="user-profile-card">...</div>

// In tests
await page.getByTestId('submit-order-btn').click();
```

### 2. Selector Priority (use in this order)
1. **getByRole** (BEST - accessibility-first)
```typescript
   page.getByRole('button', { name: 'Submit' })
   page.getByRole('heading', { name: 'Welcome' })
   page.getByRole('textbox', { name: 'Email' })
```

2. **getByLabel** (GOOD - for form inputs)
```typescript
   page.getByLabel('Email address')
   page.getByLabel('Password')
```

3. **getByPlaceholder** (OK - when no label)
```typescript
   page.getByPlaceholder('Enter your email')
```

4. **getByText** (OK - for unique text)
```typescript
   page.getByText('Welcome back!')
```

5. **getByTestId** (LAST RESORT - for complex/dynamic elements)
```typescript
   page.getByTestId('collections-sidebar-toggle')
```

### 3. Structure Tests with Page Object Model
```typescript
// pages/CheckoutPage.ts
export class CheckoutPage {
  constructor(private page: Page) {}

  // Locators as getters
  get emailInput() {
    return this.page.getByLabel('Email address');
  }

  get submitButton() {
    return this.page.getByRole('button', { name: 'Complete Order' });
  }

  get successMessage() {
    return this.page.getByTestId('order-success-message');
  }

  // Actions
  async fillEmail(email: string) {
    await this.emailInput.fill(email);
  }

  async submitOrder() {
    await this.submitButton.click();
  }

  async completeCheckout(email: string, cardNumber: string) {
    await this.fillEmail(email);
    await this.page.getByLabel('Card Number').fill(cardNumber);
    await this.submitOrder();
  }

  // Assertions
  async expectSuccessMessage() {
    await expect(this.successMessage).toBeVisible();
  }
}

// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { CheckoutPage } from '../pages/CheckoutPage';

test('user completes checkout successfully', async ({ page }) => {
  const checkoutPage = new CheckoutPage(page);
  
  await page.goto('/checkout');
  await checkoutPage.completeCheckout('user@test.com', '4242424242424242');
  await checkoutPage.expectSuccessMessage();
});
```

### 4. Setup Test Data Appropriately

**Use UI for setup when:**
- The creation/setup flow is what you're testing
- Testing multi-step user journeys
- Testing form validation or user input
- The user action is part of the business flow being tested

**Use API for setup when:**
- Testing features that need pre-existing data (view, edit, delete)
- Creating multiple items for list/search tests
- Setting up authentication state
- The creation is incidental to what you're actually testing

**Example - Testing product creation (use UI):**
```typescript
test('user can create product', async ({ page }) => {
  await page.goto('/products/new');
  await page.getByLabel('Name').fill('Test Product');
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByText('Created successfully')).toBeVisible();
});
```

**Example - Testing product deletion (use API):**
```typescript
test('user can delete product', async ({ page, request }) => {
  // API setup - not testing creation
  const product = await request.post('/api/products', {
    data: { name: 'Test Product' }
  });
  
  // Testing deletion
  await page.goto(`/products/${product.id}`);
  await page.getByRole('button', { name: 'Delete' }).click();
  await expect(page.getByText('Deleted')).toBeVisible();
});
```

**The key question: "Is this action part of what I'm verifying, or just getting the app into the right state?"**

### 5. Test Fixtures for Authentication
```typescript
// fixtures/auth.ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page, request }, use) => {
    // Login via API or UI once
    await request.post('/api/auth/login', {
      data: { email: 'test@test.com', password: 'password' }
    });
    
    await use(page);
  }
});

// In tests
test('view dashboard', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
  // Already authenticated!
});
```

## What to AVOID

### ❌ Never Do This:
```typescript
// 1. CSS Selectors
await page.locator('.btn-primary.submit').click(); // BAD
await page.locator('#email-input').fill('test'); // BAD

// 2. XPath
await page.locator('//button[@class="submit"]').click(); // BAD

// 3. Arbitrary waits
await page.waitForTimeout(3000); // BAD

// 4. Testing implementation details
await page.evaluate(() => window.__REACT_STATE__); // BAD

// 5. Chaining without awaiting
page.fill('input', 'text').click('button'); // BAD - missing awaits

// 6. Not using auto-waiting
await page.locator('button').click();
await page.waitForSelector('.success'); // BAD - unnecessary
// Playwright auto-waits in assertions!

// 7. Repeating code
test('test 1', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@test.com');
  // ... repeated in every test - use Page Object instead!
});
```

## Template for New Test Files
```typescript
import { test, expect } from '@playwright/test';
import { FeaturePage } from '../pages/FeaturePage';

test.describe('Feature Name', () => {
  let featurePage: FeaturePage;

  test.beforeEach(async ({ page }) => {
    featurePage = new FeaturePage(page);
    await page.goto('/feature-url');
  });

  test('user can [specific action]', async ({ page }) => {
    // Arrange - setup is in beforeEach or via API
    
    // Act - user interaction
    await featurePage.clickSubmitButton();
    
    // Assert - verify outcome
    await expect(featurePage.successMessage).toBeVisible();
  });

  test('displays error when [error condition]', async ({ page }) => {
    await featurePage.submitWithInvalidData();
    await expect(featurePage.errorMessage).toContainText('Invalid');
  });
});
```

## Naming Conventions
```typescript
// Page Objects: [Feature]Page.ts
// LoginPage.ts, CheckoutPage.ts, DashboardPage.ts

// Test Files: [feature].spec.ts
// login.spec.ts, checkout.spec.ts

// Test IDs: [feature]-[element]-[type]
// data-testid="checkout-submit-btn"
// data-testid="user-profile-card"
// data-testid="product-list-item"

// Test names: descriptive, user-focused
test('user can submit form with valid data', ...);
test('displays error when email is invalid', ...);
```

## Checklist for Every Test

Before submitting test code, verify:
- [ ] Uses semantic locators (getByRole, getByLabel) first
- [ ] data-testid only for complex/dynamic elements
- [ ] No CSS selectors or XPath
- [ ] No waitForTimeout
- [ ] Setup via API when possible (if not part of test)
- [ ] Page Object Model for reusable interactions
- [ ] Independent tests (can run in any order)
- [ ] Descriptive test names
- [ ] Tests user behavior, not implementation
- [ ] Proper async/await usage

## When Implementing

1. **Ask these questions first:**
   - What is the user trying to accomplish?
   - What's the happy path?
   - What common errors might occur?
   - Is the setup action part of what I'm testing?

2. **Create Page Object if reusable**
   - Multiple tests use same page
   - Complex interactions
   - Common patterns

3. **Add data-testid strategically:**
   - Dynamic content (lists, cards)
   - No semantic alternative
   - Complex nested elements

4. **Keep tests readable:**
   - Clear arrange/act/assert structure
   - Descriptive variable names
   - Comments for complex flows only

## Output Format

When implementing tests, provide:
1. **React component updates** (if data-testid needed)
2. **Page Object class** (if reusable)
3. **Test spec file** with complete test cases
4. **Brief explanation** of approach and decisions made