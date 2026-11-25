---
name: metrics-engineering
description: Design metrics for systems. Use when defining what to measure and how to alert.
metadata:
  tags: metrics, engineering
---

# Metrics Engineering

## Use this skill when
- Choosing RED vs USE vs golden signals
- Designing metric names, labels, and buckets
- Building dashboards and alert thresholds

## Do not use this skill when
- Distributed tracing (use tracing-engineering)
- Log content analysis (use logging-engineering)

## Instructions
1. Measure the golden signals: latency, traffic, errors, saturation.
2. Prefer rich counters with bounded label cardinality.
3. Choose histogram buckets that match SLOs.
4. Instrument at service boundaries and critical internals.
5. Alert on user-visible symptoms and rate-of-change, not raw spikes.
6. Keep dashboards oriented per audience (ops, exec).
7. Define alert fatigue policy: every alert has an action.

## Checklist
- Label cardinality bounded
- SLOs expressed in metrics
- Alerts actionable

## Output Format
- Metric inventory | cardinality | dashboards | alert rules

## Common Mistakes
- High-cardinality labels (per-user)
- Alerting on raw CPU only
- Dashboards nobody reads
