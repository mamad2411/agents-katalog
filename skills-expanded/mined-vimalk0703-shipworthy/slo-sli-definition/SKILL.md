---
name: slo-sli-definition
description: Define SLIs (what to measure), SLOs (target values), SLAs (business contracts), error budgets (calculation and usage), and burn rate alerting for production services.
invoke_when: Use when defining reliability targets, setting up monitoring, discussing SLOs/SLIs/SLAs, configuring alerts, planning capacity, or evaluating error budgets for deployment decisions.
---

# SLO/SLI Definition

## Core Principle

Reliability is a feature. SLOs quantify how reliable a service needs to be, error budgets tell you when to slow down, and burn rate alerts tell you when reliability is degrading faster than your budget allows.

---

## Terminology

| Term | What It Is | Who Defines It | Example |
|---|---|---|---|
| **SLI** (Service Level Indicator) | A quantitative measure of service behavior | Engineering | 99.2% of requests return 2xx in < 500ms |
| **SLO** (Service Level Objective) | A target value for an SLI over a time window | Engineering + Product | 99.9% availability over 30 days |
| **SLA** (Service Level Agreement) | A contract with customers including consequences for failure | Business + Legal | 99.95% uptime or customer gets credits |
| **Error Budget** | The allowed amount of unreliability (1 - SLO) | Derived from SLO | 0.1% = 43.2 minutes of downtime per 30 days |

**Key relationship:** SLA >= SLO > SLI measurement. Your SLO should be stricter than your SLA, and your SLI measurement should be honest.

---

## 1. SLIs -- What to Measure

Choose SLIs based on what users actually experience. The four golden signals:

### Availability

**Definition:** The proportion of valid requests that are served successfully.

```
availability = (total_requests - error_requests) / total_requests
```

What counts as an error:
- HTTP 5xx responses (server errors).
- Timeouts (no response within the timeout budget).
- HTTP 429 responses should NOT count as errors (the server is protecting itself).
- HTTP 4xx responses should NOT count as errors (client mistakes).

### Latency

**Definition:** The proportion of requests served faster than a threshold.

```
latency_sli = requests_under_threshold / total_requests
```

Measure at the p50, p95, and p99 percentiles. The SLO is typically on p99 or p95.

**Important:** Measure latency at the load balancer or API gateway, not inside the application. The user experiences the full round trip.

### Throughput

**Definition:** The rate of requests the system handles. Not always used as an SLI directly, but important for capacity planning.

### Correctness (Data SLI)

**Definition:** The proportion of operations that produce correct results. Critical for data pipelines and financial systems.

```
correctness = correct_outputs / total_outputs
```

### Freshness (Data SLI)

**Definition:** The proportion of data that is updated within the expected time window. Critical for data pipelines and caches.

```
freshness = records_updated_within_threshold / total_records
```

---

## 2. SLOs -- Target Values

### Choosing the Right SLO

| Service Type | Typical Availability SLO | Typical Latency SLO |
|---|---|---|
| User-facing API (checkout, auth) | 99.95% (26 min downtime/month) | p99 < 300ms |
| User-facing API (non-critical) | 99.9% (43 min downtime/month) | p99 < 500ms |
| Internal service | 99.9% (43 min downtime/month) | p99 < 1s |
| Batch data pipeline | 99.5% (3.6 hrs downtime/month) | Jobs complete within 2x expected |
| Async message processing | 99.9% processing success | 99% processed within 60s |

**Rules for choosing SLOs:**

1. Start with a lower SLO and tighten it. It is much harder to loosen an SLO than to tighten one.
2. Your SLO must be achievable. Check the last 90 days of data before setting the target.
3. Your SLO must be stricter than your SLA. If your SLA promises 99.9%, your SLO should be 99.95%.
4. Different endpoints can have different SLOs. The login endpoint may need 99.99%; a reporting endpoint may need 99.5%.

---

## 3. Error Budgets -- Calculation and Usage

### Calculating the Error Budget

```
error_budget = 1 - SLO

For 99.9% SLO over 30 days:
  error_budget = 0.1% = 0.001
  total_minutes = 30 * 24 * 60 = 43,200 minutes
  allowed_downtime = 43,200 * 0.001 = 43.2 minutes

For request-based SLO at 99.9% with 1M requests/month:
  allowed_failures = 1,000,000 * 0.001 = 1,000 failed requests
```

### Using the Error Budget

The error budget is the mechanism that balances feature velocity with reliability.

| Error Budget Status | Action |
|---|---|
| > 50% remaining | Ship features at full speed. Take calculated risks. |
| 25-50% remaining | Proceed with caution. Prioritize reliability-related work. |
| 10-25% remaining | Freeze risky deployments. Focus on stability improvements. |
| < 10% remaining | Feature freeze. All engineering effort goes to reliability. |
| Exhausted (0%) | Only reliability fixes and rollbacks are deployed. |

### Error Budget Policy Template

