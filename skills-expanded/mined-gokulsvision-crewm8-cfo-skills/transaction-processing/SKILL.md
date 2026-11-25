---
name: transaction-processing
description: Processes daily financial transactions including invoices, expenses, receipts, credit card charges, and reimbursements with proper categorization, duplicate detection, anomaly flagging, and general ledger posting preparation. Use when the user mentions processing transactions, categorizing expenses, entering receipts into the books, uploading CSV exports from Stripe or QuickBooks, or asks about transaction reconciliation and bookkeeping automation.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, transactions, bookkeeping, categorization, expense-processing]
related_skills:
  - ledger-management
  - bank-reconciliation
  - accounts-payable-management
  - accounts-receivable-management
inputs_required:
  - transaction-source-data
  - chart-of-accounts
  - previous-period-categorization
deliverables:
  - categorized-transaction-log
  - anomaly-flags
  - summary-statistics
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Transaction Processing

## Purpose

Every financial transaction that hits the business — invoices received, expense reports, credit card charges, reimbursements — must be categorized, deduplicated, and flagged for anomalies before it reaches the general ledger. This skill ensures every dollar in and out is accounted for, properly categorized, and ready for posting, reducing bookkeeping errors and providing clean financial data for reporting.

## When to Use

- "Process these transactions / receipts / invoices"
- "Categorize these expenses"
- "Enter these into the books"
- Upload of receipt images, CSV exports from bank/Stripe/QuickBooks, or raw transaction lists.
- "Reconcile and categorize this month's transactions"

## Inputs Required

You must gather or receive:
1. **Transaction source data** — CSV export, bank feed, API dump, or manual list. Must include: date, amount, counterparty, description.
2. **Chart of accounts** — if not already known, load via `ledger-management` skill.
3. **Previous period categorization** — optional, for consistency checking.

## Quick Reference

| Concept | What It Does | Why It Matters |
|---------|-------------|---------------|
| Auto-categorization | Maps transaction descriptions to COA categories using rules | Ensures every transaction has a home without manual effort |
| Deduplication | Scans for duplicate amounts/vendor/date combinations | Prevents double-counting, the most common bookkeeping error |
| Anomaly detection | Flags outlier amounts, missing fields, round numbers | Catches errors and potential fraud before ledger posting |
| Confidence scoring | HIGH / MEDIUM / LOW per categorization | Surfaces items that need human review |
| Multi-currency handling | Records original + USD-equivalent | Required for accurate P&L and cash reporting |

## Procedure

1. **Parse the transaction file**: detect format (CSV, JSON, PDF table). Extract: date, amount, counterparty, description, payment method.
2. **Deduplicate**: Check for duplicates against the existing transaction log. Flag any transaction that already appears.
3. **Auto-categorize each transaction** using these rules:
   - **Software/subscriptions** → `Software & Subscriptions`
   - **Payroll/contractors** → `Payroll & Contractors`
   - **Rent/office** → `Facilities`
   - **Marketing/ads** → `Marketing`
   - **Travel/meals** → `Travel & Entertainment`
   - **Legal/professional services** → `Professional Services`
   - **Loan payments/interest** → `Debt Service`
   - **Revenue from customers** → `Revenue`
   - **Investments/grants** → `Other Income`
   - Everything else → assign best-guess category and **flag for review**.
4. **Flag anomalies**:
   - Duplicate amounts to the same vendor in the same week.
   - Transactions over an outlier threshold (3x the median of the same category).
   - Round numbers that look like estimates rather than actuals.
   - Missing counterparty or description.
5. **Prepare the output** — a categorized transaction log.
6. (Optional) **Post to ledger** — hand off to `ledger-management`.

## Output Format

A structured table (Markdown or CSV):

| Date | Description | Counterparty | Amount | Category | Confidence | Flag |
|---|---|---|---|---|---|---|
| 2026-04-01 | Stripe payout | Stripe | $12,450.00 | Revenue | HIGH | — |
| 2026-04-02 | AWS Invoice #8932 | AWS | $3,421.00 | Software & Subs | HIGH | — |
| 2026-04-03 | Lunch — Joe's Diner | Joe's Diner | $42.18 | Travel & Entertain | MEDIUM | REVIEW: personal vs business? |

Summary statistics at the top:
- Total transactions processed
- By category (pie or table)
- Flagged count / review-needed count
- Uncategorized count

## Done Criteria

The skill is complete when:
1. All transactions in the source data are parsed, deduplicated, and categorized
2. Anomaly flags are applied and surfaced to the user
3. Summary statistics are provided (total, by category, flagged count)
4. Every transaction has a confidence score (HIGH, MEDIUM, or LOW)
5. The categorized log is ready for hand-off to `ledger-management`
6. No transaction is auto-posted to the ledger without human review when flags exist

## Pitfalls

- **Categorizing by payment method instead of nature**: Categorizing everything from the corporate Amex as "Corporate Card" rather than splitting into actual expense categories (travel, software, meals)
- **Forcing every transaction to HIGH confidence**: Overriding the system's MEDIUM/LOW flags to avoid review items. Unreviewed medium-confidence items silently corrupt the general ledger
- **Skipping deduplication on manual entries**: Assuming manually-entered transactions are always unique. Manual entries are the most common source of duplicates — always scan
- **Lumping bank fees into a single "Bank Charges" line**: Payment processor fees, wire fees, FX markups, and account maintenance fees are fundamentally different costs and should be split if material
- **Auto-posting without human review when flags exist**: Processing a transaction batch with 3+ flagged items straight to the ledger without pausing for review. Flags exist for a reason — every flagged batch deserves a human sanity check before ledger posting

## Verification

Can you trace any transaction from source data through categorization to the output table? Are all anomaly flags explained with a reason? Is the confidence score justified for each categorization? If a transaction is flagged MEDIUM or LOW, is there a clear path for the user to resolve it?

## Example

**Example 1: CSV Upload**
> User: "Here's our April bank export CSV — can you process and categorize all transactions?"

→ You parse the CSV, detect format (date/description/amount columns), deduplicate against prior months, auto-categorize each line item, flag 3 anomalies (one duplicate vendor payment, one $8,400 round-number transfer, one missing counterparty), and present a categorized table with summary stats and flags highlighted for review.

**Example 2: Receipt Processing**
> User: "I have 12 receipts from our team's offsite — process these"

→ You extract dates, vendors, and amounts from the receipts, categorize all as Travel & Entertainment, apply the $500/receipt founder-scrutiny rule (none flagged since amounts are small), deduplicate against the period, and present a clean categorized batch ready for ledger posting.
