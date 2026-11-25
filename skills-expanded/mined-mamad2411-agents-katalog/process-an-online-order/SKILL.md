---
name: process-an-online-order
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Review an online order and move it to the correct next status for fulfillment, hold, cancellation, or refund.

## Preconditions

- You have access to the store admin or order management system.
- The order exists and has a visible payment, customer, item, and shipping status.
- You know fraud, fulfillment, and cancellation rules for the store.

## Steps

1. **Open the order.** [BRANCH: Shopify | generic] open the order in Shopify Orders, or search the order number in the order system. → *Expect:* the full order record is visible.
2. **Check payment status.** Confirm paid, authorized, pending, refunded, or failed status. → *Expect:* payment readiness is clear.
3. **Review fraud and risk signals.** Check risk score, billing-shipping mismatch, high-value items, and unusual notes. → *Expect:* the order is safe to fulfill or needs review.
4. **Verify inventory and fulfillment status.** Confirm items are in stock and not already fulfilled. → *Expect:* the order can move forward without duplication.
5. **Check customer and shipping details.** Review address validation, delivery method, and customer messages. → *Expect:* fulfillment has a usable address and instructions.
6. **Choose the next action.** [BRANCH: fulfill | hold | cancel] send to fulfillment, place a review hold, or cancel according to policy. → *Expect:* the order status matches the decision.
7. **Notify the customer if needed.** Send a concise update for holds, address questions, cancellations, or delays. → *Expect:* the customer knows any required next step.

## Decision points

- If payment is pending or failed → do not fulfill until payment is captured or corrected.
- If fraud risk is high → hold the order and follow fraud review policy.
- If inventory is unavailable → offer delay, substitution, cancellation, or refund according to policy.

## Failure modes & recovery

- **F1 Duplicate fulfillment:** detect tracking or fulfilled status already exists → stop and reconcile before shipping again.
- **F2 Bad address:** detect carrier validation failure → contact customer for correction before fulfillment.
- **F3 Payment not captured:** detect authorized-only or failed payment → capture if authorized by policy or hold the order.

## Verification

The order has a documented next status, valid payment decision, usable fulfillment information, and customer communication if action is required.

## Variations

- Subscription order: check renewal status and subscription rules before canceling.
- B2B order: verify purchase order, tax exemption, and account terms.
- Local pickup: confirm pickup location and customer instructions instead of shipping.

## Safety & privacy

Medium risk because orders involve payment, addresses, and customer data. Use only approved systems and disclose order details only to authorized staff or the customer.
