---
name: qbo-coa
description: >
  Contains verified 15-AccountType-to-125-DetailType mapping tables with Form 1120
  line-by-line tax mapping, system/protected account restrictions matrix (A/R single-default
  architecture, OBE clearing, Retained Earnings auto-calculation), and full QBO Account
  API CRUD reference with python-quickbooks batch patterns. QBO chart of accounts, account
  type selection, detail type, Prep for Taxes, C-corp equity, holding company COA template,
  CSV JE import account matching. Consult when creating or fixing QBO accounts, choosing
  account type or detail type, mapping accounts to Form 1120 lines, setting up C-corp
  equity (Common Stock, APIC, Treasury Stock, dividends), clearing Opening Balance Equity,
  troubleshooting Retained Earnings behavior, merging or consolidating duplicate accounts,
  hitting the 250-account limit, importing journal entries via CSV or API, diagnosing
  "Line Account Invalid" or "Account Does Not Exist" errors, recording federal income
  tax expense for a C-corp, or batch-creating accounts via the QBO API.
---

# QBO Chart of Accounts

QuickBooks Online implements chart of accounts through a two-level classification system
(Account Type + Detail Type) that controls financial statement placement, Prep for Taxes
auto-mapping, and report structure. This skill covers QBO-specific COA mechanics. For
platform-agnostic COA design principles, GAAP account taxonomy, numbering conventions,
Form 1120 line mapping rationale, and book-tax differences, invoke
`accounting-foundation:chart-of-accounts`.

## QBO Account Type System

QBO has exactly **15 account types** grouped into 5 classifications. Account type is the
most consequential field on any account -- it determines which financial statement section
the account appears in and cannot be changed once subaccounts exist beneath it.

**Asset (Balance Sheet)**
- Bank -- cash and bank accounts (Current Assets)
- Accounts Receivable (A/R) -- invoice-driven receivables (Current Assets)
- Other Current Assets -- prepaids, inventory, undeposited funds, short-term investments
- Fixed Assets -- PP&E, accumulated depreciation, land, leasehold improvements
- Other Assets -- goodwill, intangibles, security deposits, long-term investments

**Liability (Balance Sheet)**
- Accounts Payable (A/P) -- bill-driven payables (Current Liabilities)
- Credit Card -- credit card accounts (Current Liabilities)
- Other Current Liabilities -- payroll liabilities, sales tax, lines of credit, loan payable
- Long Term Liabilities -- notes payable, shareholder notes payable

**Equity (Balance Sheet)**
- Equity -- common stock, preferred stock, APIC, retained earnings, treasury stock, OBE

**Revenue (P&L)**
- Income -- primary revenue, above gross profit line (Form 1120 Lines 1-3)
- Other Income -- non-operating revenue, below operating income (Form 1120 Lines 4-10)

**Expense (P&L)**
- Cost of Goods Sold -- direct costs, reduces gross profit (Form 1120 Schedule A)
- Expenses -- operating expenses (Form 1120 Lines 12-26)
- Other Expense -- depreciation, amortization, penalties, below operating income

### Detail Types (AccountSubType)

Each account type has a fixed set of detail types (~125 API values, ~154 in UI). Detail
types cannot be created, edited, or deleted by users. They are Intuit's invention for
guiding account selection.

**What detail types affect:**
- Prep for Taxes auto-mapping suggestions (primary impact for C-corps)
- How ProConnect/TurboTax categorize accounts during import
- Report filtering by detail type in Account List reports
- QBO's suggested default account during some transaction entry contexts

**What detail types do NOT affect:**
- Transaction posting or journal entry behavior
- Arithmetic calculations in QBO
- Which account type category the account belongs to

Always set the correct detail type even though the immediate financial impact is minimal --
wrong detail types cause Prep for Taxes to auto-map accounts to wrong Form 1120 lines,
creating year-end tax prep rework.

## C-Corp Equity Accounts in QBO

When the tax form is set to Form 1120, QBO suggests C-corp-specific equity detail types.
Required equity accounts for a C-corporation:

- **Common Stock** -- Equity type, detail type CommonStock. Par value of issued shares.
  Must be manually created; not auto-created by QBO.
- **Preferred Stock** -- Equity type, detail type PreferredStock. Only if applicable.
- **Additional Paid-in Capital** -- Equity type, detail type PaidInCapitalOrSurplus.
  Capital received above par value. Must be manually created.
