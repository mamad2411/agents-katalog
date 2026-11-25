---
name: coverage-gap
description: Review a diff for missing test coverage; pairs every changed behavior with an existing test or a flagged gap plus a recommended layer; finds gaps, not authoring (unit-tests).
---

# coverage-gap

> Read a code diff plus the existing test files and report which changed behaviors are unprotected. Pair-mode for `code-review` in workflows.

## When to use

- Workflow step before merging a PR (`reviewPR` invokes this as a fanout sibling).
- The user asks "what tests am I missing?".
- After `feature-dev` to verify the TDD loop actually covered everything.

## Inputs

- The diff (current `git diff` or PR diff).
- Test directories conventional for the repo.

## Procedure

1. For each changed function / method / endpoint in the diff:
   a. Search the test directories for any test that imports or calls the symbol.
   b. Search for tests whose name matches the changed behavior.
2. For each "behavior" — defined as a new branch, condition, error path, or boundary case introduced by the diff — record whether a test would fail if that branch were broken.
3. Classify gaps:
   - **MISSING (unit):** pure logic uncovered.
   - **MISSING (integration):** boundary crossing uncovered.
   - **WEAK:** test exists but only asserts a return type, not the behavior.
4. Surface coverage % only if the repo already runs a coverage tool; do not invent numbers.

## Output

```text
Coverage gaps for <branch>:

Covered:
  - <file>:<line> <symbol>  → tests/<path>:<line>

MISSING (unit):
  - <file>:<line> rate_limit_burst_threshold has no test for the boundary case (6th request within 60s).

MISSING (integration):
  - <file>:<line> /healthz response shape is asserted nowhere.

WEAK:
  - <file>:<line> refund_amount: only return type asserted; behavior un-checked.

Test scaffolding (suggested):
  - tests/test_rate_limit.py::test_blocks_sixth_request_in_window
  - tests/test_healthz.py::test_returns_status_ok_with_version
```

## Quality bar

- Every "MISSING" item nominates a concrete test name.
- Never claim full coverage just because some test exists touching the changed file.
- Don't propose tests for code paths the diff doesn't introduce.
