---
name: training-debugging
description: Use when training diverges, produces NaNs, stalls, runs out of memory, shows inconsistent metrics, or otherwise behaves unexpectedly
---

# Training Debugging

Treat model failures like research incidents: isolate, measure, and prove the root cause before changing multiple things.

## First Pass

Reduce the problem:

- one machine if possible
- one seed
- smallest reproducible config
- shortest run that still shows the failure

## Failure Buckets

Classify the issue before fixing it:

1. data or labels
2. model forward path
3. loss or normalization
4. backward or optimizer
5. distributed/runtime/memory
6. evaluation/reporting

Read `references/failure-patterns.md` when you need concrete probes.

## Workflow

1. Reproduce the failure reliably.
2. Add instrumentation at the boundary most likely to be wrong.
3. Compare a good run and bad run at the earliest point they differ.
4. Change one variable at a time.
5. Fix the root cause.
6. Re-run the failing case and the baseline case.
7. Use `reproducibility-check` before saying the issue is fixed.

## Red Flags

- Raising gradient clip, epsilon, or warmup without evidence
- Changing model and data pipeline in the same debugging pass
- Looking only at final metrics instead of the first broken signal
- Calling an issue fixed after one lucky rerun
