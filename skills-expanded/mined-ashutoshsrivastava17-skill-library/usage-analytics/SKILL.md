---
name: usage-analytics
description: >
  Analyze product usage for customer success — adoption metrics, feature
  engagement, usage trends, health indicators, and intervention triggers.
  TRIGGER when: user says /usage-analytics, needs to analyze customer product
  usage, or wants to identify at-risk accounts from usage data.
argument-hint: "[account or segment to analyze]"
user-invocable: true
---

# Customer Usage Analytics

You are a CS analytics specialist. Analyze product usage to identify health signals, expansion opportunities, and churn risks.

## Process

### Step 1: Define Usage Metrics

| Metric Category | Examples | Health Signal |
|----------------|---------|---------------|
| Adoption breadth | % of licenses active, departments using product | Low = shelfware risk |
| Adoption depth | Features used / total features, advanced feature usage | Low = shallow adoption |
| Engagement frequency | DAU/WAU/MAU ratios, session count | Declining = disengagement |
| Engagement intensity | Time in product, actions per session | Low = low value extraction |
| Growth signals | New user additions, API call growth, data volume growth | Rising = expansion opportunity |
| Stickiness | DAU/MAU ratio, return rate | Low = not habit-forming |

### Step 2: Establish Baselines

| Segment | Healthy Range | At-Risk Threshold | Critical Threshold |
|---------|-------------|-------------------|-------------------|
| Enterprise | [X-Y] | < X | < Z |
| Mid-market | [X-Y] | < X | < Z |
| SMB | [X-Y] | < X | < Z |

### Step 3: Analyze Account Health

For each account, assess:

| Dimension | Score (1-10) | Trend | Evidence |
|-----------|-------------|-------|----------|
| Adoption | X | ↑/↓/→ | X% licenses active |
| Engagement | X | ↑/↓/→ | X sessions/week avg |
| Feature depth | X | ↑/↓/→ | X/Y features used |
| Growth | X | ↑/↓/→ | X new users this quarter |
| **Composite** | **X** | **↑/↓/→** | — |

### Step 4: Identify Intervention Triggers

| Trigger | Signal | Action |
|---------|--------|--------|
| Usage drop > 20% WoW | Disengagement | Check-in call within 48 hours |
| No login in 14 days | Dormancy | Re-engagement email + CSM outreach |
| Key user churned | Champion loss | Executive outreach, identify new champion |
| Feature adoption plateau | Value ceiling | Training session, use case workshop |
| Usage spike | Expansion signal | Upsell conversation |

### Step 5: Generate Insights

```
ACCOUNT: [Name]
HEALTH: [Score] ([trend])
KEY FINDING: [What the data shows]
RISK/OPPORTUNITY: [What this means for the relationship]
RECOMMENDED ACTION: [Specific next step]
URGENCY: [High/Medium/Low]
```

## Output Format

```markdown
## Usage Analytics Report — [Period]

### Portfolio Summary
- Healthy: [N] accounts ([X]%) | At-risk: [N] ([X]%) | Critical: [N] ([X]%)

### Top Risks
| Account | Health | Signal | Recommended Action |
|---------|--------|--------|-------------------|

### Expansion Opportunities
| Account | Signal | Potential | Next Step |
|---------|--------|-----------|-----------|
```

## Quality Checklist

- [ ] Metrics cover breadth, depth, frequency, and intensity
- [ ] Baselines are segment-appropriate
- [ ] Trends use sufficient time window (not just point-in-time)
- [ ] Intervention triggers have clear ownership and SLAs
- [ ] Insights distinguish noise from signal

## Edge Cases

- For new accounts (< 90 days), use onboarding-specific benchmarks
- For seasonal businesses, compare year-over-year, not month-over-month
- If usage data is incomplete, supplement with survey/qualitative signals
- For platform products, track API usage alongside UI usage
