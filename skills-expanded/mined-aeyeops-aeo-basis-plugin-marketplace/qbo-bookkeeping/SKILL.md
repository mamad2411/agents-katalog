---
name: qbo-bookkeeping
description: >
  Contains verified QBO API reconciliation patterns (TrialBalance endpoint queries, OBE
  validation checks, pre-opening transaction detection), multi-year reconstruction workflows
  (summary JE vs transaction-level vs .QBB Desktop conversion), and retained earnings
  mechanics (automatic year-end close, OBE-to-RE clearing, prior-period adjustments).
  Catch-up bookkeeping, historical data entry, bank reconciliation, opening balances,
  period locking, bulk JE import (CSV format, SaaSAnt, Transaction Pro), CPA adjusting
  entries, closing date passwords, sub-account colon notation. Consult when reconstructing
  prior-year books in QBO, entering historical journal entries, reconciling bank statements
  for backlog periods, zeroing out Opening Balance Equity, fixing retained earnings
  mismatches, importing bulk JEs via CSV or API, locking or unlocking closed periods,
  converting QB Desktop backups to QBO, or running post-reconstruction validation checks.
---

# QBO Bookkeeping Operations

QBO-specific procedures for catch-up bookkeeping, multi-year historical reconstruction,
bank reconciliation, and validation. This skill covers the QuickBooks Online platform
mechanics — for platform-agnostic bookkeeping concepts, invoke `bookkeeping:transaction-processing`.

## Reconstruction Method Selection

Choose based on the client scenario. These are mutually exclusive per historical period.

**Option A — Summary JE per period (recommended for closed prior years)**
Post one journal entry per fiscal year (or per month for the most recent year) containing
net debit/credit amounts per account derived from a trial balance. No bank reconciliation
needed — entries go in as final, reconciled amounts. Yields trend-capable P&L and balance
sheet without transaction-level detail.

**Option B — Transaction-level entry (for full-detail reconciliation)**
Import or manually enter individual transactions. Entry order matters to prevent balance
errors: (1) past sales and AR, (2) past vendor bills and AP, (3) bank and credit card
transactions. Reconcile each account month-by-month before advancing. QBO bank feeds only
provide 90 days of downloads — older data requires CSV/QBO file import or manual entry.

**Option C — Convert from QB Desktop backup**
If a prior bookkeeper used QuickBooks Desktop, request the `.QBB` backup file. Restore in
a QB Desktop trial instance, then convert to QBO. Most efficient when the data already exists
in Desktop format.

### Decision Criteria

- Prior system has trial balances but no transaction detail → Option A
- Client needs full audit trail with bank-level reconciliation → Option B
- Data exists in QB Desktop → Option C
- Multiple years of backlog, oldest years have minimal audit risk → Option A for distant years, Option B for recent year(s)

## QBO Setup for Historical Reconstruction

### Company Start Date

Set to the earliest date you intend to enter data. In QBO Simple Start, the start date
chosen during setup cannot be changed — a new company file may be required if the wrong
date was selected.

### Chart of Accounts First

Build the complete COA before entering any transactions or opening balances. All accounts
referenced in journal entries must exist in QBO before import. Invoke
`qbo-integration:qbo-coa` for QBO-specific account creation and detail type requirements.
Invoke `accounting-foundation:chart-of-accounts` for COA design principles and numbering
conventions.

### Account Numbers and Imports

Turn account numbers OFF before importing journal entries via CSV — account numbers cause
import failures. Re-enable after import is complete.

### Sub-Account Format in CSV

Use colon notation with no spaces: `ParentAccount:SubAccount`.

## Opening Balance Handling

### Preferred Method — Journal Entry

Enter the opening balance sheet as a single JE dated on the earliest start date:
- Assets → debit entries
- Liabilities and equity → credit entries
- Contra accounts reverse direction (accumulated depreciation → credit; contra-liabilities → debit)
- Debits must equal credits exactly — no Opening Balance Equity residual

This is preferred because it forces balance and keeps OBE at zero from the start.

### Direct COA Entry (creates OBE — avoid)

Entering opening balances directly in individual account settings auto-creates an Opening
Balance Equity offset. Results in a non-zero OBE that requires cleanup. Accountants
generally discourage this approach.

### Special Account Requirements

- **Accounts Receivable** — Each customer must exist in QBO's customer list before AR balances can be posted
- **Accounts Payable** — Each vendor must exist before AP balances can be posted
- **Inventory** — Import individual items if needed; post totals to OBE temporarily if items are not yet set up
- **Retained Earnings** — Cannot receive a direct opening balance via journal entry (system-generated account); see Retained Earnings Behavior below

## Opening Balance Equity Cleanup

OBE is a temporary clearing account. After setup it must reach $0:

1. Run a trial balance as of the setup date
2. Create a JE: Debit OBE, Credit Retained Earnings (for C-corps) or the appropriate equity account
3. Verify trial balance shows OBE = $0

For C-corporations, OBE clears to Retained Earnings or Paid-in Capital. Leaving OBE
non-zero distorts the balance sheet and raises red flags during tax filing, audits, and
loan applications.

