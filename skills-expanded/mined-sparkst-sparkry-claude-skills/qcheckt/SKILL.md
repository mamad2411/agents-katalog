---
name: QCHECKT
version: 1.0.0
description: Focused review of tests only. Checks test coverage, REQ-ID mapping, edge cases, test quality, and test independence.
trigger: QCHECKT
dependencies:
  agents:
    - pe-reviewer
    - test-writer
tools:
  - coverage-analyzer.py
  - req-id-extractor.py
claude_tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# QCHECKT - Test-Focused Review

## Purpose

Specialized review focused exclusively on test quality. Ensures tests properly cover requirements, are maintainable, independent, and follow TDD best practices.

## Workflow

### 1. Analyze Test Coverage
**Tool: coverage-analyzer.py**
- Run test suite with coverage
- Parse coverage reports
- Identify uncovered lines/branches
- Calculate coverage per REQ-ID

### 2. Validate REQ-ID Mapping
**Tool: req-id-extractor.py**
**Agent: pe-reviewer**
- Extract REQ-IDs from requirements.lock.md
- Find corresponding tests
- Identify missing REQ coverage
- Verify acceptance criteria mapped to assertions

### 3. Review Test Quality
**Agent: test-writer**
- **Independence:** Tests don't depend on execution order
- **Clarity:** Descriptive test names with REQ-IDs
- **Structure:** Arrange-Act-Assert pattern
- **Determinism:** No flaky tests
- **Mocking:** Appropriate use of mocks/stubs
- **Edge cases:** Comprehensive coverage

### 4. Check Test Patterns
**Agent: pe-reviewer**
- Tests verify behavior, not implementation
- Error cases have specific assertions
- Test data is realistic and minimal
- Setup/teardown properly isolated
- Co-location with implementation files

### 5. Generate Test Report
Categorize issues:
- **P1:** Missing coverage, broken tests, flaky tests
- **P2:** Improvements (naming, structure, clarity)

## Tools

### coverage-analyzer.py
See QCODET documentation for full usage.

**Quick usage:**
```bash
npm run test -- --coverage
python coverage-analyzer.py \
  --test-results coverage/coverage-summary.json \
  --requirements requirements/requirements.lock.md \
  --threshold 80
```

### req-id-extractor.py
See QCODET documentation for full usage.

**Quick usage:**
```bash
python req-id-extractor.py \
  --lock-file requirements/requirements.lock.md \
  --test-dir src/ \
  --output req-coverage.json
```

## Output Format

```markdown
# Test Review Report: [Feature Name]

**Reviewed By:** PE Reviewer, Test Writer
**Date:** YYYY-MM-DD
**Test Files Reviewed:** 3
**Total Tests:** 24
**Issues Found:** 6 (4 P1, 2 P2)

---

## Test Coverage Summary

**Overall Coverage:** 87.5% (target: 80%) ✓

| Metric | Coverage | Status |
|--------|----------|--------|
| Statements | 92.3% | ✓ |
| Branches | 85.7% | ✓ |
| Functions | 100% | ✓ |
| Lines | 91.8% | ✓ |

### Coverage by File

| File | Statements | Branches | Functions | Lines |
|------|------------|----------|-----------|-------|
| auth.service.ts | 95.0% | 88.2% | 100% | 94.5% |
| user.model.ts | 90.0% | 85.0% | 100% | 90.0% |
| profile.service.ts | 88.0% | 83.3% | 100% | 88.5% |

---

## REQ-ID Coverage Analysis

| REQ-ID | Description | Tests | Coverage | Status |
|--------|-------------|-------|----------|--------|
| REQ-101 | User creation | 5 | 100% | ✓ |
| REQ-102 | Validation | 4 | 100% | ✓ |
| REQ-103 | ID generation | 2 | 90% | ✓ |
| REQ-104 | Error handling | 0 | 0% | ✗ Missing |
| REQ-105 | Edge cases | 3 | 75% | ~ Partial |

**Missing Requirements:** REQ-104 has no tests
**Partial Coverage:** REQ-105 missing concurrent access tests

---

## P1 Issues (IMPORTANT)

### P1-1: No Tests for REQ-104 (Error Handling)
**Requirement:** System handles database connection failures gracefully

**Issue:**
No tests verify error handling when database is unavailable.

**Missing Tests:**
```typescript
describe('REQ-104: Error handling', () => {
  it('should throw DatabaseError when connection fails', async () => {
    // Mock database unavailable
    mockDb.connect.mockRejectedValue(new Error('Connection refused'));

    await expect(createUser(validData))
      .rejects
      .toThrow(DatabaseError);
  });

  it('should retry connection up to 3 times', async () => {
    // Test retry logic
  });

  it('should log error details for debugging', async () => {
    // Verify error logging
  });
});
```

**Impact:** Error scenarios untested, production issues likely

---

### P1-2: Flaky Test Detected
**Test:** `should create user with valid data` (REQ-101)
**File:** `src/auth.service.spec.ts:45`

**Issue:**
Test fails intermittently due to timing dependency

**Current:**
```typescript
it('should create user with valid data', async () => {
  const user = await createUser(validData);

  // Flaky: depends on async ID generation timing
  setTimeout(() => {
    expect(user.id).toBeDefined();
  }, 100); // Race condition
});
```

**Fix:**
```typescript
it('should create user with valid data', async () => {
  const user = await createUser(validData);

  // Deterministic: await properly
  expect(user.id).toBeDefined();
  expect(user.email).toBe(validData.email);
});
```

**Impact:** CI/CD unreliability

---

### P1-3: Tests Depend on Execution Order
**File:** `src/user.model.spec.ts`

**Issue:**
Tests share state, must run in specific order

**Current:**
```typescript
let sharedUser: User;

