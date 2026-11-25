---
name: fix-with-proof
description: Fix a defect with evidence: reproduce, find where it started, prove the fix with the same reproduction; explain any measured number. Use for any bug or slowness.
---

# Fix with proof

Every line you ship in a fix traces to something you saw happen. A change that "might help" is a guess, and guesses do not ship.

## 1. Reproduce

See the defect yourself on the surface the person uses: the screen, the route, the command. Write down the exact steps and the wrong result. If it does not reproduce, narrow the conditions, add logging, or build the trigger until it does. A fix without a reproduction is not done.

## 2. Find where it started

The symptom is where a wrong state became visible. The cause is the first place the system did something it should not.

- Ask "why" at each step until the answer is a wrong decision in the code, not a consequence of an earlier one.
- When unsure, instrument: read the real error, the real values, the real state. Do not guess from reading code.
- Ask whether the state that broke is legitimate. If it may happen, handling it where it broke is the fix. If it should never exist, a guard there hides the bug: find what produced it.
- Guards, retries, swallowed errors and clamped values are the usual ways a bug gets hidden.
- Something fails only after a restart? Suspect saved state first: caches, config files, lock files.
- Fix the pattern, not just the instance: search for the same fault elsewhere.

## 3. When two fixes fail, attack the premise

If two fixes that share one belief failed the same way, write that belief as one sentence and test it directly before a third fix. Look at how the failures are distributed, not only at how big they are.

## 4. Prove the fix

Run the same reproduction. "Inconclusive" or "passed on a different surface" is not a pass. Where a cheap test exists, commit the failing test first and the fix on top.

## 5. Explain every number

Before you report a speedup, a regression, a latency or a score:

- State how many runs, the spread between them, and the result that would have changed your decision.
- Name what limits the number (CPU, a lock, the network, the load generator). If you cannot say why it is not twice as good, you do not know what you measured.
- Rule out the usual impostors: errors, cached or skipped work, code that never ran, a side left on defaults, noise.
- If the spread is larger than the effect, there was no effect.

## Report

What was broken, the cause, the fix, and the reproduction output before and after, pasted as it ran.
