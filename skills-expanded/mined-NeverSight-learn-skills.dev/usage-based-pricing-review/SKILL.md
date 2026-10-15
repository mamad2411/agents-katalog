---
name: usage-based-pricing-review
description: Design and audit usage-based pricing, metering, quotas, credits, overages, spend controls, billing events, cost drivers, value metrics, free allowances, invoices, expansion paths, abuse controls, and customer trust for SaaS, APIs, AI products, infrastructure tools, developer platforms, marketplaces, and consumption businesses. Use when pricing is tied to seats, usage, credits, API calls, storage, compute, messages, tokens, transactions, or metered value.
---

# Usage Based Pricing Review

Use this skill to turn usage pricing into a trustworthy revenue system instead of a surprise bill generator.

## Workflow

1. Identify buyer, user, value metric, cost driver, usage unit, billing period, and expansion path.
2. Read `references/usage-based-pricing-systems.md`.
3. Map metering, aggregation, quota, alert, invoice, adjustment, dispute, and support states.
4. Separate customer value, provider cost, predictability, abuse risk, and growth incentives.
5. Produce pricing architecture, event contract, guardrails, and experiment plan.

## Guardrails

- Do not hide metering logic, renewal price, overage rules, or invoice timing.
- Do not choose a metric solely because it is easy to meter; it must correlate with customer value.
- Provide budgets, caps, alerts, and support evidence before exposing high-variance bills.

## Output format

```text
Pricing context:
Recommended value metric:

Usage system:
- meter, unit, aggregation, allowance, overage, cap, alert

Plan architecture:
- free/trial:
- core paid:
- expansion:
- enterprise/control:

Risks and mitigations:
- <risk> -> product, billing, support, analytics response

Instrumentation:
- <event> with properties
```
