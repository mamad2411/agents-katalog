---
name: stand-py
description: Python >= 3.11 coding standards. Use when writing Python code. Requires type hints, return types, Google-style docstrings, trailing commas, explicit kwargs, StrEnum with auto(), dataclasses, pytest-style tests.
---

# Python Code Standards

Standards for Python code (>= 3.11).

## Runtime

- All Python code should be run with `uv`

## PEP Compliance

- PEP 604: Use union types as `X | Y` (not `Union[X, Y]`)
- PEP 673: Use `Self` type for self-referential types

## Required Elements

- Type hints on ALL function parameters
- Return types on ALL functions
- Docstrings in Google Style Guide format for:
  - Modules
  - Classes
  - Functions/methods

## Docstring Format (Google Style)

```python
def function_with_docstring(
    param1: str,
    param2: int,
) -> bool:
    """Short description of function.

    Longer description if needed.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is wrong.
    """
```

## Design Patterns

- Use `dataclasses` for structured records with fixed fields and named attributes
- Use `collections.defaultdict` for dynamic key-value aggregation with automatic
  defaults
- Choose based on the use case: typed record-like object (`dataclass`) vs map with
  default values (`defaultdict`)
- Each dataclass should be in a separate file
- String Enums should use `StrEnum` with `auto()`
- Use `auto()` with all Enums where it makes sense

## Idioms

Prefer Python-native constructs over verbose cross-language patterns.

- `any()`/`all()` over flag-and-break loops:

  ```python
  # Don't
  found = False
  for p in paths:
      if p.exists():
          found = True
          break

  # Do
  found = any(p.exists() for p in paths)
  ```

- `dict.get()` over key-in checks:

  ```python
  # Don't
  if name in registry:
      return registry[name]
  return None

  # Do
  return registry.get(name)
  ```

- `pathlib` over `os.path` — never mix the two in one codebase:

  ```python
  # Don't
  root = os.path.dirname(os.path.dirname(os.path.dirname(path)))

  # Do
  root = Path(path).parents[2]
  ```

- Truthiness over length checks:

  ```python
  # Don't
  if len(items) == 0:
      ...

  # Do
  if not items:
      ...
  ```

- Comprehensions over loop-append for simple transforms:

  ```python
  # Don't
  names = []
  for user in users:
      names.append(user.name)

  # Do
  names = [user.name for user in users]
  ```

- Direct boolean returns:

  ```python
  # Don't
  if count > limit:
      return True
  return False

  # Do
  return count > limit
  ```

- `contextlib.suppress(SomeError)` over a `try`/`except SomeError: pass` block
- Reach for `itertools`/`functools` (`chain`, `pairwise`, `cache`, `reduce`) when
  they replace hand-rolled loop logic

## Formatting Rules

- More than 1 arg/param requires a trailing comma:

  ```python
  # Good
  def foo(bar: str, baz: int,) -> None:

  # Bad
  def foo(bar: str, baz: int) -> None:
  ```

- Be explicit with function calls when more than 1 arg:

  ```python
  # Good
  foo(bar=bar, baz=baz)

  # Bad
  foo(bar, baz)
  ```

- Single arg can be positional:

  ```python
  # OK
  foo(bar)
  ```

## Linting

Follow the `lint` skill for linting and formatting workflow.

## Ignoring Issues

Follow the `lint` skill ignore policy (Rules section): fix the root cause
first; if suppression is genuinely required, use the narrowest possible ignore
(specific rule code, single line) with an inline justification; blanket or
file-level ignores require a documented exception.

Python-specific: Bandit requires an **inline** `# nosec` or `# nosec BXXX - reason`
on the same line as the flagged statement (preceding-line `# nosec` is silently
ignored by Bandit). See the `lint` skill for other tool ignore configurations (e.g. mypy
may use a preceding-line comment plus inline `# type: ignore`):

```python
# Don't - blanket, unjustified ignore
subprocess.run(["validate.sh"])  # nosec

# Do - narrowest code, inline justification
subprocess.run(["validate.sh"])  # nosec B603 - fixed argv list; no shell
```

Additional Python-specific note: docstrings are required even for tests — no
exceptions.

## Testing (Pytest)

- NEVER use unittest style or test classes
- Use pytest-style test functions only
- Leverage `conftest.py` for shared fixtures
- Use fixtures for reusable setup/teardown
- Use `@pytest.mark.parametrize` to reduce duplication
- ALWAYS use `assertpy` for assertions — never bare `assert` statements.
  Keep `pytest.raises` for exception contexts (assertpy does not replace it)

```python
# Don't
assert result.count == 3
assert "drift" in output

# Do
from assertpy import assert_that

assert_that(result.count).is_equal_to(3)
assert_that(output).contains("drift")
```

```python
# WRONG
class TestFoo(unittest.TestCase):
    def test_bar(self):
        ...

# CORRECT
def test_foo_bar() -> None:
    """Verify foo handles bar correctly."""
    ...
```

### Wiring vs. Behavior

A test that asserts `field == "literal"` where `"literal"` is also defined in source
code is duplication, and produces silent drift the moment either side changes.

- **Wiring tests** (does X read from canonical Y) — source from the constant. Better
  still, ask whether the test is just restating the constant's value; if so, delete it.
  The codegen / source-of-truth machinery is what guarantees that wiring, not a
  per-consumer assertion.
- **Behavior tests** (does X meet a fixed external contract — protocol versions, public
  API shapes, business rules) — hardcode the literal. The literal _is_ the contract.
- **Fixture data and parser inputs** are not wiring — keep those literal. They represent
  the world being modeled, not internal state.

Parametrize IDs should describe the case under test (`attr=min_version`), never encode
mutable data values (`min_version_is_0.43.0`) — IDs that change with every dependency
bump are a smell.

### Parametrize ID Hygiene

```python
# WRONG — id encodes the data, churns on every bump
ids=["min_version_is_0.43.0"]

# CORRECT — id names the case
ids=["attr=min_version"]
```
