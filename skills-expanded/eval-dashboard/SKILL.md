---
description: Build the interactive offline eval dashboard (eval/dashboard/index.html) — Chart.js trend, axis radar, composite histogram, per-card stacked bars, sortable card table. Use when the user wants to "see eval results", "open dashboard", "visualize quality", or "compare cards".
---

# Eval — Interactive Dashboard

Single-file offline UI over `eval/store.sqlite` + `eval/golden/`. No backend, no build step. Chart.js loads from a CDN, but everything else works over `file://`.

## How to invoke

```bash
make eval-dashboard                                  # regenerate dashboard/data.js
make eval-dashboard OPEN=1                           # also open in default browser
make eval-dashboard DASHBOARD_JUDGE=claude-haiku-4-5-20251001  # filter rows
```

Direct invocation:

```bash
python3 eval/export_dashboard.py --judge claude-haiku-4-5-20251001 --open
```

## Behavior

1. Pull rows from `eval/store.sqlite` (latest-per-date wins).
2. Join each row with its corresponding `eval/golden/<date>.json` baseline.
3. Compute summary stats: composite min/max/median/mean, axis medians, drift z-score, gate-fail count, regression count.
4. Serialize to `eval/dashboard/data.js` as `window.EVAL_DATA = {...}`.
5. Optionally launch the default browser pointing at `eval/dashboard/index.html` via `file://`.

## Panels rendered

| Panel | Visualization |
| --- | --- |
| Stat cards | Composite median + mean, drift status, gate fails, regressions |
| Composite trend | Line chart with baseline overlay + dashed 3.0 gate threshold |
| Axis radar | 5-axis median across all cards |
| Composite histogram | Buckets `< 2.5` → `≥ 4.5` |
| Per-card stacked bars | Each card's weighted axis contributions |
| Per-card table | Sortable, filterable (`All` / `Below gate` / `Regressed` / `Composite ≥ 4`), live search |

## What to tell the user

After running, tell them the dashboard path (`eval/dashboard/index.html`) and how many cards / goldens loaded. If `OPEN=1` was not passed, give them the open command for their platform (`open` on macOS, `xdg-open` on Linux, `start` on Windows). Mention the dashboard is **regenerated** from the store — they should re-run this after any `make eval-backfill` to refresh visualizations.
