---
name: billing-reconciliation-review
description: Design and audit billing reconciliation across invoices, payments, ledgers, entitlements, app-store receipts, subscriptions, IAP, payouts, refunds, chargebacks, taxes, credits, adjustments, revenue recognition inputs, and support evidence. Use when money movement, customer access, or marketplace balances must match across systems.
---

# Billing Reconciliation Review

Use this skill to convert a high-stakes product decision into a concrete, measurable, reviewable operating artifact.

## Workflow

1. Identify money systems, authoritative ledger, payment providers, entitlement source, payout surface, tax/invoice requirements, and support consumers.
2. Read `references/billing-reconciliation-patterns.md`.
3. Map event lifecycle from order/renewal through payment, entitlement, invoice, refund, dispute, payout, and adjustment.
4. Define reconciliation keys, expected invariants, mismatch classes, retry/repair workflow, and audit evidence.
5. Produce reconciliation matrix, state machine, exception queue, event schema, and support/admin view requirements.

## Guardrails

- Do not use payment provider state as the only source of truth for product access without a derived entitlement model.
- Do not silently repair money mismatches without audit logs.
- Do not mix customer-facing credits, accounting adjustments, and promotional balances without clear types.
- Escalate tax, accounting, and revenue recognition policy to qualified owners.

## Output format

```text
Billing context:
Providers / ledger / entitlement source:

Reconciliation matrix:
| Object | Source A | Source B | Key | Invariant | Mismatch action |
| --- | --- | --- | --- | --- | --- |

Exception queue:
- <mismatch> -> <severity, owner, repair, user impact>

Events/support evidence:
- <event/admin field/support macro>
```
