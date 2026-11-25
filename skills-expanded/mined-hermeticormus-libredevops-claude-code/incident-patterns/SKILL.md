---
name: incident-patterns
description: "Incident management patterns: a severity and response matrix, PagerDuty schedules and escalation, multi-window SLO burn rate alerts, a postmortem template, and incident channel communication. Use when setting up on-call and alerting, or when running an incident and its postmortem."
---

# Incident Patterns

Severity matrix, SLO burn rate alerts, postmortem template, on-call setup, and runbook structure.

## Incident Severity and Response Matrix

```
P1 - CRITICAL
├── Criteria: Production down, data loss, auth down, payment processing down
├── Page: Immediately (PagerDuty high-urgency)
├── Bridge: Open immediately, notify engineering manager at 15min
├── Status page: Update within 10 minutes
└── Resolution SLA: 2 hours

P2 - HIGH
├── Criteria: >25% error rate, major feature broken, SLO burn >5x
├── Page: PagerDuty, 30-minute response SLA
├── Status page: Update within 30 minutes if user-facing
└── Resolution SLA: 4 hours

P3 - MEDIUM
├── Criteria: Partial degradation, workaround available
├── Notify: Slack channel, team lead
└── Resolution SLA: Next business day

P4 - LOW
├── Criteria: Minor issue, no user impact, internal tools
├── Track: Create ticket, no immediate action
└── Resolution SLA: 1 week
```

## PagerDuty Schedule and Escalation

```yaml
# PagerDuty as code (via Terraform)
resource "pagerduty_schedule" "platform_oncall" {
  name      = "Platform On-Call"
  time_zone = "UTC"

  layer {
    name                         = "Primary"
    start                        = "2024-01-01T00:00:00Z"
    rotation_virtual_start       = "2024-01-01T00:00:00Z"
    rotation_turn_length_seconds = 604800  # 1 week

    users = [
      pagerduty_user.alice.id,
      pagerduty_user.bob.id,
      pagerduty_user.carol.id,
    ]
  }
}

resource "pagerduty_escalation_policy" "platform" {
  name = "Platform Escalation"

  rule {
    escalation_delay_in_minutes = 5
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.platform_oncall.id
    }
  }

  rule {
    escalation_delay_in_minutes = 30
    target {
      type = "user_reference"
      id   = pagerduty_user.team_lead.id
    }
  }

  rule {
    escalation_delay_in_minutes = 60
    target {
      type = "user_reference"
      id   = pagerduty_user.engineering_manager.id
    }
  }
}
```

## SLO Burn Rate Alerting (Multi-Window)

```yaml
# prometheus/rules/slo-alerts.yml
groups:
  - name: slo-burn-rate
    rules:
      # Error budget: 0.1% error rate (99.9% SLO)
      # Monthly budget: 43.8 minutes
      # 14.4x burn = depletes in <2hr
      # 6x burn = depletes in <5hr

      - alert: SLO_FastBurn_P1
        expr: |
          (
            sum(rate(http_requests_total{status=~"5..",service="myapp"}[1h]))
            /
            sum(rate(http_requests_total{service="myapp"}[1h]))
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
          pagerduty: "high"
        annotations:
          summary: "P1: Fast SLO burn on myapp"
          description: "Error rate {{ $value | humanizePercentage }} exceeds 14.4x burn rate. Error budget depleting rapidly."
          runbook: "https://wiki.example.com/runbooks/myapp-errors"

      - alert: SLO_SlowBurn_P2
        expr: |
          (
            sum(rate(http_requests_total{status=~"5..",service="myapp"}[6h]))
            /
            sum(rate(http_requests_total{service="myapp"}[6h]))
          ) > (6 * 0.001)
          and
          (
            sum(rate(http_requests_total{status=~"5..",service="myapp"}[30m]))
            /
            sum(rate(http_requests_total{service="myapp"}[30m]))
          ) > (6 * 0.001)
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "P2: Slow SLO burn on myapp"
          description: "Sustained {{ $value | humanizePercentage }} error rate will deplete monthly error budget in <5 hours."

      # Latency SLO: 95% of requests < 500ms
      - alert: SLO_LatencyBurn
        expr: |
          (
            sum(rate(http_request_duration_seconds_bucket{service="myapp",le="0.5"}[1h]))
            /
            sum(rate(http_request_duration_seconds_count{service="myapp"}[1h]))
          ) < 0.95
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Latency SLO burn: {{ $value | humanizePercentage }} of requests < 500ms"
```

## Postmortem Template

```markdown
# Postmortem: [Service] [Brief Description]

**Date**: [YYYY-MM-DD]
**Duration**: [HH:MM]
**Severity**: P[1-4]
**Authors**: [names]
**Status**: Draft / In Review / Final

## Executive Summary
[3 sentences: what happened, impact, what we're doing about it]

## Impact
- **Users affected**: ~[N] users ([X]% of user base)
- **Duration**: [start time UTC] to [end time UTC] ([HH:MM])
- **Error rate**: [peak]% (normal: [baseline]%)
- **Revenue impact**: ~$[N] based on [calculation method]
- **SLO**: Burned [X]% of monthly error budget

## Timeline (all times UTC)

| Time  | Event |
|-------|-------|
| 14:32 | Alert fired: `SLO_FastBurn` (error rate 4.3%) |
| 14:37 | On-call acknowledged alert |
| 14:41 | Opened bridge call, declared P1 |
| 14:45 | First status page update |
| 14:52 | Identified: deploy at 14:20 introduced null pointer exception in payment handler |
| 14:55 | Decision: roll back deployment |
| 15:03 | Rollback complete, error rate dropping |
| 15:08 | Error rate below threshold, monitoring |
| 15:15 | Declared resolved, final status update |

## Root Cause
[Technical explanation: what failed and why. Not "human error" -- what allowed the human to make this mistake?]

## Contributing Factors
1. **Technical**: No integration test covering null payment provider config
2. **Process**: Deployment went to production without staging verification
3. **Tooling**: Error alert threshold set too high (1%) -- didn't fire for 5 minutes at 0.8% error rate

## What Went Well
- Alert fired quickly and on-call responded within 5 minutes
- Rollback procedure was documented and executed in 8 minutes
- Status page updates were timely

## What Could Be Improved
- No canary deployment -- change went straight to 100% traffic
- Missing test coverage for payment configuration

## Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| Add null check test for payment config | @alice | 2024-01-22 | High |
| Enable canary deployments for payment service | @bob | 2024-02-01 | High |
| Lower alert threshold from 1% to 0.5% | @carol | 2024-01-19 | Medium |
| Add staging deploy gate to payment service pipeline | @bob | 2024-02-01 | High |
| Document rollback procedure in runbook | @alice | 2024-01-19 | Low |
```

## Incident Channel Communication

```
# Slack #incidents channel format

[P1 DECLARED] 14:41 UTC
Service: Payment Processing
Impact: Users cannot complete checkout
Error rate: 4.3% (normal: 0.02%)
Bridge: [zoom link]
IC: @alice
Status page: https://status.example.com
Runbook: https://wiki.example.com/runbooks/payments

[UPDATE] 14:55 UTC - Root cause identified
Cause: Deploy at 14:20 introduced null pointer exception in PaymentHandler
Action: Rolling back deployment now
ETA: ~10 minutes

[RESOLVED] 15:15 UTC
Service recovered. Error rate: 0.02% (normal).
Duration: 43 minutes
Postmortem: To be published within 48 hours at [confluence link]
```
