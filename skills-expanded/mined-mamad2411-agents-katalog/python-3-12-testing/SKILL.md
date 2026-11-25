---
name: python-3-12-testing
description: Helps agents design, run, and repair Python 3.12 tests using pytest or standard-library unittest while preserving deterministic behavior.
---
# Python 3.12 Testing

Use this skill when adding tests, repairing failing tests, increasing coverage, validating bug fixes, or designing test strategy for Python 3.12 code.

## Testing Principles

- Test observable behavior, not implementation details.
- Add regression tests for bug fixes.
- Prefer deterministic tests with explicit inputs and expected outputs.
- Isolate external dependencies: network, file system, clock, random values, subprocesses, databases, and third-party APIs.
- Use temporary directories and fixtures for file work.
- Keep tests readable and close to the behavior being tested.
- Avoid test-order dependencies and hidden global state.

## Tool Selection

- If the project uses `pytest`, follow existing pytest patterns.
- If the project uses `unittest`, preserve it unless the user requests migration.
- If no test tool exists, recommend pytest for most projects but avoid adding it without approval when scope is limited.

## Workflow

Use `workflows/test-repair-workflow.md` when tests fail or behavior needs regression coverage.

## Examples

Use `examples/pytest-patterns.md` for common pytest patterns.

## Test Command Discovery

Look for commands in this order:

1. Project README or developer docs.
2. `pyproject.toml` tool configuration.
3. Existing CI config.
4. Existing Makefile or task runner.
5. Common fallback:

```bash
python -m pytest
```

or:

```bash
python -m unittest
```

## Completion Checklist

* Tests cover new or changed behavior.
* Edge cases and failure paths are included.
* Test data is minimal and readable.
* External systems are isolated.
* Tests run under Python 3.12 or the exact command is documented.
