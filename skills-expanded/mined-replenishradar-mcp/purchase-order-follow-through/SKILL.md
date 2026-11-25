---
name: purchase-order-follow-through
description: Review, update, approve and send purchase orders in ReplenishRadar. Use when the seller asks about open or late purchase orders, what is on a PO, whether a supplier got an order, wants to add a note, change a draft, request approval, send an order to a supplier, record a proforma invoice, cancel an order, or import orders from a spreadsheet.
---

# Purchase order follow-through

Purchase orders move draft, approved, sent, then confirmed or proforma-received, in transit, received. Reading is always allowed. Every change below needs the "make changes" permission on the connection, and Claude asks before each one.

## Reading orders

- List: `rr_list_purchase_orders`, filtered by `status` (for example `draft,sent`) or `vendor_id`, or `search` on part of a PO number.
- One order: `rr_get_purchase_order` with the PO number (for example `PO-1042`) or id. Lines come in pages; follow `cursor` until `has_more` is false before totalling anything.
- Context: `rr_list_purchase_order_notes` and `rr_list_purchase_order_documents` for what has been said and attached.

`supplier_delivery_status` says whether the supplier received the order email: `emailed` means delivered, `queued` means waiting for the supplier's quiet hours, `unknown` means it could not be confirmed, `failed` means it did not go, null means never emailed.

## Changing orders

Before any change, show the seller exactly what will change and get a yes.

| Seller wants to | Tool | Notes |
|---|---|---|
| Add a note | `rr_add_purchase_order_note` | Adds a record; the order itself is unchanged. |
| Change a draft's notes, delivery date or supplier | `rr_update_purchase_order` | Drafts and suggested orders only. Notes passed here replace the existing notes. |
| Get approval | `rr_request_purchase_order_approval` | A manager approves in ReplenishRadar within 15 minutes. No email is sent. |
| Send to the supplier | `rr_send_purchase_order` | See below. |
| Record the supplier's proforma invoice | `rr_record_proforma_invoice` | Only with details the seller gives you. Send only the fields you have. |
| Cancel | `rr_cancel_purchase_order` | Cannot be undone here. Received orders cannot be cancelled. |
| Import orders from a spreadsheet | `rr_import_purchase_orders` | Run with `preview` true first and show the result; import with `preview` false only after the seller agrees. |

## Sending to a supplier

Sending emails a person outside ReplenishRadar and cannot be recalled.

1. Read the order with `rr_get_purchase_order`. It must be approved. If it is a draft, offer `rr_request_purchase_order_approval` instead.
2. Show the seller the supplier, the lines and quantities, and ask them to confirm sending.
3. Call `rr_send_purchase_order` with the `po_id`. Report `supplier_delivery_status`.
4. To email an already-sent order again, pass `resend` true. If the status was `emailed`, `partial` or `unknown`, the supplier may already have it: ask the seller before also passing `confirm_possible_duplicate` true.

## When something is refused

Explain the refusal in the seller's words: for example "this order is already approved, so only notes can be added". If the connection cannot make changes, the seller can reconnect ReplenishRadar and tick "make changes". Do not retry a refused change unchanged.
