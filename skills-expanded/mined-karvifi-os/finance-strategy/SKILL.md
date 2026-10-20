---
name: finance-strategy
description: Financial analysis, modeling, unit economics, fundraising strategy, and financial planning
triggers: [finance, financial model, unit economics, revenue, costs, fundraising, valuation, budget]
---

# SKILL: Finance Strategy

## Purpose
Make financially sound decisions based on models, not feelings.
Understand the numbers that actually drive your business.

## Unit Economics — The Foundation of Everything

### SaaS/Subscription Metrics
```
CAC (Customer Acquisition Cost):
  CAC = Total Sales + Marketing Spend / New Customers Acquired in Period
  Example: $50,000 spend, 100 customers = $500 CAC
  Benchmark: CAC < LTV/3 (ideally < LTV/5)

LTV (Lifetime Value):
  LTV = ARPU × Gross Margin % × Average Customer Lifetime
  Or: LTV = ARPU × Gross Margin % / Churn Rate
  Example: $100/mo ARPU × 80% margin / 5% monthly churn = $1,600 LTV

LTV:CAC Ratio:
  < 1:1 = unsustainable (losing money on every customer)
  1:1 - 3:1 = improving but not there yet
  3:1 - 5:1 = healthy (industry benchmark target)
  > 5:1 = potentially underinvesting in growth

CAC Payback Period:
  Payback = CAC / (Monthly Revenue × Gross Margin %)
  Example: $500 CAC / ($100 × 80%) = 6.25 months
  Target: < 12 months for B2C, < 18 months for B2B

Churn Rate:
  Monthly: (Customers Lost in Month / Customers at Start of Month) × 100%
  Annual: approximately 12x monthly churn (more precisely: 1 - (1-monthly_churn)^12)
  Target: B2B SaaS < 5% annual, B2C < 20% annual
  Negative churn: expansion revenue > churned revenue (best state to be in)
```

### E-commerce Metrics
```
Contribution Margin = Revenue - COGS - Variable Costs
  Must be > $0 before counting CAC
  Benchmark: > 30% of GMV for healthy economics

Repeat Purchase Rate:
  % of customers who buy more than once in 12 months
  Target: > 30% for sustainable e-commerce

Average Order Value (AOV):
  Total Revenue / Number of Orders
  Increase via: upsell, cross-sell, bundles, minimum order for free shipping

Customer Lifetime (CLT):
  Average months before customer churns
  = 1 / Monthly Churn Rate
```

## Financial Model Structure

### 3-Statement Model
```
Income Statement (P&L):
  Revenue
  - Cost of Goods Sold (COGS)
  = Gross Profit (Gross Margin %)
  - Operating Expenses (R&D, S&M, G&A)
  = EBITDA
  - Depreciation & Amortization
  = EBIT (Operating Income)
  - Interest
  = EBT (Pre-tax income)
  - Taxes
  = Net Income

Balance Sheet:
  Assets: Cash, AR, Inventory, PP&E
  Liabilities: AP, Debt, Deferred Revenue
  Equity: Paid-in Capital, Retained Earnings

Cash Flow Statement:
  Operating Cash Flow (most important — shows real cash generation)
  Investing Cash Flow
  Financing Cash Flow
  Net Change in Cash
```

### SaaS Revenue Model
```
MRR (Monthly Recurring Revenue):
  Starting MRR
  + New MRR (from new customers)
  + Expansion MRR (upgrades, seat additions)
  - Churned MRR (cancellations)
  - Contraction MRR (downgrades)
  = Ending MRR

ARR = MRR × 12 (for reporting — but model in monthly)

Growth Rate:
  MoM growth = (Current MRR - Prior MRR) / Prior MRR × 100%
  Target (early stage): 15-20% MoM = 5-6x annual growth
  Target (growth stage): 5-10% MoM = 2-3x annual growth

Rule of 40 (growth + profitability):
  Revenue Growth Rate % + EBITDA Margin % ≥ 40%
  Example: 60% growth + (-20%) margin = 40 ✓ (healthy for growth stage)
```

## Startup Financial Planning

### Runway Calculation
```
Burn Rate = Total Monthly Expenses - Monthly Revenue
Runway = Cash Balance / Net Burn Rate
Target: minimum 18 months of runway at all times

Default Alive / Default Dead:
  If growing at current rate with current expenses...
  Will you reach profitability before you run out of cash?
  "Default Alive" = yes. "Default Dead" = no (raise or cut).

Break-even calculation:
  Break-even Month = Month where Cumulative Revenue = Cumulative Costs
  Or: Monthly Revenue ≥ Monthly Expenses
```

### Fundraising Strategy

**When to raise**:
- 18 months before you would run out of cash
- After demonstrating clear product-market fit signals
- When capital will significantly accelerate what you've already proven works

**How much to raise**:
```
Raise = 18-24 months of runway at planned spending level
Example: $200k/month burn → raise $3.6-4.8M

Dilution target:
  Pre-seed: give up 10-20% (raise $250k-$1M)
  Seed: give up 15-25% (raise $1-5M)
  Series A: give up 20-30% (raise $5-20M)
```

**Valuation benchmarks**:
```
Pre-revenue: $2-5M (team, IP, market size)
$10k MRR: $1-3M valuation (100-300x MRR)
$100k MRR: $5-15M valuation  
$1M MRR: $20-80M valuation (ARR-based: 5-20x ARR)

Series A benchmarks (2024):
  $1-2M ARR + strong growth + clear path to $10M ARR
  Net revenue retention > 100% (expansion > churn)
  Gross margins > 60%
```

**Investor-ready metrics dashboard**:
```
Metric          Current   MoM Growth   Benchmark
ARR             $___      ____%        > $1M for Series A
MoM Growth      ____%     —            > 15% early, > 5% growth
Gross Margin    ____%     —            > 60% (SaaS), > 30% (marketplace)
Net Dollar Ret. ____%     —            > 100%
CAC Payback     ___ mo    —            < 18 months
Burn Multiple   ___x      —            < 1.5x (ARR added per $ burned)
Runway          ___ mo    —            > 18 months
```

## Financial Controls

**Monthly Close Checklist**:
```
□ All revenue recognized correctly (deferred revenue for prepaid)
□ COGS allocated correctly (hosting, support, implementation)
□ Payroll and contractor invoices processed
□ Credit card statements reconciled
□ Bank statement reconciled
□ MRR/ARR metrics updated
□ Cash runway recalculated
□ P&L vs. budget variance explained
□ Balance sheet reviewed for anomalies
```

## Output
- Unit economics model (CAC, LTV, payback period)
- 24-month financial model (P&L, cash flow)
- Fundraising strategy (timing, amount, dilution)
- Investor metrics dashboard

## Quality checks
- [ ] LTV > 3x CAC (if not, fix before raising)
- [ ] CAC payback < 18 months
- [ ] 18+ months of runway after any planned raise
- [ ] Revenue model accounts for churn (not just growth)
- [ ] Model has downside scenario (not just base case)
- [ ] All assumptions explicitly stated and backed by data
