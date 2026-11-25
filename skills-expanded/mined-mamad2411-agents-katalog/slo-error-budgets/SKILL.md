---
name: slo-error-budgets
description: Define SLIs, SLOs, error budgets, and multi-window multi-burn-rate alerts using OpenSLO and SRE practices. Use when establishing reliability targets or replacing symptom-based alerts with budget-driven ones.
---

# SLO and Error Budgets

SLOs turn reliability into a budget that engineering and product share. Burn-rate alerts page on actual user impact, not on every CPU spike. Codify everything so the spec, dashboard, and alert never drift.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Reference | Google SRE Workbook (Implementing SLOs, Alerting on SLOs) |
| Spec | OpenSLO 1.0 |
| Tooling | Sloth, OpenSLO + sloth-cli, Nobl9, Datadog/Grafana SLOs, Pyrra |
| Metrics backend | Prometheus 3 native histograms, OpenTelemetry |
| Alerting | Multi-window multi-burn-rate (MWMBR) |
| Dashboards | Grafana SLO panels with burn rate and remaining budget |
| Policy | Error budget policy: who pauses what when budget burns |

## When to Use
- New tier-1 service or critical user journey.
- Alert fatigue: pages don't correlate with user pain.
- Reliability is debated subjectively ("it feels slow").
- Cross-team dependency contracts need numeric SLAs underneath.

## Prerequisites
- Defined critical user journeys with owners.
- Telemetry that can compute SLI as `good_events / valid_events` with high cardinality avoided.
- Stakeholder agreement on consequences when budget is exhausted.

## Instructions

### 1. Pick SLIs per journey
Use request-based ratios. Prefer user-visible signals over internal proxies.

| Journey | SLI | Definition |
| --- | --- | --- |
| Checkout | Availability | non-5xx requests / total |
| Checkout | Latency | requests with p99 <= 300ms / total |
| Search | Freshness | events indexed within 60s / total |
| Login | Correctness | successful auths / attempted (excl. invalid creds) |

### 2. Set SLOs with explicit windows
```yaml
# OpenSLO 1.0
apiVersion: openslo/v1
kind: SLO
metadata:
  name: checkout-availability
  displayName: Checkout availability
spec:
  service: checkout
  indicator:
    metricSource:
      type: Prometheus
      spec:
        good:  "sum(rate(http_requests_total{job='checkout',code!~'5..'}[1m]))"
        total: "sum(rate(http_requests_total{job='checkout'}[1m]))"
  timeWindow:
    - duration: 28d
      isRolling: true
  objectives:
    - target: 0.999
```

### 3. Compute the error budget
```
budget_seconds  = (1 - SLO) * window
budget_requests = (1 - SLO) * total_requests_in_window
```
For 99.9% over 28 days: ~40m 19s downtime, or 0.1% of requests.

### 4. Configure multi-window multi-burn-rate alerts
Page on fast burns; ticket on slow burns. Two windows per severity to suppress flaps.

| Severity | Long window | Short window | Burn rate | Budget consumed if sustained |
| --- | --- | --- | --- | --- |
| Page  | 1h  | 5m  | 14.4 | 2% in 1h |
| Page  | 6h  | 30m | 6    | 5% in 6h |
| Ticket| 24h | 2h  | 3    | 10% in 24h |
| Ticket| 72h | 6h  | 1    | 10% in 72h |

```yaml
# Sloth -> Prometheus rules (excerpt)
version: prometheus/v1
service: checkout
slos:
  - name: availability
    objective: 99.9
    sli:
      events:
        error_query: 'sum(rate(http_requests_total{job="checkout",code=~"5.."}[{{.window}}]))'
        total_query: 'sum(rate(http_requests_total{job="checkout"}[{{.window}}]))'
    alerting:
      page_alert:   { labels: { severity: page },   annotations: { summary: "fast burn" } }
      ticket_alert: { labels: { severity: ticket }, annotations: { summary: "slow burn" } }
```

### 5. Visualize budget and burn
```mermaid
graph TD
  S[SLI streams] --> B[Burn rate (1h, 6h, 24h, 72h)]
  S --> R[Remaining budget %]
  B --> A[Alerts (page/ticket)]
  R --> D[Dashboard]
  D --> P[Product + SRE review]
```

### 6. Write and enforce an error budget policy
```markdown
# Error Budget Policy - Checkout
- If 28d budget < 0% (exhausted): freeze non-essential changes, focus on reliability.
- If burn rate > 10x for 1h: incident; rollback last change first.
- If budget healthy (> 50% remaining): change velocity unrestricted.
- Quarterly: renegotiate SLO if budget consistently > 80% (too loose) or < 0% (too tight).
```

### 7. Operate and review
- Weekly SLO review with product + SRE.
- Postmortems link to budget burn.
- Treat SLO definitions as code: versioned, reviewed, validated in CI (`opensloctl validate`, `sloth validate`).

## Common Pitfalls
| Pitfall | Why it bites | Mitigation |
| --- | --- | --- |
| One global SLO | Hides per-journey pain | SLO per critical user journey |
| Threshold alerts on SLI | Flaps and misses sustained burn | MWMBR alerts |
| 100% SLO targets | No budget = no innovation | Pick the lowest target users tolerate |
| Custom metrics that exclude failures | Inflated SLIs | Define `good` and `valid` precisely; exclude only invalid traffic |
| Policy without teeth | Reliability deprioritized when budget burns | Pre-agreed freeze + rollback rules |

## Output Format
- `slo/<service>.openslo.yaml`
- Generated Prometheus rules in `monitoring/`
- Grafana SLO dashboards as code
- `docs/reliability/error-budget-policy-<service>.md`
- Postmortem template referencing burn rate and budget

## Authoritative References
- [Google SRE Workbook - Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [Google SRE Workbook - Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [OpenSLO Specification](https://openslo.com/)
- [Sloth - Prometheus SLO Generator](https://sloth.dev/)
- [Pyrra](https://github.com/pyrra-dev/pyrra)
- [Nobl9 SLO Platform](https://www.nobl9.com/)
