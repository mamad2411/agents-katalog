---
name: qbo-reporting
description: >
  Contains verified QBO report endpoint patterns (P&L, Balance Sheet, Cash Flow, GL,
  Trial Balance, A/R and A/P Aging), multi-entity consolidation with combined trial
  balance extraction and ELIM-IC-BAL/ELIM-IC-PL/ELIM-INV elimination entries, and
  investment journal entry templates (BUY/SELL/DIV/INT DocNumber conventions with
  qualified vs ordinary dividend splits). Covers intercompany account identification,
  mirror entry recording, IC balance reconciliation, account mapping to consolidated COA,
  and openpyxl Excel export for audit workpapers. Consult when pulling or parsing any
  QuickBooks Online report, consolidating across multiple QBO company files, recording or
  reconciling intercompany due-to/due-from balances, booking investment purchases sales
  dividends or interest in QBO, generating elimination entries for consolidated
  statements, or exporting QBO data to formatted Excel.
---

# QBO Reporting

QBO-specific report access, consolidation data extraction from multi-entity QBO setups,
intercompany transaction management, and investment accounting within QuickBooks Online.
For GAAP presentation standards that govern how these reports are formatted for external
use, invoke `accounting-foundation:financial-statements`.

## Financial Report Endpoints

Four core financial reports plus analysis reports, all accessed via
`GET /v3/company/{realmId}/reports/{ReportName}`.

- **Profit and Loss** (`/reports/ProfitAndLoss`) — Income statement with revenue,
  expenses, net income. Supports `summarize_column_by` for monthly/quarterly/yearly
  columns. Response groups: `Income`, `Expenses`, `GrossProfit`, `NetIncome`.
- **Balance Sheet** (`/reports/BalanceSheet`) — Point-in-time assets, liabilities,
  equity. Uses `end_date` only (not `start_date`). Response groups: `TotalAssets`,
  `TotalLiabilities`, `TotalEquity`. Always verify the accounting equation
  (Assets = Liabilities + Equity) after parsing.
- **Cash Flow** (`/reports/CashFlow`) — Operating, investing, financing activities.
  Response groups: `NetIncome`, `OperatingActivities`, `InvestingActivities`,
  `FinancingActivities`, `CashIncrease`, `EndingCash`.
- **General Ledger** (`/reports/GeneralLedger`) — All transactions by account. Specify
  `columns` parameter to control payload: `account_name,tx_date,txn_type,doc_num,
  name,memo,subt_nat_amount,rbal_nat_amount`. Filter by `account` (ID) or
  `source_account_type` (e.g., `Bank`).
- **Trial Balance** (`/reports/TrialBalance`) — Account-level debit/credit verification.
  `GrandTotal` group summary provides total debits and credits — verify they match
  (tolerance < $0.01).
- **Account List Detail** (`/reports/AccountListDetail`) — COA metadata. Filter by
  `account_type` (Bank, Income, Expense, etc.) and `account_status` (Deleted,
  Not_Deleted).
- **A/R Aging** (`/reports/AgedReceivables`) and **A/P Aging** (`/reports/AgedPayables`)
  — Receivables and payables aging summaries.

For programmatic API access patterns (auth, pagination, error handling), invoke
`qbo-integration:qbo-api`.

## Common Query Parameters

All report endpoints accept these parameters:

- `start_date` / `end_date` — YYYY-MM-DD format
- `date_macro` — Predefined range (e.g., `This Fiscal Year`, `Last Fiscal Quarter`,
  `This Month-to-date`). Full list includes Today, Yesterday, This/Last/Next Week,
  This/Last Week-to-date, This/Last/Next Month, This/Last Month-to-date,
  This/Last/Next Fiscal Quarter, This/Last Fiscal Quarter-to-date,
  This/Last/Next Fiscal Year, This/Last Fiscal Year-to-date
