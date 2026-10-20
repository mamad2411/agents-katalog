---
name: python-api-design
description: Designs intuitive Python library APIs following principles of simplicity, consistency, and discoverability. Handles API evolution, deprecation, breaking changes, and error handling. Use when designing new library APIs, reviewing existing APIs, or managing API versioning.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: wdm0006
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F3D7\uFE0F"
    homepage: https://github.com/wdm0006/python-skills
---

# Python API Design

## Core Principles

1. **Simplicity**: Simple things simple, complex things possible
2. **Consistency**: Similar operations work similarly
3. **Least Surprise**: Behave as users expect
4. **Discoverability**: Find via autocomplete and help

## Progressive Disclosure Pattern

```python
# Level 1: Simple functions
from mylib import encode, decode
result = encode(37.7749, -122.4194)

# Level 2: Configurable classes
from mylib import Encoder
encoder = Encoder(precision=15)

# Level 3: Low-level access
from mylib.internals import BitEncoder
```

## Naming Conventions

```python
# Actions: verbs
encode(), decode(), validate()

# Retrieval: get_*
get_user(), get_config()

# Boolean: is_*, has_*, can_*
is_valid(), has_permission()

# Conversion: to_*, from_*
to_dict(), from_json()
```

## Error Handling

```python
class MyLibError(Exception):
    """Base exception with helpful messages."""
    def __init__(self, message: str, *, hint: str = None):
        super().__init__(message)
        self.hint = hint
```

## Deprecation

```python
import warnings

def old_function():
    warnings.warn(
        "old_function() deprecated, use new_function()",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function()
```

## Anti-Patterns

```python
# Bad: Boolean trap
process(data, True, False, True)

# Good: Keyword arguments
process(data, validate=True, cache=False)

# Bad: Mutable default
def process(items: list = []):

# Good: None default
def process(items: list | None = None):
```

## Review Checklist

```
Naming:
- [ ] Clear, self-documenting names
- [ ] Consistent patterns throughout
- [ ] Boolean params read naturally

Parameters:
- [ ] Minimal required parameters
- [ ] Sensible defaults
- [ ] Keyword-only after positional clarity

Errors:
- [ ] Custom exceptions with context
- [ ] Helpful error messages
- [ ] Documented in docstrings
```

## Cross-References

- `python-documentation` — documenting APIs
- `python-error-handling` — custom exceptions
- `python-release-management` — deprecation, breaking changes
