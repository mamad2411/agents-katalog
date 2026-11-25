---
name: failing-test-first
description: Reproduce a bug with a failing test before fixing it, and keep the test in the suite. Use whenever asked to fix a bug, defect, regression, wrong output, or incorrect behavior in code.
---

# Failing Test First

A bugfix without a reproduction is a guess. Run this sequence in order —
do not fix first and backfill the test.

## Sequence

1. Locate the buggy behavior and read the code and its existing tests.
2. Write a test that reproduces the reported bug (expected correct
   behavior asserted, currently failing).
3. Run it and confirm it FAILS with the reported symptom. Paste the
   failure output. If it passes, the reproduction is wrong — stop and
   re-diagnose before touching the code.
4. Apply the smallest fix at the root cause.
5. Re-run: the new test and the full suite must pass. Paste the output.
6. Keep the reproduction test in the suite permanently — it is the
   regression guard, not scaffolding.

## Completion gate

The fix is not complete until a test that failed before the fix passes
after it. Report both runs (red, then green) as evidence.
