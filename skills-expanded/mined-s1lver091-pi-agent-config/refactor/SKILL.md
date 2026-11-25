---
name: refactor
description: Safely restructure code to improve clarity, reduce duplication, or simplify design without changing observable behavior. Use when asked to clean up, simplify, or restructure code.
---

# Refactoring

The only rule: behavior must not change. If there are no tests covering the code you are about to change, say so before proceeding.

## Step 1: Understand before touching

Read the code you are about to refactor in full.
- What does it do? What are its inputs and outputs?
- Who calls it? Use `grep` to find all call sites.
- Are there tests? Run them mentally to understand what is covered.

Do not start refactoring until you can answer these questions.

## Step 2: Identify the problem

Name the specific issue before fixing it. Common cases:

- **Long function**: does more than one thing. Split at natural boundaries.
- **Duplication**: same logic in multiple places. Extract a shared function.
- **Unclear naming**: names that don't communicate intent. Rename.
- **Deep nesting**: early returns flatten logic without changing behavior.
- **God object**: class with too many responsibilities. Split by cohesion.
- **Primitive obsession**: raw strings/numbers where a type would be clearer.

## Step 3: Work in small steps

One refactoring at a time. Each step must leave the code in a working state.

For each step:
1. Make the change
2. Re-read to confirm behavior is preserved
3. Check call sites are still correct

Never combine a refactoring with a behavior change. If you discover a bug while refactoring, note it and fix it in a separate change.

## Step 4: Verify

After all changes:
- Re-read the refactored code as if seeing it for the first time. Is it clearer?
- Check all call sites still compile and make sense
- Confirm no logic was accidentally changed

## Report format

**What was refactored**
Brief description of the code and what was wrong with it.

**Changes made**
- Rename: `oldName` -> `newName` in `file.ts`
- Extract: `functionName()` pulled out to `file.ts`
- Simplify: removed nesting in `functionName()` using early returns
- etc.

**Behavior preserved**
Confirmation that observable behavior is unchanged, and how you verified it.

**Follow-up**
Any bugs or design issues you noticed but did not fix (to keep the refactor clean).
