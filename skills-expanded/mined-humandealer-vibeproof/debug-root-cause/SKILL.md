---
name: debug-root-cause
description: Use when something is broken — a bug, a test failure, unexpected behavior. Enforces the no-fix-without-root-cause loop.
---

# Debug to Root Cause

The Iron Law: **no fix without a confirmed root cause.** Patching a symptom you
don't understand just moves the bug. Work the four phases in order.

## When to use

Any error, test failure, 500, stack trace, "it worked yesterday", or behavior
that doesn't match expectations. Use this *instead of* immediately editing code.

## The four phases

### 1. Investigate (gather facts, change nothing)
- Reproduce it reliably. If you can't reproduce it, you can't fix it.
- Read the **actual** error message and stack trace — top to bottom.
- Capture the exact inputs, environment, and steps that trigger it.
- Don't theorize yet. Collect evidence.

### 2. Analyze (find the why)
- Trace from the symptom back to the source. Follow the data.
- Ask "why" repeatedly until you reach a cause, not a coincidence.
- Distinguish *where* it surfaces from *why* it happens — often different.

### 3. Hypothesize (one testable theory)
- State a single, specific hypothesis about the root cause.
- Predict what you'd see if it's true. Test that prediction.
- Wrong? Back to phase 2 with what you learned. Don't guess-and-check edits.

### 4. Fix (root cause + regression test)
- Fix the actual cause, not the symptom.
- **Write a test that fails before the fix and passes after.** This proves the
  cause and prevents regression.
- Run the full quality gate (rules/code-quality.md).

## After the fix

Record it: add a gotcha entry to `rules/error-prevention.md` (what happened,
why, how to prevent). If it caused real damage, write a lesson into memory
(rules/memory-system.md). That's how the bug stays dead.

## Anti-patterns

- Changing things randomly to see what helps.
- Adding a try/except that hides the error instead of fixing it.
- "Fixed" without reproducing the original failure first.
