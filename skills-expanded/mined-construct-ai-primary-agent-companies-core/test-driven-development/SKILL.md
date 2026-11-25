---
memory_layer: durable_knowledge
para_section: pages/skills/test-driven-development
gigabrain_tags: testing, tdd, development, quality-assurance, red-green-refactor
openstinger_context: test-first-development, quality-driven-coding, behavior-specification
last_updated: 2026-03-30
related_docs:
  - docs/testing/0000_TESTING_FRAMEWORK.md
  - docs/testing/0000_TEST_AUTOMATION_GUIDE.md
related_skills:
  - systematic-debugging
  - verification-before-completion
  - testing-verification
frequency_percent: 85.0
success_rate_percent: 92.0
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use This Skill

**Trigger Conditions:**
- Implementing new features or functionality
- Fixing bugs or resolving issues
- Refactoring existing code
- Changing behavior of existing systems
- Adding new capabilities to applications
- When quality and reliability are critical
- Before any production code implementation
- When working on complex or critical systems

**Exceptions (require human partner approval):**
- Throwaway prototypes with no long-term use
- Generated code from automated tools
- Simple configuration file changes
- Emergency hotfixes with immediate business impact

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

Implement fresh from tests. Period.

## Step-by-Step Procedure

### Step 1: Write Failing Test (RED)
Write one minimal test that demonstrates the desired behavior.

```javascript
// Example: Test for retry operation
test('retries failed operations 3 times before succeeding', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('Operation failed');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

**Test Requirements:**
- Clear, descriptive name describing behavior
- Tests one specific behavior
- Uses real code (minimal mocks)
- Demonstrates desired API/behavior

### Step 2: Verify Test Fails (RED)
**MANDATORY:** Run the test and confirm it fails correctly.

```bash
npm test path/to/test.test.ts
```

**Verify:**
- Test fails (not due to syntax errors)
- Failure message indicates missing functionality
- Fails for expected reason (feature not implemented)

**If test passes:** You're testing existing behavior - revise test
**If test errors:** Fix test syntax, then verify it fails correctly

### Step 3: Write Minimal Code (GREEN)
Implement the simplest code possible to make the test pass.

```javascript
// Minimal implementation to pass the test
async function retryOperation(operation) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === 3) throw error;
    }
  }
}
```

**Guidelines:**
- Write only enough code to pass the test
- No additional features or improvements
- Keep implementation simple and direct
- Avoid over-engineering

### Step 4: Verify Test Passes (GREEN)
**MANDATORY:** Run tests and confirm they pass.

```bash
npm test path/to/test.test.ts
```

**Verify:**
- New test passes
- All existing tests still pass
- No console errors or warnings
- Clean test output

**If tests fail:** Fix implementation, not test

### Step 5: Refactor Code (REFACTOR)
Clean up code while keeping tests green.

```javascript
// Refactored implementation
async function retryOperation(operation, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxRetries) {
        throw new Error(`Operation failed after ${maxRetries} attempts: ${error.message}`);
      }
    }
  }
}
```

**Refactoring Allowed:**
- Improve variable names
- Extract helper functions
- Remove code duplication
- Improve readability
- Add documentation

**Refactoring NOT Allowed:**
- Change behavior
- Add new features
- Break existing functionality

### Step 6: Repeat Cycle
Write next failing test for additional functionality.

```javascript
// Next test for additional behavior
test('throws error after all retries exhausted', async () => {
  const failingOperation = () => Promise.reject(new Error('Persistent failure'));

  await expect(retryOperation(failingOperation)).rejects.toThrow('Operation failed after 3 attempts');
});
```

**Continue cycle:**
- RED: Write failing test
- GREEN: Make test pass
- REFACTOR: Clean up code
- Repeat for next feature

### Step 7: Handle Edge Cases
Add tests for error conditions and edge cases.

```javascript
// Edge case tests
test('handles synchronous operations', () => {
  const result = retryOperation(() => 'immediate success');
  expect(result).toBe('immediate success');
});

test('validates retry count parameter', () => {
  expect(() => retryOperation(() => 'test', 0)).toThrow('Invalid retry count');
});
```

### Step 8: Integration Testing
Ensure component works with other parts of the system.

```javascript
// Integration test
test('retry operation integrates with API client', async () => {
  const mockApiClient = { call: jest.fn().mockRejectedValueOnce(new Error('Network error')).mockResolvedValue('success') };
  const result = await retryOperation(() => mockApiClient.call());
  expect(result).toBe('success');
  expect(mockApiClient.call).toHaveBeenCalledTimes(2);
});
```

### Step 9: Documentation and Examples
Add clear examples and documentation.

```javascript
/**
 * Retries an asynchronous operation with exponential backoff
 * @param {Function} operation - Async function to retry
 * @param {number} maxRetries - Maximum retry attempts (default: 3)
 * @returns {Promise} Result of successful operation
 * @throws {Error} Last error if all retries fail
 */
async function retryOperation(operation, maxRetries = 3) {
  // Implementation...
}
```

### Step 10: Final Verification
Complete verification checklist before marking complete.

```javascript
// Verification checklist
const verificationComplete = {
  allTestsPass: true,
  codeCoverageMet: true,
  edgeCasesCovered: true,
  integrationTestsPass: true,
  documentationComplete: true,
  noTechnicalDebt: true
};
```

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (X more hours, high confidence)
- Keep it and add tests after (30 min, low confidence, likely bugs)

The "waste" is keeping code you can't trust. Working code without real tests is technical debt.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:
- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

**"Tests after achieve the same goals - it's spirit not ritual"**

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.

Tests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).

30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## Testing Anti-Patterns

When adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:
- Testing mock behavior instead of real behavior
- Adding test-only methods to production classes
- Mocking without understanding dependencies

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.

## Cross-References

### Related Procedures
- [Testing Framework Guide](docs/testing/0000_TESTING_FRAMEWORK.md) - Complete testing setup and frameworks
- [Test Automation Guide](docs/testing/0000_TEST_AUTOMATION_GUIDE.md) - CI/CD integration and automation

### Related Skills
- `systematic-debugging` - Debugging test failures and issues
- `verification-before-completion` - Final quality validation
- `testing-verification` - Comprehensive testing strategies

### Related Agents
- `QualityForge_AI_Team` - Test creation and validation assistance
- `DevForge_AI_Team` - Implementation guidance with TDD
