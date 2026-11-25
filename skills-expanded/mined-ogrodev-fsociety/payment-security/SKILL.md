---
name: payment-security
description: |
  This skill should be used when the user mentions "payment", "payment gateway", "checkout",
  "IDOR payment", "payment bypass", "Stripe", "MercadoPago", "Binance Pay", "PIX", "PayPal",
  "Adyen", "Braintree", "Square", "Razorpay", "Mollie", "webhook", "payment webhook",
  "price manipulation", "amount tampering", "currency manipulation", "e-commerce",
  "shopping cart", "cart manipulation", "checkout flow", "checkout bypass", "order tampering",
  "refund abuse", "refund fraud", "chargeback", "race condition payment", "double spending",
  "coupon abuse", "discount stacking", "promo code", "gift card", "store credit",
  "PCI DSS", "PCI compliance", "payment card", "credit card testing", "payment token",
  "tokenization", "3D Secure", "3DS bypass", "SCA bypass", "payment callback",
  "payment confirmation", "invoice manipulation", "subscription bypass", "trial abuse",
  "payment flow", "financial API", "billing bypass", "pricing logic",
  "negative amount", "zero price", "float precision", "currency confusion",
  "payment race condition", "concurrent checkout", "gateway bypass", "gateway testing",
  "shipping fee bypass", "tax manipulation", "quantity manipulation", "item substitution",
  or discusses testing payment system security. It provides comprehensive methodology for
  payment system penetration testing using Hexstrike tools.
version: 2.0.0
---

# Payment Security Testing

Payment systems are the highest-impact attack surface in any e-commerce application. A single vulnerability translates directly to financial loss, regulatory exposure, and reputational damage. Payment findings are almost always **HIGH** or **CRITICAL** severity -- a confirmed price manipulation or payment bypass is an automatic CRITICAL.

This skill covers the full offensive lifecycle against payment systems: flow mapping, price manipulation, race conditions, IDOR exploitation, gateway bypass, cart tampering, and refund abuse.

## Triage Workflow

Follow this sequence. Each phase builds on the previous one. Skip nothing -- payment logic bugs hide in edge cases.

### Phase 1 -- Payment Flow Mapping

Before attacking, map the entire payment lifecycle. Every request from cart to confirmation is in scope.

**Map these flows:**

1. **Add to cart** -- item selection, quantity, variant, pricing source
2. **Cart management** -- update quantity, remove items, apply coupons/discounts
3. **Checkout initiation** -- address entry, shipping method selection, tax calculation
4. **Payment method selection** -- card entry, saved card, wallet, gateway redirect
5. **Payment processing** -- tokenization, charge creation, 3DS challenge
6. **Payment confirmation** -- callback/webhook, order status update, fulfillment trigger
7. **Post-payment** -- refund flow, cancellation, subscription management

**Capture with HTTP Repeater:**

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__http_repeater`

```
Intercept the full checkout flow from cart to confirmation.
For each request, note:
- Which parameters control price, quantity, item identity
- Which parameters reference user identity (user_id, session, account)
- Where the server trusts client-supplied values vs. server-side lookup
- Where the flow can be short-circuited (skip steps, replay confirmations)
```

**Key questions to answer during mapping:**

- Does the server recalculate totals, or trust the client-submitted amount?
- Are item prices embedded in the request, or looked up by product ID?
- Is the payment amount derived from the cart at checkout time, or passed as a parameter?
- Does the webhook/callback validate the payment amount matches the order total?
- Can checkout steps be reordered or skipped?

Record flow architecture:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add <target> tech-stack payment-flow \
  "gateway=<stripe|paypal|custom>, checkout=<spa|redirect|server-rendered>, webhook=<yes|no>" \
  --source "payment-flow-mapping"
```

### Phase 2 -- Price Manipulation

Test whether the application trusts client-supplied pricing data. This is the most common payment vulnerability class.

**Attack vectors (test all):**

1. **Direct amount tampering** -- modify the `amount`, `price`, `total`, or `unit_price` field
2. **Negative values** -- send negative amounts to generate credits or reverse charges
3. **Zero price** -- set amount to 0 or 0.00
4. **Float precision** -- exploit IEEE 754: `0.1 + 0.2 != 0.3`, send `19.999999999999998`
5. **Integer overflow** -- send amounts exceeding INT_MAX or BIGINT boundaries
6. **Currency confusion** -- change currency code to a weaker currency (USD -> VEF, EUR -> IRR)
7. **Discount stacking** -- apply multiple coupon codes, loyalty points + coupon + gift card simultaneously
8. **Coupon replay** -- reuse single-use coupons across sessions or accounts
9. **Quantity * price mismatch** -- change quantity to 0 or negative after price calculation

