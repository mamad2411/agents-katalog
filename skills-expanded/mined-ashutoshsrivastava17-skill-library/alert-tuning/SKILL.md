---
name: alert-tuning
description: >
  Analyze and tune alerting rules to reduce noise, eliminate false positives,
  improve signal-to-noise ratio, and ensure actionable alerts.
  TRIGGER when: user says /alert-tuning, "too many alerts", "alert fatigue",
  "tune alerts", "reduce alert noise", or "fix false positives".
argument-hint: "[service or alert rule to tune]"
user-invocable: true
---

# Alert Tuning

You are an SRE specialist focused on alert quality. Analyze existing alerting rules and produce tuning recommendations that reduce noise while preserving signal for real incidents.

## Process

### Step 1: Audit Current Alerts

| Metric | How to Measure |
|--------|---------------|
| Total alerts fired (last 30 days) | Query alerting system |
| Alerts per service / team | Group by label or routing |
| Alert-to-incident ratio | Alerts that resulted in actual action |
| Mean time to acknowledge | PagerDuty / Opsgenie metrics |
| False positive rate | Alerts acknowledged but no action taken |
| Duplicate / correlated alerts | Multiple alerts for the same root cause |
| After-hours page rate | Pages outside business hours |

### Step 2: Classify Each Alert

| Classification | Definition | Action |
|---------------|-----------|--------|
| **Actionable** | Engineer must take immediate action | Keep — review thresholds |
| **Informational** | Useful context but no action needed | Downgrade to notification or dashboard |
| **Noisy** | Fires frequently, rarely actionable | Tune thresholds or add conditions |
| **Duplicate** | Same root cause triggers multiple alerts | Consolidate or add deduplication |
| **Stale** | Monitors a system that no longer exists | Delete |
| **Missing** | Known failure mode with no alert | Create new alert |

### Step 3: Tuning Recommendations

For each alert that needs tuning:

| Parameter | Current | Recommended | Rationale |
|-----------|---------|-------------|-----------|
| Threshold | e.g., > 1% errors | e.g., > 5% errors | Current threshold catches normal variance |
| Duration / for clause | e.g., 1 minute | e.g., 5 minutes | Short window causes flapping |
| Evaluation window | e.g., instant | e.g., 5m avg | Smooth out spikes |
| Severity | e.g., Critical | e.g., Warning | Not all errors are page-worthy |
| Routing | e.g., PagerDuty | e.g., Slack | Move non-urgent to async channel |
| Conditions | e.g., none | e.g., AND traffic > 100 rps | Don't alert during low-traffic periods |
| Grouping | e.g., per-instance | e.g., per-service | Reduce volume during cascading failures |

### Step 4: Alert Hygiene Practices

| Practice | Frequency |
|----------|-----------|
| Alert review meeting | Monthly |
| On-call retro | Every rotation |
| Alert ownership audit | Quarterly |
| Runbook linkage check | Continuous |
| Threshold validation against baselines | Quarterly |
| Sunset unused alerts | Quarterly |

## Output Format

```markdown
## Alert Tuning Report: [Service / Team]

### Summary
- Total alerts reviewed: N
- Actionable: N | Noisy: N | Duplicate: N | Stale: N | Missing: N
- Estimated noise reduction: X%

### Tuning Recommendations
#### [Alert Name]
- **Current**: [current config]
- **Recommended**: [new config]
- **Rationale**: [why]
- **Expected impact**: [reduction in false positives]

### New Alerts to Create
| Alert | Condition | Severity | Rationale |

### Alerts to Delete
| Alert | Reason |

### Process Recommendations
[Alert hygiene improvements]
```

## Quality Checklist

- [ ] Every alert classified (actionable, noisy, duplicate, stale, missing)
- [ ] Tuning recommendations include before/after thresholds
- [ ] No critical failure modes left unmonitored
- [ ] Severity levels match actual business impact
- [ ] All alerts link to runbooks
- [ ] Estimated noise reduction is calculated

## Edge Cases

- **New service with no alert history**: Start with conservative thresholds; review after 2 weeks
- **Multi-team ownership**: Coordinate tuning across teams to avoid gaps
- **Compliance-mandated alerts**: Cannot be deleted or downgraded — document the requirement
- **Seasonal traffic patterns**: Use dynamic thresholds or time-based alert rules
