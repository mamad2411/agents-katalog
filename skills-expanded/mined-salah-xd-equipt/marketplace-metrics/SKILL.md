---
name: marketplace-metrics
description: "Defines and tracks marketplace health metrics including liquidity, take rate, GMV, and supply/demand balance. Use when measuring and optimizing marketplace performance."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Marketplace Metrics

## When to Use This Skill

Use this skill when you need to:
- Define the core health metrics for a two-sided marketplace
- Build a metrics dashboard for tracking marketplace performance
- Identify supply/demand imbalances and liquidity problems
- Create reporting frameworks for marketplace growth analysis

**DO NOT** use this skill for SaaS metrics (use saas-metrics-dashboard), financial modeling, or investor reporting. This is for operational marketplace health metrics.

---

## Core Principle

MARKETPLACE HEALTH IS NOT ABOUT TOTAL USERS — IT IS ABOUT WHETHER SUPPLY AND DEMAND ARE FINDING EACH OTHER. LIQUIDITY IS THE METRIC THAT MATTERS MOST.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Marketplace type** | "What does your marketplace connect?" | No default — must be provided |
| **Transaction model** | "How do transactions work? Instant purchase, booking, bidding, messaging?" | Instant purchase |
| **Revenue model** | "Commission, subscription, listing fee, or hybrid?" | Commission |
| **Current scale** | "How many active buyers, sellers, and monthly transactions?" | Pre-launch or early stage |
| **Geographic scope** | "Single market or multiple markets?" | Single market |
| **Key concern** | "What are you most worried about? Supply, demand, or matching?" | Supply/demand balance |

**GATE: Confirm the brief before defining the metrics framework.**

---

## Phase 2: Define Core Metrics

### Tier 1: Marketplace Health (Track Weekly)

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| **GMV** | Total value of all transactions | Overall marketplace size |
| **Take Rate** | Platform revenue / GMV | How much you capture per dollar transacted |
| **Liquidity** | % of listings that result in a transaction within 30 days | Whether supply is meeting demand |
| **Supply/Demand Ratio** | Active sellers / Active buyers | Balance between sides |
| **Match Rate** | Buyer searches that result in a relevant listing / Total searches | Whether buyers find what they want |

### Tier 2: Side-Specific (Track Monthly)

**Supply Metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| Active sellers | Sellers with at least 1 listing in 30 days | Growing month-over-month |
| Listings per seller | Total listings / Active sellers | 3-5+ for product marketplaces |
| Seller activation rate | New sellers with first transaction / New seller signups | 30%+ |
| Seller retention | Sellers active this month who were active last month | 70%+ |

**Demand Metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| Active buyers | Buyers with at least 1 transaction in 30 days | Growing month-over-month |
| Buyer frequency | Transactions per buyer per month | Increasing over time |
| Buyer activation rate | New buyers with first transaction / New buyer signups | 20%+ |
| Repeat buyer rate | Buyers with 2+ transactions / Total buyers | 30%+ |

### Tier 3: Unit Economics (Track Quarterly)

| Metric | Formula | Target |
|--------|---------|--------|
| **Buyer LTV** | Average spend per buyer over lifetime | 3x+ buyer CAC |
| **Seller LTV** | Average revenue generated per seller over lifetime | 3x+ seller CAC |
| **Buyer CAC** | Total buyer acquisition spend / New buyers | Sustainable relative to LTV |
| **Seller CAC** | Total seller acquisition spend / New sellers | Lower than buyer CAC typically |
| **Contribution margin** | (Take rate revenue - variable costs) / GMV | Positive and improving |

**GATE: Confirm which metrics to prioritize before designing the dashboard.**

---

## Phase 3: Build the Dashboard

### Dashboard Layout

**Top row (KPI cards):**
GMV | Take Rate | Liquidity | Active Buyers | Active Sellers

**Row 2 (Trends):**
- GMV trend (12 months, line chart)
- Supply vs. demand trend (dual-axis line chart)

**Row 3 (Health indicators):**
- Liquidity by category (bar chart)
- Match rate trend (line chart)
- Buyer/seller activation funnels (funnel charts)

**Row 4 (Cohort analysis):**
- Buyer cohort retention (heatmap)
- Seller cohort retention (heatmap)

