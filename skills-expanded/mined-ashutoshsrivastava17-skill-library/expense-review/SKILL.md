---
name: expense-review
description: >
  Review and analyze expenses with categorization, trend analysis, anomaly detection,
  policy compliance checks, and cost reduction recommendations.
  TRIGGER when: user says /expense-review, "review expenses", "expense analysis", "spending review", "cost analysis", "expense audit".
argument-hint: "[department or cost center] [time period] [focus area]"
user-invocable: true
---

# Expense Review

Perform a structured review of organizational expenses to identify trends, anomalies, policy violations, and cost reduction opportunities. This skill produces an actionable expense analysis with clear findings and recommendations.

---

## Step 1 — Scope the Review

Define what is being reviewed and why.

| Parameter              | Description                                      | Example                         |
|------------------------|--------------------------------------------------|---------------------------------|
| Review Scope           | Department, cost center, project, or company-wide | Engineering department          |
| Time Period            | Period under review                               | Q4 2025                         |
| Comparison Period      | Benchmark for trend analysis                      | Q3 2025 and Q4 2024             |
| Data Source            | ERP, expense management tool, GL export           | NetSuite GL extract             |
| Review Trigger         | Routine, audit finding, budget overrun, ad hoc    | Quarterly routine review        |
| Materiality Threshold  | Minimum amount for detailed line-item review      | Transactions > $1,000           |

### Checklist
- [ ] Data extract is complete and reconciles to GL totals
- [ ] Chart of accounts / category mapping is current
- [ ] Expense policy document is available for reference
- [ ] Prior period data is available for comparison
- [ ] Any known one-time items are pre-flagged

---

## Step 2 — Categorize and Normalize Expenses

Ensure every transaction is properly classified before analysis.

### Standard Category Taxonomy

| L1 Category         | L2 Sub-Category            | GL Code Range | Policy Limit        |
|---------------------|----------------------------|---------------|---------------------|
| People              | Salaries & Wages           | 6000–6099     | Per comp plan       |
| People              | Benefits                   | 6100–6199     | Per benefits plan   |
| People              | Contractors & Temps        | 6200–6299     | SOW-based           |
| Technology          | Cloud & Hosting            | 6300–6349     | Budget-based        |
| Technology          | Software Licenses          | 6350–6399     | Per-seat approval   |
| Technology          | Hardware & Equipment       | 6400–6449     | $2,500/item limit   |
| Facilities          | Rent & Utilities           | 6500–6549     | Lease terms         |
| Facilities          | Office Supplies            | 6550–6599     | $500/month/dept     |
| Travel              | Air & Ground Transport     | 6600–6649     | Policy class limits |
| Travel              | Lodging                    | 6650–6699     | $250/night cap      |
| Travel              | Meals & Entertainment      | 6700–6749     | $75/person/meal     |
| Marketing           | Advertising & Media        | 6800–6849     | Campaign budget     |
| Marketing           | Events & Sponsorships      | 6850–6899     | Pre-approved only   |
| Professional Svcs   | Legal                      | 6900–6929     | Engagement letter   |
| Professional Svcs   | Accounting & Audit         | 6930–6959     | Contract terms      |
| Professional Svcs   | Consulting                 | 6960–6999     | SOW required > $10K |

### Normalization Steps
1. Reclassify any miscategorized transactions.
2. Exclude inter-company transfers and reclass entries.
3. Normalize for one-time or non-recurring items.
4. Convert foreign currency transactions to reporting currency.
5. Pro-rate partial-period items for like-for-like comparison.

---

## Step 3 — Trend Analysis

Compare the review period against benchmarks to identify directional changes.

### Period-over-Period Comparison

| Category            | Prior Period | Current Period | $ Change   | % Change  | Annualized Run Rate |
|---------------------|-------------|----------------|------------|-----------|---------------------|
| People              |             |                |            |           |                     |
| Technology          |             |                |            |           |                     |
| Facilities          |             |                |            |           |                     |
| Travel              |             |                |            |           |                     |
| Marketing           |             |                |            |           |                     |
| Professional Svcs   |             |                |            |           |                     |
| Other               |             |                |            |           |                     |
| **Total**           |             |                |            |           |                     |

### Key Trend Metrics
- **Expense-to-Revenue Ratio**: Total expenses / total revenue (target: depends on stage and industry).
- **Per-Capita Spending**: Total non-people expenses / headcount.
- **Category Mix Shift**: How the percentage allocation across categories has changed.
- **Growth Rate vs. Revenue Growth**: Are expenses growing faster or slower than revenue?

---

## Step 4 — Anomaly Detection

Flag transactions and patterns that deviate from norms.

### Anomaly Detection Rules

