---
name: financial-forecast
description: >
  Build financial forecasts with revenue modeling, expense projections, cash flow analysis,
  scenario planning (best/base/worst), and documented assumptions.
  TRIGGER when: user says /financial-forecast, "forecast financials", "revenue forecast", "cash flow projection", "financial model", "scenario planning".
argument-hint: "[entity name] [forecast horizon] [scenario type]"
user-invocable: true
---

# Financial Forecast

Build rigorous financial forecasts that model revenue, expenses, and cash flow across multiple scenarios. This skill produces a structured forecast with transparent assumptions, sensitivity analysis, and clear narrative.

---

## Step 1 — Establish Forecast Parameters

Define the scope and ground rules before modeling.

| Parameter              | Description                                           | Example                         |
|------------------------|-------------------------------------------------------|---------------------------------|
| Entity                 | Company, business unit, or product line               | Acme Corp — SaaS Division      |
| Forecast Horizon       | Number of months/quarters/years                       | 12 months (monthly granularity) |
| Base Period            | Historical anchor for projections                     | Trailing 12 months actuals      |
| Reporting Currency     | Primary currency; note FX assumptions if multi-currency| USD                            |
| Granularity            | Monthly, quarterly, or annual                         | Monthly for Year 1; quarterly for Years 2–3 |
| Model Type             | Top-down, bottom-up, or hybrid                        | Hybrid                          |
| Key Stakeholders       | Who consumes the forecast                             | CFO, Board, Investors           |

### Checklist
- [ ] Historical data validated and reconciled (minimum 12 months)
- [ ] Accounting basis confirmed (accrual vs. cash)
- [ ] One-time items identified and normalized from base period
- [ ] Seasonality patterns documented
- [ ] External benchmarks sourced (industry, peers)

---

## Step 2 — Revenue Modeling

Build the revenue forecast from drivers, not just growth rates.

### Revenue Driver Framework

| Driver                  | Metric                    | Source                        | Example Value    |
|-------------------------|---------------------------|-------------------------------|------------------|
| New customers           | Monthly new logos          | Sales pipeline + conversion   | 25/month         |
| Average deal size       | ACV or ARPU               | Historical median             | $18,000 ACV      |
| Expansion revenue       | Net dollar retention      | Customer success data         | 115% NDR         |
| Churn                   | Gross revenue churn rate  | Historical churn cohorts      | 8% annual        |
| Pricing changes         | Effective price increase  | Planned price adjustment      | +5% in Q3        |
| New product lines       | Incremental revenue       | Go-to-market plan             | $200K in H2      |

### Revenue Build Template

| Month     | Beginning ARR | New ARR | Expansion | Churn   | Ending ARR | Monthly Revenue |
|-----------|---------------|---------|-----------|---------|------------|-----------------|
| Jan       |               |         |           |         |            |                 |
| Feb       |               |         |           |         |            |                 |
| ...       |               |         |           |         |            |                 |
| Dec       |               |         |           |         |            |                 |
| **Total** |               |         |           |         |            |                 |

---

## Step 3 — Expense Projections

Model costs using a combination of committed, planned, and variable components.

### Expense Categories and Drivers

| Category            | Driver / Basis                        | Projection Method                    |
|---------------------|---------------------------------------|--------------------------------------|
| Salaries            | Headcount plan x avg. comp            | Bottom-up from HR plan               |
| Benefits & Taxes    | % of salary (typically 20–30%)        | Rate x salary base                   |
| Contractors         | Planned SOWs + ad-hoc estimate        | Bottom-up + historical %             |
| Cloud / Hosting     | Usage growth tied to revenue/users    | Unit economics x projected volume    |
| Software Licenses   | Per-seat x headcount                  | Committed contracts + new seats      |
| Sales & Marketing   | % of revenue or fixed program budget  | Blended: fixed + variable component  |
| Facilities          | Lease terms + operating costs         | Contractual obligations              |
| Travel              | Per-trip cost x estimated trips       | Policy rate x planned activity       |
| Depreciation        | Asset schedule                        | Straight-line on existing + planned  |
| Interest Expense    | Debt schedule                         | Rate x outstanding balance           |

### Expense Summary Template

| Category            | Q1        | Q2        | Q3        | Q4        | Annual    | % of Revenue |
|---------------------|-----------|-----------|-----------|-----------|-----------|--------------|
| People (total)      |           |           |           |           |           |              |
| Infrastructure      |           |           |           |           |           |              |
| Sales & Marketing   |           |           |           |           |           |              |
| G&A                 |           |           |           |           |           |              |
| D&A                 |           |           |           |           |           |              |
| **Total OpEx**      |           |           |           |           |           |              |

---

## Step 4 — Cash Flow Analysis

Translate the P&L forecast into cash movements.

1. **Operating Cash Flow**: Start with net income; add back non-cash items (D&A, stock-based comp); adjust for working capital changes (AR, AP, deferred revenue).
2. **Investing Cash Flow**: CapEx, acquisitions, asset disposals.
3. **Financing Cash Flow**: Debt draws/repayments, equity raises, dividends.
4. **Net Cash Position**: Ending cash = beginning cash + net cash flow.

### Cash Flow Template

