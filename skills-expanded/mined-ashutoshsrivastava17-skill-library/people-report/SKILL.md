---
name: people-report
description: >
  Generate a people analytics or HR report covering headcount, attrition,
  diversity metrics, engagement, and workforce trends.
  TRIGGER when: user asks for a people report, HR metrics, headcount report,
  attrition analysis, diversity report, workforce analytics, turnover report,
  or people dashboard.
argument-hint: "[--period <Q1-2026|2025|monthly>] [--focus <attrition|diversity|headcount|engagement>]"
user-invocable: true
---

# People / HR Report Generator

You are a people analytics expert. Produce clear, actionable HR reports with visualizations, benchmarks, and executive-ready narratives.

## Step 1: Gather Parameters

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| Report Period | Yes | Current quarter | Month, quarter, year, or custom range |
| Report Focus | No | Comprehensive | Headcount, attrition, diversity, engagement, or all |
| Organization Scope | No | Company-wide | Specific department, team, or location |
| Comparison Period | No | Previous period | For trend analysis |
| Data Available | Yes | — | Ask what data the user can provide |
| Audience | No | Leadership | Adjusts detail level and framing |

## Step 2: Report Structure

### 2.1 Executive Summary

Provide a 3-5 bullet summary of the most important findings:

```
PEOPLE REPORT — {Period}
════════════════════════

KEY HIGHLIGHTS:
* Headcount: {X} employees (+/- {Y}% vs prior period)
* Attrition: {X}% annualized ({voluntary/involuntary split})
* Open roles: {X} ({Y} critical)
* Time to fill: {X} days average
* Engagement score: {X}/5 ({trend})
```

### 2.2 Headcount Dashboard

| Metric | Current | Prior Period | Change | Trend |
|--------|---------|-------------|--------|-------|
| Total Headcount | — | — | — | Up/Down/Flat |
| Full-Time | — | — | — | — |
| Part-Time | — | — | — | — |
| Contractors | — | — | — | — |
| New Hires (Period) | — | — | — | — |
| Departures (Period) | — | — | — | — |
| Net Change | — | — | — | — |
| Open Requisitions | — | — | — | — |

#### Headcount by Department

| Department | HC | % of Total | HC Plan | Variance |
|-----------|-----|-----------|---------|----------|
| Engineering | — | — | — | — |
| Product | — | — | — | — |
| Sales | — | — | — | — |
| Marketing | — | — | — | — |
| G&A | — | — | — | — |
| **Total** | — | **100%** | — | — |

### 2.3 Attrition Analysis

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Overall Attrition (annualized) | — | 12-18% | — |
| Voluntary Attrition | — | 8-12% | — |
| Involuntary Attrition | — | 3-5% | — |
| Regrettable Attrition | — | <5% | — |
| First-Year Attrition | — | <20% | — |
| 90-Day Attrition | — | <5% | — |
| Average Tenure at Departure | — | — | — |

#### Attrition by Dimension

Break down attrition by:
- Department
- Level / seniority
- Tenure band (0-1yr, 1-2yr, 2-5yr, 5+yr)
- Location
- Performance rating (if available)
- Manager

#### Top Departure Reasons

| Reason | % of Departures | Trend |
|--------|----------------|-------|
| Better opportunity / comp | — | — |
| Career growth / promotion | — | — |
| Manager relationship | — | — |
| Work-life balance | — | — |
| Relocation / personal | — | — |
| Involuntary / performance | — | — |

### 2.4 Diversity & Inclusion Metrics

| Dimension | Breakdown | Benchmark | Notes |
|-----------|-----------|-----------|-------|
| Gender | X% Women, Y% Men, Z% Non-binary | Industry avg | — |
| Ethnicity / Race | {breakdown} | Industry avg | US-specific, where collected |
| Age Distribution | {bands} | — | — |
| Leadership Diversity | X% URG in management+ | — | — |
| Hiring Diversity | X% of new hires from URGs | — | Pipeline conversion rates |
| Promotion Parity | Promotion rate by demographic | — | Flag disparities |
| Pay Equity | Adjusted pay gap | <2% | By gender, ethnicity |

### 2.5 Recruiting Metrics

| Metric | Value | Prior Period | Target |
|--------|-------|-------------|--------|
| Open Roles | — | — | — |
| Applications Received | — | — | — |
| Offers Extended | — | — | — |
| Offers Accepted | — | — | — |
| Offer Acceptance Rate | — | >85% | — |
| Time to Fill (avg days) | — | — | <45 days |
| Cost per Hire | — | — | — |
| Source Effectiveness | — | — | — |

### 2.6 Engagement & Satisfaction

| Indicator | Score | Prior Period | Benchmark |
|-----------|-------|-------------|-----------|
| Overall Engagement | /5 | — | 3.8+ |
| eNPS | — | — | >30 |
| Manager Effectiveness | /5 | — | — |
| Growth & Development | /5 | — | — |
| Compensation Satisfaction | /5 | — | — |
| Work-Life Balance | /5 | — | — |

## Step 3: Trend Analysis

For each key metric, provide:
- 3-6 period trend (monthly or quarterly)
- Direction and velocity of change
- Correlation with business events (layoffs, product launches, etc.)
- Forecast for next period if data supports it

## Step 4: Insights & Recommendations

### Key Insights
1. **{Insight title}**: {Description with supporting data}
2. **{Insight title}**: {Description with supporting data}
3. **{Insight title}**: {Description with supporting data}

### Recommended Actions

| Priority | Action | Owner | Expected Impact | Timeline |
|----------|--------|-------|----------------|----------|
| High | — | — | — | — |
| Medium | — | — | — | — |
| Low | — | — | — | — |

## Step 5: Presentation Format

Adapt the output to the audience:

| Audience | Format | Detail Level |
|----------|--------|-------------|
| Board / C-Suite | 1-page summary + 3 key metrics | High-level, strategic |
| VP / Directors | Full dashboard + trends | Moderate detail, actionable |
| HR Team | Complete data + drill-downs | Full detail, operational |
| All-hands | 3-5 highlights, positive framing | Light, celebratory |

## Edge Cases

- **Insufficient data**: Note which metrics cannot be calculated and recommend data collection improvements
- **Small team (<20)**: Avoid percentages that could identify individuals; use ranges or qualitative assessments
- **Privacy / legal**: Never include individual names in reports; aggregate to groups of 5+ for demographic data
- **Seasonal businesses**: Adjust benchmarks for expected seasonal headcount fluctuations
- **Rapid growth**: Distinguish between organic and M&A headcount changes
- **Multi-country**: Segment by country/region where legal frameworks differ

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
