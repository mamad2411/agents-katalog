---
name: flaky-test-diagnosis
description: Reproduces an intermittent test failure, finds the shared state or timing cause and fixes it, rather than hiding it behind retries or longer waits.
---

# Flaky test diagnosis

A flaky test is a real bug in the test or the code. Never "fix" it with a retry, a longer timeout or a skip.

## Steps

1. Get the exact test name and one failing log. Note the runner and whether CI runs tests in parallel.
2. Measure. Run the single test 50 times in a loop and count failures. Then run the whole file, then the whole suite, and compare. Failing only in the suite points to shared state or ordering.
3. Force the suspected cause: run in random or reversed order, with one worker and with many, under CPU load (`stress-ng` or a busy loop), and with the clock frozen or shifted.
4. Classify the cause: leaked global or database state, real time or timezone, unawaited promise or thread, shared port or temp file, unseeded randomness, network call, or dependence on map or set ordering.
5. Fix the cause: isolate state per test, inject the clock, await the work, use ephemeral ports and unique temp dirs, seed the random generator and print the seed on failure, sort before asserting.
6. Rerun the 50-iteration loop. Done only at zero failures.

## Rules

- Never add sleeps. Wait on a condition or an event.
- Change one thing between measurements.
- If the production code is racy, say so and fix it there.

## Report

Failure rate before and after, the classified cause, the diff, and any sibling tests with the same pattern.
