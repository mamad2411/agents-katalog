---
name: data-pipelines
description: >-
  Design reliable data/processing pipelines: correctness, freshness, completeness, late data, and idempotency per Google SRE. Use for ETL/stream reliability and pipeline SLOs.
---

# Data Pipelines

**Domain:** `resilience`  
**Sources:** SRE Book 1e Ch25, Workbook Ch13

## When to use

- Pipeline SLO design
- Freshness incidents
- Exactly-once / idempotency debates

## Principles

- Pipeline SLIs often: freshness, correctness, completeness — not just job success.
- Idempotency and replay are core reliability tools.
- Late data and skew need explicit policy.
- Probers with known outcomes beat vibes for correctness.

## Workflow

1. Define consumer CUJs that depend on pipeline output.
2. Choose SLIs (freshness windows, completeness per hour, correctness prober).
3. Document failure modes: stuck, skew, poison pill, hotspot.
4. Add observability: lag, throughput, poison rates, DLQ age.
5. Alert on budget burn for freshness/completeness.

## Decision guide

- If 'success' jobs skip records → completeness SLI required.

## Output template

```markdown
# Pipeline reliability plan
- Consumers / CUJs:
- SLIs/SLOs:
- Failure modes + detections:
- Replay/idempotency story:
```

## Anti-patterns

- Only monitoring job exit codes.
- Silent drops.

## Related skills

`sli-slo-design`, `data-integrity`, `monitoring-observability`

## Canonical references

- [Data Processing Pipelines](https://sre.google/sre-book/data-processing-pipelines/)
- [Workbook Pipelines](https://sre.google/workbook/data-processing-pipelines/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
