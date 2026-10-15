---
name: refund-and-support-flow-review
description: Design and audit refund, cancellation, chargeback, dispute, entitlement revocation, repurchase, appeal, and customer support flows for SaaS, mobile apps, games, utilities, marketplaces, and subscriptions. Use when handling refund policy, abuse ladders, support macros, account restrictions, trust recovery, or post-refund product access.
---

# Refund And Support Flow Review

Use this skill to handle refunds without damaging trust or letting abuse break the product.

## Workflow

1. Identify purchase type, provider/store, entitlement type, refund authority, and support ownership.
2. Read `references/refund-support-flow-patterns.md`.
3. Map refund detection, entitlement adjustment, user messaging, support triage, appeal, and abuse review.
4. Separate ordinary refunds from fraud, chargebacks, and repeated abuse.
5. Produce a flow, support macros, and risk ladder.

## Guardrails

- Do not auto-ban after a normal refund.
- Do not coerce repurchase with threats.
- Keep immutable ledger evidence for support and audit.

## Output format

```text
Purchase/refund context:
Authority:

Flow:
- <step> -> <state/action/message>

Decision table:
- <scenario> -> entitlement action, account action, support action

Support macros/events:
- <macro or event>
```
