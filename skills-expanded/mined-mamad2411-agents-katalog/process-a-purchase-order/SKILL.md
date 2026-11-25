---
name: process-a-purchase-order
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Process a purchase order so an approved vendor order is recorded, trackable, and ready to match against receipt and invoice.

## Preconditions

- The purchase request, vendor, items, quantities, prices, delivery address, and approver are known.
- Budget or spending approval is available.
- Vendor terms and tax or shipping treatment are understood.

## Steps

1. **Open a new purchase order.** Go to purchases, procurement, or expenses and choose purchase order. → *Expect:* a blank PO form is visible.
2. **Select the vendor.** Choose the vendor and verify contact, payment terms, and delivery details. → *Expect:* the PO is addressed to the correct supplier.
3. **Enter requested items.** Add item descriptions, quantities, unit prices, tax, shipping, project, and delivery date. → *Expect:* the PO total matches the approved request.
4. **Attach approval support.** Link the request, quote, budget approval, or contract. → *Expect:* the PO file shows why the purchase is authorized.
5. **Submit for approval if required.** Route the PO to the approver or mark the approval already received. → *Expect:* the PO status is pending approval or approved.
6. **Send the approved PO to the vendor.** ⚠️ *Irreversible:* sending may authorize the vendor to fulfill the order, so confirm vendor, quantities, price, and delivery address first. → *Expect:* the PO status shows sent or issued.
7. **Prepare for matching.** Note how receipts and vendor invoices should be matched to the PO. → *Expect:* the PO remains open for receiving and billing.

## Decision points

- Approval is missing → do not send the PO.
- Vendor quote has expired → request updated pricing before issuing.
- Order is for inventory → confirm item codes, warehouse, and receiving process.
- Vendor invoice arrives before goods → hold payment until receiving rules are satisfied.

## Failure modes & recovery

- **F1 Wrong vendor:** detect by vendor name, email, or quote mismatch → recover by canceling the unsent PO or issuing a corrected PO.
- **F2 Over budget:** detect by PO total exceeding approval → recover by reducing scope or obtaining new approval.
- **F3 Duplicate PO:** detect by same vendor, items, and quote already issued → recover by closing the duplicate and notifying the vendor if sent.
- **F4 Invoice mismatch:** detect by vendor bill price or quantity differing from PO → recover by resolving with vendor before approval to pay.

## Verification

The PO is approved and sent to the correct vendor with matching items, quantities, prices, delivery details, approval support, and open status for receipt or billing.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks can create purchase orders for vendors; Xero may require purchase order features enabled; generic tools may use procurement requests or vendor orders.
- `us`: sales tax, use tax, and resale certificates may affect vendor purchases.

## Safety & privacy

Medium risk because purchase orders can commit company spending. Limit vendor bank details and internal budget notes to authorized users.
