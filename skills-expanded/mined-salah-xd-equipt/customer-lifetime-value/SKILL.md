---
name: customer-lifetime-value
description: "Calculates customer lifetime value with segmentation, prediction models, and retention investment recommendations. Use when determining how much a customer is worth over time."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Customer Lifetime Value

## When to Use This Skill

Use this skill when you need to:
- Calculate customer lifetime value (CLV/LTV) for your business
- Segment customers by value to prioritize retention efforts
- Determine how much to spend on customer acquisition (CAC:LTV ratio)
- Build a CLV model for forecasting and budgeting

**DO NOT** use this skill for short-term revenue forecasting, individual customer profitability analysis, or financial auditing. This is for CLV modeling and strategic decision-making.

---

## Core Principle

CLV IS THE SINGLE MOST IMPORTANT METRIC FOR SUSTAINABLE GROWTH — IT TELLS YOU HOW MUCH YOU CAN AFFORD TO SPEND TO ACQUIRE AND RETAIN A CUSTOMER.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business model** | "Subscription, one-time purchase, repeat purchase, or hybrid?" | Must be provided |
| **Average order value** | "What does a customer spend per transaction?" | Must be provided |
| **Purchase frequency** | "How often does a customer buy? (monthly, quarterly, annually)" | Must be provided |
| **Customer lifespan** | "How long does a typical customer stay? (months or years)" | Estimated from churn |
| **Churn rate** | "What percentage of customers leave each month/year?" | Estimate from data |
| **Gross margin** | "What is your gross margin percentage?" | 60-70% for digital |
| **Segments** | "Any customer segments to analyze separately? (plan tier, channel, geography)" | Overall first |

**GATE: Confirm inputs before calculating.**

---

## Phase 2: Calculate

### CLV Formulas

**Simple CLV (good starting point):**
`CLV = Average Order Value x Purchase Frequency x Customer Lifespan`

**Margin-Adjusted CLV:**
`CLV = (AOV x Frequency x Lifespan) x Gross Margin %`

**Subscription CLV:**
`CLV = (Monthly Revenue per Customer / Monthly Churn Rate) x Gross Margin %`

### CAC:LTV Ratio

- **Healthy:** LTV is 3x+ CAC
- **Warning:** LTV is 1-3x CAC (growth is expensive)
- **Danger:** LTV is below CAC (losing money on every customer)

**GATE: Present the baseline CLV calculation and confirm accuracy before segmenting.**

---

## Phase 3: Build

### Deliverables

**1. CLV Calculation Worksheet**
- Formula with all inputs clearly documented
- Overall CLV number with margin adjustment
- CAC:LTV ratio with interpretation
- Payback period: months to recover acquisition cost

**2. Segmented CLV Analysis**
- CLV by customer segment (plan tier, acquisition channel, cohort)
- High-value segment profile: what do your best customers look like?
- Low-value segment: are there customers costing more than they generate?

**3. Sensitivity Analysis**
- How CLV changes if churn improves by 5%, 10%, 20%
- How CLV changes if AOV increases by 10%, 20%
- Which lever has the biggest impact on CLV?

**4. Strategic Recommendations**
- Retention investment: how much to spend keeping customers based on CLV
- Acquisition budget: maximum CAC based on target LTV ratio
- Expansion revenue opportunities: upsell potential per segment

---

## Phase 4: Polish

### CLV Dashboard Metrics

Track monthly:
- Average CLV (overall and by segment)
- CAC:LTV ratio trend
- Churn rate trend (the biggest CLV driver)
- Revenue per customer trend

### Quarterly Review

Recalculate CLV quarterly as inputs change. Update acquisition and retention budgets accordingly.

---

## Example 1: SaaS Subscription ($49/month, 5% monthly churn)

**CLV:** $49 / 0.05 = $980 gross, $686 margin-adjusted (70% margin)
**Healthy CAC target:** Under $229 (3:1 ratio)
**Key lever:** Reducing churn from 5% to 4% increases CLV by 25% to $857

## Example 2: E-commerce (AOV $75, 3 purchases/year, 2.5 year lifespan)

**CLV:** $75 x 3 x 2.5 = $562 gross, $281 margin-adjusted (50% margin)
**Healthy CAC target:** Under $94 (3:1 ratio)
**Key lever:** Increasing frequency from 3 to 4 purchases/year increases CLV by 33%

---

## Anti-Patterns

- **Using revenue instead of margin** — CLV based on revenue overstates value. Always adjust for gross margin.
- **Ignoring churn** — assuming customers stay forever inflates CLV to meaningless numbers.
- **One-size-fits-all CLV** — your best customers may be worth 10x your worst. Segment or miss the insight.
- **Static calculation** — CLV changes as your product, pricing, and retention improve. Recalculate regularly.
- **CLV without CAC context** — CLV alone is a vanity metric. The ratio to acquisition cost is what matters.

---

## Recovery

- **No churn data:** Estimate from revenue trends or customer count changes. Even a rough estimate is better than ignoring churn.
- **Too early for reliable data:** Calculate based on 3-month data and label it "projected." Revisit quarterly as data accumulates.
- **CLV is lower than CAC:** This is a critical finding. Prioritize: reduce CAC, improve retention, increase AOV, or raise prices.
- **User unsure of gross margin:** Use industry defaults (SaaS: 70-80%, e-commerce: 30-50%, services: 50-70%) and refine later.
