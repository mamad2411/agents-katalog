---
name: sli-slo-design
description: >-
  Design customer-centric SLIs and SLOs using Google SRE guidance: good/total event ratios, availability/latency/freshness/correctness/completeness, critical user journeys, and iterative targets. Use when creating or revising SLIs/SLOs, writing SLO docs, or choosing what to measure.
---

# SLI / SLO Design

**Domain:** `foundations`  
**Sources:** SRE Book 1e Ch4, Workbook Ch2–3 + App A, SRE Book 2e Ch8

## When to use

- New service needs SLIs/SLOs
- Existing SLOs are ignored or always green/red
- Writing an SLO document
- Per-customer or client-side reliability questions

## Principles

- Prefer SLI = good_events / total_events (0–100% scale → natural error budget).
- Measure from the user's perspective (load balancer / client / CUJ), not only internals.
- Separate objectives: availability, latency, freshness, correctness, completeness.
- 100% is wrong; start from data; iterate; foundational before aspirational.
- Document clarifications and caveats (what is excluded, where measured).

## Workflow

1. Identify critical user journeys (CUJs) and user-visible failure modes.
2. For each CUJ pick SLI type(s) and measurement point.
3. Write SLI as ratio with explicit good/total definitions.
4. Analyze ≥28–30 days of history; scrub known anomalies.
5. Set target near historical compliance with small headroom (foundational).
6. Derive error budget = 100% − SLO; define window (commonly 28 days).
7. Write SLO document (see docs/templates/slo-document.md).
8. Wire burn-rate alerts (skill: alerting-on-slos) before celebrating.

## Decision guide

- HTTP APIs: often success = non-5xx (or stricter app-defined); latency with dual thresholds (e.g. 90%/99%).
- Pipelines: freshness + completeness + correctness probers beat raw job success.
- Low volume: protect against noise; consider longer windows or min-request guards.
- Per-customer SLOs (2e): only when contracts/segmentation justify complexity.

## Output template

```markdown
# SLO draft
- Service / CUJ:
- SLI (good/total + measurement point):
- SLO target(s) + window:
- Error budget (events/%):
- Exclusions / caveats:
- Data window analyzed:
- Alerting plan:
```

## Anti-patterns

- CPU/disk as SLIs for user happiness.
- Aspirational targets far above current reality with no plan.
- Undefined denominators or heartbeats polluting success rate.

## Canonical SLI shapes

| Type | Example good event |
|------|--------------------|
| Availability | Request returns non-5xx (or app success) |
| Latency | Request completes under threshold T |
| Freshness | Read uses data younger than T |
| Correctness | Prober expected == actual |
| Completeness | Batch processed 100% of eligible records |

## Dual latency thresholds

Common pattern from the Workbook: e.g. 90% < 400ms AND 99% < 850ms — separate budgets.


## Related skills

`error-budget-policy`, `alerting-on-slos`, `composing-slos`, `monitoring-observability`

## Canonical references

- [Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [SLO document example](https://sre.google/workbook/slo-document/)
- [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
