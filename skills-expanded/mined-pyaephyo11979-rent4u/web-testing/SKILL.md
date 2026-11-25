# Web Testing Skill

End-to-end and integration testing guidelines for the full Rent4U stack.

## Stack

- **E2E:** Playwright (recommended) or Cypress
- **API integration:** Supertest against running backend
- **Frontend unit:** Vitest + React Testing Library

## Directory Structure

```
tests/
├── e2e/
│   ├── auth.spec.ts            # Login, register, logout flows
│   ├── search.spec.ts          # Search and filter flows
│   ├── booking.spec.ts         # Booking request flow
│   └── host-dashboard.spec.ts  # Host listing management
├── api/
│   ├── houses.test.js          # House CRUD API tests
│   └── bookings.test.js        # Booking API tests
└── fixtures/
    ├── users.json              # Test user data
    └── houses.json             # Test house data
```

## E2E Test Conventions

### Page Object Pattern
```ts
// tests/e2e/pages/LoginPage.ts
import { Page, expect } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    await this.page.click('[data-testid="login-button"]');
  }

  async expectError(message: string) {
    await expect(this.page.locator('[data-testid="error-message"]')).toContainText(message);
  }
}
```

### Test File Pattern
```ts
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('Authentication', () => {
  test('should login with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@test.com', 'password123');
    await expect(page).toHaveURL('/dashboard');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('wrong@test.com', 'wrong');
    await loginPage.expectError('Invalid email or password');
  });
});
```

### Data Test IDs
Every interactive element needs a `data-testid`:
```tsx
// Good
<button data-testid="login-button">Login</button>
<input data-testid="email-input" />

// Bad — fragile selectors
<button className="btn-primary">Login</button>
```

## API Integration Tests

### Testing Against Running Server
```js
const request = require('supertest');

const BASE_URL = 'http://localhost:3000';

describe('Houses API', () => {
  let authToken;

  beforeAll(async () => {
    // Login to get token
    const res = await request(BASE_URL)
      .post('/users/login')
      .send({ email: 'host@test.com', password: 'password123' });
    authToken = res.body.token;
  });

  it('should list houses', async () => {
    const res = await request(BASE_URL)
      .get('/houses')
      .expect(200);
    expect(Array.isArray(res.body.data)).toBe(true);
  });

  it('should require auth for creating houses', async () => {
    await request(BASE_URL)
      .post('/houses')
      .send({ name: 'Test House' })
      .expect(401);
  });
});
```

## What to Test (E2E)

### Critical User Flows
| Flow | Priority |
|------|----------|
| Register → Login → Browse houses → View details | P0 |
| Search by city → Filter by price → View results | P0 |
| Login as Host → Create listing → Upload photos | P0 |
| Guest → Select dates → Submit booking request | P0 |
| Host → View bookings → Accept/Decline | P1 |
| Guest → View booking history | P1 |
| Edit profile → Change profile picture | P2 |

### Cross-cutting Concerns
| Concern | Test |
|---------|------|
| Responsive | Test at 375px, 768px, 1280px viewports |
| Loading states | Skeleton/spinner shown during API calls |
| Error states | Network failure → user-friendly message |
| Empty states | No results → helpful message, not blank |

## Running Tests

```bash
# E2E (Playwright)
npx playwright test
npx playwright test --ui          # Visual mode
npx playwright test --headed      # See the browser

# API integration
bun test tests/api/

# Frontend unit
cd frontend && bun test
```

## Quality Checklist

- [ ] Every user flow has at least one happy-path E2E test
- [ ] Error states are tested (network failure, validation errors)
- [ ] `data-testid` on all interactive elements
- [ ] No tests depend on test execution order
- [ ] Tests clean up created data (or use isolated test DB)
- [ ] Responsive layouts tested at 3 breakpoints
