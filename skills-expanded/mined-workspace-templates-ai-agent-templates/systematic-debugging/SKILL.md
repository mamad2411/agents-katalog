---
name: systematic-debugging
description: Finds the root cause of a bug by reproducing it, isolating it and testing hypotheses before any fix. Use it when something fails and the cause is unclear.
---

# Systematic debugging

Do not edit production code until you can name the cause and show evidence for it.

## Steps

1. Restate the failure: expected result, actual result, exact error text. Ask for missing details only if you cannot proceed.
2. Reproduce it. Write the smallest command or failing test that triggers it, and run it. If it only fails sometimes, run it in a loop (`for i in $(seq 50); do ...; done`) and record the failure rate.
3. Isolate. Bisect the input, the config, or the history (`git bisect run <test command>`). Remove code and data until the failure disappears, then put back the last piece.
4. Write two or three hypotheses, each with a prediction: "if X is the cause, then logging Y at line Z will show W". Test the cheapest one first with a log line, a debugger breakpoint or an assertion. Never test two at once.
5. Confirm the root cause. Ask "why" until you reach the line or assumption that is wrong, not the place where it crashed.
6. Fix it with the smallest change. Keep the failing test from step 2 and see it pass. Run the nearby tests.
7. Remove all temporary logging.

## Rules

- Read the whole error, including the first frame in your own code and any "caused by" chain.
- Never wrap the failure in try/catch, add a retry or a sleep, or loosen an assertion to make it pass.
- If three hypotheses fail, stop and re-read the code you assumed was fine.

## Report

Cause in one sentence, the evidence, the fix with file and line, the test added, and anything related you noticed but did not change.
