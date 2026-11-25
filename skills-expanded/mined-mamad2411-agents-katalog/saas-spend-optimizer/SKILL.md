---
name: saas-spend-optimizer
description: Use to analyze SaaS billing/usage exports (Zuora, Stripe, vendor invoices) and surface optimization opportunities — unused seats, duplicate tools, over-provisioned tiers, autorenewals coming up, and ARR-at-risk.
---

# SaaS Spend Optimizer

## When to invoke
- "Find waste in our SaaS stack."
- "Which renewals are coming up in the next 60 days?"
- "What seats are unused?"

## Inputs needed
1. **Subscriptions CSV** — vendor, plan, seats, cost_monthly, renewal_date.
2. **Usage CSV** (optional but recommended) — vendor, user, last_active.
3. **Org headcount** (for benchmarking).

## Workflow
1. **Ingest** subs + usage.
2. **Compute** seat utilization, $/active user, autorenewal calendar.
3. **Classify** waste types: unused seats, dead tools, duplicates by category.
4. **Estimate savings** — annualized.
5. **Report** with actions: cancel, downgrade, consolidate, renegotiate.

## Output format
```
## Top savings opportunities
- $X/yr — vendor — action — owner
## Renewal calendar (next 90 days)
- date — vendor — amount — action by date
## Duplicates by category
- category — vendors — recommendation
```

## Guardrails
- Always show the underlying counts, not just %.
- Flag low-confidence (no usage data) recommendations as such.
- Do NOT recommend cancellation of vendors with active integrations marked critical.

## Reference code
`optimize.py` reads CSVs and emits a Markdown brief plus a JSON summary.
