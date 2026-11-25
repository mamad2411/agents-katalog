---
name: tdd-workflow
description: Builds a feature in small red, green, refactor cycles, with one failing test first and one commit per cycle, so every step stays verified.
---

# TDD workflow

Write a failing test, make it pass, clean up, commit. Repeat in small steps.

## Steps

1. Restate the feature as a list of behaviors, smallest first, in plain sentences. Show the list and start at the top. Find the project's test command and run it once to confirm the suite is green before you begin.
2. Red: write one test for the next behavior only. Name it as a sentence ("rejects an order with no items"). Run it. It must fail, and for the right reason: an assertion, not a typo or import error. If it passes, the behavior already exists; skip to the next.
3. Green: write the simplest code that passes, even if it looks naive (a hard-coded return is allowed for the first test). Run the whole suite.
4. Refactor: with all tests green, remove duplication, improve names and extract functions. Run the suite after each change. Do not add behavior here.
5. Commit with a message that states the behavior: `Reject orders with no items`.
6. Pick the next behavior. Prefer cases that force the code to generalize: another example, an edge, an error.
7. Stop when the list is done, then run lint and types, and review the tests for gaps: boundaries, invalid input, failure paths.

## Rules

- Never write production code without a failing test that requires it.
- Never edit a test to make it pass unless the requirement changed, and say so.
- If one cycle takes more than about ten minutes, the step is too big. Split it.
- Test behavior through the public interface, not private functions.

## Report

The behavior list with a checkmark each, the commits made, and any case you chose not to test.
