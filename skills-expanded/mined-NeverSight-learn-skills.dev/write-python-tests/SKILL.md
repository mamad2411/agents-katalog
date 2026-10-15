---
name: write-python-tests
description: Write or refresh tests for Python projects. Use when Codex needs to add coverage, replace stale tests, reorganize tests under `tests/`, or lock down Python behavior from source code in repos that use `nox`, `pytest`, and `mise`.
---

# Write Python Tests

## Guidelines

- files to update: `tests/`
- Ensure tests are comprehensive and coverage is good.
- Existing docs, docstrings, tests, examples may be rough, missing, incomplete or misleading, it only serves as weak hint.
- Favor bold, comprehensive rewrites over minor or incremental edits.
- Group tests into files and folders, keep test files small and focused.
- Source code is the source of truth.
- Use `nox` to run full test suites.
- Use `pytest` for targeted test runs and debugging.

## Validation

- Run `mise run lint`.
- Start with the narrowest relevant target.
- Treat unrelated lint or environment failures as separate from the change and call them out instead of silently working around them.
