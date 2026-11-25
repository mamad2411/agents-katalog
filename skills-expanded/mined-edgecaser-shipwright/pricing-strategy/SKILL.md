---
name: pricing-strategy
description: "Structures a comprehensive pricing analysis covering willingness-to-pay research design, pricing model comparison (per-seat, usage-based, flat-rate, freemium, hybrid), competitive pricing intelligence, price sensitivity testing, and packaging strategy. Helps PMs make pricing decisions grounded in data rather than gut feel."
category: pricing
default_depth: standard
---

# Pricing Strategy Analyzer

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Structures a comprehensive pricing analysis covering willingness-to-pay research design, pricing model comparison (per-seat, usage-based, flat-rate, freemium, hybrid), competitive pricing intelligence, price sensitivity testing, and packaging strategy. Helps PMs make pricing decisions grounded in data rather than gut feel.

## When to Use

- Setting initial pricing for a new product
- Evaluating a pricing model change (e.g., per-seat to usage-based)
- Annual pricing review and optimization
- Competitive pricing response
- Designing a free tier or freemium model
- Preparing for a pricing increase

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick pricing gut-check or early-stage product with no existing data | Pricing Objectives + Value Metric Identification + Model Recommendation only |
| **Standard** | Setting or revising pricing with available customer and competitive data | All sections |
| **Deep** | Major pricing model migration or enterprise pricing overhaul | All sections + segment-specific WTP analysis, migration modeling, revenue cannibalization scenarios |

**Omit rules:** At Light depth, skip WTP Research Design, Competitive Pricing Analysis, and Packaging Design. Produce only Objectives, Value Metric, and Model Recommendation.

## Framework

### Step 1: Pricing Objectives

```markdown
## Pricing Analysis: [Product / Feature]

### Pricing Objectives
| Objective | Priority | Rationale |
|---|---|---|
| Revenue maximization | [High/Med/Low] | [Why] |
| Market penetration | [High/Med/Low] | [Why] |
| Competitive positioning | [High/Med/Low] | [Why] |
| Customer acquisition efficiency | [High/Med/Low] | [Why] |
| Expansion revenue | [High/Med/Low] | [Why] |

### Current State (if existing pricing)
- Model: [Per-seat / Usage / Flat / Freemium / Custom]
- Price points: [Tier 1: $X, Tier 2: $Y, Enterprise: Custom]
- ARPU: $[X]/month
- Conversion rate (free → paid): [X]%
- Net revenue retention: [X]%
- Price-related churn: [X]% of total churn
```

### Step 2: Value Metric Identification

The value metric is what you charge for, it should align with how customers perceive and receive value.

```markdown
## Value Metric Analysis

### Candidate Value Metrics
| Metric | Scales with Value? | Easy to Understand? | Predictable for Buyer? | Grows with Usage? |
|---|---|---|---|---|
| Per seat/user | Partial | Yes | Yes | Sometimes |
| Per [unit of usage] | Yes | Moderate | No, variable | Yes |
| Per [resource] | Yes | Yes | Yes | Yes |
| Flat rate | No | Yes | Yes | No |

### Recommended Value Metric: [metric]
**Rationale:** [Why this metric best aligns price with value]
**Risk:** [What could go wrong, e.g., "Usage unpredictability may deter risk-averse buyers"]
**Mitigation:** [How to address, e.g., "Offer committed-use discounts"]
```

### Step 3: Pricing Model Comparison

```markdown
## Model Comparison

| Model | Revenue Predictability | Adoption Friction | Expansion Potential | Complexity | Best For |
|---|---|---|---|---|---|
| **Per-seat** | High | Medium | Linear (more users) | Low | Collaboration tools |
| **Usage-based** | Low | Low (pay-as-you-go) | High (organic growth) | High | API, infrastructure |
| **Flat-rate** | High | Low | None (until upgrade) | Low | Simple products |
| **Tiered** | High | Medium | Step-function (tier jumps) | Medium | Feature-gated products |
| **Freemium** | Low (free users) | Very Low | High (conversion funnel) | Medium | PLG products |
| **Hybrid** | Medium | Medium | High | High | Mature products |

### Recommended Model: [model]
**Structure:**
- Free tier: [what's included, limits]
- Tier 1 ([name]): $[X]/mo, [what's included]
- Tier 2 ([name]): $[X]/mo, [what's included]
- Enterprise: Custom, [what's included]

**Rationale:** [Why this model and structure]
```

