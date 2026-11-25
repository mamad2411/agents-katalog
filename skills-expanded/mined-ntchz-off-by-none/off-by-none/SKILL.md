---
name: off-by-none
description: Use when implementing or fixing code against a written spec, requirements doc, or ticket — especially under time pressure, "quick fix" or "minimal change" requests, or when about to declare work ready to ship.
---

# Spec-Faithful Implementation with Independent Verification

## Overview

Self-written tests inherit the same misreading as your implementation, so they pass while the code is wrong. This skill forces test cases to be derived from the spec's literal wording BEFORE implementing, with mandatory boundary-value coverage.

**Core principle: a test derived from your implementation verifies nothing. Derive every test from the spec's exact words.**

## Workflow

1. **Requirements ledger.** Number every clause of the spec, including sub-clauses hidden inside sentences ("then re-apply rule 6" is its own entry). One checklist item per clause.

2. **Derive tests from the spec text — before writing any implementation code.**
   - For every clause, write at least one case using only the spec's wording, not your planned code.
   - **Boundary rule (mandatory):** every numeric limit or boundary word — "at", "at or before", "exceeds", "up to", "at least", "within" — gets three cases: exactly N-1, exactly N, exactly N+1. Compute the expected outputs by hand from the spec sentence, character by character if needed.
   - **Boundary words bind to what they modify.** "At or before max_len" about a *position* (a delimiter, a marker, a match) requires a test where that thing sits exactly AT position max_len — a test where only the total *length* is at the limit does not cover it. For each boundary phrase, name the noun it modifies (length? index? count? position?) and put the test exactly there.
   - For every "if/when/unless" clause, one case per branch.

3. **Implement.**

4. **Run the tests. Paste actual output.** "I verified" without shown output is not verification.

5. **Adversarial re-read.** Go back to the spec, clause by clause, and for each ask: "is there an input where another literal reading of this sentence gives a different answer than my code?" Ambiguity between two readings = write a test for both readings and pick the one the spec's words actually say.

6. **Claim done only with evidence.** The final report has three REQUIRED sections (write "none" explicitly when empty):
   - **Verified:** the ledger with every item checked + pasted test output.
   - **Assumed:** every spec reference you could not inspect — external systems, config values, "same as X", "matching the existing behavior of Y". One line each. An unverifiable reference makes the ship claim conditional: state what must be confirmed, never an unqualified "ready to ship".
   - **Seen but not touched:** anything broken or suspicious in the code you worked around, outside the requested change. Before writing this section, re-read every function in every file you edited, including the ones you didn't change. For each untouched function, state what it literally does to its input step by step (especially any transformation that happens before a check) — observations only. Never write a verdict like "works correctly" on code you did not spec-test; you have no evidence for it. Report; do not fix. "None" means "I read the surrounding code and found nothing", never "I didn't look". "Minimal change" limits the diff, not the report.

## Quick Reference

| Spec wording | Required test cases |
|---|---|
| "exceeds N" / "up to N" | length N-1, N, N+1 |
| "at or before X" | exactly at X, one before X, one after X |
| "if A, do B" | A true, A false |
| "then re-apply rule K" | case where skipping rule K would show |
| empty/none mentioned | empty input, no-valid-content input |

## Common Mistakes

| Mistake | Reality |
|---|---|
| "I tested it with ~10 cases, all pass" | Cases generated from your own code's logic test your logic, not the spec. |
| "Time pressure — skip the ledger" | The ledger takes 1 minute. A shipped off-by-one costs a rollback. |
| "The boundary case is obvious" | Both baseline failures in testing this skill were exact-boundary off-by-ones that the author's own tests missed. Hand-compute expected values at the boundary. |
| "Minimal change was requested, so minimal checking" | Minimal change refers to the diff, not the verification. |
| "Spec says 'same rounding as the billing system' — that's ROUND_HALF_EVEN, done" | A reference to a system you cannot see is an assumption, not a fact. Label it in **Assumed** and make the ship claim conditional on confirming it. |
| "The other function's bug is out of scope, so don't mention it" | Out of scope to FIX, never out of scope to REPORT. It goes in **Seen but not touched**. |

## Red Flags — STOP

- About to write "ready to ship" without pasted test output
- No test case sits exactly AT a numeric limit from the spec
- Expected values in tests were copied from your function's output
- You read the spec once, at the start, and never re-read it after implementing
- "Ready to ship" while the spec references a system, module, or config value you never inspected
- A checked checklist item you never actually ran
- Your report is missing the **Assumed** or **Seen but not touched** section entirely
