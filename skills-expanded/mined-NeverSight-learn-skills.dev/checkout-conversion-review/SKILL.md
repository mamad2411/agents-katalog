---
name: checkout-conversion-review
description: Audit and design checkout, cart, payment, trial, upgrade, paywall, Apple Pay, Google Pay, card, invoice, discount, tax, error recovery, and post-purchase conversion flows for SaaS, apps, games, utilities, marketplaces, and web products. Use when improving revenue conversion, reducing payment failure, making checkout trustworthy, or reviewing checkout analytics and support readiness.
---

# Checkout Conversion Review

Use this skill to improve checkout revenue without adding dark patterns, payment fragility, or support debt.

## Workflow

1. Identify the product type, buyer intent, price model, payment channels, and entitlement granted after purchase.
2. Read `references/checkout-conversion-systems.md`.
3. Map the funnel from pricing/offer exposure to payment confirmation, entitlement grant, receipt, and support trace.
4. Separate trust, clarity, speed, payment reliability, recovery, and measurement issues.
5. Produce a prioritized conversion plan with guardrails, instrumentation, and rollback criteria.

## Guardrails

- Do not hide price, renewal, tax, cancellation, or refund consequences.
- Do not optimize click-through at the cost of refund rate, chargeback risk, or support load.
- Treat payment success and entitlement grant as separate states; both need evidence.

## Output format

```text
Checkout context:
Primary conversion constraint:

Funnel map:
- <step> -> user intent, system state, failure/recovery

Findings:
- P0 <issue> -> fix, metric, risk
- P1 <issue> -> fix, metric, risk

Instrumentation:
- <event> with key properties

Experiment/rollout:
- hypothesis, segment, success metric, guardrail metric, stop rule
```
