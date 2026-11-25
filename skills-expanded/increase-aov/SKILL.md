---
name: increase-aov
description: Use when someone wants bigger orders — "raise average order value", "AOV is flat", "get people to buy more per order", "should we do a free-shipping threshold or a bundle", "how do we sell three instead of two" — for any online store or product page.
---

# Increase AOV

Turn "AOV is $34, make it bigger" into a ranked backlog. Leave the how-to and the papers in the Depth skills. Rank **direct** findings (measured on order size) ahead of **adjacent** (measured on sales or returns) and **indirect** (measured on willingness to pay or deal attractiveness) at equal fit. Every number is what a cited study measured in its own context; do not turn it into a forecast for the user's AOV.

## When to use

- The user names AOV, basket size, units per order, or "sell more per customer" as the goal
- Deciding between a free-shipping threshold, a membership, a bundle, or a coupon

## When not to use

- More visitors buying at all → `increase-conversion`; second orders → `increase-repeat-purchases`
- Cart/checkout field design (guest, wallets, coupon-box distraction) → `checkout-ux`
- The exact wording of a discount → `discounts`; the promotion mechanic in depth → `promotions`

## Inputs

Collect, or state your assumption:

- Products, prices, typical basket (units and value), complements sold
- Whether the main product is naturally bought in multiples
- Current CTA, shipping policy, coupons, returns, any bundle and its wording
- Order frequency (for a membership) and margin (for discount depth)

## Procedure

Walk each check; note whether the setup complies, and if not, what changes. Include applicable levers the user didn't mention; list the rest as considered.

**Direct**

1. **Quantity CTAs.** Multi-unit product → Buy 1 / Buy 2 / Buy 3 instead of "Add to cart". Depth: `product-page`.
2. **Paid free-shipping membership with a minimum order.** A plain threshold without a membership isn't in the evidence — say so if recommending one. Depth: `post-purchase`.
3. **Free, easy returns.** Higher spend per order and more variety. Depth: `post-purchase`.

**Adjacent** (measured on total sales or returns, not basket size)

4. **Coupon type.** Store-wide → percentage; product-specific → amount off. Depth: `discounts`.
5. **Bundle framing.** Wanted product as the gift, "at no cost", not a "special bundle price". Depth: `promotions`.

**Indirect**

6. **Token-fee upgrades** rather than free. Depth: `promotions`.
7. **Flat rate above pay-per-use** where usage varies. Depth: `pricing`, `subscription-pricing`.
8. **Simple add-on pricing.** Rounded, same ending as the base, no service fee. Depth: `pricing`.
9. **Complements around the focal product** in the shot (raises focal-product purchase likelihood, not accessory sales). Depth: `product-visuals`.
10. **Intuitive units** ("about 15 cups", not "250 g"). Depth: `product-copy`.
11. **Rank.** Direct first; then by measured effect and distance from the rule; cheap changes (CTA, wording, coupon type) ahead of programs that need billing or logistics.

## Output

| # | Finding | Change | Measured effect (study context) | Class | Depth |
|---|---|---|---|---|---|
| 1 | Single "Add to cart" on a multi-unit product | Buy 1 / 2 / 3 | Sales up to +28% (37 experiments) | Direct | `product-page` |
| … | | | | | |

Then: what already complies. Each effect was measured on its own; don't add them up. Ship the top two or three, measure, then take the next.

## Common mistakes

- Inventing a lift for a free-shipping threshold ("+10–20%") — the evidence is for a paid membership with a minimum; say so.
- "Special bundle price" wording — gift framing is the measured lever.
- A dollar-off coupon for a store-wide promotion — percentage puts people in "the more I spend" mode.
- Defaulting the bundle in the cart instead of quantity buttons — the measured lever is the CTA format.

## Quick reference

| Lever | Depth | Direct? |
|---|---|---|
| Buy 1 / 2 / 3 | `product-page` | Direct |
| Membership + minimum | `post-purchase` | Direct |
| Free returns | `post-purchase` | Direct |
| Store-wide % coupon | `discounts` | Adjacent |
| Gift-framed bundle | `promotions` | Adjacent |
| Token-fee upgrade | `promotions` | No |
| Flat rate / simple add-ons | `pricing` | No |

Evidence and effect sizes: see [reference.md](reference.md).
