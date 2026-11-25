---
name: pricing-strategy-advisory
description: Advise on pricing strategy — competitive analysis, willingness-to-pay research, tier design, price increase modeling, discount frameworks, and packaging optimization for startup monetization.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, pricing, monetization, tier-design, price-optimization]
related_skills: [unit-economics-analysis, profitability-analysis, revenue-forecasting, strategic-initiative-modeling, business-case-modeling]
inputs_required: [current-pricing-structure, competitor-pricing-intelligence, customer-willingness-to-pay-data, unit-economics-by-segment]
deliverables: [competitive-pricing-landscape, recommended-pricing-model-and-tier-structure, price-increase-impact-analysis, discount-framework-and-approval-guidelines]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Pricing Strategy Advisory

Advise the CEO and leadership on pricing — how much to charge, how to structure tiers, when and how to raise prices, and how to package the product for maximum value capture. Goal: the company charges what it's worth, not what it's afraid to ask for.

## Purpose

Pricing is the single most leveraged lever in the business — a 10% price increase flows almost entirely to profit, and poor pricing leaves millions on the table. Yet most startups underprice by 30-50% because founders are afraid of losing deals. This skill provides the frameworks, analyses, and confidence to set prices that capture the value the product actually delivers, design tiers that maximize willingness-to-pay capture, and execute price increases without destroying customer relationships.

## When to Use

- "How should we price our product?"
- "Review our pricing tiers / packaging"
- "Should we raise prices?"
- "Competitive pricing analysis"
- "Model the impact of a price change"
- "Design our enterprise pricing"
- "Good-better-best tier strategy"

## Inputs Required

1. **Current pricing** — tiers, features per tier, pricing model (per-seat, usage, flat), current prices.
2. **Competitor pricing** — public pricing pages, sales intel, customer feedback.
3. **Customer data** — willingness to pay signals, feature adoption by tier, churn reasons related to pricing.
4. **Unit economics** — from `unit-economics-analysis` (CAC, LTV, gross margins per segment).

## Quick Reference

| Pricing Model | When to Use | Key Tradeoff |
|---------------|-------------|--------------|
| Flat rate | Simple product, single persona | Easy to sell, leaves money on table |
| Per-seat / per-user | Collaboration / productivity tools | Scales with adoption, penalizes adoption |
| Tiered (Good-Better-Best) | Most SaaS products | Captures different WTP, tier design is hard |
| Usage-based | API, AI, infrastructure | Aligned with value, unpredictable for customers |
| Hybrid (base + usage) | Platform products | Predictable base + value-aligned variable |

| Pricing Psychology Principle | Application |
|------------------------------|-------------|
| Never 2 tiers | People can't choose between 2; add a third (decoy) |
| Decoy effect | A high tier makes the middle tier feel reasonable |
| Annual discount | 15-20% off monthly anchors higher monthly price |
| .99 pricing | $99 feels meaningfully cheaper than $100 |
| Price increase timing | At renewal, grandfather existing 6-12 months |

## Procedure

### 1. Competitive Pricing Audit

For each competitor, map:

| Competitor | Starting Price | Mid-Tier | Enterprise | Pricing Model | Differentiator |
|---|---|---|---|---|---|
| Comp A | $29/seat/mo | $79/seat/mo | Custom | Per-seat | Has feature X |
| Comp B | $49/mo flat | $199/mo | $499/mo | Flat + add-ons | Cheaper at scale |
| Us | TBD | TBD | TBD | TBD | Better UX, faster |

### 2. Willingness-to-Pay Signal Analysis

Gather signals from:
- Sales conversations ("it's too expensive" vs "that seems reasonable")
- Win/loss analysis (did we lose on price?)
- Feature adoption (which features do people upgrade for?)
- Customer segments (do SMB and enterprise value things differently?)

### 3. Tier Design Recommendations

For each tier:
- Which features create the upgrade pull?
- What's the "must-have" that forces the upgrade? (SSO, reporting, API access, seats)
- Are the jumps between tiers too small (nobody upgrades) or too big (churn at renewal)?

### 4. Price Increase Modeling

Model the financial impact:

```
Current state:
  Customers: 200
  Avg ARPU: $500/mo
  Monthly Revenue: $100,000

20% Price Increase (to $600/mo):
  Assume 5% churn from price increase (10 customers)
  Remaining: 190 customers × $600 = $114,000/mo
  Net change: +$14,000/mo (+14% revenue, -5% customer count)
  
  Is the revenue gain worth the customer loss? Almost always yes.
```

