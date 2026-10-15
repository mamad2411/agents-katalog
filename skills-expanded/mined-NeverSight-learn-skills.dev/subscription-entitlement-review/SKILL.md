---
name: subscription-entitlement-review
description: Design and audit subscription and entitlement systems for SaaS, mobile apps, games, desktop utilities, and marketplaces across plans, trials, renewals, grace periods, downgrades, upgrades, restore purchases, refunds, revocations, usage limits, ledger events, and support tooling. Use when pricing, billing, access, or account state must stay consistent after payment changes.
---

# Subscription Entitlement Review

Use this skill to keep money movement, product access, and support truth aligned.

## Workflow

1. Identify billing model, platform/provider, product catalog, and entitlement surfaces.
2. Read `references/subscription-entitlement-patterns.md`.
3. Map subscription states, entitlement derivation, ledger events, support views, and user messaging.
4. Check upgrades, downgrades, trials, grace, cancellation, refund, restore, and renewal failure paths.
5. Produce a state machine, risks, and acceptance checks.

## Guardrails

- Do not treat client UI state as the source of truth for durable access.
- Do not mix cancellation, refund, failed renewal, and fraud into one state.
- Preserve user trust with clear access consequences and support traceability.

## Output format

```text
Billing model:
Provider/platform:
Entitlement surfaces:

State model:
- <state> -> <meaning and transition>

Risks and fixes:
- <rule id> <risk> -> <fix>

Support/readiness checks:
- <check>
```
