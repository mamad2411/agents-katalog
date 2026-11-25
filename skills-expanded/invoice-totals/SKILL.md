---
name: invoice-totals
description: Adds up a month of invoices from a CSV export and writes the total per supplier. Use when the user drops an invoice export and asks what they owe, or wants the month's spend broken down by supplier.
---

# Invoice totals

1. Read the CSV the user named; stop if it has no `supplier` and `amount` columns.
2. Sum `amount` per supplier and write `totals.md` with one line per supplier.
3. Print the grand total on its own line.
