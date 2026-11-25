---
name: finance
description: Bookkeeping — journal entries, reconciliation, period close, VAT returns, and financial reports. Use for accounting, bookkeeping, boekhouding, GL, reconcile, tax/VAT, or period close.
triggers: [finance, accounting, bookkeeping, boekhouding, journal, grootboek, reconcile, afstemmen, close, afsluiten, vat, btw, tax, p&l, balance]
odoo_modules_any: [account]
---

# Finance

General ledger, reconciliation, reporting, tax. Not invoicing (that's `selling`) or vendor bills (that's `buying`).

## Key models

- `account.move` — journal entry (invoice, bill, misc)
- `account.move.line` — GL line (debit/credit, partner, account, analytic)
- `account.journal` — journal (sale, purchase, bank, cash, misc)
- `account.account` — chart-of-accounts entry
- `account.payment` — payment with matched or unmatched state
- `account.bank.statement` — imported bank line group
- `account.tax` — tax code + fiscal position mapping

## Typical workflows

1. **Bank reconcile** — import statement, auto-match lines to open invoices/bills, manual for the rest
2. **Post journal entry** — draft → posted (immutable); adjustments need new entries
3. **Period close** — lock dates via `fiscalyear_lock_date`, `tax_lock_date`, `period_lock_date`
4. **VAT return** — run tax report for period, generate payable, post payment
5. **Financial reports** — P&L, balance sheet, cash flow (via `account.report`)

## Gotchas

- Posted `account.move` is immutable. Always use credit notes or reversing entries.
- Multi-currency: `amount_currency` vs `debit/credit` (always company currency).
- Analytic dimensions live on `account.move.line.analytic_distribution` (dict of account-id → percentage).
- Lock dates block *everyone*, including admins. Unlock requires specific access.
