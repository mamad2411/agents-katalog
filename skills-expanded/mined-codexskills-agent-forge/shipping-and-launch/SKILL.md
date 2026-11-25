# Shipping and Launch

## Description
Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.

## Core Philosophy: Ship Safely, Ship Often

Shipping is a skill, not an event. Reliable launches are boring launches. If shipping is exciting, you're not doing it frequently enough.

## Pre-Launch Checklist

### Code Readiness
- [ ] All tests pass (unit, integration, e2e)
- [ ] Code review completed and approved
- [ ] No debug code, console.logs, or TODO comments
- [ ] Lint and type-check pass
- [ ] Code coverage meets threshold (>= 80%)
- [ ] Security review completed for sensitive changes
- [ ] Migration scripts written and tested
- [ ] Feature flag implemented (if needed)
- [ ] Backward compatibility confirmed
- [ ] Performance tested (no regressions)

### Infrastructure Readiness
- [ ] Resource limits configured (CPU, memory, storage)
- [ ] Auto-scaling configured
- [ ] Health check endpoints working
- [ ] Database migrations tested (and reversible)
- [ ] CDN cache configured for static assets
- [ ] SSL certificates valid
- [ ] DNS records updated (if new domains)
- [ ] Load balancer configured
- [ ] Backup strategy verified
- [ ] Disaster recovery plan documented

### Monitoring Readiness
- [ ] Error tracking configured (Sentry, Bugsnag, etc.)
- [ ] APM configured (Datadog, New Relic, etc.)
- [ ] Custom metrics defined and emitting
- [ ] Dashboards created for key metrics
- [ ] Alerts configured (PagerDuty, OpsGenie, Slack)
- [ ] Log aggregation working
- [ ] Uptime monitoring configured
- [ ] Synthetic transactions set up (critical paths)
- [ ] SLOs/SLIs defined
- [ ] On-call rotation confirmed

### Communication Readiness
- [ ] Internal stakeholders notified
- [ ] Release notes drafted
- [ ] Changelog updated
- [ ] Documentation updated
- [ ] Support team briefed
- [ ] Status page updated (if user-facing)
- [ ] Rollback communication drafted
- [ ] Launch announcement drafted
- [ ] FAQ prepared for common issues
- [ ] Post-launch review scheduled

## Feature Flag Lifecycle

```
Stage 1: Development
  Flag: disabled
  Purpose: Feature in progress, hidden from all users
  Code: Behind flag check

Stage 2: Internal Testing
  Flag: enabled for internal users/team
  Purpose: Dogfooding, find bugs early
  Code: Same as production

Stage 3: Beta / Limited Release
  Flag: enabled for beta users (1-5%)
  Purpose: Validate with real users, gather feedback
  Code: Stable, monitored closely

Stage 4: Gradual Rollout
  Flag: enabled for increasing % (10%, 25%, 50%, 75%)
  Purpose: Ramp up confidence, watch metrics
  Code: Monitored at each threshold

Stage 5: Full Release
  Flag: enabled for 100% of users
  Purpose: Feature is live for everyone
  Code: Fully stable

Stage 6: Flag Removal
  Flag: deleted from codebase
  Purpose: Clean up technical debt
  Code: Always-on path only
```

### Flag Naming Convention
`flags/{team}/{feature-name}` or `feature-flags/{FEATURE_NAME}`

### Flag Removal Criteria
- Feature has been at 100% for at least 1 week
- No critical bugs reported
- Rollback not expected
- All dependent features also released

## Staged Rollout Plan

### Stage 1: Canary (5%, 10 minutes)
- Deploy to 5% of users
- Monitor error rate, latency, and custom metrics
- If error rate increases > 0.1% → ABORT, rollback
- If latency increases P95 > 200ms → ABORT, rollback
- After 10 minutes → proceed

### Stage 2: Quarter (25%, 30 minutes)
- Deploy to 25% of users
- Same monitoring as canary
- Also monitor business metrics (conversion, signups, etc.)
- After 30 minutes → proceed

### Stage 3: Half (50%, 1 hour)
- Deploy to 50% of users
- Full monitoring suite
- After 1 hour → proceed