Use `http_repeater` to modify each parameter individually and observe server response.

See `references/price-manipulation.md` for detailed techniques, edge cases, and examples.

### Phase 3 -- Race Conditions

Payment flows are stateful and time-dependent -- prime targets for TOCTOU attacks.

**Attack vectors:**

1. **Double-spending** -- send concurrent payment confirmations for the same cart
2. **Coupon race** -- apply the same single-use coupon in parallel requests
3. **Balance race** -- deplete wallet/credit balance simultaneously from multiple sessions
4. **Inventory race** -- purchase limited-stock items with concurrent checkouts
5. **Refund race** -- submit multiple refund requests before the first completes

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__http_intruder`

```
Send 20-50 concurrent identical requests to the payment confirmation endpoint.
Use null payloads mode with 50 threads.
Check: did more than one succeed? Were multiple orders created? Was balance debited once but credited twice?
```

See `references/race-conditions.md` for timing techniques and detection methodology.

### Phase 4 -- Payment IDOR

Payment IDORs let attackers access, modify, or hijack other users' transactions.

**Attack vectors:**

1. **Order ID enumeration** -- sequential or predictable order IDs in `/orders/<id>`, `/invoices/<id>`
2. **Transaction reference swapping** -- change `transaction_id` in confirmation callbacks
3. **Recipient manipulation** -- change `emailDesc`, `account_id`, `user_id` in payment creation
4. **Invoice access** -- access other users' invoices/receipts via IDOR on the invoice endpoint
5. **Horizontal escalation** -- view/modify another user's payment methods, saved cards, billing addresses
6. **Vertical escalation** -- access admin payment dashboards, refund capabilities, or transaction logs

See `references/payment-idor.md` for detailed IDOR patterns and testing methodology.

### Phase 5 -- Gateway Integration Testing

The integration layer between the application and the payment gateway is a rich attack surface.

**Attack vectors:**

1. **Webhook forgery** -- send fake payment confirmation webhooks without valid signatures
2. **Callback manipulation** -- modify return URLs to inject payment status parameters
3. **3D Secure bypass** -- skip or downgrade 3DS authentication
4. **Token replay** -- reuse payment tokens across orders or accounts
5. **Gateway downgrade** -- force fallback to a less secure payment method
6. **Split payment abuse** -- manipulate partial payment flows

See `references/gateway-testing.md` for provider-specific testing (Stripe, PayPal, Adyen, custom).

### Phase 6 -- Cart Manipulation

The shopping cart is trusted state that feeds into payment calculation. Tamper with it.

**Attack vectors:**

1. **Quantity manipulation** -- negative quantities, zero quantities, fractional quantities
2. **Item substitution** -- change product ID to a cheaper item after price calculation
3. **Shipping fee bypass** -- remove shipping charges, change shipping method to free
4. **Tax evasion** -- manipulate tax calculation via address spoofing or parameter removal
5. **Bundle breaking** -- extract individual items from bundles at bundle pricing
6. **Hidden item injection** -- add items not displayed in the cart UI via API manipulation

See `references/cart-manipulation.md` for cart-specific attack patterns.

### Phase 7 -- Refund and Post-Payment Abuse

After a legitimate payment, test the refund and post-payment flows.

**Attack vectors:**

1. **Full refund on partial return** -- request full refund while returning partial items
2. **Refund to different method** -- redirect refund to attacker-controlled payment method
3. **Double refund** -- submit refund through multiple channels (API, UI, support)
4. **Chargeback + refund** -- get both a merchant refund and a bank chargeback
5. **Subscription manipulation** -- downgrade after using premium features, cancel/resubscribe for trial reset
6. **Digital goods + refund** -- obtain digital delivery then refund the payment

See `references/refund-abuse.md` for refund flow testing methodology.

## Decision Tree -- Attack Surface by Architecture

### Stripe Integration
```
Stripe Checkout (hosted) → Focus on: webhook forgery, callback URL manipulation, metadata tampering
Stripe Elements (embedded) → Focus on: PaymentIntent amount mismatch, client-side amount override
Stripe custom (API direct) → Focus on: server-side amount validation, idempotency key abuse, token replay
```

### PayPal Integration
```
PayPal Standard (redirect) → Focus on: IPN forgery, return URL manipulation, txn_id prediction
PayPal Express/Checkout → Focus on: order amount mismatch, capture vs authorize manipulation
PayPal Braintree (SDK) → Focus on: nonce replay, client token manipulation, amount override
```

### Custom Gateway / Direct Card Processing
```
Custom gateway → Focus on: EVERYTHING -- no provider guardrails. Price manipulation, IDOR, race conditions are all likely.
Direct processing → Focus on: card data handling (PCI scope), amount manipulation, replay attacks
```

### Wallet / Crypto / PIX
```
MercadoPago/PIX → Focus on: emailDesc IDOR, webhook forgery (often no signature), instant settlement race
Binance Pay → Focus on: type confusion, emailDesc IDOR, auth bypass on payment creation
Crypto payments → Focus on: confirmation count bypass, underpayment acceptance, address reuse
```

## Severity Guide

Payment vulnerabilities map to severity as follows:

| Finding | Severity | Justification |
|---------|----------|---------------|
| Price set to zero / negative | **CRITICAL** | Direct financial loss, arbitrary free purchases |
| Payment IDOR (modify others' payments) | **CRITICAL** | Financial impact to other users |
| Webhook forgery (fake payment confirmation) | **CRITICAL** | Full payment bypass |
| Race condition (double-spending) | **CRITICAL** | Direct financial loss, balance manipulation |
| Currency confusion leading to price reduction | **HIGH** | Financial loss, requires specific conditions |
| Coupon stacking / replay | **HIGH** | Revenue loss, business logic flaw |
| Cart quantity manipulation | **HIGH** | Pricing integrity compromise |
| Shipping/tax bypass | **HIGH** | Revenue loss per transaction |
| Payment IDOR (read-only, view others' transactions) | **HIGH** | PII exposure, financial data leak |
| Refund flow manipulation | **HIGH** | Financial loss, requires post-payment access |
| 3DS bypass / downgrade | **HIGH** | Fraud liability shift |
| Order ID enumeration (info leak only) | **MEDIUM** | Information disclosure |
| Trial abuse / subscription manipulation | **MEDIUM** | Revenue loss, lower direct impact |

## Logging Findings

Payment findings MUST be logged immediately due to their severity. Use elliot's findings-tracker:

```bash
# Log a payment vulnerability
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "/api/checkout/create" \
  "idor" \
  "amount" \
  "CRITICAL" \
  "Price manipulation: server accepts client-supplied amount without validation"