- **Retained Earnings** -- Equity type, detail type RetainedEarnings. Auto-created system
  account. Cannot be deleted or made inactive. QBO auto-calculates this at report runtime
  by rolling prior-year net income; there is no explicit year-end close journal entry. The
  account has no transaction register -- viewing it shows empty, which is expected.
- **Treasury Stock** -- Equity type, detail type TreasuryStock. Contra-equity for
  repurchased shares.
- **Dividends Paid** -- No dedicated C-corp detail type exists. Use detail type
  DividendDisbursed or rename a Partner Distributions account.
- **Opening Balance Equity** -- Auto-created system account. Target state is $0 balance.
  Clear to Common Stock, APIC, or Retained Earnings via journal entry after setup.

Do NOT use the AccumulatedAdjustment detail type -- it is S-Corp specific (Form 1120S
Schedule M-2).

## Corporate Income Tax in QBO

C-corp federal income tax is NOT a deductible business expense on Form 1120. Incorrect
classification is one of the most common C-corp mistakes in QBO.

**Correct two-account pattern:**
- **Federal Income Tax Payable** -- Account Type: Other Current Liabilities, detail type
  FederalIncomeTaxPayable. Record estimated tax payments here as reductions of the
  liability.
- **Federal Income Tax Expense** -- Account Type: Other Expense, detail type
  OtherMiscellaneousExpense (rename to "Federal Income Tax Expense"). Appears below
  operating income on P&L, consistent with GAAP presentation.

If recorded as a regular Expense (with detail type TaxesPaid), it will incorrectly inflate
deductions when tax data is exported to ProConnect and cause Schedule M-1 errors.

Apply the same pattern for state income taxes using StateLocalIncomeTaxPayable.

## Tax Configuration in QBO

### Company Tax Form Setting

Set via Gear > Account and Settings > Advanced > Accounting > Income tax form used. For
C-corps, select "Form 1120 (C Corporation)." This controls:
- Which equity detail types QBO suggests during account creation
- Which tax form Prep for Taxes targets when auto-mapping

**Critical constraint:** Changing the tax form setting after initial setup unmaps ALL
previously assigned tax line associations. Transaction data is unaffected, but all
tax-line linkages must be redone.

### Prep for Taxes (QBOA Only)

QBO does not have Desktop-style per-account tax line mapping. The replacement is "Prep for
Taxes" in QuickBooks Online Accountant, which auto-maps accounts to Form 1120 lines based
on account type and detail type, then exports to ProConnect Tax Online.

**Workflow:** Open QBOA > client file > Prep for Taxes > review auto-mapped assignments >
manually correct unmapped or mis-mapped accounts > export to ProConnect.

**Accounts with unusual or ambiguous detail types require manual review.** Always verify
auto-assignments before exporting. Accounts auto-map correctly only when account type AND
detail type are both correct.

### Form 1120 Line Mapping via QBO Account Types

Key mappings from QBO account types to Form 1120 lines (see
`references/qbo-account-types-tax-mapping.md` for the complete table):

**Income lines:**
- Income / Sales of Product Income, Service/Fee Income > Line 1a (Gross receipts)
- Income / Discounts/Refunds Given > Line 1b (Returns and allowances)
- Other Income / Dividend Income > Line 4
- Other Income / Interest Earned > Line 5
- Other Income / Other Miscellaneous Income > Lines 8, 10

**Deduction lines:**
- Expenses / Payroll Expenses > Line 12 (Officer comp) or Line 13 (Wages) -- requires
  separate accounts for officer vs. staff compensation
- Expenses / Repair & Maintenance > Line 14
- Expenses / Bad Debts > Line 15
- Expenses / Rent or Lease of Buildings > Line 16
- Expenses / Taxes Paid > Line 17
- Expenses / Interest Paid > Line 18
- Expenses / Charitable Contributions > Line 19
- Other Expense / Depreciation > Line 20
- Expenses / various > Line 26 (Other deductions)

**Balance sheet (Schedule L):**
- Bank > Line 1 (Cash)
- Fixed Assets > Lines 8-10 (Depreciable assets, land)
- Other Assets / Intangible Assets, Goodwill > Line 11a
- Long Term Liabilities / ShareholderNotesPayable > Line 17 (Loans from stockholders)
- Equity / CommonStock > Line 21b; PaidInCapitalOrSurplus > Line 22;
  RetainedEarnings > Line 24; TreasuryStock > Line 28

## Special and System Accounts

QBO auto-creates approximately 12 accounts at company setup plus additional accounts when
features are activated. Several cannot be deleted, renamed, or made inactive.

