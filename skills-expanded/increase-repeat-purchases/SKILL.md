---
name: increase-repeat-purchases
description: Use when someone wants more customers to come back and buy again — "repeat rate is low", "improve retention", "get a second order", "customers buy once and disappear", "what should our post-purchase flow do" — for any online store.
---

# Increase repeat purchases

Turn "only 12% buy again" into a ranked backlog. Leave the how-to and the papers in the Depth skills. Several effects show up in retention over years, not in next month's numbers — say so. Every number is what a cited study measured in its own context; do not turn it into a forecast for the user's repeat rate.

## When to use

- The user names repeat rate, retention, lifetime value, or "second order" as the goal
- Reviewing what happens after checkout: emails, box contents, returns, loyalty

## When not to use

- First purchase → `increase-conversion`; order size → `increase-aov`
- Cart and payment-step UX → `checkout-ux`; abandonment *email* timing stays here via `post-purchase`
- Review solicitation and complaint handling in depth → `reviews`; referral mechanics → `referrals`

## Inputs

Collect, or state your assumption:

- Product and how long it takes to judge (instant vs weeks)
- Post-purchase emails: what is sent, when, first question asked
- Box contents (inserts, codes, packaging)
- Return and refund policy; loyalty program (opt-in or automatic, tiers, reward type)
- Abandoned-cart email timing; whether the store replies to reviews

## Procedure

Walk each check; include applicable levers the user didn't mention; list the rest as considered.

1. **Loyalty: automatic, single tier, threshold reward.** Enroll everyone; one rule ("buy 10, get 1 at no cost"). Effect is in multi-year retention. Depth: `post-purchase`.
2. **Feedback request with a positive open-ended first question.** "What did you enjoy most?" before any rating. Depth: `reviews`.
3. **Ask for reviews at 9–13 days**, later for products that take weeks to judge. Measured on review volume, not repeat purchase; it is the delivery vehicle for step 2. Depth: `reviews`.
4. **Handwritten thank-you note, nothing attached.** A discount on the note cancels the effect. Depth: `post-purchase`.
5. **Instant refund when the return ships.** Carrier scan, not after inspection, for items that don't need inspection. Depth: `post-purchase`.
6. **Free, easy returns.** Depth: `post-purchase`.
7. **Free-shipping membership with a minimum order.** Depth: `post-purchase`.
8. **Reply to every review** — measured on ratings and volume, not repeat. Depth: `reviews`.
9. **Abandoned-cart reminder at 24–72 h**, never within the hour. Depth: `post-purchase`.
10. **Referrals as the next step** once repeat customers exist: friend's benefit as the headline. Depth: `referrals`.
11. **Rank.** Note which effects are long-horizon (loyalty) versus immediate (email timing, refund timing). Cheap changes ahead of program builds at equal effect.

## Output

| # | Finding | Change | Measured effect (study context) | Horizon | Depth |
|---|---|---|---|---|---|
| 1 | Opt-in tiered points | Auto-enroll, single "buy 10, get 1" | +29.5% customer value over 5 years | Long | `post-purchase` |
| … | | | | | |

Then: what already complies. Each effect was measured on its own; don't add them up. Ship the top two or three, measure, then take the next.

## Common mistakes

- Inventing a lift ("could double repeat rate") — quote the study's number and its context.
- Building a replenishment sequence first — reasonable, but not in this evidence.
- Making the loyalty program visible but still opt-in — the finding is automatic enrollment.
- Keeping the discount on the thank-you note — it cancels the note's effect.
- Judging the loyalty program on next quarter's numbers — the effect is in multi-year retention.

## Quick reference

| Lever | Depth | Horizon |
|---|---|---|
| Auto-enroll single-tier loyalty | `post-purchase` | Long |
| Positive open-ended first question | `reviews` | Immediate |
| Review ask at 9–13 days | `reviews` | Immediate |
| Handwritten note, no promo | `post-purchase` | Immediate |
| Refund on carrier scan; free returns | `post-purchase` | Immediate / ongoing |
| Abandoned-cart email 24–72 h | `post-purchase` | Immediate |
| Referral ask, friend's benefit first | `referrals` | Next |

Evidence and effect sizes: see [reference.md](reference.md).