### Alert Thresholds

| Metric | Alert When | Possible Cause |
|--------|-----------|----------------|
| Liquidity drops below 20% | Supply exceeds demand | Too many sellers, not enough buyers |
| Supply/demand ratio exceeds 5:1 | Over-supply | Seller acquisition outpacing demand |
| Match rate below 50% | Poor selection or search | Category gaps or bad search algorithm |
| Buyer repeat rate below 20% | Low buyer satisfaction | Quality issues or trust gaps |
| Take rate declining | Competitive pressure | Sellers negotiating or transacting off-platform |

---

## Phase 4: Polish

### 1. Marketplace Diagnostic Framework

When a metric looks bad, diagnose with this flowchart:

**GMV is flat or declining:**
→ Check buyer count. Is it growing? If no → demand problem.
→ Check average transaction value. Is it dropping? If yes → pricing or mix shift.
→ Check transaction frequency. Is it dropping? If yes → engagement or quality problem.

**Liquidity is low:**
→ Too much supply? → Raise seller quality bar, pause seller recruitment.
→ Not enough demand? → Increase buyer acquisition spend.
→ Matching problem? → Improve search, categories, or recommendations.

### 2. Reporting Template

```
## Monthly Marketplace Report — [Month Year]

### Key Metrics
| Metric | This Month | Last Month | Change |
|--------|-----------|-----------|--------|
| GMV | | | |
| Take Rate | | | |
| Liquidity | | | |
| Active Buyers | | | |
| Active Sellers | | | |
| Repeat Buyer Rate | | | |

### Highlights
- [Top achievement or milestone]
- [Growth in a key metric]

### Concerns
- [Metric trending in wrong direction]
- [Action being taken to address it]

### Focus for Next Month
1. [Priority 1]
2. [Priority 2]
```

### 3. Quality Checklist

```
## Marketplace Metrics Checklist

- [ ] GMV tracked and trending monthly
- [ ] Take rate calculated correctly (revenue / GMV)
- [ ] Liquidity measured by category (not just overall)
- [ ] Supply and demand tracked separately with activation rates
- [ ] Match rate or search success rate is measured
- [ ] Buyer and seller retention tracked by cohort
- [ ] Unit economics (LTV, CAC) calculated quarterly
- [ ] Alert thresholds set for critical metrics
- [ ] Monthly reporting template is in use
- [ ] Diagnostic framework available for when metrics decline
```

---

## Example

**Marketplace:** Local home services
**Monthly snapshot:**
```
GMV: $145,000 (+12% MoM)
Take Rate: 14%
Platform Revenue: $20,300
Liquidity: 34% (34 of 100 listed contractors got a booking)
Active Buyers: 280
Active Sellers: 100
Supply/Demand Ratio: 1:2.8
Repeat Buyer Rate: 41%
```

**Diagnostic:** "Liquidity at 34% suggests we have more contractors than buyer demand can absorb. Recommendation: pause contractor recruitment, increase buyer acquisition spend by 30%, and launch a referral program for buyers."

---

## Anti-Patterns

- **Tracking GMV without take rate** — GMV means nothing if you are not capturing revenue. Always pair them.
- **Ignoring liquidity** — a marketplace with 10,000 listings and no transactions is a graveyard. Liquidity is the true health indicator.
- **Treating both sides the same** — buyer and seller metrics must be tracked separately. A healthy buyer side can mask a dying seller side.
- **Vanity metrics** — total signups, page views, and app downloads tell you nothing about marketplace health. Track activity and transactions.
- **No cohort analysis** — aggregate retention hides whether new cohorts are performing better or worse than older ones.

---

## Recovery

- **No transaction data yet (pre-launch):** Track supply-side metrics (listings, seller signups, listing quality) and demand signals (waitlist signups, search queries).
- **Liquidity is very low:** Narrow the marketplace scope. Focus on one category or one geography until liquidity exceeds 30%.
- **Cannot calculate LTV yet:** Start with average transaction value and repeat rate. LTV calculation becomes meaningful after 6+ months of data.
- **Metrics are inconsistent:** Define every formula in a data dictionary. Ensure buyer, seller, and transaction definitions are used consistently.
