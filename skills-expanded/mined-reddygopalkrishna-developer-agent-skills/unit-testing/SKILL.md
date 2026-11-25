---
name: unit-testing
description: Writes and updates unit tests for new or changed code in the project's existing framework and style, covering happy, error and boundary paths, then runs them with coverage and fixes failures. Use when implementing a feature or bug fix that needs tests, when asked to add or update unit tests or improve coverage for specific code, or when unit tests fail after a change. Not for choosing between test levels or fixing flaky tests (use test-strategy).
license: MIT
---

# Unit Testing

Every behavior you added or changed gets a unit test that would fail if that behavior broke. Test through the unit's public interface, match the tests already in the project, and treat coverage as a map of what you missed, never as the goal.

## When to use

- You wrote or changed a function, class, module or component and it needs tests.
- The user asks to add unit tests or raise coverage for specific code.
- Unit tests fail after a change and you must decide whether the code or the test is wrong.

Not for: deciding unit vs integration vs end-to-end, test doubles across a whole system, or flaky tests. Use the test-strategy skill for those. When you finish, run the verify-before-done skill.

## Workflow

1. **Detect the framework and conventions.** Look for config and existing tests:
   - JS/TS: `vitest.config.*`, `jest.config.*`, `"test"` in `package.json`, `*.test.ts` / `*.spec.ts`.
   - Python: `pytest.ini`, `[tool.pytest.ini_options]` in `pyproject.toml`, `conftest.py`, `test_*.py`.
   - Go: `*_test.go` next to the code.
   - Java/Kotlin: `src/test/java`, JUnit 5 or Kotest dependencies.
   - C#: `*.Tests.csproj` with xUnit, NUnit or MSTest.
   - Rust: `#[cfg(test)] mod tests` in the file, or `tests/`.
   Open the tests nearest to the code you changed. Copy their file location, naming, fixtures, factories, helpers and assertion style. Never add a second test framework.
2. **List what changed.** From the diff, write down each public function or method you added or changed, and each new branch, error path and edge case in it.
3. **Write the case list before the tests.** For each unit:
   - **Happy path:** typical valid input gives the expected output or effect.
   - **Error paths:** invalid input, thrown exceptions, rejected promises, error return values, failed dependencies.
   - **Boundaries:** empty, one, many; zero, negative, min/max; exactly at a limit and one past it; `null` / `undefined` / `None`; empty string, whitespace, Unicode; duplicates; date and time edges (month end, leap day, time zones).
   - **State:** each state transition, and calling things twice or out of order.
4. **Write the tests.** One behavior per test. Name it after the behavior (`rejects_expired_coupon`, `"returns 0 for an empty cart"`). Use Arrange-Act-Assert. Use table-driven tests for many input/output pairs (example below). Assert on outputs and visible effects, not on which private helpers were called.
5. **Keep them deterministic and fast.** Inject or fake the clock, random numbers, UUIDs and environment. No network, real database, file system or sleeps in unit tests; fake only those I/O boundaries and leave the logic under test real.
6. **Prove each new test can fail.** Break the code briefly (flip a condition, return a wrong value) or invert the expectation, watch the test fail with a clear message, then revert. A test you never saw fail may be testing nothing.
7. **Run the new tests, then the whole unit suite with coverage** (commands below). Look at uncovered lines **in the files you changed**. Add tests for uncovered behavior that matters. Leave trivial code (getters, generated code, framework glue) alone.
8. **Hand off to verification.** Run the full project checks with the verify-before-done skill before reporting.

## Running with coverage

| Stack | Command | Needs |
| --- | --- | --- |
| Vitest | `npx vitest run --coverage` | a coverage provider package, such as `@vitest/coverage-v8` |
| Jest | `npx jest --coverage` | built in |
| pytest | `pytest --cov=<package> --cov-report=term-missing` | `pytest-cov` |
| Go | `go test -coverprofile=cover.out ./...` then `go tool cover -func=cover.out` | built in |
| Maven | `mvn test jacoco:report` (report in `target/site/jacoco/`) | `jacoco-maven-plugin` configured with `prepare-agent` |
| Gradle | `./gradlew test jacocoTestReport` | the `jacoco` plugin applied |
| .NET | `dotnet test --collect:"XPlat Code Coverage"` | the `coverlet.collector` package in the test project |
| Rust | `cargo llvm-cov` | the `cargo-llvm-cov` tool installed |

If the project already has a coverage script (for example `npm run test:coverage`), use it instead. Adding a coverage package or tool changes the project, so ask the user first.

## Coverage is a signal, not a target

- Use the report to find **untested behavior**: an error branch with no test, a boundary never hit.
- Never write a test only to execute lines. A test with no meaningful assertion raises coverage and catches nothing.
- Don't lower a project's coverage threshold to make CI pass. Don't add exclusions to hide your own new code.
- High coverage with weak assertions is worse than lower coverage with strong ones, because it looks safe.

## Table-driven example

The same pattern exists in every framework (`it.each` / `test.each`, `@pytest.mark.parametrize`, Go table tests, JUnit `@ParameterizedTest`, xUnit `[Theory]`).

```python
import pytest
from shop.pricing import discount_for

@pytest.mark.parametrize(
    "total, expected",
    [
        (0, 0),          # empty cart
        (99.99, 0),      # just below threshold
        (100, 10),       # exactly at threshold
        (250, 25),       # typical
    ],
)
def test_discount_for_totals(total, expected):
    assert discount_for(total) == expected

def test_discount_rejects_negative_total():
    with pytest.raises(ValueError, match="negative"):
        discount_for(-1)
```

## Fixing failing tests

When a unit test fails after a change, decide which side is wrong before touching anything:

| Situation | Action |
| --- | --- |
| The behavior changed on purpose (new requirement) | Update the test to the new behavior, and say so in your report |
| The behavior changed by accident | Fix the code; leave the test as it is |
| The test relied on internals that were refactored | Rewrite the test against the public behavior |
| A snapshot changed | Read the diff line by line; update only if every change is intended |
| You can't tell which is right | Stop and ask the user, showing the old and new behavior |

Never delete, skip or loosen a failing test just to get green.

## Anti-patterns

- **Testing private methods directly.** Test through the public interface; if a private part needs its own tests, it may deserve its own unit.
- **Mocking the thing under test**, or mocking so much that the test only checks the mocks.
- **Asserting call sequences** (`expect(helper).toHaveBeenCalledTimes(3)`) instead of results.
- **Tautological tests** that recompute the expected value with the same logic as the code.
- **One giant test** covering ten behaviors; when it fails you don't know which one broke.
- **Snapshot everything** and approve every snapshot update without reading it.
- **Sleeps and real time** in unit tests.
- **Tests written after the fact that only pass**: never seen failing, so never proven.

## Done when

- Every added or changed behavior has a test, including its error and boundary cases.
- Each new test was seen failing once for the right reason.
- New tests follow the existing framework, layout and style.
- The unit suite passes; coverage of the changed files was reviewed, and gaps that matter are tested.
- Any test you changed is listed in your report with the reason.
