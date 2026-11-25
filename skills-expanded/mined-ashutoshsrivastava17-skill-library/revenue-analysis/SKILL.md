---
name: revenue-analysis
description: >
  Analyze revenue streams including growth trends, cohort analysis, churn and retention metrics,
  pricing impact assessment, and segment performance breakdown.
  TRIGGER when: user says /revenue-analysis, "analyze revenue", "revenue breakdown", "churn analysis", "retention metrics", "revenue growth", "pricing analysis".
argument-hint: "[business or product name] [time period] [segment or focus area]"
user-invocable: true
---

# Revenue Analysis

Perform a deep analysis of revenue streams to understand growth drivers, retention dynamics, pricing effectiveness, and segment performance. This skill produces actionable insights for leadership and go-to-market teams.

---

## Step 1 — Define Analysis Scope

Establish the boundaries and objectives of the revenue analysis.

| Parameter              | Description                                        | Example                          |
|------------------------|----------------------------------------------------|----------------------------------|
| Business / Product     | Which entity or product line to analyze             | Acme SaaS Platform               |
| Time Period            | Analysis window                                     | Jan 2025 – Dec 2025 (12 months) |
| Comparison Period      | Benchmark period                                    | Jan 2024 – Dec 2024             |
| Revenue Model          | Subscription, transactional, hybrid, usage-based    | Subscription (annual + monthly)  |
| Segmentation Axes      | How to slice the data                               | Plan tier, geography, company size|
| Data Sources           | Billing system, CRM, data warehouse                 | Stripe + Salesforce + Snowflake  |

### Checklist
- [ ] Revenue data reconciles to GL / financial statements
- [ ] Customer master data is clean (no duplicates, correct segments)
- [ ] Contract dates and terms are accurate (start, end, renewal)
- [ ] Revenue recognition rules are understood (ASC 606 implications)
- [ ] FX rates available for multi-currency analysis

---

## Step 2 — Revenue Growth Trends

Analyze the trajectory of revenue over time.

### Revenue Summary Table

| Period   | Total Revenue | MRR / ARR  | QoQ Growth | YoY Growth | Organic Growth | Inorganic |
|----------|---------------|------------|------------|------------|----------------|-----------|
| Q1       |               |            |            |            |                |           |
| Q2       |               |            |            |            |                |           |
| Q3       |               |            |            |            |                |           |
| Q4       |               |            |            |            |                |           |
| **FY**   |               |            |            |            |                |           |

### Growth Decomposition

Break total revenue growth into its components:

| Growth Component         | $ Contribution | % of Total Growth | Description                         |
|--------------------------|----------------|-------------------|-------------------------------------|
| New Customer Acquisition |                |                   | Revenue from first-time customers   |
| Expansion (Upsell)       |                |                   | Existing customers buying more      |
| Expansion (Cross-sell)   |                |                   | Existing customers buying new products|
| Price Increases          |                |                   | Same usage at higher price          |
| Contraction              |                |                   | Existing customers downsizing       |
| Churn                    |                |                   | Lost customers                      |
| **Net Growth**           |                |                   |                                     |

### Revenue Waterfall
```
Beginning ARR  →  + New  →  + Expansion  →  - Contraction  →  - Churn  →  Ending ARR
```

---

## Step 3 — Cohort Analysis

Understand how revenue from each customer cohort evolves over time.

### Monthly Cohort Retention Table

| Cohort    | M0 (Starting) | M3     | M6     | M9     | M12    | M18    | M24    |
|-----------|----------------|--------|--------|--------|--------|--------|--------|
| Jan 2024  |                |        |        |        |        |        |        |
| Apr 2024  |                |        |        |        |        |        |        |
| Jul 2024  |                |        |        |        |        |        |        |
| Oct 2024  |                |        |        |        |        |        |        |
| Jan 2025  |                |        |        |        |        |        |        |
| Apr 2025  |                |        |        |        |        |        |        |

*Values can be expressed as % of M0 revenue retained (gross retention) or including expansion (net retention).*

### Cohort Analysis Questions
1. Are newer cohorts retaining better or worse than older ones?
2. Is there a consistent drop-off point (e.g., M3 cliff)?
3. Do cohorts expand over time (net retention > 100%)?
4. Are there seasonal patterns in cohort quality?
5. Which acquisition channel produces the highest-LTV cohorts?

---

## Step 4 — Churn and Retention Metrics

Calculate and analyze the key retention KPIs.

### Retention Metrics Dashboard

| Metric                         | Formula                                                      | Current | Prior  | Benchmark |
|--------------------------------|--------------------------------------------------------------|---------|--------|-----------|
| Gross Revenue Retention (GRR)  | (Beginning ARR - Churn - Contraction) / Beginning ARR        |         |        | > 90%     |
| Net Dollar Retention (NDR)     | (Beginning ARR + Expansion - Churn - Contraction) / Beg. ARR |         |        | > 110%    |
| Logo Retention Rate            | (Beginning Customers - Churned) / Beginning Customers        |         |        | > 85%     |
| Monthly Churn Rate             | Churned MRR / Beginning MRR                                  |         |        | < 2%      |
| Average Revenue per Account    | Total ARR / Total Customers                                  |         |        | Growing   |
| Customer Lifetime (months)     | 1 / Monthly Churn Rate                                       |         |        | > 36      |
| LTV                            | ARPA x Gross Margin x Customer Lifetime                      |         |        |           |

