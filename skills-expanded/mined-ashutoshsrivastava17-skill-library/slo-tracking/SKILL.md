---
name: slo-tracking
description: >
  Define and track Service Level Objectives — SLI selection, error budget calculation,
  burn rate alerts, reporting cadence, and escalation procedures.
  TRIGGER when: user says /slo-tracking, asks to define SLOs, calculate error budgets,
  set up SLO monitoring, or establish reliability targets.
argument-hint: "[service name, current SLOs, or reliability requirements]"
user-invocable: true
---

# SLO Tracking & Error Budget Management

You are a senior SRE establishing and managing SLOs. Produce well-defined SLOs with measurable SLIs, actionable error budgets, and clear escalation procedures.

## Process

### Step 1: Understand the Service

Before defining SLOs, determine:
- What is the service and who are its users? (external customers, internal teams, API consumers)
- What are the critical user journeys? (login, checkout, search, data export)
- What are the current reliability metrics? (if any exist)
- What is the business impact of downtime or degradation?
- What are contractual SLA obligations? (SLOs should be stricter than SLAs)
- What is the team's capacity to respond to reliability issues?

### Step 2: Select SLIs (Service Level Indicators)

Choose SLIs based on the service type:

| Service Type | Recommended SLIs | Measurement Point |
|-------------|-----------------|-------------------|
| **Request-driven (API, web)** | Availability (success rate), Latency (P50, P99), Throughput | Load balancer, application metrics |
| **Data processing (pipeline, ETL)** | Freshness (data age), Correctness (validation pass rate), Coverage (% records processed) | Pipeline output, validation checks |
| **Storage (database, object store)** | Availability (read/write success), Durability (data loss events), Latency | Client-side instrumentation |
| **Streaming (Kafka, event bus)** | Throughput (events/sec), Freshness (consumer lag), Availability (produce success) | Producer/consumer metrics |
| **Scheduled jobs (cron, batch)** | Execution success rate, Timeliness (completed within window), Correctness | Job scheduler metrics |

**SLI Specification Template:**

| Field | Description | Example |
|-------|-------------|---------|
| **Name** | Descriptive name | HTTP Availability |
| **Description** | What it measures | Proportion of HTTP requests that return a non-5xx status |
| **Good Event** | Definition of a successful event | HTTP response status < 500 |
| **Valid Event** | All events in scope (denominator) | All HTTP requests excluding health checks |
| **Measurement** | Where and how it is measured | Load balancer access logs, counted per 1-minute window |
| **Data Source** | Specific metric or log query | `sum(rate(http_requests_total{status!~"5.."}[1m])) / sum(rate(http_requests_total[1m]))` |

### Step 3: Set SLO Targets

| SLO Target | Monthly Downtime Budget | Nines | Typical Use Case |
|-----------|------------------------|-------|------------------|
| 99.0% | 7 hours 18 min | Two nines | Internal tools, batch processing |
| 99.5% | 3 hours 39 min | Two and a half nines | Internal APIs, staging environments |
| 99.9% | 43 min 50 sec | Three nines | Customer-facing web services |
| 99.95% | 21 min 55 sec | Three and a half nines | Payment processing, core APIs |
| 99.99% | 4 min 23 sec | Four nines | Infrastructure services, DNS, auth |

**Guidelines for Setting Targets:**
- Start conservative (lower target) and tighten over time based on data
- SLO target must be stricter than any external SLA commitment
- Different SLIs for the same service can have different targets
- Factor in planned maintenance windows
- Consider dependencies — your SLO cannot exceed the worst-case SLO of your critical dependencies

### Step 4: Calculate Error Budgets

**Error Budget Formula:**
```
Error Budget = 1 - SLO Target
Monthly Budget (minutes) = Error Budget x Total Minutes in Period

Example:
  SLO = 99.9%
  Error Budget = 0.1%
  Monthly Budget = 0.001 x 43,200 minutes = 43.2 minutes of downtime
```

**Error Budget Tracking Table:**

| Metric | Formula | Example (99.9% SLO, 30-day window) |
|--------|---------|-------------------------------------|
| Total budget | `(1 - SLO) x window_minutes` | 43.2 minutes |
| Budget consumed | `bad_minutes / total_budget x 100%` | 15 min / 43.2 min = 34.7% |
| Budget remaining | `total_budget - bad_minutes` | 28.2 minutes |
| Projected depletion | `budget_remaining / daily_burn_rate` | 28.2 min / 0.5 min/day = 56 days |
| Budget status | Green / Yellow / Red | Green (< 50% consumed with > 50% window remaining) |

**Budget Status Thresholds:**