### Permanently Protected Accounts

**Undeposited Funds** -- Other Current Assets. Holding account for payments before bank
deposit. Cannot be deleted or inactivated. Common pitfall: bypassing this account by
recording deposits directly to income overstates income. Balance should be zero after all
payments are deposited; non-zero balance means incomplete deposit recording.

**Retained Earnings** -- Equity. Auto-calculated at report runtime. No transaction
register. Cannot be inactivated. The invisible year-end close transfers prior-year net
income automatically on the first day of the new fiscal year. For prior-period adjustments,
post to a separate equity adjustment account rather than directly to Retained Earnings to
preserve auto-calculation integrity.

**Opening Balance Equity** -- Equity. QBO credits/debits OBE as a placeholder when only one
side of an opening balance is entered. Cannot be deleted. Target: $0 balance. Clear to
appropriate equity accounts (Common Stock, APIC, Retained Earnings) via JE after setup
is complete. A non-zero OBE balance on any balance sheet after setup indicates unresolved
entry errors.

**Unapplied Cash Payment Income / Unapplied Cash Bill Payment Expense** -- System accounts
for cash-basis reporting. Appear when payment dates precede invoice/bill dates. Cannot be
deleted. Journal entries do NOT fix these -- they affect both cash and accrual. The correct
fix is date correction: ensure invoice dates precede payment dates.

**Uncategorized Income / Expense / Asset** -- System catch-alls. Cannot be deleted. Balances
here indicate unclassified bank feed transactions. Must be reclassified before period close.

### Feature-Triggered Accounts

- **Inventory Asset / Cost of Goods Sold / Sales of Product Income** -- created when
  inventory is enabled. Sales of Product Income auto-recreates if deleted.
- **Reconciliation Discrepancies** -- created on first reconciliation adjustment.
- **Sales Tax Payable** -- per tax agency; owned by QBO's sales tax engine.
- **Payroll Liabilities** -- created when payroll is enabled.

### A/R and A/P: Single-Default Architecture

QBO routes ALL invoices to the single default A/R account and ALL bills to the single
default A/P account. Creating additional A/R or A/P accounts does NOT integrate them
into the invoice/bill workflow:
- No dropdown exists on invoices to select alternative A/R accounts
- A/R Aging and A/P Aging reports pull ONLY from the default accounts
- Receive Payment / Bill Pay functions are hardwired to defaults
- JE lines posting to A/R require a Customer name; A/P lines require a Vendor name
- Cannot mix A/R and A/P lines in the same journal entry

**Rule: Use one A/R account and one A/P account.** Use sub-customers, classes, or
locations for dimensional tracking instead of multiple A/R/A/P accounts.

## Common Pitfalls

### Wrong Account Type (Most Dangerous Error)

Account type determines financial statement placement. Wrong type = both statements wrong.
- Expense classified as Income: inflates gross revenue, understates costs
- COGS classified as Expenses: breaks gross profit calculation on Form 1120 Schedule A
- Fixed asset classified as Other Current Assets: asset won't depreciate properly; Form
  1120 Line 20 depreciation deduction will be incorrect
- Asset expensed instead of capitalized: immediate over-deduction, missing future
  depreciation

