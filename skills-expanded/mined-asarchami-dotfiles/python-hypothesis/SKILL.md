---
name: python-hypothesis
description: Generate property-based tests using Hypothesis. Builds input strategies in tests/strategies.py that model the valid search-space for each function, then writes minimal, behaviour-focused tests.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: honnibal
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F9EA"
    homepage: https://github.com/honnibal/claude-skills
---

# Property-Based Tests with Hypothesis

Read production code, design Hypothesis strategies that model the valid input space for each function, and write property-based tests that exercise core behavioural contracts.

## Scope

- If the user names specific files or directories, scope work to those.
- Prioritise modules with complex logic and no existing tests.

## Strategy Design (`tests/strategies.py`)

### Principles

1. **Start from the function, not the type.** Read the function body. Look for guards, assertions, early returns, conditional branches, and error paths.
2. **Encode constraints, don't filter.** Prefer `st.integers(min_value=1)` over `st.integers().filter(lambda x: x > 0)`.
3. **Mirror the production domain.** Use `st.builds()` and `@st.composite` to construct structured objects.
4. **Compose from small pieces.** Build reusable atomic strategies and compose them.
5. **`st.builds()` for simple constructors, `@st.composite` for everything else.**

```python
@st.composite
def valid_date_range(draw):
    start = draw(st.dates(min_value=date(2020, 1, 1)))
    end = draw(st.dates(min_value=start))
    return DateRange(start=start, end=end)
```

6. **Register strategies for your types.** `st.register_type_strategy(Task, st.builds(...))` so `st.from_type(MyType)` works automatically.

### Structure of `tests/strategies.py`

```python
"""Hypothesis strategies for <project name>."""
from hypothesis import strategies as st

# -- Atomic strategies (reused across composed strategies) --
# -- Composed / domain strategies (@st.composite for dependent fields) --
# -- Type registrations (so st.from_type(T) resolves automatically) --
```

## Test Design

### What to test

Core behavioural contracts:
- **Roundtrip / inverse:** `decode(encode(x)) == x`
- **Idempotence:** `f(f(x)) == f(x)`
- **Invariant preservation:** `len(merge(a, b)) <= len(a) + len(b)`
- **Equivalence to a reference:** `fast_path(x) == naive_impl(x)`

### What NOT to test

- Structural trivia (keys in output schema)
- Reimplementing the function
- Side effects of the current implementation
- Functions that are just glue

### Structure of test files

```python
"""Property-based tests for <module>."""
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from tests.strategies import <relevant strategies>
from mypackage.module import <functions under test>

class TestFunctionName:
    @given(...)
    def test_<property_name>(self, ...):
        ...
```

## Critical Rules

- Read before testing. Never write strategies for code you haven't read.
- Valid inputs only. Strategies must generate values the function is designed to handle.
- Strategies go in `tests/strategies.py`. Keep them separate from tests.
- Each test should assert one property. Don't bundle multiple checks.

## Cross-References

- `python-testing` — pytest patterns, fixtures, parametrization
- `python-mutation-testing` — test suite strength assessment
