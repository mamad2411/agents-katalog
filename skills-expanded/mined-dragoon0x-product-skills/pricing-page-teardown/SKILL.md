---
name: pricing-page-teardown
description: "Analyze a pricing page and identify what's working, what's broken, and what's leaving money on the table. Covers tier structure, anchor pricing, CTA clarity, and anti-patterns that kill conversion. Use when designing, redesigning, or diagnosing an underperforming pricing page."
---

# Pricing Page Teardown

Analyze a pricing page and identify what's working, what's broken, and what's leaving money on the table.

## How to use

- `/pricing-page-teardown` Apply pricing teardown constraints to this conversation.
- `/pricing-page-teardown <url or description>` Tear down a specific pricing page.

## Constraints

### 5-Second Test
- Can a visitor tell what this product does in under 5 seconds?
- Can they immediately see how many plans exist?
- Is there an obvious recommended or default choice?
- Is the price visible before scrolling?
- If any answer is no, that's a conversion leak. Flag it.

### Tier Architecture
- MUST have 3 tiers for most products. 2 feels limiting. 4+ creates decision paralysis.
- MUST name tiers by who they serve, not by size ("For teams" beats "Business")
- Each upgrade MUST have one clear hero feature that justifies the price jump
- NEVER gate basic functionality that makes the free tier feel broken
- SHOULD highlight the recommended plan visually

### Value Metric Alignment
- The thing you charge for MUST scale with the value the customer gets
- Per seat: good for collaboration tools where more users = more value
- Per usage: good for infrastructure, APIs, compute
- Flat rate: good for simple tools where value doesn't scale with volume
- NEVER charge per seat for a tool only one person uses
- NEVER use a value metric that punishes customer success

### CTA and Friction Audit
- Primary CTA MUST match the buying model ("Start free trial" for complex, "Get started" for simple)
- MUST show annual vs. monthly savings clearly with a toggle
- SHOULD show a money-back guarantee near the CTA
- Count clicks from pricing page to paying. Every unnecessary click kills conversion.
- NEVER require a credit card for trial unless intentionally filtering volume

### Trust and Objection Handling
- MUST include social proof near pricing (logos, testimonials, user counts)
- SHOULD include a FAQ section addressing common objections
- SHOULD show security/compliance badges if relevant to the buyer
- MUST make cancellation policy clear and visible

### Anti-Patterns
- The Feature Dump: 40-row comparison table nobody reads. Limit to 5-7 differentiating features.
- Hidden Costs: base price looks great, then add-ons multiply the real cost
- The Vanity Free Tier: free plan so limited it generates negative word-of-mouth
- Price Shock: no context for why something costs what it costs. Always anchor value before showing price.
- The Identical Middle: two plans that look almost the same. If you can't articulate the difference, merge them.
