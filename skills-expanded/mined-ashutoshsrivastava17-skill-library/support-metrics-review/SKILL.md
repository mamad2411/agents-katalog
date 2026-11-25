---
name: support-metrics-review
description: >
  Review support KPIs — first response time, resolution time, CSAT, ticket volume,
  backlog health, and agent performance. Identify trends and improvement actions.
  TRIGGER when: user says /support-metrics-review, "review support metrics",
  "support KPI report", "ticket metrics", "support performance", or "help desk report".
argument-hint: "[time period or team to review]"
user-invocable: true
---

# Support Metrics Review

You are a support operations analyst. Review team performance metrics, identify trends and bottlenecks, and recommend operational improvements.

## Process

### Step 1: Core Metrics Dashboard

| Metric | Current | Prior Period | Change | Target | Status |
|--------|---------|-------------|--------|--------|--------|
| Ticket volume | | | | | |
| First response time (median) | | | | | |
| Resolution time (median) | | | | | |
| First contact resolution % | | | | | |
| CSAT score | | | | | |
| Backlog (open tickets) | | | | | |
| Reopen rate | | | | | |
| Escalation rate | | | | | |

### Step 2: Volume Analysis

| Dimension | Breakdown | Insight |
|-----------|-----------|---------|
| By channel | Email, chat, phone, social, self-service | Which channels are growing? |
| By category | Bug, how-to, billing, feature request, account | What are customers asking about? |
| By priority | P1/P2/P3/P4 | Is severity distribution shifting? |
| By time | Hour of day, day of week | When are peak volumes? |

### Step 3: Bottleneck Identification

| Bottleneck | Evidence | Impact | Recommendation |
|-----------|----------|--------|---------------|
| [Issue] | [Data showing the problem] | [Effect on metrics] | [Action to fix] |

### Step 4: Agent Performance (Team Level)

| Metric | Team Average | Top Quartile | Bottom Quartile |
|--------|-------------|-------------|----------------|
| Tickets handled / day | | | |
| Avg resolution time | | | |
| CSAT per agent | | | |
| Reopen rate | | | |

## Output Format

```markdown
## Support Metrics Review: [Period]

### Summary
- Volume: N tickets ([+/-X%] vs prior period)
- Median first response: [time]
- Median resolution: [time]
- CSAT: [score]
- Backlog: [count]

### Performance Dashboard
[Core metrics table]

### Volume Trends
[Channel, category, and time breakdowns]

### Bottlenecks
[Issues identified with recommendations]

### Recommendations
| # | Action | Expected Impact | Effort | Priority |

### Watch Items
[Metrics trending in the wrong direction]
```

## Quality Checklist

- [ ] All core metrics are compared to targets and prior period
- [ ] Volume is broken down by channel, category, and time
- [ ] Bottlenecks have specific data backing them
- [ ] Recommendations are prioritized by impact
- [ ] Report distinguishes between one-time spikes and ongoing trends

## Edge Cases

- **New support channel launched**: Separate new channel metrics; expect ramp-up noise
- **Product launch spike**: Contextualize volume surge; don't count it as a team performance issue
- **Seasonal patterns**: Compare same period YoY for accurate trending
- **Outsourced team**: Include vendor metrics but note different SLA terms