| Status | Condition | Action |
|--------|-----------|--------|
| **Green** | Budget consumed % < Window elapsed % | Normal operations, feature work proceeds |
| **Yellow** | Budget consumed % exceeds Window elapsed % by < 20 points | Prioritize reliability work, limit risky deploys |
| **Red** | Budget consumed % exceeds Window elapsed % by > 20 points | Freeze feature releases, all hands on reliability |
| **Exhausted** | 100% of error budget consumed | Full feature freeze until budget recovers or window resets |

### Step 5: Configure Burn Rate Alerts

Burn rate alerts detect when the error budget is being consumed too quickly.

| Alert Name | Burn Rate | Window | Budget Consumed | Severity | Response |
|-----------|-----------|--------|----------------|----------|----------|
| **Fast Burn (acute)** | 14.4x | 1 hour | 2% of 30-day budget | Critical | Page on-call immediately |
| **Fast Burn (sustained)** | 6x | 6 hours | 5% of 30-day budget | Critical | Page on-call |
| **Slow Burn (emerging)** | 3x | 1 day | 10% of 30-day budget | Warning | Notify team channel |
| **Slow Burn (chronic)** | 1.5x | 3 days | 15% of 30-day budget | Warning | Triage in next planning |

**Multi-Window Alert Pattern (recommended):**
Each alert should use two windows — a long window to detect the trend and a short window to confirm it is still happening:
- Fast burn: 1-hour long window AND 5-minute short window
- Slow burn: 3-day long window AND 6-hour short window
- This prevents alerting on brief spikes that have already resolved

### Step 6: Establish Reporting & Escalation

**Reporting Cadence:**

| Report | Frequency | Audience | Content |
|--------|-----------|----------|---------|
| **SLO Dashboard** | Real-time | On-call, engineering | Current SLI values, budget remaining, burn rate |
| **Weekly SLO Summary** | Weekly | Engineering team | Budget consumption trend, incidents impacting SLO, action items |
| **Monthly SLO Review** | Monthly | Engineering + management | SLO attainment, budget analysis, reliability investments, target adjustments |
| **Quarterly Business Review** | Quarterly | Leadership | SLO vs SLA, customer impact, reliability roadmap |

**Escalation Procedure:**

1. **Budget > 50% consumed before mid-window:** Engineering lead reviews active issues, prioritizes fixes
2. **Budget > 75% consumed:** Skip-level escalation, defer non-critical feature work, staff reliability sprint
3. **Budget exhausted:** Feature freeze communicated to product and leadership, all engineering effort on reliability
4. **SLA breach imminent:** Executive escalation, customer communication plan activated, incident commander assigned

## Output Format

```
## SLO Definitions: [Service Name]

### Service Overview
[Brief description, users, critical journeys]

### SLI Definitions
[Table of SLIs with specification details]

### SLO Targets
[Table of SLOs with targets and rationale]

### Error Budget Status
[Current budget consumption, projection, status]

### Burn Rate Alerts
[Alert definitions with thresholds and routing]

### Reporting & Governance
[Cadence, audience, escalation procedures]

### Implementation Tasks
[Prioritized checklist to implement SLO tracking]
```

## Quality Checklist

- [ ] SLIs measure user experience, not internal system metrics
- [ ] SLO targets are based on data (historical reliability) and business needs, not arbitrary
- [ ] Error budget calculation is correct and accounts for the measurement window
- [ ] Burn rate alerts use multi-window approach to reduce false positives
- [ ] Reporting cadence is established with clear ownership
- [ ] Escalation procedure is documented and agreed upon with management
- [ ] SLOs are stricter than any external SLA commitments
- [ ] Dashboard shows real-time SLO status, error budget, and burn rate
- [ ] Planned maintenance is accounted for in error budget calculations
- [ ] SLO definitions are version-controlled and reviewed quarterly

## Edge Cases

- **New Services Without Baseline:** Run in "observation mode" for 2-4 weeks. Collect SLI data without enforcing SLOs. Set initial targets at the observed P10 (10th percentile of performance) to ensure the target is achievable.
- **Shared Dependencies:** If multiple services depend on the same database or API, define SLOs for the dependency itself. Downstream service SLOs should account for dependency SLO limits.
- **Multi-Region Failover:** Define SLOs at the global level (user-perceived) and per-region level (operational). Global SLO should survive a single-region failure. Regional SLO helps detect issues before they affect global numbers.
- **Seasonal Traffic:** Use rolling windows instead of calendar months. Consider different SLO targets for peak vs. normal periods, or accept higher budget consumption during peak seasons.
- **Partial Degradation:** Define what counts as "degraded but available" vs. "unavailable." A service returning cached/stale data may count as available for an availability SLI but bad for a correctness SLI.
- **SLO Conflicts:** When improving one SLI degrades another (e.g., adding retries improves availability but increases latency), prioritize the SLI that most directly impacts user satisfaction.
