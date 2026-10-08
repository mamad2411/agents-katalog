---
name: startup-business-models
description: Use when choosing or evaluating a startup revenue model, pricing/value metric, packaging/tier design, or calculating unit economics (LTV, CAC, payback, gross margin, NRR), including usage-based/credit/AI pricing and variable compute/COGS constraints.
---

# Startup Business Models

Systematic workflow for choosing revenue models, pricing, and unit economics.

## Quick Start (Inputs)

Ask for the smallest set of inputs that makes the decision meaningful:

- Business type: SaaS, usage-based/API, marketplace, services, hardware + service
- ICP/segment(s): SMB / mid-market / enterprise (and ACV/ARPA bands)
- Current pricing and packaging: value metric, tiers, limits, discount policy, billing cadence
- Unit economics drivers: fully-loaded CAC, gross margin/COGS (include LLM/infra/third-party), churn/retention, expansion (NRR)
- Constraints: sales motion (PLG vs sales-led), implementation constraints (billing metering, proration), gross margin floor, payback target

If numbers are missing, proceed with ranges + explicit assumptions and highlight what to measure next.

## Workflow

1) Classify the model
- Subscription, usage-based, freemium, marketplace take-rate, transaction fee, ads, outcome-based, credit-based, hybrid.

2) Build a segment-level unit economics snapshot
- Use [the bundled unit-economics methodology](../financial-unit-economics/resources/methodology.md) for formulas and pitfalls; verify any benchmark against the relevant segment and stage.
- Prefer cohort/segment views over blended averages.

3) Evaluate model fit and risks
- Align price metric with value delivered and cost incurred (especially usage + AI compute).
- Identify failure modes: margin compression, adverse selection, channel conflict, support cost explosions, metering/overage friction.

4) Propose pricing + packaging changes
- Use [pricing-strategy](../pricing-strategy/SKILL.md) for willingness-to-pay research and tier differentiation.
- Draft a tier table with segment, value metric, price, included usage, limits, upgrade trigger, and enforcement rule. Label untested prices as hypotheses.

5) Define measurement and roll-out
- Define success metric + guardrails, evaluation design, and explicit lag windows (conversion now, retention later).

6) Deliver a decision-ready output
- Recommendation, rationale, assumptions, scenarios (base/best/worst), and next experiments.

## 2026 Heuristics (Context-Dependent)

- Prioritize payback and gross margin over a single ratio; LTV:CAC is easiest to game.
- Typical SaaS targets (directional, by segment/stage): LTV:CAC 3-5x, payback 6-12 months (PLG) or 12-18 months (sales-led early), NRR >100% (mid-market/enterprise) and gross margin >70% (software-only).
- For usage-based / AI products: model contribution margin per unit (token/job/workflow) and set pricing guardrails (rate limits, minimums, commit tiers, credit expiries).

## Related Skills (Routing)

- [product-strategist](../product-strategist/SKILL.md): competitive positioning, go-to-market planning, and the business model canvas.
- [startup-financial-modeling](../startup-financial-modeling/SKILL.md): revenue projections, runway, and fundraising scenarios.
- [pricing-strategy](../pricing-strategy/SKILL.md): pricing research and packaging.

For idea validation, record the customer problem, evidence of willingness to pay, and the next experiment before committing to a model.

## Pricing Change Measurement & Experiment Design
Use this when you are changing pricing, packaging, value metric, limits, discounts, or billing cadence.

### 1) Define success and guardrails (before launch)
| Type | Examples |
|------|----------|
| Primary success metric | Net revenue retention (NRR), ARPA/ARPU, gross margin %, payback period, upgrade rate, expansion MRR |
| Guardrails | New logo conversion, activation rate, refund rate, support load, churn (logo + revenue), sales cycle length |

### 2) Pick an evaluation design
| Design | Best when | How to read results |
|--------|-----------|---------------------|
| A/B (randomized) | Self-serve / PLG flows | Compare conversion, ARPA, refunds, and downstream retention by assignment |
| Holdout/control cohort | Pricing is hard to randomize | Compare treated vs. holdout cohorts matched on segment, channel, and start month |
| Step rollout (time-based) | Enterprise contracts, invoicing cycles | Compare pre/post with a parallel cohort (not exposed yet) to reduce seasonality bias |
| Geo/account rollout | Regions/segments are separable | Compare regions/segments; watch for channel mix shifts |

### 3) Use explicit lag windows (avoid premature conclusions)
- Short lag (days to 2 weeks): checkout conversion, activation, sales cycle friction, refund/support spikes.
- Medium lag (4 to 8 weeks): upgrades, expansion MRR, usage growth, discounting behavior, proration effects.
- Long lag (90 to 180+ days, B2B): churn, net revenue retention, renewal outcomes, contraction risk.

### 4) Report an "all-in" view (not just conversion)
- Revenue quality: net revenue after refunds, discounts, and credits; gross margin impact (including variable compute/COGS).
- Segments: break down by plan, seat band, channel, ACV/ARR band, and customer age (new vs. renewal).
- Decision rule: write a go/no-go threshold (example: "NRR +2pts with no >0.5pt drop in activation and no >10% increase in support load").

## Available Resources and Outputs

| Need | Bundled guidance |
|------|------------------|
| CAC, LTV, payback, and cohort analysis | [Unit-economics methodology](../financial-unit-economics/resources/methodology.md) and [worksheet](../financial-unit-economics/resources/template.md) |
| Willingness-to-pay and tier design | [Pricing strategy](../pricing-strategy/SKILL.md) |
| Business model canvas | [Product strategist](../product-strategist/SKILL.md), Business Model Canvas section |
| MRR/ARR, burn, runway, and scenarios | [Startup financial modeling](../startup-financial-modeling/SKILL.md) |

Create the pricing-tier table described in Workflow step 4 and an assumptions table with input, value/range, source URL, date, and confidence. This skill does not bundle separate canvas/pricing template files or a data-source catalog. Use current, attributable sources for business decisions.

---

## Do / Avoid (Jan 2026)

### Do

- Define your value metric (seat/usage/outcome) and validate willingness-to-pay early.
- Include COGS drivers in pricing decisions (especially usage-based).
- Use discount guardrails and renewal logic (avoid ad-hoc deals).

### Avoid

- Pricing as an afterthought (“we’ll figure it out later”).
- Margin blindness (shipping usage growth that destroys gross margin).
- Misleading LTV calculations from immature cohorts.

## What Good Looks Like

- Packaging: a clear value metric, tier logic, and discount policy (with enforcement rules).
- Unit economics: CAC, gross margin, churn, payback, and retention defined and tied to cohorts.
- Assumptions: one inputs sheet, ranges/sensitivities, and scenarios (base/best/worst).
- Experiments: pricing changes tested with decision rules (not “gut feel” rollouts).
- Risks: margin compression, adverse selection, channel conflict, and support cost modeled.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Summarize pricing research and competitor snapshots; verify manually before acting.
- Draft pricing page copy; humans verify claims and consistency with contracts.
