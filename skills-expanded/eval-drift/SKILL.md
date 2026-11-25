---
description: Detect quality drift in published briefings by comparing the trailing-7d median composite score against the trailing-30d median (MAD-scaled). Use when the user asks to "check drift", "compare last week to baseline", or "is briefing quality slipping".
---

# Eval — Drift Detection

Surface quality slides before readers notice them. Robust to small-sample outliers via median + MAD scaling.

## How to invoke

```bash
make eval-drift D=YYYY-MM-DD                    # status: ok / alert (informational)
make eval-drift D=YYYY-MM-DD ALERT_EXIT=1       # exit 3 on alert (cron-friendly)
```

Direct invocation supports tuning windows and thresholds:

```bash
python3 eval/drift.py --as-of YYYY-MM-DD \
    --short-window 7 --long-window 30 \
    --z-thresh 1.5 --streak 2 \
    --exit-nonzero-on-alert
```

## Algorithm

For each of the last `--streak` days (default 2):

```
short_med = median(last 7 days of composites)
long_med  = median(last 30 days of composites)
long_mad  = median(|x - long_med|)
scale     = max(long_mad, 0.05)         # floor avoids div-by-zero on flat history
z         = (short_med - long_med) / scale
```

A day is "bad" when `z < -1.5`. If every day in the streak is bad, status flips to `alert`.

## Output

JSON blob with `status` (`ok` / `alert` / `no_data`), the medians, the MAD, the z-score, and an `alerts` list of offending days.

## What to tell the user

Lead with the status. If `alert`, show the offending dates and the z-scores; recommend running `make eval-show` and inspecting the per-card notes to identify which axis is dragging quality down. If `ok`, report the rolling medians anyway so the user has a sense of current quality.