```markdown
## Error Budget Policy for [Service Name]

**SLO:** 99.9% availability measured over a rolling 30-day window.
**Error Budget:** 43.2 minutes of downtime per 30 days.

**When budget > 50%:**
- Normal feature development pace.
- Deployments proceed as usual.

**When budget 10-50%:**
- All deployments require explicit approval from the on-call engineer.
- Risky changes (new dependencies, schema migrations) are deferred.

**When budget < 10%:**
- Feature freeze. Only reliability improvements and bug fixes are deployed.
- Incident review for all budget-consuming events.
- Daily stand-up includes error budget status.

**When budget is exhausted:**
- Complete deployment freeze except for reliability fixes.
- Escalation to engineering leadership.
- Post-mortem required for each budget-consuming event.
```

---

## 4. Burn Rate Alerting

**Problem:** Traditional threshold alerts (e.g., "alert if error rate > 1%") are either too noisy or too slow. Burn rate alerting solves this by asking: "At the current rate of errors, when will we exhaust our error budget?"

### Burn Rate Definition

```
burn_rate = (actual_error_rate) / (error_budget_rate)

Where error_budget_rate = (1 - SLO) / SLO_window_in_hours

For 99.9% SLO over 30 days:
  error_budget_rate = 0.001 / 720 hours = 0.00000139 per hour

If actual errors are consuming budget at 10x the sustainable rate:
  burn_rate = 10
  Budget will be exhausted in 720 / 10 = 72 hours (3 days)
```

### Multi-Window, Multi-Burn-Rate Alerts

Set up two types of alerts with different urgency levels:

| Alert | Burn Rate | Long Window | Short Window | Action |
|---|---|---|---|---|
| Page (wake someone up) | 14.4x | 1 hour | 5 minutes | Budget gone in ~2 days |
| Page (urgent) | 6x | 6 hours | 30 minutes | Budget gone in ~5 days |
| Ticket (next business day) | 3x | 3 days | 6 hours | Budget gone in ~10 days |
| Ticket (low priority) | 1x | 7 days | 1 day | On track to exhaust budget |

Both windows must be in violation to fire the alert. The long window prevents alert noise; the short window ensures fast detection.

### Prometheus Example

```yaml
# Alert: High burn rate (page-worthy)
- alert: HighErrorBudgetBurn
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    ) > (14.4 * 0.001)
    and
    (
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))
    ) > (14.4 * 0.001)
  for: 2m
  labels:
    severity: page
  annotations:
    summary: "Error budget burning at 14.4x -- will exhaust in ~2 days"
    dashboard: "https://grafana.internal/d/slo-dashboard"
```

---

## 5. SLO Definition Template

Use this template for every production service:

```markdown
## SLO Definition: [Service Name]

**Owner:** [Team Name]
**Last Reviewed:** [Date]
**Review Cadence:** Quarterly

### SLIs

| SLI | Measurement | Data Source |
|---|---|---|
| Availability | % of requests returning non-5xx | Load balancer access logs |
| Latency (p99) | 99th percentile response time | Application metrics (histogram) |
| Correctness | % of orders with matching totals | Reconciliation job |

### SLOs

| SLI | Target | Window | Error Budget |
|---|---|---|---|
| Availability | 99.9% | 30 days rolling | 43.2 min / 1,000 errors per 1M requests |
| Latency (p99) | < 500ms | 30 days rolling | 0.1% of requests may exceed 500ms |
| Correctness | 99.99% | 30 days rolling | 100 incorrect orders per 1M |

### Error Budget Policy

[Link to error budget policy document]

### Alerts

| Alert | Condition | Severity | Notification |
|---|---|---|---|
| High burn rate | 14.4x over 1h + 5m | Page | PagerDuty |
| Elevated burn rate | 6x over 6h + 30m | Page | PagerDuty |
| Slow burn | 3x over 3d + 6h | Ticket | Jira |

### SLA (if applicable)

| Metric | Guarantee | Consequence |
|---|---|---|
| Availability | 99.9% monthly | Service credits: 10% for each 0.1% below SLA |

### Dependencies

| Service | Their SLO | Impact if Down |
|---|---|---|
| Database (RDS) | 99.95% | Full outage |
| Cache (Redis) | 99.9% | Degraded latency |
| Payment Provider | 99.9% | Cannot process payments |
```

---

## Checklist

- [ ] Every production service has documented SLIs and SLOs.
- [ ] SLOs are based on actual historical performance, not aspirational targets.
- [ ] Error budgets are calculated and tracked on a dashboard.
- [ ] Burn rate alerts are configured with multi-window, multi-burn-rate rules.
- [ ] An error budget policy exists that defines actions at each budget threshold.
- [ ] SLOs are reviewed quarterly and adjusted based on business needs.
- [ ] The SLO is stricter than the SLA.
- [ ] SLIs are measured from the user's perspective (at the load balancer, not inside the app).
