---
name: smb-month-end-prep
version: 1.0.0
description: Walk the owner through month-end close — reconcile books against processor payouts, flag discrepancies, and export a review packet.
author: matrixx0070
tags: [finance, bookkeeping, reconciliation, month-end, accounting, close]
capabilities: []
---

# Month-End Prep

## When to use
Use this at month-end to close the books with confidence. It guides you through reconciling recorded revenue against what payment processors actually deposited, flags mismatches, and assembles a packet for the owner or accountant.

**Not for:** tax estimates or the accountant handoff (use smb-tax-season-organizer); forward cash forecasting (use smb-month-heads-up); making unapproved edits to financial records — every adjustment needs owner sign-off.

## Method
1. **Gather sources.** The month's bookkeeping records plus payout reports from each processor (card, online, marketplace).
2. **Reconcile.** Match recorded income against processor deposits by date and amount. Surface unmatched transactions, unbooked fees, refunds, and chargebacks.
3. **Rank discrepancies.** For each mismatch: likely cause and dollar amount, sorted largest first. Decision point: never silently adjust — a large unexplained gap is a stop-and-ask, not an auto-fix.
4. **Check common gaps.** Uncategorized expenses, missing receipts, duplicate entries, outstanding invoices.
5. **Propose corrections.** Present findings and suggested adjustments. Apply only owner-approved changes.
6. **Export the packet.** Reconciliation summary, flagged items, and a corrections log. State where it was saved. Books are the owner's to sign off.

## Example
March recorded card revenue $24,000; Stripe deposited $22,910. Reconcile: gross $24,000 minus $690 processor fees (not booked) minus two refunds ($400) = $22,910 — matches, so the "gap" is just unbooked fees. Flag: fees $690, action "book as expense." Separately, a $180 charge appears twice — duplicate entry, remove one. Gaps: 3 expenses uncategorized, 1 receipt missing. Packet exported; owner approves the two adjustments before they're applied.

## Pitfalls
- Treating processor fees or refunds as "missing money" instead of expected deductions from gross.
- Silently adjusting entries to force a match — that hides the real error and breaks the audit trail.
- Reconciling only the biggest account and skipping the marketplace payouts where small fees pile up.
- Exporting the packet before the owner has approved corrections, so the numbers ship half-baked.

## Output format
- **Reconciliation summary:** recorded vs deposited | net difference.
- **Discrepancy list (ranked):** item | amount | likely cause | suggested action.
- **Gaps checklist:** uncategorized | missing receipts | duplicates | outstanding invoices.
- **"Approve the adjustments to apply"** gate.
- **Exported packet:** reconciliation + flagged items + corrections log, with save location.

## Reference

### Month-end close checklist (work top to bottom)
1. **Cash / bank reconciliation** — match every bank line to a booked entry; resolve outstanding checks and deposits in transit.
2. **Processor payout reconciliation** — Stripe/Square/PayPal/marketplace: gross sales − fees − refunds − chargebacks − holds/reserves = net deposit. Do each processor separately.
3. **Accounts receivable** — confirm open invoices, apply received payments, age the balance.
4. **Accounts payable** — record all bills received; accrue known unbilled expenses.
5. **Expense categorization** — clear the uncategorized bucket; attach missing receipts.
6. **Payroll** — wages, taxes, and benefits recorded for the period.
7. **Inventory** (if applicable) — adjust to counts; book COGS.
8. **Sales tax** — reconcile collected vs liability.
9. **Duplicates & anomalies** — scan for double entries and out-of-range amounts.
10. **Review & export packet** — summary, flagged items, corrections log; owner/accountant sign-off.

### The processor reconciliation formula
The single most common "missing money" confusion is treating fees and refunds as a gap. They aren't:

`Net deposit = Gross sales − Processor fees − Refunds − Chargebacks − Reserves/holds + Reserve releases`

Worked example: recorded card revenue $24,000; Stripe deposited $22,910. $24,000 − $690 fees − $400 refunds = $22,910 → **matches**; the "gap" is just unbooked fees. Action: book $690 as a processing-expense, book the $400 refunds against revenue. A residual that *doesn't* resolve to fees/refunds/timing is a real discrepancy — stop and investigate.

### Discrepancy triage (rank largest first, never silently adjust)
| Type | Likely cause | Standard action |
|------|--------------|-----------------|
| Unbooked processor fees | Fees netted at payout, not recorded | Book as expense |
| Refund/chargeback not recorded | Post-sale reversal | Book against revenue; note chargeback |
| Timing difference | Sale in month, deposit next month | Record as deposit-in-transit; carry forward |
| Duplicate entry | Same charge booked twice | Remove one; check for a pattern |
| Missing deposit | Payout in reserve/hold, or unrecorded | Trace to processor statement before adjusting |
| Uncategorized expense | Not yet coded | Categorize; request receipt if missing |
| Unexplained large gap | Unknown | **Stop-and-ask** — owner decision, do not force a match |

### Discrepancy tolerance
Set a materiality threshold (e.g. amounts under $5-10 or a small % of the account may be booked as a rounding/misc adjustment with a note). Anything above the threshold, or any *unexplained* gap regardless of size, is escalated to the owner — never plugged. Forcing a match hides the real error and destroys the audit trail.

### Documents to have on hand
Bank statements (all accounts), each processor's monthly payout/fees report, credit-card statements, loan statements, payroll reports, the general ledger / bookkeeping export, open-invoice (AR) and open-bill (AP) lists, and prior-month closing balances to roll forward.

### Cadence and controls
Close within ~5-10 business days of month-end while transactions are fresh. Keep a **corrections log** (what changed, from → to, why, approved by) so the close is auditable. Reconcile *every* account including small marketplace payouts where fees quietly accumulate. Export the packet only *after* the owner has approved the adjustments — the books are the owner's to sign off, and no entry is finalized without that approval.