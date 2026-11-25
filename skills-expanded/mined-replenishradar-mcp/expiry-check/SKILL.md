---
name: expiry-check
description: Find stock that is likely to expire before it sells in ReplenishRadar. Use when the seller asks what is expiring or about to expire, which lots are at risk, about best-by or expiration dates, Amazon FBA removal windows for dated products, whether a product will sell through before it expires, or when to send the next shipment of a dated product.
---

# Expiry check

For sellers of dated products (food, supplements, cosmetics): which lots are expected to be left unsold when they become unusable, and what to do about one product. Read-only.

## Steps

1. **Start with the whole catalog.** Call `rr_list_expiring_lots`. Page with `cursor` while `has_more` is true. Rows come soonest first. Pass `status` set to `past_cutoff` for lots that have already reached their unusable date, or `at_risk` for lots expected to be left unsold when they reach it.
2. **Read the summary before saying "nothing is expiring".** An empty list is not a clean bill of health. The summary counts what could not be scored: lots at locations with no sales rate, stock with no lot recorded, lots with no expiry date, disconnected stores and positions that could not be read. Report those counts when they are not zero.
3. **Go deep on one product when asked.** Call `rr_get_product_expiry_risk` with the `sku` (or the `item_id` if you have it). It shows, location by location, each lot's expiry date, the date it becomes unusable, the units remaining and the units at risk.
   - A product that returns `requires_expiration` false is not tracked for expiry. Say so; do not report it as safe.
   - A location marked `no_demand` has no sales rate, so its lots are not scored. Name the location and say the risk there is unknown.
   - At Amazon FBA the answer also says when the next shipment should arrive so the old stock is nearly sold through without running out. When both cannot hold, it gives the latest date that keeps the product in stock and the units likely still there then. Pass that on as the trade-off it is.

## The answer

Lead with the count and the soonest date: "4 lots are at risk, the first becomes unusable on 12 March." Then a table: product, location, lot, expiry date, unusable date, units at risk. Put lots already past their unusable date first.

## Rules that keep the answer honest

- These are estimates. Amazon does not report which lot it sold, so the lots on hand are inferred from arrival order. Say "probably still on hand", not "is on hand".
- The unusable date is earlier than the printed expiry date: Amazon's removal window at FBA, the product's days-to-consume elsewhere. Use the unusable date when you say how long the seller has.
- Cost at risk appears only when the connection was approved with costs included. Leave money out otherwise.

## Follow-ups the seller may ask for

- "What should I do with it?" Slow sales are the usual cause. Use the overstock-review skill for the product's sales rate and the cash tied up.
- "Should I reorder this product?" Use the sku-deep-dive skill, and mention the lots at risk beside the reorder advice so the seller does not buy on top of stock that will not sell through.
