---
name: python-mutation-testing
description: Assess test suite strength by introducing deliberate bugs (mutations) one at a time and checking whether any test catches each one. Reports on test suite gaps and optionally implements missing tests.
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

# Mutation Testing

Assess the strength of the project's test suite by introducing deliberate bugs (mutations) into the source code, one at a time, and checking whether any test fails. A mutation that the tests don't catch reveals a gap in coverage.

## Scope

- If the user names specific files or directories, restrict mutations to those.
- Only mutate production code, never test files.
- Prioritise code with meaningful logic (branching, arithmetic, state changes).

## Pre-flight

1. **Clean working tree.** Run `git status`. If there are uncommitted changes, ask the user to commit or stash first.
2. **Find the test runner.** Look for `pytest.ini`, `pyproject.toml [tool.pytest]`, or a `tests/` directory. Confirm the suite passes before starting.
3. **Map the code.** Read the files in scope. Build a mental model of data flow.

## Workflow

1. **Choose mutations.** Read the file and identify 3–8 candidate mutations from the catalogue below.
2. **Apply, test, revert.** For each mutation:
   a. Apply the mutation using a single-line change.
   b. Run the test suite.
   c. Record the result: **Killed** (a test failed) or **Survived** (no test failed).
   d. Revert the mutation with `git checkout -- <file>`.

## Mutation Catalogue

1. **Delete or skip a side effect** — remove an assignment, method call, append.
2. **Negate or invert a condition** — `if x` → `if not x`, `and` → `or`.
3. **Change a boundary** — `<` → `<=`, `>=` → `>`, `== 0` → `== 1`.
4. **Swap or hardcode a return value** — `return score` → `return 0`.
5. **Delete an early return or guard clause** — remove `if not items: return []`.
6. **Change an operator** — `+` → `-`, `*` → `/`.
7. **Modify a default argument or constant** — change a default parameter value.
8. **Swap argument order** — reverse arguments in a non-commutative call.

## Assessing test failures

Rate diagnostic quality:
- **Clear** — test name and failure message immediately point to the bug.
- **Indirect** — failure describes a symptom rather than root cause.
- **Cascading** — many tests failed, making it hard to locate the root cause.

## Reporting

Produce a summary table:

```
| # | File | Mutation | Result | Diagnostic | Notes |
|---|------|----------|--------|------------|-------|
```

Then provide:
1. **Mutation score**: killed / total (e.g. 6/8 = 75%)
2. **Uncaught mutations**: list each survived mutation with explanation
3. **Diagnostic quality**: note indirect/cascading failures
4. **Recommended tests**: for each survived mutation, describe a test that would catch it

## Critical Rules

- Always revert after every test run. Never stack mutations.
- Don't mutate test files, imports, type annotations, or docstrings.
- 3–8 mutations per file is enough. Quality over quantity.

## Cross-References

- `python-testing` — pytest patterns, coverage
- `python-hypothesis` — property-based testing
