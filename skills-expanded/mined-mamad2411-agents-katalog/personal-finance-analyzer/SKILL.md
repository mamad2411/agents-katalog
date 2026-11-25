---
name: personal-finance-analyzer
description: Categorize bank transactions from a CSV export, identify spending patterns, flag anomalies, and generate a monthly financial summary with actionable observations. Use when the user exports their bank or credit card transactions and wants insight into their spending without uploading data to a third-party app. Runs entirely in Claude — no external service required. Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today."
---

# Personal Finance Analyzer

Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today" (Intermediate Tier, #13).

> Categorizes bank transactions and generates a monthly spending summary from CSV.

## What this skill produces

From a pasted CSV or transaction list:
- **Categorized spending**: each transaction assigned to a category
- **Monthly summary**: total per category with % of total spend
- **Top merchants**: ranked by total spend
- **Anomaly flags**: unusual charges, duplicates, subscriptions you may have forgotten
- **Savings observations**: where spending is high relative to typical benchmarks
- **Budget snapshot**: actual vs. any budget targets you provide

## Copy-paste prompt to use

```
You are a personal finance analyst. Analyze the following bank/credit card transactions and produce a monthly financial summary.

TRANSACTIONS (paste CSV or list):
[PASTE TRANSACTIONS HERE — format: date, description, amount]

MY CONTEXT (optional):
- Monthly income (after tax): $[AMOUNT] or [LEAVE BLANK]
- Budget targets: [e.g. "dining out: $300, groceries: $400"] or [LEAVE BLANK]
- Anything I want you to watch for: [e.g. "flag any subscription over $20"]

Please:
1. Categorize every transaction into one of these categories:
   Housing | Groceries | Dining Out | Transport | Subscriptions | Health | Shopping | Entertainment | Utilities | Income | Transfer | Other

2. Build a summary table:
   | Category | Total Spent | % of Total | # Transactions |

3. List top 10 merchants by spend

4. Flag any of these:
   - Recurring charges (same amount, same merchant, monthly pattern)
   - Unusually large transactions (over $200 in a normally low-spend category)
   - Possible duplicate transactions
   - Subscriptions you might have forgotten about

5. Give me 3–5 specific observations about my spending — be direct, not diplomatic

6. If I gave you income or budget targets, show actual vs. budget per category

Rules:
- Do not make up transactions that aren't in the data
- If a description is ambiguous (e.g. "ACH TRANSFER 4829"), categorize as "Transfer" and note it
- Flag, don't assume — if something looks odd, say so and ask rather than deciding for me
```

## Privacy note

Paste transactions directly into Claude — no third-party service receives the data. For extra caution:
- Remove account numbers from the CSV before pasting
- Remove payee reference numbers you consider sensitive
- Claude doesn't retain data between sessions

## CSV export instructions (common banks)

| Bank | How to export |
|---|---|
| Chase | Accounts → Activity → Download → CSV |
| Bank of America | Transactions → Download → Comma Delimited |
| Revolut | Payments → Statement → Export CSV |
| Monzo | Help → Export transactions |
| Any bank | Look for "Download transactions" or "Export" in transaction history |

## Related skills

- **invoice-receipt-processor**: Business/reimbursable expense tracking (separate from personal)
- **n8n-agent-builder**: Automate monthly analysis — trigger on the 1st of each month, pull from Google Sheets, email the report
- **the-leverage-stack-auditor**: If you're a business owner, audit the business expense layer with this skill
