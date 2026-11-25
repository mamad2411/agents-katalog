---
name: ce-orders
description: Commerce Engine order management - create orders, list/detail, shipment tracking, payment status, cancellation, and refunds.
license: MIT
allowed-tools: Bash
metadata:
  author: commercengine
  version: "1.0.0"
---

> **LLM Docs Header**: All requests to `https://llm-docs.commercengine.io` **must** include the `Accept: text/markdown` header (or append `.md` to the URL path). Without it, responses return HTML instead of parseable markdown.

# Order Management

> **Prerequisite**: Order creation requires a cart with items and addresses. See `cart-checkout/`.

## Quick Reference

| Task | SDK Method |
|------|-----------|
| Create order | `sdk.order.createOrder({ cart_id, payment_method? })` |
| List orders | `sdk.order.listOrders({ page, limit })` |
| Get order detail | `sdk.order.getOrderDetails({ order_number })` |
| Get shipments | `sdk.order.listOrderShipments({ order_number })` |
| Get payments | `sdk.order.listOrderPayments({ order_number })` |
| Payment status | `sdk.order.getPaymentStatus(orderNumber)` — **takes a plain string, not `{ order_number }`** |
| Retry payment | `sdk.order.retryOrderPayment({ order_number }, { payment_method })` |
| Cancel order | `sdk.order.cancelOrder({ order_number }, { cancellation_reason, refund_mode })` |
| Get refunds | `sdk.order.listOrderRefunds({ order_number })` |

> **Note**: Returns are managed by the brand admin (Admin Portal), not the storefront. Customers can **cancel** within the cancellation window (`is_cancellation_allowed`); the admin then decides whether to schedule a return shipment or issue a direct refund. The default behavior is to refund if cancelled within the window. Return/replacement request APIs for storefront are under development.

## Decision Tree

```
User Request
    │
    ├─ "Place order" / "Checkout"
    │   └─ sdk.order.createOrder() → handle payment_info
    │       → See cart-checkout/ for full checkout flow
    │
    ├─ "My orders" / "Order history"
    │   └─ sdk.order.listOrders({ page, limit })
    │
    ├─ "Order detail" / "Order #123"
    │   └─ sdk.order.getOrderDetails({ order_number })
    │
    ├─ "Track shipment"
    │   └─ sdk.order.listOrderShipments({ order_number })
    │       → tracking_url, awb_no, status, eta_delivery
    │
    ├─ "Payment failed" / "Retry"
    │   ├─ Check → sdk.order.getPaymentStatus(orderNumber)
    │   └─ Retry → sdk.order.retryOrderPayment({ order_number }, { payment_method })
    │
    └─ "Cancel order"
        ├─ Check is_cancellation_allowed first
        └─ sdk.order.cancelOrder({ order_number }, { ... })
```

## Order Statuses

| Status | Description |
|--------|-------------|
| `draft` | Order created, awaiting payment |
| `confirmed` | Payment successful, order confirmed |
| `processing` | Being prepared for shipment |
| `shipped` | In transit |
| `delivered` | Delivered to customer |
| `cancelled` | Order cancelled |

## Payment Statuses

| Status | Description | Action |
|--------|-------------|--------|
| `pending` | Payment not yet processed | Poll again after delay |
| `success` | Payment successful | Show confirmation |
| `failed` | Payment failed | Check `is_retry_available` |

## Key Patterns

### Create Order from Cart

> See `cart-checkout/references/payment-patterns.md` § "Building Payment Payloads" for all payment_method shapes.

```typescript
const { data: order, error } = await sdk.order.createOrder({
  cart_id: cartId,
  payment_method: {
    payment_provider_slug: "juspay",
    integration_type: "hyper-checkout",
    gateway_reference_id: gatewayRefId,
    return_url: "https://yoursite.com/order/confirm",
    action: "paymentPage",
  },
});

if (order.payment_required) {
  // Use payment_info to redirect or handle payment flow
}
```

### List Orders with Filters

```typescript
const { data, error } = await sdk.order.listOrders({
  page: 1,
  limit: 10,
  sort_by: JSON.stringify({ order_date: "desc" }),
});

// data.orders → OrderList[] (summary view)
// data.pagination → { total_records, total_pages, next_page }
```

### Poll Payment Status

```typescript
async function pollPaymentStatus(orderNumber: string) {
  // Note: getPaymentStatus takes a string, not an object
  const { data, error } = await sdk.order.getPaymentStatus(orderNumber);

  if (data.status === "pending") {
    setTimeout(() => pollPaymentStatus(orderNumber), 3000);
    return;
  }

  if (data.status === "success") {
    showConfirmation(orderNumber);
  } else if (data.is_retry_available) {
    showRetryOption(orderNumber);
  } else {
    showPaymentFailed();
  }
}
```

### Cancel Order

```typescript
// First check if cancellation is allowed
const { data: order } = await sdk.order.getOrderDetails({
  order_number: orderNumber,
});

if (order.is_cancellation_allowed) {
  const { data, error } = await sdk.order.cancelOrder(
    { order_number: orderNumber },
    {
      cancellation_reason: "Changed my mind",
      refund_mode: "original_payment_mode",
      feedback: "Optional feedback",
    }
  );
}
```

### Shipment Tracking

```typescript
const { data, error } = await sdk.order.listOrderShipments({
  order_number: orderNumber,
});

data.shipments.forEach((shipment) => {
  console.log(shipment.status);        // "shipped", "delivered", etc.
  console.log(shipment.tracking_url);  // Courier tracking link
  console.log(shipment.awb_no);        // Air waybill number
  console.log(shipment.eta_delivery);  // Estimated delivery date
});
```

## Common Pitfalls

| Level | Issue | Solution |
|-------|-------|----------|
| CRITICAL | Creating order without address | Cart must have billing/shipping addresses set before `createOrder()` |
| HIGH | Not polling payment status | After gateway redirect, always poll `getPaymentStatus()` |
| HIGH | Showing cancel button when not allowed | Check `is_cancellation_allowed` from order detail first |
| MEDIUM | Not handling multiple shipments | One order can have multiple shipments — iterate `data.shipments` |
| MEDIUM | Missing `return_url` | Must provide `return_url` for payment gateway callback |
| MEDIUM | Building a returns flow on storefront | Returns are admin-managed. Storefront supports cancellation only (`cancelOrder`). Show order/refund status, not a "Request Return" form. |
| LOW | Not filtering orders by status | Use `status[]` query param to show relevant orders per tab |

## See Also

- `cart-checkout/` - Cart management and checkout flow
- `webhooks/` - Real-time order status updates via webhooks

## Documentation

- **Checkout Flow**: https://www.commercengine.io/docs/storefront/checkout
- **My Account - Orders**: https://www.commercengine.io/docs/storefront/my-account
- **API Reference**: https://www.commercengine.io/docs/api-reference/orders
- **LLM Reference**: https://llm-docs.commercengine.io/storefront/operations/create-order