### Stage 4: Full (100%)
- Deploy to all users
- Continue monitoring for 24-48 hours
- Declare launch successful after 48 hours with no issues

## Rollback Procedures

### Automated Rollback Triggers
- Error rate increases by > 0.5% above baseline
- P95 latency increases > 500ms above baseline
- Any paging alert fires within 10 minutes of deploy
- Business metric drops by > 5% (e.g., conversion rate)
- Health check fails 3 consecutive times

### Rollback Steps
1. Identify the rollback trigger (metric, time, scope)
2. Notify the team: `@channel Rollback initiated: [REASON]`
3. Execute rollback: redeploy previous version
   - Feature flag: disable the flag
   - Blue/green: switch back to old
   - Git: `git revert HEAD && git push`
4. Verify rollback: monitoring shows metrics returning to baseline
5. Communicate: update status page, notify stakeholders
6. Post-mortem: investigate root cause, document timeline

### Rollback Safety
- Database migrations must be reversible
- Feature flags for quick disable without redeploy
- Keep old artifacts available for at least 48 hours
- Document rollback steps in runbook

## Monitoring Setup

### Metrics to Track (RED Method)
- **Rate**: Requests per second (throughput)
- **Errors**: Number or percentage of failed requests
- **Duration**: Latency distribution (P50, P95, P99)

### Health Check Endpoints
```
GET /health          → Basic alive check
GET /health/ready    → Ready to serve traffic
GET /health/deps     → Dependency health (DB, cache, etc.)
GET /metrics         → Prometheus metrics endpoint
```

### Alert Thresholds
| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | > 0.1% | > 1% |
| P95 latency | > 200ms | > 500ms |
| CPU usage | > 70% | > 90% |
| Memory usage | > 70% | > 90% |
| Disk usage | > 80% | > 95% |
| 5xx rate | > 0.5% | > 2% |
| 4xx rate | > 5% | > 10% |

### Dashboard Layout
```
Row 1: Overview (RPS, Error Rate, Latency P95)
Row 2: System (CPU, Memory, Disk, Network)
Row 3: Dependencies (DB latency, Cache hit rate, Queue depth)
Row 4: Business (Signups, Orders, Active users)
Row 5: Deployment (Version, Host count, Uptime)
```

## Launch Communication Template

```markdown
# Launch: [Feature Name]

**Status**: 🔴 Not Started / 🟡 In Progress / 🟢 Complete / 🔴 Rolled Back

## Timeline
- **Start**: YYYY-MM-DD HH:MM TZ
- **Canary (5%)**: YYYY-MM-DD HH:MM
- **Quarter (25%)**: YYYY-MM-DD HH:MM
- **Half (50%)**: YYYY-MM-DD HH:MM
- **Full (100%)**: YYYY-MM-DD HH:MM
- **Rollback window ends**: YYYY-MM-DD HH:MM

## What's Shipping
[Brief description of the feature or change]

## Monitoring
- Dashboard: [link]
- Alerts: [link]
- Runbook: [link]

## Communication
- Release notes: [link]
- Docs: [link]
- Support FAQ: [link]

## Contacts
- Launch lead: @person
- Engineering: @team
- Support: @team
- Product: @person

## Current Metrics
| Metric | Current | Baseline | Threshold |
|--------|---------|----------|-----------|
| Error rate | 0.02% | 0.01% | 0.1% |
| P95 latency | 120ms | 100ms | 200ms |
| RPS | 1500 | 1400 | - |

## Rollback Status
- Feature flag kill switch: ✅ Ready
- Database rollback: ✅ Tested
- Previous artifact: ✅ Available
```

## Post-Launch Checklist
- [ ] Metrics stable for 48 hours
- [ ] No critical bugs reported
- [ ] Feature flag cleaned up (if at 100%)
- [ ] Post-mortem documented
- [ ] Launch retrospective scheduled
- [ ] Performance impact documented
- [ ] Capacity planning updated
- [ ] Runbook updated with lessons learned

## Usage
Load this skill when preparing a production launch, setting up deployment monitoring, or planning a staged rollout. Follow the pre-launch checklist, execute the staged rollout plan, and ensure rollback readiness at every step.
