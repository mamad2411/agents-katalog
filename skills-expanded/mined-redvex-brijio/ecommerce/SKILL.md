---
name: ecommerce
description: "Automate e-commerce checkout flows on authenticated pages: add to cart, fill shipping, apply coupons, fill payment — stopping before final submit."
---

# E-Commerce Checkout Automation

Guide users through e-commerce checkout flows using Brijio. Handles the
full pipeline: product selection, cart management, address forms, promo codes,
and payment — always stopping before the final "Place Order" step.

## When to Use

- Filling checkout forms for repeat purchases
- Testing e-commerce flows on staging environments
- Applying coupon codes and verifying discounts
- Comparing shipping options and prices
- Any task involving multi-step checkout on an authenticated shopping site

## Workflow

### 1. Check Connection and Cart State

```
1. list_browsers → Confirm browser connected
2. read_current_page → Check current page
```

Verify the user is on a product page or cart page. If they need to add items
first, help them navigate using the [navigation](skill://brijio/navigation)
skill.

### 2. Add to Cart (if needed)

If the user is on a product page:

```
1. read_current_page → Find the "Add to Cart" action
2. Select product options (size, color) using select_options/set_checked
3. click_element(kind: "action", id: "a3") → "Add to Cart"
4. Wait for cart update, re-read page
```

### 3. Navigate to Checkout

```
1. read_current_page → Find "Cart" or "Checkout" link
2. click_element(kind: "link", id: "e7") → Navigate to cart/checkout
3. read_current_page → Verify on cart or checkout page
```

### 4. Review Cart

Before proceeding to checkout, review the cart with the user:

- Item names, quantities, prices
- Subtotal, tax, shipping estimates
- Any applied discounts

Confirm the user wants to proceed before moving to the checkout form.

### 5. Fill Shipping Address

```
1. read_current_page → Get checkout form
2. fill_input(formId, controlId, text) → Address fields
3. select_options → Country/state dropdowns
4. set_checked → "Billing same as shipping" if applicable
5. click_element(kind: "action") → "Continue to shipping" or "Next"
6. read_current_page → Verify shipping step
```

### 6. Select Shipping Method

```
1. read_current_page → Find shipping options
2. set_checked(formId, controlId, true) → Select shipping method
3. Note the updated total with shipping cost
4. click_element(kind: "action") → "Continue to payment"
5. read_current_page → Verify on payment step
```

### 7. Apply Coupons/Promo Codes

If the user has a promo code:

```
1. read_current_page → Find "Promo code" or "Coupon" input
2. fill_input(formId, controlId, "SAVE20") → Enter code
3. click_element(kind: "action") → "Apply" button next to the promo field
4. read_current_page → Verify discount applied, check updated total
```

### 8. Fill Payment (STOP BEFORE SUBMIT)

```
1. read_current_page → Get payment form
2. Fill card number, expiry, CVV — ⚠️ CARD NUMBER FIELDS MAY BE PASSWORD-TYPE
3. If fill_input returns browser_error for card number:
   → Ask user to fill payment details manually
4. NEVER click "Place Order" / "Complete Purchase" unless explicitly asked
```

### 9. Final Review

Present the complete order summary to the user:

```markdown
## Order Summary

**Items:**

- Product Name × 1 — $29.99
- Product Name × 2 — $59.98

**Subtotal:** $89.97
**Shipping:** $5.99 (Standard)
**Discount:** -$20.00 (SAVE20)
**Tax:** $7.00
**Total:** $82.96

**Shipping to:** 123 Main St, City, ST 12345
**Payment:** •••• 4242 (entered manually)

⚠️ Ready to submit — awaiting your confirmation.
```

## Pitfalls

### Payment Iframes

Many e-commerce sites embed payment forms in iframes (Stripe, PayPal, etc.).
Brijio may not be able to interact with iframe-embedded fields. If
`read_current_page` doesn't show card number fields inside the form, they're
likely in an iframe. Ask the user to fill payment details manually.

### Password-Type Fields

Card number, CVV, and some expiry fields use `type="password"`. Brijio
returns `browser_error` for these fields. This is correct security behavior —
let the user fill sensitive payment data manually.

### Dynamic Totals

Shipping, tax, and discounts may update dynamically after each step. Always
re-read the page after any action that could change the total (selecting
shipping, applying a coupon, changing quantities).

### Address Autocomplete

Some checkout forms have address autocomplete. If `fill_input` on an address
field triggers a dropdown, the dropdown items have their own IDs. Re-read the
page and click the correct autocomplete suggestion.

### Cart Expiration

Shopping carts may expire after a timeout. If the user takes too long between
steps, the cart may empty or show errors. Re-read the page if you suspect this.

### Multi-Step Checkout

E-commerce checkout often spans 3-4 pages (Cart → Shipping → Payment → Review).
After each "Continue" click, re-read the page — all element IDs are invalid
after navigation.

## NEVER Auto-Submit

**Never** click "Place Order", "Complete Purchase", "Confirm", or any final
submit button without the user's explicit confirmation. Present the order
summary and wait for the user to say "submit" or "place the order".
