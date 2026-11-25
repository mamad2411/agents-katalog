---
name: catchup-bookkeeping
description: >
  Contains verified opening-balance JE construction logic, summary-vs-detailed entry strategy
  decision framework (2-year threshold), and bank statement transaction-type routing tables that
  produce more precise answers than reasoning from general training alone. Backlog assessment,
  catch-up period boundaries, monthly summary JEs, OBE cleanup, hybrid multi-year reconstruction,
  fiscal year alignment, tax-filing readiness gates. Consult when books are months or years behind,
  reconstructing GL from statements, or asking "should I use summary JEs or enter each transaction."
---

# Catch-Up Bookkeeping

Operational skill for planning and executing multi-period bookkeeping reconstruction.
Covers the full lifecycle from backlog assessment through transaction entry to period
validation, with decision logic for choosing between summary and detailed approaches.

## When This Skill Applies

- Business has fallen behind on bookkeeping (months or years of unrecorded activity)
- Migrating from another system with incomplete or missing data
- Reconstructing records from bank/brokerage statements
- Preparing for audit or tax filing of prior years
- Converting messy/partial records into a clean general ledger

## Engagement Planning

### Source Document Checklist

Gather before starting any catch-up work:

**Bank and Financial Statements** — All checking, savings, money market statements; credit card statements; loan statements with amortization schedules; brokerage/investment account statements

**Income Documentation** — Invoices issued, payment receipts, 1099s received for prior years, sales reports or POS summaries

**Expense Documentation** — Bills, receipts, and vendor invoices; payroll records and pay stubs; prior tax filings (if any exist); contracts, leases, and agreements

**Priority**: Bank and credit card statements are the minimum viable source set. If nothing else is available, statements alone can reconstruct cash-basis books.

### Assess Current State

Before entering transactions, determine what already exists:

1. **Check account count** — Does the company file have any accounts beyond system defaults?
2. **Check Opening Balance Equity** — A non-zero balance indicates partial setup was attempted
3. **Find earliest transaction** — Query journal entries, deposits, expenses, and invoices ordered by date ascending to identify what period coverage already exists
4. **Identify gaps** — Compare existing transaction dates against bank statement periods to find months with no recorded activity

This assessment determines the catch-up period boundaries and whether you are starting from zero or filling gaps in partial records.

### Define the Catch-Up Period

The catch-up period runs from the first month with missing records through the current period. Key decisions:

- **Start date**: Day after the last reliable closing (or incorporation date if no books exist)
- **End date**: Current month or the last period needed for an upcoming filing deadline
- **Fiscal year alignment**: Track fiscal year boundaries separately if the entity uses a non-calendar fiscal year (fiscal_year_end_month != 12). Each fiscal year is a discrete unit for closing and tax purposes.
- **Year list**: Enumerate every calendar/fiscal year in the range to plan work sequentially

Work oldest-to-newest within the catch-up period. Each fiscal year should balance independently before moving to the next.

## Entry Strategy Decision

The single most important decision in catch-up bookkeeping: summary or detailed.

### Monthly Summary Approach

One journal entry per month aggregates all activity into category totals.

**Choose when**: Catch-up period exceeds 2 years, source documentation is limited to bank statements only, the goal is tax-filing readiness (not audit), or budget is constrained.

**How it works**: For each month, total deposits by income category and withdrawals by expense category from bank statements. Create a single journal entry dated the last day of the month with one line per category and the bank account as the offset.

**Trade-offs**: Faster execution (minutes per month vs. hours). Higher audit risk — no transaction-level detail. Acceptable for cash-basis tax returns. Not suitable if the client may face IRS examination on specific transactions.

### Detailed Transaction Approach

Enter individual transactions from statements as native accounting entries (deposit entries, expense entries, transfer entries, check payments).

**Choose when**: Catch-up period is under 2 years, audit preparation is required, tax planning requires transaction-level granularity, or the client needs detailed P&L reporting by period.

**How it works**: Classify each bank/credit card line item by transaction type (deposit, withdrawal, transfer, check, fee). Enter each as the appropriate entry type with correct account coding.

