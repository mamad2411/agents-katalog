---
name: accounting-bookkeeping
description: Bookkeeping and small-business accounting — double-entry basics, chart of accounts, journal entries, bank reconciliation, accruals vs cash basis, month-end close, P&L (income statement), balance sheet, cash flow statement, VAT/invoice records, expense categorization, trial balance. Use when recording transactions, closing the books, reconciling accounts, or preparing financial statements for a small business.
---

# Accounting & Bookkeeping (double-entry, close, statements)

## The invariant everything hangs on

```
Assets = Liabilities + Equity                (must hold after EVERY entry)
Debits = Credits                              (per entry and in the trial balance)
Debit increases:  assets, expenses
Credit increases: liabilities, equity, revenue
```

Every transaction is a journal entry with at least one debit and one credit, a date, and a
description that names the source document (invoice #, receipt, bank line). An entry you can't
trace to a document is an entry you can't defend.

## Chart of accounts

Keep it small and stable: assets (1xxx), liabilities (2xxx), equity (3xxx), revenue (4xxx),
COGS (5xxx), operating expenses (6xxx) is the common numbering convention. Add accounts when a
category needs its own line on a statement, not for every vendor. Renaming or merging accounts
mid-year breaks comparability — map, don't mutate.

## Accrual vs cash basis — pick one and label it

- **Cash basis**: record when money moves. Simple, matches the bank, distorts months with big
  prepayments or late-paying customers.
- **Accrual basis**: record when earned/incurred. Revenue when invoiced/delivered, expense when
  consumed — with accounts receivable/payable, prepaid expenses, and accrued liabilities carrying
  the timing difference.

Mixing them (accrual revenue, cash expenses is the classic) overstates profit. Statements must
state their basis.

## Bank reconciliation — the truth test

Monthly, per account: start from the bank statement balance, tick off every book entry against a
bank line, and explain every difference (deposits in transit, uncleared checks, bank fees not yet
booked, errors). The reconciliation is done when `bank balance ± reconciling items = book balance`
to the cent. Unreconciled differences "written off to misc expense" are how fraud and duplicate
payments hide.

## Month-end close, in order

1. Post all transactions; chase missing invoices/receipts.
2. Reconcile every bank, card, and loan account.
3. Book accruals/deferrals: earned-not-invoiced, invoiced-not-earned, prepaid amortization,
   depreciation, payroll accrued to the cut-off.
4. Run the trial balance — total debits must equal total credits; investigate, never plug.
5. Review P&L and balance sheet against prior month; explain every large swing before publishing.
6. Lock the period. Post-lock changes go in the next period with a note, never edited in place.

## The three statements and how they tie

- **P&L**: revenue − COGS = gross profit; − operating expenses = operating profit; − interest/tax
  = net income, over a period.
- **Balance sheet**: assets, liabilities, equity at a point in time. Equity includes retained
  earnings, which grows by net income — that's the tie to the P&L.
- **Cash flow statement**: net income adjusted for non-cash items and working-capital changes
  (indirect method), plus investing and financing flows. Ending cash must equal the balance-sheet
  cash line. A profitable P&L with shrinking cash is a receivables or inventory problem, not a mystery.

## VAT / sales tax records

VAT collected on sales is a **liability**, not revenue; VAT paid on purchases is a receivable
(input credit), not an expense — in jurisdictions with input-credit VAT. Book them to dedicated
accounts, reconcile the net against each filing, and keep invoices sequentially numbered with the
tax shown separately. Local rules vary; treat the filing-vs-ledger reconciliation as mandatory.

## Failure modes

- Statements that don't tie: balance-sheet cash ≠ cash flow ending cash, or retained earnings not
  moving by net income.
- Trial balance forced to balance with a "suspense" or "misc" plug that never gets cleared.
- Owner's personal spending run through the business (or paid from personal and never recorded) —
  book it to owner's draw/loan account, not expenses.
- Revenue recognized at invoice for undelivered work, or deposits treated as revenue.
- Negative balances that make no sense (negative cash, negative payables) left uninvestigated.
- VAT included in revenue, inflating the top line by the tax rate.

## Reviewer checklist

- [ ] Basis (cash vs accrual) stated on every statement
- [ ] Every bank/card account reconciled to the cent, differences itemized
- [ ] Trial balance in balance with no aging suspense entries
- [ ] Accruals, prepaids, and depreciation posted before close
- [ ] Cash flow ending cash ties to balance-sheet cash; retained earnings ties to net income
- [ ] VAT booked as liability/receivable, reconciled to filings
- [ ] Prior periods locked; adjustments posted forward, not edited in place

## Provenance

Standard double-entry and month-end-close practice. Account numbering and close order are
conventions, not requirements; VAT treatment varies by jurisdiction — confirm against local rules
and the entity's accountant before filing anything.
