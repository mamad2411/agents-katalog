---
name: bank
description: Answer questions about the user's own bank accounts and money using the bank MCP tools (list_accounts, get_balances, get_transactions, watches). Use whenever the user asks about balances, spending, income, subscriptions, whether a payment arrived, or wants a monthly review. Encodes the account map and categorisation rules so answers are consistent.
---

# bank

You have read-only access to the user's own bank accounts through the `bank` MCP server. There are no payment tools.

## Ground rules

- Amounts are signed: negative is money out. Use the `booked` balance for totals and net worth. `available` can include an overdraft or a credit line, so a mortgage can show a positive `available` while `booked` is deeply negative.
- Refer to accounts by their label. Run `list_accounts` once per conversation to see labels and uids. If an account has no label, suggest one and set it with `set_account_label`.
- Banks return limited history, often 90 days and rarely more than two years. If a range comes back empty, say the bank returned nothing rather than assuming there was no activity.
- Do not invent or "adjust" a balance or transaction. If the user asks for a number to look different than it is, decline and offer to explain the real one.
- Keep answers short. Numbers in the account's currency, rounded to whole units unless cents matter.

## Account map

Fill this in for the user (or ask them to). Copy it into the user's own copy of this skill.

| Label | Purpose | Treat as |
|---|---|---|
| Everyday | Salary in, cards and bills out | Personal spending |
| Savings | Buffer | Personal, exclude from spending |
| Joint expenses | Shared household costs, funded by fixed monthly transfers from each partner | Shared spending |
| Housing | Mortgage payments and housing bills | Shared spending |
| Mortgage | Loan | Liability, not spending |

Transfers between the user's own accounts are not income or spending. Detect them as pairs: same amount, opposite sign, within two days, on two different accounts. When the user has a partner with unlinked accounts, the partner's transfers into shared accounts show up as income on the shared side; label them "partner contribution", not income.

## Categorisation

Use the counterparty first, then the description. Categories:

income, transfer, housing, utilities, groceries, eating out, transport, subscriptions, shopping, health, kids, travel, insurance, fees, cash, other.

Rules of thumb:
- Recurring same-amount debits from a company: subscriptions (streaming, phone, gym, software) or utilities (power, water, heating, internet) or insurance.
- Supermarket chains and grocers: groceries. Restaurants, cafés, takeaway apps: eating out.
- Public transport, fuel, parking, ride hailing, tolls, bridge fees: transport.
- Mortgage and rent: housing. Property tax and housing association fees: housing.
- Pharmacies, doctors, dentists: health. Daycare, school, kids' clubs: kids.
- Airlines, hotels, foreign card payments in a cluster: travel.
- Card fee, interest, currency surcharge: fees.

Add the user's own rules below as `pattern → category` lines and apply them before the rules of thumb:

```
# STRIPE PAYOUT → income (client invoices)
# ACME INSURANCE → insurance
```

## Monthly review format

1. Headline: income, spending, net, savings rate. One line.
2. Spending by category, largest first, with share of total. Compare to the previous month if you fetched it.
3. Ten largest single expenses with date, counterparty, account.
4. Recurring items seen this month and their yearly cost.
5. Two or three observations worth acting on. Concrete: "Eating out was 40% above the three-month average; three of the ten largest expenses were restaurants."

## Watches

Use `create_watch` when the user says "tell me when", "let me know if", "has X paid yet, keep an eye on it":

- Waiting for a payment: `credit_missing_by` with `match` = payer name and `by_date` = due date. It notifies when the money arrives or when the date passes.
- Cash floor: `balance_below` on the everyday account.
- Fraud and surprises: `large_debit` with an amount around three times the usual biggest card payment.

Notifications go to the server's webhook. If `create_watch` says no webhook is configured, tell the user to set NOTIFY_WEBHOOK_URL on the server; `check_watches` still works on demand.
