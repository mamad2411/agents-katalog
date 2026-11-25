---
name: do-observability
version: 1.0.0
description: Instrument logs, metrics, and traces with OpenTelemetry, then define SLOs and burn-rate alerts that page only on real user pain.
author: matrixx0070
tags: [observability, monitoring, slo, telemetry, alerting, opentelemetry]
capabilities: []
---

# do-observability

## When to use

You need to add or improve instrumentation on a service, define what "healthy" means as SLOs, or replace noisy alerts with ones that page only on real user impact.

**Not for:** writing the on-call response steps (use do-incident-runbook), Kubernetes probes/resources (use do-kubernetes), or CI test reporting (use do-ci-pipeline).

## Method

1. Cover the three pillars: structured logs (JSON, leveled, correlation IDs), metrics (RED for services — Rate, Errors, Duration; USE for resources — Utilization, Saturation, Errors), and distributed traces across service boundaries.
2. Standardize on OpenTelemetry for vendor-portable instrumentation; propagate trace context through every hop and attach the trace ID to logs.
3. Define SLIs from the user's perspective (successful requests, latency percentiles). Decision: set the SLO target where users actually feel pain (e.g. p99 < 300ms), not at an arbitrary round number; derive an error budget from it.
4. Alert on symptoms, not causes: page on SLO burn rate. Decision: use a fast-burn window (minutes) for acute outages and a slow-burn window (hours) for gradual erosion; every page links a runbook.
5. Build dashboards that answer "is it the service, its dependencies, or the infra?" and expose golden signals at a glance.
6. Control cost and cardinality: sample traces, bound label dimensions, and set retention deliberately.

## Example

```yaml
# SLO: 99.9% of requests succeed over 30d -> ~43m budget/month
# Fast-burn alert: 2% budget consumed in 1h -> page now
- alert: CheckoutErrorBudgetFastBurn
  expr: |
    sum(rate(http_requests_total{job="checkout",code=~"5.."}[5m]))
      / sum(rate(http_requests_total{job="checkout"}[5m]))
    > (14.4 * 0.001)          # 14.4x burn of a 0.1% error SLO
  for: 2m
  labels: { severity: page }
  annotations: { runbook: "https://runbooks/checkout" }
```

## Pitfalls

- Alerting on causes (CPU 80%, pod restart) instead of symptoms — you page for conditions users never notice and miss the ones they do.
- Unbounded label cardinality (user ID, full URL as a metric label) — the metrics backend cost and latency explode.
- Averages instead of percentiles: a fine-looking mean hides the p99 tail where real users suffer.
- Logs without a shared correlation/trace ID, so you cannot stitch one request across services.

## Output format

```
Instrumentation: log schema, metric definitions, trace setup snippets.

SLI/SLO table:
| SLI | target | window | error budget |

Alerts:
| alert | burn rate | window | severity | runbook |
```
