---
name: product-lifecycle-architect
description: Plan and review products end to end across strategy, market research, product design, UI, monetization, distribution, operations, promotion, customer support, and lifecycle management. Use when designing a new app, SaaS, game, utility, web product, desktop product, product roadmap, launch plan, or full product operating system.
---

# Product Lifecycle Architect

Use this skill to turn a product idea into a complete operating blueprint rather than a pile of features.

## Workflow

1. Classify the product type: mobile app, game, web app, SaaS, desktop utility, developer tool, marketplace, or hybrid.
2. Read `references/product-lifecycle-matrix.md` and select the relevant lifecycle rows.
3. Define the product promise, target user, wedge, business model, and distribution path.
4. Map all required systems: onboarding, account, payment, entitlement, notification, backup, support, analytics, promotion, and operations.
5. Identify missing state machines, edge cases, metrics, and support flows.
6. Produce a phased roadmap with P0/P1/P2, but ensure every P0 item is production-shaped.

## Output format

```text
Product type:
Wedge:
Business model:
Distribution channels:

P0 product operating system:
- <system> — user promise, states, edge cases, metrics

P1/P2 roadmap:
- <system> — why later, dependency, proof needed

Risks:
- <risk and mitigation>
```
