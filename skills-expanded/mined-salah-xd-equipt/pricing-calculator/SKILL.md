---
name: pricing-calculator
description: "Builds pricing models, comparison tables, and rate calculators for services, products, and subscriptions with profit margin analysis and competitive positioning. Use when a user needs to set prices for their offerings, wants to create tiered pricing, or needs to calculate freelance rates, project fees, or subscription pricing."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Pricing Calculator

## When to Use This Skill

Use this skill when:
- A user needs to set prices for a service, product, or subscription
- A freelancer wants to calculate their hourly, project, or retainer rate
- A user is building tiered pricing packages (Good / Better / Best)
- Someone needs a profit margin analysis on their current or planned pricing
- A SaaS founder needs to structure subscription tiers with feature matrices
- A user says "how much should I charge" or "help me price this"

**DO NOT** use this skill for:
- Writing proposals or invoices (use proposal or invoice skills)
- Financial forecasting or P&L modeling (this calculates prices, not business plans)
- Investment or tax advice (consult a financial professional)

---

## Quick Reference: Capabilities

| Feature | Details |
|---------|---------|
| Pricing models | 6 (Hourly, Project, Retainer, Tiered Packages, Value-Based, Subscription) |
| Psychology tactics | 5 (Charm, Anchoring, Decoy, Bundle, Price-to-Value Framing) |
| Margin analysis | Cost-plus, target margin, and break-even formulas |
| Tier framework | 3-tier system with tested multipliers (1x, 2x, 3.5x) |
| Output format | Markdown pricing document saved as `.md` file |

## Quick Reference: Pricing Models

| Model | Formula | Best For | Pros | Cons |
|-------|---------|----------|------|------|
| **Hourly** | (Income + expenses + taxes + profit) / billable hours | New freelancers, consulting | Simple to explain | Punishes efficiency |
| **Project-Based** | (Hours x rate) + complexity buffer (15-25%) | Defined deliverables | Predictable, rewards speed | Scope creep risk |
| **Retainer** | Monthly deliverables x unit rate | Ongoing services | Predictable income | Scope ambiguity |
| **Tiered Packages** | 3 tiers at 1x / 2x / 3.5x | Variable scope, agencies | Clients self-select | Decision fatigue if 4+ |
| **Value-Based** | % of client's expected ROI (10-20%) | High-impact consulting | Highest earning potential | Hard to prove upfront |
| **Subscription** | MRR target with CAC payback + LTV math | SaaS, memberships | Recurring revenue | Churn risk |

**DEFAULT: Tiered Packages** -- most versatile for solopreneurs. When in doubt, build three tiers.

## Quick Reference: Pricing Psychology

| Tactic | How It Works | Example |
|--------|-------------|---------|
| **Charm Pricing** | Prices ending in 7 or 9 feel lower | $997 instead of $1,000 |
| **Anchoring** | Show premium first so others feel affordable | Lead with $7,500, then $4,500, then $2,500 |
| **Decoy Effect** | Middle tier looks best when low-to-mid gap is small, mid-to-high is large | $500 / $997 / $2,500 nudges to $997 |
| **Bundle Discount** | Combined discount vs. buying separately | $4,500 worth of services bundled at $3,497 |
| **Price-to-Value Framing** | Reframe as fraction of value delivered | "$2,500/mo = $125/business day" |

## Quick Reference: Margin Formulas

| Calculation | Formula | Example |
|-------------|---------|---------|
| **Cost-Plus Markup** | Price = Cost x (1 + Markup %) | $50 x 1.60 = $80 (60% markup) |
| **Target Margin** | Price = Cost / (1 - Margin %) | $50 / (1 - 0.40) = $83.33 (40% margin) |
| **Gross Margin** | (Price - Cost) / Price x 100 | ($83.33 - $50) / $83.33 = 40% |
| **Break-Even** | Fixed Costs / (Price - Variable Cost) | $10,000 / ($80 - $50) = 334 units |
| **Effective Hourly** | Project Price / Actual Hours | $5,000 / 32 hrs = $156.25/hr |

