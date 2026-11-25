---
name: freemium-vs-paid-gate
description: "Decide whether a product should offer a free tier, free trial, or go straight to paid. Structured decision framework based on economics, distribution model, and competitive landscape. Use when launching a new product or reconsidering your pricing model."
---

# Freemium vs. Paid Gate

Decide whether to offer a free tier, free trial, or go straight to paid.

## How to use

- `/freemium-vs-paid-gate` Apply pricing model constraints to this conversation.
- `/freemium-vs-paid-gate <product>` Recommend a pricing model for the described product.

## Constraints

### Qualifying Questions
Answer all five before choosing a model:
1. Does the product have natural network effects? (More users = better for everyone)
2. What's the marginal cost per free user? (Near zero, moderate, or high)
3. How long until the user hits the aha moment? (Minutes, days, or weeks)
4. Is the buyer the same person as the user?
5. Do competitors offer a strong free tier?

### Model Selection
- Free tier IF: network effects exist, marginal cost is low, aha moment takes time, selling bottom-up into organizations
- Free trial IF: value is obvious quickly, marginal cost is moderate-to-high, selling to individual decision-makers
- Straight to paid IF: niche with high willingness to pay, product requires onboarding investment, B2B enterprise with long sales cycles
- Usage-limited free IF: API or infrastructure product where value scales linearly with usage

### Gate Design
- Feature gates: lock specific pro features behind paid. MUST ensure free tier still delivers real value.
- Usage gates: limits on volume, storage, API calls, team members. MUST correlate with growing value.
- Time gates: full access for limited time. Best for complex products that need evaluation time.
- NEVER design gates that make the free product feel intentionally broken

### Conversion Benchmarks
- Free to paid conversion: 2-5% is typical, 10%+ is exceptional
- Free trial to paid: 15-25% is typical for good products
- If below these ranges, the problem is usually activation, not pricing

### Anti-Patterns
- The Zombie Free Tier: millions of free users, almost none converting. You've built a charity.
- The Bait and Switch: generous free tier you suddenly restrict. Destroys trust instantly.
- Free as Default: offering free because you're afraid to charge, not because it serves strategy
- Ignoring Free User Cost: not tracking what free users actually cost in infrastructure and support
