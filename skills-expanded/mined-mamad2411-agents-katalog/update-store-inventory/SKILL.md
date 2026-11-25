---
name: update-store-inventory
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Update store inventory so customers can only buy quantities the business can fulfill.

## Preconditions

- You have access to inventory management in the store platform.
- You know the correct SKU, location, and new quantity or adjustment amount.
- Any physical count, receiving record, or inventory correction has been approved.

## Steps

1. **Find the SKU.** [BRANCH: Shopify | generic] search Products or Inventory in Shopify, or search the SKU in the inventory system. → *Expect:* the correct item and variants are visible.
2. **Confirm the location.** Select the warehouse, store, or fulfillment location being updated. → *Expect:* the adjustment applies to the intended stock pool.
3. **Compare current quantity.** Review available, committed, incoming, and reserved counts if shown. → *Expect:* the system quantity difference is understood.
4. **Enter the adjustment.** Change the quantity or add/subtract the approved amount with a reason note. → *Expect:* the new available quantity is previewed or saved.
5. **Save the change.** Confirm the inventory update in the platform. → *Expect:* the SKU shows the updated quantity.
6. **Check storefront availability.** Open the product page or admin availability view. → *Expect:* customers see in-stock, low-stock, or sold-out status correctly.
7. **Record the reason.** Add a note, tag, or tracker entry for receiving, damage, cycle count, or correction. → *Expect:* the adjustment is auditable.

## Decision points

- If the SKU has multiple variants → update only the affected variant.
- If stock is committed to open orders → avoid reducing below committed quantity without fulfillment review.
- If the count is uncertain → place a temporary hold or mark unavailable until confirmed.

## Failure modes & recovery

- **F1 Wrong SKU:** detect product title or variant does not match → revert the adjustment and update the correct SKU.
- **F2 Wrong location:** detect stock changed in the wrong warehouse → transfer or correct both locations with notes.
- **F3 Oversold item:** detect open orders exceed available stock → pause sales and contact affected customers.

## Verification

The correct SKU and location show the approved available quantity, and the storefront availability matches that quantity.

## Variations

- Bulk import: validate a sample of rows before uploading and keep the original file.
- Bundle product: update component inventory, not only the bundle listing.
- Physical retail: reconcile point-of-sale counts with online available inventory.

## Safety & privacy

Low risk. Inventory errors can cause overselling or lost sales, so use approved counts and keep an audit trail.
