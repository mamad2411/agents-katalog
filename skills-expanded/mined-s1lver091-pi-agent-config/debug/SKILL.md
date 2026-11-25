---
name: debug
description: Systematically diagnose and fix bugs, unexpected behavior, or failing tests. Use when something is broken and the cause is not immediately obvious.
---

# Debugging

Do not guess. Work systematically: reproduce, isolate, hypothesize, verify.

## Step 1: Reproduce

Before touching any code, confirm you can reproduce the problem.
- What is the exact input or sequence of actions that triggers it?
- Is it consistent or intermittent?
- Does it happen in all environments or only some?

If you cannot reproduce it, stop and ask for more information.

## Step 2: Read the error

If there is an error message or stack trace:
- Read the full trace, not just the first line
- Find the deepest frame in your own code (not library internals) — that is your starting point
- Check what values were in scope at that point

## Step 3: Isolate

Narrow down where the problem lives before reading more code.
- Add temporary logging or assertions to confirm assumptions about state
- Bisect: is the problem in the input, the transformation, or the output?
- Check: when did this last work? Use `git log` and `git blame` to find recent changes

## Step 4: Form a hypothesis

Write one sentence: "I believe X is happening because Y."
Do not skip this. It prevents you from randomly changing code and hoping it works.

## Step 5: Verify the hypothesis

Find the code that should implement the behavior you described.
- Read it carefully
- Check the actual values at runtime if possible
- Look for edge cases the author may have missed

If your hypothesis is wrong, return to step 3. Do not guess-and-check.

## Step 6: Fix

Make the smallest possible change that fixes the root cause.
- Do not refactor surrounding code while fixing a bug
- Do not fix multiple bugs in one change
- After fixing, re-read the change and ask: could this break anything else?

## Step 7: Verify the fix

- Confirm the original issue no longer reproduces
- Check that related behavior still works
- If a test was failing, confirm it now passes and no others broke

## Report format

**Root Cause**
One sentence: what was actually wrong.

**Fix**
What you changed and why that addresses the root cause.

**Files Changed**
- `path/to/file.ts:42` — what changed

**Regression Risk**
Any adjacent behavior that should be tested after this fix.
