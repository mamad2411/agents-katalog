---
name: test-and-verify
description: Use after implementing code to systematically verify behavior, tests, regressions, and important edge cases.
---

# Test and Verify

## Goal

Verify a completed coding change instead of assuming that a successful edit means the task is complete.

## Workflow

1. Inspect the diff.
2. Identify the behavior changed.
3. Find existing tests that cover it.
4. Add focused tests when coverage is missing and the task warrants them.
5. Run the narrowest useful test first.
6. Run broader checks when appropriate.
7. Inspect failures rather than hiding or weakening tests.
8. Check formatting, linting, types, and build status when relevant.
9. Report exactly what was run and what was not run.
10. Never claim a test passed unless it actually ran successfully.

## Final report

- Changed behavior
- Tests/checks executed
- Results
- Remaining risks
