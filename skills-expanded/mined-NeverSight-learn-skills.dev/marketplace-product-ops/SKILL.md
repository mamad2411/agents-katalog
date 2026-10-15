---
name: marketplace-product-ops
description: Design and audit marketplace operating systems including two-sided marketplaces, creator marketplaces, plugin/skill/app marketplaces, listings, submissions, review queues, ranking, trust and safety, payouts, disputes, refunds, moderation, quality scoring, discovery, support, and growth loops. Use when creating or improving a marketplace repository, store, directory, creator platform, or community exchange.
---

# Marketplace Product Ops

Use this skill to make marketplaces trustworthy, discoverable, fair, and operable before growth exposes weak rules.

## Workflow

1. Identify sides of the marketplace, supply unit, demand job, transaction type, and trust risk.
2. Read `references/marketplace-product-ops-systems.md`.
3. Map submission, review, listing, ranking, install/purchase, fulfillment, support, dispute, payout, and removal states.
4. Separate quality control, moderation, fraud, incentives, discovery, and creator success.
5. Produce an operating model with policies, queues, metrics, and escalation paths.

## Guardrails

- Do not launch open submission without review, abuse handling, and takedown paths.
- Do not rank only by engagement when quality, safety, or freshness matters.
- Do not mix creator payout decisions with opaque moderation decisions without appeal paths.

## Output format

```text
Marketplace type:
Supply/demand sides:
Trust model:

Operating system:
- submission/review:
- listing/discovery:
- transaction/fulfillment:
- support/disputes:
- payouts/incentives:

Policy gaps:
- <gap> -> rule, owner, evidence

Metrics:
- supply quality, demand success, trust, revenue, support load
```
