---
name: hui-tdd
description: >
  Test-Driven Development discipline: RED-GREEN-REFACTOR. Write a failing test
  first, watch it fail for the right reason, write minimal code to pass, watch
  it pass, then refactor. Refuses to claim "done" until a test exists and passes.
  Trigger: /hui-tdd, "use tdd", "write the test first", "red green refactor".
---

# HUI TDD

Write tests first. RED → GREEN → REFACTOR. Never claim done until a test exists and passes.

## Cycle

1. **RED** — write one failing test for the next behavior. Run it. Confirm it fails for the RIGHT reason (assertion, not setup/compile error). State the observed failure.
2. **GREEN** — write the minimal code that makes the test pass. Run it. Confirm green. No extra features.
3. **REFACTOR** — improve structure with tests green after each change. Re-run if unsure.

## Rules

- Test before implementation. If implementation exists first, write the test that would have caught it and confirm it fails against the current code.
- Run the test; never claim it passes from reading. Report the exact command and observed output.
- One behavior per test. Name tests as sentences: `it_rejects_expired_token`.
- Minimal code to pass. No speculative generics, no future-proofing.
- If a test cannot be written (no test runner, infra missing): state that explicitly as Unknown/blocked. Do not claim the work is verified.

## Completion

A change is not done until:
- at least one test exists for the new/changed behavior,
- that test was run this session and observed passing,
- the command and outcome were reported.

If you wrote code before tests, do not delete it — but do not claim "done" or "works" until a test covers it and passes. State the gap explicitly: "Implementation done, test coverage pending."

## Anti-patterns

- Writing implementation, then writing a test that trivially passes against it.
- Claiming "tests pass" without running them this session — the `hui-guard` Stop hook blocks this.
- Skipping RED — if the test passes before any implementation, the test is wrong or redundant.

## Boundaries

Only shapes test discipline. Does not choose the test runner, add dependencies, or run builds. Pair with `hui-constraints` for evidence/verification rules. Trivial changes (typo, comment, config) are exempt.
