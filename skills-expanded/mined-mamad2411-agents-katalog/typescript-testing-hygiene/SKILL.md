---
name: typescript-testing-hygiene
description: |
  TypeScript strict-mode standards, testing pyramid, and code hygiene rules.
  Apply for any TypeScript or JavaScript file — frontend or backend. Enforces strict config,
  no-any policy, interface/type/enum conventions, unit/integration/E2E coverage,
  function size limits, naming, and TODO format. Frontend tests default to Vitest.
---

# TypeScript, Testing & Code Hygiene

## TypeScript Configuration (Mandatory)
```json
// tsconfig.json — strict mode, no exceptions
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": false
  }
}
```

## Type System Rules

### No `any` — Use `unknown` + Narrowing
```typescript
// ❌ NEVER
function process(data: any) { return data.value; }

// ✅ CORRECT
function process(data: unknown): string {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return String((data as { value: unknown }).value);
  }
  throw new Error('Invalid data shape');
}
```

### Interface vs Type
```typescript
// Interface → object shapes, class contracts, extendable APIs
interface UserProfile {
  id: string;
  email: string;
  role: UserRole;
  createdAt: Date;
}

// Type → unions, intersections, primitives, utility types
type ApiResponse<T> = { success: true; data: T } | { success: false; error: ApiError };
type UserId = string;
type LoadingState = 'idle' | 'loading' | 'success' | 'error';
```

### Enums and `as const`
```typescript
// Use enum for database-stored values or when you need reverse mapping
enum OrderStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled',
}

// Use `as const` for config objects, route maps, and small fixed sets
const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile/:id',
} as const;

type Route = (typeof ROUTES)[keyof typeof ROUTES];
```

## Testing Pyramid

### Unit Tests — Business Logic (Vitest for frontend)
```typescript
// vitest
import { describe, it, expect, vi } from 'vitest';

describe('calculateOrderTotal', () => {
  it('should apply discount when order exceeds threshold', () => {
    const items = [{ price: 100, qty: 3 }]; // 300 total
    const result = calculateOrderTotal(items, { discountThreshold: 250, discountRate: 0.1 });
    expect(result.discount).toBe(30);
    expect(result.total).toBe(270);
  });

  it('should not apply discount below threshold', () => {
    const items = [{ price: 50, qty: 2 }]; // 100 total
    const result = calculateOrderTotal(items, { discountThreshold: 250, discountRate: 0.1 });
    expect(result.discount).toBe(0);
    expect(result.total).toBe(100);
  });

  it('should throw when items array is empty', () => {
    expect(() => calculateOrderTotal([], {})).toThrow('Items cannot be empty');
  });
});
```

### Integration Tests — API Endpoints
```typescript
// Test the full request-response cycle including middleware
describe('POST /api/v1/orders', () => {
  it('should create order and return 201 when payload is valid', async () => {
    const token = await getTestAuthToken();
    const res = await request(app)
      .post('/api/v1/orders')
      .set('Authorization', `Bearer ${token}`)
      .send({ items: [{ productId: 'prod_1', quantity: 2 }] });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.id).toBeDefined();
  });
});
```

### E2E Tests — Critical User Flows (Playwright)
```typescript
// Test the flows that MUST work in production
const CRITICAL_FLOWS = [
  'User registration → email verification → login',
  'Product search → add to cart → checkout → payment',
  'Password reset flow',
  'Admin: create product → publish → verify on storefront',
];

test('user can complete purchase flow', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="product-card"]:first-child');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout-btn"]');
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
});
```

### Coverage Targets
| Layer | Minimum Coverage |
|-------|----------------|
| Business logic (services) | 80% |
| API controllers | 70% |
| Utility functions | 90% |
| UI components | 60% |

## Code Hygiene Rules

### Function Size
- Maximum **30 lines** per function
- If longer: extract helper functions with descriptive names
- Single responsibility: one function does one thing

### File Size
- Maximum **300 lines** per file
- If larger: split into logical modules
- Each file: one primary export + related helpers

### Naming Conventions
```typescript
// Variables and functions: camelCase, descriptive
const userActiveOrders = await fetchUserOrders(userId, { status: 'active' });

// Constants: SCREAMING_SNAKE_CASE
const MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024;

// Types/Interfaces: PascalCase
interface PaymentGatewayConfig { ... }

// Enums: PascalCase members
enum PaymentMethod { CreditCard, BankTransfer, Crypto }

// Boolean variables: is/has/can/should prefix
const isAuthenticated = checkAuth(token);
const hasPermission = await checkPermission(userId, resource);
const canDelete = user.role === 'admin';
```

### Comment Philosophy
```typescript
// ✅ WHY — explain the reason, not the what
// Using exponential backoff because Stripe recommends it for 429 responses
const delay = Math.min(1000 * 2 ** attempt, 30000);

// ❌ WHAT — this just repeats the code
// Multiply delay by 2 to the power of attempt
const delay = Math.min(1000 * 2 ** attempt, 30000);
```

### TODO Format (Strict)
```typescript
// TODO(hayotbek): 2024-12-01 - Replace with proper queue when Redis is set up - TICKET-142
// FIXME(hayotbek): 2024-12-05 - Race condition when two users edit simultaneously - TICKET-187
// HACK(hayotbek): 2024-12-10 - Temporary workaround for Payme API bug - remove after v2.1 - TICKET-203
```
