---
description: Run Unit, Integration, and API Contract Testing Standards Check
globs:
  ['**/*.test.ts', '**/*.spec.ts', '**/__tests__/**/*.ts', 'vitest.config.ts', 'jest.config.js']
---

# Testing: Automated Testing Standards

<audit_rules>

- You MUST enforce a minimum test coverage threshold (e.g., ≥70%) for business logic (`lib/`, `utils/`, `services/`).
- You MUST ensure all API routes have at least one response contract test verifying the response shape matches the expected JSON (Zod schema).
- You MUST verify that external APIs (e.g., Stripe, SendGrid) are mocked in tests to prevent hitting real services.
- You MUST verify that database integration tests use an isolated test database or in-memory container, NOT the development or production database.
- You MUST ensure test names describe behavior, not implementation (e.g., "should decline card with insufficient funds" instead of "test_payment_fail").
- You MUST flag skipped tests (`it.skip`) in critical files (auth, payments, billing).
  </audit_rules>

<example_good>

```typescript
import { describe, it, expect, vi } from 'vitest'
import { processPayment } from './payment.service'
import { stripe } from '@/lib/stripe'

// Mock external service
vi.mock('@/lib/stripe', () => ({
  stripe: { charges: { create: vi.fn() } },
}))

describe('processPayment', () => {
  it('should decline transaction when funds are insufficient', async () => {
    vi.mocked(stripe.charges.create).mockRejectedValueOnce(new Error('insufficient_funds'))

    const result = await processPayment({ amount: 100, source: 'tok_visa' })

    expect(result.status).toBe('declined')
    expect(result.error).toBe('insufficient_funds')
  })
})
```

</example_good>

<example_bad>

```typescript
// BAD: Vague test name, hitting real database/API
it('tests the payment function', async () => {
  const result = await processPayment({ amount: 100, source: 'tok_visa' })
  expect(result).toBeTruthy()
})
```

</example_bad>