**Fix difficulty escalates with time.** You can change account type after posting, but
NOT if subaccounts exist beneath the account (error: "Cannot change the type of an account
with subaccounts"). Fix subaccount types first, then the parent.

### Duplicate Accounts

Created via manual entry with slightly different names, CSV re-import, or bank feed
reconnection. Transactions fragment across duplicates, making reports inaccurate.

**Merge is permanent and irreversible.** Before merging: export reconciliation reports as
PDFs. Merge deletes reconciliation reports for the absorbed account. Merge blockers:
connected to online banking, used by a product/service, has subaccounts, mismatched detail
types.

### Accidental Merge via Rename

Renaming an account to exactly match another account's name triggers QBO's merge prompt.
If accepted, the merge is irreversible. Always verify the new name is unique before
renaming.

### Parent/Subaccount Balance Mismatch

Posting to a parent account does NOT update subaccount balances. Posting to subaccounts
rolls up to the parent. Post only to leaf-level subaccounts; never post to parent accounts
directly. Bank feeds cannot connect simultaneously to parent and subaccounts.

### Income vs Other Income Misclassification

Income appears above gross profit on the P&L (Form 1120 Lines 1-3). Other Income appears
below operating income (Form 1120 Lines 4-10). Primary operating revenue must use the
Income type. Non-operating items (interest, dividends, capital gains) use Other Income.
Misclassification distorts gross profit, operating income, and Prep for Taxes auto-mapping.

## Account Numbering in QBO

Account numbers are OFF by default. Enable via Gear > Account and Settings > Advanced >
Chart of Accounts > Enable account numbers. Optionally enable "Show account numbers" for
reports and transactions.

Numbers are informational metadata -- they control sort order and display but do not affect
QBO matching or lookup. The API always matches by account Id, not AcctNum. Numbers are
stored and returned by the API regardless of whether the UI feature is enabled.

**Important for CSV JE import:** account numbers must be disabled before importing journal
entries via CSV, then re-enabled after import. The CSV importer matches by exact account
name string, and enabled account numbers interfere with matching.

## Account Limits

- Simple Start, Essentials, Plus: **250 active accounts** (subaccounts count)
- Advanced: unlimited
- System/default accounts do NOT count toward the limit
- Inactive accounts do NOT count toward the limit
- Maximum subaccount depth: 4 levels below root (5 total including parent)

## Journal Entry Import Account Matching

### CSV Import

**Exact string match only** -- no fuzzy matching, no case-insensitive fallback. The Account
Name column must match the QBO COA entry character-for-character including capitalization,
spacing, and punctuation. Referencing a nonexistent account fails the entire batch with
"Account Does Not Exist."

**Subaccounts in CSV** require `Parent:Child` colon notation with no spaces around the
colon. The native CSV importer has known issues with subaccount posting -- "Line Account
Invalid" errors even when the subaccount exists. Workarounds: temporarily flatten
subaccounts, use the API, or use third-party importers (SaasAnt, Transaction Pro).

**Pre-import checklist:** All referenced accounts exist in QBO COA. Account numbers
disabled. Every JE balances (debits = credits). A/R lines include Customer name; A/P lines
include Vendor name. No negative amounts (use opposite column). Max 1,000 rows per file.

### API Import

The API matches by numeric account Id (`AccountRef.value`), not name. Workflow: query
accounts to resolve names to Ids, then use Ids in JournalEntry line items. The API accepts
subaccount Ids without restriction (no "Line Account Invalid" issue). Accounts must be
pre-created via the Account API before they can be referenced in JEs -- QBO does not
auto-create accounts from JE payloads.

**Rate limits:** 500 requests/minute per realm. Batch API accepts up to 30 operations per
request (counts as 1 API call). A full COA of 100-150 accounts can be created in 3-5 batch
calls with no throttling concern.

## API Account Management

### Account Creation

Minimum required fields: `Name` (max 100 chars, no colons) and `AccountType` (exact enum
string). `AccountSubType` is optional but strongly recommended -- if omitted, QBO assigns
a default.

API `AccountType` strings (case-sensitive): `Bank`, `AccountsReceivable`,
`OtherCurrentAsset`, `FixedAsset`, `OtherAsset`, `AccountsPayable`, `CreditCard`,
`OtherCurrentLiability`, `LongTermLiability`, `Equity`, `Income`, `CostOfGoodsSold`,
`Expense`, `OtherIncome`, `OtherExpense`.

**Note:** The API string is `CostOfGoodsSold` (capital O in "Of") but appears as
`CostofGoodsSold` in some SDK documentation. Verify against the current API reference.

**Name uniqueness:** Names must be unique within the same parent level. Error 6240
("Duplicate Name Exists") on conflict. If an AccountSubType is invalid for the given
AccountType, the API returns "Invalid Enumeration."

### Account Updates

All updates require `Id` and `SyncToken`. Always fetch the current account object before
updating to get the current SyncToken (stale token = conflict error). Use `sparse: true`
for partial updates to avoid nulling out omitted fields.

### Account Merge

**Not supported via API.** Merge is UI-only (accountant view). Both accounts must have
identical AccountType and AccountSubType. Merge is triggered by renaming one account to
match the other. Reconciliation reports for the absorbed account are permanently deleted.

### Deactivation

Set `Active = false`. System accounts (A/R, A/P, Retained Earnings, OBE, Undeposited
Funds) cannot be deactivated. Banking-connected accounts cannot be deactivated until the
connection is removed. Accounts with active subaccounts cannot be deactivated until
subaccounts are deactivated first.

## Holding Company COA Pattern

For investment holding companies structured as C-corps, the COA emphasizes investment
assets and income with minimal operating expenses. Key structural differences from
operating companies:

- Investment accounts split by holding period (short-term as Other Current Asset,
  long-term as Other Asset) and security type (equity vs. fixed income)
- Income accounts under Other Income for dividends (qualified vs. non-qualified),
  interest (taxable vs. tax-exempt), and capital gains (short-term vs. long-term)
- Intercompany accounts (Due from/to Related Parties) for subsidiary transactions
- Minimal expense structure focused on investment fees, professional fees, and
  administrative costs

For foreign-owned corporations (25%+ foreign ownership), add sub-accounts to track
Form 5472 reportable transactions by category. See
`references/coa-holding-company-template.md` for the complete account listing with API
type/subtype values and python-quickbooks code patterns.

## Supporting References

Read these for deeper detail on specific topics:

- `references/qbo-account-types-tax-mapping.md` -- Complete enumeration of all 15 QBO
  account types, ~125 API detail types, and full Form 1120 line-by-line mapping tables
  (income, COGS, deductions, Schedule L). Read when you need the exact detail type for a
  specific Form 1120 line or when verifying Prep for Taxes auto-mapping correctness.

- `references/qbo-official-coa-guidance.md` -- Official Intuit documentation on COA
  structure, default vs custom accounts, account lifecycle (rename, merge, inactivate),
  account limits, naming conventions, and entity-specific account setup. Read when you
  need official Intuit guidance on a specific COA operation or want to cite Intuit's
  recommended approach.

- `references/qbo-special-accounts-behavior.md` -- Deep dive into system account
  mechanics: A/R and A/P default-only architecture, OBE clearing procedures, Retained
  Earnings auto-calculation, Undeposited Funds workflow, unapplied cash payment accounts,
  and the full restrictions matrix. Read when troubleshooting system account behavior or
  planning historical reconstruction workflows.

- `references/qbo-community-coa-pitfalls.md` -- Community-reported problems: account type
  errors, duplicate accounts, merge destruction, rename side effects, parent/subaccount
  imbalances, CSV import failures, negative balance investigation, and the 250-account
  limit. Read when diagnosing a COA problem or advising on error prevention.

- `references/qbo-api-account-management.md` -- Complete API reference for account CRUD:
  all Account entity fields, valid AccountType-to-AccountSubType mappings, create/update/
  deactivate operations, batch API usage, rate limits, name uniqueness rules, and common
  API errors. Read when building or scripting COA operations via the QBO API.

- `references/qbo-je-import-account-matching.md` -- Account matching rules for CSV and
  API journal entry imports: exact string match requirements, subaccount colon notation,
  CSV format rules, A/R/A/P name requirements, field length limits, multi-year historical
  import strategy, and pre-import checklist. Read when planning a JE import or diagnosing
  import failures.

- `references/cpa-qbo-coa-recommendations.md` -- CPA and ProAdvisor best practices:
  consolidation vs. granularity guidance, C-corp-specific account setup for Form 1120,
  Prep for Taxes workflow, account naming conventions, classes vs. sub-accounts decision
  framework, COA templates, and ongoing maintenance recommendations. Read when designing
  a new COA or reviewing an existing one for best-practice alignment.

- `references/coa-holding-company-template.md` -- Complete COA template for C-corp
  holding/investment companies with QBO API type/subtype values, python-quickbooks code
  for account creation and investment transaction recording (purchases, sales with
  gain/loss, dividends), intercompany transaction patterns, and Form 5472 tracking for
  foreign-owned corporations. Read when setting up a holding company or investment entity.

## Cross-Plugin References

For platform-agnostic COA knowledge:
- Invoke `accounting-foundation:chart-of-accounts` for GAAP account type taxonomy,
  numbering conventions (4-digit ranges with gap strategy), hierarchical COA design,
  C-corp equity account structure, Form 1120 tax-line mapping rationale, and book-tax
  difference analysis. That skill covers the conceptual "what and why"; this skill covers
  the QBO-specific "how."

For related QBO integration:
- Invoke `qbo-integration:qbo-api` for general QBO API authentication, connection setup,
  and non-COA API operations
- Invoke `qbo-integration:qbo-reporting` for QBO report configuration that depends on COA
  structure

For downstream consumers:
- `bookkeeping:transaction-processing` uses QBO account classifications for categorization
- `tax-prep:form-1120-prep` uses QBO account-to-tax-line mappings for return preparation
- `tax-prep:tax-planning` uses QBO COA structure for book-tax difference analysis
