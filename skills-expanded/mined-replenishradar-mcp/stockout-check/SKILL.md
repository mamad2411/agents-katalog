---
name: stockout-check
description: Check which products are running out or need attention today in ReplenishRadar. Use when the seller asks what is at risk of stocking out, what needs attention, for a morning or daily inventory check, about open alerts, or how the store is doing overall.
---

# Stockout check

A short daily read of the store: what is about to run out, what alerts are open, and whether the numbers can be trusted. Read-only.

## Steps

1. Call `rr_get_inventory_health` for the catalog snapshot: how many products sit at each risk level and how many alerts of each type are active.
2. Call `rr_list_stockout_risks` with `risk_level` set to `critical`, then `high`. Page through each with `cursor` while `has_more` is true.
3. Call `rr_list_alerts` with `status` set to `active`. Use `severity` `critical` first if the list is long.
4. Call `rr_get_data_freshness`. If anything is stale, the risk figures may be out of date; say which.

## The answer

Lead with the count: "3 products are critical, 5 are high risk." Then list the critical products with the days until each runs out and the suggested order quantity (`planned_order.qty`). Keep high-risk products to a short list unless the seller asks for all of them. Mention open critical alerts that are not already covered by the stockout list (for example a sync failure). Close with how current the data is.

## Rules that keep the answer honest

- A product missing from the stockout list is not proven healthy. Products without enough sales history, and products paused or discontinued, are left out. To answer about one product, call `rr_get_inventory_position` for it.
- At an Amazon FBA location `available_qty` is null because Amazon does not report one. Null means not reported, not zero. Use `sellable_qty`.
- Estimated days until stockout is a forecast, not a promise. Say "expected to run out in about 6 days", not "will run out on Friday".

## Follow-ups the seller may ask for

- "What should I order?" Use the weekly-reorder-review skill.
- "Tell me more about this product." Use the sku-deep-dive skill.
- "What happened this week?" Call `rr_get_recent_activity`. It covers the last 7 days unless you pass `days` (up to 30) and returns counts only: alerts created and resolved, purchase orders created and received, sync runs and failures. It contains no money amounts.
- "Is anything about to expire?" Use the expiry-check skill.
- "Mark that alert as seen." Call `rr_acknowledge_alert` with the `alert_id` and an optional `note`. This changes the alert's status and needs the "make changes" permission.