**CRITICAL: Markup and margin are NOT the same.** 50% markup on $100 = $150 (33% margin). 50% margin on $100 cost = $200 (100% markup). Always clarify which one the user means.

---

## Core Workflow

EVERY PRICING CALCULATION STARTS WITH THE USER'S COSTS AND INCOME GOALS -- NEVER SET A PRICE WITHOUT UNDERSTANDING WHAT IT NEEDS TO COVER.

### Step 1: Gather Inputs

**For freelancers/services:** (1) What do you offer? (2) Monthly fixed costs? (3) Annual income goal? (4) Hours per week available? (5) Billable ratio? (Default: 60% solo, 70% with systems) (6) Competitor pricing range? (7) Target client?

**For products/SaaS:** (1) What is the product? (2) Cost per unit/user? (3) Monthly fixed costs? (4) Target MRR or annual revenue? (5) Competitor pricing? (6) CAC? (7) Target customer?

If the user provides items 1-3, proceed with defaults for the rest and flag them.

**Brief prompt for vague requests:**
```
I will build your pricing model. Quick details needed:
1. What do you sell? (Service, product, subscription)
2. What are your monthly costs to run the business?
3. What annual income do you want to take home?
4. What do competitors charge? (Even a rough range helps)
5. Who is your ideal customer?
```

### Step 2: Calculate

Run the appropriate model. **Show all math transparently** so the user can verify and recalculate.

**Freelance hourly:** Annual income + expenses + tax reserve (30%) + profit buffer (10%) = total revenue needed. Divide by (hours/week x billable ratio x 48 working weeks) = minimum hourly rate.

**Project-based:** Estimated hours x hourly rate + complexity buffer (15-25%) = project rate.

**Tiered packages:** Base tier at 1x, mid at 2x, top at 3-3.5x. Apply charm pricing to at least the target tier.

**Subscription:** Calculate minimum price from margin target (cost / (1 - margin%)). Calculate CAC payback (CAC / price = months). Calculate LTV (price / monthly churn rate). Verify LTV:CAC ratio is at least 3:1. Set annual discount at 2 months free (16.7% off).

**Product cost-plus:** COGS + fulfillment = unit cost. Price = unit cost / (1 - target margin%). Apply charm pricing.

**Value-based:** Client's expected ROI x capture rate (10-20%). Sanity check: should be 1.5x-5x over cost-based calculation.

**GATE: Present all calculations to the user before building the pricing document.** Ask: "Does this math match your expectations? Any costs I should adjust?"

### Step 3: Present the Pricing Document

Build a document with these sections: (1) Pricing Summary with tier names and prices, (2) What Is Included (comparison table), (3) Profit Margin Analysis, (4) Competitive Positioning (budget / mid-market / premium), (5) Psychology Applied, (6) Formulas for Recalculation.

**Always mark one tier as "MOST POPULAR" or "Recommended."** Default to the middle tier.

**GATE: Present the complete pricing document for review before saving.**

### Step 4: Deliver

1. Save as `pricing-[offering-name].md` in the working directory (or user-specified path)
2. Confirm: "Your pricing model has been saved to [path]. It includes [X] tiers, [margin%] average margin, and recalculation formulas."
3. Offer: "Would you like a client-facing pricing page or a proposal using these rates?"

---

## Example 1: Freelance Web Designer -- Rate + 3-Tier Packages

**User says:** "I am a freelance web designer. I want to make $120K/year. Expenses are $3,500/month. I work 35 hours/week. Competitors charge $100-$200/hour. Clients are small to mid-size businesses."

**Step 2 calculation:**
```
Revenue needed: $120,000 + $42,000 expenses + $48,600 tax (30%) + $21,060 profit (10%) = $231,660
Billable hours: 35 hrs/wk x 60% x 48 weeks = 1,008 hrs/yr
Minimum rate: $231,660 / 1,008 = $229.82 -> $230/hr (above competitor range)
Recommended: increase billable ratio to 70% -> 1,176 hrs -> $196.99 -> $200/hr
```

