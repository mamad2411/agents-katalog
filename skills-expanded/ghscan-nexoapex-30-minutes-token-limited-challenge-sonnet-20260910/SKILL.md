---
name: flaky-test-finder
description: Diagnose and fix a flaky/intermittently-failing test. Use when the user mentions "flaky test", "intermittent failure", "passes locally but fails in CI", or "test fails randomly".
---

# Flaky Test Finder

Flaky tests almost always have a real, non-random cause. Treat "flaky" as a
label for "cause not yet found," not as an acceptable diagnosis.

## Steps

1. Run the test in isolation, then in the full suite, then repeated in a tight
   loop (10-20x) — note which condition reproduces the failure. If none do,
   check for CI-specific factors: parallelism, timing, resource limits.
2. Look for the usual root causes, in order of likelihood:
   - Shared mutable state between tests (module-level variables, a shared
     database/fixture not reset between runs, test execution order dependency).
   - Real timing/race conditions (async code without proper awaiting, a
     `setTimeout`/sleep used to "wait long enough").
   - Non-deterministic input (relying on `Date.now()`, random values, or
     external network calls without mocking).
   - Resource exhaustion under parallel test runs (port conflicts, connection
     pool limits).
3. Reproduce the failure deterministically once you have a hypothesis — don't
   propose a fix until you can make it fail on demand.
4. Fix the root cause, not the symptom — do not paper over it with a retry
   wrapper, an increased timeout, or `test.skip` unless you've exhausted the
   above and are flagging it as a known issue explicitly.
5. Confirm the fix by running the same repro loop that used to fail.

## Report

State the root cause in one sentence, the fix, and how you verified it (exact
command/loop count).
