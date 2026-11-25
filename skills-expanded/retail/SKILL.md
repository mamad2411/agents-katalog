---
name: retail
description: Point-of-sale operations — sessions, orders, cash control, and end-of-day closing. Use for POS, kassa, retail, cash register, or shop-floor transactions.
triggers: [pos, retail, kassa, point of sale, cash register, session, shop, storefront]
odoo_modules_any: [point_of_sale]
---

# Retail

In-person, cash-and-card-fast sales through the POS.

## Key models

- `pos.config` — a physical POS terminal (cash box, printer, payment methods)
- `pos.session` — a shift at a terminal (opened → in_progress → closed)
- `pos.order` — one transaction (sale or refund)
- `pos.order.line` — item sold
- `pos.payment` — how it was paid (one order can split across methods)
- `pos.payment.method` — cash / card / gift card

## Typical workflows

1. **Open session** — `pos.session` with opening cash count
2. **Take orders** — `pos.order` created per transaction; often offline, synced later
3. **Split payment** — one `pos.order` with multiple `pos.payment` rows
4. **Refund** — new `pos.order` with negative lines, links to original
5. **Close session** — count cash, reconcile against expected, post to journal

## Gotchas

- POS works offline — orders buffer on the client and sync when back online. Expect duplicates if sync retries.
- Session must close with zero variance; differences post to a loss/gain account set on `pos.config`.
- Stock moves happen at session close, not per order (unless `update_stock_quantities = 'real'`).
- Fiscal/cash register laws vary by country — check `l10n_*_pos` modules before tampering with amounts.
