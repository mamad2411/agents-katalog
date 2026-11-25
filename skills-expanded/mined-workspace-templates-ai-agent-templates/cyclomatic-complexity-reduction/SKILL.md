---
name: cyclomatic-complexity-reduction
description: Flattens deeply nested conditionals with guard clauses, lookup tables and extraction, and proves with tests that the behavior did not change.
---

# Cyclomatic complexity reduction

Change the shape, never the behavior. Tests decide whether a step is allowed to stay.

## Steps

1. Find the target: the function the user named, or the worst offenders from the project's linter (`eslint --rule 'complexity: [error, 10]'`, `radon cc -s`, `gocyclo`, or similar). Record the current score.
2. Check for tests that reach every branch. If a branch is untested, write a characterization test for it first and see it pass on the unchanged code.
3. Apply these moves, one per commit-sized step, in this order:
   - Guard clauses: invert the condition and return or throw early, so the happy path sits at the lowest indentation.
   - Remove else after return.
   - Replace nested conditions on the same value with a lookup table or a map of handlers.
   - Name complicated boolean expressions by extracting them into predicates (`isEligibleForRefund`).
   - Extract the body of each remaining branch into a function when it exceeds about 8 lines.
   - Replace a repeated type switch with polymorphism only if it appears in three or more places.
4. Run the tests after each move. If one fails, undo that move and try a smaller one.
5. Recount complexity and confirm it fell.

## Rules

- Keep evaluation order and short-circuit behavior; a reordered condition can change which side effect runs.
- Do not merge branches that look alike but differ in a subtle way; flag them.
- No new dependencies and no renamed public functions.

## Report

Before and after complexity score, the moves applied, test results, and branches you left alone with the reason.
