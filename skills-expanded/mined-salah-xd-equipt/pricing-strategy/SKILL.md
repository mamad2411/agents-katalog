---
name: pricing-strategy
description: "Develops pricing strategies with market positioning, perceived value analysis, and price sensitivity testing. Use when setting or revising prices for products or services."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Pricing Strategy

## When to Use This Skill

Use this skill when you need to:
- Set pricing for a new product or service
- Evaluate and adjust existing pricing
- Design tiered or value-based pricing structures
- Analyze competitor pricing and position your offer

**DO NOT** use this skill for creating rate cards (use freelance-rate-card), commission structures, or cost analysis without pricing context. This is for strategic pricing decisions.

---

## Core Principle

PRICE IS A SIGNAL — IT COMMUNICATES VALUE, POSITIONS YOUR BRAND, AND DETERMINES WHO YOUR CUSTOMER IS. NEVER SET PRICES BASED ON COST ALONE.

---

## Phase 1: Pricing Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product/service** | "What are you pricing?" | No default — must be provided |
| **Cost to deliver** | "What does it cost you to deliver this? (COGS, time, materials)" | No default — must be provided |
| **Target customer** | "Who is the ideal buyer? (budget level, sophistication)" | Solopreneurs and small businesses |
| **Competitor prices** | "What do competitors charge for similar offerings?" | Unknown — will research |
| **Current price (if exists)** | "What are you charging now?" | New product — no current price |
| **Revenue model** | "One-time, subscription, retainer, or usage-based?" | One-time purchase |

**GATE: Do not proceed without the product, cost to deliver, and target customer.**

---

## Phase 2: Pricing Analysis

### Cost-Plus Foundation

```
## Cost Analysis

| Component | Cost |
|-----------|------|
| Direct cost (materials, COGS, delivery) | $[X] |
| Time cost (hours x hourly rate) | $[X] |
| Overhead allocation | $[X] |
| **Total cost to deliver** | **$[X]** |

| Markup | Price | Margin |
|--------|-------|--------|
| 2x cost | $[X] | 50% |
| 3x cost | $[X] | 67% |
| 5x cost | $[X] | 80% |
```

### Value-Based Pricing

```
## Value Analysis

| Value Element | Description | Estimated Value to Customer |
|--------------|-------------|---------------------------|
| Time saved | [Hours saved x customer's hourly value] | $[X] |
| Revenue generated | [Expected revenue impact] | $[X] |
| Cost avoided | [Costs eliminated by using product] | $[X] |
| Risk reduced | [Problems prevented] | $[X] |
| **Total value delivered** | | **$[X]** |

**Value-based price range:** 10-20% of total value delivered = $[X] - $[X]
```

### Competitive Positioning

```
## Market Positioning

| Competitor | Price | Positioning |
|-----------|-------|-------------|
| [Comp 1] | $[X] | [Premium / Mid / Budget] |
| [Comp 2] | $[X] | [Premium / Mid / Budget] |
| [Comp 3] | $[X] | [Premium / Mid / Budget] |

**Your positioning options:**
- **Premium (above market):** Requires differentiation, social proof, premium experience
- **Market rate (competitive):** Safe but undifferentiated, compete on features
- **Below market (penetration):** Gains volume fast but hard to raise later, signals lower quality
```

---

## Phase 3: Pricing Structure

### Recommended Pricing Model

Choose and present the right structure:

**Single Price:**
Best for: Simple products, clear value, low consideration purchases

**Tiered Pricing (Good/Better/Best):**
```
| Tier | Price | Includes | Target Buyer |
|------|-------|----------|-------------|
| [Basic] | $[X] | [Core features] | Price-sensitive buyers |
| [Pro] | $[X] | [Core + advanced] | Most buyers (anchor here) |
| [Premium] | $[X] | [Everything + extras] | Power users, enterprises |
```
Best for: SaaS, courses, service packages

**Subscription:**
Monthly vs. annual pricing with discount for annual commitment (typically 15-20% off monthly)

**Pay-per-result:**
Price tied to outcomes delivered — highest value capture, highest risk

### Price Anchoring

- Present the highest tier first to anchor perception
- The middle tier should be the target — most customers choose it
- Include a decoy tier if needed to make the target tier look like the best value

---

## Phase 4: Testing Plan

### Price Sensitivity Testing

```
## Price Testing Plan

### A/B Test Structure
- Test 2-3 price points simultaneously
- Minimum 100 visitors per variant for significance
- Measure: Conversion rate, revenue per visitor, total revenue

### Price Points to Test
| Variant | Price | Hypothesis |
|---------|-------|-----------|
| A (current/low) | $[X] | Higher conversion, lower revenue per sale |
| B (target) | $[X] | Balanced conversion and revenue |
| C (premium) | $[X] | Lower conversion, higher revenue per sale |

### Signals to Watch
- Conversion rate drops >30% at higher price = price too high
- No conversion change at higher price = room to increase
- High refund rate at any price = value delivery problem, not pricing
```

---

## Example: Online Course Pricing

**Cost:** $2,000 to create, $5/sale in delivery costs.
**Value:** Students save 10 hours/week (worth $500/week at $50/hour).
**Competitors:** $97-$497 range.

**Recommendation:** $197 single tier or $97/$197/$497 three-tier. Middle tier ($197) includes course + templates. Premium ($497) adds coaching calls. Price captures ~2% of monthly value delivered.

---

## Anti-Patterns

- **Cost-plus only pricing** — your costs are irrelevant to the buyer. Price on value delivered, not cost incurred.
- **Copying competitor prices** — your differentiation should justify different pricing. Copy the model, not the number.
- **Pricing too low out of fear** — low prices attract price-sensitive buyers who churn fastest and complain most
- **Too many tiers** — 3 tiers maximum. More creates decision paralysis.
- **Never testing** — set a price, test it, adjust. Pricing is iterative, not permanent.

---

## Recovery

- **No competitor data:** Price based on value analysis. Use the 10-20% of value delivered rule as a starting point.
- **Commodity product (no differentiation):** Compete on experience, bundling, or guarantees — not price. Or find a niche where you can differentiate.
- **Price increase needed on existing product:** Grandfather existing customers, raise for new customers. Communicate added value with the increase.
- **Customers say it is too expensive:** This is normal — 20-30% of prospects should find you too expensive. If nobody does, you are priced too low.