## Retained Earnings Behavior in QBO

This is a critical QBO-specific mechanic that differs from textbook accounting.

### Automatic Year-End Close

QBO does NOT create an actual journal entry at year-end. The close is:
- Calculated at **report time**, not stored as a transaction
- An invisible operation — no register entry, no journal, no audit log line
- Automatic: on the first day of each new fiscal year, QBO adds the prior year's net income to the RE balance on the balance sheet

The Retained Earnings register shows a QuickReport with computed "Closing Entry" line items
per year. These are not clickable transactions — they are calculated values.

### Critical Rule: Never Post Manual RE Closing Entries

Do NOT create a JE to move net income to Retained Earnings at year-end. QBO handles this
automatically. A manual closing JE will **double-count** and corrupt retained earnings
across all subsequent periods.

### Setting an Opening RE Balance

Since QBO blocks direct opening balance entry for RE, use one of these workarounds:

1. **OBE-to-RE JE** — When zeroing out OBE, credit Retained Earnings to transfer accumulated historical equity
2. **Equity adjustment account** — Create a temporary equity account (e.g., "Accumulated Adjustments"), post the historical RE balance there, then zero it out once system-computed RE matches expected
3. **Implied RE through P&L history** — If all historical P&L JEs are entered correctly per year, QBO will auto-compute the correct RE without any manual RE entry

### Verifying RE Is Correct

Run P&L for the full date range (company inception to present). Sum all net income figures.
That total should equal the Retained Earnings balance on the balance sheet.

### Prior-Period RE Corrections

If a previously filed tax year needs an RE correction:
- Do NOT edit historical transactions (distorts filed return data)
- Post a Retained Earnings adjustment JE in the current year or first day of the year following the erroneous year
- This is the standard "prior period adjustment" approach

## Period Locking

### Setting the Closing Date

Gear > Account and Settings > Advanced > Accounting > "Close the books" (toggle on). Set a
closing date and optionally a password. Any attempt to create or edit a transaction on or
before the closing date will warn the user or require the password.

### Recommended Locking Protocol

After completing each year in a historical reconstruction:
1. Verify all JEs are entered and reconciled for that year
2. Run P&L and Balance Sheet — verify against source documents
3. Post CPA adjusting journal entries if needed
4. Export/save reconciliation reports and trial balance as PDFs
5. Set closing date to December 31 of that year with a password
6. Lock before moving to the next year

Setting a closing date does NOT trigger any year-end close — the automatic RE close is
driven purely by the fiscal year boundary and happens at report time regardless of locking.

### Unlocking for CPA Adjusting Entries

The only valid reason to unlock a closed period after tax filing: entering CPA adjusting
journal entries. Temporarily clear the closing date, enter the AJEs, then re-lock.

## Bulk Journal Entry Import

### Native QBO CSV Import

The native CSV JE import is **unavailable in the US version of QBO** (available in
Canada/UK). It may be accessible in QBO Advanced or QBO Accountant, but availability is
inconsistent.

When available (Settings > Import Data > Journal Entries):
- Format: CSV with headers — Journal Date, Ref Number (Journal No.), Account Name, Debit, Credit, Description/Memo
- All lines of one JE must share the same Ref Number
- Limit: 1,000 rows per file
- Account names must exactly match existing COA (case-sensitive in some versions)
- Turn off account numbers before importing
- Sub-accounts use `ParentAccount:SubAccount` format

### QBO API for Bulk Import

The QBO Accounting API supports back-dated journal entries via the `TxnDate` field (defaults
to server date if omitted). Rate limits: 500 requests/minute per realm ID, 10 concurrent
requests, 40 batch operations/minute, HTTP 429 on exceed. For API patterns and
implementation, invoke `qbo-integration:qbo-api`.

### Third-Party Import Tools

- **SaaSAnt Transactions** — Supports Excel, CSV, IIF; handles bulk imports; good for large-scale migrations
- **Transaction Pro Importer** — Frequently recommended in QBO community for bulk JE imports

## Bank Reconciliation Workflow

### Monthly Reconciliation Process

For each bank/credit card account, each month:
1. Obtain the bank statement ending balance for the period
2. Pull the QBO trial balance as of the same period end date
3. Compare the QBO account balance to the statement balance
4. Identify and resolve any differences (unmatched transactions, timing items)
5. Mark reconciled when the difference is less than $0.01

### Reconciliation via QBO API

Bank reconciliation verification can be performed programmatically by querying the
TrialBalance report endpoint with a custom date range and comparing account balances
against statement data. See the reference file for the full API pattern including
report parsing logic.

### Key Rules

- Work chronologically — start with the earliest period, complete before moving forward
- Reconcile monthly — do not batch-enter an entire year and reconcile at year-end
- For summary JE imports (Option A), bank reconciliation is not applicable — the amounts are pre-reconciled
- Accounts linked to bank feeds cannot be merged; save reconciliation PDFs before any account merges

## Validation Checks

Run after completing catch-up bookkeeping for each period:

