---
name: post-purchase
description: Use when designing or reviewing what happens after checkout in an online store — packaging inserts and thank-you notes, shipping subscriptions and free-shipping thresholds, return and refund policy, loyalty programs, and cart-abandonment or retargeting timing — e.g. "when should the abandoned-cart email go out", "should we offer free returns", "set up a loyalty program", "what goes in the box".
---

# Post-purchase

Design shipping, returns, loyalty, and re-engagement so each order raises the odds of the next. The wins are timing and sincerity: a reminder sent too early does worse than no reminder, and a coupon attached to a thank-you note cancels the note's benefit.

## When to use

- Reviewing a post-purchase or retention plan
- Abandoned-cart timing, return/refund/shipping policy, packaging inserts, loyalty program

## When not to use

- Cart layout, checkout fields, wallets, or payment-step errors → `checkout-ux` (this skill owns abandonment *email* timing, not the checkout surface)
- Asking for reviews or handling complaints → the `reviews` skill
- Referral mechanics → the `referrals` skill
- Site-wide trust signals (warranties, cost transparency) → the `store-audit` skill

## Inputs

Collect, or state your assumption:

- Abandonment-email timing; what's in the box (inserts, codes)
- Return policy: who pays, when refunded, drop-off options; whether items need inspection
- Loyalty structure (tiers, opt-in vs automatic, reward type)
- Average order value; free-shipping threshold

## Procedure

1. **Abandoned-cart reminder at 24–72 hours.** Never within the first hour: that soon, people become *less* likely to buy than with no reminder. The motive fades over days and is gone within a week, so 24–72 h is the window.
2. **Handwritten thank-you note, nothing attached.** A handwritten note in every order (photocopy works; personalization optional). No discount code or promotion on or with it — that reads as a sales tactic and cancels the effect. Strongest on loyal customers. Optionally scent the packaging for memorability.
3. **Free-shipping subscription with a minimum order.** If order frequency supports it, sell a membership for free delivery (members spent more and bought a wider range; a separate uncited report puts it at over 3× †). Require a minimum order (e.g. $20), or members split purchases into many small orders.
4. **Free, easy returns.** Customers expect free, no-questions returns; the long-term result is higher spend per order and broader baskets. Include a label (or print-at-home), accept the original packaging, offer drop-off points. Shoppers benchmark you against Amazon, and returns/refunds are where others fall short. †
5. **Instant refund when the return ships.** Refund on the carrier scan, not after inspection: satisfaction and loyalty rise, return rates don't. If abuse is a concern, limit to items that don't need inspection (books, sealed consumables, low-value goods) and keep the inspection step for items that must be checked for use or damage (electronics, cosmetics, apparel).
6. **Loyalty: automatic, single tier, threshold reward.** Enroll everyone automatically. One rule ("buy 10, get 1 free") is enough — the study didn't test tiers, so don't add them for their own sake: +29.5% customer value over five years, showing up in retention, not the next quarter. Making the reward variable ("your 11th purchase is 20% or 80% off") drove more repeat behavior in a separate opt-in study — its "fewer sign up" trade-off doesn't arise under auto-enrollment, and the combination of the two designs is untested.

## Output

The user's plan as a table: element, keep/change, replacement, rule + number. Then the sequence in order (confirmation → box contents → return policy text → loyalty enrollment → abandonment timing).

## Common mistakes

- A 30-minute abandoned-cart email as "standard" — under an hour it backfires.
- A 10% code on the thank-you card — it undermines the note's sincerity; send offers separately.
- Free returns as "something to test" — they're the expected standard.
- Refund after inspection — refund on ship-back; inspect only where needed.
- Tiers because they look sophisticated — the evidence is for one automatic threshold reward; tiers weren't tested.
- Free shipping with no minimum — members fragment orders.

## Quick reference

| Element | Do |
|---|---|
| Abandoned cart email | 24–72 h after; never < 1 h |
| Thank-you note | Handwritten (copy is fine), no promo attached |
| Shipping subscription | Paid membership + minimum order threshold |
| Returns | Free, label included, drop-off options, same packaging |
| Refund timing | Instant on carrier scan (limit to no-inspection items if abuse is a risk) |
| Loyalty | Auto-enroll, one tier, "buy N get 1", variable reward |
| Packaging | Consider a scent for memorability |

† No primary citation on file for this rule — a practitioner tip, not a measured finding.

Evidence and effect sizes: see [reference.md](reference.md).
