---
name: monthly-close-process
description: Runs the full month-end close process end-to-end, including revenue recognition, accruals, reconciliations, journal entries, and the financial close checklist. Use when the user mentions month-end close, closing the books, revenue recognition, posting month-end accruals, or asks about running the close checklist.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, month-end-close, revenue-recognition, accruals, reconciliation]
related_skills: [financial-statement-generation, audit-preparation, internal-controls-design]
inputs_required: [general-ledger-trial-balance, bank-and-credit-card-statements, ar-and-ap-subledger-reports, payroll-register, revenue-contracts-and-deferred-revenue-schedule, prepaid-and-fixed-asset-schedules]
deliverables: [completed-close-checklist, balanced-trial-balance, flux-analysis-with-commentary, revenue-recognition-summary, deferred-revenue-rollforward]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Monthly Close Process

Run the full month-end close — the disciplined process that turns a month of transactions into reliable financial statements. Handle revenue recognition, accruals, reconciliations, adjustments, and the close checklist. Goal: the books are closed within 5-10 business days of month-end, every month.

## Purpose

The month-end close is the heartbeat of financial operations. Without a disciplined, repeatable close process, financial statements are unreliable, decisions are made on stale or wrong data, and audits become nightmares. This skill provides the step-by-step workflow, accrual methodologies, and close checklist needed to produce reliable financials on a predictable schedule every single month.

## When to Use

- "Run month-end close"
- "Close the books for [month]"
- "Revenue recognition for the month"
- "Post month-end accruals"
- "Month-end reconciliation checklist"
- "Are we ready to close?"

## Inputs Required

- General ledger trial balance as of month-end
- Bank and credit card statements for all accounts
- AR and AP subledger reports
- Payroll register for the month
- Active revenue contracts and deferred revenue schedule
- Prepaid expense and fixed asset schedules
- Prior month's close package for flux comparison

## Quick Reference

| Close Phase | Days | Key Tasks |
|-------------|------|-----------|
| Transaction Cutoff & Subledger Close | 1-3 | Bank rec, AR/AP reconciliation, payroll verification |
| Revenue Recognition | 3-5 | Deferred revenue schedule, adjusting entries |
| Accruals & Adjustments | 5-7 | Unbilled AP, payroll accrual, prepaids, depreciation, bad debt |
| Review & Analysis | 7-8 | Trial balance review, flux analysis, balance sheet tie-out |
| Statement Preparation | 8-10 | Hand off to financial-statement-generation |

| Accrual Type | Calculation | Example |
|---|---|---|
| Unbilled AP | Services received, no invoice yet | Legal work done in March, bill in April |
| Payroll accrual | Days worked but paid next month | (Monthly payroll / working days) × days between pay date and month-end |
| Prepaid amortization | Total prepaid / months of coverage | 12-month policy = 1/12 per month |
| Depreciation | Asset cost / useful life (months) | Straight-line |

## Procedure

### Day 1-3: Transaction Cutoff & Subledger Close

| Task | Owner | Dependency |
|---|---|---|
| Stop processing new AP invoices for the month | AP | — |
| Stop processing new AR invoices for the month | AR | — |
| Reconcile all bank accounts to GL | Treasury | Bank statements |
| Reconcile all credit cards to GL | Treasury | Card statements |
| Reconcile AR subledger to GL | AR | Payments matched |
| Reconcile AP subledger to GL | AP | Invoices entered |
| Verify payroll entries match pay stubs | Payroll | Payroll register |

### Day 3-5: Revenue Recognition

For SaaS businesses, the critical month-end step:

```
1. Identify all revenue contracts active during the month.
2. Calculate recognized revenue:
   - Subscription: (Total contract value / contract months) × months elapsed this period
   - Usage-based: actual usage × contracted rate
   - Professional services: % of completion or upon delivery
3. Post adjusting entries:
   DR Deferred Revenue, CR Revenue (for amounts earned this period)
   DR Revenue, CR Deferred Revenue (for amounts collected but not yet earned)
4. Reconcile deferred revenue balance = sum of remaining unrecognized amounts across all contracts.
```

### Day 5-7: Accruals & Adjustments

| Accrual Type | How to Calculate | Example |
|---|---|---|
| **Unbilled AP** | Services received but no invoice yet (e.g., lawyer worked in March, bills in April) | Estimate from hourly logs or contract |
| **Payroll accrual** | Days worked in the month but paid next month | (Monthly payroll / working days) × days between last pay date and month-end |
| **Accrued vacation / PTO** | Unused PTO days × daily rate | Only if the company's policy pays out unused PTO |
| **Commissions accrual** | Deals closed this month × commission rate | Even if commission is paid next month |
| **Bonus accrual** | Pro-rata share of expected annual bonus | If bonuses are formulaic |
| **Prepaid amortization** | Total prepaid / months of coverage = monthly amortization | 12-month insurance policy = 1/12 per month |
| **Depreciation** | Asset cost / useful life (months) = monthly depreciation | Straight-line unless a better method applies |
| **Bad debt expense** | Aging-based: 1% of AR 0-30 days, 5% of 31-60, 20% of 61-90, 50% of 90+ | Update the allowance account |

### Day 7-8: Review & Analysis

Before declaring close complete:

1. **Trial balance review**: all accounts have reasonable balances. No negative balances where unexpected.
2. **Flux analysis**: every P&L line item vs prior month and vs same month last year. Flag changes > 20% or > $10k.
3. **Balance sheet tie-out**: cash = bank, AR = subledger, AP = subledger, deferred revenue = schedule.
4. **Gross margin check**: within 2% of expected range. If not, investigate COGS or revenue classification.
5. **Headcount check**: GL payroll expense / number of employees = reasonable average cost per employee.