- `accounting_method` — `Cash` or `Accrual`
- `summarize_column_by` — `Total`, `Month`, `Quarter`, `Year`
- `customer`, `vendor`, `department`, `class` — Comma-separated ID filters
- Always include `minorversion=65` for latest API features

## Report Response Parsing

All QBO reports share a common response structure with three top-level keys:

- **Header** — Report metadata: `ReportName`, `ReportBasis`, `StartPeriod`, `EndPeriod`,
  `Currency`, `SummarizeColumnsBy`. Check `Header.Option` for `NoReportData=true`
  to detect empty reports.
- **Columns** — Column definitions with `ColType` (Account, Money) and `ColTitle`.
- **Rows** — Nested `Row` array. Each row has a `type` (`Section` or `Data`) and
  optional `group` identifier. Sections contain `Header`, nested `Rows`, and `Summary`.
  Data rows contain `ColData` arrays with `value` and optional `id` fields.

Parsing pattern: iterate `Rows.Row`, match on `group` for financial statement sections,
extract amounts from `Summary.ColData[1].value`. For line-item detail, recurse into
nested `Rows.Row` where `type == "Data"`.

## Multi-Period Comparative Reports

Use `summarize_column_by` for intra-year comparisons:

- Monthly P&L: set `start_date`/`end_date` to full year, `summarize_column_by=Month`
- Quarterly P&L: same date range, `summarize_column_by=Quarter`

For year-over-year comparison, fetch separate reports per year and compare parsed
results. The API does not natively support multi-year columns in a single request.

## Report Export to Excel

Export any QBO report to formatted Excel using `openpyxl`:

- Sheet name limited to 31 characters (Excel constraint)
- Write report header (name, period, generation timestamp) in rows 1-3
- Column headers from `Columns.Column` in row 5
- Data rows recursively with indentation tracking via `Alignment(indent=N)`
- Summary/total rows in bold
- Auto-adjust column widths (cap at 50 characters)

This is critical for audit workpaper preparation — always export reports before
they are needed for review.

## Multi-Entity Consolidation

For parent-subsidiary structures where each entity has its own QBO company file.

### Entity and Group Model

Each QBO company in a consolidated group is identified by:

- `realm_id` — QBO company ID (unique per entity)
- `entity_type` — parent, subsidiary, or affiliate
- `ownership_pct` — Ownership percentage (affects NCI calculations)
- `functional_currency` — Default USD

All entities in a group share the same `AuthClient` but require separate `QuickBooks`
client instances, each initialized with the entity's `realm_id`.

### Combined Trial Balance Extraction

Pull all active account balances from each entity and combine into a single dataset.
Each row carries entity identification alongside account data.

- Extract `Account.all()` from each entity's QBO client
- Skip inactive accounts and zero-balance accounts
- Determine debit/credit based on classification: Asset and Expense accounts have
  normal debit balances; Revenue, Liability, and Equity have normal credit balances
- Negative balances reverse the normal side (e.g., negative asset → credit)

### Account Mapping for Consolidation

Map each entity's accounts to a standardized consolidated COA using pattern matching:

- Cash/checking/savings → 1000 Cash and Equivalents
- Accounts receivable → 1200 AR, net
- Property/equipment → 1600 PP&E, net
- Accounts payable → 2000 AP
- Revenue/sales → 4000 Revenue
- Cost of goods/revenue → 5000 Cost of Revenue
- Operating expenses → 6000 Operating Expenses
- Interest expense → 7000 Interest Expense
- Income tax → 8000 Income Tax Expense

Explicit mapping rules override pattern matching. Unmapped accounts fall back to
classification-based defaults (unknown assets → 1900, unknown liabilities → 2700).

For foundational account classification guidance, invoke
`accounting-foundation:chart-of-accounts`.

## Intercompany Transactions

### Account Identification

Intercompany accounts follow naming conventions that enable automated detection:

- **Due to/from** — "Due to [Entity]", "Due from [Entity]", "IC Receivable",
  "IC Payable", "Intercompany Receivable/Payable"
