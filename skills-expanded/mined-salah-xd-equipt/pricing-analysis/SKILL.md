---
name: pricing-analysis
description: "Analyzes pricing effectiveness with elasticity estimates, competitor benchmarking, value perception, and optimization recommendations. Use when evaluating or adjusting your pricing."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Pricing Analysis

## When to Use This Skill

Use this skill when you need to:
- Evaluate whether your current pricing is optimal
- Benchmark your prices against competitors
- Analyze the impact of a price change before implementing it
- Design a pricing structure (tiers, bundles, freemium)

**DO NOT** use this skill for financial modeling, revenue forecasting, or cost accounting. This is for pricing strategy analysis and optimization.

---

## Core Principle

PRICE BASED ON VALUE DELIVERED, NOT COST INCURRED — YOUR PRICE SHOULD REFLECT WHAT THE CUSTOMER GAINS, NOT WHAT IT COSTS YOU TO DELIVER.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product/service** | "What are you pricing?" | Must be provided |
| **Current price** | "What do you charge now?" | Must be provided |
| **Pricing model** | "One-time, subscription, per-unit, tiered, usage-based?" | Must be provided |
| **Competitors** | "Who are your top 3 competitors and what do they charge?" | Will research |
| **Customer feedback** | "Have customers commented on price? (too high, fair, would pay more)" | No direct feedback |
| **Goal** | "What are you optimizing for? (revenue, volume, market share, margin)" | Revenue maximization |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Analyze

### Analysis Framework

1. **Competitive positioning** — where you sit relative to competitors (premium, mid-market, budget)
2. **Value metric alignment** — does your pricing scale with the value customers receive?
3. **Price sensitivity indicators** — signals from conversion rates, objections, or win/loss data
4. **Willingness to pay estimation** — Van Westendorp or comparable framework
5. **Margin analysis** — gross margin at current price and at proposed alternatives

### Competitive Benchmark Table

| Competitor | Price | Model | Key Differentiator |
|-----------|-------|-------|-------------------|
| Competitor A | $X/mo | Subscription | Feature X |
| Competitor B | $Y one-time | Lifetime | Community access |
| You | $Z/mo | Subscription | Your differentiator |

**GATE: Present analysis findings and wait for direction before making recommendations.**

---

## Phase 3: Build

### Deliverables

**1. Pricing Analysis Report**
- Competitive benchmark with positioning map
- Current pricing strengths and weaknesses
- Price sensitivity assessment
- Revenue impact estimates for proposed changes

**2. Pricing Recommendations**
- 2-3 pricing options with projected outcomes
- Tier structure recommendations (if applicable)
- Bundling or packaging suggestions
- Implementation approach (grandfather existing, phase in, immediate)

**3. Price Change Impact Model**
- Scenario table: price x estimated volume = projected revenue
- Conservative, base, and optimistic scenarios
- Break-even analysis: how many customers can you lose before the increase hurts?

**4. Communication Plan**
- How to announce price changes to existing customers
- Messaging framework that leads with value, not cost
- Grandfather policy recommendations
- FAQ for customer-facing team

---

## Phase 4: Polish

### Testing Recommendations

- A/B test pricing page if traffic allows
- Offer the new price to new customers first, keep existing customers on current plan
- Survey 10 customers with "Would you pay $X for this?" before committing

### Review Cadence

Reassess pricing every 6-12 months as value delivered, costs, and competitive landscape change.

---

## Example 1: SaaS Product ($29/month, considering increase)

**Finding:** Competitors charge $39-$79/month for similar features. Current price signals "basic tool" not "premium solution."
**Recommendation:** Increase to $49/month for new customers, grandfather existing at $29 for 12 months. Expected: 10% volume decrease, 55% revenue increase.

## Example 2: Digital Product ($97 one-time, considering tiers)

**Finding:** Single price forces budget-conscious and premium buyers into the same option.
**Recommendation:** Three tiers — Basic ($67), Standard ($127), Premium ($247) — with clear feature differentiation. Expected 30% revenue increase from upsell capture.

---

## Anti-Patterns

- **Cost-plus pricing** — adding a margin to your costs ignores what customers value. A course that costs $50 to produce may be worth $500 to the buyer.
- **Competitor matching** — pricing at the same level without differentiation is a race to the bottom. Price reflects positioning.
- **Fear of raising prices** — most businesses underprice. If nobody complains about your price, it is probably too low.
- **One price for everyone** — different segments have different willingness to pay. Tiers or packages capture more value.
- **Changing price without communicating value** — a price increase without reinforced value feels like a cash grab. Always lead with value.

---

## Recovery

- **No competitor data:** Use industry benchmarks, comparable products in adjacent categories, or customer willingness-to-pay surveys.
- **User afraid to raise prices:** Start with new customers only. Grandfather existing customers to reduce risk. Test small increases first.
- **Customers already say price is too high:** Investigate whether it is a price problem or a value communication problem. Often the landing page is the issue, not the price.
- **Pricing is genuinely complex:** Simplify first. If you cannot explain your pricing in 10 seconds, customers cannot evaluate it.
