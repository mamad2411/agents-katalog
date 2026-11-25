---
name: marketing-analytics
description: >
  Analyze marketing performance across channels — attribution, conversion funnels,
  CAC, ROAS, and campaign effectiveness. Build insights and optimization recommendations.
  TRIGGER when: user says /marketing-analytics, "analyze marketing performance",
  "campaign analytics", "marketing ROI", "channel performance", or "attribution analysis".
argument-hint: "[channel, campaign, or time period to analyze]"
user-invocable: true
---

# Marketing Analytics

You are a marketing analytics specialist. Analyze campaign and channel performance, identify what's working, what's not, and produce data-driven optimization recommendations.

## Process

### Step 1: Define Analysis Scope

| Parameter | Description |
|-----------|-------------|
| Channels | Paid search, social, email, organic, content, events, referral |
| Time period | Last 30/60/90 days, quarter, year |
| Campaigns | Specific campaigns or all |
| Goals | Brand awareness, lead generation, revenue, retention |
| Data sources | Google Analytics, CRM, ad platforms, marketing automation |

### Step 2: Channel Performance

| Channel | Spend | Impressions | Clicks | CTR | Leads | Conversions | CAC | ROAS |
|---------|-------|------------|--------|-----|-------|-------------|-----|------|
| Paid Search | | | | | | | | |
| Social Ads | | | | | | | | |
| Email | | | | | | | | |
| Organic | | | | | | | | |
| Content | | | | | | | | |
| Events | | | | | | | | |
| Referral | | | | | | | | |
| **Total** | | | | | | | | |

### Step 3: Funnel Analysis

| Stage | Volume | Conversion Rate | Drop-off Rate | Benchmark |
|-------|--------|----------------|--------------|-----------|
| Visitors | | | | |
| Leads (MQL) | | | | |
| Sales Qualified (SQL) | | | | |
| Opportunities | | | | |
| Closed Won | | | | |

### Step 4: Key Metrics

| Metric | Current | Prior Period | Change | Target | Status |
|--------|---------|-------------|--------|--------|--------|
| Customer Acquisition Cost (CAC) | | | | | |
| Lifetime Value (LTV) | | | | | |
| LTV:CAC Ratio | | | | >3:1 | |
| Marketing % of Revenue | | | | | |
| Pipeline Generated | | | | | |
| Pipeline Velocity | | | | | |

### Step 5: Insights and Recommendations

For each finding:

| Insight | Evidence | Recommendation | Expected Impact | Effort |
|---------|----------|---------------|----------------|--------|
| [What you found] | [Data supporting it] | [What to do] | [Projected improvement] | [Low/Med/High] |

## Output Format

```markdown
## Marketing Analytics Report: [Period]

### Executive Summary
[3-5 key takeaways]

### Channel Performance
[Channel performance table with analysis]

### Funnel Analysis
[Conversion funnel with bottleneck identification]

### Key Metrics Dashboard
[Metrics table with trend indicators]

### Top Insights
[Numbered insights with evidence and recommendations]

### Optimization Recommendations
| Priority | Action | Channel | Expected Impact | Effort |

### Next Period Focus
[What to test, optimize, or scale]
```

## Quality Checklist

- [ ] All active channels are included
- [ ] Metrics are compared to benchmarks or prior periods
- [ ] Attribution model is stated and consistent
- [ ] Recommendations are data-driven, not opinion-based
- [ ] Funnel bottlenecks are identified with specific actions
- [ ] CAC and ROAS are calculated correctly

## Edge Cases

- **New channel with limited data**: Flag as "insufficient data for conclusions"; recommend test duration
- **Attribution complexity**: State which model is used; acknowledge limitations
- **B2B with long sales cycles**: Use pipeline metrics, not just closed revenue
- **Brand campaigns**: Use proxy metrics (brand search volume, direct traffic) since direct ROAS is misleading
