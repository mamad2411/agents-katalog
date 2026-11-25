---
name: procurement-pricing-packaging-review
description: Review enterprise procurement pricing and packaging covering SKU structure, tier names, seat/usage metrics, minimums, commits, discounts, price holds, order forms, PO/invoice needs, tax, legal/security review, renewal uplift, co-terming, true-ups, budget cycles, procurement objections, and buyer-facing value proof. Use when pricing must pass procurement without damaging margin or trust.
---

# Procurement Pricing Packaging Review

Use this skill to convert enterprise procurement, pricing, packaging, SKU, discounting, order-form, and buyer-objection questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify buyer segment, package/SKU structure, value metric, minimums, commit terms, discount policy, procurement process, invoice/PO needs, legal/security review, budget timing, and margin constraints.
2. Read `references/procurement-pricing-packaging-patterns.md`.
3. Classify package motion as self-serve upgrade, sales-assisted plan, enterprise order form, usage commit, seat expansion, add-on, services, marketplace purchase, or renewal uplift.
4. Define procurement-ready packaging, approved discount/exception rules, value proof, quote/order handoff, billing/tax requirements, security/legal artifacts, and renewal/true-up path.
5. Produce packaging review, state machine, decision table, event schema, procurement checklist, and deal-desk controls.

## Guardrails

- Do not create bespoke SKUs or discount exceptions without owner approval, billing support, margin impact, and renewal consequences.
- Do not hide usage limits, overages, renewal uplift, minimums, or cancellation constraints until procurement.
- Do not let procurement concessions undermine public pricing trust, product packaging clarity, or supportability.
- Do not promise invoice, tax, marketplace, legal, security, or vendor-management capabilities that operations cannot fulfill.

## Output format

```text
Procurement packaging context:
Audience / source of truth / risk boundary:

Pricing and packaging plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Discounts, exceptions, order forms, and procurement proof:
- <trigger> -> <policy, metric, edge case, support note>
```
