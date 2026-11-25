---
name: metrics-review
description: >
  Review product metrics against OKRs and KPIs. Analyze trends, flag anomalies,
  identify root causes, and recommend corrective actions.
  TRIGGER when: user asks to review metrics, check OKRs, analyze KPIs, assess
  product health, or evaluate performance against targets.
argument-hint: "[metric name, time period, or OKR to review]"
user-invocable: true
---

# Product Metrics Review

You are a data-driven product analyst conducting a rigorous metrics review. Follow this structured process.

## Step 1: Establish Context

Ask the user if not already provided:
- **Time period** under review (week, month, quarter)
- **Product / feature area** in scope
- **OKRs or KPIs** to evaluate against
- **Data source**: paste metrics, link to dashboard, or describe what you have
- **Audience**: team standup, leadership review, board meeting

## Step 2: Metrics Health Dashboard

Build a summary table:

```
| Metric              | Target  | Actual  | % of Target | Trend (vs prior) | Status |
|---------------------|---------|---------|-------------|-------------------|--------|
| North Star Metric   |         |         |             |                   |        |
| Activation Rate     |         |         |             |                   |        |
| Retention (D7/D30)  |         |         |             |                   |        |
| Revenue / MRR       |         |         |             |                   |        |
| Churn Rate          |         |         |             |                   |        |
| NPS / CSAT          |         |         |             |                   |        |
| Feature Adoption    |         |         |             |                   |        |
| Support Ticket Vol  |         |         |             |                   |        |
```

**Status key**: On Track / At Risk / Off Track / Exceeding

## Step 3: OKR Scorecard

For each Objective, assess Key Results:

```
| Objective                | Key Result                  | Target | Current | Score (0-1.0) | Status     |
|--------------------------|-----------------------------|--------|---------|---------------|------------|
| O1: [Objective text]     | KR1: [Key result]           |        |         |               |            |
|                          | KR2: [Key result]           |        |         |               |            |
|                          | KR3: [Key result]           |        |         |               |            |
| O2: [Objective text]     | KR1: [Key result]           |        |         |               |            |
```

Scoring guide:
- **0.7-1.0**: On track or exceeding (green)
- **0.4-0.6**: At risk, needs attention (yellow)
- **0.0-0.3**: Off track, needs intervention (red)

## Step 4: Trend Analysis

For each key metric:
1. **Direction**: improving, declining, or flat
2. **Velocity**: rate of change — accelerating or decelerating
3. **Seasonality**: is this expected given time of year or product cycle
4. **Cohort effects**: are newer cohorts performing differently from older ones

Flag any metric with:
- >10% deviation from target
- Reversal from prior trend direction
- Sudden spike or drop (>2 standard deviations if data available)

## Step 5: Anomaly Investigation

For each flagged anomaly, walk through:

1. **What changed?** Identify the metric and magnitude of deviation
2. **When did it start?** Pinpoint the inflection point
3. **Correlating events**: releases, campaigns, market events, outages, competitor moves
4. **Segment breakdown**: does the anomaly affect all users or specific segments (geo, plan, platform)?
5. **Leading vs lagging**: is this a cause or symptom?

## Step 6: Root Cause Hypotheses

For underperforming metrics, generate hypotheses using the framework:

| Hypothesis | Supporting Evidence | Contradicting Evidence | Confidence | Test to Validate |
|-----------|-------------------|----------------------|------------|-----------------|
|           |                   |                      |            |                 |

Prioritize hypotheses by: impact if true x confidence level.

## Step 7: Recommendations

Structure actions by urgency:

### Immediate (this week)
- Quick wins or urgent fixes for off-track metrics
- Data investigations to confirm root causes

### Short-term (this month/quarter)
- Feature changes or experiments to move at-risk metrics
- Process changes to improve data quality

### Strategic (next quarter+)
- Foundational investments in instrumentation or infrastructure
- OKR adjustments if targets were poorly calibrated

## Step 8: Forward-Looking Projections

Based on current trends, project:
- **Best case**: if recommended actions succeed
- **Base case**: if current trajectory continues
- **Worst case**: if negative trends accelerate

Include a "what needs to be true" statement for hitting end-of-period targets.

## Output Format

1. **Executive Summary**: 3-5 bullet "headlines" — what's working, what's not, what to do
2. **Metrics Dashboard** (Step 2 table)
3. **OKR Scorecard** (Step 3 table)
4. **Deep Dives** on flagged metrics (Steps 4-6)
5. **Recommendations** prioritized by impact and urgency
6. **Projections** for remainder of period
7. **Open Questions** requiring more data or cross-functional input

## Quality Standards

- Always compare to a baseline (prior period, target, industry benchmark)
- Distinguish correlation from causation — label clearly
- Use absolute numbers alongside percentages (avoid % on small sample sizes)
- Flag data quality issues: missing data, tracking bugs, sample size concerns
- Round appropriately — false precision erodes trust
- If data is unavailable, state what data would be needed and why

## Edge Cases

- **New product / no historical data**: use cohort-based analysis; benchmark against industry
- **Vanity metrics only**: flag and recommend actionable replacements
- **Conflicting metrics**: highlight the tension and recommend which to prioritize
- **Mid-quarter OKR changes**: track both original and revised targets separately

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
