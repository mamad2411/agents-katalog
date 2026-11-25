---
name: reorder-logic
description: Recommend how much to reorder and when, from real sales velocity and supplier lead time — so you replenish before you stock out without over-ordering cash into shelves. Use when the user asks "what should I reorder" or "how much of X do I buy".
metadata: { "openclaw": { "emoji": "🔁" } }
---

# Reorder Logic

Turn sales velocity + supplier lead time into a concrete purchase order recommendation. The
goal is a boring, defensible number: enough to not stock out before the next shipment lands,
without parking cash in inventory you won't sell for months.

## When to use (trigger phrases)

Use this skill when the user says:

- "what should I reorder?"
- "how many units of SKU-XYZ should I buy?"
- "am I about to stock out on anything?"
- "build me a PO for [supplier]"
- "what's my reorder point on [product]?"

## How it works

Read config from `~/.openclaw/ecom-ops/config.json` (store, `apiVersion`, `leadTimeDaysDefault`,
`safetyDaysDefault`, `primaryLocationId`) and the token from `$SHOPIFY_ADMIN_TOKEN`.

1. **Pull sales velocity.** Sum units sold per variant over a trailing window (default 30 days;
   use 60–90 for slow movers). One order can have many line items, so aggregate by `sku` /
   `variant_id`, not by order.
   ```bash
   STORE=$(jq -r .store ~/.openclaw/ecom-ops/config.json)
   VER=$(jq -r .apiVersion ~/.openclaw/ecom-ops/config.json)
   SINCE=$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders.json?status=any&financial_status=paid&created_at_min=$SINCE&fields=line_items,created_at&limit=250" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" \
     | jq -r '.orders[].line_items[] | [.sku, .quantity] | @tsv' \
     | awk -F'\t' '{s[$1]+=$2} END{for(k in s) print k"\t"s[k]}'
   ```
   Paginate via the `Link` header (`rel="next"` + `page_info`) — a 30-day window on a real store
   is many pages. Exclude cancelled/refunded quantities so velocity isn't inflated.

2. **Compute daily velocity.** `velocity = units_sold / window_days`. If the product had a
   stockout inside the window, its true velocity is *higher* than observed — note that and, if
   you know the out-of-stock days, divide by in-stock days instead. This is the #1 way naive
   reorder math under-buys bestsellers.

3. **Get on-hand.** For each variant, resolve `inventory_item_id`, then read available at the
   primary location:
   ```bash
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/inventory_levels.json?inventory_item_ids=$IIDS&location_ids=$LOC" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" | jq '.inventory_levels'
   ```
   Add inbound-but-unreceived units if the user tracks POs (ask; Shopify doesn't model this natively).

4. **Reorder point (when to buy).**
   `reorder_point = (velocity × lead_time_days) + safety_stock`
   where `safety_stock = velocity × safety_days`. Use the SKU's lead time / safety days if set,
   else the config defaults. If `on_hand ≤ reorder_point`, it needs a PO **now**.

5. **Order quantity (how much).** Order up to a target coverage window (default: cover
   `lead_time + review_cycle`, commonly 45–60 days):
   `order_qty = ceil((target_days × velocity) − on_hand − inbound)`
   Then round to the supplier's case pack / MOQ (ask or read from config) and never go below
   MOQ. Cap at what clears before expiry for perishables.

6. **Sanity-check the cash.** Multiply `order_qty × unit_cost` per line and show a PO subtotal.
   Flag any single line > 40% of the PO so the user notices concentration risk.

## Output

A per-supplier PO table plus a one-line rationale each. Example:

```
Supplier: Shenzhen Widgets · lead time 21d · safety 10d · target coverage 50d

SKU        On hand  Inbound  30d velocity  Days cover  Reorder pt  ORDER  Unit $  Line $
CBL-USBC   18       0        3.4/day       5.3d ⚠      106         200*    2.10    420.00   *rounded to 100-pack MOQ
HUB-7PORT  240      0        1.1/day       218d        44          0       —       —        healthy, skip
MAT-STD    9        50       6.0/day       9.8d† ⚠     130         320     4.80    1,536.00 †incl. 50 inbound

PO subtotal: $1,956.00  ·  2 lines need action, 1 healthy
† had a 4-day stockout in the window — real velocity likely ~15% higher; consider +1 case.
```

Then ask: "Want me to draft this as a CSV / email to the supplier?" — but do not send anything
without explicit confirmation.

## Notes

- **This recommends; it does not purchase.** There's no auto-buy. The agent produces a PO the
  human reviews and places with the supplier.
- Velocity is a trailing average — it is blind to launches, promos, and seasonality. For a Q4
  or a known spike, tell the agent the multiplier ("plan for 2× on gift SKUs") rather than
  trusting the 30-day number.
- Requires a Shopify custom app with `read_products`, `read_orders`, and `read_inventory`
  scopes; token in `$SHOPIFY_ADMIN_TOKEN` (never in the config JSON). See the pack README.
- Unit cost and MOQ/case pack aren't reliably in Shopify. Keep them in the config file or a
  `costs.csv` the agent reads; otherwise it will ask.
- Standard REST is a leaky bucket (~2 req/s, 40 burst). On a large catalog, prefer the GraphQL
  Admin API `inventoryItems`/`productVariants` bulk query to cut round-trips.
