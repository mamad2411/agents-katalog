---
name: ledger-management
description: Maintain the general ledger — chart of accounts design, journal entries, month-end adjustments, account reconciliations, and trial balance production.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, general-ledger, chart-of-accounts, journal-entries, trial-balance, bookkeeping]
related_skills:
  - transaction-processing
  - accounts-payable-management
  - accounts-receivable-management
  - payroll-processing
  - bank-reconciliation
  - monthly-close-process
  - financial-statement-generation
inputs_required:
  - chart-of-accounts
  - transaction-batches
  - bank-feeds
  - prior-period-trial-balance
deliverables:
  - chart-of-accounts
  - trial-balance
  - journal-entry-log
  - reconciliation-reports
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Ledger Management

## Purpose

The general ledger is the single source of truth for every financial transaction. This skill designs and maintains the chart of accounts, records journal entries, performs month-end adjustments, reconciles subledgers, and produces the trial balance. Without it, financial data is fragmented, the trial balance doesn't balance, and financial statements cannot be trusted.

## When to Use

- "Update the general ledger / post these entries"
- "Design / review our chart of accounts"
- "Record this journal entry / adjustment"
- "What accounts do we have?"
- "Reconcile this account"
- "Produce a trial balance"

## Inputs Required

1. **Chart of accounts** — if none exists, build one. If one exists, read it.
2. **Transaction batches** — from `transaction-processing`, `accounts-payable-management`, `accounts-receivable-management`, `payroll-processing`.
3. **Bank feeds** — for cash account reconciliation.
4. **Prior period trial balance** — for opening balances.

## Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| Journal Entry | Balanced debit/credit record for every transaction | DR AR $10k / CR Revenue $10k |
| Trial Balance | Summary of all account balances with debits = credits | Every asset, liability, equity, revenue, expense account |
| Chart of Accounts | Numbered hierarchy of all accounts (1000-9999) | 1000 Cash, 2000 AP, 4000 Revenue, 6000 R&D |
| Accrual Basis | Revenue/expenses recorded when earned/incurred, not when cash moves | Bill in March, collect in April → record revenue in March |
| Account Reconciliation | Matching GL balance to external source (bank, subledger) | Cash GL balance = bank statement balance |
| Materiality Threshold | $500 minimum for adjustments in startups < $1M annual spend | Don't waste time on $200 prepaid amortization |

## Procedure

### 1. Journal Entry Creation

For every transaction, create a balanced journal entry:
- **Date**: transaction date.
- **Description**: concise, searchable (include vendor name, invoice #).
- **Debits = Credits**: ALWAYS. The system should verify this.
- **Supporting reference**: link to invoice, receipt, contract, or approval.

### 2. Common Journal Entry Patterns

**Revenue Recognition (SaaS):**
```
DR  Accounts Receivable         $10,000
  CR Revenue                       $8,333  (earned this month)
  CR Deferred Revenue             $1,667  (unearned)
```

**Prepaid Expense:**
```
DR  Prepaid Software            $12,000
  CR Cash                        $12,000

(each month):
DR  Software Expense             $1,000
  CR Prepaid Software             $1,000
```

**Payroll:**
```
DR  Salary Expense              $50,000
DR  Employer Payroll Tax Exp     $3,825
DR  Benefits Expense             $5,000
  CR Cash                        $41,175  (net pay)
  CR Payroll Tax Payable         $3,825
  CR Benefits Payable            $5,000
```

**Depreciation:**
```
DR  Depreciation Expense        $500
  CR Accumulated Depreciation    $500
```

### 3. Month-End Close Adjustments

At each period end, post:
- Accrued expenses (unbilled services, payroll accrual)
- Deferred revenue amortization
- Prepaid expense amortization
- Depreciation
- Bad debt expense (if not automated)
- Foreign exchange revaluation

Hand off to `monthly-close-process` for the full checklist.

### 4. Account Reconciliation

For every balance sheet account, quarterly:
- **Cash** → reconcile to bank statement (`bank-reconciliation`)
- **AR** → reconcile AR subledger to GL
- **AP** → reconcile AP subledger to GL
- **Prepaid** → amortization schedule vs GL balance
- **Deferred Revenue** → revenue recognition schedule vs GL balance
- **Fixed Assets** → asset register vs GL
- **Debt** → lender statements vs GL

### 5. Trial Balance

Produce a trial balance showing:
- Account number, name
- Beginning balance
- Debits and credits for the period
- Ending balance
- Debit/credit totals must match

## Output Format

- Chart of accounts (Markdown table or CSV)
- Trial balance (Markdown table)
- Journal entry log for the period
- Reconciliation reports for flagged accounts
- Period-over-period flux analysis (> 20% change in any account flagged)

## Done Criteria

The skill is complete when:
1. All journal entries are recorded with balanced debits and credits (debits = credits)
2. Month-end adjustments are posted (accruals, deferrals, depreciation, revaluation)
3. Trial balance is produced with all account balances
4. Balance sheet accounts are reconciled to their subledgers or external sources
5. Period-over-period flux analysis is completed with > 20% changes flagged
6. All entries include supporting references (invoice, contract, approval)

## Pitfalls

- **Posting unbalanced journal entries**: Debits must always equal credits. The system should enforce this, but a manual double-check catches data-entry errors
- **Ignoring accrual basis**: Cash-basis accounting is OK for very early stage but transition to accrual before any serious fundraising or revenue. Investors and auditors expect accrual-basis financials
- **Skipping month-end adjustments**: Missing accrued expenses (unbilled services, payroll accrual) and deferred revenue amortization. These are the most common cause of misstated financials
- **Not reconciling subledgers to GL**: If the AR subledger says $100k but the GL says $95k, you have a problem that compounds every month. Reconcile quarterly at minimum
- **Inconsistent categorization**: Categorizing the same transaction type differently month over month. Once a transaction type is categorized one way, ALWAYS categorize it that way. If a change is needed, document it

## Verification

Does the trial balance balance (total debits = total credits)? Are all balance sheet accounts reconciled to subledgers or external statements? Is the chart of accounts consistently applied across all journal entries? Are month-end adjustments posted for accruals, deferrals, depreciation, and FX revaluation? Is the period-over-period flux analysis complete with all > 20% changes flagged?

## Example

**Example 1: Month-End Close**
> User: "Close the books for March — here are the transaction batches from AP, AR, and payroll"

→ You post the AP batch ($45,200 in vendor invoices), the AR batch ($38,100 in customer invoices), and the payroll batch ($62,400 gross payroll). You post month-end adjustments: $3,500 deferred revenue amortization, $1,200 prepaid software amortization, $800 depreciation, and a $2,100 accrued expense for unbilled legal services. You produce the trial balance ($1.2M total debits = $1.2M total credits), run the reconciliation on cash (matches bank), AR (matches subledger), and AP (matches subledger), and flag a 27% increase in the Software & Subscriptions account from last month for review.

**Example 2: Chart of Accounts Design**
> User: "We're a new startup — design our chart of accounts"

→ You build a complete COA from scratch: Balance Sheet accounts (1000-2999) covering Cash (1010-1030), AR (1100-1120), Prepaids (1200-1230), Fixed Assets (1400-1440), AP (2000-2020), Payroll Liabilities (2100-2130), Deferred Revenue (2410), and Equity (2600-2800). Income Statement accounts (4000-9999) covering Revenue (4000-4200), COGS (5000-5200), R&D (6000-6030), S&M (7000-7040), G&A (8000-8070), and Other Income/Expense (9000-9300). All numbered with gaps for future additions.
