---
name: tdd-cycle
description: "Use when implementing any behavior change - before writing production code. Defines the red-green-refactor cycle, how Gherkin scenarios map to tests, the coverage non-regression baseline, and the lint/test quality gate. Keywords: TDD, red green refactor, failing test, coverage baseline, make test, make lint."
---

# TDD cycle

Behavior changes follow Red -> Green -> Refactor. Tests are written or
confirmed failing before production code exists, and the task's Gherkin
scenarios are the primary source for test cases.

## Red

- Derive one test per observable behavior from the task file's acceptance
  criteria: every scenario must be realized as at least one automated test
  (a BDD test if the repo's BDD tooling is active, an equivalent pytest
  otherwise).
- Run the new tests and verify each fails for the expected reason (missing
  behavior, `NotImplementedError`, `AttributeError` on a not-yet-built API) -
  not for an unrelated error like a typo or import failure.
- If a test passes before any production code exists, it is not specifying
  new behavior - fix the test; never weaken the assertion.
- For previously untested existing behavior, write characterization tests
  first (see the `characterization-tests` skill).

## Green

- Write the minimum production code that makes the failing tests pass.
- Keep changes strictly inside the approved requirement scope.

## Refactor

- Clean up with tests green. Do not change observable behavior.

## Quality gate

- Run `make lint && make test` before finishing; both must pass.
- If the task's story/scenarios and the referenced requirements have drifted
  apart, STOP - never implement from the story side of a discrepancy. Route
  it back through a requirements or task-drafting round first.

## Coverage non-regression

- The task-start coverage baseline is recorded by running `make test`
  immediately before implementation starts - after the requirements and
  task-file commits are merged - so it measures the code state
  implementation departs from.
- At completion, total coverage must be equal to or higher than the
  baseline. If it dropped, add tests to recover it before marking the task
  done.
