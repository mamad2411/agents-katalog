---
description: Run the eval harness against every card under example-cards/ in parallel and persist scores to eval/store.sqlite. Use when the user asks to "backfill", "score everything", or "score all cards" for quality eval.
---

# Eval — Backfill All Cards

Score every card in `example-cards/*-card.json` and write rows to `eval/store.sqlite`.

## How to invoke

```bash
make eval-backfill                       # stub judge, offline
make eval-backfill JUDGE=claude          # real Claude Haiku judge, ~$0.04 for 18 cards
```

Direct invocation supports `--workers` and `--max-calls`:

```bash
python3 eval/runner.py backfill --judge claude --workers 4 --max-calls 50
```

## Behavior

- Stub runs serially (instant).
- Real backends parallelize via a `ThreadPoolExecutor` (default 4 workers). 18 cards usually finish in ~3-5 minutes.
- A pre-call status line prints per card (`[HH:MM:SS] YYYY-MM-DD: judging...`). Full subprocess traces append to `logs/eval-judge-YYYY-MM-DD.log` so the user can `tail -f` while it runs.
- Failures on individual cards are logged but do not abort the whole backfill.
- `--max-calls 50` caps accidental sweeps; bump it deliberately if the cap is hit.

## What to tell the user

Show the trailing summary: number of cards judged, total elapsed time, per-card amortized cost. If any card failed, surface the failing date and the error. Mention `tail -f logs/eval-judge-$(date +%F).log` so the user can monitor progress without re-running.
