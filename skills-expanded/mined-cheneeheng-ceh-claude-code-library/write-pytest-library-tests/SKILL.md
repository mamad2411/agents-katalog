---
name: write-pytest-library-tests
description: >-
  Load this skill when writing pytest tests for a Python library: unit tests, public-API tests,
  fixtures, and what to mock versus test for real. Auto-load when a test file is created or
  modified.
disable-model-invocation: false
user-invocable: false
paths:
  - "**/test_*.py"
  - "**/*_test.py"
  - "**/tests/**"
  - "**/conftest.py"
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI on first
  sync. `pytest` and its plugins are not assumed to be installed globally - `uv sync` installs
  them into the project environment and tests run via `uv run pytest`.
license: Apache-2.0
---

# Write pytest Tests for a Library

Framework: **pytest** with **pytest-asyncio** (`asyncio_mode = "auto"` in `pyproject.toml`)

Write library tests against the public API at the lowest tier that can show the behavior, with no
I/O. Done when each test asserts one behavior and the suite touches no network or filesystem.

## Procedure

1. Choose the inputs and scenarios first (see Hands off to).
2. Put each test in `tests/unit/` or `tests/api/` by whether it reaches private modules or imports the
   package as a consumer would.
3. Mock external boundaries only, never the code under test.
4. Run coverage and read the untested regions. Never add a test just to reach the floor.

## Rules

### Test structure

```
your_library/
└── tests/
    ├── unit/         # Isolated — no I/O, mock all external dependencies
    ├── api/          # Exercise the public package API as a consumer would import it
    └── conftest.py   # Shared fixtures and mock factories
```

Test files mirror source structure. Naming: `test_<what>_<expected_behavior>.py`. One logical behavior per test.

Test against the public API surface (`import your_library`), not private modules — tests that reach
into `_private` internals lock in implementation details and break on every refactor.

### Unit tests: no I/O

```python
class TestRetryPolicy:
    def test_backoff_grows_exponentially(self):
        policy = RetryPolicy(base=1.0, factor=2.0)
        assert [policy.delay(n) for n in range(3)] == [1.0, 2.0, 4.0]
```

### Public API tests: import as a consumer

```python
import your_library


def test_public_entry_point_is_importable():
    assert callable(your_library.parse_duration)
    assert your_library.parse_duration("1h") == timedelta(hours=1)
```

### Mocking rules

- Mock external HTTP services and clock/filesystem at the boundary; never mock the code under test.
- Use `unittest.mock` or `pytest-mock`.
- Prefer real objects over mocks when construction is cheap.

### Coverage floor

A floor for finding blind spots, not a goal. Below the number, look for the untested regions.
Reaching it proves nothing and is never a reason to add tests.

| Area                                  | Floor |
| ------------------------------------- | ----- |
| Library package                       | 80%   |
| Public API and core logic             | 95%   |

```bash
uv run pytest --cov=your_library --cov-report=term-missing
```

## Hands off to

This skill covers the **tooling** — runner, fixtures, mocking, coverage. It does not decide
_which_ inputs and cases a test should cover. Before writing the cases:

- Invoke the Skill tool with skill="ceh-testing:design-test-cases" to choose them. It supplies
  equivalence partitions, boundary values, decision tables, pairwise combinations, properties, and
  metamorphic relations — stack-agnostic technique that the sections above assume has already been
  applied.
