---
name: pricing-page
description: "Present pricing in ways that reduce friction and increase clarity. Handles tier naming, feature comparison, anchor pricing, and plan selection psychology. Use when designing pricing pages, plan selectors, or upgrade prompts."
---

# Pricing Page

Present pricing in ways that reduce friction and increase clarity.

## How to use

- `/pricing-page` Apply pricing page constraints to this conversation.

## Constraints

### Structure
- MUST lead with the recommended plan (visual emphasis, "Most Popular" badge)
- MUST limit to 3-4 tiers. More creates decision paralysis.
- MUST name tiers by who they serve, not by size ("For teams" not "Business")
- MUST show monthly and annual pricing with clear savings callout
- NEVER hide pricing behind "Contact us" unless average deal size exceeds $10k/year

### Feature Comparison
- MUST group features by category, not random list
- MUST bold the differentiating features between tiers
- SHOULD use checkmarks sparingly. Specific values beat yes/no.
- NEVER list features the user doesn't understand without explanation
- MUST highlight what the user loses by choosing a lower tier, not just what they gain

### Psychology
- Anchor with the highest-priced tier first (right to left reading)
- SHOULD include a free or low-cost entry point to reduce commitment anxiety
- MUST make the upgrade path obvious from within the product
- NEVER use dark patterns (hidden fees, pre-checked add-ons, confusing renewals)

### Copy
- Plan descriptions: one sentence explaining who this tier is for
- CTA button text should reflect the action ("Start free trial" not "Submit")
- Price should be the largest text element in each tier card
- MUST show what currency the price is in
