---
name: financial-statement-generation
description: Generates the three core financial statements — P&L (income statement), balance sheet, and cash flow statement — with proper formatting, classifications, and period-over-period comparisons. Use when the user mentions financial statement generation, producing a P&L, creating a balance sheet, formatting a cash flow statement, or asks about consolidated financials.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, financial-statements, profit-and-loss, balance-sheet, cash-flow]
related_skills: [monthly-close-process, board-reporting, audit-preparation, cash-forecasting]
inputs_required: [general-ledger-trial-balance-post-close, prior-period-financial-statements, chart-of-accounts-with-classification, revenue-recognition-schedule, fixed-asset-register, debt-amortization-schedules, equity-rollforward]
deliverables: [profit-and-loss-statement, balance-sheet, cash-flow-statement, summary-kpi-dashboard, flagged-items-report]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Financial Statement Generation

Produce the three core financial statements from the general ledger. Format them for management, board, and investor consumption. Goal: anyone can pick up these statements and understand the company's financial health in under 60 seconds.

## Purpose

Financial statements are the primary communication tool for the company's financial health — used by the CEO for decisions, the board for oversight, investors for diligence, and auditors for assurance. This skill transforms a closed trial balance into clear, well-formatted statements with period-over-period comparisons and the KPIs that matter. Without this skill, raw data stays in the accounting system where nobody can act on it.

## When to Use

- "Generate the P&L / income statement"
- "Produce the balance sheet"
- "Create a cash flow statement"
- "Give me the financial statements for [period]"
- "Format our financials for the board"
- "Consolidated financial statements"

## Inputs Required

- General ledger trial balance (balanced, post-month-end-close)
- Prior period financial statements for comparison
- Chart of accounts with proper departmental and functional classification
- Revenue recognition schedule (deferred revenue rollforward)
- Fixed asset register and depreciation schedule
- Debt amortization schedules
- Equity rollforward and cap table
- Board/investor formatting preferences (KPIs to highlight)

## Quick Reference

| Statement | What It Shows | Key Check |
|-----------|---------------|-----------|
| P&L (Income Statement) | Revenue, costs, and profit over a period | Include % of revenue and prior period comparison |
| Balance Sheet | Assets, liabilities, and equity at a point in time | Assets = Liabilities + Equity |
| Cash Flow Statement | Sources and uses of cash over a period | Ending cash = balance sheet cash |
| EBITDA | Operating Income + Depreciation + Amortization | Proxy for operating cash flow |
| Net Burn | Net Income (if negative) | Cash consumption rate |

## Procedure

1. Complete the monthly close (`monthly-close-process`).
2. Generate the P&L from the income statement accounts.
3. Calculate the balance sheet from the ending trial balance.
4. Derive the cash flow statement (P&L + BS changes = CF).
5. Verify: ending cash on CF = cash on BS.
6. Add period-over-period comparisons and % calculations.
7. Add KPI summary at the top (revenue, gross margin, EBITDA, net income, cash, burn).

### 1. Income Statement (P&L)

Format: monthly or quarterly columns, with % of revenue where useful.