| Line Item                       | Q1       | Q2       | Q3       | Q4       | Annual   |
|---------------------------------|----------|----------|----------|----------|----------|
| Net Income                      |          |          |          |          |          |
| + Depreciation & Amortization   |          |          |          |          |          |
| + Stock-Based Compensation      |          |          |          |          |          |
| +/- Working Capital Changes     |          |          |          |          |          |
| **Operating Cash Flow**         |          |          |          |          |          |
| - Capital Expenditures          |          |          |          |          |          |
| **Investing Cash Flow**         |          |          |          |          |          |
| +/- Debt (net)                  |          |          |          |          |          |
| +/- Equity (net)                |          |          |          |          |          |
| **Financing Cash Flow**         |          |          |          |          |          |
| **Net Change in Cash**          |          |          |          |          |          |
| Beginning Cash Balance          |          |          |          |          |          |
| **Ending Cash Balance**         |          |          |          |          |          |

### Cash Runway Calculation
- Monthly burn rate = average of last 3 months operating cash flow (if negative)
- Cash runway (months) = current cash balance / monthly burn rate
- Flag if runway < 12 months

---

## Step 5 — Scenario Planning

Model three scenarios to bound the range of outcomes.

| Assumption              | Worst Case         | Base Case          | Best Case          |
|-------------------------|--------------------|--------------------|--------------------|
| Revenue growth rate     |                    |                    |                    |
| Gross margin            |                    |                    |                    |
| Headcount additions     |                    |                    |                    |
| Churn rate              |                    |                    |                    |
| Marketing spend         |                    |                    |                    |
| New product revenue     |                    |                    |                    |

### Scenario Summary

| Metric                  | Worst Case         | Base Case          | Best Case          |
|-------------------------|--------------------|--------------------|--------------------| 
| Total Revenue           |                    |                    |                    |
| Total Expenses          |                    |                    |                    |
| EBITDA                  |                    |                    |                    |
| EBITDA Margin           |                    |                    |                    |
| Free Cash Flow          |                    |                    |                    |
| Ending Cash Balance     |                    |                    |                    |
| Cash Runway (months)    |                    |                    |                    |

### Scenario Triggers
Define what real-world events would push toward each scenario:
- **Worst Case**: Major customer loss, market downturn, regulatory change, key hire departures.
- **Best Case**: Viral adoption, large enterprise deal, favorable market shift, successful product launch.

---

## Step 6 — Assumptions Documentation

Every forecast is only as good as its assumptions. Document them explicitly.

### Assumptions Log

| # | Assumption                                    | Value / Range      | Source                  | Confidence | Review Date |
|---|-----------------------------------------------|--------------------|-------------------------|------------|-------------|
| 1 | Monthly new customer acquisition              |                    |                         |            |             |
| 2 | Average contract value                        |                    |                         |            |             |
| 3 | Gross revenue churn rate                      |                    |                         |            |             |
| 4 | Avg. fully-loaded cost per employee           |                    |                         |            |             |
| 5 | Cloud cost per unit                           |                    |                         |            |             |
| 6 | Effective tax rate                            |                    |                         |            |             |
| 7 | Days Sales Outstanding (DSO)                  |                    |                         |            |             |
| 8 | Days Payable Outstanding (DPO)                |                    |                         |            |             |

---

## Output Format

```
## Financial Forecast — [Entity] — [Horizon]

### 1. Executive Summary
- Key takeaway in 3-5 bullets
- Headline numbers: revenue, EBITDA, cash position

### 2. Revenue Forecast
[Driver-based revenue build with monthly/quarterly detail]

### 3. Expense Forecast
[Categorized expense projections]

### 4. P&L Summary
[Income statement: revenue through net income]

### 5. Cash Flow Forecast
[Operating, investing, financing cash flows; ending balance]

### 6. Scenario Analysis
[Side-by-side comparison of worst/base/best]

### 7. Assumptions & Risks
[Numbered assumptions log; key risks and mitigants]

### 8. Appendix
- Monthly detail tables
- Sensitivity tables (e.g., revenue +/- 10%, COGS +/- 5%)
- Bridge from prior forecast to current
```

---

## Quality Checklist

- [ ] Revenue drivers are bottom-up, not just "last year + X%"
- [ ] Expenses tie to headcount plan and committed contracts
- [ ] Cash flow reflects working capital timing, not just P&L
- [ ] Three scenarios are meaningfully different, not just +/- 10%
- [ ] Every assumption has a source and confidence level
- [ ] Model balances (assets = liabilities + equity, if full balance sheet)
- [ ] Forecast is compared to prior forecast and actuals (bridge analysis)
- [ ] Seasonality is reflected in monthly/quarterly phasing

---

## Edge Cases

| Scenario                                | Handling Approach                                                              |
|-----------------------------------------|--------------------------------------------------------------------------------|
| Pre-revenue startup                     | Use TAM/SAM/SOM framework; anchor to comparable company benchmarks             |
| Highly seasonal business                | Use seasonal indices from 2+ years of history; avoid straight-line phasing     |
| Multi-currency operations               | Forecast in local currency; translate at forward FX rates; show FX sensitivity |
| Pending M&A or divestiture              | Model standalone and combined; flag integration costs separately               |
| Regulatory uncertainty (e.g., tax reform)| Model with current rules as base; sensitivity on proposed changes             |
| Rapid hypergrowth (>100% YoY)           | Use cohort-based revenue model; stress-test unit economics at scale           |
