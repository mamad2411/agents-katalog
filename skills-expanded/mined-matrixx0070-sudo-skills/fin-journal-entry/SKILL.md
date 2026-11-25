---
name: fin-journal-entry
version: 1.0.0
description: Draft balanced, review-ready journal entries (accruals, depreciation, rev-rec, reclasses) with calculation, support, and reversal.
author: matrixx0070
tags: [finance, accounting, journal-entry, accruals, depreciation, revenue-recognition]
---

# Journal Entry

## When to use
Use this to draft a journal entry that passes review the first time — accruals, prepaid amortization, depreciation, revenue recognition, or reclasses — with the debits, credits, calculation, and support an approver needs.

**Not for:** correcting entries that fall out of a reconciliation (fin-reconciliation proposes those), or sequencing when entries post during close (fin-close-management). This is the *content* of one entry.

## Method
1. **Identify transaction and type.** State what happened, the entry type (accrual, deferral, depreciation, rev-rec, reclass), and the period it belongs to.
2. **Apply the treatment.** Cite the driver: matching principle for accruals, straight-line (or chosen method) for depreciation, ASC 606 five-step for revenue.
3. **Compute the amount.** Show the calculation step by step (e.g., (cost − salvage) / useful life; contract value × % complete or ratable portion).
4. **Build the entry.** List each account with number, debit or credit, and amount. Decision point: debits must equal credits — if they don't, do not post; find the missing leg.
5. **Attach support.** Reference the invoice, contract, schedule, or accrual worksheet backing each line.
6. **Plan the reversal.** Decision point: if it is an accrual or deferral, set the reversal date and mechanism now — an unreversed accrual double-counts next period.
7. **Self-check.** Confirm it balances, hits the correct period, and uses valid active accounts.

## Example
Accrue December consulting: work done, invoice not received, belongs to December (matching). Estimate from the SOW: $12,000/month, 80% complete = $9,600.
```
Dr 6200 Consulting expense   9,600
   Cr 2100 Accrued liabilities   9,600
```
Debits = credits = $9,600. Support: SOW #C-4471, PM completion note. Reversal: Jan 1, auto-reverse (invoice will post against 2100). Reviewer note: estimate; true-up on receipt.

## Pitfalls
- **Entry that doesn't balance.** A one-sided or mistyped amount is the most common review kick-back — total both columns before submitting.
- **Wrong period.** Booking December work in January defeats the accrual's purpose and distorts both months.
- **Missing reversal on an accrual.** It silently double-counts when the actual invoice posts.
- **No support reference.** "Accrual, $9,600" with no SOW or worksheet is unauditable — the approver cannot verify the number.

## Output format
```
Description: <...> | Type: <accrual/...> | Period: <...> | Posting date: <...>
Rationale: <principle / ASC standard>
Calculation: <shown step by step>
Entry:
  | account | acct # | debit | credit |
  Totals:            | <sum> | <sum> |  → equal? [yes/no]
Support: <invoice / contract / schedule refs>
Reversal: <date + mechanism, or N/A>
Reviewer notes: <...>
```

## Reference

### Standard entry patterns
Every entry below balances (debits = credits). Signs assume normal balances: assets/expenses rise with debits, liabilities/equity/revenue rise with credits.

| Situation | Debit | Credit | Driver / note |
|---|---|---|---|
| **Expense accrual** (service used, no invoice) | Expense | Accrued liabilities | Matching principle; reverse next period |
| **Revenue accrual** (earned, not billed) | Unbilled AR (contract asset) | Revenue | ASC 606; becomes AR when invoiced |
| **Prepaid — initial** | Prepaid asset | Cash / AP | Pay now, consume later |
| **Prepaid — amortization** | Expense | Prepaid asset | Monthly = total ÷ term |
| **Depreciation** | Depreciation expense | Accumulated depreciation | Contra-asset; never credit the asset directly |
| **Deferred revenue — cash in** | Cash | Deferred revenue (liability) | Obligation not yet satisfied |
| **Deferred revenue — recognition** | Deferred revenue | Revenue | As performance obligation is met |
| **Payroll — gross** | Salary/wage expense | Cash, taxes payable, benefits payable | Gross wage splits into net pay + withholdings |
| **Employer payroll tax** | Payroll tax expense | Payroll taxes payable | Employer FICA/FUTA/SUTA — separate from withheld |
| **Bad debt (allowance method)** | Bad debt expense | Allowance for doubtful accounts | Contra-AR; write-off later hits allowance vs AR |
| **Inventory purchase (perpetual)** | Inventory | AP | |
| **COGS at sale (perpetual)** | COGS | Inventory | Two-line sale: also Dr AR / Cr Revenue |
| **Accrued interest** | Interest expense | Interest payable | Principal × rate × days/360 (or /365) |
| **FX remeasurement (monetary)** | FX loss (or Cr FX gain) | Payable/receivable | Reprice monetary balances at period-end rate |

### Key calculations
- **Straight-line depreciation:** (Cost − Salvage) ÷ Useful life (years). Monthly = annual ÷ 12; pro-rate the acquisition month.
- **Double-declining balance:** Net book value × (2 ÷ useful life); switch to straight-line when it yields a larger deduction; never depreciate below salvage.
- **Prepaid amortization:** Total prepaid ÷ coverage months; partial first month = daily rate × days remaining.
- **Accrued interest:** Principal × annual rate × (days ÷ 360). Confirm day-count convention (30/360 vs actual/365) from the note.
- **Units-of-production depreciation:** (Cost − Salvage) ÷ total estimated units × units this period.

### ASC 606 five-step (revenue recognition)
1. Identify the contract with the customer.
2. Identify the distinct performance obligations (POs).
3. Determine the transaction price (include variable consideration, capped at the amount not likely to reverse).
4. Allocate the price to POs by relative standalone selling price (SSP).
5. Recognize revenue as each PO is satisfied — point-in-time (control transfers) or over-time (customer consumes / you have an enforceable right to payment for work done).

Common 606 shapes: a SaaS subscription is over-time (ratable); a perpetual license is point-in-time; a bundled license + support splits by SSP and recognizes each leg on its own pattern. Unbilled earned revenue = **contract asset**; cash collected ahead of delivery = **contract liability (deferred revenue)**.

### Reversal discipline
Auto-reverse accruals and deferrals on day 1 of the next period so the actual invoice/payment posts cleanly against the reversed accrual with no double count. Non-reversing entries: depreciation, amortization of a multi-period prepaid (only the consumed slice each month), and true one-time reclasses. A quick test: if the entry estimates something the real transaction will later record, it reverses.

### Review checklist
- Debits = credits, to the cent.
- Correct period and posting date (cutoff respected).
- Accounts active and valid; expense vs. capitalize decision defensible.
- Support attached and traceable to the amount.
- Reversal set (or explicitly N/A).
- Estimate flagged with a true-up plan.
