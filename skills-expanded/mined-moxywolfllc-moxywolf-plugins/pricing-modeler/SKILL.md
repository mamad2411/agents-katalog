---
name: pricing-modeler
description: >
  This skill should be used when the user says "build my pricing model",
  "design pricing tiers", "set my price points", "create a tier structure",
  "what should I charge", "model my pricing", "pricing spreadsheet",
  "revenue model", "value metric selection", "feature gating strategy",
  "freemium vs paid model", "usage-based pricing model", "API pricing tiers",
  "calculate price points", "pricing sensitivity analysis", or any request
  to translate pricing research into concrete tier definitions, price points,
  and revenue projections. This skill takes the output of pricing-research
  and turns it into an implementable pricing architecture. Use this whenever
  someone has research and needs to make actual pricing decisions — this is
  where strategy becomes numbers.
version: 0.1.0
---

# Pricing Modeler

Transform pricing research into implementable pricing architecture — tiers, price points, value metrics, feature gates, and revenue projections.

## Prerequisites

This skill works best when fed by pricing-research output. If no research package exists, prompt the user to run pricing-research first — or work with whatever competitive intelligence they can provide.

## Modeling Workflow

### Step 1: Select the Value Metric

The value metric is what you charge per. It's the single most important pricing decision because it determines how revenue scales with customer value.

#### Value Metric Evaluation Framework

For each candidate metric, score on these dimensions:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Value alignment** | 30% | Does it scale with the value the customer receives? |
| **Predictability** | 20% | Can customers predict their monthly bill? |
| **Measurability** | 15% | Can you accurately track and report it? |
| **Growth incentive** | 15% | Does it encourage product adoption (not punish it)? |
| **Competitive fit** | 10% | How does it compare to what competitors charge per? |
| **Simplicity** | 10% | Can you explain it in one sentence? |

#### Common SaaS Value Metrics

| Metric | Best For | Caution |
|--------|----------|---------|
| Per seat | Team collaboration tools | Discourages broad adoption |
| Per asset/item | Content management, security scanning | Scales with portfolio size |
| Per API call | Developer tools, data APIs | Unpredictable bills scare users |
| Per scan/check | Compliance, security tools | Aligns with compliance cycles |
| Flat rate | Simple tools, SMB focus | Doesn't capture enterprise value |
| Per organization | Platform tools, multi-team | Misses expansion revenue |
| Data volume | Storage, analytics, ETL | Technical metric, less intuitive |

#### STIGViewer-Specific Value Metrics

Consider these for STIGViewer SaaS:
- **Per STIG profile managed** — scales with compliance scope
- **Per system/asset under compliance** — maps to the thing customers actually care about
- **Per user/seat** — simple but may limit adoption in large orgs
- **Per organization** — easy but misses size variation
- **Hybrid: seat + asset volume** — captures both adoption and scope

For the API gateway:
- **Per API call** — standard, well-understood
- **Per content item served** — ties to content value
- **Per automated compliance check** — ties to compliance outcomes
- **Credit-based** — flexible for varied operation types

Read `references/value-metric-decision-tree.md` for a guided decision flow.

### Step 2: Design the Tier Architecture

#### The 3-Tier Standard

Most B2B SaaS succeeds with 3 published tiers + enterprise:

**Free / Community**
- Purpose: Top-of-funnel acquisition, product-led growth
- Design principle: Generous enough to be useful, limited enough to create natural upgrade pressure
- Key limits: Usage caps, feature restrictions, no team features, community support only
- Success metric: Free-to-paid conversion rate (target 2-5% for PLG)

**Starter / Team**
- Purpose: Convert individuals and small teams to paying customers
- Design principle: Remove the specific friction that makes the free tier insufficient for professional use
- Price anchor: Should feel like "obvious value" — well below the value delivered
- Success metric: Net revenue retention, expansion rate

**Pro / Business**
- Purpose: Capture the core ICP at the price that maximizes revenue
- Design principle: Complete solution for the primary use case; this is where most revenue comes from
- Price anchor: The "recommended" tier — highlight visually, make it the default
- Success metric: Revenue per account, gross margin

