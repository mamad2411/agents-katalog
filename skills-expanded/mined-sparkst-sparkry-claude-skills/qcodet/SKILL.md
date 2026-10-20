---
name: QCODET
version: 1.0.0
description: Write tests first (TDD red phase). Tests reference REQ-IDs, fail initially, pass prettier/typecheck/lint. Co-located test files with clear assertions.
trigger: QCODET
dependencies:
  agents:
    - test-writer
tools:
  - test-scaffolder.py
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

# QCODET - Test-Driven Development (Red Phase)

## Purpose

Write failing tests first following TDD methodology. Tests cite REQ-IDs from requirements.lock.md and establish the contract that implementation must satisfy.

## Workflow

### 1. Extract REQ-IDs
**Tool: req-id-extractor.py**
- Parse `requirements/requirements.lock.md`
- Extract all REQ-IDs and acceptance criteria
- Generate test checklist

### 2. Generate Test Stubs
**Tool: test-scaffolder.py**
**Agent: test-writer**
- Analyze implementation plan
- Create co-located test files (`*.spec.ts`)
- Generate describe/it blocks per REQ-ID
- Add TODO comments for each test case

### 3. Implement Test Cases
**Agent: test-writer**
- Write test setup (mocks, fixtures)
- Implement assertions per acceptance criteria
- Add edge case tests
- Reference REQ-IDs in test descriptions

### 4. Verify Test Failures
**Tool: coverage-analyzer.py**
- Run test suite: `npm run test`
- Confirm all new tests fail (red phase)
- Verify test quality (no false positives)
- Document expected failures

### 5. Quality Gates
- Run prettier: `npm run format` or verify formatting
- Run typecheck: `npm run typecheck`
- Run lint: `npm run lint`
- All gates must pass (except tests fail as expected)

## Tools

### req-id-extractor.py
Extracts requirements from lock file:

**Usage:**
```bash
python req-id-extractor.py \
  --lock-file requirements/requirements.lock.md \
  --output test-checklist.json
```

**Output:**
```json
{
  "REQ-101": {
    "description": "User can create account",
    "acceptance": ["Email validation", "Password strength check"],
    "edge_cases": ["Duplicate email", "Special characters"]
  }
}
```

### test-scaffolder.py
Generates test file stubs:

**Usage:**
```bash
python test-scaffolder.py \
  --requirements test-checklist.json \
  --implementation-file src/auth.service.ts \
  --output src/auth.service.spec.ts
```

**Output:**
```typescript
// src/auth.service.spec.ts
import { AuthService } from './auth.service';

describe('AuthService', () => {
  describe('REQ-101: User can create account', () => {
    it('validates email format', () => {
      // TODO: Implement test
    });

    it('checks password strength', () => {
      // TODO: Implement test
    });
  });
});
```

### coverage-analyzer.py
Analyzes test coverage:

**Usage:**
```bash
python coverage-analyzer.py \
  --test-results coverage/coverage-summary.json \
  --requirements requirements/requirements.lock.md \
  --threshold 80
```

**Output:**
```
Coverage Report:
- Lines: 0% (expected for red phase)
- Branches: 0%
- REQ-101: 2 tests written
- REQ-102: 3 tests written
Missing tests:
- REQ-103: Edge case for [scenario]
```

## Test Structure

### Co-located Tests
```
src/
  feature/
    auth.service.ts
    auth.service.spec.ts    # Co-located with implementation
    user.model.ts
    user.model.spec.ts
```

### Test Template
```typescript
// feature-name.spec.ts

import { describe, it, expect, beforeEach } from '@jest/globals';
import { FeatureName } from './feature-name';

describe('FeatureName', () => {
  let service: FeatureName;

  beforeEach(() => {
    service = new FeatureName();
  });

  describe('REQ-101: [Requirement Description]', () => {
    it('should [acceptance criterion 1]', () => {
      // Arrange
      const input = { /* test data */ };

      // Act
      const result = service.method(input);

      // Assert
      expect(result).toEqual(expected);
    });

    it('should handle edge case: [scenario]', () => {
      // Arrange - edge case setup
      const invalidInput = { /* edge case data */ };

      // Act & Assert
      expect(() => service.method(invalidInput)).toThrow('Expected error');
    });
  });

  describe('REQ-102: [Next Requirement]', () => {
    // ... more tests
  });
});
```

## Output Format

```markdown
# Test Implementation Report: [Feature Name]

## REQ Coverage

| REQ-ID | Description | Tests Written | Status |
|--------|-------------|---------------|--------|
| REQ-101 | User creation | 3 | FAILING |
| REQ-102 | Validation | 2 | FAILING |

## Test Files Created

- `src/auth.service.spec.ts` (5 tests)
- `src/user.model.spec.ts` (3 tests)

## Test Execution Results

```
FAIL src/auth.service.spec.ts
  ✕ REQ-101: validates email format (expected failure)
  ✕ REQ-101: checks password strength (expected failure)
  ...

Test Suites: 0 passed, 2 failed, 2 total
Tests:       0 passed, 8 failed, 8 total
```

**Status:** RED PHASE COMPLETE ✓

All tests fail as expected. Implementation not yet written.

## Quality Gates

- ✓ Prettier: All files formatted
- ✓ TypeCheck: No type errors in tests
- ✓ Lint: No linting issues
- ✗ Tests: 8 failing (expected in red phase)

## Coverage Goals

**Target:** 80% coverage after QCODE implementation

**Current:** 0% (no implementation exists)

**Missing Tests:** None - all requirements have test coverage

## Next Steps

1. Run QCODE to implement functionality
2. Tests should turn green one by one
3. Aim for all tests passing
4. Run QCHECK for code review
```

## Success Criteria

- All REQ-IDs from requirements.lock.md have tests
- Tests are co-located with implementation files
- Tests cite REQ-IDs in descriptions
- All tests FAIL (red phase)
- Prettier, typecheck, lint all pass
- No false positives (tests fail for right reasons)
- Test coverage plan reaches 80%+ threshold

## Quality Checklist

- [ ] Tests reference REQ-IDs in describe/it blocks
- [ ] Acceptance criteria mapped to assertions
- [ ] Edge cases have explicit tests
- [ ] Arrange-Act-Assert pattern used
- [ ] Mocks/stubs set up correctly
- [ ] Tests are deterministic (no flaky tests)
- [ ] Error cases test specific error messages
- [ ] Tests verify behavior, not implementation details

## Related Skills

- **QPLAN**: Provides implementation plan and REQ-IDs
- **QCODE**: Next step - implement to make tests pass
- **QCHECKT**: Focused review of test quality
- **QCHECK**: Full code review including tests
