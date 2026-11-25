---
name: overstock-review
description: Find slow-moving, overstocked and dead stock in ReplenishRadar and the money tied up in it. Use when the seller asks what is not selling, what to stop reordering, where cash is tied up in inventory, what to discount or liquidate, or what the inventory is worth.
---

# Overstock review

Finds stock that is not earning its keep. Read-only.

## Steps

1. Call `rr_list_slow_movers` with `days` set to 90 (the maximum) unless the seller asks for a shorter window. Page with `cursor` while `has_more` is true. Each product has stock on hand, units sold and a `dead_stock` flag: true means held stock with no sale in 12 months; null means the sales history is too short to tell.
2. Call `rr_list_top_sellers` with the same window, so the answer can contrast what sells against what sits.
3. Call `rr_get_inventory_value` for total units and value held.
4. For any product the seller is considering dropping, check `rr_list_suggested_purchase_orders` and `rr_list_recommendations` with its SKU. If ReplenishRadar is still suggesting a reorder for a slow mover, point that out.

## The answer

Lead with the headline number: how many products have had no sale in 12 months, and, when the connection includes costs, the value at cost. Then a table of the slowest products with stock held, units sold in the window, and months of cover at the current rate (stock held divided by monthly sales; say "no sales" rather than dividing by zero).

Value and cost figures appear only when the connection was approved with costs and revenue included. If they are missing, give units and say that value needs that permission.

Suggest, do not decide: products with a `dead_stock` flag are candidates to stop reordering or clear out, but the seller knows about seasonality, new launches and bundles that the numbers cannot show.
