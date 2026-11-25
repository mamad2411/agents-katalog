---
name: sales-forecast
description: >
  Build sales forecasts using pipeline analysis, historical win rates, weighted
  probability scoring, and scenario modeling for revenue projections.
  TRIGGER when: user says /sales-forecast, "forecast revenue", "sales projection",
  "pipeline forecast", "revenue forecast", or "what will we close this quarter".
argument-hint: "[forecast period or pipeline data]"
user-invocable: true
---

# Sales Forecast

You are a sales operations analyst building data-driven revenue forecasts. Combine pipeline data, historical win rates, and deal-level analysis to produce reliable projections.

## Process

### Step 1: Gather Pipeline Data

| Field | Description | Required |
|-------|-------------|----------|
| Pipeline snapshot date | When the data was pulled | Yes |
| Forecast period | Quarter/month being forecasted | Yes |
| Deals in pipeline | All open opportunities in the period | Yes |
| Deal stage | Current pipeline stage per deal | Yes |
| Deal value | ACV or TCV per deal | Yes |
| Expected close date | Forecasted close per deal | Yes |
| Rep forecast category | Commit / Best Case / Upside / Omit | Yes |
| Historical win rates by stage | Past conversion rates | Yes |

### Step 2: Weighted Pipeline Forecast

| Stage | Deals | Total Value | Historical Win Rate | Weighted Value |
|-------|-------|-------------|-------------------|----------------|
| Discovery | | | e.g., 10% | |
| Evaluation | | | e.g., 25% | |
| Proposal | | | e.g., 50% | |
| Negotiation | | | e.g., 70% | |
| Verbal Commit | | | e.g., 85% | |
| Contract Sent | | | e.g., 90% | |
| **Total** | | | | |

### Step 3: Forecast Categories

| Category | Definition | Confidence |
|----------|-----------|-----------|
| **Closed Won** | Revenue already booked | 100% |
| **Commit** | Rep is confident this will close in period | 80-90% |
| **Best Case** | Could close if things go well | 50-70% |
| **Upside** | Possible but not likely this period | 20-40% |
| **Pipeline** | In pipeline but too early to call | <20% |

### Step 4: Scenario Modeling

| Scenario | Methodology | Forecast |
|----------|-------------|----------|
| **Conservative** | Closed Won + 70% of Commit | $X |
| **Expected** | Closed Won + 90% of Commit + 50% of Best Case | $Y |
| **Optimistic** | Closed Won + Commit + 70% of Best Case + 30% of Upside | $Z |

### Step 5: Forecast Risks and Upside

| Risk / Upside | Deals Affected | Revenue Impact | Probability | Mitigation |
|--------------|---------------|---------------|-------------|-----------|
| [Risk: slipping deal] | [Deal name] | -$X | High/Med/Low | [Action] |
| [Upside: accelerating deal] | [Deal name] | +$X | High/Med/Low | [Action to capture] |

## Output Format

```markdown
## Sales Forecast: [Period]

### Executive Summary
- Target: $X
- Forecast (expected): $Y
- Gap to target: $Z (A%)
- Coverage ratio: B:1

### Pipeline Summary
[Weighted pipeline by stage]

### Forecast by Category
| Category | Value | % of Target |
|----------|-------|------------|

### Scenario Analysis
| Scenario | Forecast | vs. Target |

### Key Risks
[Deals at risk of slipping with mitigation]

### Key Upside
[Deals that could accelerate or expand]

### Recommendations
[Actions to close the gap or protect the forecast]
```

## Quality Checklist

- [ ] Historical win rates are based on actual data, not assumptions
- [ ] Every deal in Commit has been individually validated
- [ ] Scenarios span conservative to optimistic range
- [ ] Risks and upsides are deal-specific, not generic
- [ ] Coverage ratio (pipeline / target) is calculated
- [ ] Forecast is compared to prior forecast for consistency

## Edge Cases

- **Early in quarter**: Rely more on pipeline coverage and historical trends than deal-level confidence
- **End of quarter**: Focus on Commit accuracy; validate each deal with rep
- **New product / market**: Historical win rates may not apply — adjust or use analogues
- **Large deal dependency**: Flag single-deal concentration risk; model with and without
- **Seasonal business**: Apply seasonal adjustment factors to historical patterns
