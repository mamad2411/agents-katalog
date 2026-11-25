---
name: ga4-ecommerce
description: Implement Google Analytics 4 (GA4) e-commerce tracking. Use when adding tracking to online stores, carts, or checkout flows.
---

# Google Analytics 4 E-commerce Tracking

When the user asks to implement e-commerce tracking for GA4, use the standard GA4 e-commerce events and item arrays.

## Core E-commerce Events
Implement these essential events for a complete funnel:
- `view_item_list`: User views a list of items.
- `view_item`: User views a specific product.
- `add_to_cart`: User adds an item to their cart.
- `begin_checkout`: User starts the checkout process.
- `purchase`: User completes a transaction.

## The `items` Array
All e-commerce events require an `items` array. Each item should have at least:
- `item_id` or `item_name`
- `price`
- `quantity` (optional for views, required for cart/purchase)

Example `purchase` event:
```javascript
gtag('event', 'purchase', {
  transaction_id: "T12345",
  value: 25.42,
  tax: 4.90,
  shipping: 5.99,
  currency: "USD",
  items: [
    {
      item_id: "SKU_12345",
      item_name: "Stan and Friends Tee",
      affiliation: "Google Merchandise Store",
      coupon: "SUMMER_FUN",
      currency: "USD",
      discount: 2.22,
      index: 0,
      item_brand: "Google",
      item_category: "Apparel",
      item_category2: "Adult",
      item_category3: "Shirts",
      item_category4: "Crew",
      item_category5: "Short sleeve",
      item_list_id: "related_products",
      item_list_name: "Related Products",
      item_variant: "green",
      location_id: "ChIJIQBpAG2ahYAR_6128GcTUEo",
      price: 9.99,
      quantity: 1
    }
  ]
});
```
