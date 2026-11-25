---
description: Scan the codebase for deficiencies, generate a prioritized report ranked by efficiency (points per iteration), and optionally transition into focused improve loops area-by-area until the user stops or the score hits 100.
---

# Audit Skill

## Pre-flight

1. Check `.claude/autoimprove/config.md` exists. If not, stop: "Run /autoimprove:setup first."
2. Check git is available and working tree is clean.

## Step 1: Run Measurement Suite

Run the measure skill to get the composite score and per-metric breakdown. Capture both the scores AND the raw command output for each metric.

For each metric defined in the config:
- Run the command (e.g., `tsc --noEmit 2>&1`, `pnpm test 2>&1`, `pnpm lint 2>&1`)
- Record the score (using the measure skill's scoring logic)
- Also capture the raw output for deficiency counting

## Step 2: Count Individual Deficiencies

Parse the raw output from each command to count specific issues:

- **Type errors:** Count lines matching error patterns (e.g., `error TS` for TypeScript, `error:` for Rust). Group by file.
- **Build:** Pass/fail only — no granular count. If build fails, it becomes top priority.
- **Tests:** Count passing vs total from test runner output. Identify failing test names if any.
- **Lint:** Count warning/error lines from linter output. Group by rule if possible.

## Step 3: Calculate Efficiency

For each metric with a gap (score < max):

1. **Point gap** = max_weight - current_score
2. **Estimated iterations** = `ceil(issue_count / issues_per_iteration)` using these heuristics:
   - Type errors: ~3 per iteration (clustered in files)
   - Lint warnings: ~2.5 per iteration
   - Tests (new): ~1 per iteration
   - Build fix: ~1-2 iterations
   - These are initial estimates — actual results will vary
3. **Efficiency** = point_gap / estimated_iterations
4. **Estimated tokens** = estimated_iterations × 22000 (rough average per iteration)

Read weights dynamically from `.claude/autoimprove/config.md`. If a metric is not applicable, skip it and redistribute weight as the measure skill already handles.

Sort areas by efficiency (highest pts/iteration first).

## Step 4: Display Report

Print the audit report:

```
━━━ Codebase Audit ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Current Score: XX/100

  [Metric 1]:  XX/WW  [progress bar]  (gap pts to max) or ✓ maxed
  [Metric 2]:  XX/WW  [progress bar]  (gap pts to max) or ✓ maxed
  [Metric 3]:  XX/WW  [progress bar]  (gap pts to max) or ✓ maxed
  [Metric 4]:  XX/WW  [progress bar]  (gap pts to max) or ✓ maxed

━━━ Fastest Path to 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  #  Area          Gap    Issues  Est. iterations  Efficiency
  1  [best area]   Xpts   N items  M iterations    X.X pts/iter ← best
  2  [next area]   Xpts   N items  M iterations    X.X pts/iter
  ...

  Total: ~N iterations to reach 100/100
  ⚡ Estimated token usage: ~XXXK tokens (rough estimate, actual usage varies)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The progress bar uses filled blocks (█) and empty blocks (░), scaled to 10 characters per metric.

**If score is 100/100:** Still print the full report (progress bars, efficiency table with all zeroes, and token estimate of ~0K tokens) so the output format is always consistent. After the report, print "Nothing to improve." and stop — do not prompt for the interactive fix loop.

**If build fails:** Show build as #1 priority with a note: "⚠️ Build is failing — other metrics may be unreliable. Fix the build first."

**If only one area has a gap:** Skip the selection prompt. Just ask: "Fix [area]? (~N iterations, ~XXXK tokens) (Y/n)"

## Step 5: Interactive Fix Loop

**Check for interrupted session first:** If `.claude/autoimprove/log.md` exists and the last session has `IN_PROGRESS` status, show: "↩️ You have an interrupted session. Use `/autoimprove:continue` to resume, or continue with this audit for a fresh start."

Prompt the user:

```
Would you like to start fixing? (Y/n)
```

**If no:** Stop. User can run `/autoimprove:improve` manually.

**If yes:**

```
Which area? (Enter number, or press Enter for #1 — [area name], ~N iterations)
>
```

If the user picks a number, use that area's estimate. If they press Enter, use the most efficient area.

### Starting the improve loop

Count all `**Branch:** autoimprove/experiment-` entries in `.claude/autoimprove/log.md` (if it exists) to determine the experiment offset.

Invoke the improve-loop skill directly with:
- **iterations:** The estimated count for the selected area
- **focus:** Generated focus string for that area:
  - Type safety → "Fix type errors"
  - Build → "Fix build errors"
  - Tests → "Add unit tests for untested functions"
  - Lint → "Fix lint warnings"
- **session_mode:** `new`
- **baseline_score:** The score just measured
- **start_iteration:** 1
- **total_iterations:** Same as iterations
- **experiment_offset:** Count of existing experiments

### After area completes

Re-run the measurement suite (Step 1-3) to get updated scores. Then show:

```
━━━ Area Complete: [area name] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Score: XX → YY/100 (+delta)
  [area]:  WW/WW  ██████████  ✓ maxed

Remaining work:
  #  Area     Gap    Est. iterations  Efficiency
  1  [next]   Xpts   M iterations     X.X pts/iter
  ...

  Remaining: ~N iterations (~XXXK tokens)

Continue to next area? (Y/n)
```

**If yes:** Repeat the selection prompt (or auto-select if only one area left). Start a new improve-loop session for that area.

**If no:** Stop. Print final score.

**If all areas maxed:** "🎉 Codebase score: 100/100. All areas maxed!"

### If area doesn't fully improve

If the improve loop finishes its estimated iterations but the area isn't maxed yet, show actual results:

```
Area [name] partially improved: XX → YY (expected ZZ)
Run more iterations on this area? (Y/n)
```

If yes, run more iterations (re-estimate based on remaining gap). If no, move to the next area.
