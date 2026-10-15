---
name: analyze-tests
description: Test suite analysis. Use when asked to analyze, review, or evaluate a project's tests for quality, coverage gaps, and best practices.
---

# Test Suite Analysis

Perform a focused analysis of this project's test suite. Follow the procedural workflow
below; use the rubric sections as reference when interpreting findings.

## Usage

When asked to analyze test quality:

### 1. Run coverage

Establish baseline coverage (prefer lintro when available):

```bash
uv run lintro tst    # runs tests with coverage when configured
```

If lintro is unavailable, use the project's native test command with coverage
(`uv run pytest --cov`, `bun test --coverage`, `cargo llvm-cov`, etc.).

Note overall coverage percentage and files below threshold.

### 2. Find "nothing burger" tests

Search for tests that assert little or trivially pass:

```bash
# Empty or minimal assertions
rg -U 'def test_\w+.*\n(\s+pass|\s+assert True|\s+assert 1 == 1)' --type py

# Tests with no expect/assert (JS/TS)
rg -n 'it\(|test\(' --type ts --type js -A 5 | rg -B2 '^\s*\}\);?\s*$' 

# Placeholder / TODO tests
rg -n '(test_|it\(|describe\().*(skip|todo|pending|\.only)' -i
rg -n '@pytest\.mark\.skip|pytest\.skip\(' --type py
```

Flag tests that don't validate real behavior.

### 3. Find missing parametrization

Detect copy-paste test patterns with similar names:

```bash
# Similar test function names (Python)
rg -n 'def test_\w+_\w+_\d+' --type py
rg -n 'def test_(create|update|delete|get)_' --type py | sort

# Repeated it() blocks with numeric suffixes (JS/TS)
rg -n "it\('.*\d+'" --type ts --type js
```

When multiple tests differ only by input values, recommend `@pytest.mark.parametrize`
or table-driven equivalents.

### 4. Check isolation

Find shared mutable state and order-dependent tests:

```bash
# Module-level mutable state in test files
rg -n '^[A-Z_]+\s*=\s*\[\]|^[a-z_]+\s*=\s*\{\}' tests/ --type py
rg -n 'global |beforeAll|afterAll' tests/ -i

# Tests that modify shared fixtures or class state
rg -n 'self\.\w+\s*=' tests/ --type py
rg -n '@pytest\.fixture.*scope\s*=\s*["\x27]session' --type py
```

Verify tests are independent and deterministic.

### 5. Fixture reuse

Identify duplicated setup that should be shared:

```bash
rg -n '@pytest\.fixture|def setUp|beforeEach' tests/ --type py
rg -n 'def test_' -A 15 tests/ --type py | rg -c 'client\s*=|db\s*=|setup\s*=' 
```

Look for repeated boilerplate across tests in the same file.

### 6. Report gaps with specifics

For each finding, include:

- File path and test function name (e.g., `tests/test_auth.py::test_login_invalid`)
- Severity: **Critical** | **Should Fix** | **Nice to Have**
- Concrete improvement (add parametrization, assert on behavior, extract fixture, etc.)

Summarize coverage gaps: untested modules, missing edge cases, and integration points
without tests.

---

## Reference — Test Design & Quality

- Overall test structure and organization
- Adherence to testing best practices for the framework used
- Alignment with SOLID and DRY principles

## Reference — Problem Areas

- "Nothing burger" tests—tests that pass trivially or don't validate real behavior
- Missing parametrization where similar cases are tested with copy-paste
- Overly complex test code that's hard to maintain
- Large test files that should be split into logical groupings

## Reference — Test Hygiene

- Test isolation—do tests have side effects or depend on execution order?
- Flaky tests—tests that pass/fail inconsistently
- Mocking practices—appropriate use vs. over-mocking that hides real bugs
- Test naming—do names clearly describe the scenario and expected outcome?
- Setup/teardown—duplicated fixtures that should be shared
- Execution time—slow tests that could be optimized or parallelized

## Reference — Coverage Gaps

- Edge cases and failure modes not adequately tested
- Integration points lacking coverage
