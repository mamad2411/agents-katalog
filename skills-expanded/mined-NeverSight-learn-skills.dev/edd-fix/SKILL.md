---
name: edd-fix
description: 'Slash command: /edd-fix — detect regressions, diagnose root causes from rubrics and prompt, fix the prompt, and verify.'
---

# /edd-fix — Detect, Diagnose, Fix, Verify

Run this when the user types `/edd-fix` or asks you to fix failing evals.

## Step 1: Detect

Run `npx @scalvert/edd run --fail-on-regression` to identify regressions against the baseline.

If the command exits with an error, regressions were detected. Parse the output to find which test cases regressed.

If no regressions are found and all tests pass, tell the user and stop.

## Step 2: Diagnose

For each regressed test case, read **all three** of these:

1. **The test case rubric** — found in the tests directory (configured in `edd.config.json`). The rubric defines the _specific behavior_ being evaluated. This is the contract.
2. **The prompt file** — the system prompt that produced the failing behavior.
3. **The baseline** — found at `baselines/<prompt-name>.json` (or the path in config). Shows what scores these tests achieved previously.

Identify the root cause. Common patterns:

- A recent prompt edit removed or weakened a constraint the rubric requires.
- A new instruction conflicts with an existing one for certain inputs.
- The prompt covers the general case but the test input hits an edge case gap.
- Language was made more ambiguous (e.g., "try to avoid" replaced "never").

## Step 3: Fix

Make a targeted edit to the prompt file. Follow these principles:

- **Always fix the prompt, not the tests.** Tests define the behavioral contract. Edit the prompt to satisfy the failing rubric. Do not modify test cases or rubrics unless the user explicitly says the prompt change was intentional and the tests should be updated to match.
- **Fix only what's broken.** Don't restructure the prompt or "improve" unrelated sections.
- **Preserve passing behavior.** Before editing, identify which prompt instructions the passing tests depend on. Don't weaken those.
- **Be specific.** If the rubric says "must not reveal personal information," the prompt needs an explicit rule about personal information, not just "be careful with data."
- **Match the rubric's language.** If the rubric says "must politely decline," the prompt should instruct polite declining, not just "refuse."

## Step 4: Verify

Run `npx @scalvert/edd run` again (without `--fail-on-regression` so you can see all results).

Check two things:

1. The previously failing tests now pass.
2. No previously passing tests broke.

**If new failures appear**, go back to Step 2 with the new failures. Iterate up to 3 times.

**If after 3 iterations there are still failures**, stop and explain the situation to the user. Show which tests are failing and why the fixes are conflicting. The user may need to adjust rubrics or accept a tradeoff.

## Step 5: Suggest baseline

If all tests pass (or the user is satisfied with the results), suggest running `npx @scalvert/edd baseline` to promote the current run.

**Always ask before saving a baseline.** Baselines are committed to git and represent the accepted behavior standard.

Example:

> All 6 tests passing with a pass rate of 1.000. Would you like me to run `npx @scalvert/edd baseline` to save this as the new baseline?

## Important

- Never skip reading the rubric. The rubric is the source of truth for what "correct" means.
- Never overwrite a baseline without asking.
- If the prompt and rubric genuinely conflict (the rubric asks for something the prompt shouldn't do), flag this to the user rather than silently changing one or the other.
