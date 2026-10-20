---
name: loop-debug
description: Root-cause debugging loop. Use when a bug, failing test, or unexpected behavior appears and the cause is not yet proven — before proposing any fix, and again whenever a previous fix did not stick.
---

# Debugging Loop

Most bad fixes come from skipping straight to a plausible cause. This loop forces the
cause to be *proven* in the real system before any fix is written — and treats a fix
that didn't stick as evidence about the investigation, not bad luck.

## When to reach for this

- A test fails, an error appears, or behavior diverges from expectation
- A fix was applied and the symptom returned
- An error is about to be dismissed as "just log noise"
- "My change broke something" and the culprit edit is unknown

## Iron law

**No fix without a proven root cause.** A cause is proven when an instrumented
observation of the real system confirms it — not when it merely explains the symptom.

## The loop

1. **Reproduce deterministically.** Capture the exact command, input, and failing
   output. No reproduction → no debugging, only guessing.
2. **Read the wiring end-to-end** — the full path from trigger to failure — before
   forming any theory. The bug is often in unchanged code the change now interacts with.
3. **State one falsifiable hypothesis at a time.** "X is null because Y skips
   initialization when Z" — something an observation can kill.
4. **Instrument the real system** (log line, probe, debugger, temporary assertion) and
   observe. Never reason from code fragments alone, and never test the hypothesis on a
   toy reproduction — toys reproduce the toy.
5. **Record the verdict in a ledger and loop** until a hypothesis survives:

   | # | Hypothesis | Observation that would kill it | Result |
   |---|---|---|---|
   | 1 | cache returns stale row | log cache key + hit/miss at read site | killed — always miss |
   | 2 | writer commits after reader starts | log txn begin/commit ordering | **confirmed** |

6. **Fix with a failing test first.** Write the test that reproduces the root cause,
   watch it fail, apply the fix, watch it pass (`loop-verify` for the evidence bar).
7. **Three failed fixes = wrong altitude.** Stop patching; the defect is in an
   assumption or architecture a level above where the fixes were aimed.

## Isolation techniques

| Situation | Technique |
|---|---|
| Regression after a batch of edits | Revert changed files to base one at a time until the symptom flips |
| Regression somewhere in history | `git bisect` with the reproduction as the test |
| Works in env A, fails in env B | Diff the environments (versions, config, data), not the code |
| Intermittent failure | Loop the reproduction until the failure rate is measured, then instrument |

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's probably just log noise" | Every error means something is mis-wired; noise is a diagnosis, not a default |
| "A config tweak might fix it" | Levers pulled without a cause are experiments run on production trust |
| "Patch it in the caller for now" | A symptom patch in one caller leaves the same bug armed everywhere else |
| "Two hypotheses at once saves time" | Confounded observations kill neither — slower than one at a time |

## Pitfalls

- Fixing the first plausible explanation instead of the proven one
- Instrumenting the toy reproduction instead of the real system
- Deleting the reproduction after the fix — keep it as the regression test
- Closing the loop without recording the root cause where the next session can find it
  (`loop-compound`)

---
*Related: `loop-verify` (the evidence bar for step 6), `loop-compound` (record the
root cause permanently), `code-review-checklist` (the bug is often in unchanged code) ·
output/ADR format: `playbook-conventions`*
