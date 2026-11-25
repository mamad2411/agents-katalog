---
name: python-contract-docstrings
description: Write docstrings that document each function's contract — what it requires of callers, what it guarantees, and how it fails. Analyses input invariants, errors raised on violation, errors from external state, and silenced errors.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: honnibal
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://github.com/honnibal/claude-skills
---

# Contract Docstrings

Read Python source files, analyse each function's actual behaviour, and write docstrings that document the function's **contract** — what it demands and guarantees.

Most docstrings describe what a function *does*. These docstrings describe what a function *demands and guarantees*.

## Scope

- If the user names specific files or directories, scope work to those.
- Skip trivial functions (one-liners, simple property accessors, `__repr__`).

## Workflow

1. **Read deeply.** Trace every code path. Read callees. Read callers. Build a picture of real constraints.
2. **Analyse the contract.** For each function, answer the four questions in the analysis checklist.
3. **Write docstrings.** Add or replace docstrings using the format below.
4. **Verify.** Run the test suite and type checker after editing.

## Analysis Checklist

### 1. Input invariants (preconditions)

What must be true about the arguments for the function to behave correctly? Look beyond the type signature.

**Look at:** guard clauses, assertions, unhandled exception paths, implicit assumptions (iterating twice means it can't be a single-use iterator), relationships between arguments.

### 2. Errors raised on invariant violation

What happens when preconditions are violated?
- **Explicit check** — document the exception type.
- **Implicit fail** — `TypeError`, `KeyError`, `IndexError` from side effects.
- **Silently wrong** — most dangerous. Document if wrong input silently produces garbage.

### 3. Errors from external state

Filesystem, network, database, environment variables, global mutable state. For each, document what errors can result and whether they're handled.

### 4. Silenced errors

Exceptions caught and hidden: bare `except:`, `contextlib.suppress()`, `.get()` defaults masking missing keys, broad handlers that return defaults.

## Docstring Format

Use Google style. Contract sections go after any existing summary:

```python
def process_batch(items: list[Record], batch_size: int = 100) -> list[Result]:
    """Process records in batches and return aggregated results.

    Contract:
        Preconditions:
            - `items` must be non-empty. If empty, raises `ValueError`.
            - `batch_size` must be positive. If zero, raises
              `ZeroDivisionError` from chunking logic (implicit).

        Raises:
            ValueError: If `items` is empty (explicit guard).
            ConnectionError: If database is unreachable (from
                `db.write_results()`, not caught).

        Silences:
            - `OSError` during cache writes. Logs warning and continues.
            - `KeyError` from malformed records via `.get("type")` default.
    """
```

## Critical Rules

- Read before writing. Never write contract docstrings for code you haven't read thoroughly.
- Accuracy over completeness. If unsure, leave it out.
- Don't change behaviour. You are writing docstrings, not refactoring code.
- Trace callees. Don't assume what a function raises — read it.

## Cross-References

- `python-documentation` — Google-style docstring format, Sphinx
- `python-try-except` — auditing error handling
