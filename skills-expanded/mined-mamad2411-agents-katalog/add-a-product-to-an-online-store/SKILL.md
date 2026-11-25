---
name: add-a-product-to-an-online-store
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a complete product listing in an online store without publishing incorrect price, inventory, or customer-facing details.

## Preconditions

- You have product name, description, price, images, SKU, inventory, shipping details, and tax category.
- You have permission to edit the store catalog.
- Any required legal, brand, or merchandising approval is complete.

## Steps

1. **Open product creation.** [BRANCH: Shopify | generic] choose Products > Add product in Shopify, or open the store platform's new product form. → *Expect:* a blank product editor is open.
2. **Enter product basics.** Add title, description, vendor or brand, product type, and tags or collections. → *Expect:* the listing can be found and categorized.
3. **Upload media.** Add approved images or video and set alt text if supported. → *Expect:* product media displays in the intended order.
4. **Set pricing.** Enter price, compare-at price if approved, cost if tracked, and taxable status. → *Expect:* checkout pricing matches the approved amount.
5. **Add variants.** Create size, color, format, or bundle variants with unique SKUs. → *Expect:* each purchasable option has a SKU and price.
6. **Set inventory and fulfillment.** Enter stock quantity, inventory tracking, weight, shipping profile, and fulfillment location. → *Expect:* the store can sell and ship the item correctly.
7. **Preview the listing.** Review desktop and mobile product pages before publishing. → *Expect:* copy, images, price, variants, and availability look correct.
8. **Publish or save.** ⚠️ *Irreversible:* before publishing, confirm price, inventory, shipping, and legal claims because customers may purchase immediately. → *Expect:* the product is active or saved as an approved draft.

## Decision points

- If price or inventory is not final → save as draft instead of publishing.
- If a product has regulated claims → get compliance review before publishing.
- If variants differ in shipping weight → enter weight per variant.

## Failure modes & recovery

- **F1 Missing SKU:** detect a variant has no SKU → assign the correct SKU before activation.
- **F2 Wrong price:** detect preview or test cart shows incorrect price → unpublish or correct immediately.
- **F3 Image mismatch:** detect media shows wrong product or color → remove and upload approved media.

## Verification

The product page or draft has correct title, media, price, variants, SKU, inventory, shipping settings, and publish status.

## Variations

- Digital product: disable physical shipping and confirm delivery file or license flow.
- Preorder: label expected ship date and inventory rules clearly.
- Marketplace listing: follow marketplace category attributes and prohibited-item policies.

## Safety & privacy

Low risk. Avoid unsupported health, safety, environmental, or warranty claims, and do not expose supplier-only notes or internal cost data.
