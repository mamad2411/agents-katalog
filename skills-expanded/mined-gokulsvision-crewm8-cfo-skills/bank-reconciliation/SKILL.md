---
name: bank-reconciliation
description: Reconciles bank accounts and credit cards monthly — matches every transaction to the ledger, resolves exceptions, tracks uncleared items, and documents the process. Use when the user mentions bank reconciliation, transaction matching, reconciling accounts, GL cash balance not matching the bank, or asks about month-end reconciliation or corporate card reconciliation.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, cash, treasury, bank-reconciliation, transaction-matching]
related_skills:
  - transaction-processing
  - ledger-management
  - cash-monitoring
  - accounts-payable-management
  - accounts-receivable-management
inputs_required:
  - bank-statement-for-the-period
  - GL-cash-account-detail-from-ledger-management
  - AP-and-AR-subledgers-for-matching
  - prior-month-reconciliation
deliverables:
  - bank-reconciliation-statement-per-account
  - uncleared-items-register-with-age-analysis
  - summary-of-adjusting-journal-entries-needed
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Bank Reconciliation

Reconcile every bank account and corporate credit card each month. Match bank transactions to the general ledger, resolve discrepancies, track uncleared items, and ensure the books reflect reality. Goal: the GL cash balance always ties to the bank.

## Purpose

Bank reconciliation is the most fundamental financial control — it catches fraud, bank errors, and data entry mistakes before they compound. An unreconciled GL means the company doesn't actually know how much cash it has. This skill ensures every account ties to the bank statement every month, with full documentation of timing differences and adjustments.

## When to Use

- "Reconcile the bank accounts"
- "Match these transactions"
- "Why doesn't the GL cash balance match the bank?"
- "Reconcile corporate cards"
- "Month-end bank reconciliation"

## Inputs Required

1. **Bank statement** — full transaction history for the period (CSV, PDF, or API).
2. **GL cash account detail** — from `ledger-management`.
3. **AP and AR subledgers** — for vendor payment and customer receipt matching.
4. **Prior month reconciliation** — the ending reconciled balance becomes this month's starting point.

## Quick Reference

| Reconciling Item | Treatment | Example |
|--- |--- |--- |
| Deposits in transit | Add to bank balance | Customer check deposited but not cleared |
| Outstanding checks | Deduct from bank balance | Check issued but not yet cashed |
| Bank fees not yet recorded | Record in GL | Monthly maintenance fee, wire fee |
| Interest income not yet recorded | Record in GL | Interest earned on account balance |
| ACH settlements in flight | Track, should clear in 1-3 days | Payroll sent but not debited |
| Bank errors | Dispute with bank immediately | Wrong amount debited/credited |

## Procedure

### 1. Start with Prior Reconciliation

```
Beginning book balance = Prior month reconciled ending balance
Beginning bank balance = Prior month reconciled ending balance (they should match)
```

If the prior month didn't tie, start by resolving last month's outstanding items FIRST.

### 2. Import Bank Transactions

For each bank account and credit card, get all transactions for the period. Normalize to:
- Date, description, amount, type (debit/credit), bank reference number.

### 3. Match to Ledger Transactions

For each bank transaction, find the corresponding GL entry:

**Auto-match rules** (high confidence):
- Same date (±1 day for ACH settlement lag), same exact amount.
- Same counterparty name (case-insensitive fuzzy match on vendor/customer name).
- Transaction reference numbers match.

**Manual match rules** (medium confidence, flag for review):
- Same amount but different date (2-5 days off) — could be settlement delay.
- Single bank transaction matching multiple GL entries (batch payments).
- Multiple bank transactions matching a single GL entry (split payments).

**No match**:
- Bank transaction with no GL entry → missing from books.
- GL entry with no bank transaction → uncleared / outstanding / duplicate.

### 4. Identify Reconciling Items

Standard reconciling items:

| Type | Example | Treatment |
|---|---|---|
| **Deposits in transit** | Customer check deposited but not yet cleared | Add to bank balance |
| **Outstanding checks** | Check issued but not cashed | Deduct from bank balance |
| **Bank fees not yet recorded** | Monthly maintenance fee, wire fee | Record in GL |
| **Interest income not yet recorded** | Interest earned on account balance | Record in GL |
| **ACH settlements in flight** | Payroll sent but not debited | Track, should clear in 1-3 days |
| **Bank errors** | Wrong amount debited/credited | Dispute with bank immediately |

### 5. Produce Reconciliation Statement

