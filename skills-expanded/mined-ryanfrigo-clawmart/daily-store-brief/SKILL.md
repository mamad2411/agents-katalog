---
name: daily-store-brief
description: A morning brief for your store — yesterday's sales vs your baseline, stockouts, refunds, unfulfilled orders, and the 3 things actually worth doing today. Use for "give me the store brief" or run it on a schedule before you wake up.
metadata: { "openclaw": { "emoji": "☀️" } }
---

# Daily Store Brief

The one thing to read with coffee. It rolls up the numbers, calls the other skills in this pack
for the details, and — most importantly — ends with a short, ranked "handle these today" list so
the brief drives action instead of just reporting vibes.

## When to use (trigger phrases)

Use this skill when the user says:

- "give me the store brief" / "morning brief"
- "how did the store do yesterday?"
- "what do I need to handle today?"
- (scheduled) run it at, say, 7am and post to the alert channel

## How it works

Read `~/.openclaw/ecom-ops/config.json` (`store`, `apiVersion`, `alertChannel`). Token from
`$SHOPIFY_ADMIN_TOKEN`. This skill *composes* the others — it doesn't duplicate their logic.

1. **Yesterday's sales.** Pull paid orders for the prior local day and aggregate:
   ```bash
   STORE=$(jq -r .store ~/.openclaw/ecom-ops/config.json)
   VER=$(jq -r .apiVersion ~/.openclaw/ecom-ops/config.json)
   MIN=$(date -u -v-1d -v0H -v0M -v0S +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d 'yesterday 00:00' +%Y-%m-%dT%H:%M:%SZ)
   MAX=$(date -u -v0H -v0M -v0S +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d 'today 00:00' +%Y-%m-%dT%H:%M:%SZ)
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders.json?status=any&financial_status=paid&created_at_min=$MIN&created_at_max=$MAX&limit=250&fields=total_price,subtotal_price,line_items,refunds" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" | jq '.orders'
   ```
   Compute: order count, gross revenue, units, AOV. Get refunds issued yesterday (sum refund
   `transactions`) for a net figure.

2. **Baseline it.** A number means nothing alone. Compare to the trailing 7-day and 28-day daily
   average (pull once, cache to `~/.openclaw/ecom-ops/state/baseline.json`, refresh daily). Show
   the delta and whether it's inside normal variance or genuinely off — don't cry "sales down!"
   on a normal Tuesday dip.

3. **Pull the operational sections by calling the pack's other skills** (reuse, don't re-implement):
   - `inventory-watch` → the STOCKOUT + CRITICAL rows (top 3–5 only).
   - `order-triage` → count clean, list only flagged orders needing a human.
   - `refund-assistant` ledger → yesterday's refunds and any emerging reason trend.
   - open fulfillments: orders `paid` + `unfulfilled` older than your SLA (e.g. >24h) — these are
     the ones a customer is about to email about.

4. **Synthesize "today's 3".** This is the value. From everything above, pick the 3 highest-
   leverage actions and order them. Ranking rule of thumb: active lost sales (stockout on a fast
   mover) > money/‑trust at risk (fraud-flag, aging unfulfilled) > growth chores (reviews,
   reorders that aren't yet urgent). Be specific and name the SKU/order.

5. **Deliver.** Print the brief. On a scheduled run, post it to `alertChannel` via the user's
   Slack/Discord/email skill. Keep it skimmable — sections with counts, details collapsed to what
   matters.

## Output

One screen. Numbers first, action last. Example:

```
☀️ Store brief — Tue Jul 1

SALES (yesterday)
  41 orders · $3,880 gross · 96 units · AOV $94.6
  vs 7-day avg $3,410 (+14%) · 28-day avg $3,600 (+8%)  → a good day, within normal upside
  Refunds: 2 · $118

NEEDS ATTENTION
  📦 Stockouts/critical (3): MAT-STD sold out (was 6/day — losing sales) · CBL-USBC ~5d cover ·
     HERO-KIT ~7d cover
  🚦 Flagged orders (2): #1042 $412 fraud-lean (hold) · #1039 bad address (get line-1)
  ⏳ Unfulfilled >24h (4): #1017, #1019, #1021, #1023 — oldest is 41h
  ↩️ Refund trend: 2 of last 5 returns are "wrong size" on GRIP-BLK — check the size chart?

TODAY'S 3
  1. Reorder MAT-STD now — it's out and it was your #1 mover (run reorder-logic).
  2. Ship the 4 aging orders (or tell me why they're held) — SLA breach on #1017.
  3. Decide on #1042 ($412 fraud-lean) — draft to confirm billing is ready to send.
```

## Notes

- **Read-and-report.** The brief never ships, refunds, reorders, or cancels — it tells you to,
  with the details ready. Each recommended action is a separate, explicit step you (or another
  skill) take on purpose.
- "Down vs up" needs a baseline, not a hunch. The 7/28-day averages are what keep this from
  false-alarming on normal daily variance or over-celebrating a fluke. If there's no baseline
  yet (first runs), say the numbers are un-baselined rather than inventing a comparison.
- It's a composition skill: it's only as good as `inventory-watch` / `order-triage` /
  `refund-assistant`, which must be installed alongside it. If one is missing, run the section it
  can and note what it skipped.
- Time zone matters — "yesterday" should be *your store's* day. Set the machine/OpenClaw timezone
  correctly or the sales window will be off by hours.
- Requires `read_orders`, `read_inventory`, `read_products` (transitively, via the skills it
  calls). Posting to a channel uses the user's own Slack/Discord/mail skill.
