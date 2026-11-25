---
name: increase-conversion
description: Use when someone wants more visitors to buy — "conversion rate is low", "how do I get more people to check out", "what should we fix first to lift conversions", "our product page isn't converting", "rank what would move conversion" — for an online store or product page. Cart and payment-form work goes to checkout-ux.
---

# Increase conversion

Turn "conversion is 1.4%, make it higher" into a ranked backlog. This skill does not audit a checkout page and does not restate the task skills. Walk the levers below, note whether the setup already complies, and order the misses by measured effect × distance from the rule. Every number lives in the Depth skill; do not convert it into a forecast for the user's rate.

## When to use

- The user names conversion, checkout *rate*, or "people don't buy" as the goal
- The user shares a store or product page and asks what to fix first

## When not to use

- Cart, checkout, or payment-form drop-off → `checkout-ux`
- Basket size → `increase-aov`; second orders → `increase-repeat-purchases`
- A single element in depth (a photo brief, a price, a discount) → the Depth skill named in that step

## Inputs

Collect, or state your assumption:

- The page or store: URL (fetch it), screenshot, or element-by-element description
- Whether drop-off is on the product page or at cart/payment (if payment, stop and use `checkout-ux`)
- Product, price, variants, sold-out share, review snapshot
- Company size; whether the product is high-tech; any real sustainability practice

> **Classify the product first.** *Hedonic* = bought for enjoyment, pleasure, or the experience (chocolate, fashion, decor, travel, spa, perfume). *Utilitarian* = bought to do a job, judged on function and value (detergent, appliances, insect repellent, tools, accounting software). If it's mixed, decide by what the buyer is optimizing for at the moment of purchase.

## Procedure

Walk each check. Include levers the user didn't mention if they apply; list the ones that don't apply in one line at the end.

1. **Checkout and cart, if they have one.** Guest vs forced account, field count, wallets, total/shipping surprise, coupon-field distraction. Often the largest conversion hole and out of scope for this router. Depth: `checkout-ux`.
2. **Product-page mechanics.** Price below the image; view or purchase counts; sold-out variants visible at 10–30%; quantity CTAs on multi-unit products; options in steps of 2–5. Depth: `product-page`.
3. **Media.** Hedonic → video/GIF, gaze away, first-person hand, shine, spacing. Utilitarian → stills are enough. Depth: `product-visuals`.
4. **Copy.** Three best claims, plain language, intuitive units. Depth: `product-copy`.
5. **Trust.** Cost breakdown; say you're small if low-tech; extraordinary warranty if the category is known but you aren't. Depth: `store-audit`.
6. **Offer.** "For $0" not "free"; wanted product framed as the gift; token fee for upgrades. Depth: `promotions`.
7. **Price and discount.** Quality-led or hedonic → rounded; price-led or promotion → just-below. Discounts ≤ 40%. Depth: `pricing`, `discounts`.
8. **Urgency.** Deadline with a reason and timezone; never a unit cap. Depth: `discounts`.
9. **Reviews.** 4.0–4.5 sells more than a perfect average; reply to every review. Depth: `reviews`.
10. **Rank.** Compare like with like: the studies report sales, conversion, intent, and willingness to pay. A WTP percentage is a weaker surrogate for conversion than a measured sales lift. Cheap, no-inventory fixes ahead of shoots and builds at equal effect. Each effect was measured on its own; don't add them up.

## Output

| # | Finding | Change | Measured effect (study context) | Depth |
|---|---|---|---|---|
| 1 | Forced account before payment | Guest continue | Spool: +45% customers purchasing (one large retailer) † | `checkout-ux` |
| 2 | Price above image | Move below | +35.2% sales (liquor store) | `product-page` |
| … | | | | |

Then: what already complies, and the caveat that effects are from the cited contexts, not predictions. Ship the top two or three, measure, then take the next.

## Common mistakes

- Auditing the checkout page inside this skill — hand it to `checkout-ux`.
- Inventing a lift ("30–50% relative") — quote the study's number and its context only.
- Ranking price position last as cosmetic — it is one of the largest measured effects on the page.
- Treating a 4.9 as an asset to protect — 4.0–4.5 sells more.

## Quick reference

| Check | Depth |
|---|---|
| Cart / payment form | `checkout-ux` |
| Price, social proof, CTA, variants | `product-page` |
| Photos and video | `product-visuals` |
| Claims and units | `product-copy` |
| Cost breakdown, size, warranty | `store-audit` |
| Gifts, "$0", upgrades | `promotions` |
| Digits and markdowns | `pricing`, `discounts` |
| Review average and replies | `reviews` |

† No primary citation on file for this rule — a practitioner tip, not a measured finding.

Evidence and effect sizes: see [reference.md](reference.md).
