---
name: smb-close-month
version: 1.0.0
description: Run a small-business month-end close — reconcile books against processors and bank, propose adjustments, and produce a plain-English P&L narrative.
author: matrixx0070
tags: [small-business, month-end, close, reconciliation, p&l, bookkeeping]
capabilities: []
---

# Close the Month

## When to use
Use this at month-end to close the books cleanly: match recorded revenue and fees against payment processors and bank deposits, catch missing entries, and explain the month's P&L in plain language.

**Not for:** forward forecasting (use smb-cash-flow) or a live status read (use smb-business-pulse). This closes a completed period and never posts to the books without sign-off.

## Method
1. **Set the period.** State the month, the ledger source, and the processors and accounts in scope (bank, Stripe/Square/PayPal, card).
2. **Reconcile deposits.** Match each processor payout and bank deposit to recorded revenue. Surface unmatched items and processor fees not yet booked.
3. **Reconcile expenses.** Tie card and bank charges to recorded bills. Flag duplicates, personal charges, and uncategorized spend.
4. **Book adjustments.** List accruals, deferrals, and corrections, each with amount and reason. Decision point: propose only — do not post without owner or accountant sign-off.
5. **Build the P&L.** Summarize revenue, COGS, gross margin, operating expenses, and net income vs prior month and vs budget.
6. **Write the narrative.** Explain the three biggest drivers of the change in plain English.

Anything that changes the books is a proposal for the owner (or their accountant) to approve.

## Example
June, QuickBooks + Stripe + bank. Stripe payout $8,420 matched revenue but $310 in fees weren't booked — proposed adjustment. Two $49 charges to the same SaaS vendor on the same day flagged as a likely duplicate. Net income $12,100, up $2,300 vs May, driven by higher repeat orders, lower ad spend, and the un-booked Stripe fees now corrected. Awaiting sign-off on 3 adjustments.

## Pitfalls
- **Posting adjustments directly.** Always propose; the owner or accountant approves every book change.
- **Ignoring processor fees.** Gross payouts booked as revenue overstate income — reconcile net of fees.
- **Force-matching to clear the list.** An unmatched item is a signal, not a nuisance; leave it flagged.
- **A P&L with no story.** Numbers without the top-3 drivers leave the owner guessing.

## Output format
```
Period: <month> | Accounts: <list>
Reconciliation (per account):
  matched $__ | unmatched <n> | fees to book $__
Adjustments proposed (pending approval):
  - <item> — $__ — <reason>
P&L: revenue $__ | COGS $__ | gross $__ | opex $__ | net $__
       vs prior <±> | vs budget <±>
Narrative: top 3 drivers
Open items / sign-off gate
```

## Reference

### Month-end close checklist (run in order)
A clean close is a sequence, not a scramble. Work top to bottom; each step feeds the next:

1. **Cutoff.** Confirm all transactions dated in the month are entered and nothing from the next month leaked in. Verify invoice and bill dates match when the work/goods actually changed hands.
2. **Bank reconciliation.** Match every line on the bank statement to the ledger. Ending balance on the statement must equal the reconciled ledger balance. Investigate outstanding checks/deposits in transit.
3. **Processor reconciliation.** For each of Stripe/Square/PayPal: gross sales − refunds − fees = net payout to bank. Book the fees as an expense; don't record gross as revenue.
4. **Credit-card & AP reconciliation.** Tie every card charge and vendor bill to a receipt/invoice; categorize the uncategorized.
5. **AR review.** Confirm open invoices are real and current; age them; write off/allow for the truly uncollectible (propose only).
6. **Inventory / COGS.** Adjust for counts, spoilage, or shrinkage if you carry stock; ensure COGS matches units actually sold.
7. **Payroll.** Confirm wages, payroll taxes, and benefits are booked in the correct period.
8. **Accruals & deferrals.** Book expenses incurred but not yet billed (accrue) and prepaid items spread over time (defer/amortize).
9. **Owner/personal cleanup.** Move any personal charges out of business expense; record owner draws/contributions correctly.
10. **Review & lock.** Compare P&L and balance sheet vs prior month and budget; explain variances; then propose closing/locking the period so it can't be silently changed.

### Common close gaps (the usual suspects)
- **Processor fees not booked** — the #1 SMB miss; overstates revenue and net income.
- **Duplicate bills/charges** — same vendor, same/near amount, close dates (auto-pay + manual entry).
- **Deposits booked gross** — a $10,000 payout that was $10,340 in sales minus $340 fees.
- **Personal on the business card** — inflates expenses, distorts margin, creates tax risk.
- **Uncategorized "Ask my accountant" bucket** — clear it every month; it hides both errors and deductions.
- **Timing/cutoff errors** — December work invoiced in January (or vice versa) throws off the period.
- **Sales tax treated as revenue** — it's a liability you collected and owe, not income.
- **Unrecorded accruals** — the utility bill that arrives on the 5th but belongs to last month.

### Adjusting-entry types (for the proposals)
- **Accrual** — record revenue earned or expense incurred but not yet invoiced (e.g., accrue $600 for work delivered, billing next month).
- **Deferral** — spread a prepaid amount (annual insurance/software) across the months it covers.
- **Depreciation/amortization** — periodic write-down of an asset's cost.
- **Reclassification** — move a mis-coded transaction to the right account.
- **Correction/reversal** — fix or reverse a duplicate or erroneous entry.
Each proposed entry needs: account(s) affected, debit/credit amount, and a plain-English reason.

### Tie-out targets (what "matched" means)
- Bank: reconciled ledger balance = statement ending balance, to the cent.
- Each processor: recorded net revenue = payouts to bank, with fees separately expensed.
- AR/AP subledgers = the control accounts on the balance sheet.
- Sales tax collected = sales tax liability on the books.
Anything that won't tie stays on the open-items list as a flag — never force a match to clear the queue.

### The P&L narrative (top-3 drivers)
Numbers need a story. For each of the three biggest month-over-month or vs-budget swings, state: what moved, by how much, and why (one sentence). Example: "Net income up $2,300 vs May: repeat orders up ~$4k, ad spend down ~$1.5k, offset by newly-booked Stripe fees of $310." Distinguish one-offs from trends so the owner doesn't over-read a lucky month.

### Owner/accountant sign-off gate
This skill reconciles and proposes; it posts nothing. Every adjusting entry, write-off, reclass, and the period-lock itself is presented for the owner (or their accountant) to approve. Return the change list so the close is auditable after approval.
