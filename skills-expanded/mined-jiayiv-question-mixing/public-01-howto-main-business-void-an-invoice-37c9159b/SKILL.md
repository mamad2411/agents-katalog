---
name: void-an-invoice
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Void an invoice that should no longer be collectible while preserving an audit trail of the original invoice number and reason.

## Preconditions

- The invoice exists and you have authority to void it.
- You know why the invoice should be voided instead of edited, credited, or paid.
- You have checked whether payments, credits, tax filings, or reminders are linked to it.

## Steps

1. **Open the invoice.** Locate the invoice by number, customer, or date. → *Expect:* the invoice details and current status are visible.
2. **Check linked activity.** Review payments, credits, tax, reminders, and customer communications tied to the invoice. → *Expect:* you know the downstream impact of voiding.
3. **Confirm void is the right action.** Compare voiding against editing, issuing a credit memo, or writing off the balance. → *Expect:* voiding is appropriate for an invoice that should not exist as collectible.
4. **Add a reason note.** Record the reason, replacement invoice number if any, and approval. → *Expect:* the audit trail explains the void.
5. **Void the invoice.** ⚠️ *Irreversible:* voiding may permanently cancel the invoice and preserve its number, so confirm customer, invoice number, and reason before proceeding. → *Expect:* the invoice status changes to voided.
6. **Notify affected parties.** Tell the customer or internal team if they received, approved, or were chasing the invoice. → *Expect:* no one continues trying to pay or collect the voided invoice.

## Decision points

- Invoice was already paid → issue a refund or credit instead of voiding unless your accountant approves.
- Invoice was included in a filed tax period → ask your accountant before voiding.
- Customer still owes a corrected amount → create a replacement invoice and reference it.
- Invoice is merely wrong but not sent → edit the draft instead of voiding.

## Failure modes & recovery

- **F1 Voided wrong invoice:** detect by customer, amount, or invoice number mismatch after voiding → recover by recreating the invoice with approval and documenting the error.
- **F2 Payment left unapplied:** detect by customer credit or unapplied payment after voiding → recover by applying, refunding, or crediting according to the situation.
- **F3 Tax report changed:** detect by sales-tax or revenue report variance → recover by consulting accountant and filing adjustments if required.
- **F4 Customer pays old invoice:** detect by payment referencing voided invoice → recover by applying payment to replacement invoice or refunding it.

## Verification

The invoice status is voided, the balance is no longer collectible, the reason and approval are documented, and any replacement invoice or linked payment is handled.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks supports voiding some invoices; Xero may void approved invoices with audit history; generic tools may use cancel, delete, or write-off with different accounting effects.
- `us`: voiding invoices from prior tax periods can affect sales-tax and income reporting.

## Safety & privacy

Medium risk because voiding can change revenue, tax, and customer balances. Preserve the audit trail and do not delete records to hide mistakes.
