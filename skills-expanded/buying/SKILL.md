---
name: buying
description: Work with vendors, RFQs, purchase orders, receiving goods, and paying vendor bills. Use when the user mentions buying, purchase, inkoop, vendors/suppliers, POs, bills, or procurement.
triggers: [buy, buying, purchase, inkoop, po, rfq, vendor, supplier, leverancier, bill, procurement]
odoo_modules_any: [purchase, account]
---

# Buying

End-to-end procurement: RFQ → PO → receipt → vendor bill → payment.

## Key models

- `res.partner` — vendor (`supplier_rank > 0`)
- `product.supplierinfo` — vendor-product link (price, lead time, min qty)
- `purchase.order` — RFQ (draft/sent) then PO (purchase/done)
- `purchase.order.line` — PO lines
- `stock.picking` — incoming receipt (auto-created from PO)
- `account.move` — vendor bill (`move_type = in_invoice`)
- `account.payment` — payment sent

## Typical workflows

1. **RFQ** → create `purchase.order` in draft, send via `action_rfq_send`
2. **Confirm PO** → `button_confirm` (state: draft → purchase), creates incoming picking
3. **Receive** → validate `stock.picking`, quantities flow to `stock.quant`
4. **Bill** → create vendor bill from PO (`action_create_invoice`)
5. **Three-way match** → verify PO qty/price ↔ receipt qty ↔ bill qty/price
6. **Pay** → register `account.payment`, reconcile against bill

## Gotchas

- `product.supplierinfo` is per product+vendor — reorder rules pick lowest-price supplier by default.
- Lead time = `product.supplierinfo.delay` + `purchase_calendar` if set.
- Bill can be created before receipt — watch for "Bill received but goods not yet in stock".
- Currency on vendor bill follows vendor default, not company — check `currency_id`.
