---
name: test-driven-development
description: Enforces the Red-Green-Refactor cycle with strict test pyramid discipline (80% unit, 15% integration, 5% e2e). Mandates DAMP over DRY in test code, the Beyoncé Rule (if you liked it then you should've put a test on it), intentional mocking patterns, and the Prove-It pattern for bug fixes.
---

# Test-Driven Development

## Overview

Test-driven development is not "write tests first." It's a **design discipline** that produces better code, not just verified code. The three laws:

1. **Red:** Write a failing test before any production code. One test at a time.
2. **Green:** Write the minimum production code to make that test pass. Nothing more.
3. **Refactor:** Clean up both test and production code, keeping all tests green.

The result: every line of code is written because a test demanded it. No dead code. No untested paths. No "I'll test it later" (you won't).

But TDD without structure is chaos. This skill defines the **exact protocols**: test sizing (80/15/5 pyramid), naming (DAMP not DRY), coverage mandates (the Beyoncé Rule), mocking contracts (mocks vs fakes vs stubs), and the Prove-It pattern for regression prevention.

## When to Use

| Trigger | Description |
|---------|-------------|
| Any new logic | Functions, components, services, utilities — anything with branching |
| Bug fix | Write a test that reproduces the bug FIRST, then fix it |
| Refactoring | Characterization tests before touching untested code |
| API design | TDD drives better interfaces — test-consumable code is better code |
| Complex algorithms | State machines, calculations, data transformations |
| Integration points | Database queries, API calls, file I/O — test with real or fake |

**Do NOT use** when: exploring a problem space (throwaway spike), the test costs more to maintain than the code it tests (stable code, no churn), or trivial getters/setters with zero logic.

## Test Pyramid (80/15/5)

### Unit Tests — 80% of test suite

**Characteristics:**
- Test a single unit in isolation (function, class, component)
- No network calls, no database, no file system
- Mocks only for external boundaries (IO, 3rd party SDK)
- Milliseconds to run
- Thousands in the suite

**What to test:**
- Business logic
- Validation rules
- Edge cases (null, empty, overflow, boundary)
- Happy path
- Error paths

**What NOT to test:**
- Framework internals (React renders, Express routing)
- Constants
- Third-party library behavior
- Boilerplate code without logic

```typescript
// GOOD unit test — tests logic, not framework
describe('calculateDiscount', () => {
  it('applies 10% discount for orders over $100', () => {
    expect(calculateDiscount({ total: 150, tier: 'standard' })).toBe(135);
  });

  it('applies 20% discount for premium members', () => {
    expect(calculateDiscount({ total: 200, tier: 'premium' })).toBe(160);
  });

  it('returns 0 for empty cart', () => {
    expect(calculateDiscount({ total: 0, tier: 'standard' })).toBe(0);
  });
});
```

### Integration Tests — 15% of test suite

**Characteristics:**
- Test interactions between units (service + database, controller + service)
- Real database (test container or in-memory)
- Real HTTP server (Supertest, Playwright for API)
- Seconds to run
- Hundreds in the suite

**What to test:**
- API endpoints (request → response)
- Database queries (insert → select)
- Service layer composing multiple units
- Auth middleware

```typescript
describe('POST /users', () => {
  it('creates user and returns 201', async () => {
    const res = await request(app)
      .post('/users')
      .send({ email: 'test@example.com', name: 'Test' });

    expect(res.status).toBe(201);
    expect(res.body.email).toBe('test@example.com');

    // Verify persistence
    const user = await db.query('SELECT * FROM users WHERE email = $1', ['test@example.com']);
    expect(user.rows[0].name).toBe('Test');
  });
});
```

### End-to-End Tests — 5% of test suite

**Characteristics:**
- Full system — browser or service, real dependencies
- Tests user journeys
- Minutes to run
- Dozens in the suite

**What to test:**
- Critical user paths (signup → browse → purchase)
- Cross-system flows (web app → API → notification)
- Visual regression (screenshot comparison)

```typescript
test('user can complete purchase', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="product-1"]');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('[name="email"]', 'test@example.com');
  await page.click('[data-testid="submit-order"]');
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
});
```

## Red-Green-Refactor Protocol

### Step 1: RED — Write a Failing Test

- Write exactly ONE test
- Run it — it MUST fail (if it passes, you're testing the wrong thing)
- The failure should be clear: "Expected 135 but got undefined"
- Resist the urge to fix the code yet

**Bad red:** Test fails because of a syntax error in the test itself.
**Good red:** Test correctly describes behavior, and the code doesn't implement it yet.

### Step 2: GREEN — Make It Pass

- Write the **minimum** production code to pass the test
- Copy-paste is allowed. Hardcoding is allowed. Ugly is allowed.
- Do not refactor. Do not optimize. Do not generalize.
- If the test passes in less than 2 minutes, you're doing it right.

**Quiz:** After writing a "Green" step, your code is:
- A) Elegant and well-structured — no, that's Step 3
- B) The simplest thing that works — yes, exactly
- C) Production-ready — not yet

