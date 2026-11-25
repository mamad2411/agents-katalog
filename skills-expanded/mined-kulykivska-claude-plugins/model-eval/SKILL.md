---
name: model-eval
description: >-
  Prove a model change is real before shipping it. Trigger on "did it get better?",
  "check the model", "evaluate this model change", "did this improve MAE", or
  before any PR that claims a metric win. Runs the multi-season leave-one-out
  harness and applies the regression gate.
---

# Model evaluation

The gate exists because a change that wins on the current season and loses on
the four before it is noise wearing a result's clothes.

## Steps

1. **Freeze the comparison.** Baseline is the currently deployed model, not the
   last thing you trained. Same data cut, same seeds, same preprocessing on
   both arms. If either differs, the number is meaningless.
2. **Run leave-one-out across every available season**, not just the latest.
   Each held-out unit is predicted by a model that never saw it, including in
   its rolling features.
3. **Report pooled effect with a significance figure**, plus the per-season
   breakdown. A pooled win with one season badly regressing is a different
   decision from a pooled win that holds everywhere, and the table is what
   makes that visible.
4. **Apply the gate:**
   - pooled metric improves, and
   - no season regresses meaningfully, and
   - the effect survives a significance check rather than sitting inside the
     run-to-run spread.
   Fail any of the three and the change does not ship, however good the
   intuition behind it.
5. **Check calibration separately from accuracy.** Probability outputs that got
   sharper but less calibrated are worse for anything downstream that consumes
   them as probabilities. Verify outputs that must sum or stay coherent still
   do.
6. **Record the verdict where the next person will find it**: the change, the
   pooled number, the per-season table, the decision. A rejected experiment is
   worth as much written down as an accepted one.

## What does not count as evidence

One season. One event. A backtest where the held-out event fed its own rolling
features. An improvement smaller than the spread between two seeded runs of the
same configuration. Eyeballing a chart.
