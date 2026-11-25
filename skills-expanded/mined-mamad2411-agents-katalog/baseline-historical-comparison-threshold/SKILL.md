---
tags: [backend, baseline, historical, comparison, threshold]
name: baseline-historical-comparison-threshold
description: Evaluate a current metric against a historical baseline (prev hour/day/week/month/year, with MIN/AVG/MAX aggregation) as a dynamic threshold; supports RATE or VALUE change modes and dampening.
trigger: Fixed thresholds false-positive during normal daily/weekly cycles; alarms should fire only on deviation from historical norms.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# Baseline Historical-Comparison Threshold

## Shape

Evaluator pulls a pre-aggregated historical value at a configured offset (e.g. same hour yesterday), compares the current reading to it via RATE or VALUE change, and applies dampening before firing.

## Steps

1. Define `BaselineType`: `LAST_HOUR`, `YESTERDAY`, `YESTERDAY_SAME_HOUR`, `LAST_WEEK_SAME_DAY`, `LAST_WEEK_SAME_DAY_AND_HOUR`, `LAST_MONTH`, `LAST_YEAR`.
2. Define `BaselineCalcType`: `MIN` / `AVG` / `MAX` (aggregation over the reference bucket).
3. Compute reference timestamp from `BaselineType`; query pre-aggregated stats (hour-bucket or day-bucket table).
4. Define `ThresholdChangeType`:
   - `RATE` → `(current - baseline) / baseline * 100`
   - `VALUE` → `current - baseline`
5. Apply dampening: `CONSECUTIVE` (N in a row) or `LAST_N_EVAL` (N out of M).
6. Evaluate `change OP threshold` with operator (`GT`, `LT`, `GE`, `LE`, ...).
7. Historical data missing → return empty (no alarm, not false-trigger).
8. Emit condition text containing metric name, baseline type, calc method, and computed change for audit.

## Counter / Caveats

- Zero baseline + `RATE` → division error; short-circuit to empty or VALUE mode.
- Historical aggregates must exist before evaluation — bootstrap period yields no alarms.
- Baseline comparison amplifies noise on low-volume metrics; prefer `VALUE` with `AVG` there.
- Seasonality the baseline type doesn't capture (quarterly, yearly events) still produces false positives — document the limits.
