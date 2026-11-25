---
name: invoice-health-check
description: Use when scoring invoice completeness, billing accuracy, customer clarity, and collection risk before sending an invoice or publishing a shareable invoice review.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/invoice-health-check/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Invoice Health Check

Use this skill to review an invoice for correctness, clarity, and collection risk before it goes out.

## Inputs

- Invoice draft or export.
- Customer account details, contract or order form, payment terms, billing policy, tax requirements, and prior dispute history.
- Optional benchmark: company invoice checklist or brand tone.

## Workflow

1. Check required invoice fields: legal entity, customer name, billing contact, invoice number, date, due date, terms, currency, tax details, remittance instructions, and payment link.
2. Check billing logic: products, quantities, rates, discounts, credits, billing period, proration, taxes, and totals.
3. Check customer clarity: line descriptions, usage details, support contact, and explanatory notes for unusual charges.
4. Check collection risk: overdue history, invoice complexity, missing PO, disputed account, weak contact, and large variance from prior invoice.
5. Score the invoice from 0-100 and explain the drivers.

## Output

Return:

- Invoice health score.
- Pass/fail checklist.
- Material issues and recommended fixes.
- Collection-risk notes.
- Customer-safe explanation for non-obvious charges when requested.

## Guardrails

- Do not approve an invoice if contract support is missing for material charges.
- Do not add tax, legal, or payment language unless source policy supports it.
- Do not send the invoice.
- Keep the score explainable and source-backed.
