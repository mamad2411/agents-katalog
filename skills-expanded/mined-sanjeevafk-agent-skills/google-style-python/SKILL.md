---
name: google-style-python
description: >
  Apply Google's official Python style guide when writing, reviewing,
  formatting, or linting Python code. Use this skill whenever the user
  asks to review Python code for style, wants to know how Google formats
  Python, asks about docstring format, import ordering, type annotations,
  naming conventions, or whether something is idiomatic Python by Google
  standards. Also triggers on: "is this good Python?", "clean up this
  Python file", "how should I name this variable/function/class in Python?",
  "does this follow PEP 8 / Google style?", "how do I write a docstring?",
  or any request involving pylint, pyink, or Black in a Google-style context.
---

# Google Python Style Guide

Google's Python style guide is one of the most widely adopted in the industry.
It builds on PEP 8 but makes specific, opinionated choices — notably mandating
type annotations, prescribing a detailed docstring format, and discouraging
several "power features" of the language in favour of readability.

---

## Key Rules at a Glance

### Language rules
- **Imports**: Use `import x` for modules, `from x import y` for modules (not for types/classes/functions). Always use full package paths — no relative imports.
- **Exceptions**: Never use bare `except:`. Never catch `Exception` broadly unless re-raising or at an explicit isolation boundary.
- **Comprehensions**: Allowed for simple cases; no multiple `for` clauses or deeply nested filter expressions.
- **Global state**: Avoid mutable module-level globals. Constants are fine (ALL_CAPS).
- **Lambda**: Use only for simple, one-expression cases. Prefer named functions for anything complex.
- **Type annotations**: Required for all public API functions. Use `from __future__ import annotations` at the top for forward references.

### Style rules
- **Line length**: 80 characters maximum.
- **Indentation**: 4 spaces. No tabs.
- **Semicolons**: Never.
- **Imports ordering**: stdlib → third-party → local, each block alphabetical, separated by a blank line.
- **String quotes**: Use double quotes `"` consistently; single quotes acceptable but pick one per file.
- **f-strings**: Preferred over `.format()` and `%` formatting for Python 3.6+.

### Naming conventions
| Category | Style | Example |
|---|---|---|
| Modules & packages | `snake_case` | `my_module` |
| Classes | `CapWords` | `MyClass` |
| Functions & methods | `snake_case` | `compute_value()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private attrs | leading `_` | `_internal_cache` |
| "Protected" methods | leading `_` | `_helper()` |
| Type variables | CapWords or single letter | `T`, `AnyStr` |

### Docstring format (Google style)
```python
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch JSON data from the given URL.

    Args:
        url: The endpoint to request.
        timeout: Request timeout in seconds.

    Returns:
        A dict parsed from the JSON response.

    Raises:
        RequestError: If the request fails after retries.
    """
```

---

## Mode: Reviewing Python Code

When asked to review code for Google style compliance, work through:

1. **Imports** — correct ordering? `from x import y` of modules only? Full package paths?
2. **Naming** — correct case for each category above? No single-letter names outside loops?
3. **Type annotations** — all public functions annotated? Return type present?
4. **Docstrings** — present on all public functions/classes? Following Google format (Args/Returns/Raises)?
5. **Line length** — any lines > 80 chars?
6. **Exception handling** — any bare `except:` or overly broad catches?
7. **Comprehensions** — any overly complex comprehensions with multiple `for` clauses?
8. **Global state** — any mutable module-level variables that should be constants or class attrs?

For each issue found:
- Cite the rule by section (e.g. "§2.2 Imports")
- Show the problematic snippet
- Show the corrected version

---

## Mode: Writing New Python Code

When writing new Python following Google style:

1. Start with `from __future__ import annotations` if using forward references.
2. Order imports: stdlib → third-party → local (blank line between groups).
3. Write docstrings for every module, class, and public function — use Args/Returns/Raises sections.
4. Add type annotations to all function signatures.
5. Use 4-space indentation, 80-char line limit.
6. Name things according to the table above.
7. Prefer `with` statements for resource management (files, locks).
8. Avoid mutable default arguments (`def f(x=[])` — use `None` sentinel instead).

---

## When to Load the Full Guide

Load `references/full_guide.md` when:
- The user asks about a specific rule you're not sure about
- Doing a comprehensive review of an entire file
- Questions about specific sections: §2 (language rules), §3 (style rules), §4 (type annotations)

The full guide is ~3,700 lines — search for section headings like `## 2.4 Exceptions` or `## 3.16 Naming` to jump to the relevant part.

**Also see**: `google-style-common` for cross-language naming and comment philosophy.