### Step 4: Willingness-to-Pay Research

```markdown
## WTP Research Design

### Van Westendorp Price Sensitivity Meter
Ask target customers these 4 questions:

1. "At what price would you consider [product] to be **so expensive** that you would not consider buying it?"
2. "At what price would you consider [product] to be **expensive** but you would still consider buying it?"
3. "At what price would you consider [product] to be a **bargain**, a great buy for the money?"
4. "At what price would you consider [product] to be **so cheap** that you would question its quality?"

**Output:** Plot the 4 curves to find:
- Point of Marginal Cheapness (PMC)
- Point of Marginal Expensiveness (PME)
- Optimal Price Point (OPP), where "too cheap" and "too expensive" intersect
- Indifference Price Point (IDP), where "cheap" and "expensive" intersect

### Gabor-Granger Direct Pricing
For each price point, ask:
"Would you purchase [product] at $[X]/month?"
- Definitely would
- Probably would
- Might or might not
- Probably would not
- Definitely would not

Test 5-7 price points to build a demand curve.

### Research Parameters
- **Sample size:** Minimum [N] per segment (recommend 100+)
- **Segments to test:** [Segment A, Segment B, Segment C]
- **Recruitment:** [How to find respondents, existing users, prospects, panel]
- **Timeline:** [How long to run the study]
```

### Step 5: Competitive Pricing Analysis

If structured research facts are available from a prior `collect-research.mjs` run, generate the comparison table deterministically instead of by hand:

```bash
node scripts/pricing-diff.mjs \
  .shipwright/research/competitor-a/facts.json \
  .shipwright/research/competitor-b/facts.json
# or, if you staged only the intended packs together:
# node scripts/pricing-diff.mjs --dir path/to/comparison-set/
```

The output is a ready-to-cite markdown table covering plan names, prices, billing periods, free tier presence, and confidence levels. Paste it directly into the Competitive Pricing Landscape section. If facts files are not available, build the table manually below.

```markdown
## Competitive Pricing Landscape

| Competitor | Model | Entry Price | Mid-Tier | Enterprise | Free Tier? |
|---|---|---|---|---|---|
| [Comp A] | Per-seat | $[X]/user/mo | $[Y]/user/mo | Custom | [Yes/No] |
| [Comp B] | Usage | $[X]/[unit] | Volume discounts | Custom | [Yes/No] |

### Positioning Options
| Strategy | Our Price vs. Market | Message | When to Use |
|---|---|---|---|
| Premium | 20-50% above | "Worth every penny" | Strong differentiation |
| Parity | Within 10% | "Same value, better X" | Feature parity, compete on other dimensions |
| Penetration | 20-40% below | "All the value, lower cost" | Entering established market |
| Freemium | $0 entry | "Start free, pay when you grow" | PLG, network effects |
```

### Step 6: Packaging Design

```markdown
## Packaging Strategy

### Tier Design Principles
- **Free/Starter:** Enough value to hook, limits that create natural upgrade triggers
- **Mid-tier:** Sweet spot for your ICP. This is where most revenue should come from.
- **Enterprise:** Removes all limits, adds admin/security/compliance features

### Upgrade Triggers
| Trigger | From | To | Why It Works |
|---|---|---|---|
| [Hit seat limit] | Free | Starter | Natural team growth |
| [Need advanced feature] | Starter | Pro | Value demonstrated |
| [Compliance requirement] | Pro | Enterprise | Non-negotiable need |

### Feature Gating Matrix
| Feature | Free | Starter | Pro | Enterprise |
|---|---|---|---|---|
| [Core feature] | ✓ (limited) | ✓ | ✓ | ✓ |
| [Power feature] | ✗ | ✓ | ✓ | ✓ |
| [Admin feature] | ✗ | ✗ | ✓ | ✓ |
| [Enterprise feature] | ✗ | ✗ | ✗ | ✓ |
```

