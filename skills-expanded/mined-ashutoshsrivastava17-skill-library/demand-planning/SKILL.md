---
name: demand-planning
description: >
  Forecast product or service demand using historical analysis, seasonal patterns, market signals,
  consensus planning, forecast accuracy metrics, and bias correction.
  TRIGGER when: user says /demand-planning, "forecast demand", "demand forecast", "predict demand", "sales forecast", "demand plan".
argument-hint: "[product/SKU] [time-horizon] [market-or-region]"
user-invocable: true
---

# Demand Planning

Build accurate, actionable demand forecasts that align supply with expected customer demand while minimizing forecast error and inventory risk.

---

## Input Gathering

Collect the following before starting the forecast cycle:

| Input                  | Description                                              | Required |
|------------------------|----------------------------------------------------------|----------|
| Historical sales data  | Minimum 24 months of shipment or POS data by SKU/region | Yes      |
| Product hierarchy      | Category, family, SKU mapping                            | Yes      |
| Time horizon           | Short (0-3 mo), Medium (3-12 mo), Long (12-36 mo)       | Yes      |
| Granularity            | Weekly, monthly, quarterly                               | Yes      |
| Promotional calendar   | Planned promotions, price changes, launches              | No       |
| Market intelligence    | Competitor actions, economic indicators, trends          | No       |
| Channel breakdown      | D2C, wholesale, retail, e-commerce split                 | No       |

---

## Step-by-Step Process

### Step 1 — Data Cleansing and Baseline Preparation

- Remove or flag outliers (stockouts, one-time bulk orders, data entry errors).
- Normalize for calendar effects (trading days, leap years).
- Fill gaps using interpolation or proxy SKU behavior.
- Document every adjustment with reason codes.

### Step 2 — Statistical Forecast Generation

Run appropriate models based on demand pattern:

| Demand Pattern   | Recommended Model             |
|------------------|-------------------------------|
| Stable / Smooth  | Exponential Smoothing (Holt)  |
| Trending         | Holt-Winters, Linear Regression |
| Seasonal         | SARIMA, Holt-Winters Seasonal |
| Intermittent     | Croston, SBA (Syntetos-Boylan)|
| New Product      | Analogous product mapping     |
| Lumpy            | Bootstrapping, Willemain      |

- Generate point forecasts and prediction intervals (80% and 95%).
- Produce forecasts at the lowest meaningful granularity, then aggregate upward.

### Step 3 — Demand Sensing and Signal Integration

Layer external signals onto the statistical baseline:

- **Leading indicators**: Web search trends, social media sentiment, foot traffic.
- **Economic signals**: GDP growth, consumer confidence, commodity prices.
- **Customer intelligence**: Pipeline data, customer forecasts, POS sell-through.
- **Competitive signals**: Product launches, pricing moves, store openings/closures.

Weight each signal by its historical correlation to actual demand.

### Step 4 — Consensus Planning and Collaborative Review

Facilitate a structured demand review meeting:

1. Present statistical forecast vs. prior period actuals.
2. Overlay sales team input (bottom-up account-level adjustments).
3. Incorporate marketing input (promotions, campaigns, launches).
4. Reconcile finance top-down targets with bottom-up build.
5. Lock the consensus number for each SKU-location combination.
6. Record assumption log for every manual override.

### Step 5 — Forecast Accuracy Measurement

Calculate and track these KPIs each cycle:

| Metric | Formula | Target |
|--------|---------|--------|
| MAPE   | Mean Absolute Percentage Error | < 20% at SKU-month |
| Bias   | (Forecast - Actual) / Actual | Between -5% and +5% |
| WMAPE  | Weighted MAPE by revenue | < 15% |
| Forecast Value Added (FVA) | Accuracy improvement over naive model | > 0 for every step |
| Tracking Signal | Cumulative error / MAD | Between -4 and +4 |

### Step 6 — Bias Correction and Continuous Improvement

- Identify persistent over- or under-forecasting by product, region, or planner.
- Apply bias correction factors to the statistical baseline.
- A/B test new models or signals against the incumbent.
- Archive each forecast vintage for retrospective analysis.
- Update model parameters quarterly; retrain models annually.

---

## Output Format

```
## Demand Forecast — [Product/Region] — [Period]

### Executive Summary
- Forecast horizon: [start] to [end]
- Total forecasted demand: [units/revenue]
- Forecast confidence: [high/medium/low]
- Key assumptions: [list]

### Forecast by Period
| Period | Statistical Forecast | Adjusted Forecast | YoY Change | Confidence Interval |
|--------|----------------------|-------------------|------------|---------------------|
| ...    | ...                  | ...               | ...        | ...                 |

### Accuracy Scorecard (Prior Cycle)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| MAPE   | ...   | < 20%  | ...    |
| Bias   | ...   | +/- 5% | ...    |

### Assumptions and Risks
- [Numbered list of key assumptions]
- [Identified upside/downside risks with probability]

### Recommendations
- [Actionable next steps]
```

---

## Quality Checklist

- [ ] Historical data covers at least 24 months and has been cleansed
- [ ] Outliers documented and handled with reason codes
- [ ] Appropriate model selected for each demand pattern
- [ ] Prediction intervals generated alongside point forecasts
- [ ] External signals evaluated and weighted
- [ ] Consensus review completed with cross-functional input
- [ ] Every manual override has a documented rationale
- [ ] Accuracy metrics calculated against prior forecast
- [ ] Bias correction applied where persistent drift detected
- [ ] Forecast locked and communicated to supply planning

---

## Edge Cases

- **New product launch with zero history**: Use analogous product mapping; identify 2-3 similar past launches and scale by expected distribution and marketing spend.
- **Demand during supply-constrained periods**: Back-calculate unconstrained demand using lost-sales estimates; do not train models on constrained actuals.
- **Promotional cannibalization**: Model baseline and promotional lift separately; account for pull-forward and pantry-loading effects.
- **Market discontinuities (pandemic, regulation change)**: Segment data into pre- and post-event; weight recent data more heavily or restart baseline.
- **Highly intermittent / spare-parts demand**: Switch to Croston or bootstrapping; report demand probability and expected order size separately.
- **Currency or price-driven volume shifts**: Decompose demand into price-driven and organic components; forecast each independently.