**When to raise prices:**
- NPS > 40 (customers are happy)
- Win rate > 30% (you're winning enough)
- Competitors charge more (you're underpriced)
- Product has materially improved since last pricing change

**When NOT to raise prices:**
- Churn is already high
- Major product gaps vs competitors
- Just lost a round of funding (looks desperate)
- During a competitor's launch or price war

### 5. Discounting Framework

| Discount Type | When to Use | Max Discount | Requirements |
|---|---|---|---|
| **Annual prepay** | Always offer | 15-20% | 12-month commitment |
| **Multi-year** | Strategic accounts | 20-30% (year 2-3) | 24-36 month term |
| **Volume / seats** | > 50 seats | 10-20% | Minimum seat commitment |
| **Startup program** | Early stage, logo value | 50%+ for year 1 | Case study, reference, logo |
| **Non-profit / education** | Mission-aligned | 50%+ | Verification |
| **Never discount because they asked**: | Unless there's a strategic reason | — | — |

### Pricing Frameworks

#### Value-Based Pricing (the goal)

```
Price = Value delivered to the customer × Value capture rate

Example: Your tool saves a company $100k/year in engineering time.
  Value capture at 25% = $25k/year price.
```

Not what it costs to build. Not what competitors charge. What it's worth to the customer.

#### SaaS Pricing Models

| Model | When to Use | Pros | Cons |
|---|---|---|---|
| **Flat rate** | Simple product, single persona | Easy to sell, predictable | Leaves money on the table |
| **Per-seat / per-user** | Collaboration / productivity tools | Scales with adoption | Penalizes adoption, seat-capping |
| **Tiered (Good-Better-Best)** | Most SaaS products | Captures different WTP, upgrade path | Tier design is hard |
| **Usage-based** | API, AI, infrastructure products | Aligned with value delivered | Unpredictable for customers |
| **Hybrid** (base + usage) | Platform products | Predictable base + value-aligned variable | Complexity |

#### The Good-Better-Best Framework

| Tier | Target Customer | Price Point | Features | Purpose |
|---|---|---|---|---|
| **Good** (Starter) | Individual / small team | Low | Core features, limited usage | Acquire, prove value |
| **Better** (Growth) | Growing team | 3-5x Good | Core + collaboration + integrations | The anchor — most will buy this |
| **Best** (Enterprise) | Large teams | 2-3x Better | Everything + SSO + SLA + support | Capture high WTP |

## Output Format

- Competitive pricing landscape
- Recommended pricing model and tier structure
- Price increase impact analysis (with churn sensitivity)
- Discount framework and approval guidelines
- Revenue forecast under new pricing (from `revenue-forecasting`)

## Done Criteria

The skill is complete when:
1. Competitive pricing audit is completed for at least 3-5 competitors.
2. Willingness-to-pay signals are analyzed from sales and customer data.
3. Tier structure is recommended with clear upgrade drivers between tiers.
4. Price increase impact is modeled with churn sensitivity.
5. Discounting framework is defined with approval guidelines.
6. A clear recommendation is provided with supporting data.

## Pitfalls

1. **Underpricing by 30-50%** — most startup founders are afraid of pricing. The data consistently shows that startups undercharge significantly. Price pushback from 10-20% of deals is a sign you're in the right range.
2. **Designing pricing in a vacuum** — pricing decisions made without competitor analysis, willingness-to-pay data, or unit economics inputs are guesses. All three data sources are necessary.
3. **Too many tiers** — more than 3-4 tiers paralyze buyers. Good-Better-Best is the proven framework for a reason.
4. **Putting enterprise pricing on the website** — "Contact us" for enterprise. Pricing is part of the negotiation. Putting it on the website gives away leverage.
5. **Never raising prices** — SaaS companies that don't raise prices annually leave 5-15% revenue on the table every year. Annual price increases are standard and expected.

### Heuristics

- **Most startups undercharge by 30-50%**: founders are afraid of pricing. Push them.
- **If you're not losing 10-20% of deals on price, you're too cheap**: price pushback is a sign you're in the right range.
- **Raise prices annually**: 5-15% per year is standard in SaaS. Inflation + more value = justified.
- **Grandfathering is a tactic, not a strategy**: eventually, bring everyone to the new pricing. Sunset old plans.
- **Enterprise pricing should NOT be on your website**: "Contact us" for enterprise. Pricing is part of the negotiation.

### Edge Cases

- **Freemium to paid conversion**: the free tier must be genuinely useful but limited enough to create upgrade urgency. The free-to-paid conversion rate is the critical metric.
- **International pricing**: PPP-adjusted pricing is complex. Typically, price at 60-80% of US for EU, 40-60% for emerging markets.
- **Platform / marketplace pricing**: take-rate pricing (X% of transaction). Model the take-rate sensitivity carefully.
- **Bundling multiple products**: bundling increases stickiness but can mask which products are actually valuable.

## Verification

Can you answer "What is our price relative to the value we deliver?" and "If we raised prices by 20%, how much revenue would we gain vs lose to churn?" and "What feature would force a customer to upgrade from Starter to Growth?" If not, the pricing analysis is incomplete.

## Example

> **User**: "Review our pricing tiers and recommend improvements. We currently have a single flat $49/mo plan with 200 customers."
> **Expected behavior**: You analyze willingness-to-pay signals from customer conversations, run a competitive audit of 5 competitors with similar products, recommend a 3-tier Good-Better-Best structure ($49 Starter / $149 Growth / $399 Enterprise), identify the feature that forces upgrades (SSO and API access for Enterprise), model the financial impact (estimated 30% increase in blended ARPU), and propose a grandfathering plan for existing $49 customers.

> **User**: "Should we raise prices by 25%?"
> **Expected behavior**: You check the preconditions (NPS > 40, win rate > 30%, competitors charge more, product has improved), model the financial impact with churn sensitivity (assume 5-10% churn from price increase, calculate net revenue gain), recommend the timing (at renewal, not mid-contract), and propose a grandfathering period (6 months) for customers on legacy pricing.

## Linked Skills

- Customer lifetime value & willingness to pay → `unit-economics-analysis`
- Profitability impact by segment → `profitability-analysis`
- Revenue forecast with new pricing → `revenue-forecasting`
- Strategic moves (new tier launch) → `strategic-initiative-modeling`
- Business case for pricing change → `business-case-modeling`