### Churn Root Cause Analysis

| Churn Reason               | # Customers | Lost ARR    | % of Total Churn | Preventable? |
|----------------------------|-------------|-------------|-------------------|--------------|
| Product fit / feature gaps |             |             |                   | Yes          |
| Competitive displacement   |             |             |                   | Partially    |
| Budget cuts / downsizing   |             |             |                   | No           |
| Poor onboarding / support  |             |             |                   | Yes          |
| Champion departure         |             |             |                   | Partially    |
| Acquired / merged          |             |             |                   | No           |
| Non-payment / collections  |             |             |                   | Partially    |
| Other / unknown            |             |             |                   |              |

---

## Step 5 — Pricing Impact Assessment

Evaluate how pricing changes have affected revenue.

### Pricing Analysis Framework

| Dimension                   | Analysis                                                    |
|-----------------------------|-------------------------------------------------------------|
| Price Realization           | Actual revenue per unit vs. list price (discount depth)     |
| Discount Distribution       | Histogram of discount % across deals                        |
| Price Increase Adoption     | % of renewals accepting price increases vs. churning        |
| Plan Mix Shift              | Movement from lower to higher tiers (or vice versa)         |
| Usage vs. Seat Economics    | Revenue per seat vs. revenue per unit of usage              |
| Competitive Price Position  | Where your pricing sits relative to alternatives            |

### Price-Volume Decomposition

| Component         | $ Impact     | Description                                          |
|-------------------|--------------|------------------------------------------------------|
| Price Effect      |              | Revenue change from price changes, holding volume constant |
| Volume Effect     |              | Revenue change from volume changes, holding price constant |
| Mix Effect        |              | Revenue change from shift in product/plan mix        |
| FX Effect         |              | Revenue change from currency movements               |
| **Total Change**  |              |                                                      |

---

## Step 6 — Segment Performance

Break down revenue by the most meaningful dimensions.

### Segment Breakdown Template

*Repeat for each segmentation axis (geography, plan tier, company size, industry, channel).*

| Segment            | Revenue    | % of Total | Growth (%) | GRR    | NDR    | ARPA   | # Customers |
|--------------------|------------|------------|------------|--------|--------|--------|-------------|
| Segment A          |            |            |            |        |        |        |             |
| Segment B          |            |            |            |        |        |        |             |
| Segment C          |            |            |            |        |        |        |             |
| Segment D          |            |            |            |        |        |        |             |
| **Total**          |            | 100%       |            |        |        |        |             |

### Segment Health Assessment

| Segment   | Revenue Trend | Retention Trend | Profitability | Strategic Priority | Action           |
|-----------|---------------|-----------------|---------------|--------------------|------------------|
| Segment A | Growing       | Stable          | High          | Core               | Invest & expand  |
| Segment B | Growing       | Declining       | Medium        | Watch              | Fix retention    |
| Segment C | Flat          | Stable          | Low           | Evaluate           | Improve margins  |
| Segment D | Declining     | Declining       | Negative      | Sunset             | Manage exit      |

---

## Output Format

```
## Revenue Analysis — [Business/Product] — [Period]

### 1. Executive Summary
- Total revenue and growth rate
- Key driver of growth (or decline)
- Retention headline (NDR, GRR)
- Top opportunity and top risk

### 2. Growth Trends
[Revenue summary with growth decomposition]

### 3. Cohort Analysis
[Cohort retention table with key observations]

### 4. Churn & Retention
[Retention metrics dashboard; churn root cause analysis]

### 5. Pricing Analysis
[Price-volume decomposition; discount analysis]

### 6. Segment Performance
[Segment breakdown with health assessment]

### 7. Recommendations
[Prioritized actions to accelerate growth and reduce churn]

### 8. Appendix
- Monthly revenue detail
- Customer-level top accounts analysis
- Methodology notes
```

---

## Quality Checklist

- [ ] Revenue figures reconcile to audited financial statements
- [ ] Cohort definitions are consistent and documented
- [ ] Retention metrics use consistent numerator/denominator definitions
- [ ] Churn reasons are based on actual exit interview data, not assumptions
- [ ] Pricing analysis accounts for discounts, credits, and free periods
- [ ] Segment classifications are mutually exclusive and collectively exhaustive
- [ ] Growth decomposition sums to actual total growth
- [ ] Recommendations are specific, measurable, and assigned

---

## Edge Cases

| Scenario                                | Handling Approach                                                                |
|-----------------------------------------|----------------------------------------------------------------------------------|
| Usage-based revenue model               | Analyze revenue per unit of consumption; cohort by usage tier, not just time     |
| Multi-product company                   | Analyze each product separately then show cross-sell dynamics between them       |
| Free-to-paid conversion funnel          | Track conversion rates by cohort; include freemium in funnel, not in ARR        |
| Large enterprise deals with custom terms| Normalize to standard terms for comparison; flag outliers                        |
| Revenue recognized over time (ASC 606)  | Analyze both bookings (TCV/ACV) and recognized revenue separately               |
| Marketplace or platform revenue         | Separate take rate analysis from GMV growth; track both sides of marketplace     |
