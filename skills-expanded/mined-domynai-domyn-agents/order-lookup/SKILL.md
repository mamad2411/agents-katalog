---
name: order-lookup
description: How to look up an order and read its status back to a customer. Use before calling get_order_info or get_customer_orders.
version: "1.0"
enforcement: advisory
metadata:
  requires:
    tools: [get_order_info, get_customer_orders]
---

## What you need before looking anything up

An order id, or a user id you can list orders for. If you have only the user id,
call `get_customer_orders` first and ask the customer which one they mean when it
returns more than one — do not pick the newest and hope.

## Reading a status

`get_order_info` returns a status and a tracking number. Translate it; the raw
value is internal vocabulary:

| status | what to tell the customer |
|---|---|
| `processing` | not yet handed to the courier — still changeable |
| `shipped` | with the courier, tracking number is live |
| `delivered` | the courier recorded it as delivered; if the customer disagrees, this is a claim, not a lookup |

Always give the tracking number with a `shipped` status. A status without a
tracking number leaves the customer with nothing to do.

## When the answer is a refund

Establish the delivery facts first, then read `refund-policy` before deciding.
