---
name: revenue-recognition-policy-review
description: Review revenue recognition policy impacts for SaaS, subscriptions, usage billing, credits, discounts, bundles, upgrades, downgrades, renewals, cancellations, refunds, implementation fees, marketplaces, deferred revenue, contract modifications, and finance handoffs. Use when product, pricing, billing, or sales changes could affect when revenue should be recognized.
---

# Revenue Recognition Policy Review

Use this skill to convert revenue recognition, pricing, billing, contract modification, deferred revenue, and finance handoff questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify product motion, contract type, performance obligations, pricing model, billing cadence, delivery/activation event, refund/credit terms, modification path, and finance owner.
2. Read `references/revenue-recognition-policy-patterns.md`.
3. Classify the change as new sale, renewal, upgrade, downgrade, usage overage, prepaid credit, implementation service, refund, cancellation, bundle, marketplace transaction, or contract modification.
4. Define recognition trigger, evidence source, accounting review, billing/revenue reconciliation, customer communication, exception approval, and control owner.
5. Produce recognition-impact review, state machine, decision table, event schema, control checklist, and launch gate.

## Guardrails

- Do not treat invoice date, cash receipt, entitlement grant, and revenue recognition as automatically equivalent.
- Do not launch new pricing, credits, bundles, or contract changes without finance/accounting review.
- Do not hide refunds, concessions, side letters, usage corrections, or implementation obligations from revenue controls.
- Do not present accounting conclusions as legal/accounting advice; route final policy to qualified owners.

## Output format

```text
Revenue context:
Audience / source of truth / risk boundary:

Recognition policy plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Controls, exceptions, and finance handoffs:
- <trigger> -> <policy, metric, edge case, support note>
```
