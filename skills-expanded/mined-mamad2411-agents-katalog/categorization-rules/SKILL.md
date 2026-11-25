---
name: categorization-rules
description: >
  Contains verified C-corp vendor-to-GL mapping table (13 vendor types with account numbers),
  Form 1120 tax-line expense sub-range assignments (5xxx-9xxx with line numbers), and
  CapEx/OpEx capitalization threshold decision tree. Deductible vs non-deductible classification
  (meals 50% IRC 274, entertainment 0% post-TCJA, penalties IRC 162(f)), operating/investing/financing
  for cash flow, bank feed rule engine logic, split transaction patterns, personal vs business
  separation. Consult when categorizing any transaction to a GL account, asking "what account
  does this go to," fixing a miscategorized charge, deciding whether to expense or capitalize
  a purchase, splitting a multi-category transaction, setting up bank feed auto-categorization
  rules, or separating deductible from non-deductible expenses.
---

# Categorization Rules

Foundation-level knowledge for classifying transactions to GL accounts. Every
journal entry, bank feed item, and expense receipt ultimately needs an account
assignment — this skill provides the decision logic for making that assignment
correctly.

## Account Selection Framework

Transaction categorization starts with two questions: which root type, and which
sub-range within that type.

### Root Type Decision

Every GL account belongs to exactly one of five root types. Selecting the wrong
root type puts the transaction on the wrong financial statement.

- **Asset** (1000–1999) — Resources owned or controlled. Ask: did we acquire
  something of future value? Cash received, equipment purchased, prepaid insurance.
- **Liability** (2000–2999) — Obligations owed. Ask: do we owe someone? AP, accrued
  wages, loan proceeds, unearned revenue.
- **Equity** (3000–3999) — Ownership interest changes. Rarely the target of routine
  categorization — primarily affected by year-end close, dividends, and capital
  transactions.
- **Revenue** (4000–4999) — Inflows from operations. Ask: did we earn income?
  Service fees, product sales, interest earned, rental income.
- **Expense** (5000–9999) — Costs incurred. The most common categorization target.
  Sub-divided into COGS (5xxx), operating expenses (6xxx–7xxx), non-operating
  items (8xxx), and income tax (9xxx).

### Sub-Range Selection

Within expenses (the highest-volume category), the standard C-corp numbering
convention maps to Form 1120 lines:

- 5000–5999 COGS / Cost of Revenue — Direct costs of delivering services or goods
- 6000–6099 Compensation and benefits — Officer comp (Line 12) vs staff wages (Line 13)
- 6100–6199 Rent and occupancy → Form 1120 Line 16
- 6200–6299 Professional fees (legal, accounting, consulting)
- 6300–6399 Insurance
- 6400–6499 Office and administrative
- 6500–6599 Technology and software
- 6600–6699 Marketing and advertising
- 6700–6799 Travel and entertainment — separate deductible meals (50%) from entertainment (0%)
- 6800–6899 Depreciation and amortization → Form 1120 Line 20
- 7000–7099 Utilities
- 7100–7199 Taxes and licenses (non-income) → Form 1120 Line 17
- 7300–7399 Charitable contributions → Form 1120 Line 19 (10% limit)
- 7400–7499 Penalties and fines — non-deductible, triggers M-1 adjustment
- 8000–8099 Interest expense → Form 1120 Line 18
- 8100–8199 Gain/loss on asset disposal

The tax-line mapping matters because items with different tax treatment need
separate accounts. Lumping deductible meals with non-deductible entertainment
into one account creates year-end reclassification work. Separate at the GL level
from the start.

## Vendor-to-Account Mapping Patterns

Most recurring transactions can be mapped by vendor. The pattern: identify the
vendor → assign the default account → apply exceptions for non-standard charges.

### Common Vendor Type Mappings

- **Landlord / property management** → 6100 Rent and occupancy
- **Law firm / CPA firm / consultant** → 6200 Professional fees
- **Insurance carrier** → 6300 Insurance (split GL if multiple policy types)
- **Office supply vendor** → 6400 Office and administrative
- **SaaS / software vendor** → 6500 Technology and software
- **Ad platform / marketing agency** → 6600 Marketing and advertising
- **Airline / hotel / rideshare** → 6700 Travel (not meals — meals need separate account)
- **Restaurant / catering** → 6710 Meals (50% deductible — requires business purpose + attendees per IRC 274)
- **Utility company** → 7000 Utilities
- **Government / tax authority** → 7100 Taxes and licenses (non-income)
- **Subcontractor** → 5200 Subcontractor costs (if directly billable to client)
- **Payroll provider** → mapped via payroll journal entries, not single-account categorization
- **Bank / lender** → 8000 Interest expense (for interest portion; principal is a liability reduction)

