---
name: pricing-20-videos
description: Helps price a B2B product or service (strategy, packaging, raising prices, value-based pricing) using rules weighted by how many of the 20 most-watched videos repeat each one, and flags where the experts disagree so you A/B test instead of guessing. Use when the user says "help me price this", "should I raise my prices", "value-based pricing", "how should I package my tiers", "stop charging hourly", "hybrid or usage pricing", or "review my pricing page".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /pricing

This skill is built from the transcripts of the 20 most-watched videos on B2B pricing from the last 6 months (since 2026-03-14). Those videos have 78,215 views and 76,828 words. From them, 415 pieces of advice were extracted, 381 were kept because their verbatim quote was found in the transcript, and they group into 148 distinct themes. The number next to each rule is how many of the 20 videos say it, and the sources are in sources.md.

The most repeated rule reached 9 of 20. Treat the weights as odds, not laws.

## Inputs
1. What you sell and who buys it: product or service, ideal customer profile, and how the buyer is billed today.
2. Your current pricing: model (hourly, fixed fee, subscription, usage, hybrid), price points, tiers, and when prices last changed.
3. The value you create for the buyer, backed by evidence: time saved, revenue gained, or costs cut. Include customer or churn feedback if you have it.
4. Your real numbers where available: close rate, churn, customer lifetime, sales cycle length, and the cost to serve.

Refuse to invent customer value figures, close rates, churn data, or competitor prices. If they are missing, ask for them or mark them as unknown.

## The rules, by weight

### Strong (5 to 9 of 20)
- **Price on outcomes and value delivered, not effort or cost.** (9/20) For example, anchor the price to a client going from $200k to $400k in revenue, or set a fixed fee for a defined scope and outcome.
- **Use higher price as a filter for committed customers.** (6/20) In one case, cutting from $99 to $19/month collapsed LTV 10x, with a 3.1 month lifetime at $19 against 8.8 months at $99.
- **Combine a base fee with usage or performance charges.** (6/20) An example is a $2,000 setup fee plus 5% of sales generated. Watch heavy users, since 5-10% of users can use 80% of compute.
- **Raise prices only after proving and adding real value.** (6/20) For example, grow proven savings from 20% to 30% first, then charge more.
- **Gather ongoing customer and churn feedback to inform pricing.** (6/20) You don't need a 100k survey.
- **Don't underprice out of fear or to seem affordable.** (5/20) One company, Jimdo, went 5 years without raising prices because of fear.
- **Price at a premium to win fewer, better-paying clients.** (5/20) One business cut its client list in half and grew revenue 3-5x.
- **Treat pricing as a continuous, evolving hypothesis.** (5/20) Update pricing the way you update product and marketing, not once and forget it.

### Solid (4 of 20)
- **Stop billing hourly; grow value per hour instead.** (4/20) At $300/hr, 1,400 realistic billable hours caps you near $400k. One $40,000 engagement equals 133 of those hours.
- **Offer multiple pricing tiers, such as three tiers.** (4/20) For example: solo, team, enterprise.
- **Avoid cost-plus pricing.** (4/20) Customers don't care about your costs, so cost-plus underprices high-value products.
- **Build recurring subscription revenue over one-time pricing.** (4/20) In one case, switching back to subscription grew MRR after pay-per-review had stalled it.
- **Review pricing on a regular cadence.** (4/20) Suggested cadences range from every 1-2 months to quarterly. Another option is to match your sales cycle and review against that cohort's data.
- **Align and verify your value metric with customer perception.** (4/20) If the metric is misaligned, no price point will feel right to customers.

### Mentioned (3 of 20)
Quantify the concrete dollar value you create for clients · Charge a fraction of the value you create · Choose pricing model to fit the project, market, and stage · Define what value you actually sell before pricing · Raise prices gradually and modestly, measuring results · Tie pricing to outcomes or consumption, not seats or subscriptions · Don't compete by undercutting competitors on price · Offer free or low tiers to capture leads and upgrades · Don't copy or average competitor prices · Settle framing, packaging, and model before price points · Use a structured, deliberate pricing process, not gut feel · Treat price optimization as a high-leverage growth lever

## Where the experts disagree: do not pick, test

| Choice | Side A | Side B |
|---|---|---|
| How to raise prices | Price at a premium to win fewer, better-paying clients (5/20) | Raise prices gradually and modestly, measuring results (3/20) |
| What to charge for | Build recurring subscription revenue over one-time pricing (4/20) | Tie pricing to outcomes or consumption, not seats or subscriptions (3/20) |

## Steps
1. **Collect the inputs.** List every missing number as unknown and do not fill gaps with guesses.
2. **Define the value.** Write down what value you actually sell and the buyer's measurable outcome, in the buyer's terms. Check that your value metric matches how customers see that value.
3. **Check the current model.** Look for hourly billing, cost-plus markups, fear-based low prices, or competitor copying. Name each one you find and the Strong or Solid rule it breaks.
4. **Settle structure before numbers.** Decide packaging, then structure, then metric (tiers, base fee plus usage or performance, subscription or outcome-based). Only then set price points.
5. **Set prices from proven value, not cost.** Where the value is quantified, use it as the anchor. Only propose a raise where value has been proven or added.
6. **Pick one disagreement to A/B test.** Examples are a premium jump against a modest step increase, or subscription against an outcome-based charge. Define the metric to watch, such as close rate over the next set of calls, churn, or customer lifetime.
7. **Set a feedback loop and review date.** Gather customer and churn feedback continuously, and choose a review cadence tied to the sales cycle.
8. **Summarize.** List which rules were applied with their weight (for example, "Price on outcomes and value delivered, 9/20") and state which choice is being A/B tested.

## Never
- Never claim results the user has not measured, such as revenue lift, lower churn, or a better close rate.
- Never invent facts about the prospect or customer, including their budget, the value they get, or their willingness to pay.
- Never set a price by copying, averaging, or undercutting competitor prices.
