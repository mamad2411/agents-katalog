---
name: subscription-pricing
description: Use when structuring or reviewing prices for a subscription, membership, recurring plan, or member dues — plan tiers, upgrade paths, pay-per-use vs flat rate, extra-seat or overage pricing, membership perks — e.g. "how should I price Basic vs Pro", "flat monthly or per video", "what should extra seats cost", "how do we get more upgrades", "is a paid membership worth it".
---

# Subscription pricing

Structure recurring prices so people choose a plan, pay the flat rate, and step up a tier. This skill is the delta versus `pricing`, `discounts`, and `post-purchase`. One-off digital products → `digital-product-pricing`.

## When to use

- Designing or reviewing plan tiers and their prices
- Choosing flat-rate vs pay-per-use, or pricing seats, storage, minutes
- Adding a paid membership perk, or rewards for members

## When not to use

- One-off digital products → `digital-product-pricing`
- Shared digit and component rules in isolation → `pricing`
- Wording a plan discount → `discounts`; measuring willingness to pay per month → `price-research`

## Inputs

Collect, or state your assumption: tiers, prices, billing period; any per-unit component; whether members optimize for quality or lowest price; which tier you want people to move to; order/usage frequency.

## Procedure

Only the rules that change for recurring plans. Shared catalogs live in the Depth skills.

1. **Lead with a flat rate that covers what most members want**, priced *above* the pay-per-use equivalent. Keep pay-per-use only as a low-commitment entry. The source study is purchasing professionals buying usage-based services; applying it to consumer memberships is a transfer. Depth: `pricing`.
2. **Put the upgrade path on the same left digit.** No just-below on the lower tier if you want Basic → Pro ($40 → $48, not $39.99 → $48). Depth: `pricing`.
3. **Simplify every component.** Rounded per-seat / per-GB prices, the same ending, no admin fee. Depth: `pricing`.
4. **Paid perk needs a minimum.** A membership that unlocks free shipping or member rates raises spend; without a minimum, members split into many small orders. Depth: `post-purchase`.
5. **Rewards: automatic, single tier, threshold.** Optionally variable; combining variable rewards with auto-enrollment is untested. Depth: `post-purchase`.

Shared, unchanged: quality-led → rounded, price-led or post-trial → just-below (subject to step 2); "for $0" on free trials; abandoned-signup reminder at 24–72 h is an assumption transferred from carts. Depth: `pricing`, `promotions`, `post-purchase`.

## Worked example

Membership site, plan: Basic $9.99, Pro $29.99, pay-per-video $2.49, extra seats $4.61 + $6 admin fee, opt-in 3-tier rewards, goal: more Basic→Pro upgrades.

- **$10 → $30** removes the just-below start that discourages the step up. Same-left-digit ($40.50 → $48.50) is the stronger version and needs closer tiers.
- Pay-per-video stays as entry, priced so ~10 videos equals Pro.
- Seats: **$5, no admin fee**.
- Rewards: **auto-enroll, one tier**.

## Output

| Item | Value |
|---|---|
| Tiers | Basic $10/month · Pro $30/month |
| Upgrade path | No .99 on Basic |
| Pay-per-use | Entry only; heavy users cheaper on Pro |
| Components | $5 per extra seat, no admin fee |
| Perk / rewards | Minimum order on the perk; auto-enrolled single tier |
| Why | one line per choice |

## Common mistakes

- Adding a mid-tier to "shrink the jump" — the jump is the .99 boundary; fix the digits first.
- Pricing the flat rate at the pay-per-use equivalent "to be fair" — people pay more for the cap.
- A perk with no minimum — members fragment usage to exploit it.
- Opt-in tiered rewards — automatic, single tier, threshold reward.

## Quick reference

| Situation | Do | Depth |
|---|---|---|
| Plan structure | Flat rate above pay-per-use; pay-per-use as entry | `pricing` |
| Want upgrades | Same left digit; no .99 on the lower tier | `pricing` |
| Seats / storage | Rounded, same endings, no fee | `pricing` |
| Membership perk | Minimum order/usage | `post-purchase` |
| Member rewards | Auto-enroll, single tier | `post-purchase` |

Evidence and effect sizes: see [reference.md](reference.md).
