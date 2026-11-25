---
name: order-lifecycle
description: Order state machine, fulfillment flow, cancellation handling, refund processing, and notification triggers for e-commerce applications.
invoke_when: Building or modifying order management, fulfillment, cancellation, refund, or return functionality.
---

# Order Lifecycle

## Order State Machine

Orders follow a strict state machine. Never skip states or allow arbitrary transitions.

```
                    ┌─────────┐
                    │ CREATED │
                    └────┬────┘
                         │ payment initiated
                    ┌────▼─────────┐
                    │ PAYMENT_PENDING│
                    └────┬─────────┘
                    ┌────┴────┐
               payment   payment
               success    failed
                    │         │
             ┌──────▼──┐  ┌──▼───────┐
             │CONFIRMED │  │ FAILED   │
             └────┬─────┘  └──────────┘
                  │ fulfillment started
             ┌────▼──────┐
             │ PROCESSING │
             └────┬──────┘
                  │ shipped
             ┌────▼────┐
             │ SHIPPED  │
             └────┬────┘
                  │ delivered
             ┌────▼─────┐
             │ DELIVERED │
             └──────────┘
```

### Allowed transitions:
| From | To | Trigger |
|------|----|---------|
| CREATED | PAYMENT_PENDING | Checkout initiated |
| PAYMENT_PENDING | CONFIRMED | Payment success webhook |
| PAYMENT_PENDING | FAILED | Payment failure / timeout |
| CONFIRMED | PROCESSING | Fulfillment started |
| CONFIRMED | CANCELLED | Customer cancellation (before fulfillment) |
| PROCESSING | SHIPPED | Tracking number assigned |
| SHIPPED | DELIVERED | Delivery confirmed |
| DELIVERED | RETURN_REQUESTED | Customer initiates return |
| RETURN_REQUESTED | RETURNED | Return received and inspected |
| Any (post-payment) | REFUNDED | Refund processed |

### Rule: Every state transition is an event
Store transitions in an `order_events` table, not just the current state:

```sql
CREATE TABLE order_events (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  from_state VARCHAR(50),
  to_state VARCHAR(50) NOT NULL,
  triggered_by VARCHAR(100), -- "customer", "system", "admin"
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

This gives you: full audit trail, debugging, analytics, and the ability to reconstruct state.

## Cancellation Rules

- **Before fulfillment (CONFIRMED state)**: Customer can self-cancel. Full refund, automatic.
- **During fulfillment (PROCESSING)**: Customer requests cancellation. Requires manual review (may already be packed/shipped). Partial refund possible.
- **After shipping (SHIPPED)**: Cannot cancel — must wait for delivery then initiate return.
- **After delivery**: Return flow, not cancellation.

### Rule: Cancellation is a request, not an instant action
```
POST /orders/{id}/cancel
-> Returns 202 Accepted (not 200 OK)
-> Creates a CANCELLATION_REQUESTED event
-> Background job processes the cancellation
-> Webhook/notification when cancellation is confirmed or denied
```

## Refund Processing

### Rule: Refunds go through the payment provider
Never adjust balances manually. Always use the payment provider's refund API (Stripe refunds, PayPal refunds, etc.).

### Refund types:
- **Full refund**: Order cancelled before fulfillment, or return accepted
- **Partial refund**: Damaged item, wrong item shipped, price adjustment
- **Store credit**: Alternative to cash refund (customer choice)

### Rule: Refund amount cannot exceed the original payment
This sounds obvious but: if a promo code was applied, the refund maximum is the amount actually charged, not the pre-discount total.

### Rule: Log everything
Every refund must record:
- Amount refunded
- Reason (enum: `CUSTOMER_CANCELLED`, `ITEM_DEFECTIVE`, `WRONG_ITEM`, `NOT_RECEIVED`, `OTHER`)
- Who initiated (customer, support agent, system)
- Payment provider refund ID

## Notification Triggers

Send notifications at these state transitions:

| Transition | Customer Email | Admin Alert |
|-----------|---------------|-------------|
| CONFIRMED | "Order confirmed" with summary | No |
| PROCESSING | "Your order is being prepared" | No |
| SHIPPED | "Your order has shipped" with tracking | No |
| DELIVERED | "Your order has been delivered" | No |
| CANCELLED | "Your order has been cancelled" + refund info | Yes (if post-CONFIRMED) |
| REFUNDED | "Your refund has been processed" | Yes |
| FAILED | "There was an issue with your payment" | Yes |

### Rule: Notifications are async
Never make the state transition wait on email delivery. Publish an event, let a background worker handle notifications. If the email fails, the order state is still correct.

## Database Design

### Minimum tables:
- `orders` — order header (customer, status, totals, timestamps)
- `order_items` — line items (product, quantity, price AT TIME OF ORDER)
- `order_events` — state transitions (audit trail)
- `refunds` — refund records (linked to order and payment)

### Rule: Snapshot prices at order time
`order_items.unit_price` stores the price when the order was placed. NEVER join to the product catalog for pricing on existing orders — prices change.

### Rule: Soft-delete orders
Never hard-delete order records. They're financial records with legal retention requirements.
