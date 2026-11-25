---
name: weekly-reorder-review
description: Plan what to reorder from suppliers using ReplenishRadar. Use when the seller asks what to reorder or restock, what to buy this week, which purchase orders to place, or wants a reorder plan grouped by supplier.
---

# Weekly reorder review

Builds a reorder plan from the seller's own ReplenishRadar data: what is about to run out, what ReplenishRadar suggests buying, and what is already on order, grouped by supplier. Reading changes nothing. Creating draft orders is a separate step the seller asks for.

## Steps

1. **Check the data is current.** Call `rr_get_data_freshness`. If `primary_concern` says sync, stock or demand is stale, say so in one line at the top of the answer and keep going: a stale plan is still useful when it is labelled. If a store looks disconnected, follow the data-health-check skill after the plan.
2. **Find what is at risk.** Call `rr_list_stockout_risks`, first with `risk_level` set to `critical`, then `high`. Page with `cursor` while `has_more` is true. For each product keep the SKU, days until stockout, daily sales rate and `planned_order.qty`.
   - A product with `name_review_hold` and no `planned_order` has an order waiting on a supplier name review in ReplenishRadar. Report it as "order on hold for review", never as "no order needed".
   - This list leaves out products with too little sales history and products paused or discontinued. An empty list does not mean stock is healthy.
3. **Get the suggested orders.** Call `rr_list_suggested_purchase_orders` (page through all of it). These are ReplenishRadar's suggestions built from risk, demand and supplier reliability. Use their quantities rather than computing your own.
4. **Subtract what is already coming.** Call `rr_list_purchase_orders` with `status` set to `draft,sent`. If an at-risk product is already on an open order, show that order's number and status beside it instead of suggesting it again.
5. **Add supplier context.** Call `rr_list_suppliers` for lead times. A product whose days until stockout is shorter than its supplier's lead time will run out before a new order can arrive: flag it.

## The answer

Group by supplier. For each supplier give a short table: product (name and SKU), days until stockout, suggested quantity, and anything already on order. Put the products that will run out before the lead time first. End with one line on how current the data is.

Keep money out of the answer unless the seller asks for it. Cost and revenue figures appear only when the connection was approved with costs included.

## Turning the plan into orders

Only when the seller asks:

- To create a draft order for a supplier, call `rr_create_purchase_order` with the supplier's `vendor_id`, a `destination_location_id`, and `items` of `{sku, quantity, unit_cost}`. If you do not know the receiving location or a unit cost, ask; do not invent one. The order is created as a draft and nothing goes to the supplier.
- If the plan came from prepared replenishment work (`rr_list_recommendations`), use `rr_preview_recommendation` and then `rr_create_draft_from_recommendation` instead, so the draft stays linked to that work. Pass the `updated_at` from the preview as `expected_updated_at` and a fresh value of your choosing as `idempotency_key`. The recommendation-follow-through skill has the full routine, including what to do when a call is refused.
- Sending an order to a supplier is a separate step. See the purchase-order-follow-through skill.

If a write is refused because the connection cannot make changes, tell the seller they can reconnect ReplenishRadar and tick "make changes" on the sign-in screen. Do not retry the write.