**Trade-offs**: Slower but produces a complete audit trail. Each transaction is individually reconcilable. Required for accrual-basis reporting or if payroll detail matters.

### Hybrid Strategy

For multi-year backlogs, combine both approaches:

- **Older periods** (>2 years back): Monthly summary JEs
- **Recent periods** (<2 years): Detailed transaction entry
- **Transition point**: The fiscal year that will appear on the next tax return being filed

This gives tax-ready books for filing years while minimizing effort on statute-expired periods.

## Chart of Accounts Setup

Before entering any transactions, establish the account structure. A catch-up COA needs at minimum:

**Balance Sheet** — Operating Checking, Savings (per actual bank accounts), Undeposited Funds, Accounts Receivable, Fixed Assets with Accumulated Depreciation, Security Deposits, Accounts Payable, Company Credit Card (per actual card), Notes Payable, Owner's Equity, Owner's Draw, Opening Balance Equity

**Income** — Sales Revenue, Service Revenue, Interest Income, Other Income

**COGS** — Cost of Goods Sold (expand if the business has distinct cost categories)

**Expenses** — Advertising, Bank Fees, Insurance, Office Supplies, Professional Services, Rent, Utilities, Payroll Expenses, Travel, Meals, Miscellaneous

Create only accounts that will actually receive postings. Add accounts as needed during transaction entry rather than building an exhaustive structure upfront. Duplicate account names are silently skipped if the account already exists in the system.

Invoke `accounting-foundation:chart-of-accounts` for numbering conventions, Form 1120 tax-line mapping, and C-corp equity account design.

## Opening Balances

Opening balances record account values as of the day before the catch-up period starts. They establish the balance sheet starting point so that catch-up transactions flow correctly.

### When Opening Balances Are Needed

- Starting from a clean company file with no prior data
- Known asset/liability balances exist from prior tax returns or financial statements
- Bank accounts had balances on the catch-up start date

### How to Record

Create a single journal entry dated one day before the catch-up start date:

1. **Debit** asset accounts (Bank, AR, Fixed Assets, Other Assets, Prepaid) for their known balances
2. **Credit** liability accounts (AP, Credit Card, Loans, Accrued Liabilities) for their known balances
3. **Credit** equity accounts (Common Stock, Retained Earnings) for known equity
4. **Opening Balance Equity** absorbs the difference — it is the automatic balancing line

**Normal balance direction by account type**: Asset, Expense, and COGS accounts have normal debit balances. Liability, Equity, and Revenue accounts have normal credit balances. Positive balances follow the normal direction; negative balances reverse it.

### Opening Balance Equity Cleanup

After entering opening balances, the Opening Balance Equity account should hold the net difference. As the catch-up progresses:

- It should trend toward zero as retained earnings from catch-up periods accumulate
- Any residual balance after all catch-up periods are closed indicates a data gap
- Final cleanup: reclassify remaining OBE balance to Retained Earnings with a journal entry and memo explaining the source

## Monthly Summary Journal Entries

For months using the summary approach:

### Process Per Month

1. **Categorize statement lines** — Assign each bank/credit card transaction to an expense or income account
2. **Total by category** — Sum all transactions per account for the month
3. **Create JE** — Date it the last day of the month. Each category becomes one line. The bank account is the offset (credit for net outflows, debit for net inflows).
4. **Private note** — Tag with "Monthly summary for MM/YYYY" for identification

### Category Mapping

When categorizing statement transactions for summaries:

- **Deposits** → Income accounts (Sales Revenue, Service Revenue, Interest Income, Other Income)
- **Withdrawals** → Expense accounts matched by vendor/description pattern
- **Transfers between own accounts** → Exclude from JE (handle as separate transfer entries)
- **Loan payments** → Split: principal to Notes Payable, interest to Interest Expense
- **Payroll** → Payroll Expenses (gross, or split wages/taxes/benefits if detail available)
- **Owner draws** → Owner's Draw equity account, not an expense
- **Uncategorizable** → Miscellaneous expense (flag for client follow-up)

### Validation Per Month

After each monthly summary JE, verify:

