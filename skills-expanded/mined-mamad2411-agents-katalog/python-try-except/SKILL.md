---
name: python-try-except
description: Audit try/except blocks for overly broad scope, by-catch risk, and catches of built-in exceptions that should be conditional checks. Tightens each block so the try covers only the operation that can actually raise the expected exception.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: honnibal
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F50D"
    homepage: https://github.com/honnibal/claude-skills
---

# Interrogate Try/Except Usage

Read Python source files, find every `try/except` block, and evaluate whether each one is correctly scoped, catches the right exceptions, and doesn't mask bugs.

**Guiding principle:** try/except is for external state you cannot control (filesystem, network, concurrent access). For conditions over local values, use `if`, `in`, `hasattr`, or similar checks.

## Scope

- If the user names specific files or directories, scope work to those.
- For large codebases, ask the user which modules to start with.

## Workflow

1. **Find all try/except blocks.** Grep for `try:` across the files in scope.
2. **Classify each block.** Work through the analysis checklist below.
3. **Propose changes.** Explain the issue and show the fix. Apply edits.
4. **Verify.** Run the test suite after editing.

## Analysis Checklist

### 1. Is try/except the right mechanism?

Try/except is appropriate for:
- **External state** — filesystem, network, database, subprocess
- **Validation-as-parsing** — `json.loads()`, `int()`, `datetime.strptime()`, `pydantic.model_validate()`

Try/except is **not** appropriate for local value checks:
| Instead of catching... | Use this |
|------------------------|----------|
| `KeyError` on `d[key]` | `if key in d:` or `d.get(key)` |
| `AttributeError` on `x.y` | `if hasattr(x, "y"):` |
| `IndexError` on `lst[i]` | `if i < len(lst):` |

### 2. Is the try block minimally scoped?

The try block should contain only the operation that can raise the expected exception. Move setup statements above the `try`, processing after it (into `else` if appropriate).

### 3. Is the except clause too broad?

Rank from most to least dangerous: bare `except:` → `except Exception:` → tuple of types → specific type. Each caught type should have a clear justification.

### 4. Does the handler mask failure?

- `pass` — completely swallowed
- Returns default — caller can't distinguish success from failure
- Logs and continues — better, but still silences for the caller

### 5. Are there nested try/except blocks?

Often signals the outer block is too wide.

## Common Patterns to Flag

- `except KeyError` on dict access → use `.get()` or `if key in`
- `except AttributeError` on method call → use `hasattr()` or protocol
- `except TypeError` as type switch → use `isinstance()`
- `except Exception` in middle of logic → catch specific exceptions

## Critical Rules

- Read before editing. You need to understand what each statement in the try block does.
- Trace callees to know what exceptions they can raise.
- Don't remove error handling blindly — flag cases where narrowing might surface previously-silenced errors.
- Run tests after changes. Exception handling alters control flow.

## Cross-References

- `python-error-handling` — exception patterns, custom exceptions, logging
- `python-code-quality` — anti-patterns, bare except warnings
