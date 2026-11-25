---
name: contract-to-invoice
description: Use when extracting billing obligations from contracts, order forms, SOWs, pricing tables, or amendments and comparing them against draft or issued invoices.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/contract-to-invoice/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Contract To Invoice

Use this skill to compare what a customer contract says should be billed against what an invoice shows.

## Inputs

- Contract, order form, SOW, amendment, or pricing excerpt.
- Invoice draft or issued invoice.
- Billing period, subscription start and end dates, renewal terms, usage terms, and discounts.
- Any billing policy for proration, taxes, credits, or minimums.

## Workflow

1. Extract billing terms: customer, product, quantity, price, discount, term, billing frequency, start date, end date, minimums, overages, taxes, payment terms, and special conditions.
2. Compare extracted terms to invoice lines.
3. Recalculate invoice expectations where enough data exists.
4. Classify exceptions:
   - Missing line.
   - Extra line.
   - Incorrect quantity.
   - Incorrect rate.
   - Incorrect billing period.
   - Missing discount or credit.
   - Tax or payment-term mismatch.
   - Ambiguous contract language.
5. Identify whether each exception is customer-facing, accounting-only, or requires legal or sales review.

## Output

Return:

- Contract billing summary.
- Invoice comparison table with expected value, invoice value, variance, source reference, and confidence.
- Exception list with severity and owner.
- Questions for sales, legal, billing, or the customer.

## Guardrails

- Quote short source snippets only when needed and keep them minimal.
- Do not interpret ambiguous legal terms as final. Escalate ambiguity.
- Do not approve an invoice for sending when material terms are missing.
- Preserve source references so reviewers can verify every variance.