### Step 3: REFACTOR — Clean Up

- Now that tests are green, improve the code
- Extract duplication, rename variables, simplify logic
- Run tests after every change — if they break, you changed behavior
- Refactor tests too (they must stay clean)

**Refactor checklist:**
- [ ] No magic numbers or strings
- [ ] No dead code
- [ ] No commented-out code
- [ ] Functions are small (< 20 lines)
- [ ] Names communicate intent
- [ ] Tests still pass

## DAMP over DRY in Tests

**DAMP:** Descriptive And Meaningful Phrases.
**DRY:** Don't Repeat Yourself.

In production code, DRY wins. In test code, DAMP wins.

### Why

Test code must communicate intent. A dry, abstracted test is hard to read and harder to debug. A damp, slightly repetitive test tells a clear story.

```typescript
// ❌ DRY — hard to follow, what's different?
test.each([
  { email: '', pass: '',           expected: 'Email required' },
  { email: 'bad', pass: 'good1',   expected: 'Invalid email' },
  { email: 'a@b.com', pass: '',    expected: 'Password required' },
  { email: 'a@b.com', pass: '12',  expected: 'Password too short' },
])('validates: $email, $pass', ({ email, pass, expected }) => {
  expect(validateLogin(email, pass)).toBe(expected);
});

// ✅ DAMP — clear story, easy to read failure messages
it('requires email', () => {
  expect(validateLogin('', 'password1')).toBe('Email required');
});

it('validates email format', () => {
  expect(validateLogin('bad', 'password1')).toBe('Invalid email');
});

it('requires password', () => {
  expect(validateLogin('a@b.com', '')).toBe('Password required');
});

it('requires password at least 8 characters', () => {
  expect(validateLogin('a@b.com', '12')).toBe('Password too short');
});
```

### DAMP Rules

1. One assertion per test (or related group of assertions)
2. Test name is a sentence: "it returns 404 for nonexistent user"
3. Arrange-Act-Assert separated by blank lines
4. Test data is inline, not in a factory 3 files away
5. Don't share state between tests (no `let` variables reused)

## The Beyoncé Rule

> "If you liked it, then you should've put a test on it."

### Interpretation

Every time you find a bug, **write a test that reproduces it before fixing it.** That test becomes your regression guard. The bug will never come back without you knowing.

### Why

- Fixing a bug without a test means it will happen again
- The test documents the edge case
- The test proves the fix works
- Future refactoring won't silently reintroduce the bug

### Process

```typescript
// Step 1: Write a test that reproduces the bug (it fails)
describe('Bug #427 — negative price allowed', () => {
  it('rejects product with negative price', () => {
    expect(() => new Product({ name: 'Test', price: -5 }))
      .toThrow('Price must be positive');
  });
});

// Step 2: Fix the production code
class Product {
  constructor({ name, price }) {
    if (price < 0) throw new Error('Price must be positive');
    // ...
  }
}

// Step 3: Test passes. Bug is fixed. Never coming back.
```

### Beyoncé Rule Checklist

- [ ] Found a bug? Wrote a failing test first?
- [ ] Fixed the bug?
- [ ] Test passes?
- [ ] Did you check if similar bugs exist nearby? (e.g., negative quantity, negative discount)

## Mocking Patterns

### Mocks vs Fakes vs Stubs

| Type | What It Is | When to Use |
|------|-----------|-------------|
| **Mock** | Expects specific calls, asserts behavior | Testing that a function was called with specific args |
| **Stub** | Returns pre-configured values | Testing a code path that depends on external data |
| **Fake** | Lightweight implementation (in-memory DB) | Testing integration without real infrastructure |

### Mocking Rules

1. **Mock the boundary, not the implementation.** Mock the database interface, not the query builder.
2. **Never mock what you don't own.** Don't mock `fetch`, `fs`, or `Date.now` — wrap them in your own interface.
3. **Mock at the edge of your system.** If you mock internal calls, your test is coupled to implementation.
4. **Prefer fakes over mocks.** An in-memory database is more valuable than a mock of the database interface.

```typescript
// ❌ Bad — mocking an internal detail
jest.mock('../../services/email');
// Your test must know about internal email service

// ✅ Good — mocking at the system boundary
const emailSender = { send: jest.fn() };
// Inject emailSender. Test doesn't care what happens inside.
```

### The Mocking Hierarchy

```
Prefer this:      Fake (in-memory DB, test HTTP server)
                  ↓
                  Stub (pre-configured returns)
                  ↓
Avoid unless      Mock (behavior verification)
necessary:
                  ↓
Never do this:    Mocking internals, mocking what you don't own
```

