---
name: order-triage
description: Summarize the day's orders and surface the ones that need a human — fraud/chargeback signals, address problems, and stuck fulfillments — with a drafted response for each. Use for "go through today's orders" or "anything sketchy come in".
metadata: { "openclaw": { "emoji": "🚦" } }
---

# Order Triage

Most orders need nothing. This skill finds the few that do — likely-fraud, "will bounce back
from the warehouse", and "customer is about to email you" — and hands you a decision plus a
drafted reply, so you spend two minutes instead of scrolling the orders tab.

## When to use (trigger phrases)

Use this skill when the user says:

- "go through today's orders"
- "anything sketchy / high-risk come in?"
- "which orders need me?"
- "triage the queue"
- (scheduled) as the orders section of `daily-store-brief`

## How it works

Read `~/.openclaw/ecom-ops/config.json` (`store`, `apiVersion`). Token from `$SHOPIFY_ADMIN_TOKEN`.

1. **Pull the window.** Default: orders created since the last run (or since midnight local).
   Get financial + fulfillment + shipping + customer fields so you can score without extra calls.
   ```bash
   STORE=$(jq -r .store ~/.openclaw/ecom-ops/config.json)
   VER=$(jq -r .apiVersion ~/.openclaw/ecom-ops/config.json)
   SINCE=$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ)
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders.json?status=any&created_at_min=$SINCE&limit=250&fields=id,name,created_at,total_price,currency,email,financial_status,fulfillment_status,shipping_address,billing_address,customer,tags,note,line_items,shipping_lines" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" | jq '.orders'
   ```

2. **Pull Shopify's own risk signal** for anything not obviously clean. Shopify already scores
   fraud; don't reinvent it:
   ```bash
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders/$ID/risks.json" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" | jq '.risks[] | {recommendation, score, message}'
   ```
   `recommendation` is `accept` / `investigate` / `cancel`. Treat `investigate`/`cancel` as an
   automatic FLAG.

3. **Layer your own heuristics** (any one → FLAG, note *why* — these are signals, not verdicts):
   - **Fraud-lean:** Shopify risk `investigate`/`cancel`; billing country ≠ shipping country;
     shipping address is a known freight forwarder / reshipper; first order + AOV far above your
     norm; expedited shipping on a high-value order; multiple orders same card/email in minutes;
     mismatched name on card vs shipping.
   - **Fulfillment-risk:** missing/partial address (no house number, empty zip), PO box on a
     carrier that won't deliver to it, oversized/HAZMAT SKU to an incompatible method, a SKU on
     the order that's currently out of stock (cross-check `inventory-watch`).
   - **Service-risk:** customer note present ("please deliver before…", "wrong size"), gift order
     flags, duplicate of a very recent order (accidental double-buy), high-LTV repeat customer
     (VIP — handle warmly, fast).

4. **Draft the next move** for each flagged order — the actual message or internal action, not
   just a label. Match the store's voice if a `voice.md` exists in config; otherwise plain,
   friendly, specific. See Output.

5. **Report + optionally route.** Clean orders get a one-line count. Flagged orders get a card
   each. If `alertChannel` is set on a scheduled run, post only the FLAG cards.

## Output

A short header plus one card per flagged order. Example:

```
Orders since midnight: 41 · $3,880 · AOV $94.6 · 39 clean, auto-fulfilling.

⚠ #1042 · $412 · new customer · FRAUD-LEAN
  Signals: Shopify risk = investigate (0.71); bill US / ship NG; expedited; 3.4× your AOV.
  Suggest: hold fulfillment, request card-matching billing confirmation before shipping.
  Draft (to buyer): "Hi Sam — quick check before we ship your order #1042. For security on
  higher-value orders we confirm the billing address matches the card. Can you reply with the
  billing ZIP on file? We'll ship the moment it's confirmed."

⚠ #1039 · $58 · FULFILLMENT-RISK
  Signals: shipping address missing house number ("Main St, Austin TX").
  Suggest: don't ship; get the full line-1.
  Draft: "Hi Priya — we want #1039 to reach you. The street address came through without a
  house/apt number — could you reply with the full line 1? Shipping out as soon as we have it."

★ #1051 · $260 · VIP (7th order, $1.9k lifetime) — no issue, just flagging to prioritize.
```

Do not cancel, refund, or contact anyone automatically. Present; the human decides and sends
(or tells the agent to send via the mail/Slack skill).

## Notes

- **Signals, not judgments.** A country mismatch is common and legitimate (gifts, expats). Never
  auto-cancel; false positives cost you real customers. The agent flags and drafts; you decide.
- Shopify's order-risk data quality depends on your plan and payment provider (Shopify Payments
  gives the richest signal). If `/risks.json` is empty, lean on the heuristics and say so.
- Freight-forwarder detection needs a list — ship-to addresses at known reshipper hubs (parts of
  Portland OR, Miami, Delaware). Keep a `forwarders.txt` in config; don't hardcode a stale list.
- "Your AOV" and "your norm" should come from a trailing baseline (reuse `daily-store-brief`'s
  numbers), not a guess. Don't invent a threshold.
- Requires `read_orders` and `read_customers` scopes. This is read + draft only; no write scopes
  needed for triage itself.
