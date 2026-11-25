---
description: Emit a Markdown weekly digest of briefing quality scores (coverage, composite stats, axis medians, per-day table). Use when the user asks for a "weekly report", "eval summary", or "quality digest" for a specific date range.
---

# Eval — Weekly Markdown Report

Pull the trailing N-day window from `eval/store.sqlite` and emit a Markdown digest suitable for publishing to Notion / Teams / Slack, or for committing under `logs/eval-reports/`.

## How to invoke

```bash
make eval-report D=YYYY-MM-DD W=7                            # 7-day window to stdout
make eval-report D=YYYY-MM-DD W=14 OUT=logs/eval-week.md     # write to file
```

Direct invocation:

```bash
python3 eval/report.py --as-of YYYY-MM-DD --window 7 --out logs/eval-week.md
```

## Behavior

1. Fetch all `eval_runs` rows in `[as_of - window + 1, as_of]`.
2. Pick the latest run per `card_date` (so re-runs don't double-count).
3. Compute coverage (`N / window` days judged), composite min/max/median, and per-axis medians.
4. Emit:
   - H1 header with the date range
   - Coverage + composite stats
   - Axis medians table
   - Per-day detail table (date, composite, F/N/D/S/C, judge model, truncated notes)

## When to use

- Monday morning summary across the previous 7 days.
- Investigating a drift alert (`make eval-drift`) — the per-day table shows which axes are dragging.
- After a re-baselining workflow, to confirm the new judge/prompt produces consistent quality.

## What to tell the user

If `OUT` is set, mention the file path and a quick `cat` or preview command. If piping to stdout, show the digest verbatim (the user can scroll the terminal). For Notion/Teams publishing, point at `scripts/notify-teams.sh` or the Notion MCP — the harness intentionally does not publish on its own.
