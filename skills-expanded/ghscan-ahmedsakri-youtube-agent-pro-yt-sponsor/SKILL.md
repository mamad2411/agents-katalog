---
name: yt-sponsor
description: >-
  Model sponsorship pricing assumptions, draft a brand reply, and write
  an integration using the creator's view data and proposed deal terms. Use for "a brand emailed me", "how much do I charge", "rate
  card", "sponsorship", "sponsor integration script", or "is this offer
  fair".
---

# yt-sponsor

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Most creators underprice the first deal and then read the sponsor segment like a hostage. This fixes
both: a rate you can defend, and an integration people do not skip.

A tool lives here and it runs.

```bash
python3 "$YT_SKILL_DIR/ratecard.py" --views 12000 --niche tech --placement all
```

## Before you quote

1. Use the available voice profile or creator context (see the operating guide). The integration is read out loud, in the creator's voice. A
   segment in ad-voice is the segment everyone scrubs past.
2. Use the **median of the last 10 videos**, not the best one and not the subscriber count. You are
   selling the views this video will realistically get.

## Pricing

Run `ratecard.py` with the median views and the niche. It returns low / mid / high for the three
placements advertisers actually buy: a mention, an integrated mid-roll (the default, 60-90s), and a
dedicated video. The bundled CPM bands are **illustrative assumptions**, not verified current market
rates. Label the currency and assumptions; replace them with the creator's own deal history or
sourced comparable rates when available. Do not imply the computed range guarantees an offer.

- **The mid** can be a discussion starting point, subject to production costs and deal scope.
- **The high** is the number for exclusivity, a tight deadline, or usage rights (they want to run it
  as an ad). Name those as the reason, not as a favour.
- **The low** is an illustrative range endpoint, not a walk-away floor. A real floor needs the
  creator's costs, usage-rights terms, and preference; do not invent one from this heuristic.

## The reply

Write the response to the brand: thank, confirm the median-views number plainly, quote the mid, and
ask the two questions that decide the real price - exclusivity, and whether they want usage rights.
Short. Brands trust a creator who answers like a business.

## The integration

Write the 60-90 second segment so it survives the retention graph:
- **Place it at a peak, not a cliff** - just after a payoff, never before the hook lands.
- **Make it relevant or make it honest** - "I use this / I do not, but here is the offer".
- **One claim, from the brief, that the creator will actually say** - never invent a product claim.
- **A clean hand-back** to the video so the retention curve recovers.

## What to hand back

- the rate card (three placements, three bands)
- the reply to the brand, ready to send
- the integration script in the creator's voice, with a placement note
- the key unresolved commercial terms and any creator-specified minimum
