---
name: pricing
description: "Pricing, packaging and monetization strategy. Use when deciding what to charge, structuring tiers, running a free trial or freemium, or auditing a pricing page."
metadata:
  version: 2.1.1
---

# Pricing Strategy

Design pricing that captures value, drives growth and fits willingness to pay. Read `.agents/product-marketing.md` (or `.claude/product-marketing.md`) first when it exists.

Ask only what is missing: product type and market (SMB, mid-market, enterprise), go-to-market (self-serve, sales-led, hybrid), current pricing, conversion, ARPU and churn, primary value delivered, alternatives and how competitors price, customer feedback on price, and the goal (growth, revenue, profitability; upmarket or downmarket).

## Three axes

- **Packaging**: what each tier includes (features, limits, support).
- **Value metric**: what you charge for; it should scale with the value customers get. Test: "as a customer uses more of this, do they get more value?" Good metrics are easy to understand, grow with the customer and resist gaming. Per seat (collaboration), per usage (variable consumption), per contact or record (CRM, email), per transaction (payments), flat fee (simple products).
- **Price point**: the number.

Price sits between the next best alternative (floor for differentiation) and the customer's perceived value (ceiling). Cost to serve is a baseline only, and a competitor's price is a data point, not a target.

## First price: a bet you can learn from

With no data, pick an order of magnitude by customer: about $10/mo for prosumers, about $100/mo for SMB teams, about $1,000/mo for mid-market or business-critical. Start near the round number and move within the bucket once there is signal.

Avoid ultra-low prices (the "$9 trap"): they create false traction from people who would never pay a real price, make a later 5 to 10x raise hard, and attract the customers who churn most. Round and slightly higher beats clever and cheap. Early on, shipping a price and watching buyers beats modeling ("just charge $50 and see what happens"): if nobody flinches, raise it.

The eight ways to charge (flat, usage, tier, user, feature, credit, outcome, hybrid): [references/pricing-models.md](references/pricing-models.md).

## Tiers

Good-better-best: entry (core features, limited usage, low price), recommended (full features, reasonable limits, the anchor), premium (everything, 2 to 3x the recommended price). Differentiate by feature gating, usage limits, support level, or access (API, SSO, branding). Persona-based packaging and detailed structures: [references/tier-structure.md](references/tier-structure.md).

## Research

Van Westendorp (four price-perception questions; the intersections give the acceptable range) and MaxDiff (most/least important feature sets, to decide what goes in which tier): [references/research-methods.md](references/research-methods.md).

## Raising prices

Signs: competitors raised, prospects don't flinch, "it's so cheap" feedback, conversion above 40%, monthly churn under 3%, much value added since the last change. Roll out in stages: test on new customers first, treat grandfathering as a time-boxed transition, move 5 to 10% of existing customers first and widen in waves, and explain the why months ahead with a generous option (lock-in on annual, grace window, credit). Some churn from the least profitable accounts is expected. Math and sequence: [references/raising-prices.md](references/raising-prices.md).

## Pricing page

- Above the fold: tier comparison, recommended tier highlighted, monthly/annual toggle, a CTA per tier.
- Also: who each tier is for, feature comparison, FAQ, annual discount callout (17 to 20%), money-back guarantee, trust signals.
- Psychology: anchor with the higher price, make the middle tier the best value, .99 endings for value positioning and round prices for premium.
- Put prices in text, not images or "Contact us" only, so buyers and AI agents can read them. Quick check: ask a browsing AI "what are the plans and prices?" for the URL.

Audit of an existing page for clarity, transparency and AI-readability (10-dimension rubric, scoring, report template): [references/pricing-page-teardown.md](references/pricing-page-teardown.md). Conversion testing belongs to `cro`; `Offer` structured data and extractability to `ai-seo`.

## Checklist

Before setting prices: personas defined, competitor pricing reviewed, value metric identified, willingness-to-pay researched, features mapped to tiers. Structure: tier count chosen, tiers clearly differentiated, price points grounded in research, annual discount set, enterprise/custom tier planned.
