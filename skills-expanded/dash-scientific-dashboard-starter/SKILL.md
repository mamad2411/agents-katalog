# Dash Scientific Dashboard Starter

Use this skill to build a deterministic Dash dashboard scaffold from toy measurements and inspect the resulting layout, callback, and preview artifacts.

## What This Skill Does

- loads a small tabular measurement set
- defines a Dash app with a metric selector, summary cards, and a trend graph
- writes both a Dash HTML shell and a standalone preview figure plus a machine-readable summary

## When To Use It

- when you need a runnable `dashboards` starter
- when you want a local Dash scaffold before wiring in live scientific data sources
- when you need deterministic layout and callback metadata for repository tests

## Run

```bash
./slurm/envs/reporting/bin/python skills/visualization-and-reporting/dash-scientific-dashboard-starter/scripts/build_dash_scientific_dashboard.py \
  --input skills/visualization-and-reporting/dash-scientific-dashboard-starter/examples/toy_measurements.tsv \
  --html-out scratch/dash/dashboard_preview.html \
  --summary-out scratch/dash/dashboard_summary.json
```

## Notes

- The Dash app is not served in tests; instead the skill validates the app structure, registered callback map, and offline preview outputs.
- The preview HTML is self-contained so it remains viewable without a running Dash server.
