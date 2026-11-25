---
name: tdd
description: Test-driven development workflow for implementing features or fixing bugs through red-green-refactor. Use when the user asks to build, change, or fix behavior and the codebase has a practical automated test surface.
---

# TDD

Use this skill to make behavior changes with a tight feedback loop.

## Workflow

1. Clarify behavior
   - Identify the user-visible behavior, input, output, and edge cases.
   - Find the smallest vertical slice that proves the behavior.
   - If the request is ambiguous, make a conservative assumption and state it.

2. Find the test seam
   - Prefer the seam closest to real behavior: integration, API, component, e2e, then unit.
   - Avoid tests that only assert implementation details.
   - If no useful seam exists, note that as design pressure and choose the best available signal.

3. Red
   - Write one failing test for the next slice.
   - Run only the narrowest relevant test command first.
   - Confirm the failure is for the expected reason.

4. Green
   - Implement the smallest change that passes the test.
   - Keep changes scoped to the behavior under test.
   - Do not refactor unrelated code during green.

5. Refactor
   - Improve clarity only after the test passes.
   - Preserve behavior and rerun the relevant tests.
   - Remove duplication only when it is real and local.

6. Expand
   - Add edge cases only after the core path works.
   - Repeat red-green-refactor for each slice.
   - Finish by running the broader relevant suite.

## Test Quality Rules

- A good test fails before the fix and passes after it.
- Test names should describe behavior, not implementation.
- Do not mock the thing being tested.
- Prefer fixtures over hand-built objects when local patterns already use fixtures.
- Keep assertions specific enough to catch the bug or behavior contract.

## Verification

- The new or changed test fails before the implementation when practical.
- The focused test command passes after the implementation.
- A broader relevant suite passes when the change touches shared behavior.
- Untested risk is named when broader validation is not practical.

## Completion Report

End with:

- Behavior implemented
- Tests added or changed
- Commands run
- Any untested risk
