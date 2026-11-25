---
description: Judge a single AI News Briefing card against the 5-axis quality rubric (factuality, novelty, source diversity, signal density, coherence) and persist the score. Use when the user asks to "score", "judge", "evaluate", or "rate" a briefing for a specific date.
---

# Eval — Score One Card

Run the LLM-as-judge against one daily briefing card and write the result to `eval/store.sqlite`.

## How to invoke

Prefer the Makefile target. Default `JUDGE` is `stub` (offline heuristic, no API). Use `JUDGE=claude` for the real Claude Haiku 4.5 judge.

```bash
make eval D=YYYY-MM-DD                  # stub backend, no API cost
make eval D=YYYY-MM-DD JUDGE=claude     # real Claude judge (~$0.002/card)
make eval D=YYYY-MM-DD JUDGE=claude GATE=1  # also exit 2 if composite < 3.0
```

Equivalent direct invocation:

```bash
python3 eval/runner.py score --date YYYY-MM-DD --judge claude
```

## Behavior

1. Read the card JSON at `example-cards/YYYY-MM-DD-card.json` (or `logs/YYYY-MM-DD-card.json` for fresh runs).
2. Pull the prior 7 days' headlines from `example-cards/` as the novelty baseline.
3. Compose the judge prompt (`eval/judge_prompt.md`) + briefing text + prior headlines.
4. Send to the selected backend; the judge returns a JSON block with the 5 axis scores plus a `notes` field.
5. Compute `composite = 0.30·F + 0.20·N + 0.15·D + 0.20·S + 0.15·C` and upsert into `eval_runs` keyed on `(card_date, prompt_version, judge_model)`.
6. Print the result as JSON. With `--gate`, exit 2 if composite is below `--gate-threshold` (default 3.0).

## What to tell the user

Report the composite score, the per-axis breakdown, and the judge's notes verbatim — those notes usually call out the weakest axis with a concrete reason. If `--gate` is set and the run failed, surface that loudly along with the threshold.