**Tiered packages** (typical website = 20-40 hours at $200/hr):

| Tier | Scope | Hours | Calculation | Price |
|------|-------|-------|-------------|-------|
| Starter | 5-page site, standard design | 20 | $4,000 + 15% buffer | $4,597 |
| Professional (MOST POPULAR) | 8-page + SEO + content strategy | 32 | $6,400 + 20% buffer | $7,997 |
| Premium | 12-page + SEO + branding + 60-day support | 48 | $9,600 + 25% buffer + VIP | $15,997 |

**Package comparison table:**

| Feature | Starter ($4,597) | Professional ($7,997) | Premium ($15,997) |
|---------|:-:|:-:|:-:|
| Custom pages | 5 | 8 | 12 |
| Responsive design | Yes | Yes | Yes |
| SEO setup | -- | Yes | Yes |
| Content strategy | -- | Yes | Yes |
| Brand identity refresh | -- | -- | Yes |
| Revision rounds | 1 | 2 | 3 |
| Post-launch support | 7 days | 30 days | 60 days |
| **Best for** | Startups, MVPs | **Most small businesses** | Established brands |

**Delivered:** Saved to `pricing-web-design.md` with 82-88% margins, recalculation formulas, and competitive positioning (mid-to-premium).

---

## Example 2: SaaS Founder -- Subscription Pricing

**User says:** "I built a project management tool for freelancers. $2.80/user/month hosting. $8K/month fixed costs. Want $50K MRR. CAC is ~$120. Competitors: $10-$15 basic, $30-$50 pro."

**Step 2 calculation:**
```
Margin floor: $2.80 / (1 - 0.80) = $14/mo minimum at 80% margin
CAC payback: $120 / 4 months = $30/mo target
LTV at 7% churn: $15/0.07=$214 (1.8:1), $29/0.07=$414 (3.5:1), $79/0.07=$1,129 (9.4:1)
Blended ARPU (40/45/15 mix): $30.90 -> 1,618 users to hit $50K MRR
Break-even: $8,000 / ($30.90 - $2.80) = 285 paying users
```

**Pricing tiers:**

| Tier | Monthly | Annual (2mo free) | Margin | LTV:CAC |
|------|---------|-------------------|--------|---------|
| Starter | $15/mo | $150/yr | 81.3% | 1.8:1 |
| Pro (MOST POPULAR) | $29/mo | $290/yr | 90.3% | 3.5:1 |
| Business | $79/mo | $790/yr | 96.5% | 9.4:1 |

**Feature matrix:**

| Feature | Starter ($15/mo) | Pro ($29/mo) | Business ($79/mo) |
|---------|:-:|:-:|:-:|
| Active projects | 5 | 25 | Unlimited |
| Time tracking | Basic | Advanced | Advanced |
| Client portal | -- | Yes | Yes |
| Invoicing integration | -- | Yes | Yes |
| File storage | 1 GB | 10 GB | 50 GB |
| API access | -- | -- | Yes |
| Support | Email | Priority | Dedicated rep |
| **Best for** | Side hustlers | **Full-time freelancers** | Agencies |

**Delivered:** Saved to `pricing-project-management-saas.md` with LTV:CAC analysis and break-even at 285 users.

---

## Pricing Tier Framework

| Tier | Multiplier | Purpose | Psychology |
|------|-----------|---------|------------|
| **Starter / Basic** | 1x | Low barrier, attracts price-sensitive buyers | Makes middle tier look like a better deal |
| **Professional / Growth** | 2x | The tier you want most clients to choose | Labeled "MOST POPULAR" -- social proof nudge |
| **Premium / Scale** | 3-3.5x | Captures high-willingness-to-pay clients | Anchors middle tier as reasonable |

**CRITICAL: The Professional tier must be the obvious best value.** Starter-to-Professional gap should feel small. Professional-to-Premium gap should feel large. This is the decoy effect.