```
===== BANK RECONCILIATION - SVB Operating Account =====
Period: April 2026

Ending balance per bank statement:        $1,842,300.00
Add: Deposits in transit                     $45,000.00
Less: Outstanding checks                    ($12,300.00)
Adjusted bank balance:                    $1,875,000.00

Ending balance per GL:                    $1,870,500.00
Add: Interest not yet recorded                $2,100.00
Less: Bank fees not yet recorded             ($1,600.00)
Add: Deposits recorded but not in bank       $45,000.00
Less: Checks recorded but not cleared      ($12,300.00)
Less: Payroll ACH in transit               ($28,700.00)
Adjusted book balance:                    $1,875,000.00

Difference:                                       $0.00 ✓ RECONCILED
```

### 6. Track Uncleared Items

Maintain a list of uncleared items older than:
- **7 days**: flag as "attention needed"
- **30 days**: flag as "stale — investigate"
- **60 days**: flag as "potential error — contact bank or counterparty"

## Output Format

- Bank reconciliation statement per account (formatted as above)
- Uncleared items register with age analysis
- Summary of adjustments needed to the GL
- Reconciliation status: `RECONCILED | RECONCILED WITH ITEMS | UNRECONCILED`

## Done Criteria

The skill is complete when:
1. Every transaction on the bank statement is matched to a GL entry or identified as a reconciling item
2. A reconciliation statement is produced showing adjusted bank balance = adjusted book balance (or the exact difference)
3. Uncleared items are aged and flagged by severity (7 / 30 / 60 days)
4. Any adjusting journal entries required are listed with amounts and accounts
5. Reconciliation status is clearly reported

## Pitfalls

- **Reconciling only at year-end**: deferring reconciliation until the annual audit dumps 12 months of unmatched transactions on you at once. By month 3, errors compound and become nearly impossible to trace. Monthly reconciliation is non-negotiable.
- **Force-matching to make it tie**: adjusting the GL with a plug entry or "miscellaneous reconciling item" to force the books to match the bank without tracing the root cause. This paper over fraud, bank errors, and duplicate entries — each forced match is a latent control failure.
- **Not aging uncleared items**: logging reconciling items and never following up. An outstanding check from 6 months ago is not "just outstanding" — it's either lost, voided, or fraudulent. Uncleared items must be aged and escalated on a fixed schedule.
- **Double-counting credit card transactions**: reconciling a corporate card statement against the GL without first ensuring the card charges were already posted to the correct expense accounts. This produces phantom "unmatched" entries that lead to duplicate posting.
- **Reconciling from the GL outward instead of the bank inward**: starting with the GL balance and adjusting it to match the bank statement. The correct direction is bank statement → adjust for reconciling items → should equal the adjusted GL balance. Reversing this direction means you trust the GL (which may have errors) over the bank (which is the source of truth for cash).

## Verification

Can you answer "does the GL cash balance tie to the bank statement?" from the reconciliation output? Are all reconciling items properly aged with follow-up actions assigned? If the statement shows UNRECONCILED, is the exact difference and root cause identified? If not, the reconciliation is incomplete.

## Example

**User prompt**: "Reconcile our SVB operating account for April."
**What should happen**: Pull the April bank statement, import all transactions, match each against GL entries using auto-match and manual-match rules, identify reconciling items (deposits in transit, outstanding checks, bank fees, interest), produce the full reconciliation statement, report the status (RECONCILED / RECONCILED WITH ITEMS / UNRECONCILED), and list any adjusting journal entries needed.

**User prompt**: "Our GL shows $50k more cash than the bank — find the difference."
**What should happen**: Run a side-by-side transaction comparison between the GL cash account and the bank statement for the period, highlight every unmatched item on both sides, categorize the variance by type (timing difference, missing entry, duplicate, error), and provide a step-by-step resolution plan with specific GL adjustments required.

**User prompt**: "Reconcile all our corporate cards for last month and flag anything suspicious."
**What should happen**: Pull the card statement for the period, match each charge to GL expense entries and employee expense reports, identify unmatched charges, run fraud heuristics (duplicate charges, unusual merchant categories, weekend/off-hours transactions, amounts just below approval thresholds), and produce a reconciliation statement with a separate fraud-flag appendix.

## Linked Skills

- Categorize unmatched transactions → `transaction-processing`
- Post reconciling journal entries → `ledger-management`
- Cross-check cash balance → `cash-monitoring`
- Verify vendor payments cleared → `accounts-payable-management`
- Match customer deposits → `accounts-receivable-management`