# Log technique used
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  "http_repeater" \
  "<target>" \
  "price-manipulation" \
  "success" \
  --notes "Amount field in POST /api/checkout/create is not validated server-side"
```

## Tool Loading

| Tool | Use Case | Load Command |
|------|----------|-------------|
| `http_repeater` | Intercept and modify payment requests | `ToolSearch` -> `select:mcp__hexstrike-ai__http_repeater` |
| `http_intruder` | Race conditions, fuzzing, enumeration | `ToolSearch` -> `select:mcp__hexstrike-ai__http_intruder` |
| `http_set_rules` | Auto-replace tokens, session fixation | `ToolSearch` -> `select:mcp__hexstrike-ai__http_set_rules` |
| `jwt_analyzer` | Payment token analysis | `ToolSearch` -> `select:mcp__hexstrike-ai__jwt_analyzer` |
| `comprehensive_api_audit` | Broad payment API assessment | `ToolSearch` -> `select:mcp__hexstrike-ai__comprehensive_api_audit` |

## Common Payment Endpoint Patterns

```
POST /api/payments/create              — Payment initiation
POST /api/payments/confirm             — Payment verification
POST /api/payments/webhook             — Provider callback
POST /api/checkout                     — Checkout submission
POST /api/cart/update                  — Cart modification
POST /api/coupons/apply                — Coupon application
POST /api/orders                       — Order creation
GET  /api/orders/<id>                  — Order details (IDOR target)
GET  /api/invoices/<id>                — Invoice access (IDOR target)
POST /api/refunds                      — Refund submission
POST /api/subscriptions                — Subscription management
POST /api/payments/*/url               — Payment URL generation (Binance, MercadoPago)
POST /wp-content/themes/*/payment/*.php — WordPress custom payment handlers
POST /api/v1/charge                    — Direct charge endpoints
POST /api/wallet/topup                 — Wallet credit operations
```

## References

| Reference | Coverage |
|-----------|----------|
| `references/payment-idor.md` | IDOR patterns in payment contexts, horizontal/vertical escalation, order/invoice/transaction ID enumeration |
| `references/price-manipulation.md` | Client-side price tampering, negative values, float precision, currency confusion, discount stacking, coupon abuse |
| `references/race-conditions.md` | TOCTOU in payment processing, double-spending, concurrent checkout, thread timing, detection methodology |
| `references/cart-manipulation.md` | Quantity manipulation, item substitution, shipping/tax bypass, bundle breaking, hidden item injection |
| `references/gateway-testing.md` | Webhook forgery, 3DS bypass, callback manipulation, tokenization attacks, provider-specific testing |
| `references/refund-abuse.md` | Refund flow manipulation, double refund, chargeback patterns, subscription abuse, digital goods fraud |
