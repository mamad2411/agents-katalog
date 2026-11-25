---
name: Debug
description: Track a bug to its root cause with a reproducible loop instead of guessing. Use for failing tests, crashes, broken UI, or flaky behavior.
---

# Debug

Change one variable at a time. Never fix code you have not seen fail.

## Loop

1. **Reproduce**
   - Find the smallest command, test, or interaction that fails.
   - Capture the exact error, stack trace, versions, and environment.
   - If it cannot be reproduced, gather logs and identify the missing observation instead of guessing.

2. **Localize**
   - Read the code path from entry point to failure.
   - Use `grep` for the symbol, error string, and configuration key.
   - Check recent changes (`git log`, `git diff`) before assuming the code was always wrong.
   - Form 2–3 hypotheses and rank them by evidence, not vibes.

3. **Instrument**
   - Add the minimum logging or a focused temporary test.
   - Verify assumptions one at a time. Check inputs, state, timing, and boundaries.
   - Remove instrumentation afterward.

4. **Fix the cause**
   - Prefer the smallest change that addresses the root cause. Do not mask a symptom with retries or sleeps unless that is genuinely the contract.
   - Add a regression test that fails before the fix and passes after.

5. **Verify**
   - Run the focused test, then the broader suite or build.
   - Re-read the diff. Check error paths and adjacent behavior.
   - Report the root cause in one sentence, the fix, and the verification.

## Common traps

- Environment drift: installed version vs lockfile, stale build output, wrong Node/Python.
- Data shape: null vs empty vs missing; strings that look numeric.
- Async: unawaited promises, shared mutable state, event ordering.
- Cache/config: old values loaded at boot, duplicated sources of truth.

## Guardrails

- Do not delete failing tests to make a suite green.
- Do not claim a fix without running the reproduction again.
- If the fix requires a larger refactor, stop and present the tradeoff.
