---
name: review-requests
description: Find orders that were delivered, wait the right amount of time, and draft a personalized review request per customer — without spamming repeat buyers or people who've opted out. Use for "chase reviews" or "who's due for a review ask".
metadata: { "openclaw": { "emoji": "⭐" } }
---

# Review Requests

Post-purchase reviews are the cheapest social proof you'll ever get, but the ask has to land at
the right moment (after they've *used* the thing, not when it ships) and never feel like spam.
This skill picks the right customers, at the right time, with a message that references what they
actually bought.

## When to use (trigger phrases)

Use this skill when the user says:

- "chase reviews" / "send review requests"
- "who's due for a review ask?"
- "ask my recent customers for reviews"
- (scheduled) a daily/weekly review sweep

## How it works

Read `~/.openclaw/ecom-ops/config.json` — `reviewDelayDays` (days after delivery to ask,
default 5), `reviewPlatform` (`judgeme` | `loox` | `okendo` | `yotpo` | `shopify-email` | `plain`),
`store`, `apiVersion`. Token from `$SHOPIFY_ADMIN_TOKEN`.

1. **Find delivered orders in the eligible window.** Delivery beats "fulfilled" — asking before
   it arrives kills your response rate. Use the fulfillment's `shipment_status`:
   ```bash
   STORE=$(jq -r .store ~/.openclaw/ecom-ops/config.json)
   VER=$(jq -r .apiVersion ~/.openclaw/ecom-ops/config.json)
   SINCE=$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders.json?status=any&fulfillment_status=fulfilled&created_at_min=$SINCE&limit=250&fields=id,name,email,customer,line_items,fulfillments" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" \
     | jq '.orders[] | {name, email, delivered: [.fulfillments[]?|select(.shipment_status=="delivered")|.updated_at], items:[.line_items[].title]}'
   ```
   Eligible = delivered ≥ `reviewDelayDays` ago AND ≤ ~30 days ago (stale asks feel odd). If
   `shipment_status` is null (carrier doesn't report delivery), fall back to
   `fulfilled_at + typical_transit_days` as an estimated delivery date and note the estimate.

2. **Apply suppression rules** — this is what separates a request from spam:
   - Skip anyone in `~/.openclaw/ecom-ops/state/review-suppress.txt` (opted out / already asked).
   - Ask **once per customer per window**, not once per order — a 3-order customer gets one ask.
   - Skip customers with an open support ticket, a refund, or a flagged order — don't ask an
     unhappy customer for a public review; route them to support instead.
   - Respect the platform's own dedupe if you're handing off to Judge.me/Loox (see step 4).

3. **Personalize the ask.** Reference the actual product(s) and, if it's a repeat customer, say
   so warmly. One clear CTA (the review link). Keep it short; offer an incentive only if the
   store's policy allows it *and* the platform permits incentivized reviews with disclosure.

4. **Send via the configured platform.** Prefer the review app the store already runs — Judge.me,
   Loox, Okendo, and Yotpo have their own request scheduling/APIs and handle unsubscribes and
   review-link tokens for you; in that case this skill's job is to *verify coverage and flag gaps*
   (orders the app missed), not to send a parallel email. For `plain`/`shopify-email`, draft the
   message and hand it to the user's mail skill (e.g. `himalaya`) — but **draft only**; sending
   bulk email is human-confirmed.

5. **Record** who was asked in `~/.openclaw/ecom-ops/state/review-asked.csv`
   (`date,order,email,platform`) so the next run suppresses them.

## Output

A list of eligible customers with a personalized draft each, plus who was skipped and why.
Example:

```
Eligible for a review ask (delivered ≥5d, not previously asked): 3
Skipped: 4 (2 already asked · 1 had a refund · 1 opted out)

→ #1031 · dana@… · delivered 6d ago · bought "Standard Mat"
  "Hi Dana — hope the Standard Mat's working out! If you've had a few days with it, a quick
   review would genuinely help other folks decide: [review link]. Thanks for the support. 🙏"

→ #1028 · lee@… · delivered 9d ago · 3rd order (VIP) · bought "USB-C 1m", "7-Port Hub"
  "Hi Lee — thanks for coming back again! When you've had a chance to try the new hub, we'd love
   a quick review: [review link]. Really appreciate you. "

→ #1024 · sam@… · delivered 5d ago · bought "Grip Black"
  "Hi Sam — how's the Grip holding up? A short review would mean a lot and helps the next person
   choose: [review link]. Thank you!"

Say "send via himalaya" to dispatch, or "these look good, log them" to record without sending.
```

## Notes

- **Draft-and-confirm for email; never blast.** Bulk-emailing your list unattended is how you
  land in spam and burn deliverability. Sending is always human-confirmed, and every message must
  honor unsubscribe/opt-out (CAN-SPAM / your local equivalent). The suppression list is not
  optional.
- Don't fish for only-positive reviews or hide the link from unhappy customers to game your
  rating — asking everyone eligible and routing complaints to support is both more honest and
  more durable. No fake or incentivized-without-disclosure reviews.
- If you already run Judge.me/Loox/Okendo/Yotpo, let it own sending; use this skill to catch the
  orders it missed rather than double-asking. Two review emails from two systems is the fastest
  way to look amateur.
- Delivery detection depends on the carrier reporting back to Shopify. When it doesn't, you're
  estimating — say so, and lean toward waiting a bit longer rather than asking too early.
- Requires `read_orders` + `read_customers`. Sending uses whatever channel skill the user has
  configured; this pack does not send on its own.
