---
name: ar-aging-and-cash-application
description: Build an accounts receivable aging report and apply incoming cash to invoices. Covers aging buckets, due dates from payment terms, allocation order, early-payment (settlement) discounts, partial payments, credit memos, unapplied cash, disputes and collection stages. Use for AR aging, collections prioritisation, or cash application tasks.
---

# AR aging and cash application

Goal: as of a reporting date, determine what each customer still owes, how overdue it is, and what to do about it. Correctness depends on the order of operations and on rules that are usually implied, so enumerate them first.

## 1. Read all sources before computing
Read every policy document, terms file and notes in full. Tables of history (terms that changed over time, disputes, write-offs) are rules too, not decoration. Hints in a collections policy about discounts or exclusions are binding. If a rule has an obvious generic meaning (below), apply it even if only mentioned once.

## 2. Due dates and terms
- Due date = invoice date + terms days (Net N), or end of month + N for EOM terms. Use the terms that were in force on the invoice date, not the current terms, when a terms history exists.
- "Days past due" = reporting date - due date. Not yet due (<= 0) goes in the current bucket. Be explicit whether the due date itself counts as past due (normally not).
- Standard buckets: current, 1-30, 31-60, 61-90, 90+ days past due. Use the spec's bucket edges; boundaries are inclusive on the upper side of each bucket.
- Only invoices dated on or before the reporting date count; payments after it are ignored (as-of semantics).

## 3. Payments, credits and allocation
- A payment that references an invoice is applied to that invoice first. A reference may be messy (case, spacing, prefix); normalise before matching and never apply to a non-existent invoice.
- Unreferenced cash is applied in a fixed order. Default: oldest due date first (FIFO by due date), ties by invoice date then id. Use the spec's order if stated. Allocate across invoices until the cash is exhausted; the last one may be partially paid.
- Partial payments reduce the open balance; the remainder keeps the ORIGINAL due date and ages from it.
- Cash left after all open invoices are settled is unapplied cash. It is a credit to the customer, not a negative bucket; report it separately.
- Credit memos reduce the amount owed. A memo tied to an invoice reduces that invoice; an unattached memo is a customer credit that offsets the total balance. Keep customer credits (unapplied cash plus unapplied memos) distinct from past-due buckets, and make net exposure = open invoices - credits only if the spec defines it so.
- Chargebacks, refunds and reversals reopen or create balance; reversals of a payment must be undone before allocation.

## 4. Discounts and settlement terms
- Terms of the form "x/y Net z" mean: x% discount if paid within y days of the invoice date, otherwise the full amount is due in z days. Count days from the invoice date, inclusive of the last discount day.
- A payment inside the discount window that equals the discounted amount (net of the discount, within rounding) settles the invoice in full; the withheld discount is not an open balance. Apply the discount test before treating the shortfall as a partial payment.
- Payments just short of the full amount because of rounding or bank fees leave small residuals; treat residuals under the spec's materiality limit as zero.
- Late payments forfeit the discount.

## 5. Disputes and collections stages
- Disputed invoices stay in the aging buckets (they are still owed) but are normally excluded from collections-reminder/escalation actions. Apply the exclusion only to the action, not to the balance, unless told otherwise.
- Collections stage is driven by days past due of the oldest unpaid undisputed item, per spec thresholds. Compute the stage from what remains AFTER cash application.

## 6. Money and rounding
- Work in integer cents (or Decimal). Round discounts and percentages once, half up, at the point the spec defines. Never accumulate floats.
- Totals must tie: sum of buckets = total open; open + credits relationships stated in the spec must hold exactly.

## 7. Order of operations (most common bug source)
1. Parse and normalise invoices, payments, memos, terms (with history).
2. Drop anything after the reporting date.
3. Apply referenced payments (with discount test), then credit memos.
4. Apply unreferenced cash in the allocation order.
5. Zero out immaterial residuals.
6. Age what remains, bucket it, compute credits and stage.
7. Format output exactly as specified (key names, ordering, units).

## 8. Self-checks
- Pick customers with a partial payment, a discount payment, a dispute, unapplied cash and changed terms and recompute by hand.
- No invoice has a negative open amount; no payment is applied twice; total cash in = applied + unapplied.
- Count of customers and sort order match the spec.