| Rule                              | Logic                                                    | Severity |
|-----------------------------------|----------------------------------------------------------|----------|
| Single transaction spike          | Any single transaction > 3x category monthly average     | High     |
| Category budget overrun           | Category spend > 110% of budget                          | High     |
| Duplicate payments                | Same vendor, same amount, within 7 days                  | High     |
| Round-number transactions         | Exact round amounts ($5,000, $10,000) — possible estimate| Medium   |
| Weekend / holiday submissions     | Expense submitted on non-business day                    | Low      |
| Split transactions                | Multiple transactions just below approval threshold      | High     |
| Vendor concentration              | Single vendor > 30% of category spend                    | Medium   |
| Rapid growth vendor               | Vendor spend up > 50% period-over-period                 | Medium   |
| Missing receipts                  | Transactions above receipt threshold lacking documentation| High     |
| Late submissions                  | Expense submitted > 60 days after incurrence             | Medium   |

### Anomaly Log Template

| # | Date       | Vendor      | Amount  | Category   | Anomaly Type           | Severity | Resolution  |
|---|------------|-------------|---------|------------|------------------------|----------|-------------|
| 1 |            |             |         |            |                        |          |             |
| 2 |            |             |         |            |                        |          |             |

---

## Step 5 — Policy Compliance Check

Validate expenses against the organization's expense policy.

### Compliance Checklist

| Policy Rule                                  | Compliant? | Exceptions Found | Action Required         |
|----------------------------------------------|------------|-------------------|-------------------------|
| All expenses have valid receipts             |            |                   |                         |
| Travel booked through approved channel       |            |                   |                         |
| Meals within per-diem limits                 |            |                   |                         |
| Hotel rates within policy cap                |            |                   |                         |
| Manager approval obtained before spend       |            |                   |                         |
| Vendor on approved vendor list               |            |                   |                         |
| Contracts signed for engagements > $10K      |            |                   |                         |
| No personal expenses reimbursed              |            |                   |                         |
| Expense reports submitted within 30 days     |            |                   |                         |
| Proper GL coding applied                     |            |                   |                         |

---

## Step 6 — Cost Reduction Opportunities

Identify actionable savings based on the review findings.

### Opportunity Assessment Template

| # | Opportunity                          | Category    | Est. Annual Savings | Effort   | Timeline  | Owner    |
|---|--------------------------------------|-------------|---------------------|----------|-----------|----------|
| 1 | Renegotiate cloud hosting contract   | Technology  | $45,000             | Medium   | 60 days   |          |
| 2 | Consolidate software licenses        | Technology  | $22,000             | Low      | 30 days   |          |
| 3 | Enforce travel policy compliance     | Travel      | $18,000             | Low      | Immediate |          |
| 4 | Eliminate unused SaaS subscriptions  | Technology  | $15,000             | Low      | 30 days   |          |
| 5 | Shift consulting to internal capacity| Prof. Svcs  | $60,000             | High     | 90 days   |          |

### Prioritization Framework
- **Quick Wins**: Low effort, immediate savings (< 30 days).
- **Medium-Term**: Moderate effort, requires negotiation or process change (30–90 days).
- **Strategic**: High effort, structural change needed (90+ days), but large impact.

---

## Output Format

```
## Expense Review — [Scope] — [Period]

### 1. Executive Summary
- Total spend: $X (change vs. prior period)
- Key findings (3-5 bullets)
- Total identified savings opportunity: $X

### 2. Spend Overview
[Category breakdown table with trends]

### 3. Trend Analysis
[Period-over-period comparison; key ratios]

### 4. Anomalies & Exceptions
[Anomaly log with severity and resolution status]

### 5. Policy Compliance
[Compliance checklist with exception details]

### 6. Cost Reduction Recommendations
[Prioritized opportunity list with savings estimates]

### 7. Action Items
[Owner, deadline, expected outcome for each recommendation]
```

---

## Quality Checklist

- [ ] Data reconciles to GL totals within $1 tolerance
- [ ] All categories are represented; no "uncategorized" bucket > 2%
- [ ] Trend comparison uses like-for-like periods (normalized for one-time items)
- [ ] Anomalies are documented with specific transaction detail
- [ ] Policy compliance findings reference specific policy sections
- [ ] Savings estimates are conservative and methodology is documented
- [ ] Every finding has a clear owner and timeline for resolution

---

## Edge Cases

| Scenario                                  | Handling Approach                                                              |
|-------------------------------------------|--------------------------------------------------------------------------------|
| Incomplete data (missing months)          | Flag data gaps; analyze available periods; note confidence limitation          |
| Chart of accounts changed mid-period      | Map old codes to new taxonomy; document mapping logic                          |
| Acquisition added new cost centers        | Separate acquired entity expenses; analyze organic vs. inorganic trends        |
| Currency volatility skewing comparisons   | Show constant-currency comparison alongside reported figures                   |
| Shared services / cost allocations        | Review allocation methodology; ensure drivers are current and fair             |
| COVID or force-majeure period in baseline | Exclude distorted periods or use 2019 as normalized baseline                   |
