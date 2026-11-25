---
name: test-coverage-gap-analysis
description: Reads the coverage report, ranks uncovered branches by risk and writes meaningful tests for the top gaps instead of chasing a percentage.
---

# Test coverage gap analysis

Spend tests where a failure would hurt, not where the percentage is cheapest.

## Steps

1. Generate branch coverage with the project's own tool (`jest --coverage`, `pytest --cov --cov-branch`, `go test -coverprofile`, JaCoCo). Prefer machine-readable output (lcov, JSON, XML).
2. List uncovered files and branches. Add two signals: recent churn (`git log --since=6.months --name-only` counts) and how critical the path is.
3. Rank the top 10 gaps. Weight highest: authorization checks, money and quantity math, data writes and deletes, input validation, error handling and retries, parsing of external data. Weight lowest: logging, getters, generated code, trivial wrappers.
4. For each of the top gaps, write a test that asserts an outcome. Cover the failing branch with a concrete input, not a call that merely executes the line.
5. Rerun coverage and confirm the branch moved. If a test raises coverage but would still pass after you break the code, delete it.
6. Mark code that should not be tested (dead code, generated files) and propose removal or an exclusion with a comment.

## Rules

- Never add assertions like "does not throw" as the only check.
- Never lower a threshold or add ignore pragmas to hit a number.
- One test per behavior, named after it.

## Report

A table of the ranked gaps with the risk reason, the tests written, branch coverage before and after, and the gaps left open.