- Bank account GL balance matches the ending bank statement balance for that month
- No negative expense account balances (indicates a categorization error)
- Revenue totals are plausible relative to known business activity

## Detailed Transaction Import

For months using the detailed approach:

### Transaction Type Routing

Each bank statement line maps to an accounting entry type:

- **Deposit** (positive amount) → Deposit entry, coded to income account
- **Withdrawal** (negative amount) → Expense entry, coded to expense account
- **Check** (negative, has check number) → Check payment entry with check number reference
- **Fee** (bank/card fee) → Expense entry coded to Bank Fees
- **Transfer** (movement between own accounts) → Transfer entry with from/to account references

### Coding Defaults

When the expense category is unknown, route to Miscellaneous. When the income category is unknown, route to Other Income. Flag these for client review. It is better to enter the transaction with a placeholder category than to skip it — skipped transactions break reconciliation.

### Credit Card Statements

Process credit card statements the same way as bank statements but with the credit card account as the source. Each charge becomes an expense against the credit card; payments from checking become transfers from the bank to the credit card account.

## Reconciliation Approach

After entering all transactions for a given month, reconcile that month before proceeding to the next.

**Per-month reconciliation sequence**:

1. Pull the bank statement ending balance for the month
2. Compare to the GL bank account balance as of the same date
3. Identify and resolve differences (missing transactions, duplicate entries, miscategorized transfers)
4. Mark the month as reconciled
5. Move to the next month

**Multi-account reconciliation**: Reconcile each bank and credit card account independently. A month is not complete until all accounts for that month are reconciled.

Invoke `bookkeeping:reconciliation` for the full reconciliation workflow and variance resolution procedures.

## Quality Gates

### Per-Period Checks

Before marking any catch-up period as complete:

- All bank/credit card accounts reconcile to statements for every month
- Opening Balance Equity trends toward zero (or has a documented, explained balance)
- No orphaned transactions in Uncategorized Income/Expense
- Revenue and expense totals pass reasonableness checks against prior tax filings or known business volume

### Tax-Filing Readiness

A catch-up period is ready for tax filing when:

- All 12 months of the fiscal year are entered and reconciled
- The trial balance balances (debits = credits)
- Income and deductions can be mapped to Form 1120 lines
- Book-tax differences are identified and documented (depreciation, meals, etc.)

### Transition to Ongoing Bookkeeping

Once the catch-up is current:

- Switch from catch-up entry mode to real-time transaction processing
- Establish a monthly close cadence to prevent future backlog
- Set up bank feeds or statement import for ongoing periods

Invoke `bookkeeping:transaction-processing` for day-to-day entry patterns after catch-up is complete.

## Supporting References

Read these for implementation detail and workflow patterns:

- `references/catchup-planning.md` — Assessment and planning phase: source document gathering, company file state evaluation, catch-up period definition, COA setup for catch-up, opening balance journal entry construction. Read for the full account structure template and opening balance creation logic.
- `references/catchup-transaction-entry.md` — Transaction entry phase: monthly summary JE creation, bank statement classification by transaction type, deposit/expense/transfer entry patterns. Read for the detailed workflow of each transaction type and the summary-vs-detailed decision framework.

## Cross-Plugin References

For platform-specific catch-up execution:
- Invoke `qbo-integration:qbo-bookkeeping` for QBO-specific catch-up workflows, bank feed import, and multi-year reconstruction within QBO

For foundational knowledge used during catch-up:
- Invoke `accounting-foundation:chart-of-accounts` for COA design, numbering conventions, and Form 1120 tax-line mapping when building the catch-up account structure

For related bookkeeping workflows:
- Invoke `bookkeeping:reconciliation` for per-period bank reconciliation procedures and variance resolution
- Invoke `bookkeeping:transaction-processing` for standard entry patterns used after catch-up is complete

## Cross-Plugin Consumers

- `tax-prep:form-1120-prep` — Catch-up often directly precedes delinquent-year return preparation
- `tax-prep:tax-planning` — Completed catch-up provides historical data for tax projection
- `financial-planning:budgeting-forecasting` — Reconstructed historical periods feed budget baselines
