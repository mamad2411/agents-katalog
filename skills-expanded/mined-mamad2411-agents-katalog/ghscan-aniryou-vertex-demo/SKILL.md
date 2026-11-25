---
apiName: dispute_triage
displayName: "Dispute triage"
version: 1
description: >
  Use when a customer disputes an order or asks about cancellations, refunds, or
  returns.
appliesTo:
  objectTypes: [Dispute, SalesOrder, DeliveryOrder]
  linkTypes:   [deliveryRaisesDispute]
  actions:     [raiseException]
invokes:       [raiseException]
reads:
  objectTypes: [Dispute, SalesOrder, DeliveryOrder]
  datasources: [sap]
---
# Dispute Triage

Goal: triage a disputed order against policy and route it correctly.

Steps:
1. Look up the order with `ask_orders` and confirm its current status.
2. Use `search_policies` to find the dispute / cancellation / refund rules that apply.
3. CANCELLED or CLOSED orders cannot be re-flagged — explain the policy instead.
4. For an OPEN disputed order that meets the policy bar, `flag_order_for_review`
   with reason "customer dispute" so a human can adjudicate.
5. Return the policy citation you relied on.
