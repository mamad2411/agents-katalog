---
name: QCODE
version: 1.0.0
description: Implement functionality to pass tests (TDD green phase). Write minimal code, run tests iteratively, ensure prettier/typecheck/lint pass.
trigger: QCODE
dependencies:
  agents:
    - sde-iii
    - implementation-coordinator
tools: []
claude_tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
---

# QCODE - Implementation (Green Phase)

## Purpose

Implement functionality to make failing tests pass. Write minimal, clean code that satisfies test requirements without over-engineering.

## Workflow

### 1. Read Failing Tests
**Agent: sde-iii**
- Read all test files created by QCODET
- Understand acceptance criteria from assertions
- Identify test setup requirements (dependencies, mocks)
- List tests in order of implementation

### 2. Plan Implementation Order
**Agent: implementation-coordinator**
- Start with simplest tests (foundational logic)
- Build up to complex tests (integration)
- Identify shared utilities to implement first
- Coordinate parallel implementation if multiple files

### 3. Implement Minimum Code
**Agent: sde-iii**
- Write only enough code to pass current test
- Follow existing codebase patterns
- Use domain vocabulary
- Keep functions small and focused
- Type safety with branded types
- No comments - code explains itself

### 4. Run Tests Iteratively
**Cycle per test:**
```bash
# Run single test
npm run test -- path/to/file.spec.ts -t "test name"

# If fails: debug and fix
# If passes: commit and move to next test

# Run all tests periodically
npm run test
```

### 5. Quality Gates
After each significant change:
```bash
npm run format     # Prettier formatting
npm run typecheck  # Type checking
npm run lint       # Linting
npm run test       # All tests
```

### 6. Refactor (Optional)
**Only if tests pass:**
- Extract duplicate code
- Improve naming
- Simplify complex functions
- Re-run tests after each refactor

## Implementation Principles

### Minimal Code
Write only what's needed to pass tests:
```typescript
// BAD: Over-engineering
class UserService {
  private cache: Map<string, User>;
  private eventEmitter: EventEmitter;

  async createUser(data: UserData): Promise<User> {
    // Caching, events, etc. not needed yet
  }
}

// GOOD: Minimal
export function createUser(data: UserData): User {
  validateEmail(data.email);
  validatePassword(data.password);
  return { id: generateId(), ...data };
}
```

### Type Safety
Use branded types for domain concepts:
```typescript
// BAD: Primitive obsession
function getUser(id: string): User { }

// GOOD: Branded types
type UserId = string & { readonly brand: unique symbol };
function getUser(id: UserId): User { }
```

### Domain Vocabulary
Use business language:
```typescript
// BAD: Technical names
function processData(input: any): any { }

// GOOD: Domain names
function enrollStudent(application: StudentApplication): Enrollment { }
```

### Small Functions
```typescript
// BAD: Large function
function createAccount(data: FormData): Account {
  // 50 lines of validation, transformation, persistence
}

// GOOD: Composed small functions
function createAccount(data: FormData): Account {
  const validated = validateAccountData(data);
  const account = buildAccount(validated);
  return persistAccount(account);
}
```

## Output Format

```markdown
# Implementation Report: [Feature Name]

## Test Status

| File | Tests Passing | Tests Failing |
|------|---------------|---------------|
| auth.service.spec.ts | 5/5 | 0 |
| user.model.spec.ts | 3/3 | 0 |
| **Total** | **8/8** | **0** |

**Status:** GREEN PHASE COMPLETE ✓

## Files Implemented

### src/auth.service.ts
- `createUser()` - REQ-101: User creation
- `validateEmail()` - REQ-102: Email validation
- `validatePassword()` - REQ-102: Password validation
- Lines: 45
- Complexity: Low

### src/user.model.ts
- `UserModel` interface - REQ-101: User data structure
- `generateId()` - REQ-103: ID generation
- Lines: 20
- Complexity: Low

## Implementation Summary

**Total Lines Added:** 65
**Story Points Completed:** 3.5 SP
**Test Coverage:** 92%

## Quality Gates

```bash
✓ Prettier: All files formatted
✓ TypeCheck: No type errors
✓ Lint: No linting issues
✓ Tests: 8 passing, 0 failing
```

## Test Execution

```
PASS src/auth.service.spec.ts
  ✓ REQ-101: validates email format (12ms)
  ✓ REQ-101: checks password strength (8ms)
  ✓ REQ-101: creates user with valid data (15ms)
  ✓ REQ-102: rejects duplicate email (10ms)
  ✓ REQ-102: handles special characters (9ms)

PASS src/user.model.spec.ts
  ✓ REQ-103: generates unique IDs (5ms)
  ✓ REQ-103: creates valid user object (7ms)
  ✓ REQ-103: enforces required fields (6ms)

Test Suites: 2 passed, 2 total
Tests:       8 passed, 8 total
Time:        1.234s
```

## Code Patterns Used

**Reused from codebase:**
- `src/shared/validation.ts` - email/password validators
- `src/shared/id-generator.ts` - ID generation utility
- `src/types/common.ts` - base type definitions

**New patterns introduced:**
- Branded type `UserId` for type safety
- Function composition for user creation
- Explicit error types for validation failures

## Refactoring Done

1. Extracted `validateEmail()` - used in 3 places
2. Simplified `createUser()` - removed nested conditionals
3. Renamed `makeNewUser()` → `createUser()` for consistency

All refactorings verified by re-running tests.

## Coverage Report

```
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
auth.service.ts     |   92.5  |   88.2   |  100.0  |   93.1  |
user.model.ts       |   90.0  |   85.7   |  100.0  |   90.9  |
--------------------|---------|----------|---------|---------|
All files           |   91.8  |   87.5   |  100.0  |   92.3  |
```

## Next Steps

1. Run QCHECK for comprehensive code review
2. Run QDOC to update documentation
3. Consider QGIT to commit changes
```

## Success Criteria

- All tests passing (green phase)
- Quality gates pass (prettier, typecheck, lint, test)
- Code follows codebase conventions
- Functions are small and focused
- Type safety with branded types where appropriate
- Domain vocabulary used throughout
- Test coverage ≥80%
- No over-engineering - minimal code only

## Anti-Patterns to Avoid

### Over-Engineering
Don't add features not required by tests:
- Caching (unless REQ specifies)
- Event systems (unless REQ specifies)
- Complex abstractions (unless multiple uses)

### Premature Optimization
Write clear code first:
- No micro-optimizations
- No clever tricks
- Readability over performance (unless REQ specifies)

### Implementation Details Leaking
Hide internals:
```typescript
// BAD: Leaking SQL details
export async function getUser(sql: string): Promise<User>

// GOOD: Clean interface
export async function getUser(id: UserId): Promise<User>
```

### Skipping Quality Gates
Must pass after each change:
```bash
# BAD: Skip checks, commit broken code
git commit -m "quick fix"

# GOOD: Verify all gates
npm run typecheck && npm run lint && npm run test
git commit -m "feat: implement user creation (REQ-101)"
```

## Related Skills

- **QCODET**: Provides failing tests to implement
- **QCHECK**: Next step - comprehensive code review
- **QCHECKF**: Lighter review focused on functions
- **QDOC**: Update documentation after implementation
- **QGIT**: Commit changes with conventional commits
