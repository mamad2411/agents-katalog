---
name: selling
description: Work with customers, leads, quotes, sales orders, and customer invoices. Use when the user mentions selling, sales, CRM, pipeline, quotes/offertes, orders, invoicing customers, or chasing payments.
triggers: [sell, selling, sales, verkoop, quote, offerte, order, invoice, factuur, customer, klant, deal, pipeline, lead, crm]
odoo_modules_any: [sale_management, crm, account]
---

# Selling

End-to-end revenue flow: lead → quote → sales order → invoice → payment.

## Key models

- `crm.lead` — leads and opportunities (same model, `type` field distinguishes)
- `res.partner` — customer (company or individual, `is_company`)
- `sale.order` — quotation (draft/sent) then sales order (sale/done)
- `sale.order.line` — line items
- `account.move` — customer invoice (`move_type = out_invoice`)
- `account.payment` — payment received

## Typical workflows

1. **Qualify lead** → update `stage_id`, set `expected_revenue` + `probability`, assign `user_id`
2. **Quote from lead** → create `sale.order` with `opportunity_id` link
3. **Confirm order** → `action_confirm` (state: draft → sale), stock moves created
4. **Invoice** → `_create_invoices()` on the SO, or via `sale.advance.payment.inv` wizard
5. **Collect** → match `account.payment` to invoice via reconciliation

## Gotchas

- Once `sale.order` is confirmed, lines become effectively locked — changes need an unlock or amendment.
- Taxes resolve via `fiscal.position` (country/VAT-based), not the raw product tax.
- `crm.lead` and `crm.opportunity` share the model; filter on `type` when searching.
- Invoice `state = posted` is immutable — use credit note, don't edit.