## The Prove-It Pattern

For bug fixes and regression prevention.

```typescript
// Step 1: Prove the bug exists
describe('Bug report #512: Discount not applied to bundled items', () => {
  it('reproduces bug: bundled item shows full price', () => {
    const bundle = new Bundle([item1, item2]);
    // This assertion FAILS — proving the bug
    expect(bundle.totalWithDiscount()).toBe(85); // should be 85, is 100
  });
});

// Step 2: Fix the code
// Step 3: Test passes — bug is fixed
// Step 4: Add another test to prove the fix works across scenarios
it('applies bundle discount correctly for 3 items', () => {
  const bundle = new Bundle([item1, item2, item3]);
  expect(bundle.totalWithDiscount()).toBe(120);
});

it('does not apply bundle discount to single items', () => {
  const single = new Bundle([item1]);
  expect(single.totalWithDiscount()).toBe(50); // no discount for 1 item
});
```

### Prove-It Checklist

- [ ] Test reproduces the bug exactly (same inputs → same wrong output)
- [ ] Test name references the bug report (traceability)
- [ ] After fix, test passes
- [ ] At least one more scenario tested (the fix didn't break other cases)

## Anti-Rationalization Table

| Temptation | Why It Happens | Why It's Dangerous | What To Do Instead |
|------------|----------------|--------------------|--------------------|
| "I'll write tests after the code is done" | Speed illusion, pressure | Tests never written, or written to pass not to catch bugs | Write the test first. It's faster. |
| "The test passed on the first run" | You tested the wrong thing | False confidence | Make sure the test fails when run against the old code |
| "I don't need a test for this edge case" | Laziness, low probability | The edge case happens in production at 3 AM | Write the test. It takes 30 seconds. |
| "I'll use parameterized tests" | DAMP/DRY confusion | Tests become unreadable matrices | Write individual tests. Duplication is OK in tests. |
| "I can't test this because of X" | Genuine difficulty | Untestable code is badly designed code | Refactor to make it testable, then test it |
| "This test is just testing that the framework works" | Wrong test level | Brittle tests that fail on framework upgrades | Test at the right level — integration for framework behavior |
| "I mocked everything so this is a unit test" | Mocking abuse | Tests pass but system breaks in production | Use fakes for real behavior, mocks only for verification |
| "100% coverage means no bugs" | Metric fixation | High coverage of wrong things | Coverage tells you what wasn't tested, not what was tested well |

## Red Flags

1. Tests don't follow the pyramid — more integration than unit, or missing unit tests entirely
2. Tests share mutable state — `let` variables shared across tests (test pollution)
3. Tests have conditional logic — `if` statements in tests (you're testing two things)
4. Tests are order-dependent — Test B only passes if Test A ran first
5. Tests mock internals — calling `jest.mock('../../internal/service')` instead of injecting
6. Tests have > 50 lines of setup — the code under test is too coupled
7. Tests use `sleep` or `setTimeout` — flaky, slow, unreliable
8. Bug fixes have no regression test — the bug will come back
9. Coverage is reported but tests are low quality — metric gamed, not achieved
10. Test names are generic — "test 1", "should work", "unit test" (no intent communicated)
11. Tests are slower than 1 second per unit test — they're not unit tests
12. No test for the "impossible" case — the case the developer says can't happen

## Verification

- [ ] **Test pyramid respected:** 80% unit, 15% integration, 5% e2e
- [ ] **Red-Green-Refactor** cycle followed for every change
- [ ] **Tests fail first** (Red) before code is written
- [ ] **Minimum code** written to pass the test (Green)
- [ ] **Code refactored** after tests pass (Refactor)
- [ ] **Tests are DAMP** — descriptive names, one assertion per test, inline data
- [ ] **Beyoncé Rule** applied — every bug fix has a regression test
- [ ] **Mocking rules** followed — mock at boundary, prefer fakes, don't mock what you don't own
- [ ] **Prove-It pattern** used for bug reproduction and fix verification
- [ ] **No shared state** between tests
- [ ] **No conditional logic** in tests
- [ ] **No flaky tests** — no sleep, no timing dependencies, no network calls in unit tests
- [ ] **Test names are sentences** — readable as documentation

## Red-Green-Refactor Quick Reference

```
RED    → 1. Write one failing test
       → 2. Run it — it must fail
       → 3. If it passes, test is wrong

GREEN  → 4. Write minimum code to pass
       → 5. Run test — it passes
       → 6. Duplication allowed, ugly allowed

REFACTOR → 7. Clean production code
         → 8. Clean test code
         → 9. Run tests — still green
         → 10. Commit

Repeat for next test.
```
