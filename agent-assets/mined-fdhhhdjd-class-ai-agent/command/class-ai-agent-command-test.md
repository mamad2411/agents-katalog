---
name: test
description: Write tests using TDD patterns — tests are proof of correctness
---

# /test — Test-Driven Development

> "Tests are proof, not afterthought."

## Purpose

Write tests that prove code works correctly. Use the RED-GREEN-REFACTOR cycle for new features and the Prove-It pattern for bug fixes.

## For New Features: RED-GREEN-REFACTOR

### RED: Write Failing Test First

```javascript
describe('UserService.findById', () => {
  it('should return user when found', async () => {
    // Arrange
    const userId = 'user-123';
    
    // Act
    const user = await userService.findById(userId);
    
    // Assert
    expect(user).toBeDefined();
    expect(user.id).toBe(userId);
  });

  it('should throw NotFoundError when user does not exist', async () => {
    await expect(userService.findById('non-existent'))
      .rejects.toThrow(NotFoundError);
  });
});
```

Run tests — **they should fail** (proves nothing is implemented yet).

### GREEN: Write Minimal Code to Pass

```javascript
async findById(id: string): Promise<User> {
  const user = await this.db.user.findUnique({ where: { id } });
  if (!user) throw new NotFoundError('User not found');
  return user;
}
```

Run tests — **they should pass**.

### REFACTOR: Improve While Green

Clean up code while keeping tests passing:
- Better naming
- Extract helpers
- Remove duplication

---

## For Bug Fixes: Prove-It Pattern

### Step 1: Write Test That Reproduces the Bug

```javascript
it('should not duplicate items when adding to cart twice', async () => {
  // This test should FAIL with the current buggy code
  await cart.addItem('product-1', 1);
  await cart.addItem('product-1', 1);
  
  expect(cart.items).toHaveLength(1);
  expect(cart.items[0].quantity).toBe(2);
});
```

### Step 2: Verify Test Fails

Run the test — confirm it **fails** (proving the bug exists).

### Step 3: Fix the Bug

```javascript
async addItem(productId: string, quantity: number) {
  const existing = this.items.find(i => i.productId === productId);
  if (existing) {
    existing.quantity += quantity;  // Fix: increment instead of duplicate
  } else {
    this.items.push({ productId, quantity });
  }
}
```

### Step 4: Verify Test Passes

Run the test — confirm it **passes** (proving the fix works).

### Step 5: Run Full Suite

```bash
npm test  # Ensure no regressions
```

---

## Test Pyramid

| Level | Percentage | Speed | Scope |
|-------|------------|-------|-------|
| **Unit** | 80% | ms | Single function, no I/O |
| **Integration** | 15% | seconds | API + DB, component interactions |
| **E2E** | 5% | minutes | Full user flows |

---

## Writing Good Tests

### Arrange-Act-Assert Pattern

```javascript
it('should calculate total with discount', () => {
  // Arrange — setup
  const cart = new Cart();
  cart.addItem({ price: 100 });
  cart.applyDiscount(10);

  // Act — execute
  const total = cart.calculateTotal();

  // Assert — verify
  expect(total).toBe(90);
});
```

### DAMP Over DRY

Tests should be **Descriptive And Meaningful Phrases**. Each test reads independently:

```javascript
// ✅ DAMP — clear and independent
it('should reject password shorter than 8 characters', () => {
  const result = validatePassword('short');
  expect(result.valid).toBe(false);
  expect(result.error).toBe('Password must be at least 8 characters');
});

// ❌ Too DRY — requires reading shared setup
it('should reject short password', () => {
  expect(validate(shortPassword)).toBe(false);
});
```

### Descriptive Test Names

```javascript
// ✅ Good — describes behavior
'should return 404 when user is not found'
'should increment quantity when adding existing product'
'should send welcome email after registration'

// ❌ Bad — vague
'works correctly'
'handles error'
'test user'
```

### One Behavior Per Test

```javascript
// ✅ Good — focused
it('should validate email format', () => { ... });
it('should require email field', () => { ... });

// ❌ Bad — testing multiple things
it('should validate email', () => {
  expect(validate('')).toBe(false);      // required
  expect(validate('bad')).toBe(false);   // format
  expect(validate('a@b.c')).toBe(true);  // valid
});
```

---

## Test Doubles Preference

```
1. Real implementations (best)
2. In-memory fakes (test DB, fake filesystem)
3. Stubs (canned responses)
4. Mocks (verify interactions — use sparingly)
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Testing internals | Breaks on refactor | Test inputs/outputs only |
| Flaky tests | Erodes trust | Use deterministic data, isolate state |
| Over-mocking | False confidence | Prefer real implementations |
| Snapshot abuse | Large diffs ignored | Use for rare cases only |
| Shared state | Tests affect each other | Reset state in beforeEach |

---

## Verification Checklist

- [ ] All new behaviors have tests
- [ ] Bug fixes have reproduction tests
- [ ] Test names describe behavior
- [ ] No skipped or disabled tests
- [ ] Coverage maintained or improved
- [ ] Full test suite passes
