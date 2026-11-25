---
name: testing
description: Use this skill when writing or improving tests of any kind — unit tests, integration tests, end-to-end (E2E) tests, API tests, or test coverage analysis. Trigger on keywords: test, spec, unit test, integration test, E2E, Playwright, Jest, Vitest, pytest, mock, coverage, TDD, test suite, assertion.
---

# Testing

## Core Philosophy

AI-generated code is untrusted until it passes a human-reviewed test suite. Tests are not optional — they are the safety net that makes refactoring and agentic code generation safe. Treat test code with the same quality standards as production code.

**The Verify Output Principle:** Every piece of AI-generated code should pass through an AI-generated but human-reviewed test suite before being considered complete.

---

## Test Pyramid

```text
        /\
       /E2E\          ← Few, slow, high confidence
      /------\
     /Integr. \       ← Some, medium speed
    /------------\
   /   Unit Tests  \  ← Many, fast, isolated
  /------------------\
```

- **Unit tests** — 70% of your suite. Fast, isolated, no external dependencies.
- **Integration tests** — 20%. Test how components work together.
- **E2E tests** — 10%. Test real user flows from browser to DB.

---

## Unit Testing

### Principles
- Test **behavior**, not implementation details
- One assertion concept per test
- Use the **AAA pattern**: Arrange → Act → Assert
- Mock all external dependencies (APIs, databases, file system)
- Test edge cases: null, empty, boundary values, error paths

### Structure
```
describe('ComponentOrFunction', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = ...

      // Act
      const result = functionUnderTest(input)

      // Assert
      expect(result).toBe(expectedValue)
    })
  })
})
```

### What to Test
| Scenario | Priority |
|---|---|
| Happy path (expected behavior) | Must have |
| Edge cases (null, empty, boundary) | Must have |
| Error paths (exceptions, failures) | Must have |
| Invalid inputs | Must have |
| Performance-critical paths | Nice to have |

---

## Integration Testing

### Integration Principles
- Test the **contract** between components, not their internals
- Use a real (but isolated) database — not mocks
- Clean up test data after each test
- Test API endpoints with realistic payloads

### Database Integration Tests
```python
# Python example
def test_create_user_persists_to_db(db_session):
    # Arrange
    user_data = {"name": "James", "email": "james@test.com"}

    # Act
    user = create_user(db_session, user_data)

    # Assert
    saved = db_session.query(User).filter_by(id=user.id).first()
    assert saved.email == "james@test.com"
```

### API Integration Tests
- Test request/response contracts
- Test authentication and authorization flows
- Test error responses (400, 401, 403, 404, 500)
- Test pagination and filtering

---

## End-to-End (E2E) Testing

### Tool Recommendation
Use **Playwright** for E2E testing — it supports all major browsers, has auto-wait built in, and works well with AI agent verification.

### Selector Priority (Most to Least Robust)
1. `getByRole()` — ARIA roles (most resilient)
2. `getByText()` — visible text
3. `getByTestId()` — data-testid attributes
4. `getByLabel()` — form labels
5. CSS selectors — (avoid, brittle)

### E2E Test Structure
```typescript
test('user can complete checkout flow', async ({ page }) => {
  // Navigate
  await page.goto('/products')

  // Interact
  await page.getByRole('button', { name: 'Add to Cart' }).first().click()
  await page.getByRole('link', { name: 'Checkout' }).click()

  // Fill form
  await page.getByLabel('Email').fill('test@example.com')

  // Assert
  await expect(page.getByText('Order confirmed')).toBeVisible()
})
```

### What to Cover with E2E
- Critical user journeys (signup, login, core feature flows)
- Payment or checkout flows
- Authentication flows (login, logout, password reset)
- Error states visible to users

---

## Mocking & Test Doubles

| Type | When to Use |
|---|---|
| **Mock** | Verify a function was called with specific arguments |
| **Stub** | Replace a function with a fixed return value |
| **Spy** | Observe calls without replacing behavior |
| **Fake** | Lightweight working implementation (e.g., in-memory DB) |

### Mock External APIs
Always mock external API calls in unit/integration tests:
```typescript
jest.mock('../services/paymentService', () => ({
  chargeCard: jest.fn().mockResolvedValue({ success: true })
}))
```

---

## Test Coverage Guidelines

| Coverage Level | Meaning |
|---|---|
| < 60% | Dangerous — high risk of regressions |
| 60–80% | Acceptable for early-stage projects |
| 80–90% | Good — production ready |
| 90–95% | Excellent |
| > 95% | Diminishing returns — focus on quality not quantity |

**Coverage doesn't equal quality.** 95% coverage with weak assertions is worse than 80% coverage with strong assertions.

---

## Testing AI-Generated Code

1. **Generate tests before or alongside the code** — don't test after
2. **Review AI-generated tests critically** — they often miss edge cases
3. **Add tests for every bug found** — regression coverage
4. **Test the behavior described in the spec**, not just what the code does
5. **Mutation testing** — use tools like Stryker to verify tests actually catch bugs

---

## Framework Quick Reference

| Language | Unit | Integration | E2E |
|---|---|---|---|
| TypeScript/JS | Jest / Vitest | Supertest + Jest | Playwright |
| Python | pytest | pytest + SQLAlchemy | Playwright |
| Java | JUnit 5 | Spring Boot Test | Playwright |
