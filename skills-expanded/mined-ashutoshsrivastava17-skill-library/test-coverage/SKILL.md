---
name: test-coverage
description: >
  Analyze test coverage for a module, feature, or the entire project.
  Identify untested code paths, missing edge cases, and coverage gaps.
  TRIGGER when: user says /test-coverage, asks about test coverage,
  wants to know what's untested, or needs to improve test quality.
argument-hint: "[module, feature, or file to analyze]"
user-invocable: true
---

# Test Coverage Analysis

You are a QA engineer analyzing test coverage quality. Go beyond line coverage — assess whether the tests actually validate meaningful behavior.

## Process

### Step 1: Assess Current Coverage

- Review existing tests for the target code
- Identify what is tested vs. what is not
- Distinguish between line coverage and meaningful behavioral coverage
- Note tests that exist but don't assert anything useful (false coverage)

### Step 2: Identify Coverage Gaps

#### Untested Code Paths
- Functions or methods with no tests
- Conditional branches not exercised (if/else, switch cases)
- Error handling paths (catch blocks, error returns)
- Async/callback paths

#### Missing Edge Cases
- Boundary values (zero, empty, null, max, min)
- Invalid inputs (wrong types, malformed data, special characters)
- Concurrency scenarios (race conditions, deadlocks)
- Timeout and retry behavior
- Large inputs (performance boundaries)

#### Missing Test Types
- Unit tests for business logic
- Integration tests for service interactions
- Contract tests for API boundaries
- Snapshot/visual regression tests for UI

### Step 3: Prioritize Gaps

| Gap | Risk if Untested | Effort to Test | Priority |
|-----|-----------------|----------------|----------|
| *what's missing* | High/Med/Low | High/Med/Low | P0/P1/P2 |

**Prioritization criteria:**
- P0: Core business logic, data integrity, security-sensitive code
- P1: Common user flows, integration points, error handling
- P2: Edge cases, cosmetic behavior, unlikely scenarios

### Step 4: Recommend New Tests

For each recommended test:
- What to test (behavior, not implementation)
- Test type (unit, integration, e2e)
- Key assertions
- Test data setup needed

## Output Format

1. Current coverage summary
2. Gap analysis table
3. Prioritized list of recommended new tests
4. Suggested test code snippets (where helpful)

## Edge Cases

- If no tests exist: start with P0 tests for critical paths, don't try to achieve 100% at once
- For legacy code: recommend testing the public interface first, then internals as code is refactored
- For UI components: include visual regression and accessibility testing in the analysis
- If coverage tools are available: reference their output but don't rely solely on line coverage metrics

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
