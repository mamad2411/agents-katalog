---
name: pricing-triage
description: Use when pricing goals are unclear or mixed, or for brief pricing definitions.
---

# Pricing triage

**Before step 1, read the [shared rules](../references/shared-rules.md).**

## 1. Route

- Send explicit tasks straight to their skill.
- For an unclear request, ask one focused question about the decision or priority. Continue any independent work meanwhile.
- Route by the result the user needs:
  - reusable company facts: [intake](../pricing-intake/SKILL.md)
  - verified calculations or performance explanations: [analyze](../pricing-analyze/SKILL.md)
  - opportunity leads: [scan](../pricing-scan/SKILL.md)
  - an action choice: [recommend](../pricing-recommend/SKILL.md)
  - a strategy or pricing structure: [design](../pricing-design/SKILL.md)
  - a rollout plan: [execute](../pricing-execute/SKILL.md)
- When `.pricing/context.md` is missing, belongs to another company or scope, or lacks a definition the request depends on (such as the price level, cost, returns or currency), also run [intake](../pricing-intake/SKILL.md): propose those facts and ask, while continuing the request under the shared rules.
- Combine only the workflows the request needs, and reuse completed work.
- Route silently, without narrating the routing.

## 2. Brief definitions

- Answer from confirmed facts in `.pricing/context.md`.
- If the company's definition is missing or disputed, ask for it. Label general explanations as general.
- For general price levels, use the [price waterfall](../knowledge/price-waterfall.md). For other general definitions, use the card that owns the term:
  - whether a reported metric is correct and comparable: [metric verification](../knowledge/metric-verification.md)
  - margin movements and their drivers: [margin drivers](../knowledge/margin-drivers.md)
  - realized price change: [price realization](../knowledge/methods/price-realization.md)
  - a proposed price change and breakeven: [price-change economics](../knowledge/methods/price-change-economics.md)
  - recurring revenue, cohorts and churn: [recurring metrics](../knowledge/recurring-metrics.md)
  - retail, channel or order measures: [retail economics](../knowledge/retail-economics.md)
  - hybrid offers: [hybrid offers](../knowledge/methods/hybrid-offers.md)
  - anything else: the [knowledge index](../knowledge/index.md)
- Keep factual answers short.
