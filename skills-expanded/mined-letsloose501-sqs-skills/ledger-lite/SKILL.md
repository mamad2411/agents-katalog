---
name: ledger-lite
description: Records a cash transaction and answers what the balance is. Use when the user reports a payment, when a receipt is handed over to be logged, or when they ask what the current balance is.
---

# Ledger lite

1. Read the amount, the date and the counterparty off whatever was handed over.
2. Append one row to `ledger.csv` in that order. Stop when the row is written.
3. Print the new balance, with the currency, on its own line.

## When to open which reference

[format.md](references/format.md) holds the column order and the rounding rule. Open it
before writing a row; the input's own layout never decides the column order.