it('should create user', () => {
  sharedUser = createUser(data); // Sets shared state
});

it('should update user', () => {
  updateUser(sharedUser, updates); // Depends on previous test
});
```

**Fix:**
```typescript
describe('User model', () => {
  let user: User;

  beforeEach(() => {
    user = createUser(data); // Fresh state per test
  });

  it('should create user', () => {
    expect(user).toBeDefined();
  });

  it('should update user', () => {
    const updated = updateUser(user, updates);
    expect(updated.name).toBe(updates.name);
  });
});
```

**Impact:** Tests fail when run in isolation or different order

---

### P1-4: Missing Edge Case Tests
**Requirement:** REQ-105 (Handle special characters in names)

**Issue:**
Tests only cover ASCII names, missing Unicode/emoji tests

**Current Tests:**
```typescript
it('should accept valid name', () => {
  expect(validateName('John Doe')).toBe(true);
});
```

**Missing:**
```typescript
it('should accept Unicode names (REQ-105)', () => {
  expect(validateName('José García')).toBe(true);
  expect(validateName('李明')).toBe(true);
  expect(validateName('Müller')).toBe(true);
});

it('should reject emoji in names (REQ-105)', () => {
  expect(() => validateName('John 😀'))
    .toThrow('Names cannot contain emoji');
});

