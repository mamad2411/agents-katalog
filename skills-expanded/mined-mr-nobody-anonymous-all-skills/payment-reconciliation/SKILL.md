---
name: payment-reconciliation
description: Use when matching payments, deposits, processor payouts, remittance advice, bank activity, invoices, credit memos, and unapplied cash for finance operations.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/payment-reconciliation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Payment Reconciliation

Use this skill to match cash activity to invoices and identify reconciliation exceptions.

## Inputs

- Bank export, processor payout report, or payment gateway export.
- Invoice register, AR subledger, customer IDs, and payment references.
- Remittance advice, lockbox files, or customer emails.
- FX rates, fees, chargebacks, refunds, credits, and unapplied cash reports if available.

## Workflow

1. Normalize dates, currencies, customer names, references, invoice IDs, and amounts.
2. Match using strongest evidence first: invoice ID, payment reference, customer ID, exact amount, remittance detail, then fuzzy name/date/amount matching.
3. Separate fees, refunds, chargebacks, FX variance, partial payments, and overpayments.
4. Assign match confidence: exact, strong, probable, weak, or unmatched.
5. Prepare an exception list for manual review.

## Output

Return:

- Reconciliation summary: matched amount, unmatched amount, fees, refunds, and material exceptions.
- Match table with payment, invoice, amount, date, confidence, and evidence.
- Unmatched cash and unapplied credit queue.
- Recommended journal or subledger action as a draft only, never posted.

## Guardrails

- Do not post entries, apply payments, issue refunds, or write off balances.
- Do not force-match weak evidence to clear a variance.
- Preserve original transaction IDs and source filenames.
- Flag duplicate payments and suspicious activity for human review.
