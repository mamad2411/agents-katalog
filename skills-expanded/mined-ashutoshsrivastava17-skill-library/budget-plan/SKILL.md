---
name: budget-plan
description: >
  Create and manage comprehensive budgets including revenue projections, cost categories,
  allocation strategy, variance tracking, and approval workflows.
  TRIGGER when: user says /budget-plan, "create a budget", "budget planning", "allocate budget", "budget template", "annual budget", "quarterly budget".
argument-hint: "[department or project name] [time period] [total budget amount]"
user-invocable: true
---

# Budget Plan

Create structured, defensible budgets for departments, projects, or the entire organization. This skill walks through revenue projections, cost categorization, allocation strategy, variance thresholds, and approval workflows.

---

## Step 1 — Define Budget Scope and Parameters

Gather the foundational inputs before building any numbers.

| Parameter            | Description                                      | Example                        |
|----------------------|--------------------------------------------------|--------------------------------|
| Budget Owner         | Department or project lead responsible            | VP of Engineering              |
| Time Period          | Fiscal quarter, half-year, or full year           | FY2026 (Jan–Dec)               |
| Budget Type          | Operating, capital, project, or zero-based        | Operating                      |
| Currency             | Reporting currency and FX considerations          | USD                            |
| Total Envelope       | Hard cap or flexible ceiling                      | $2.4M hard cap                 |
| Approval Authority   | Who signs off at each tier                        | Dir < $50K, VP < $250K, CFO above |
| Baseline Reference   | Prior period actuals or industry benchmarks        | FY2025 actuals                 |

### Checklist
- [ ] Confirm fiscal calendar alignment (calendar year vs. fiscal year)
- [ ] Identify all cost centers and GL codes in scope
- [ ] Obtain prior-period actuals (minimum 2 periods for trend)
- [ ] Clarify headcount plan and hiring timeline
- [ ] Document any board-mandated constraints (e.g., "hold OpEx flat")

---

## Step 2 — Revenue Projections

Model the revenue side before allocating costs.

1. **Historical Trend**: Pull 3–5 periods of revenue data; compute CAGR and sequential growth.
2. **Pipeline-Weighted Forecast**: Apply probability weights to sales pipeline stages.
3. **Segment Breakdown**: Split by product line, geography, or customer tier.
4. **Sensitivity Band**: Model optimistic (+15%), base, and conservative (-15%) scenarios.

### Revenue Projection Template

| Revenue Stream       | FY2025 Actual | Base Growth % | FY2026 Base | Optimistic | Conservative |
|----------------------|---------------|---------------|-------------|------------|--------------|
| Product A            |               |               |             |            |              |
| Product B            |               |               |             |            |              |
| Services             |               |               |             |            |              |
| Other                |               |               |             |            |              |
| **Total Revenue**    |               |               |             |            |              |

---

## Step 3 — Cost Categorization

Classify every line item into a standard taxonomy.

| Category             | Sub-Category          | Fixed / Variable | Discretionary? |
|----------------------|-----------------------|------------------|----------------|
| People               | Salaries & Wages      | Fixed            | No             |
| People               | Benefits & Taxes      | Fixed            | No             |
| People               | Contractors           | Variable         | Yes            |
| Infrastructure       | Cloud / Hosting       | Variable         | Partially      |
| Infrastructure       | Software Licenses     | Fixed            | Yes            |
| Infrastructure       | Hardware / Equipment  | Fixed            | Yes            |
| Go-to-Market         | Advertising           | Variable         | Yes            |
| Go-to-Market         | Events & Sponsorships | Variable         | Yes            |
| Operations           | Office & Facilities   | Fixed            | No             |
| Operations           | Travel & Entertainment| Variable         | Yes            |
| R&D                  | Research Programs     | Variable         | Yes            |
| R&D                  | Tooling & Prototyping | Variable         | Yes            |

### Checklist
- [ ] Every line item maps to a GL code
- [ ] Fixed vs. variable classification is validated with Finance
- [ ] Discretionary flags are agreed with budget owner
- [ ] No "miscellaneous" bucket exceeds 5% of total budget

---

## Step 4 — Allocation Strategy

Distribute the budget envelope across categories.

1. **Priority Ranking**: Rank categories by strategic alignment (must-have, should-have, nice-to-have).
2. **Baseline Lock**: Lock non-discretionary fixed costs first (salaries, rent, committed contracts).
3. **Growth Investment**: Allocate a defined percentage (e.g., 15–25%) to growth initiatives.
4. **Reserve Buffer**: Hold 3–5% as contingency for unplanned needs.
5. **Quarterly Phasing**: Spread allocations by quarter, accounting for seasonality and hiring ramps.

