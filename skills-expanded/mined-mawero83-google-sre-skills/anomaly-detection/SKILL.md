---
name: anomaly-detection
description: >-
  Apply statistical and ML-aware anomaly approaches for SRE: baselines, seasonality, binomial error-rate intuition, and post-alert analysis. Use when tuning detectors, investigating weird metrics, or adding intelligent alerting.
---

# Anomaly Detection

**Domain:** `foundations`  
**Sources:** SRE Book 2e Ch9 + App F/G, Workbook Ch5

## When to use

- Static thresholds fail on seasonal traffic
- Need principled error-rate alerting
- Evaluating AI/ML anomaly products

## Principles

- Monitoring is an imperfect lens; cardinality and noise bound what you can see.
- Error rates: use statistical confidence (binomial) especially on low volume.
- Latency alerting has dedicated math — do not treat like error rates.
- AI detectors need human-defined impact; anomaly ≠ incident.
- Prefer detect → triage → confirm user impact via SLI before paging.

## Workflow

1. Characterize metric: volume, seasonality, heavy tails, deployment correlation.
2. Choose method: burn-rate (preferred for SLIs), seasonal baseline, or change-point.
3. Backtest on known incidents + quiet periods.
4. Set page vs ticket thresholds with expected weekly volume.
5. Add annotation hooks for deploys/config changes.

## Decision guide

- If volume low → widen windows or require min events.
- If AI vendor opaque → require shadow mode before paging.

## Output template

```markdown
# Detector design
- Metric / SLI:
- Method + parameters:
- Backtest true/false positive notes:
- Page criteria:
- Owner + review cadence:
```

## Anti-patterns

- Paging on every z-score blip.
- Training anomaly models on unlabeled toil.

## Related skills

`alerting-on-slos`, `monitoring-observability`, `ai-supports-sre`

## Canonical references

- [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
