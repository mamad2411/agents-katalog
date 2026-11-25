---
name: testing
version: 1.0.0
description: Write, run, and interpret tests — assess coverage and quality
uses:
  - analysis/research
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:write
    - command:execute
  requires_approval: false
---

# Testing

Write, run, and interpret tests for any codebase. This skill covers the full testing lifecycle — determining what to test, writing effective tests, running them, interpreting results, and assessing coverage quality.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `test` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- Writing tests for new code (before or after implementation)
- Running existing tests and interpreting failures
- Assessing test coverage and identifying gaps
- Evaluating test quality (are tests meaningful or just coverage padding?)
- Diagnosing flaky tests
- Choosing a testing strategy for a new feature

## Methodology

### 1. Understand the Test Target

Before writing or evaluating tests, understand:
- **What does the code do?** Read the implementation thoroughly
- **What are the inputs?** Parameters, configuration, external data
- **What are the outputs?** Return values, side effects, state changes
- **What can go wrong?** Error cases, edge cases, boundary conditions
- **What are the dependencies?** External services, databases, file systems

### 2. Choose Testing Strategy

| Strategy | When to Use | Characteristics |
|----------|-------------|-----------------|
| **Unit tests** | Individual functions/methods | Fast, isolated, mock dependencies |
| **Integration tests** | Component interactions | Slower, real dependencies, verify wiring |
| **End-to-end tests** | Full workflows | Slowest, full stack, verify user scenarios |
| **Property-based tests** | Input-dependent logic | Generated inputs, verify invariants |
| **Regression tests** | After bug fixes | Reproduce the bug, verify the fix |

**Default**: Start with unit tests. Add integration tests for critical paths. E2E tests for key user workflows.

### 3. Design Test Cases

For each function/behavior, design cases covering:

**Happy path**: Normal inputs, expected behavior
- Typical use case with valid inputs
- Expected output matches specification

**Edge cases**: Boundary conditions
- Empty inputs (empty string, empty list, zero, null)
- Single element (list with one item, string with one character)
- Maximum values (very large numbers, very long strings)
- Boundary values (off-by-one, exactly at limits)

**Error cases**: Things that should fail
- Invalid inputs (wrong type, out of range)
- Missing required inputs
- External dependency failures (network down, file not found)
- Permission errors

**State transitions**: If stateful
- Initial state → action → expected state
- Invalid state transitions (should be rejected)

### 4. Write Tests

Follow the **Arrange-Act-Assert** pattern:

```
Arrange: Set up preconditions and inputs
Act:     Execute the code under test
Assert:  Verify the expected outcome
```

**Naming convention**: `test_<what>_<condition>_<expected>`
- `test_login_valid_credentials_returns_token`
- `test_login_expired_password_raises_auth_error`
- `test_parse_empty_input_returns_empty_list`

**Test independence**: Each test must be self-contained. No test should depend on another test's output or side effects.

### 5. Run Tests

Execute the test suite using the project's test runner:
- Detect the framework (pytest, jest, cargo test, go test, etc.)
- Run with verbose output to see individual test results
- Capture both pass/fail status and any error output

### 6. Interpret Results

For failures, diagnose:
- **Assertion failure**: Expected vs actual — is the test wrong or the code?
- **Exception/error**: What threw and why — missing mock, real bug, or test setup issue?
- **Timeout**: Test hanging — infinite loop, deadlock, or waiting for external resource?
- **Flaky**: Passes sometimes — race condition, time-dependent, or order-dependent?

### 7. Assess Coverage

Evaluate test quality beyond just line coverage:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Line coverage** | Lines executed by tests | 80%+ for critical code |
| **Branch coverage** | Decision branches taken | Every if/else, every case |
| **Mutation coverage** | Tests that catch code changes | Tests fail when code is wrong |
| **Edge case coverage** | Boundary conditions tested | Every edge case from step 3 |

**Coverage is necessary but not sufficient**: 100% line coverage with no assertions is worthless. Focus on meaningful assertions.

## Output Format

```
## Testing: [Target]

### Strategy
- Approach: [unit/integration/e2e]
- Framework: [detected framework]
- Files: [test file paths]

### Test Cases
| # | Test | Category | Status |
|---|------|----------|--------|
| 1 | [name] | [happy/edge/error] | [pass/fail/skip] |

### Results
- Passed: [N]
- Failed: [N]
- Skipped: [N]
- Duration: [time]

### Failures (if any)
| Test | Error | Diagnosis |
|------|-------|-----------|
| [name] | [error summary] | [test bug / code bug / setup issue] |

### Coverage Assessment
- Line coverage: [%]
- Missing coverage: [list of uncovered areas]
- Quality: [meaningful assertions / coverage padding / gaps]

### Recommendations
- [what to add/fix/improve]
```

## Quality Criteria

- Tests cover happy path, edge cases, and error cases
- Tests follow Arrange-Act-Assert pattern
- Test names clearly describe what they verify
- Tests are independent (no shared mutable state between tests)
- Assertions are meaningful (verify behavior, not just execution)
- Mocks are used appropriately (mock external dependencies, not the thing under test)
- Test failures produce clear error messages
- Coverage targets critical code paths, not just line count

## Common Mistakes

- **Testing implementation, not behavior**: Asserting internal state or method calls instead of observable behavior. Tests should verify WHAT the code does, not HOW it does it.
- **No edge case coverage**: Only testing the happy path. Real bugs live at boundaries — empty inputs, maximum values, null pointers.
- **Test interdependence**: Test B relies on Test A running first. Reorder the tests and B fails. Each test must set up its own state.
- **Over-mocking**: Mocking the thing you're testing. Mock external dependencies (databases, APIs), not the code under test.
- **Assertion-free tests**: Running code without asserting anything. This verifies the code doesn't crash, but not that it works correctly.
- **Flaky tests ignored**: Tests that sometimes pass and sometimes fail indicate real problems (race conditions, time dependencies). Don't ignore them.
- **Coverage worship**: Optimizing for line coverage percentage rather than test quality. A test that covers 10 lines with a meaningful assertion is better than one that covers 100 lines with no assertions.

## Completion

Testing is complete when:
- Test strategy is chosen appropriately for the target
- Test cases cover happy path, edge cases, and error cases
- Tests are written following best practices (AAA, independence, clear naming)
- Tests are run and results are interpreted
- Failures are diagnosed (test bug vs code bug)
- Coverage is assessed for quality, not just quantity
- Recommendations for improvement are provided
