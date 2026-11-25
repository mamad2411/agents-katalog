---
name: debug
description: Root-cause debugging discipline — use when encountering any bug, failing test or check, unexpected behavior, or build failure, BEFORE proposing fixes; and again before claiming anything is fixed. Especially when a "quick obvious fix" is tempting or previous fixes didn't stick. When the person says 'debug' or 'root cause', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: No tooling; read before fixing and before claiming a fix.
metadata:
  version: "0.12.1"
---

# Debug to the root cause; claim with evidence

These are one project's working rules; a project adopts them by installing this skill and keeps what fits.

Random fixes waste more time than investigation ever does, and a symptom fix plants the same bug's next occurrence.
The discipline below is fast precisely when it feels too slow to afford.

## 1. Understand before touching anything

- Read the error completely — message, stack, line numbers, exit code.
  It often contains the answer.
  When it arrives with pages of context (elaborated terms, a full log), cut it to its error blocks before reasoning.
- Reproduce it reliably.
  Not reproducible → gather more data; don't guess.
- Check what changed: diff, recent commits, dependency or config drift, environment differences.
- In multi-layer failures (pipeline → build → tool; API → service → store), add evidence at each boundary — log what enters and leaves each layer, run once, and let the evidence say WHERE it breaks before reasoning about why.
- Trace bad values backward to their origin; fix at the source, not where the symptom surfaced.

## 2. Compare against what works

Find the nearest working sibling (similar code, a passing case, a reference implementation) and list the differences — all of them, including the ones that "can't matter".
Read references completely before adapting them; partial understanding of a pattern is how adaptations break.

## 3. One hypothesis, minimal test

State it: "X is the root cause because Y."
Change the smallest thing that tests it — one variable at a time, never a bundle of fixes.
Wrong → form a new hypothesis; do NOT stack another fix on top.

**Circuit breaker:** three failed fixes means the problem is architectural, not local — each fix revealing a new problem elsewhere is the signature.
Stop fixing and question the design with the user instead of attempting a fourth.

## 4. Fix, then prove the fix

- Capture the failure as a test or a planted-defect check before fixing, where the project's tooling allows; verify it fails, fix, verify it passes (red → green — a regression test that never failed proves nothing).
- One change; no while-I'm-here refactoring mixed in.
- Claiming "fixed"/"passing"/"done" requires FRESH evidence from this session: run the project's full verification gate, read the output, then state the claim with the evidence.
  "Should work now" is not a status.
  If a check fails, say so with the output — a true "it's still broken" beats a false "done" every time.
- Judge a check by its exit status, never by grepping its output: a pipe or a filter reports a failure as a success; a background command's exit code is read from the tool's report of it, never from a trailing `echo`, which masks it.
- A scripted edit is verified afterwards by searching for every anchor it inserted, since an anchor that does not match leaves the file unchanged without a word.
- A green that did not run on the file is not a green: when a check passes suspiciously, confirm its scope and its trigger both included the file — the two are separate lists and widening one does not widen the other.
