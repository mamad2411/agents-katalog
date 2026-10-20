# Cart Modify Checkout

## When To Use

Use this skill when the user asks to alter an existing cart state before checkout rather than starting the purchase flow from scratch.

Use it for shopping flows where the key challenge is correcting or modifying an already-existing cart state.

Do not use it for:

- initial product discovery without cart state
- generic product-page browsing
- non-commerce forms or procurement tasks that do not behave like a cart

## Procedure

1. Read the current cart contents before making changes.
2. Record the current item, quantity, price, and any visible coupon or discount state.
3. Determine whether the requested change is a variant swap, product replacement, quantity change, or add/remove operation.
4. Perform the minimum mutation needed to reach the requested cart state.
5. Re-read the cart and confirm the requested item is present and the old item is removed or replaced as intended.
6. If the site uses a mini-cart, drawer, or intermediate cart page, adapt to that structure instead of assuming a full cart page.
7. Apply coupon or promo code only after the cart contents are correct, unless the site clearly requires the reverse order.
8. Re-read totals and visible discount state.
9. Proceed to checkout only after the cart contents and pricing state match the request.
10. Read the checkout form and fill every required field using details supplied by the user or a saved profile. Ask for missing details rather than inventing personal information. After submission, verify the order confirmation.

## Required Evidence

- Cart contents before modification
- Cart contents after modification
- Coupon or discount state
- Checkout readiness

## Common Failures

- Adding the new item without removing the old one
- Applying a coupon before cart state stabilizes
- Treating a cart-edit task like a fresh product-page purchase flow
- Proceeding to checkout without checking visible totals or discount markers
- Assuming all commerce UIs expose the same cart structure or coupon timing

## Verification

- Deterministically confirm product names, quantities, and discount markers when possible.
- Use LLM verification only for ambiguous bundled-cart or custom UI layouts.

## Relevance

This skill is a real workflow candidate, but it has the highest current overfitting risk because shopping UIs vary widely across sites.

Current strongest E2E target:

- `tests/e2e/continuation-cart-swap.test.ts`

Additional candidate targets:

- `tests/e2e/online-shop.test.ts`
- `tests/e2e/online-shop-boundaries.test.ts`
- `tests/e2e/procurement-list.test.ts`

Status:

- Provisional until it proves useful across multiple distinct shopping-style tasks
