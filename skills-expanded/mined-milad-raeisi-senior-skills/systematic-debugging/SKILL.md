---
name: systematic-debugging
description: Root-cause-first debugging. Use for any bug, failing or flaky test, crash, exception, wrong output, hang, memory leak, performance regression, or "works on my machine" problem, before proposing any fix, and especially after a first fix attempt didn't work. Replaces guess-and-patch with reproduce, isolate, hypothesize, test, fix at the root, and lock it in with a regression test.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Systematic Debugging

The fastest way to fix a bug is to stop guessing. Each guess-and-patch cycle feels quick but leaves the real cause in place, adds code that hides symptoms, and teaches you nothing. A root cause you can state in one sentence, backed by a reproduction, is the only finish line.

**Rule:** no fix without (1) a reproduction and (2) a root cause you can explain, including why the code behaves this way and not just where it breaks.

## Phase 1: Reproduce

- Read the **entire** error: message, stack trace, logs before the failure, exit code. The answer is often in the line people skip.
- Get a reliable reproduction, ideally a single command or a failing test. Note the exact inputs, environment, versions, and steps.
- If it doesn't reproduce: compare environments (versions, config, env vars, data, OS, time zone, locale, concurrency). The difference *is* the clue.
- For flaky failures, loop it (`for i in $(seq 50); do <cmd> || break; done`), fix random seeds, and vary timing or parallelism to make it deterministic.

## Phase 2: Isolate

Shrink the search space until the cause has nowhere to hide:

- **What changed?** `git log -p --since=...` on the affected files. When there's a known-good commit, bisect: `git bisect start <bad> <good>`, then `git bisect run <test-cmd>`, and `git bisect reset` when done so the repo returns to your branch. Bisect turns hours of reasoning into minutes of mechanical search.
- **Minimize the input.** Remove half the data, config, or steps; keep the half that still fails.
- **Binary-search the code path.** Add assertions or logs at the midpoint between "input is right" and "output is wrong".
- **Compare working and broken.** A similar case that works is a gift: diff the two paths.
- **Check assumptions explicitly.** Print the actual values, types, versions, and paths instead of believing what they should be.

## Phase 3: Hypothesize and test

Keep a short hypothesis log; it stops you from circling:

```
H1: cache returns stale user after update -> predict: bypassing cache fixes it -> result: still fails -> rejected
H2: update writes to primary, read hits a lagging replica -> predict: reading from primary fixes it -> result: confirmed by query log
```

Change **one variable at a time**. Prefer experiments that can falsify the hypothesis. A hypothesis that can't fail tells you nothing.

## Phase 4: Fix at the root

- Write a failing test that reproduces the bug first (see `test-driven-development`). It must fail for the *right reason*.
- Fix the cause, not the symptom. A `try/catch`, null check, retry, or `sleep` that makes the symptom disappear is a patch over a cause you haven't found; use one only if you can explain why it's the correct behavior.
- Search for siblings: the same mistake often exists in other places (`rg` for the pattern).
- Run the new test (it passes), then the full relevant suite (nothing else broke).

## The three-strikes rule

If three fix attempts have failed, stop patching. Three misses mean your model of the system is wrong. Go back to Phase 1 with fresh eyes: re-read the error, question the assumption you've been most sure about, and consider whether the design itself is the problem. Report this honestly rather than trying a fourth variation.

## Debugging report

```markdown
**Symptom:** what the user saw.
**Root cause:** one or two sentences: what was wrong and why it produced the symptom.
**Evidence:** the reproduction, and the observation that confirmed the cause.
**Fix:** what changed and why it addresses the cause.
**Verified:** regression test (fails before, passes after) and full suite result.
**Related risks:** similar code checked, or worth checking.
```

## Anti-patterns

| Tempting move | What to do instead |
|---|---|
| "Let me try changing X and see" | Form a hypothesis that predicts the outcome first |
| Fixing the first suspicious thing you see | Confirm it's the cause with an experiment |
| Adding retries or sleeps to make a flaky test pass | Find the race or ordering dependency |
| Catching and logging the exception | Find why it's thrown |
| Several changes at once | One variable per experiment |
| "Fixed" without re-running the reproduction | Re-run it; see `evidence-before-claims` |
