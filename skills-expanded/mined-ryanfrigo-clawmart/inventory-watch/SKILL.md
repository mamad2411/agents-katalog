---
name: inventory-watch
description: Watch stock levels across your catalog and alert when SKUs cross a low-stock threshold, ranked by how fast they're selling so you act on the ones that matter first. Use for "what's low", "am I about to stock out", or a scheduled stock sweep.
metadata: { "openclaw": { "emoji": "📦" } }
---

# Inventory Watch

Surface the SKUs that are actually at risk — not just "below 10 units", but "below 10 units and
selling 4 a day". A flat threshold treats a dead SKU and your hero product the same; this ranks
by days-of-cover so you triage the fires first.

## When to use (trigger phrases)

Use this skill when the user says:

- "what's running low?"
- "am I about to stock out on anything?"
- "check inventory" / "run a stock sweep"
- "which SKUs need attention?"
- (scheduled) as the stock check inside `daily-store-brief`

## How it works

Read `~/.openclaw/ecom-ops/config.json` for `store`, `apiVersion`, `primaryLocationId`,
`lowStockThresholds` (a map of `sku → units`, with a `default`), and `leadTimeDaysDefault`.
Token comes from `$SHOPIFY_ADMIN_TOKEN`.

1. **List variants + current stock.** Pull products and their variants, then read live inventory
   levels for the primary location. REST works, but on a catalog over a few hundred variants the
   GraphQL Admin API is far fewer calls:
   ```bash
   STORE=$(jq -r .store ~/.openclaw/ecom-ops/config.json)
   VER=$(jq -r .apiVersion ~/.openclaw/ecom-ops/config.json)
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/graphql.json" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" \
     -H 'Content-Type: application/json' \
     -d '{"query":"{ productVariants(first:250){ edges{ node{ sku displayName inventoryQuantity } } pageInfo{ hasNextPage endCursor } } }"}'
   ```
   `inventoryQuantity` is the sellable on-hand at all locations; if you run multiple locations,
   query `inventoryItem { inventoryLevels }` and filter to `primaryLocationId` instead.

2. **Compute velocity** the same way `reorder-logic` does — trailing 30-day units sold per SKU
   ÷ 30. Cache it if you already ran reorder-logic this session; don't re-pull orders twice.

3. **Classify each SKU:**
   - `days_cover = on_hand / velocity` (∞ if velocity is 0).
   - **STOCKOUT** — `on_hand ≤ 0`.
   - **CRITICAL** — `days_cover < lead_time` (you will stock out before a reorder can land).
   - **LOW** — `on_hand ≤ threshold` for that SKU (absolute floor, catches slow movers with
     small safety stock).
   - **OK** — everything else. Don't list OK items unless asked.

4. **Rank** by severity, then by velocity descending within a tier. A CRITICAL hero SKU sits
   above a CRITICAL long-tail SKU. Skip velocity==0 items from CRITICAL (they can't "run out"
   on a timeline) but still show them under LOW so dead-but-zero stock is visible.

5. **Alert.** Return the table. If `alertChannel` is set and this run is scheduled/unattended,
   post the STOCKOUT + CRITICAL rows there (via the user's `slack`/`discord`/email skill). Only
   alert on *newly* crossed thresholds if a prior snapshot exists at
   `~/.openclaw/ecom-ops/state/inventory-last.json` — don't re-nag daily about the same known-low
   SKU. Write the fresh snapshot after alerting.

## Output

A ranked table, worst first, with the action implied. Example:

```
🔴 STOCKOUT (2)
  MAT-STD "Standard Mat"        0 on hand   ·   6.0/day   ·   was selling — lost sales now
  CBL-USBC-2M "USB-C 2m"        0 on hand   ·   2.1/day

🟠 CRITICAL — will stock out before reorder lands (3)   [lead time 21d]
  HERO-KIT "Starter Kit"       31 on hand   ·   4.4/day   ·   ~7d cover   → reorder today
  CBL-USBC "USB-C 1m"          18 on hand   ·   3.4/day   ·   ~5d cover   → reorder today
  GRIP-BLK "Grip Black"        26 on hand   ·   1.9/day   ·  ~14d cover

🟡 LOW — below floor (2)
  HUB-7PORT "7-Port Hub"        8 on hand   ·   1.1/day   ·  threshold 15
  DECAL-LT "Decal (LE)"         3 on hand   ·   0.0/day   ·  slow mover, no urgency

3 items need a PO now. Run reorder-logic to size them, or say "build the PO".
```

## Notes

- **Read-only.** This never changes stock counts. It reads inventory and reports; adjustments
  happen in Shopify or via a separate, explicitly-invoked action.
- "On hand" ≠ "sellable" if you oversell or hold committed units for open orders. Shopify's
  `available` already nets out committed; if you use a 3PL/OMS as source of truth, point the
  skill at that API instead and keep the same classification logic.
- Thresholds are a floor, not the whole story — the days-of-cover math is what catches a fast
  mover that's technically "above threshold" but 4 days from zero.
- Needs a custom app with `read_products` + `read_inventory` (and `read_orders` for velocity).
  Rate limits: REST ~2 req/s; GraphQL is cost-based (1000-point bucket) — the bulk query above
  keeps you well under it.
- Multi-location stores: decide whether "low" means low at the fulfillment location or low in
  total. Set `primaryLocationId` and be explicit; totals hide a location that's already empty.