## Minimum Evidence Bar

**Price-change decision boundary:** For a proposed change, carry the user's timing, affected customer population, and stated conditions through the recommendation, next action, and Decision Frame. A relative period is a planning window, not an exact effective or notice date. Leave unspecified dates, contract terms, and rollout scope unknown; label any suggested dates or cohorts as proposals. Keep acquisition and retention evidence distinct: a test of new-buyer conversion may inform new-buyer demand, but extending a change to existing customers needs evidence about renewal, downgrade, churn, or a relevant existing-customer test. If that evidence is missing, give a provisional verdict and name the missing check rather than making a rollout commitment.

**Financial claims:** State the population, horizon, baseline, and assumptions behind any break-even calculation. A revenue threshold is arithmetic under those assumptions, not an observed response, acceptable churn target, profit result, or causal forecast. Evaluate contribution profit and longer-term effects separately when the decision depends on them; mark missing inputs rather than inferring them from list-price arithmetic.

**Required inputs:** Product description with target customer segment, current pricing (if any), and at least one of: customer interview data, competitive pricing data, or usage/conversion analytics. At Light depth, product description and target customer segment are sufficient, data inputs are deferred to Standard/Deep.

**Acceptable evidence:** Van Westendorp or Gabor-Granger survey results, win/loss data citing price, competitive pricing pages, ARPU and conversion cohorts, customer interviews mentioning willingness-to-pay, usage data showing value metric correlation.

**Insufficient evidence:** With no customer, competitive or usage evidence, return a hypothesis-only model comparison and the smallest research step that could change the decision. Do not invent a price range. Choose WTP research method and sample needs for the segment and decision; no fixed respondent count guarantees reliable pricing.

**Hypotheses vs. findings:**
- **Findings:** Current state metrics, competitive pricing landscape, and value metric alignment scores must be grounded in evidence.
- **Hypotheses:** Recommended price points, projected conversion impact, and tier boundaries without WTP data are hypotheses, must be labeled as such.

## Output Format

Produce a Pricing Strategy Document with:
1. **Pricing Objectives**, what we're optimizing for
2. **Value Metric**, what we charge for and why
3. **Model Recommendation**, pricing model with structure
4. **WTP Research Plan**, methodology for validating price points
5. **Competitive Analysis**, market pricing landscape
6. **Packaging Design**, tier structure with feature gating and upgrade triggers

**Shipwright Signature (required closing):**
7. **Decision Frame**, Recommended pricing model and price point, acquisition vs. revenue trade-off, confidence level with evidence quality, pricing owner, decision date, revisit trigger (e.g., competitive move, NRR shift)
8. **Unknowns & Evidence Gaps**, WTP ranges not yet validated, segments not surveyed, competitive pricing behind sales walls
9. **Pass/Fail Readiness**, PASS for a pricing recommendation if the value metric and model have evidence-backed rationale and the range is defensible. Light depth may PASS as a hypothesis-only model assessment with evidence gaps explicit; it is not approval to change prices.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Cost-plus pricing**, Price based on value delivered, not cost to build
- **One price for everyone**, Different segments have different willingness-to-pay; tiering captures this
- **Free tier too generous**, If there's no reason to upgrade, free users stay free forever
- **Pricing without research**, Gut-feel pricing leaves money on the table or prices you out of deals
- **Never raising prices**, If you haven't raised prices in 2+ years, you're almost certainly underpriced

## Weak vs. Strong Output

**Weak:**
> "We recommend usage-based pricing because it aligns with value."

No value metric specified, no comparison to alternatives, no evidence for why this model fits the product or buyer.

**Strong:**
> "We recommend usage-based pricing on API calls (metered monthly, billed in arrears) over per-seat, because 78% of revenue comes from 12% of accounts by volume, per-seat would undertax heavy integrators by 4x, and 3 of 4 direct competitors already use usage-based models, reducing buyer friction on model comprehension."

Specific metric, quantified rationale, competitive validation, and addresses buyer experience.
