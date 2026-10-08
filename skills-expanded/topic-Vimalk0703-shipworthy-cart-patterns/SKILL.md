---
name: cart-patterns
description: E-commerce cart management patterns — cart state, inventory reservation, price calculation, discount application, tax computation, and cart abandonment handling.
invoke_when: Building or modifying shopping cart functionality, checkout flow, pricing logic, or inventory reservation systems.
---

# Cart Patterns

## Cart State Management

### Rule: Cart is server-authoritative
Never trust client-side cart state for pricing or inventory. The client holds product IDs and quantities; the server calculates everything else.

```
Client sends: { items: [{ productId: "abc", quantity: 2 }] }
Server returns: { items: [{ productId: "abc", quantity: 2, unitPrice: 29.99, lineTotal: 59.98, available: true }], subtotal: 59.98, tax: 5.40, total: 65.38 }
```

### Rule: Use integers for money
Never use floating-point for currency. Store prices in the smallest currency unit (cents for USD, pence for GBP).

```
// WRONG
const price = 29.99;
const total = price * 3; // 89.97000000000001

// RIGHT
const priceInCents = 2999;
const totalInCents = priceInCents * 3; // 8997
const displayPrice = (totalInCents / 100).toFixed(2); // "89.97"
```

### Rule: Validate inventory at checkout, not at cart-add
- Adding to cart: check inventory but don't reserve — show "low stock" warning if < 5 remaining
- Starting checkout: reserve inventory with a TTL (10-15 minutes)
- Completing payment: convert reservation to deduction
- Timeout/abandonment: release reservation

### Rule: Idempotent cart operations
Cart mutations (add, remove, update quantity) must be idempotent. If a user clicks "Add to Cart" twice due to a slow network, they should get quantity 1 (or quantity+1 from current), not quantity 2.

Use: `PUT /cart/items/{productId}` with desired quantity, not `POST /cart/items` with delta.

## Price Calculation

### Order of operations (always this order):
1. Base price per item
2. Apply item-level discounts (sale prices, volume discounts)
3. Calculate line totals (price * quantity)
4. Calculate subtotal (sum of line totals)
5. Apply cart-level discounts (promo codes, loyalty points)
6. Calculate tax (on discounted subtotal, jurisdiction-dependent)
7. Add shipping
8. Calculate total

### Discount rules
- Only one promo code at a time (unless explicitly supporting stacking)
- Validate promo code server-side: is it active? Has it expired? Has it hit its usage limit? Is the cart minimum met?
- Never expose discount calculation logic to the client — only the result
- Log every discount application for audit trail

## Tax Calculation

- Use a tax service (TaxJar, Avalara) for production — don't calculate manually
- For MVP: apply a flat tax rate, clearly labeled as "estimated tax"
- Tax rates vary by jurisdiction, product category, and customer type — this is NOT something to hard-code
- Store the tax rate used on each order for compliance (rates change over time)

## Cart Abandonment

- Persist cart state for logged-in users (database)
- For anonymous users: use session storage or a guest cart with cookie-based ID
- Cart TTL: 30 days for logged-in, 7 days for guest
- Don't delete abandoned carts — mark them as expired for analytics

## Security Considerations

- Rate-limit cart operations (prevent cart bombing)
- Validate product IDs against catalog on every cart operation
- Never let the client set prices — always compute server-side
- Sanitize promo codes (SQL injection, XSS in code field)
- Don't expose inventory counts to the API (only "in stock" / "low stock" / "out of stock")
