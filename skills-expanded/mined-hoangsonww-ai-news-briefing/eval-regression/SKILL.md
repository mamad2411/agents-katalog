---
description: Re-judge every pinned golden card in eval/golden/ and fail if any composite has dropped more than 0.5 points vs its baseline. Use when the user asks to "run regression", "check golden set", or wants CI-style quality gating after a prompt or judge change.
---

# Eval — Regression Gate

Guard against silent quality regressions when the daily prompt, judge model, or judge prompt changes.

## How to invoke

```bash
make eval-regression                        # stub judge, fast smoke test
make eval-regression JUDGE=claude           # real Claude Haiku judge — production gate
```

Direct invocation supports a tighter (or looser) drop tolerance:

```bash
python3 eval/runner.py regression --judge claude --regression-drop 0.5
```

## Behavior

1. Read every `eval/golden/*.json` baseline (currently 18 cards, real-judge composites 2.9–4.2).
2. Re-judge each card against the configured backend.
3. Compute `delta = new_composite - baseline_composite`.
4. Fail (exit 2) if any card's delta is below `-regression-drop` (default `-0.5`).
5. Print per-card OK / REGRESSED with explicit deltas.

## When to run

- After bumping `PROMPT_VERSION` in `eval/judge.py` or editing `eval/judge_prompt.md`.
- After switching judge models (`EVAL_JUDGE_MODEL`).
- In CI before merging changes to the daily `prompt.md`.
- After a re-baselining workflow to confirm the new goldens hold.

## What to tell the user

If regressions are flagged, list each offending card with its delta and the judge's notes — they explain *why* the score dropped. If no regressions, report total cards passed and the worst-case delta so the user knows how much headroom remains.
