---
name: testing
description: "Test generation and coverage analysis. Activated when the user says \"create tests\", \"write tests\", \"test this\", \"check coverage\", \"add test\", \"missing tests\", \"TDD\", or wants to create or improve tests."
allowed tools: Read, Write, Edit, Grep, Glob, Bash
---

# Testing

Analyze code and generate meaningful tests. Not just "test the function" —
understand what the code does, identify edge cases, and create tests that
catch real bugs.

## Rules

1. **Read before testing** — understand the code's purpose and dependencies before writing tests
2. **AAA pattern** — every test: Arrange (setup), Act (execute), Assert (verify)
3. **One assertion per concept** — test one behavior per `it`/`test` block
4. **Test behavior, not implementation** — test what the function does, not how it does it
5. **Edge cases matter** — null, empty, boundary values, error paths
6. **Name tests descriptively** — `"should return 0 when cart is empty"`, not `"test1"`
7. **No test interdependence** — each test must work independently and in any order
8. **Run after writing** — always execute the tests to confirm they pass

## Workflow

### Phase 1: Analyze the code
1. Read the source file(s) to test
2. Identify:
   - **Public API surface** — exported functions, class methods, endpoints
   - **Dependencies** — what it imports, what needs mocking
   - **Side effects** — DB calls, HTTP requests, file I/O, timers
   - **Edge cases** — null inputs, empty arrays, boundary values, error conditions
   - **Business rules** — domain-specific logic that MUST be correct

### Phase 2: Decide test type

| What you're testing | Test type | Approach |
|---|---|---|
| Pure function (no side effects) | Unit test | Direct call, no mocks needed |
| Function with dependencies | Unit test | Mock dependencies, test logic in isolation |
| Multiple modules working together | Integration test | Minimal mocking, test the interaction |
| API endpoint | Integration test | Test request/response cycle |
| User workflow | E2E test | Test full flow from user perspective |
| Data transformation | Unit test | Input → expected output tables |

### Phase 3: Generate tests

#### Structure
```
describe('[ModuleName]', () => {
  describe('[functionName]', () => {
    // Happy path
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      // Act
      // Assert
    });

    // Edge cases
    it('should [behavior] when input is null/empty/zero', () => { ... });
    it('should [behavior] when input is at boundary', () => { ... });

    // Error cases
    it('should throw/return error when [invalid condition]', () => { ... });
  });
});
```

#### Test categories (check all that apply)
- [ ] **Happy path** — normal expected inputs produce correct output
- [ ] **Empty/null inputs** — graceful handling of missing data
- [ ] **Boundary values** — min, max, zero, one, off-by-one
- [ ] **Invalid inputs** — wrong type, out of range, malformed
- [ ] **Error paths** — network failure, timeout, permission denied
- [ ] **Async behavior** — promises resolve/reject correctly, timeouts work
- [ ] **State changes** — before/after state is correct
- [ ] **Concurrency** — race conditions, parallel execution
- [ ] **Security** — injection, overflow, unauthorized access

### Phase 4: Mock strategy

| What to mock | When | How |
|---|---|---|
| External APIs | Always in unit tests | Mock the HTTP client or service layer |
| Database | Unit tests | Mock the repository/ORM. Integration: use test DB |
| File system | When testing logic, not I/O | Mock fs module |
| Time/dates | When testing time-dependent logic | Mock `Date.now()` or clock |
| Random values | When testing deterministic behavior | Mock `Math.random()` or seed |
| Environment vars | When testing config-dependent paths | Mock `process.env` or equivalent |

**Do NOT mock:**
- The thing you're testing
- Simple data transformations
- Standard library functions

### Phase 5: Run and verify
1. Run the new tests: `[SPEC] test command`
2. All tests should **pass** — if not, fix the test or the code
3. Check coverage of the new tests: `[SPEC] coverage command`
4. If coverage gaps remain in the tested code, add more tests

## Test quality checklist
- [ ] Tests fail when the code is wrong (try breaking the code to verify)
- [ ] Tests don't depend on execution order
- [ ] No hardcoded ports, file paths, or timing assumptions
- [ ] Async tests use proper await/done patterns (no fire-and-forget)
- [ ] Test data is created within the test (not shared mutable state)
- [ ] Mocks are reset between tests (`beforeEach` / `setUp`)
- [ ] Error messages in assertions are descriptive

## [SPEC] Project-specific patterns
- Test framework: [SPEC] (Jest, Vitest, Pytest, Go testing, etc.)
- Test file location: [SPEC] (`__tests__/`, `*.test.ts`, `*_test.go`, `test_*.py`)
- Test file naming: [SPEC] (`{source}.test.{ext}`, `test_{source}.{ext}`)
- Fixture pattern: [SPEC] (factory, builder, fixtures dir)
- Mock framework: [SPEC] (jest.mock, unittest.mock, testify/mock)
- Coverage tool: [SPEC] (istanbul/c8, coverage.py, go cover)
- Minimum coverage: [SPEC]% (suggestion: 80% overall, 90% for business logic)
- Max test time: [SPEC] (unit: 10s, integration: 60s, e2e: 5min)

## References
- `docs/specs/testing-strategy/` — test pyramid, QA process
- Test framework docs: [SPEC]
