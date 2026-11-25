---
name: lyra-tdd
description: "Test-driven development with a coverage gate that catches dummy tests. Use when writing new code, fixing bugs test-first, or enforcing coverage across nine languages."
compatibility: "No tools required. Optional: language-specific test runners and mutation tools (Stryker, mutmut, Infection, cargo-mutants, PIT)."
---

# lyra-tdd

## What it does

Test-driven development with a coverage gate that actually catches dummy tests. Reach for it when writing new code, fixing bugs test-first, or enforcing coverage thresholds across TypeScript, JavaScript, Python, PHP, Go, Rust, Java, C#, and Ruby. The 100% line number is a weak signal — `if (x > 0)` with only `x = 1` hits 100% lines and misses half the branches — so this skill layers branch coverage and mutation testing on top. Seven anti-dummy-test rules block the easy routes to a green suite that asserts nothing. Throwaway spikes, pure layout, and one-off scripts don't need it.

## The rules

### 1. Plan first — no code without a spec

State the behavior in one sentence ("Given X, when Y, then Z"), list inputs, outputs, side effects, edge cases, and error paths, then turn each line into a test name. Coding to "discover" the spec is debugging with extra steps.

### 2. One test at a time: red, green, refactor

Write one failing test, confirm it fails for the right reason (assertion, not compile error), write the minimum code to pass, refactor with the test green. Never batch — batching is test-after-the-fact in a TDD costume.

| Language | Run one test                   | Coverage                                                    |
| -------- | ------------------------------ | ----------------------------------------------------------- |
| TS/JS    | `vitest -t "name"`             | `vitest run --coverage.enabled`                             |
| Python   | `pytest -k name`               | `pytest --cov=<pkg> --cov-branch --cov-report=term-missing` |
| PHP      | `pest --filter=name`           | `pest --coverage --min=100`                                 |
| Go       | `go test -run TestName`        | `go test -coverprofile=cover.out ./...`                     |
| Rust     | `cargo test name`              | `cargo llvm-cov --fail-under-lines 100`                     |
| Java     | `mvn -Dtest=Class#method test` | `mvn test jacoco:report`                                    |
| C#       | `dotnet test --filter Name`    | `coverlet /p:Threshold=100`                                 |
| Ruby     | `rspec -e "name"`              | `SimpleCov` + `minimum_coverage 100`                        |

### 3. 100% coverage is the floor, not the goal

Line=100 with branch=80 means you have holes. Require 100% branches as the floor, 100% lines as the secondary gate, and a mutation score ≥ 95% as the truth check — surviving mutants are dummy tests wearing a 100%-coverage costume. Documented exclusions only: generated code, feature-flag-gated code, and type-system-unreachable branches. Each exclusion gets a comment naming the reason. Everything else is covered or it does not merge.

| Language | Coverage                            | Mutation                   |
| -------- | ----------------------------------- | -------------------------- |
| TS/JS    | vitest --coverage / jest --coverage | Stryker                    |
| Python   | pytest-cov + coverage.py            | mutmut or cosmic-ray       |
| PHP      | Pest/PHPUnit --coverage             | Infection (`--min-msi=95`) |
| Go       | go test -coverprofile               | go-mutesting               |
| Rust     | cargo-tarpaulin / cargo-llvm-cov    | cargo-mutants              |
| Java     | JaCoCo                              | PIT                        |
| C#       | coverlet                            | Stryker.NET                |
| Ruby     | SimpleCov                           | mutant                     |

Mutation is slow — run it nightly in CI, not on every push. Coverage runs on every push.

### 4. No tautology tests

A tautology test asserts the thing it set up. It tests the language, not your code.

```python
# bad
def test_add():
    result = 2 + 2
    assert result == 4  # tests Python, not your code

# good
def test_add_returns_sum():
    assert add(2, 2) == 4
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### 5. No `expect(true)` or empty assertions

If a test's only assertion is `assert True`, `expect(true).toBe(true)`, or `.toBeTruthy()` on a constant, it is not a test. Delete it.

```typescript
// bad
it("calculates total", () => {
  calculateTotal([1, 2, 3]);
  expect(true).toBe(true); // function could return anything
});

// good
it("returns the sum of line items", () => {
  expect(calculateTotal([1, 2, 3])).toBe(6);
});
it("returns 0 for an empty cart", () => {
  expect(calculateTotal([])).toBe(0);
});
```

### 6. Don't test the mock

A mock verifies the system under test calls its dependency correctly. Asserting on a value you set on the mock tests the mock framework.

```typescript
// bad
const db = { find: vi.fn().mockReturnValue(user) };
expect(db.find()).toEqual(user); // tests the mock, not the service

// good
const db = { find: vi.fn().mockReturnValue(user) };
const result = service.getUser(42);
expect(db.find).toHaveBeenCalledWith(42); // verifies the call
expect(result).toEqual(user); // verifies the transformation
```

### 7. Every test asserts at least one observable outcome

Observable means return value, thrown error, published event, written row, or sent message. A test that only calls code asserts nothing — rename it `smoke_*` and move it out of the unit suite. It does not count toward coverage.

### 8. No happy-path-only suites

For every public function, exercise at minimum one valid input, one boundary, one invalid, and one empty/null where applicable. Happy-path-only suites hit 100% coverage and miss every bug.

### 9. No copy-paste parameterized tests with identical assertions

Parameterized tests where every row asserts the same shape without exercising different paths are coverage padding.

```python
# bad
@pytest.mark.parametrize("x", [1, 2, 3, 4, 5])
def test_is_positive(x):
    assert is_positive(x) == True

# good
@pytest.mark.parametrize("x,expected", [
    (1, True), (0, False), (-1, False), (10**9, True),
])
def test_is_positive(x, expected):
    assert is_positive(x) == expected
```

### 10. A surviving mutant is a dummy test

Run mutation testing. Every surviving mutant is a test that happens to pass. Fix the test, not the mutant.

---

_Part of the [skill collection](../README.md)._