---

## Anti-Patterns

- **DO NOT set prices based solely on competitor pricing.** Start from your own costs and income goals. Competitors are a reference, not a formula.
- **DO NOT create more than 4 pricing tiers.** Three is ideal. More causes decision paralysis.
- **DO NOT hide the recommended tier.** Always label one tier "MOST POPULAR." Without a nudge, clients default to cheapest.
- **DO NOT price below cost without a documented strategy.** Loss-leader pricing requires a clear upsell path and time limit.
- **DO NOT use round numbers for everything.** Charm pricing ($4,997 vs $5,000) increases conversions. Exception: ultra-premium brands.
- **DO NOT present pricing without showing what is included.** Prices without context trigger sticker shock.
- **DO NOT confuse markup with margin.** 50% markup on $100 = $150. 50% margin on $100 = $200. Clarify which the user means.
- **DO NOT skip the profit buffer.** Always include 10-15% on top of income goals.
- **DO NOT ignore market position.** New freelancers cannot charge agency rates without a portfolio. Veterans should not undercharge.
- **DO NOT set subscription prices without LTV and CAC analysis.** $10/mo sounds good until CAC is $200 and churn is 10%.

---

## Recovery and Troubleshooting

### User Does Not Know Their Costs
1. Walk through typical freelancer costs ($350-$2,300/mo range: software $100-$500, insurance $100-$300, marketing $0-$500, education $50-$200, equipment $100-$300, workspace $0-$500)
2. Use midpoint ($1,325/mo) as default, flag it clearly
3. Include formula so they can recalculate with real numbers later

### User Is Severely Underpricing
1. Show the math: "At $50/hr with your expenses, you net $18/hr after taxes -- below minimum wage"
2. Show what the rate should be based on their goals
3. Suggest a transition plan: raise new client rates immediately, give existing clients 30-day notice, full rate within 3-5 months
4. **Flag it clearly but respect the user's final decision**

### Competitor Data Unavailable
1. Use industry benchmarks: design $75-$250/hr, dev $100-$300/hr, marketing $100-$350/hr, coaching $150-$500/hr, writing $50-$200/hr, SaaS B2B $15-$500/mo, SaaS B2C $5-$50/mo
2. Flag as industry-wide ranges, recommend surveying 3-5 peers
3. Proceed with midpoint of relevant range

### Multiple Services to Price
1. Price each service independently using the same base rate
2. Build bundle packages at 10-20% off individual pricing
3. Keep to 3 tiers maximum per service -- never 3 services x 3 tiers = 9 options

### User Rejects Pricing After 3 Attempts
1. Diagnose: "Is the total too high, or is the value not clear enough?"
2. If too high: reduce scope, not margin. Remove lowest-value deliverable.
3. If value unclear: reframe with price-to-value language
4. If disagreement persists: deliver with margin warning and suggest revisiting after first quarter

### File Write Fails
1. Report error, present pricing document as formatted text in chat
2. Offer different file path. **If 3 attempts fail, stop and present in chat.**

---

## Pre-Delivery Checklist

**DO NOT SKIP ANY ITEM.**

| Check | What to Verify |
|-------|----------------|
| Math correct | Every formula produces the stated result; margins match; totals add up |
| Costs accounted for | Fixed costs, variable costs, taxes, and profit buffer all included |
| Income goal achievable | Pricing generates enough revenue to hit stated goal |
| Tiers logical | Each tier adds clear value; no overlap confusion |
| Recommended tier marked | One tier labeled "MOST POPULAR" or "Recommended" |
| Psychology applied | At least one tactic used and documented |
| Competitive position stated | User knows if budget, mid-market, or premium |
| Formulas included | User can recalculate when costs change |
| No placeholder text | Every number is real; no `[TBD]` remains |
| Margin above 30% | If below, flag explicitly with recommendation |
| File saved | Write tool confirmed successful |
| Next steps offered | User knows what to do next (sales page, proposal, etc.) |
