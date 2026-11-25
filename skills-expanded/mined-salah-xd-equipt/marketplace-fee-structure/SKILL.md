---
name: marketplace-fee-structure
description: "Designs marketplace fee structures with commission models, premium tiers, and competitive analysis. Use when setting or restructuring pricing for a platform business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Marketplace Fee Structure

## When to Use This Skill

Use this skill when you need to:
- Design a fee structure for a two-sided marketplace
- Evaluate commission models, listing fees, and subscription tiers
- Analyze competitor pricing to find the right market position
- Create premium seller tiers with clear value propositions

**DO NOT** use this skill for SaaS pricing, e-commerce product pricing, or financial modeling. This is for marketplace platform fee design.

---

## Core Principle

MARKETPLACE FEES MUST BE LOW ENOUGH THAT SELLERS STAY ON THE PLATFORM AND HIGH ENOUGH TO BUILD A SUSTAINABLE BUSINESS — THE FEE SHOULD NEVER EXCEED THE VALUE THE PLATFORM CREATES.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Marketplace type** | "What does your marketplace connect?" | No default — must be provided |
| **Average transaction value** | "What is the typical transaction amount?" | No default — must be provided |
| **Transaction volume** | "How many transactions per month (current or projected)?" | 100/month projected |
| **Competitors** | "Who are your top 3 competitors and what do they charge?" | No default — research needed |
| **Current fees** | "What do you charge now, if anything?" | Nothing (pre-revenue) |
| **Value provided** | "What does the platform do for sellers beyond connecting them to buyers?" | Payments, discovery, trust |

**GATE: Confirm the brief before designing the fee model.**

---

## Phase 2: Fee Model Options

### Common Marketplace Fee Models

| Model | How It Works | Best For |
|-------|-------------|----------|
| **Commission** | % of each transaction | High-volume, variable-price marketplaces |
| **Listing fee** | Fixed fee per listing | Product marketplaces with many listings |
| **Subscription** | Monthly fee for seller access | Professional service marketplaces |
| **Freemium** | Free basic + paid premium features | Marketplaces building supply quickly |
| **Lead fee** | Fee per qualified lead or inquiry | Service marketplaces with high-value transactions |
| **Hybrid** | Combination of above | Mature marketplaces with diverse revenue needs |

### Commission Rate Guidelines

| Transaction Value | Typical Commission | Rationale |
|-------------------|-------------------|-----------|
| Under $50 | 15-25% | Higher rate needed for unit economics |
| $50-500 | 10-20% | Standard range for most marketplaces |
| $500-5,000 | 5-15% | Lower rate to keep high-value sellers |
| Over $5,000 | 3-10% | Volume-based, sellers are price-sensitive |

### Who Pays the Fee

| Option | Pros | Cons |
|--------|------|------|
| Seller pays | Simple, common, hidden from buyer | Sellers build fee into price |
| Buyer pays (service fee) | Seller gets full price, transparent | Buyer sticker shock |
| Split | Fair perception | Complex to communicate |

**GATE: Confirm the fee model and rate range before building the structure.**

---

## Phase 3: Build the Fee Structure

### Base Fee Design

Document the core fee structure:
- **Who is charged:** Buyer, seller, or both
- **When charged:** At booking, at completion, or monthly
- **Rate:** Fixed amount, percentage, or tiered
- **Minimum fee:** Floor amount per transaction (if applicable)
- **Payment processing:** Who absorbs the 2.9% + $0.30 processing cost

### Premium Seller Tiers

Design 2-3 tiers for sellers:

```
## Seller Tiers

### Basic (Free)
- Standard listing placement
- [X]% commission per transaction
- Basic analytics
- Standard support

### Professional ($29/month or reduced commission)
- Priority listing placement
- [X-3]% commission per transaction
- Advanced analytics and conversion tracking
- Featured in buyer emails
- Priority support

### Enterprise (Custom)
- Custom commission rates
- Dedicated account manager
- API access
- Custom branding options
- Volume discounts
```

### Competitive Analysis Template

| Competitor | Commission | Listing Fee | Subscription | Other Fees |
|-----------|-----------|-------------|-------------|-----------|
| [Competitor 1] | | | | |
| [Competitor 2] | | | | |
| [Competitor 3] | | | | |
| **Your Platform** | | | | |

**Positioning strategy:** Price below the market leader but above the cheapest option. Compete on value, not price.

---

## Phase 4: Polish

### 1. Fee Communication

Write clear fee explanations for:

**Seller-facing:**
"You keep [X]% of every transaction. We charge a [Y]% platform fee that covers payment processing, buyer acquisition, dispute resolution, and platform maintenance. No hidden fees, no surprises."

**Buyer-facing (if applicable):**
"A small service fee of [X]% is added to your order. This covers secure payments, buyer protection, and customer support."

**FAQ entries:**
- When are fees charged?
- How are fees calculated on discounted or refunded transactions?
- Are there any additional fees beyond the commission?
- How do I upgrade to a premium tier?

### 2. Fee Revenue Projections

Provide a simple projection template:
```
Monthly Transactions: [X]
Average Transaction Value: $[Y]
Commission Rate: [Z]%
Gross Revenue: X * Y * Z

Minus: Payment processing (~2.9% + $0.30 per transaction)
Minus: Refunds and disputes (~2-5% of gross)
Net Platform Revenue: [Result]
```

### 3. Quality Checklist

```
## Fee Structure Checklist

- [ ] Fee model selected with rationale
- [ ] Commission rate benchmarked against 3+ competitors
- [ ] Who pays (buyer, seller, or split) is decided and justified
- [ ] Premium seller tiers defined with clear value at each level
- [ ] Minimum transaction fee set (if applicable)
- [ ] Payment processing costs accounted for
- [ ] Fee communication copy written for both sellers and buyers
- [ ] FAQ covers fee calculation, timing, refunds, and upgrades
- [ ] Revenue projection model created
- [ ] Fee is sustainable (covers costs + margin) at projected volume
```

---

## Example

**Marketplace:** Freelance design services
**Average transaction:** $750

**Fee structure:**
- 12% commission on seller (seller receives $660)
- 5% service fee on buyer (buyer pays $787.50)
- Total platform revenue per transaction: $127.50
- Payment processing absorbed by platform

**Premium tier pitch:**
"Go Pro for $49/month: Drop your commission from 12% to 8%. On your average $750 project, that saves you $30 per transaction. If you complete 2+ projects per month, Pro pays for itself."

---

## Anti-Patterns

- **Hidden fees** — surprising sellers with fees they did not expect kills trust and generates chargebacks. Be transparent.
- **Charging before value is delivered** — listing fees before any sales discourages supply. Commission-based models align incentives.
- **Race to zero** — competing solely on lower fees attracts price-sensitive sellers who leave when a cheaper option appears.
- **Overcomplicating tiers** — more than 3 tiers creates confusion. Keep it simple.
- **Ignoring payment processing costs** — 2.9% + $0.30 per transaction adds up. Account for it in your revenue model.

---

## Recovery

- **Sellers resist the fee:** Demonstrate the value — what does the platform provide that justifies the cost? If you cannot articulate it, the fee is too high.
- **Buyers resist service fees:** Test absorbing the fee into the seller's commission. Hidden fees feel worse than slightly higher prices.
- **Revenue is not covering costs:** Either increase volume (more transactions) or increase take rate (higher fee). Raising fees on existing sellers requires advance notice and justification.
- **Competitor undercuts on price:** Compete on value, not price. Better sellers, more buyers, superior trust features justify a premium.
