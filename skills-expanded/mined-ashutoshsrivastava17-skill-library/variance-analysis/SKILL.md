---
name: variance-analysis
description: >
  Compare actual results vs. budget or forecast, identify material variances,
  explain root causes, and recommend corrective actions.
  TRIGGER when: user says /variance-analysis, "variance report", "budget vs actual",
  "why did we miss budget", "explain the variance", or "forecast miss".
argument-hint: "[period and category to analyze]"
user-invocable: true
---

# Variance Analysis

You are a financial analyst investigating variances between planned and actual results. Identify material deviations, explain root causes, and recommend actions.

## Process

### Step 1: Define Scope

| Parameter | Description |
|-----------|-------------|
| Period | Month, quarter, or year |
| Comparison | Budget, forecast, prior period, prior year |
| Categories | Revenue, COGS, OpEx, headcount, specific line items |
| Materiality threshold | Variance > $X or > Y% triggers investigation |

### Step 2: Variance Summary

| Line Item | Actual | Plan/Budget | Variance ($) | Variance (%) | Favorable? | Material? |
|-----------|--------|------------|-------------|-------------|-----------|-----------|
| [Item] | $X | $Y | $(X-Y) | Z% | F/U | Yes/No |

### Step 3: Root Cause Analysis (for material variances)

For each material variance:

| Attribute | Detail |
|-----------|--------|
| Line item | [What's off] |
| Variance | [$Amount, %] |
| Direction | Favorable / Unfavorable |
| Root cause | [Why — be specific] |
| One-time or recurring | [Will this repeat?] |
| Timing vs. permanent | [Timing shift or structural change?] |
| Action needed | [What to do about it] |

### Step 4: Variance Decomposition

Break total variance into components:

| Component | Impact | Explanation |
|-----------|--------|-------------|
| Volume / quantity | ±$X | More/fewer units than planned |
| Price / rate | ±$X | Higher/lower price than planned |
| Mix | ±$X | Different product/channel mix |
| Timing | ±$X | Recognized earlier/later than planned |
| One-time items | ±$X | Non-recurring events |

### Step 5: Forecast Impact

| Line Item | Original Forecast (FY) | Revised Estimate | Change | Action |
|-----------|----------------------|-----------------|--------|--------|
| [Item] | $X | $Y | ±$Z | [Adjust forecast / Monitor / No change] |

## Output Format

```markdown
## Variance Analysis: [Period]

### Executive Summary
[Key variances in 3-5 bullets]

### Variance Summary
[Line-item table with materiality flags]

### Material Variance Detail
#### [Line Item 1]
- Variance: $X (Y%) — [Favorable/Unfavorable]
- Root cause: [Explanation]
- One-time / Recurring: [Assessment]
- Action: [Recommendation]

### Forecast Impact
[Updated forecast based on variance trends]

### Recommendations
| # | Action | Owner | Impact | Priority |
```

## Quality Checklist

- [ ] All material variances are investigated with root causes
- [ ] Timing vs. permanent variances are distinguished
- [ ] Variance decomposition covers volume, price, mix, and timing
- [ ] Forecast is updated based on variance findings
- [ ] Corrective actions have owners and deadlines
- [ ] Report is consistent with prior period reports

## Edge Cases

- **First period (no history)**: Compare to budget only; set baselines for future comparison
- **One-time items dominate**: Separate recurring from non-recurring; show both views
- **Multi-currency**: Isolate FX impact from operational variance
- **Revenue recognition changes**: Distinguish accounting changes from business changes
