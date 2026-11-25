---
name: test-driven-development
description: Test-driven development methodology - RED-GREEN-REFACTOR cycle. Use when implementing any feature or bugfix, before writing implementation code.
category: engineering
exposure: standard
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask user):**
- Throwaway prototypes
- Generated code
- Configuration files

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## Red-Green-Refactor

### RED - Write Failing Test

Write one minimal test showing what should happen.

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

Clear name, tests real behavior, one thing.

### Verify RED

Run the test. Confirm it fails for the RIGHT reason.

```
Run: bun test -t "retries failed"
Expected: FAIL - "retryOperation is not defined"
Actual: FAIL - "retryOperation is not defined" ✅
```

Wrong failure? Fix the test, not the code.

### GREEN - Minimal Implementation

Write the MINIMUM code to make the test pass.

```typescript
async function retryOperation(operation: () => Promise<string>): Promise<string> {
  for (let i = 0; i < 3; i++) {
    try {
      return await operation();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```

Don't add extra features. Don't optimize. Just pass.

### Verify GREEN

Run the test. Confirm it passes.

```
Run: bun test -t "retries failed"
Expected: PASS
Actual: PASS ✅
```

### REFACTOR - Clean Up

Improve code quality while keeping tests green.

- Extract constants
- Improve naming
- Remove duplication
- Add types

**After each refactor step:** Run tests. Stay green.

## Anti-Patterns

| Anti-Pattern | Reality |
|--------------|---------|
| "I'll write tests after" | You won't. Or they'll test the wrong thing. |
| "This is too simple to test" | Simple bugs have simple root causes. Test it. |
| "I know it works" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "The test is obvious" | If it's obvious, write it. Takes 30 seconds. |

## Test Design Principles

1. **One behavior per test** - Test fails = one thing broke
2. **Clear test names** - `test('throws when input is empty')` not `test('error')`
3. **Arrange-Act-Assert** - Setup, execute, verify
4. **No test interdependence** - Each test runs in isolation
5. **Test behavior, not implementation** - Don't test private methods

## Quick Reference

```
RED:    Write failing test → Verify fails correctly
GREEN:  Write minimal code → Verify passes
REFACTOR: Clean up → Verify still passes
```

## Integration with Our Workflow

- **Before implementation:** Run this skill
- **During implementation:** Follow RED-GREEN-REFACTOR
- **After implementation:** Use `verification-before-completion` skill
- **Code review:** Use `receiving-code-review` skill
