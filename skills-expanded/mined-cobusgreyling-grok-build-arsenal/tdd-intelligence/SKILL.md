---
name: tdd-intelligence
description: |
  Apply rigorous test-first development. Write failing tests (or characterization tests)
  that capture desired behavior before implementing. Maintain high test coverage on changed code.
  Use for new features, refactors, and bug fixes where regression protection matters.
  Triggers: "TDD this", "test first", "write the test then implement", "add characterization tests".
version: 1.0.0
author: Cobus Greyling
---

# TDD Intelligence

True test-driven development with agentic discipline.

## Core Loop

1. **Understand the desired behavior** (read existing code, docs, issues).
2. **Write the smallest failing test** (or characterization test for legacy) that expresses the goal.
   - Run the test and confirm it fails for the right reason.
3. **Implement the minimal code** to make the test pass.
4. **Refactor** for cleanliness while keeping tests green.
5. **Add any additional edge-case or regression tests** suggested by the implementation.
6. **Verify** the full relevant test suite still passes.

## For Refactors and Legacy Code

- First write characterization tests that lock in current (even if imperfect) behavior.
- Then change implementation.
- Confirm the characterization tests still pass (proving behavior preservation).

## Rules

- Never implement before at least one relevant test exists and is failing appropriately.
- Prefer focused unit tests over broad integration tests for the core logic.
- When editing UI or complex flows, combine with `browser-qa` or manual verification steps.
- Update or add tests in the same diff as the feature when possible.

## Subagent Support

Use a subagent to:
- Explore the test surface area before writing tests.
- Generate additional edge cases after the happy path is implemented.

## Verification Commands

Always surface the actual commands the project uses:
- Python: `pytest ... -q --tb=short`
- Next.js: `npm test` or `vitest`
- Rust: `cargo test`

Discover these via the repo rather than assuming.

## Success Criteria
- The new/changed behavior is covered by tests that would have failed before the change.
- All tests in the affected area are green at the end.
- Diff size remains reasonable (tests + implementation together).

## Anti-Patterns
- Writing implementation then retrofitting tests.
- Skipping tests "because it's simple".
- Large untested refactors justified by "we'll add tests later".