```
[Company Name]
Income Statement
For the [Month/Quarter/Year] Ended [Date]
(USD, Accrual Basis)

                                     Current Month     % of Rev     Prior Month     % of Rev     YoY (Same Month)
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
REVENUE
  Subscription Revenue                  $380,000         88%          $350,000         89%          $210,000
  Professional Services                  $50,000         12%           $45,000         11%           $30,000
TOTAL REVENUE                          $430,000        100%          $395,000        100%          $240,000

COST OF REVENUE
  Hosting & Infrastructure               $38,000          9%           $35,000          9%           $22,000
  Payment Processing Fees                $12,900          3%           $11,850          3%            $7,200
  Customer Support                       $25,000          6%           $24,000          6%           $18,000
TOTAL COST OF REVENUE                   $75,900         18%           $70,850         18%           $47,200

GROSS PROFIT                           $354,100         82%          $324,150         82%          $192,800

OPERATING EXPENSES
  Research & Development
    Engineering Salaries                $145,000         34%          $140,000         35%           $95,000
    Cloud Infrastructure (Dev)           $22,000          5%           $20,000          5%           $14,000
    Engineering Tools                     $8,000          2%            $7,500          2%            $5,000
    Total R&D                           $175,000         41%          $167,500         43%          $114,000

  Sales & Marketing
    Sales Salaries + Commissions         $82,000         19%           $78,000         20%           $52,000
    Marketing Salaries                   $38,000          9%           $37,000          9%           $25,000
    Advertising & Promotion              $25,000          6%           $20,000          5%            $8,000
    Total S&M                           $145,000         34%          $135,000         34%           $85,000

  General & Administrative
    Executive Salaries                   $45,000         10%           $44,000         11%           $30,000
    Finance & Accounting                  $8,000          2%            $7,500          2%            $5,000
    Legal                                $12,000          3%             $500           0%            $3,000
    Office & Facilities                   $6,000          1%            $6,000          2%            $4,000
    Insurance                             $4,000          1%            $4,000          1%            $2,000
    Other G&A                             $5,000          1%            $4,000          1%            $3,000
    Total G&A                            $80,000         19%           $66,000         17%           $47,000

TOTAL OPERATING EXPENSES               $400,000         93%          $368,500         94%          $246,000

OPERATING INCOME (LOSS)               ($45,900)       −11%         ($44,350)       −11%         ($53,200)

OTHER INCOME / EXPENSE
  Interest Income                         $8,500          2%            $8,200          2%            $1,200
  Interest Expense                      ($3,000)        −1%          ($3,000)        −1%               $0
  Other                                    ($200)         0%               $0           0%               $0

NET INCOME (LOSS)                     ($40,600)        −9%         ($39,150)       −10%         ($52,000)
```

Key metrics below the P&L:
- EBITDA = Operating Income + Depreciation + Amortization
- Net Burn = Net Income (if negative)
- Gross Burn = Total Operating Expenses + COGS (excluding revenue-linked costs)

### 2. Balance Sheet

```
[Company Name]
Balance Sheet
As of [Date]
(USD)

ASSETS                                                  Current          Prior Month-End
────────────────────────────────────────────────────────────────────────────────────────
CURRENT ASSETS
  Cash & Cash Equivalents                            $2,847,000           $2,861,200
  Accounts Receivable (net)                            $245,000             $230,000
  Prepaid Expenses                                      $48,000              $44,000
  Other Current Assets                                   $6,500               $6,500
TOTAL CURRENT ASSETS                                 $3,146,500           $3,141,700

NON-CURRENT ASSETS
  Property & Equipment (net)                            $65,000              $67,000
  Security Deposits                                     $15,000              $15,000
  Other Assets                                               $0                   $0
TOTAL NON-CURRENT ASSETS                                $80,000              $82,000

TOTAL ASSETS                                         $3,226,500           $3,223,700

LIABILITIES & EQUITY
────────────────────────────────────────────────────────────────────────────────────────
CURRENT LIABILITIES
  Accounts Payable                                      $68,000              $72,000
  Accrued Expenses                                      $42,000              $38,000
  Payroll Tax Payable                                   $18,500              $17,200
  Deferred Revenue (current)                           $185,000             $192,000
  Credit Cards Payable                                  $12,000              $15,000
TOTAL CURRENT LIABILITIES                              $325,500             $334,200

LONG-TERM LIABILITIES
  Convertible Notes                                   $500,000             $500,000
  Venture Debt                                        $250,000             $250,000
  Deferred Revenue (long-term)                         $80,000              $85,000
TOTAL LONG-TERM LIABILITIES                           $830,000             $835,000

TOTAL LIABILITIES                                    $1,155,500           $1,169,200

EQUITY
  Common Stock                                           $1,000               $1,000
  Preferred Stock                                      $500,000             $500,000
  Additional Paid-In Capital                         $4,500,000           $4,500,000
  SAFE Instruments (equity-classified)                $300,000             $300,000
  Accumulated Deficit                              ($3,230,000)         ($3,246,500)
TOTAL EQUITY                                         $2,071,000           $2,054,500

TOTAL LIABILITIES & EQUITY                           $3,226,500           $3,223,700

Check: Assets = Liabilities + Equity ✓
```

### 3. Cash Flow Statement

Use the **indirect method** (start from net income, adjust for non-cash items):

