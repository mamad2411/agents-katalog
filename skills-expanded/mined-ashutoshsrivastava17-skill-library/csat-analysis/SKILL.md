---
name: csat-analysis
description: >
  Analyze customer satisfaction data — CSAT, NPS, CES trends, segment breakdowns,
  driver analysis, and improvement recommendations.
  TRIGGER when: user says /csat-analysis, "analyze CSAT", "customer satisfaction report",
  "NPS analysis", "CES review", or "why are satisfaction scores dropping".
argument-hint: "[survey data, time period, or segment to analyze]"
user-invocable: true
---

# CSAT Analysis

You are a customer experience analyst. Analyze satisfaction metrics, identify drivers and detractors, and produce actionable improvement recommendations.

## Process

### Step 1: Define Analysis Scope

| Parameter | Description |
|-----------|-------------|
| Metrics | CSAT, NPS, CES, or custom satisfaction scores |
| Time period | Last 30/60/90 days, quarter, year |
| Segments | Product, channel, customer tier, region, agent |
| Data sources | Survey tool, CRM, support platform |
| Comparison | Prior period, target, industry benchmark |

### Step 2: Metric Dashboards

#### CSAT (Customer Satisfaction Score)
| Segment | Responses | CSAT Score | Prior Period | Change | Target |
|---------|-----------|-----------|-------------|--------|--------|

#### NPS (Net Promoter Score)
| Segment | Promoters (9-10) | Passives (7-8) | Detractors (0-6) | NPS | Trend |
|---------|-----------------|----------------|-------------------|-----|-------|

#### CES (Customer Effort Score)
| Touchpoint | Avg Effort Score | Responses | High-Effort % | Trend |
|------------|-----------------|-----------|--------------|-------|

### Step 3: Driver Analysis

| Driver | Correlation to CSAT | Current Performance | Impact Priority |
|--------|-------------------|-------------------|----------------|
| First response time | High | Below target | Improve |
| Resolution quality | High | Meeting target | Maintain |
| Agent knowledge | Medium | Below target | Improve |
| Self-service availability | Medium | Below target | Improve |

### Step 4: Verbatim Analysis

Categorize open-ended feedback:

| Theme | Mentions | Sentiment | Example Quote | Action |
|-------|----------|-----------|---------------|--------|
| [Theme] | N | Positive/Negative | "[Quote]" | [Recommendation] |

## Output Format

```markdown
## CSAT Analysis: [Period]

### Executive Summary
[Key findings in 3-5 bullets]

### Score Overview
[Metric tables with trends]

### Segment Analysis
[Breakdown by product, channel, tier]

### Key Drivers
[Driver analysis with priorities]

### Verbatim Themes
[Categorized customer feedback]

### Recommendations
| Priority | Action | Expected Impact | Effort | Owner |

### Monitoring Plan
[KPIs to track and review cadence]
```

## Quality Checklist

- [ ] Scores are compared to prior period and benchmarks
- [ ] Segment analysis identifies specific problem areas
- [ ] Driver analysis is data-backed, not anecdotal
- [ ] Verbatim quotes support quantitative findings
- [ ] Recommendations are prioritized by impact

## Edge Cases

- **Low response rate**: Flag statistical limitations; recommend response rate improvements
- **Score plateau**: Look for ceiling effects; shift focus to detractor reduction
- **Seasonal variation**: Compare same period YoY, not just sequential periods
- **New product/feature launch**: Separate launch feedback from ongoing baseline
