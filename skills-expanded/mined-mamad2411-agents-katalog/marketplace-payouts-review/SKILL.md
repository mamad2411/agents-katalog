---
name: marketplace-payouts-review
description: Design and audit marketplace payout, earnings, fee, revenue share, seller balance, creator payout, refund, chargeback, hold, clawback, split payment, ledger, tax/compliance handoff, payout support, and dispute flows for creator marketplaces, app/plugin stores, gig marketplaces, game marketplaces, affiliate programs, and two-sided platforms. Use when money moves from buyers through the platform to sellers or creators.
---

# Marketplace Payouts Review

Use this skill to make marketplace payouts traceable, fair, supportable, and resilient to refunds or abuse.

## Workflow

1. Identify marketplace type, parties, transaction model, fee model, payout schedule, risk window, and provider constraints.
2. Read `references/marketplace-payout-systems.md`.
3. Map buyer payment, platform fee, seller earnings, pending balance, holds, refunds, disputes, adjustments, payout, and reconciliation.
4. Separate ledger truth, displayed balances, provider state, policy decisions, and support evidence.
5. Produce payout state machine, fee table, risk controls, support views, and reconciliation checks.

## Guardrails

- Do not treat displayed balance as ledger truth.
- Do not pay out funds that remain within a refund, fraud, chargeback, or delivery-risk window unless risk is explicitly accepted.
- Do not make opaque holds or clawbacks without reason, evidence, and appeal/support path.

## Output format

```text
Marketplace/payout context:
Fee and risk model:

Payout flow:
- <state> -> owner, evidence, user message

Decision table:
- <scenario> -> balance action, payout action, support action

Ledger/events:
- <event> with properties

Open risks:
- <risk> -> mitigation
```
