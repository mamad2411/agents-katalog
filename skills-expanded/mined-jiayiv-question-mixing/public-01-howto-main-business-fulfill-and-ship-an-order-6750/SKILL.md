---
name: fulfill-and-ship-an-order
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 20min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Pick, pack, label, and mark an order as shipped with accurate tracking.

## Preconditions

- The order is paid or approved for fulfillment.
- Inventory is available and allocated to the order.
- You have packing materials, carrier access, and shipping rules.

## Steps

1. **Open the fulfillment record.** [BRANCH: Shopify | generic] open the order's fulfillment section in Shopify, or open the warehouse/order system task. → *Expect:* items, quantities, address, and shipping method are visible.
2. **Verify ship eligibility.** Confirm payment, fraud review, address validation, and hold status. → *Expect:* no active hold blocks shipment.
3. **Pick items.** Collect the exact SKUs, variants, quantities, and inserts listed on the order. → *Expect:* physical items match the order record.
4. **Pack the order.** Use suitable packaging, protection, and required documents. → *Expect:* contents are secure and ready for carrier handling.
5. **Create the label.** Buy or generate the shipping label using the correct service, weight, dimensions, and address. → *Expect:* a label and tracking number are available.
6. **Attach label and hand off.** Put the label on the package and place it in the correct carrier pickup or drop-off area. ⚠️ *Irreversible:* confirm package contents and address before carrier handoff because shipped packages may be hard to recall. → *Expect:* the package is accepted for shipment or ready for pickup.
7. **Mark fulfilled.** Enter or confirm tracking in the order system and send shipment notification if appropriate. → *Expect:* the order shows fulfilled or shipped with tracking.

## Decision points

- If an item is missing → hold fulfillment and escalate inventory or substitution options.
- If address validation fails → contact the customer before buying a label.
- If shipping cost or service differs from policy → get approval before purchase.

## Failure modes & recovery

- **F1 Wrong item picked:** detect SKU or variant mismatch during packing → replace before sealing.
- **F2 Bad label:** detect wrong address, weight, or service → void label if possible and create a corrected one.
- **F3 Tracking missing:** detect order marked shipped without tracking → add tracking and notify customer.

## Verification

The order is fulfilled with correct items, carrier label, tracking number, shipment status, and customer notification if required.

## Variations

- Split shipment: fulfill only available items and communicate remaining items.
- Local delivery: use route or courier tracking instead of parcel carrier label.
- International shipment: include customs forms, HS codes, and declared values.

## Safety & privacy

Medium risk because shipping exposes customer address and affects paid orders. Protect labels, verify addresses, and share tracking only with authorized parties.
