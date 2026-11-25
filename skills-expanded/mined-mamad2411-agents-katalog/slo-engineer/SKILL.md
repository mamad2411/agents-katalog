---
name: slo-engineer
description: "Defines Service Level Objectives (SLOs) and SLIs for a service: identifies the right metrics to measure, sets realistic targets, calculates error budgets (30-day rolling), and generates burn-rate alert rules. Outputs an SLO spec document plus Prometheus/alertmanager configuration. Triggers: SLO, SLI, error budget, service level objective, reliability target, 99.9%, uptime, latency target, burn rate alert, 服務可靠性, 服務等級."
metadata:
  category: dev
---

## Purpose

Turn "we need 99.9% uptime" into a measurable, actionable reliability contract. Define what to measure (SLI), what to aim for (SLO), how much failure is budgeted (error budget), and when to alert before the budget burns out (burn rate alerts).

## Trigger

Apply when:
- "define SLO", "set reliability target", "error budget", "服務等級"
- "what should our uptime target be", "burn rate alert", "99.9%"
- Service is going to production and needs a reliability baseline
- Incident postmortem identified the need for formal SLOs

Do NOT trigger for:
- Setting up monitoring dashboards — use `observability-designer` instead
- General infrastructure setup — use `ci-cd-pipeline-builder` instead

## Prerequisites

- Service name and type (API, background job, data pipeline, UI)
- Traffic profile: rough RPS, P50/P95 latency expectations
- Downstream dependencies (databases, external APIs)

## Steps

### Step 1 — Choose the Right SLIs

Select SLIs that directly correlate with user experience. Ask:

> "What does a user notice when this service is degraded?"

| Service Type | Recommended SLIs |
|-------------|-----------------|
| HTTP API | Availability (% successful requests), Latency (P95, P99) |
| Background job / queue | Freshness (max age of processed item), Error rate |
| Data pipeline | Completeness (% records processed), Freshness (pipeline lag) |
| Storage service | Durability (% reads returning correct data), Availability |
| UI / Frontend | Interaction success rate, Core Web Vitals (LCP, CLS, INP) |

**SLI formula:**
```
Availability SLI = good_requests / total_requests
Latency SLI     = requests_under_threshold / total_requests
Error Rate SLI  = (total_requests - error_requests) / total_requests
```

Where `good` = HTTP 2xx/3xx (excluding expected 4xx), latency < agreed threshold.

### Step 2 — Set Realistic SLO Targets

Start conservative. A 99.9% SLO you can meet beats a 99.99% SLO you'll constantly violate.

| SLO Target | Monthly error budget | Appropriate for |
|-----------|---------------------|-----------------|
| 99.0% | 7h 18m | Internal tools, batch jobs |
| 99.5% | 3h 39m | Non-critical production APIs |
| 99.9% | 43m 48s | Standard production services |
| 99.95% | 21m 54s | High-traffic user-facing services |
| 99.99% | 4m 22s | Payment, auth, core infra |

**Rule:** SLO = observed reliability over past 90 days minus one nines. Never set an SLO you haven't already been achieving.

### Step 3 — Calculate Error Budget

```
Error Budget (time) = (1 - SLO) × window_duration
Error Budget (requests) = (1 - SLO) × total_requests_in_window

Example (99.9% SLO, 30-day window):
= (1 - 0.999) × 30 × 24 × 60
= 43.8 minutes of downtime allowed per month
```

Define error budget policy:
- Budget > 50% remaining → release cadence normal
- Budget 10–50% remaining → increased scrutiny on releases
- Budget < 10% remaining → freeze non-critical changes
- Budget exhausted → incident declared, root cause required before next release

### Step 4 — Design Burn Rate Alerts

Alert before the budget is exhausted, not after. Use multi-window burn rate alerts:

| Alert | Burn Rate | Window | Severity | Meaning |
|-------|-----------|--------|----------|---------|
| Page immediately | 14.4× | 1h | P0 | Will exhaust 30d budget in 2h |
| Page | 6× | 6h | P1 | Will exhaust 30d budget in 5d |
| Ticket | 3× | 1d (72h+24h) | P2 | Will exhaust 30d budget in 10d |
| Warning | 1× | 3d | Info | Burning exactly at budget rate |

Burn rate formula:
```
burn_rate = error_rate / (1 - SLO)

Example: If SLO = 99.9% and current error rate = 1.44%
burn_rate = 0.0144 / 0.001 = 14.4× → fire P0 page alert
```

### Step 5 — Generate Artifacts

Produce two files: `slo-spec.md` and `slo-alerts.yml`.

## Output Format

**slo-spec.md:**
```markdown
# SLO Specification: [Service Name]
_Owner: [team]  Review: quarterly_

## SLIs
| Metric | Definition | Good Event |
|--------|-----------|-----------|
| Availability | HTTP 2xx/3xx / total_requests | HTTP status < 500 |
| Latency P95  | % requests < 300ms | response_time < 300ms |

## SLOs (30-day rolling)
| SLI | Target | Error Budget |
|-----|--------|-------------|
| Availability | 99.9% | 43m 48s |
| Latency P95  | 95%   | — |

## Error Budget Policy
- > 50% remaining: normal releases
- < 10% remaining: change freeze (P2 and below)
- Exhausted: incident, freeze all non-P0 work
```

**slo-alerts.yml (Prometheus / alertmanager):**
```yaml
groups:
  - name: slo-[service-name]
    rules:
      - alert: SLOBurnRateCritical
        expr: |
          (
            sum(rate(http_requests_total{job="[service]",status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total{job="[service]"}[1h]))
          ) > 0.01440
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "14.4x burn rate — exhausts 30d budget in 2h"

      - alert: SLOBurnRateHigh
        expr: |
          (
            sum(rate(http_requests_total{job="[service]",status=~"5.."}[6h]))
            /
            sum(rate(http_requests_total{job="[service]"}[6h]))
          ) > 0.00600
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "6x burn rate — exhausts 30d budget in 5d"
```

## Rules

### Must
- Set SLO based on observed historical data, not aspirational targets
- Define error budget policy before going live — not after the first incident
- Use multi-window burn rate alerts (1h + 6h at minimum) to reduce alert fatigue
- Review SLOs quarterly and adjust based on actual performance data
- Exclude expected client errors (4xx) from availability SLI calculations

### Never
- Never set 100% SLO — this makes every incident an SLO violation with no budget to improve
- Never alert only on SLO breach — by then the budget is already consumed; alert on burn rate
- Never conflate SLA (contractual) with SLO (internal target) — SLO should be stricter than SLA
- Never use uptime monitors (ping checks) as a proxy for user-facing availability

## Examples

### Good Example

```
Service: Order API
SLI: availability = HTTP 2xx-3xx / total_requests (excluding 4xx)
SLO: 99.9% over 30-day rolling window
Error budget: 43m 48s / month

Alert: 14.4× burn rate over 1h → P0 page (exhausts budget in 2h)
Alert: 6× burn rate over 6h → P1 page (exhausts budget in 5 days)
Alert: 3× burn rate over 72h → P2 ticket (exhausts budget in 10 days)
```

### Bad Example

```
We need 99.99% uptime. Set up an alert if the service goes down.
```

> Why this is bad: 99.99% means only 4 minutes of downtime per month — almost certainly unachievable for a service with deployments. "Alert if down" is a binary check that fires after the damage is done; burn-rate alerts give time to react before budget exhaustion.