```
[Company Name]
Statement of Cash Flows
For the [Period] Ended [Date]
(USD)

CASH FLOWS FROM OPERATING ACTIVITIES
  Net Income (Loss)                                  ($40,600)
  Adjustments to reconcile net income:
    Depreciation & Amortization                        $3,500
    Bad Debt Expense                                    $1,200
    Non-cash Interest (SAFE/Note accretion)             $1,500
  Changes in working capital:
    (Increase) / Decrease in AR                      ($15,000)
    (Increase) / Decrease in Prepaid                  ($4,000)
    Increase / (Decrease) in AP                       ($4,000)
    Increase / (Decrease) in Accrued Expenses           $4,000
    Increase / (Decrease) in Deferred Revenue         ($12,000)
    Increase / (Decrease) in Payroll Tax Payable        $1,300
NET CASH PROVIDED BY (USED IN) OPERATING             ($64,100)

CASH FLOWS FROM INVESTING ACTIVITIES
  Purchase of Equipment                               ($1,500)
NET CASH USED IN INVESTING                            ($1,500)

CASH FLOWS FROM FINANCING ACTIVITIES
  Proceeds from Stock Option Exercises                 $16,500
  SAFE Issuance Proceeds                                    $0
  Repayment of Venture Debt                           ($5,000)
NET CASH PROVIDED BY FINANCING                        $11,500

NET CHANGE IN CASH                                   ($54,100)

Cash at Beginning of Period                        $2,861,200
Cash at End of Period                              $2,807,100

SUPPLEMENTAL DISCLOSURES:
  Interest Paid                                         $3,000
  Income Taxes Paid                                         $0
```

## Output Format

- P&L (current period + prior period + YoY comparison)
- Balance sheet (current + prior period-end)
- Cash flow statement
- Summary KPI dashboard
- Flagged items: unusual balances, large swings, negative accounts

## Done Criteria

The skill is complete when:
1. All three statements (P&L, Balance Sheet, Cash Flow) are generated from a closed trial balance.
2. Period-over-period comparisons (prior month, YoY) are included with variance percentages.
3. % of revenue is shown on the P&L for every line item.
4. Ending cash on the cash flow statement ties to cash on the balance sheet.
5. KPI summary (revenue, gross margin, EBITDA, net income, cash, burn) is included.
6. Any unusual items are flagged for review.

## Pitfalls

- **Generating statements before the close is complete**: drafting financials from an unreconciled trial balance means the numbers will change. Wait until the close checklist is signed off.
- **Omitting % of revenue from the P&L**: raw dollar amounts without ratio context mislead readers. A $50k legal line item at $5M revenue vs $500k revenue tells entirely different stories.
- **Using different classification logic across periods**: moving expenses between departments or between COGS and OpEx without restating prior periods destroys comparability.
- **Forgetting to verify the cash flow ties to the balance sheet**: a cash flow statement whose ending cash doesn't match the balance sheet is invalid. This is the single most common error in manual preparation.
- **Presenting non-GAAP metrics without reconciliation**: if you show EBITDA or Adjusted Revenue, always include a reconciliation back to GAAP net income. Skipping this invites auditor questions and investor skepticism.

### Heuristics

- **Always include % of revenue on the P&L**: context is everything. $100k in legal spend means something very different at $500k revenue vs $5M revenue.
- **Always include prior period comparisons**: a single month in isolation is useless.
- **Cash flow statement is the truth-teller**: a company with great P&L but terrible cash flow is in trouble. The cash flow statement reveals it.
- **Balance sheet must balance**: sounds obvious, but this is the #1 error in manually prepared statements.
- **Accrual basis, always**: cash-basis statements have their place, but label them clearly as such.

### Edge Cases

- **Consolidated statements** (parent + subsidiaries): eliminate intercompany transactions and balances.
- **Multi-currency**: translate foreign subs at the period-end rate for BS, average rate for P&L. Put FX translation adjustments in Other Comprehensive Income.
- **Comparative periods for new companies**: if the company is < 12 months old, just show "since inception" or monthly from month 1.

## Verification

Does the cash flow statement's ending cash balance match the balance sheet? Does every line on the P&L have a % of revenue? Can someone pick up this package and understand the company's financial health in under 60 seconds? If not, the statements need more work.

## Example

1. "Generate the quarterly financial statements for Q1 2026 — P&L, balance sheet, and cash flow statement with YoY comparisons."
2. "We have two subsidiaries in different currencies. Produce consolidated financial statements with proper FX translation."
3. "Format our financials for the board deck — include % of revenue, prior quarter comparisons, and a KPI summary at the top."

## Linked Skills

- Close the books first → `monthly-close-process`
- Format for board → `board-reporting`
- Audit support → `audit-preparation`
- Cash forecast tie-in → `cash-forecasting`
