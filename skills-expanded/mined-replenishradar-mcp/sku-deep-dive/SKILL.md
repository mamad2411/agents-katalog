---
name: sku-deep-dive
description: Explain one product's stock, sales and forecast in ReplenishRadar. Use when the seller names a SKU or product and asks how much is in stock, where it is, how fast it sells, what demand to expect, whether to reorder it, or why it was not restocked or transferred.
---

# Product deep dive

A full picture of one product from the seller's ReplenishRadar data. Read-only.

## Steps

1. **Find the product.** If the seller gave a name or a partial SKU, call `rr_list_products` with `search`. If several match, ask which one. For an exact Amazon SKU, ASIN or FNSKU question, pass the exact value as `search` with `include_listing_identity` set to `true`.
2. **Stock by location.** Call `rr_get_inventory_position` with the `sku`. Each row is one place the product is held. Report `on_hand`, inbound and `sellable_qty` per location and the total. `available_qty` is null where the channel does not report it (Amazon included); that is not zero.
3. **Sales.** Call `rr_list_sales_history` with the `sku` and `granularity` set to `month` for the trend over the last 12 months. For the last few weeks, use the default daily rows with `days` up to 90.
4. **Forecast.** Call `rr_get_demand_forecast` with the `sku` (default 30 days; set `window_days` if the seller asks for another horizon). Report the expected demand, whether a seasonal factor is pushing it up or down, and the track record: whether past forecasts beat a simple same-as-last-week baseline, or there is too little history to judge.
5. **Risk and suggested order.** Call `rr_list_stockout_risks` with the `sku`. If the product is not in the result, it was not evaluated (too little history, or excluded from planning); say that rather than calling it safe.
6. **Only if asked:** sales lost to stockouts (`rr_list_lost_sales` lists every product; find this one's row), open orders for it (`rr_list_purchase_orders`, then `rr_get_purchase_order`), alerts (`rr_list_alerts` with `sku`), or why it was not moved between locations (`rr_list_transfer_decisions` with `sku`).

## The answer

Start with the one-line verdict, for example "120 sellable across 2 locations, selling about 8 a day, expected to run out in about 15 days; ReplenishRadar suggests ordering 240." Then the location table, the sales trend in a sentence, and the forecast with its track record. Where the app can draw one, offer a small chart of the monthly sales.

Treat forecasts as estimates. If the track record says the forecast has not beaten the baseline, say so plainly.
