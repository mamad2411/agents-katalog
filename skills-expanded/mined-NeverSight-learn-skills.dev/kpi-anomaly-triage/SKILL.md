---
name: kpi-anomaly-triage
description: Vendor-neutral skill to analyze KPI time-series data, detect anomalies, and generate a triage summary with likely drivers.
---

## When to invoke
- When monitoring weekly/daily KPI dashboards for sudden changes.
- When preparing an investigation checklist for metric movements.

## Inputs needed
- `--input`: Path to a CSV file with columns `date` (YYYY-MM-DD) and `value`.
- Optional `--window`: Rolling window size in days (default 14).
- Optional `--z`: Z-score threshold (default 3.0).
- Optional `--out`: Path to write a JSON report.

## Workflow
1. Parse dates and values; sort by date.
2. Compute rolling mean and standard deviation.
3. Flag points with 
   \[ z = \frac{x - \mu}{\sigma} \]
   above threshold.
4. Summarize recent anomalies and basic context (last 7 days trend).

## Output format
JSON with:
- `anomalies`: list of `{date, value, z, mean, std}`.
- `recent_summary`: last value, 7d min/max, direction.

## Guardrails
- If standard deviation is zero, do not divide by zero; skip anomaly scoring.
- Purely statistical heuristic; not a root cause analysis.

## Reference code
- `kpi_anomaly_triage.py`
