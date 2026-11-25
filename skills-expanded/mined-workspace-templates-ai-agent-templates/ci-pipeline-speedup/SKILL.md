---
name: ci-pipeline-speedup
description: Measures where a CI pipeline spends its time, then cuts minutes with caching, parallel jobs and skipping work that did not change.
---

# CI pipeline speedup

Measure first. Optimize only the steps that dominate the run.

## Steps

1. Get timings for the last 10 to 20 runs of the main pipeline: the CI provider's CLI or API, or the run logs. Record per-job and per-step duration, and the median.
2. Rank steps by total time. Ignore anything under 5 percent of the run.
3. For each top step, find the cause: cold dependency install, rebuilt artifacts, a serial test suite, a large checkout, or an oversized image pull.
4. Apply the matching fix:
   - cache dependencies and build output, keyed on lockfile and config hashes
   - shallow checkout (`fetch-depth: 1`) unless history is needed
   - shard the test suite across parallel jobs and balance by past duration
   - path filters so docs-only changes skip the tests
   - run lint and unit tests before slow integration jobs, and cancel superseded runs
5. Re-run twice and compare the median to the baseline. A cache only shows its value on the second run.

## Rules

- Never remove a check, lower coverage or mark a flaky test as allowed-to-fail to save time. Quarantine it and report it.
- Keep a cache key specific enough that stale output cannot be restored.
- Change one thing at a time so each saving is attributable.

## Report

A table of step, before, after and change made, the new median run time, and any risk you accepted.
