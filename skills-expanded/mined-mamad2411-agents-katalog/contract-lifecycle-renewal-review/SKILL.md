---
name: contract-lifecycle-renewal-review
description: Review SaaS and enterprise contract lifecycle, renewals, auto-renewal windows, true-ups, co-terming, amendments, cancellations, expansion, procurement, legal, billing, entitlements, and customer-success handoffs. Use when agents need to design or audit renewal workflows that protect revenue without trapping customers.
---

# Contract Lifecycle Renewal Review

Use this skill to convert contract lifecycle, renewal, expansion, cancellation, true-up, amendment, procurement, billing, and entitlement questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify customer segment, contract type, term dates, renewal notice window, auto-renewal rule, pricing model, entitlements, billing source of truth, legal owner, and customer-success owner.
2. Read `references/contract-lifecycle-renewal-patterns.md`.
3. Classify the account as new contract, active term, renewal-ready, renewal-risk, expansion, downgrade, cancellation, true-up, dispute, or post-term reconciliation.
4. Define renewal calendar, health signals, commercial approvals, quote/order/invoice handoff, entitlement change gate, customer communication, cancellation path, and exception policy.
5. Produce renewal operating plan, state machine, decision table, event schema, risk checklist, and owner-by-date action list.

## Guardrails

- Do not rely on surprise auto-renewal, hidden cancellation windows, or dark-pattern retention to protect revenue.
- Do not change entitlements from CRM notes alone; reconcile contract, billing, provisioning, and support records.
- Do not treat usage true-ups, price increases, expansion, and collections disputes as the same workflow.
- Do not promise renewal terms, credits, cancellations, or legal exceptions without an accountable commercial/legal owner.

## Output format

```text
Renewal context:
Audience / source of truth / risk boundary:

Renewal operating plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Renewal, downgrade, cancellation, and true-up handling:
- <trigger> -> <policy, metric, edge case, support note>
```
