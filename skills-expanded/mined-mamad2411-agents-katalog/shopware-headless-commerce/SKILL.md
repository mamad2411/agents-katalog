---
name: shopware-headless-commerce
description: Build headless storefronts against the Shopware 6 Store API (6.6+). Use when working with Shopware session/context management (sw-context-token), cart operations (add/update/remove line items, promotions), checkout flow (order creation, payment handling with sync/async redirects), and customer account features (registration, login, addresses, password recovery, order history, wishlists). Covers the stateful/write side of the Store API — not product data fetching (use Frontic for that).
---

# Shopware 6 Store API — Headless Storefront

Procedural guide for building headless storefronts against Shopware 6.6+ Store API. Covers the **stateful/write operations**: context, cart, checkout, and account. For product data, listings, and pages use the Frontic skill instead.

## Architecture

```
Frontic Client  →  Product data, listings, pages, categories (read)
Store API       →  Context, cart, checkout, account, payment (write/session)
```

Both share the same Shopware backend. Frontic handles optimized data delivery; the Store API handles session-bound operations.

## Essential Headers

Every request to `/store-api/*` requires:

| Header | Required | Purpose |
|---|---|---|
| `sw-access-key` | Always | Sales channel API key (from Admin > Sales Channels) |
| `sw-context-token` | After first request | Session token. Persist from every response. |
| `sw-language-id` | Optional | Override language |
| `sw-currency-id` | Optional | Override currency |
| `Content-Type` | For POST/PATCH | `application/json` |

**Critical rule**: Always read and persist the `sw-context-token` from response headers. It can change after login, registration, or context switches.

## Core Workflows

### Guest → Cart → Login → Checkout

```
1. GET  /store-api/context                          → Get anonymous token
2. POST /store-api/checkout/cart/line-item           → Add items to cart
3. POST /store-api/account/login                     → Login (merges guest cart)
   (update stored sw-context-token from response)
4. PATCH /store-api/context                          → Set payment + shipping method
5. POST /store-api/checkout/order                    → Create order
6. POST /store-api/handle-payment                    → Initiate payment
7. If redirectUrl → redirect to provider → return to finishUrl
```

### Guest Checkout (No Account)

```
1. GET  /store-api/context                           → Get anonymous token
2. POST /store-api/account/register { guest: true }  → Register as guest
3. POST /store-api/checkout/cart/line-item            → Add items
4. PATCH /store-api/context                           → Set methods + addresses
5. POST /store-api/checkout/order                     → Create order
6. POST /store-api/handle-payment                     → Handle payment
```

### Payment Redirect Handling

```typescript
const { redirectUrl } = await storeApi('/handle-payment', {
  orderId, finishUrl, errorUrl
})

if (redirectUrl) {
  // Async payment (PayPal, Stripe, etc.) — redirect to provider
  window.location.href = redirectUrl
} else {
  // Sync payment (invoice, prepayment) — show confirmation
  navigateTo('/checkout/finish')
}
```

## Reference Files

- **[Context & session management](references/context.md)**: Headers, context token lifecycle, `GET/PATCH /context`, available languages/currencies/countries/payment methods/shipping methods
- **[Cart operations](references/cart.md)**: Add/update/remove line items, promotion codes, cart structure, calculation pipeline
- **[Checkout & payment](references/checkout.md)**: Order creation, `handle-payment` flow, sync vs async payments, payment retry, order cancellation
- **[Account management](references/account.md)**: Registration (regular + guest + double opt-in), login/logout, profile, addresses, password recovery, order history, wishlist, newsletter

## Common Patterns

### API Client Wrapper

Create a typed wrapper for Store API calls:

```typescript
async function storeApi<T>(
  endpoint: string,
  body?: Record<string, unknown>,
  method: string = 'POST'
): Promise<T> {
  const contextToken = getContextToken() // from cookie/storage

  const response = await fetch(`${SHOPWARE_URL}/store-api${endpoint}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'sw-access-key': SW_ACCESS_KEY,
      ...(contextToken && { 'sw-context-token': contextToken }),
    },
    body: body ? JSON.stringify(body) : undefined,
  })

  // Always persist the (potentially new) context token
  const newToken = response.headers.get('sw-context-token')
  if (newToken) setContextToken(newToken)

  if (!response.ok) {
    const error = await response.json()
    throw new StoreApiError(error)
  }

  return response.json()
}
```

### Error Response Shape

Store API errors follow this structure:

```json
{
  "errors": [
    {
      "status": "400",
      "code": "CHECKOUT__CART_PRODUCT_NOT_FOUND",
      "title": "Not Found",
      "detail": "Product not found",
      "meta": { "parameters": { "productId": "..." } }
    }
  ]
}
```

Handle errors by checking `errors[].code`. Common codes:

| Code | Meaning |
|---|---|
| `CHECKOUT__CART_PRODUCT_NOT_FOUND` | Product ID doesn't exist |
| `CHECKOUT__CUSTOMER_NOT_LOGGED_IN` | Endpoint requires authentication |
| `CHECKOUT__ORDER_PAYMENT_METHOD_NOT_CHANGEABLE` | Payment can't be changed |
| `VIOLATION::*` | Validation errors (missing fields, invalid format) |

### Criteria Object (Filtering & Pagination)

Many list endpoints accept a criteria body:

```json
{
  "limit": 10,
  "page": 1,
  "sort": [{ "field": "createdAt", "order": "DESC" }],
  "filter": [
    { "type": "equals", "field": "active", "value": true }
  ],
  "associations": {
    "stateMachineState": {},
    "deliveries": {}
  }
}
```

### Associations

Load related entities by specifying `associations` in the request body. These can be nested:

```json
{
  "associations": {
    "transactions": {
      "associations": {
        "stateMachineState": {}
      }
    }
  }
}
```