**Enterprise**
- Purpose: Capture large organizations with complex needs
- Design principle: Custom pricing, white-glove onboarding, compliance features, SLAs
- Key features: SSO/SAML, audit logs, dedicated support, custom integrations, data residency
- Price anchor: "Contact us" — enables value-based negotiation
- Success metric: ACV, logo acquisition, net revenue retention

#### The Feature Gate Strategy

Decide what goes in each tier using this hierarchy:

1. **Table stakes** (all tiers including free): Core features that define the product category. Without these, it's not even the product.
2. **Differentiators** (paid tiers): Features that make your product better than alternatives. These justify the price.
3. **Multipliers** (higher tiers): Features that increase value at scale — team features, automation, integrations.
4. **Enterprise gates** (enterprise only): Security, compliance, admin controls. These exist because enterprise buyers require them AND will pay a premium.

Read `references/feature-gating-matrix.md` for a structured decision template.

### Step 3: Set Price Points

#### Price Point Selection Process

1. **Start with the research range**: Use the acceptable price range from Van Westendorp or competitor benchmarks
2. **Apply value-based anchoring**: Calculate 10-30% of the quantified value delivered
3. **Check psychological pricing**: Use .99 or round numbers depending on brand positioning
   - Round numbers ($50, $100) signal quality and simplicity
   - Precise numbers ($49, $97) signal optimization and deals
4. **Apply tier spacing**: Each tier should be 2-3x the previous (not 1.5x, not 5x)
5. **Test the "10x value" rule**: At each price point, can you articulate 10x the value?

#### Pricing Math Template

```
Product: [Name]
Value Metric: [per X]

| Component | Free | Starter | Pro | Enterprise |
|-----------|------|---------|-----|------------|
| Monthly Price | $0 | $__/mo | $__/mo | Custom |
| Annual Price | $0 | $__/yr | $__/yr | Custom |
| Annual Discount | — | __% | __% | Negotiated |
| [Value Metric] Limit | __ | __ | __ | Unlimited |
| Seats Included | 1 | __ | __ | Unlimited |
| Overage Rate | N/A | $__/unit | $__/unit | Negotiated |
```

#### Revenue Projection Model

For each tier, model:
- **Expected customer count** (month 1, 6, 12, 24)
- **Average revenue per account**
- **Conversion rates** (free→starter, starter→pro, pro→enterprise)
- **Churn rate by tier**
- **Net revenue retention** (including expansion)
- **Monthly recurring revenue (MRR)** trajectory
- **Annual recurring revenue (ARR)** projection

### Step 4: API Gateway Pricing Model

If the product includes an API, model it separately or as an add-on:

#### Standalone API Pricing
- Define request tiers with volume discounts
- Set rate limits per tier
- Design overage pricing (per-request or hard cap)
- Model burst pricing vs. sustained usage

#### API as SaaS Feature
- Include base API access at each SaaS tier
- Set per-tier API call limits
- Design overage handling (upgrade prompt vs. per-call billing)
- Consider separate API-only plans for developer segment

Read `references/api-revenue-model.md` for API-specific revenue modeling templates.

### Step 5: Sensitivity Analysis

Test the model against scenarios:

1. **Price increase +20%**: What happens to conversion? Revenue?
2. **Price decrease -20%**: Volume increase needed to maintain revenue?
3. **Competitor undercuts by 30%**: Is value differentiation strong enough?
4. **Value metric doubles for top customers**: Does pricing still feel fair?
5. **Free tier removed**: Impact on pipeline and brand?
6. **Annual-only billing**: Impact on SMB conversion?

## Output: The Pricing Model

Deliver a structured pricing model document:

```
# Pricing Model: [Product Name]
## Date: [date]
## Based on: [link to research package]

## 1. Value Metric Decision
- Selected metric: [what]
- Rationale: [why]
- Alternatives considered: [list with rejection reasons]

## 2. Tier Architecture
[Full tier definition table]

## 3. Feature Gating
[Feature-by-tier matrix]

## 4. Price Points
[Pricing table with monthly/annual]

## 5. API Pricing (if applicable)
[API-specific pricing model]

## 6. Revenue Projections
[12-month and 24-month models]

## 7. Sensitivity Analysis
[Scenario results]

## 8. Implementation Recommendations
- Billing system requirements
- Metering/tracking needs
- Pricing page design recommendations
- Launch strategy (grandfather existing? migration path?)
```

Save to `pricing-model-[product]-[date].md`.