it('should handle names with multiple spaces (REQ-105)', () => {
  expect(validateName('Mary  Jane')).toBe(true); // Double space
});
```

**Impact:** Production bugs with international users

---

## P2 Issues (NICE-TO-HAVE)

### P2-1: Vague Test Descriptions
**File:** `src/auth.service.spec.ts`

**Issue:**
Test names don't reference REQ-IDs or describe expected behavior

**Current:**
```typescript
it('works', () => { }); // Too vague
it('test user creation', () => { }); // Missing REQ-ID
it('should return user', () => { }); // Missing context
```

**Suggested:**
```typescript
it('should create user with valid email and password (REQ-101)', () => { });
it('should reject duplicate email (REQ-101 edge case)', () => { });
it('should validate password strength (REQ-102)', () => { });
```

**Impact:** Test clarity and maintenance

---

### P2-2: Inconsistent Assertion Style
**File:** `src/user.model.spec.ts`

**Issue:**
Mix of assertion styles in same file

**Current:**
```typescript
expect(user.id).toBeDefined(); // Jest matcher
assert(user.email === 'test@example.com'); // Node assert
user.name.should.equal('John'); // Chai style
```

**Suggested:**
Pick one style and use consistently:
```typescript
// Jest style (recommended for Jest projects)
expect(user.id).toBeDefined();
expect(user.email).toBe('test@example.com');
expect(user.name).toBe('John');
```

**Impact:** Code consistency

---

## Test Quality Analysis

### Independence Score
```
Independent tests:  20/24 (83%) ✓
Dependent tests:    4/24  (17%) ✗
Recommendation: Fix P1-3 - isolate dependent tests
```

### Clarity Score
```
Clear descriptions: 18/24 (75%) ✓
Vague descriptions: 6/24  (25%) ~
Recommendation: Add REQ-IDs to test descriptions
```

### Determinism Score
```
Deterministic:      23/24 (96%) ✓
Flaky tests:        1/24  (4%)  ✗
Recommendation: Fix P1-2 - remove timing dependency
```

### Arrange-Act-Assert Pattern
```
Follows AAA:        22/24 (92%) ✓
Mixed pattern:      2/24  (8%)  ~
```

### Mock/Stub Usage
```
Appropriate:        18/20 (90%) ✓
Over-mocked:        2/20  (10%) ~
Recommendation: Consider testing actual implementation for simple utilities
```

---

## Coverage Gaps

### Uncovered Lines

**auth.service.ts:78-82** (REQ-104 error handling)
```typescript
} catch (error) {
  logger.error('Database error', error); // UNCOVERED
  throw new DatabaseError(error);        // UNCOVERED
}
```
**Solution:** Add P1-1 tests

**user.model.ts:45** (edge case)
```typescript
if (name.includes('  ')) {  // UNCOVERED
  name = name.replace(/\s+/g, ' '); // UNCOVERED
}
```
**Solution:** Add multiple spaces test

### Uncovered Branches

**auth.service.ts:validatePassword()**
```
Branch 1: password.length < 8     ✓ Covered
Branch 2: password.length > 100   ✗ NOT COVERED
Branch 3: !hasSpecialChar         ✓ Covered
```

**Solution:**
```typescript
it('should reject passwords longer than 100 characters (REQ-102)', () => {
  const longPassword = 'a'.repeat(101);
  expect(() => validatePassword(longPassword))
    .toThrow('Password too long');
});
```

---

## Recommendations

### Immediate Actions (P1)
1. Add tests for REQ-104 (error handling)
2. Fix flaky test in auth.service.spec.ts
3. Isolate dependent tests in user.model.spec.ts
4. Add edge case tests for REQ-105 (Unicode names)

### Improvements (P2)
1. Add REQ-IDs to all test descriptions
2. Standardize assertion style (use Jest consistently)

### Best Practices
- **Test Independence:** Use beforeEach for setup, no shared state
- **Naming:** Include REQ-ID and expected behavior
- **Edge Cases:** Test boundaries, nulls, empty, special characters
- **Error Cases:** Test every throw/reject path
- **Coverage:** Aim for 80%+ statements/branches
- **Determinism:** No timeouts, race conditions, random data
- **Focus:** Test behavior, not implementation details

---

## Next Steps

1. Add missing tests for REQ-104
2. Fix flaky test (P1-2)
3. Isolate dependent tests (P1-3)
4. Add Unicode/edge case tests (P1-4)
5. Re-run test suite and coverage
6. Verify all gates pass:
   ```bash
   npm run test -- --coverage
   npm run typecheck
   npm run lint
   ```
7. Update test documentation if needed
```

## Success Criteria

- Test coverage ≥80% (statements, branches, functions, lines)
- All REQ-IDs have corresponding tests
- No flaky tests
- Tests are independent (can run in any order)
- Clear test descriptions with REQ-IDs
- Edge cases covered
- Error paths tested
- Consistent assertion style
- Arrange-Act-Assert pattern followed

## When to Use QCHECKT vs QCHECK

**Use QCHECKT when:**
- Focused on test quality only
- Adding tests to existing code
- Reviewing test coverage
- Debugging flaky tests
- Quick test audit needed

**Use QCHECK when:**
- Full code review including implementation
- Security audit required
- Pre-merge comprehensive review
- Multiple files changed (code + tests)

## Related Skills

- **QCODET**: Write tests before running QCHECKT
- **QCHECK**: Full review including tests and implementation
- **QCHECKF**: Focused review of functions
- **QCODE**: Fix implementation if tests reveal gaps
- **QDOC**: Document test patterns and conventions