### Day 8-10: Financial Statement Preparation

Hand off to `financial-statement-generation` for P&L, balance sheet, and cash flow statement production.

### Close Checklist

```
=== MONTH-END CLOSE CHECKLIST ===

📥 CASH & BANK
  [ ] All bank accounts reconciled
  [ ] All credit cards reconciled
  [ ] Stripe/PayPal balance confirmed
  [ ] Outstanding checks > 60 days investigated
  [ ] Bank fees recorded

📥 ACCOUNTS RECEIVABLE
  [ ] AR subledger ties to GL
  [ ] All invoices issued for the month
  [ ] All payments matched
  [ ] Bad debt allowance updated
  [ ] DSO calculated

📥 ACCOUNTS PAYABLE
  [ ] AP subledger ties to GL
  [ ] All invoices entered
  [ ] Recurring AP auto-posted
  [ ] AP aging reviewed (nothing > 90 days unexplained)

📥 PAYROLL
  [ ] Payroll entries posted
  [ ] Payroll accrual posted (if pay date crosses month)
  [ ] PTO accrual updated (if applicable)
  [ ] Benefits invoices matched to employee elections
  [ ] 401(k) contributions and match recorded

📥 REVENUE
  [ ] Revenue recognition entries posted
  [ ] Deferred revenue schedule reconciled
  [ ] Revenue by customer trend reviewed (anomalies?)

📥 PREPAIDS & ACCRUALS
  [ ] Prepaid amortization posted
  [ ] New prepaids identified and set up
  [ ] Unbilled AP accrued
  [ ] All other material accruals posted

📥 FIXED ASSETS
  [ ] Depreciation posted
  [ ] New assets added to register
  [ ] Disposals / write-offs recorded

📥 DEBT
  [ ] Interest accrued
  [ ] Principal repayments recorded
  [ ] Covenant compliance checked

📥 EQUITY
  [ ] New option grants recorded (memo entry)
  [ ] Option exercises recorded (if any)
  [ ] SAFE/note activity recorded (if any)

📥 TAXES
  [ ] Sales tax liability reconciled
  [ ] Payroll tax liability reconciled
  [ ] Income tax provision (if applicable)

📥 FINAL REVIEW
  [ ] Trial balance balanced (debits = credits)
  [ ] Flux analysis completed, variances explained
  [ ] Financial statements drafted
  [ ] Close package sent for review
```

## Output Format

- Completed close checklist
- Trial balance (balanced)
- Flux analysis with commentary
- Revenue recognition summary
- Deferred revenue rollforward
- Prepaid expense rollforward
- "Close complete" sign-off

## Done Criteria

The skill is complete when:
1. All bank, credit card, AR, and AP accounts are reconciled.
2. Revenue recognition entries are posted and deferred revenue schedule is balanced.
3. All material accruals (payroll, unbilled AP, prepaids, commissions, depreciation, bad debt) are posted.
4. Trial balance is balanced (debits = credits).
5. Flux analysis is completed with explanations for all material variances.
6. The close checklist is fully signed off.

## Pitfalls

- **Rushing the close by skipping reconciliations**: meeting an arbitrary deadline by skipping bank recs or subledger tie-outs guarantees errors that compound into larger problems.
- **Posting journal entries to "plug" unexplained variances**: plugging a variance without investigating the root cause buries the real issue. Every plug becomes a ticking time bomb for the next close.
- **Deferring revenue recognition analysis**: assuming "the auditors will figure it out" is dangerous. Revenue recognition errors can mean restatements.
- **Treating the close checklist as optional**: skipping steps because "they didn't cause issues last month" erodes process integrity. The one month you skip a step is the month it mattered.
- **Closing without reviewing flux analysis**: declaring the books closed before checking for unusual swings means shipping financials with undetected errors.

### Heuristics

- **Close within 5-10 business days**: any longer and the data is stale before anyone sees it.
- **Same process, every month**: predictability catches errors. A changing close process is a broken close process.
- **Close checklist is non-negotiable**: skipping steps to go faster guarantees errors. Follow the checklist.
- **Revenue recognition is the #1 risk area**: it's where most startups get it wrong and where auditors dig deepest.

### Edge Cases

- **First month closing with accrual accounting** (transitioning from cash basis): the first accrual close is the hardest. Extra time, extra review.
- **Multi-entity close**: close each entity separately, then consolidate. Intercompany eliminations needed.
- **Acquisition mid-month**: close the acquired entity separately. Post-acquisition results go into consolidated from the close date.
- **Year-end close vs month-end close**: year-end has additional steps (inventory counts, 1099 prep, bonus true-ups, audit prep).

## Verification

Can you confirm that every balance sheet account has a supporting schedule that ties to the GL? Can you explain every swing > 20% on the P&L month-over-month? Is the close package ready for review within 10 business days? If not, the close isn't complete.

## Example

1. "Run the month-end close for March 2026 — start with bank reconciliations, then handle revenue recognition and accruals."
2. "We just acquired a company mid-month. Help me close the books properly with intercompany eliminations."
3. "Review the close checklist and confirm whether we're ready to sign off on the May close."

## Linked Skills

- Statement generation → `financial-statement-generation`
- Audit support → `audit-preparation`
- Controls compliance → `internal-controls-design`