- **Investment** — "Investment in [Subsidiary]", "Subsidiary", "Affiliate"
- **Loan** — "Intercompany Loan", "Loan to/from [Entity]", "Note Receivable/Payable
  Related Party"
- **Revenue/Expense** — "Management Fee", "Intercompany Revenue/Expense", "Royalty"

### Recording Patterns

All intercompany transactions require mirror entries in both entities with matching
`DocNumber` values for traceability.

**Due to/from (management fee example)**:
- Paying entity: Debit Management Fee Expense, Credit Due to Subsidiary
- Receiving entity: Debit Due from Parent, Credit Management Fee Revenue

**Intercompany loan origination**:
- Lender: Debit IC Loan Receivable, Credit Cash
- Borrower: Debit Cash, Credit IC Loan Payable

**Intercompany interest accrual**:
- Lender: Debit Interest Receivable, Credit Interest Income
- Borrower: Debit Interest Expense, Credit Interest Payable

### Reconciliation

For each pair of intercompany accounts, balances must offset to zero across entities.
A receivable in Entity A should equal the corresponding payable in Entity B.

- Pull `CurrentBalance` from both sides of each IC account pair
- For due to/from pairs: `balance_A + balance_B` should equal zero (within $0.01)
- Flag any pair where the difference exceeds threshold as an exception
- Generate reconciliation report with per-pair status (OK vs. EXCEPTION)
- Reconcile monthly — do not defer to year-end

### Elimination Entries

Three standard elimination types for consolidated statements:

**IC Balance Elimination** (ELIM-IC-BAL):
- Debit IC Payable (liability decreases), Credit IC Receivable (asset decreases)
- Removes intercompany receivable/payable from consolidated balance sheet

**IC Revenue/Expense Elimination** (ELIM-IC-PL):
- Debit IC Revenue (revenue decreases), Credit IC Expense (expense decreases)
- Removes intercompany revenue/expense from consolidated income statement

**Investment Elimination** (ELIM-INV):
- Debit Subsidiary Common Stock + Retained Earnings, Credit Investment in Subsidiary
- Removes parent's investment account against subsidiary's equity

Apply eliminations to the combined trial balance by indexing on (entity, account_id),
then calculate consolidated balance as: original balance + elimination debits -
elimination credits.

## Investment Accounting in QBO

### Account Structure

Investment assets, income, and expenses require granular sub-accounts for tax compliance.

**Asset accounts** (by holding period):
- 1300s Short-Term: Equity Securities, Fixed Income, Money Market Funds
- 1500s Long-Term: Equity Investments, Bond Investments, Private Equity/LLC

**Income accounts** (by tax character):
- 4010 Dividend Income — Qualified (lower tax rate under IRC)
- 4020 Dividend Income — Ordinary
- 4100 Interest Income — Taxable
- 4110 Interest Income — Tax-Exempt (municipal bonds)
- 4200/4210 Capital Gains — Short-Term / Long-Term
- 4300 Unrealized Gains (mark-to-market)

**Expense accounts**:
- 5010/5020/5030 Brokerage, Management, Custodian Fees
- 5710/5720 Capital Losses — Short-Term / Long-Term
- 5800 Unrealized Losses

### Journal Entry Patterns

**Stock purchase**: Debit Investment Account (shares x price), Debit Brokerage Fees
(commission), Credit Bank (total cost). DocNumber format: `BUY-{SYMBOL}-{DATE}`.

**Stock sale**: Debit Bank (net proceeds), Debit Brokerage Fees (if any), Credit
Investment Account (cost basis), then Credit Capital Gain or Debit Capital Loss for
the difference. Holding period (short vs. long term) determines the gain/loss account.
DocNumber format: `SELL-{SYMBOL}-{DATE}`.

