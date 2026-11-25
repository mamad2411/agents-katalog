---
name: testing-patterns
description: Testing methodology — what to test, how to test it, test structure, and common patterns.
---

# Testing Patterns

## What to Test

### Always Test
- Happy path (the main use case)
- Edge cases (null, empty, 0, negative, max values)
- Error paths (what happens when things fail)
- Integration points (API calls, database, file I/O)

### Don't Bother Testing
- Simple getters/setters
- Framework code you don't own
- Implementation details (test behavior, not implementation)
- Trivial utilities with no logic

## Test Structure

```
describe('UserService', () => {
  describe('createUser', () => {
    it('creates a user with valid data', () => { ... })
    it('rejects duplicate emails', () => { ... })
    it('hashes the password', () => { ... })
    it('returns user without password field', () => { ... })
  })
})
```

Pattern: `describe` the unit, `it` describes the behavior in plain English.

## Test Pyramid

```
        /  E2E  \        ← Few, slow, high confidence
       / Integration \   ← Some, medium speed
      /   Unit Tests   \  ← Many, fast, focused
```

- Unit tests: 70% — test individual functions
- Integration tests: 25% — test modules working together
- E2E tests: 5% — test the full user journey

## Common Patterns

### Arrange-Act-Assert
```
// Arrange: set up the test data
const user = { name: 'Test', email: 'test@example.com' }

// Act: call the function
const result = createUser(user)

// Assert: check the result
expect(result).toHaveProperty('id')
expect(result.email).toBe('test@example.com')
```

### Mock External Dependencies
```
jest.mock('./database', () => ({
  query: jest.fn().mockResolvedValue([{ id: 1 }])
}))
```

### Test Error Cases
```
it('throws on invalid input', () => {
  expect(() => parseConfig(null)).toThrow('Config is required')
})
```

## Coverage

- Aim for 80%+ line coverage
- But coverage ≠ quality — 100% coverage with no edge case tests is worthless
- Focus on covering the paths that matter most
