---
name: usage-billing-review
description: Use when reviewing metered usage invoices against usage exports, pricing rules, minimum commitments, credits, customer entitlements, and billing exceptions.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/usage-billing-review/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Usage Billing Review

Use this skill to validate usage-based billing before an invoice goes to the customer.

## Inputs

- Usage export with customer ID, meter name, period, quantity, unit, and source timestamp.
- Pricing terms, rate cards, tiers, included units, minimum commitments, and overage rules.
- Draft invoice lines.
- Known exceptions such as test accounts, internal usage, credits, outages, or contract overrides.

## Workflow

1. Confirm the billing period and customer identifiers match across usage, contract, and invoice data.
2. Aggregate usage by billable meter and compare it with the invoice.
3. Apply pricing rules in this order: included usage, credits, tiering, minimums, overages, discounts, and taxes if provided.
4. Flag usage anomalies: sudden spikes, negative usage, duplicate records, missing days, unknown meters, and units that do not match the contract.
5. Classify variances by customer impact and materiality.

## Output

Return:

- Billing readiness summary: ready, ready with minor cleanup, blocked, or requires approval.
- Meter comparison table with usage quantity, billed quantity, expected charge, invoice charge, variance, and evidence.
- Exception queue with owner and recommended resolution.
- Customer-safe explanation for material usage variance when requested.

## Guardrails

- Do not assume internal, test, or failed usage is billable unless source policy says so.
- Do not smooth or alter usage data without preserving the original source values.
- Do not approve billing for unknown meters or unmapped customer IDs.
- Escalate material variances before invoice release.
