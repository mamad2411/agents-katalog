---
name: testing-methodology
description: >
  Testing strategy and patterns. Test pyramid, AAA pattern, TDD workflow, coverage targets,
  edge case checklists, and framework-specific patterns. Use when writing tests, designing
  test strategies, or reviewing test quality.
---

# testing-methodology

Testing strategy and patterns.

## how to use

- `/testing-methodology`
  Apply these testing standards to all test code in this conversation.

- `/testing-methodology <file>`
  Review test file against rules below and report:
  - violations (quote the exact line or snippet)
  - why it matters (one short sentence)
  - a concrete fix

## when to apply

Reference these guidelines when:
- writing unit, integration, or end-to-end tests
- designing a test strategy for a new feature
- reviewing test quality and coverage
- setting up test infrastructure or CI pipelines
- choosing between mocking strategies
- debugging flaky tests

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | test structure | critical |
| 2 | test pyramid | critical |
| 3 | edge cases | high |
| 4 | mocking strategy | high |
| 5 | test quality | medium |
| 6 | CI integration | medium |

## quick reference

### 1. test structure (critical)

- follow AAA pattern: Arrange, Act, Assert
- one logical assertion per test (multiple asserts OK if testing one behavior)
- test names describe the scenario and expected outcome: `test_<action>_<condition>_<expected>`
- keep tests independent; no shared mutable state between tests
- use fixtures/factories for test data setup
- tests must be deterministic; no random data without seeding
- prefer real values over magic numbers in test data

### 2. test pyramid (critical)

**Target ratios** (guideline, not dogma):
- Unit tests: 70% — fast, isolated, test single functions/methods
- Integration tests: 20% — test component interactions, API contracts, database queries
- E2E tests: 10% — test critical user flows, smoke tests

**Unit tests**:
- test one unit of behavior in isolation
- mock external dependencies (APIs, databases, filesystem)
- should run in < 100ms per test
- cover happy path, error cases, and boundary conditions

**Integration tests**:
- test real interactions between components
- use test databases or containers where possible
- verify API contracts and response shapes
- test database migrations and queries against real schemas

**E2E tests**:
- cover critical business flows only (login, checkout, core workflow)
- use stable selectors (data-testid, aria-label) over CSS classes
- implement retry logic for flaky network conditions
- keep E2E suite small and fast; run in CI

### 3. edge cases (high)

**Always test these boundaries**:
- empty input (null, undefined, empty string, empty array, 0)
- maximum/minimum values (MAX_INT, boundary conditions)
- off-by-one errors (< vs <=, first/last element)
- unicode and special characters in text input
- concurrent access and race conditions
- timeout and network failure scenarios
- invalid/malformed input
- permission denied scenarios
- large inputs (performance boundary)

### 4. mocking strategy (high)

**Decision tree**:
- External API: mock (use recorded responses or fixtures)
- Database: integration test with test DB; mock for unit tests
- Time/dates: mock (use clock injection)
- Filesystem: mock for unit tests; use temp dirs for integration
- Internal modules: prefer real implementation; mock only at boundaries

**Rules**:
- mock at boundaries, not internals
- verify mock interactions only when the interaction IS the behavior
- keep mocks simple; complex mocks indicate design problems
- use spies over mocks when you only need to observe
- update mocks when API contracts change

### 5. test quality (medium)

- tests should fail for the right reason and pass for the right reason
- delete tests that test implementation details instead of behavior
- flaky tests must be fixed immediately or quarantined
- test code deserves the same quality standards as production code
- avoid testing framework/library internals
- coverage target: 80%+ for critical paths, 60%+ overall (measure branch coverage)
- 100% coverage is not a goal; diminishing returns past 85%

### 6. CI integration (medium)

- run unit tests on every push
- run integration tests on PR and main branch
- run E2E tests on main branch and before deploy
- fail fast: run fastest tests first
- parallelize test suites where possible
- cache dependencies between runs
- report coverage trends, not just absolute numbers

## framework patterns

### pytest (Python)
- use `@pytest.fixture` for setup, `conftest.py` for shared fixtures
- use `@pytest.mark.parametrize` for data-driven tests
- use `tmp_path` fixture for filesystem tests
- group tests with classes for shared setup
- use `pytest-cov` for coverage, `pytest-xdist` for parallelism

### vitest / jest (TypeScript/JavaScript)
- use `describe`/`it` blocks for grouping
- use `beforeEach`/`afterEach` for setup/teardown
- use `vi.mock()` / `jest.mock()` for module mocking
- prefer `toEqual` for deep comparison, `toBe` for identity

### playwright (E2E)
- use Page Object Model for maintainability
- use `data-testid` attributes for element selection
- use `expect(locator).toBeVisible()` over raw selectors
- implement proper waiting strategies; avoid hard waits

## anti-patterns

| anti-pattern | problem | fix |
|-------------|---------|-----|
| testing implementation details | breaks on refactor | test behavior and outputs |
| shared mutable state | flaky, order-dependent | isolate each test |
| no assertions | test always passes | add meaningful assertions |
| excessive mocking | tests don't catch real bugs | mock at boundaries only |
| sleep/wait in tests | slow and flaky | use proper async/event waiting |
| testing getters/setters | no value | test meaningful behavior |
