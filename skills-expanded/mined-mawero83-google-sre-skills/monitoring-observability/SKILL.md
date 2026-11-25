---
name: monitoring-observability
description: >-
  Design monitoring and observability the Google SRE way: four golden signals, telemetry vs analytics, OpenTelemetry, customer-centric monitoring, and value-vs-cost of data. Use when building dashboards, instrumentation plans, or observability architecture.
---

# Monitoring Observability

**Domain:** `foundations`  
**Sources:** SRE Book 1e Ch6, Workbook Ch4, SRE Book 2e Ch9

## When to use

- Greenfield instrumentation
- Dashboard sprawl / blind spots
- Choosing metrics vs logs vs traces
- Customer-experienced reliability measurement

## Principles

- Four golden signals: latency, traffic, errors, saturation.
- Symptoms over causes for paging; causes for diagnosis.
- Observability evolves monitoring: ask new questions without new deploys when possible.
- Separate high-availability telemetry (pages you) from analytics telemetry (cost-sensitive).
- OpenTelemetry is the modern interchange; standardize thoughtfully.
- Cardinality and retention are first-class cost/reliability decisions.

## Workflow

1. List CUJs and failure modes → required signals.
2. For each signal: metric / trace attribute / log field + owner.
3. Define RED/USE or golden-signal dashboards per service tier.
4. Add distributed tracing on critical path spans (not only roots).
5. Set retention tiers; drop or sample low-value high-cardinality series.
6. Validate with a game-day: can you diagnose last incident from telemetry alone?

## Decision guide

- Page on symptom SLIs; ticket on causes.
- If AI/ML workloads → add accelerator/utilization and nondeterministic-output aware signals (see sre-supports-ai).

## Output template

```markdown
# Observability plan
- Service / CUJ:
- Golden signals + sources:
- Trace strategy:
- Log strategy + PII concerns:
- Dashboards (symptom vs cause):
- Retention / cardinality budget:
```

## Anti-patterns

- Paging on CPU alone.
- Infinite-cardinality labels (user_id on every metric).
- Dashboards nobody uses during incidents.

## Related skills

`alerting-on-slos`, `anomaly-detection`, `effective-troubleshooting`, `ai-supports-sre`

## Canonical references

- [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Workbook Monitoring](https://sre.google/workbook/monitoring/)
- [SRE on Google Cloud](https://sre.google/cloud/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
