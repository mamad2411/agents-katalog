---
name: tdd
description: >-
  Canon test-driven development (specify, encode, fulfill) for the host project's
  test framework. Clarify specifications, one failing test at a time, minimal
  code to green, approval gates, kitchen-cleaning refactor when needed. Use for
  TDD, specify-encode-fulfill, or red-green-refactor sessions.
user-invocable: false
---
# Test-driven development

## Role

You guide a **specify → encode → fulfill** session (Canon TDD): turn agreed specifications into executable tests one at a time, then write only enough production code to make the current failure go away. The user approves each test and each behavior commit. You do not batch-write tests or ship with a dirty test suite.

## When to use

Use when the user invokes `/tdd` with a draft behavior specification. For broad test coverage without the red-green loop, use `write-unit-tests`. For full feature delivery from a requirement, use `requirement-to-implementation`. For fixing a broken suite without new behavior, use `run-all-tests-and-fix`.

## Initial specification

Take the **initial specification** from the user's message (draft scenarios, examples, or file references). If missing, ask one focused question before proceeding.

## Specify-encode-fulfill

At session level:

1. **Specify**: agree what to build as concrete scenarios.
2. **Encode**: turn each scenario into one automated test (executable specification).
3. **Fulfill**: write production code so the current test passes.

At fine grain (repeat until the specification list is empty):

1. Maintain a numbered **specification list** for this session.
2. **Encode** exactly **one test** per cycle: one list item as a failing automated test.
3. **Fulfill** with code *just barely enough* to make that failure go away, no speculative coding.
4. **Commit the behavior change** before any refactor; never mix behavior changes with refactoring in one commit.
5. Optionally refactor after the behavior commit, with user approval.
6. Return to step 2 for the next list item.

Reference: [Canon TDD](https://tidyfirst.substack.com/p/canon-tdd) (Kent Beck).

## Clarifying specifications

Before writing tests:

1. Repeat the specifications in your own words (scenario form: **under scenario A, X happens; under scenario B, Y happens**).
2. Ask the user to confirm or correct.
3. If confirmed, proceed; otherwise revise and repeat from step 1.

## Encoding tests (framework-agnostic)

- Map each scenario to a named example or case in the host project's test framework (e.g. nested group + single case).
- Assert **what** the correct behavior is, never "works correctly", "works properly", or vague "handles" without stating expected outcomes.
- One behavior per test case where possible.
- Use the host repo's test style (imports, factories, matchers). Detect from existing tests or project docs.
- For **RSpec** hosts, see [appendix-rspec-examples.md](appendix-rspec-examples.md).

## Cleaning the kitchen

Before writing the next test:

1. Picture where the test will live in the test tree and where production code will change.
2. If the new behavior does not fit the current conceptual model, propose a **restructuring refactor** (new branch, clean working state, refactor only, then pause).
3. If the user approves, abandon the current behavior change until the kitchen is clean, then restart this loop from clarified specifications.

Do not add behavior on top of a muddled structure when a small refactor would clarify the design.

## Pre-existing failures (kitchen rule)

If the test suite has **pre-existing failures** unrelated to the current change:

- **Stop** the TDD session.
- Stash or park work, fix the pre-existing failure on a clean baseline, then resume.
- Do not commit or push while justifying unrelated reds ("our new specs pass").

## Fulfilling specifications

- Write **only enough** production code to clear the **current** test failure.
- Avoid defensive or speculative code not required by the current test.
- After the test is approved and written, run the **inline test review** (below).
- After code is written, run the **inline code review** (below).
- Show the test, wait for **approval**, then show code, wait for **approval** before commit.

## Inline light review

Replace separate design-review commands in v1.

**After the test:**

- Scenario is visible in the test name or structure
- Assertion states expected outcome, not vague correctness
- One focused behavior; no extra cases in the same commit

**After the production code:**

- Diff is minimal relative to the test
- No unused paths or defensive branches without test pressure
- Matches host patterns in neighboring code

## Workflow summary

1. User provides draft specification via `/tdd`.
2. Clarify until specifications are confirmed.
3. Check kitchen (conceptual fit; pre-existing failures).
4. Write **one** failing test → user approves.
5. Minimal green code → inline reviews → user approves commit.
6. Repeat from step 4 or add specifications and continue.

## Safety

- Commits and pushes only when the user approves.
- No force-push to protected branches unless the user explicitly requests it in line with their git rules.
- Run the host project's test command for affected paths (from README, Makefile, or existing CI).

## Distinction from other commands

- **`write-unit-tests`**: add tests for existing code, not the one-test Canon loop.
- **`requirement-to-implementation`**: plan and implement a requirement end-to-end, not per-test approval TDD.
- **`run-all-tests-and-fix`**: restore a green suite, not specify-encode-fulfill for new behavior.
- **`refactor-code`**: behavior-preserving refactor; in TDD, refactor only after a behavior commit.

## Guardrails

- Encode one test per cycle and write only enough code to pass it; never batch tests or add speculative code.
- Assert concrete expected outcomes, never "works correctly" or "handles properly".
- Keep behavior commits clean: do not commit with unrelated pre-existing failures, and do not mix refactoring into a behavior commit.
- Commit and push only with the user's approval; no force-push to protected branches unless the user explicitly requests it.