### When Vendor Alone Is Insufficient

Some vendors span multiple account categories:
- **Amazon** — could be office supplies (6400), technology (6500), or inventory (1300).
  Categorize by item purchased, not by vendor.
- **Credit card payment** — this is a liability reduction (2200), not an expense.
  The expenses were recorded when individual charges were categorized.
- **Payroll service** — the payroll journal entry splits across wages (6000/6010),
  payroll taxes (6050), benefits (6060), and liability accounts (2500s).
  Never categorize the gross payroll withdrawal as a single expense.
- **Owner/shareholder** — could be officer compensation (6000), shareholder loan
  (2600), or dividend (3500). Requires context about the payment's purpose.

## Rule Engine Logic

Categorization rules follow a condition → action pattern. Conditions evaluate
transaction attributes; actions assign the GL account and optional dimensions.

### Condition Types

- **Direction** — money in (deposit) or money out (withdrawal). Most expenses are
  outflows; revenue is typically inflows.
- **Payee / vendor name** — exact match is safer than partial match. "AT&T" exact
  avoids catching "AT&T Stadium Event" as a phone bill.
- **Description keywords** — the bank's transaction description. Use exact match
  ("PAYROLL") over contains ("PAY") to prevent miscategorization.
- **Amount** — exact, range, greater than, less than. Useful for fixed recurring
  charges (rent is always $X).
- **Combination logic** — AND (all conditions must match) for precision; OR (any
  condition matches) for catching variants of the same vendor.

### Action Components

- **Account** — the GL account (leaf-level, never a group account)
- **Class / department** — cost allocation dimension (if tracking is enabled)
- **Customer / project** — for job costing or project-based billing
- **Split** — multi-line categorization for transactions that span accounts
  (e.g., a $1,200 charge that is $800 software + $400 consulting)

### Priority and Ordering

Rules execute top-to-bottom; first match wins. Design rule sets with:

1. **Most specific rules first** — exact vendor + exact amount catches the known
   recurring charge before a broader rule can grab it
2. **Vendor-specific rules in the middle** — vendor name match with standard account
3. **Broad catch-alls last** — "any outflow containing 'FEE'" as a fallback

Keep the total rule count manageable (under 100–200). Consolidate similar rules.
Remove rules for vendors no longer used. Audit rules quarterly to verify they
still map to active accounts and current vendor names.

### Auto-Categorize Threshold

Auto-categorization (skipping human review) should only be enabled for
transactions that meet all of:
- Fixed recurring amount (rent, fixed-fee subscriptions)
- Single vendor with no ambiguity (not Amazon, not a multi-service vendor)
- Rule has run correctly for 3+ consecutive months with zero errors
- Account assignment has been verified against GL posting requirements

Default to "categorize and manually review" — this pre-fills the account but
keeps the transaction visible for human confirmation.

## Classification Decision Trees

### CapEx vs OpEx

The threshold question: does this expenditure create or extend the life of an
asset, or is it a period cost?

- **Capitalize (Asset 1500s)** if: useful life > 1 year AND cost exceeds the
  entity's capitalization threshold (commonly $2,500–$5,000 for mid-market C-corps)
- **Expense (6xxx–7xxx)** if: consumed within the period, routine maintenance,
  or below capitalization threshold
- **Edge cases**: software licenses — capitalize if multi-year perpetual license;
  expense if annual SaaS subscription. Leasehold improvements — capitalize and
  amortize over shorter of useful life or lease term.

Note: tax treatment may differ from book treatment (Section 179 expensing,
bonus depreciation). The GL categorization follows book/GAAP rules; the tax
difference is handled as a book-tax adjustment at year-end. Keep separate
depreciation expense accounts by asset class if book and tax methods differ.

### Operating vs Investing vs Financing

This classification drives the cash flow statement (ASC 230):

- **Operating** — day-to-day business activities. Revenue receipts, expense
  payments, payroll, rent, supplies, insurance, taxes paid. The vast majority
  of transactions.
- **Investing** — acquiring or disposing of long-term assets. Equipment purchases,
  vehicle purchases, investment securities, loan receivables issued or collected.
- **Financing** — transactions with owners and creditors about the entity's capital
  structure. Loan proceeds, loan principal repayments, stock issuance, dividends
  paid, treasury stock purchases.

### Deductible vs Non-Deductible

Separate at the account level — do not mix in a single account:

- **Meals** (50% deductible) vs **entertainment** (0% deductible post-TCJA) —
  use separate accounts (e.g., 6710 Meals, 6720 Entertainment)
- **Penalties and fines** (non-deductible per IRC §162(f)) → 7400, not lumped
  with other admin expenses