### Allocation Summary Template

| Category             | Annual Allocation | Q1        | Q2        | Q3        | Q4        | % of Total |
|----------------------|-------------------|-----------|-----------|-----------|-----------|------------|
| People               |                   |           |           |           |           |            |
| Infrastructure       |                   |           |           |           |           |            |
| Go-to-Market         |                   |           |           |           |           |            |
| Operations           |                   |           |           |           |           |            |
| R&D                  |                   |           |           |           |           |            |
| Contingency Reserve  |                   |           |           |           |           |            |
| **Total**            |                   |           |           |           |           | 100%       |

---

## Step 5 — Variance Tracking Framework

Define how actuals will be monitored against the plan.

| Metric                    | Threshold (Yellow) | Threshold (Red) | Review Cadence | Escalation Path        |
|---------------------------|--------------------|-----------------|----------------|------------------------|
| Line-item variance        | > 5%               | > 10%           | Monthly        | Budget owner -> Dir    |
| Category variance         | > 8%               | > 15%           | Monthly        | Dir -> VP              |
| Total budget variance     | > 3%               | > 7%            | Monthly        | VP -> CFO              |
| Forecast-to-actual delta  | > 5%               | > 12%           | Quarterly      | FP&A -> CFO            |
| Headcount vs. plan        | +/- 1 HC           | +/- 3 HC        | Monthly        | HR + Finance           |

### Variance Response Actions
- **Yellow**: Document root cause; adjust forecast; no reallocation needed.
- **Red**: Mandatory reforecast within 5 business days; reallocation proposal required; leadership review.

---

## Step 6 — Approval Workflow

Route the budget through the appropriate sign-off chain.

1. **Draft Submission**: Budget owner submits to FP&A for structural review.
2. **FP&A Review**: Validate assumptions, cross-check with headcount plan, flag anomalies (2 business days).
3. **Department Head Approval**: Sign-off on priorities and trade-offs.
4. **Finance Leadership Review**: CFO or Finance Director reviews aggregate picture.
5. **Executive / Board Approval**: For budgets above materiality threshold or with strategic implications.
6. **Lock and Publish**: Freeze approved numbers in the financial system; distribute to cost center owners.

### Approval Checklist
- [ ] All assumptions documented and sourced
- [ ] Headcount plan reconciled with HR
- [ ] Capital vs. operating expenditure correctly classified
- [ ] Inter-department transfers and chargebacks reflected
- [ ] Prior-period variance commentary included
- [ ] Contingency reserve justified

---

## Output Format

Deliver the budget plan as a structured document containing:

```
## Budget Plan — [Department / Project] — [Time Period]

### 1. Executive Summary
- Total budget: $X
- Key assumptions (3-5 bullets)
- Major changes vs. prior period

### 2. Revenue Projections (if applicable)
[Revenue table with scenarios]

### 3. Cost Breakdown
[Categorized cost table with quarterly phasing]

### 4. Allocation Rationale
[Priority ranking and strategic justification]

### 5. Variance Thresholds & Governance
[Threshold table and escalation paths]

### 6. Approval Status
[Sign-off tracker with dates]

### 7. Appendix
- Detailed line-item schedule
- Assumption log
- Comparison to prior period
```

---

## Quality Checklist

- [ ] Revenue and cost figures reconcile to the total envelope
- [ ] All line items have an owner and a GL code
- [ ] Quarterly phasing sums to annual totals
- [ ] Assumptions are explicit, not buried in formulas
- [ ] Variance thresholds are realistic and agreed upon
- [ ] Approval workflow has clear SLAs
- [ ] Document is version-controlled with change log

---

## Edge Cases

| Scenario                              | Handling Approach                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------------|
| Mid-year organizational restructure   | Trigger a budget reforecast; re-map cost centers; preserve audit trail            |
| Unexpected headcount freeze           | Lock people costs; redistribute freed funds to highest-priority discretionary items|
| Currency fluctuation > 10%            | Apply hedging assumptions; report in both local and reporting currency            |
| Merger or acquisition mid-cycle       | Create a separate integration budget; do not co-mingle with BAU budget           |
| Zero-based budgeting mandate          | Require every line item to be justified from zero; no automatic rollover          |
| Grant or restricted funding           | Track separately with fund accounting; ensure compliance with donor restrictions  |