**Dividend income**: Debit Bank (net of withholding), Debit Tax Withheld (if any),
Credit Qualified Dividend Income, Credit Ordinary Dividend Income. IRS requires
separate tracking for Form 1120 Schedule C (dividends-received deduction).
DocNumber format: `DIV-{SYMBOL}-{DATE}`.

**Interest income**: Debit Bank, Credit Interest Income (taxable or tax-exempt based
on source). Taxable vs. tax-exempt distinction required for Form 1120.
DocNumber format: `INT-{DATE}`.

### Investment Best Practices

- Track cost basis accurately — essential for capital gains on Form 1120
- Separate qualified from ordinary dividends — required for Schedule C DRD computation
- Distinguish short-term (held <= 1 year) from long-term — different tax rates
- Record brokerage fees as separate line items — deductible investment expenses
- Use consistent DocNumber conventions for audit trail

For Form 1120 tax-line mapping of investment accounts, invoke
`tax-prep:form-1120-prep`. For COA design principles underlying investment account
structure, invoke `accounting-foundation:chart-of-accounts`.

## Error Handling

- Check `Header.Option` for `NoReportData=true` on every report response
- HTTP 401 — Authentication failed; refresh the OAuth token
- HTTP 429 — Rate limit exceeded; implement retry with backoff
- Timeout — Large reports (especially GL) may exceed default timeout; use 60-second
  minimum
- Always verify report totals after parsing (TB debits = credits, BS accounting
  equation, P&L sections sum to net income)

## Best Practices

- Cache generated reports to reduce API calls against QBO rate limits
- Specify only needed columns in GL requests to reduce payload size
- Use date macros for standard periods rather than computing dates manually
- Export reports to Excel for audit workpapers before they are needed
- For comparative analysis, use `summarize_column_by` before building multi-request
  year-over-year workflows

## Supporting References

Read these for implementation detail, code examples, and extended patterns:

- `references/reports-financial.md` — Python code for P&L, Balance Sheet, Cash Flow,
  and General Ledger report access and parsing. Read when implementing report extraction
  or when you need the exact response JSON structure and field-level parsing logic.
- `references/reports-analysis.md` — Trial Balance, Account List Detail, A/R and A/P
  aging endpoints, multi-period comparative report construction, Excel export code, and
  error handling patterns. Read when building comparative reports or export workflows.
- `references/consolidation-statements.md` — Combined trial balance extraction from
  multiple QBO entities, consolidated COA mapping rules, and consolidated balance
  sheet/income statement generation code. Read when building consolidation workflows
  from scratch.
- `references/consolidation-intercompany.md` — Entity registry data model, IC account
  identification patterns, mirror journal entry recording, IC balance reconciliation,
  elimination entry construction, and reconciliation Excel export. Read when setting up
  or debugging intercompany workflows.
- `references/investments-accounting.md` — Full investment account hierarchy, journal
  entry code for stock purchase/sale, dividend and interest recording with tax-character
  splits. Read when recording investment transactions or designing investment sub-accounts.

## Cross-Plugin References

For related platform and foundation knowledge:

- Invoke `qbo-integration:qbo-api` for OAuth, pagination, rate limiting, and raw API
  access patterns underlying all report endpoints
- Invoke `qbo-integration:qbo-coa` for QBO-specific account creation, detail types,
  and tax-line mapping within QBO
- Invoke `accounting-foundation:financial-statements` for GAAP presentation standards
  governing how report data is formatted for external financial statements
- Invoke `accounting-foundation:chart-of-accounts` for foundational COA design,
  numbering conventions, and Form 1120 tax-line mapping
- Invoke `accounting-foundation:entity-profile` for corporate entity details that
  affect consolidation group structure

## Cross-Plugin Consumers

- `bookkeeping:monthly-close` — Trial balance verification and report generation
- `tax-prep:form-1120-prep` — Investment income reporting and tax-line mappings
- `financial-planning:budgeting-forecasting` — Comparative P&L data for variance analysis