- **Federal income tax expense** → 9000, never deductible
- **Officers' life insurance** (non-deductible if corp is beneficiary) → separate
  from deductible group insurance
- **Political contributions** (non-deductible per IRC §162(e)) → separate account

Items that are non-deductible will require Schedule M-1 or M-3 adjustments at
tax time. If they share an account with deductible items, extracting them
requires manual review of every transaction in that account.

### Personal vs Business

For mixed-use scenarios (common when owner and business share accounts):

- Default action: exclude personal transactions from the books entirely
- If personal charges have business accounting implications (e.g., owner paid
  a business expense from personal funds), record as Owner Draw or Shareholder
  Loan — never categorize personal expenses into business expense accounts
- Long-term fix: maintain separate business and personal banking

## Recurring Transaction Templates

Standard recurring transactions with their expected categorization:

- **Monthly rent** → 6100, fixed amount, same payee — strong auto-categorize candidate
- **Payroll** → split across multiple accounts via payroll journal entry (officer comp 6000, staff wages 6010, payroll taxes 6050, benefits 6060, withholding liabilities 2500s)
- **Monthly SaaS subscriptions** → 6500 Technology, fixed amount per vendor
- **Quarterly insurance premiums** → 6300 Insurance (or prepaid 1400 if policy term crosses fiscal year boundary, then amortize monthly)
- **Monthly loan payments** → split: interest portion to 8000, principal to liability reduction (2600s)
- **Quarterly estimated tax payments** → 9000 Federal / 9100 State income tax
- **Annual professional memberships** → 6400 Office and administrative (or prepaid if material)
- **Credit card statement payment** → 2200 Credit card liability reduction (NOT an expense — the expenses were the individual charges)

## GL Posting Preconditions

A transaction cannot be categorized to just any account. The GL enforces:

- **Leaf accounts only** — group/parent accounts aggregate child balances for
  reporting but never receive direct postings
- **Active accounts only** — frozen or disabled accounts reject postings
  (unless the user has an override role)
- **Correct company** — account must belong to the entity being booked
- **Open period** — posting date must fall within an open accounting period;
  closed periods reject new entries
- **Cost center required for P&L** — expense and revenue accounts require a
  cost center assignment (drives departmental reporting)
- **Party required for Receivable/Payable** — AR (1200) and AP (2000) accounts
  require a customer or vendor party identifier
- **Budget validation** — if budgets are active, posting checks the account +
  cost center combination against budget limits before accepting the entry

If a categorization attempt is rejected, check these preconditions before
assuming the account choice is wrong.

## Supporting References

Read these for deep detail when the synthesized content above isn't sufficient:

- **`references/bank-feed-automation.md`** — Read when setting up or troubleshooting
  bank feed rules. Covers connection methods, auto-matching engine (amount/date/payee
  signals), duplicate handling, disconnection recovery, and multi-account setup.
  Key sections: Bank Rules (rule creation, conditions, actions, priority), Decision
  Points (auto-categorize threshold, mixed-use accounts, duplicate resolution).

- **`references/ccorp-coa-design.md`** — Read when the categorization question is
  really a COA design question ("we don't have an account for X"). Covers the full
  C-corp numbering convention (1xxx–9xxx), hierarchical structure, tax-line mapping
  table, book-tax differences (timing vs permanent), and special account types
  (undeposited funds, suspense, intercompany). Key sections: Numbering Convention,
  Form 1120 Tax-Line Mapping, Book-Tax Differences, COA Design Principles.

- **`references/accounting-system-architecture.md`** — Read when investigating GL posting failures or
  understanding the validation pipeline. Covers the complete GL entry validation
  chain (25+ checks from budget to period closing), journal entry structure,
  payment flow, reconciliation mechanics, and period closing procedures. Key
  sections: GL Entry Validation Rules, General Ledger Engine, Period Closing &
  Fiscal Year, Validation Order (GL Posting).

- **`references/receipt-document-capture.md`** — Read when categorization involves
  receipt or document substantiation. Covers IRS substantiation requirements
  (IRC 274 five-element test for meals), the capture-to-storage workflow,
  OCR matching, and common pitfalls (missing meals substantiation, personal
  expense mixing, duplicate entry). Key sections: IRS Substantiation Requirements,
  Capture-to-Storage Workflow, Common Pitfalls.

## Cross-Plugin Dependencies

- Invoke `accounting-foundation:chart-of-accounts` for COA structure, account type
  taxonomy, and tax-line mapping when the categorization question requires COA
  design changes
- Invoke `bookkeeping:transaction-processing` for platform-specific bank feed rule
  configuration and day-to-day transaction processing workflows
- Invoke `qbo-integration:qbo-coa` for QuickBooks Online account setup, special
  account behaviors, and QBO-specific categorization constraints