1. **Opening Balance Equity = $0** — Query the OBE account balance; any non-zero amount indicates incomplete setup
2. **Trial balance balanced** — Total debits must equal total credits (difference < $0.01)
3. **No pre-opening transactions** — Query JournalEntry records dated before the opening date; count should be zero
4. **AR/AP aging matches GL** — Aging report totals should tie to the general ledger balances
5. **Undeposited Funds = $0 or explained** — Any balance requires investigation
6. **Retained Earnings = sum of historical net income** — Run P&L from inception to verify

For API-based validation patterns (querying OBE, running trial balance reports, checking
transaction dates programmatically), see the catchup-reconciliation reference file.

## Year-by-Year Reconstruction Workflow

Complete CPA-reviewed workflow for historical catch-up:

### Pre-Work
- Collect all bank/credit card/loan statements (PDF or CSV) for the backlog period
- Gather prior reconciliation records, trial balances, and AR/AP aging reports
- Identify connected app payout schedules (payment processors, e-commerce platforms)

### Per-Year Process
1. Build or verify the COA covers all accounts needed for the year
2. Post opening balance JE for the first year being reconstructed (balance sheet as of start date)
3. Post P&L JEs for each month (or one annual JE for distant years)
4. For transaction-level reconstructions: reconcile each bank/CC account to statements, month by month
5. Verify P&L and Balance Sheet tie to source documents
6. Post CPA adjusting entries (depreciation, accruals, prepaids)
7. Export/save reconciliation reports and trial balance as PDFs
8. Set closing date for December 31 of that year
9. Advance to next year

### Post-Reconstruction Checks
- AR and AP aging reports match the general ledger
- Undeposited Funds balance is zero or explained
- Balance sheet retained earnings matches sum of all historical net income

### Documentation Protocol
- Monthly folders: statements, reconciliation exports, workpapers
- Memo attached to every adjusting JE linking to source document
- Master checklist tracking status per account per month

## COA Evolution Over Multiple Years

When reconstructing books that span COA changes:

- **Stability principle** — Do not change the COA once a good one is set up; add new accounts rather than modifying existing ones
- **Renaming** — Retroactively changes the name on all historical reports; useful for minor corrections, confusing for material changes
- **Merging** — Irreversible; transaction history moves to the keeper account; save reconciliation PDFs first; accounts linked to bank feeds cannot be merged
- **Sub-account strategy** — Making old accounts sub-accounts of new parents fixes collapsed report views but retroactively alters historical financial statement structure

For full COA design guidance, invoke `accounting-foundation:chart-of-accounts`. For
QBO-specific account operations, invoke `qbo-integration:qbo-coa`.

## Common Pitfalls

1. **Manually posting RE closing entries** — QBO auto-closes at report time; manual entries double-count
2. **Non-zero Opening Balance Equity after setup** — Distorts balance sheet; always zero out to appropriate equity account
3. **Back-dating entries after filing** — Affects current balance sheet (running total from day one); post current-year adjustments instead
4. **Merging accounts destroys reconciliation history** — Irreversible; save reconciliation reports as PDFs before merging
5. **Advancing without monthly reconciliation** — Compounding errors make it impossible to isolate discrepancies
6. **Importing against non-existent COA accounts** — CSV imports fail silently or error when account names don't match exactly

## QBO Accountant Features

- **Working Trial Balance** — Available only in QBO Accountant (not standard QBO); shows opening and closing balances per period; critical for year-by-year verification
- **Adjusting Journal Entry flag** — Marks JEs as AJEs in reports, visually distinguishing CPA entries from operating entries
- **Prep for Taxes** — Maps QBO accounts to Form 1120 lines and exports to ProConnect for tax return preparation

## IRS Audit Considerations

- QBO maintains an audit trail logging all changes including back-dated entries
- Attach source document memos to every JE for a defensible paper trail
- For historical reconstructions, the audit trail will show entry timestamps that postdate the transaction dates — this is expected and defensible when properly documented

## Cross-Plugin References

- Invoke `qbo-integration:qbo-api` for API patterns, rate limits, and programmatic operations
- Invoke `qbo-integration:qbo-coa` for QBO account creation, detail types, and tax-line mapping within QBO
- Invoke `qbo-integration:qbo-reporting` for QBO report generation and export
- Invoke `accounting-foundation:chart-of-accounts` for COA design principles and numbering conventions
- Invoke `accounting-foundation:categorization-rules` for transaction-to-account routing logic
- Invoke `bookkeeping:transaction-processing` for platform-agnostic bookkeeping concepts

## Supporting References

Read these for implementation-level detail:

- `references/catchup-reconciliation.md` — Python code patterns for QBO API-based bank reconciliation, year-end closing entry generation, and validation checks (OBE balance, trial balance, pre-opening transaction detection). Read when implementing automated reconciliation or building validation scripts against the QBO API.
- `references/qbo-multi-year-reconstruction.md` — Comprehensive knowledge base covering reconstruction method selection, opening balance handling, retained earnings behavior, period locking, bulk JE import mechanics, COA evolution, and common pitfalls with sourced citations. Read when planning or executing a multi-year historical reconstruction engagement.
