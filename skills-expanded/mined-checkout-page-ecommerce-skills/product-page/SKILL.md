---
name: product-page
description: Use when reviewing, auditing, or designing a product page, landing page, or offer page for an online store — e.g. "audit my product page", "look at this landing page and tell me what's wrong", "why isn't this page converting", "how should I show variants / sold-out options / the price", "should I show how many people viewed this", or a URL/screenshot of a page that sells one thing.
---

# Product page

Audit a product page against peer-reviewed findings and return prioritized changes with expected effects. Layout, counts, and choice structure make a product feel wanted and worth the price before the copy does.

## When to use

- A user shares a product page (URL, screenshot, or description) and asks what to change
- Designing a new product page template, or deciding how to show variants, stock, social proof, CTAs, or price

## When not to use

- A cart, checkout, or payment form → `checkout-ux`
- Writing the description → `product-copy`; briefing photos/video → `product-visuals`
- Discount framing → `discounts`; setting the price → `pricing`

## Inputs

Collect, or state your assumption:

- The page: URL (fetch it), screenshot, or element-by-element description
- Product and price; whether it is naturally bought in multiple units (consumables, cans, candles)
- Number of options and how many are sold out
- View and purchase counts and the views-to-purchase rate, if tracked
- Company size

> **Classify the product first.** *Hedonic* = bought for enjoyment, pleasure, or the experience (chocolate, fashion, decor, travel, spa, perfume). *Utilitarian* = bought to do a job, judged on function and value (detergent, appliances, insect repellent, tools, accounting software). If it's mixed, decide by what the buyer is optimizing for at the moment of purchase.

## Procedure

1. **Social proof numbers.** Show a view or purchase count (purchase intent up to ~58% higher). Views while the numbers are small; once views run into the thousands (e.g. 15,600), switch to the purchase count, because large view counts are hard to process. If views→purchases ≥ 5%, show both. Change what the badge counts; don't remove it.
2. **Sold-out options.** Visible and marked sold out (sales up to 31% higher — measured among shoppers who hadn't settled on a specific option). Keep the sold-out share at 10–30%; above that, hide some or restock.
3. **Quantity CTAs.** Multi-unit product → Buy 1 / Buy 2 / Buy 5 buttons instead of "Add to cart" (+14% conversion average, sales up to +28%). Start with three; test quantities.
4. **Choice partitioning.** More than a handful of options → steps of 2–5 similar options, technical before aesthetic, big decisions first. If one attribute alone has more than 5 values (8 colors), group them by similarity (warm / cool / neutral) and let people pick the group first. Never one grid of every combination.
5. **Add-on pricing.** Rounded prices with the same ending as the base ($22 → $32), or a flat rate.
6. **Price position.** Below the product image (reads ~9% lower; store sales +35.2%).
7. **Copy (depth in `product-copy`).** Three claims max; best features only; intuitive units; plain language; science wording only if utilitarian. †
8. **Visuals (depth in `product-visuals`).** Hedonic → video; models look away; first-person hand touching the product; a shine; graspable product toward the right; products spaced apart; complementary props.
9. **Trust.** Small business → say so (unless high-tech). Extraordinary warranty when the category is known but the brand isn't.

Rank by expected effect × distance from the rule. Cart and payment-step issues are out of scope here; Depth: `checkout-ux`.

## Output

| # | Issue | Change | Measured effect (study context) | Source |
|---|---|---|---|---|
| 1 | Single "Add to cart" on a multi-unit product | Buy 1 / 2 / 5 buttons | +14% conversion | Duke & Amir 2023 |

Close with what the page already does right.

## Common mistakes

- Deleting a large view count because it "looks fake" — switch it to purchases.
- Greying out sold-out options only for email capture — the point is the quality signal; watch the 30% ceiling.
- Splitting a variant grid but leaving 8+ options in one step — 2–5 per step.
- Ranking price position last as cosmetic — it moves perceived price and sales.

## Quick reference

| Check | Rule |
|---|---|
| Social proof | Views while small → purchases once views hit thousands; both if ≥ 5% conversion |
| Sold-out | Show, marked; 10–30% of options |
| CTA | Quantity buttons for multi-unit products |
| Options | Steps of 2–5; big decisions first |
| Add-ons | Rounded, same ending, or flat rate |
| Price | Below the product |
| Claims | Three, best only |
| Media | Video if hedonic; hand, gaze away, shine, spacing |

† No primary citation on file for this rule — a practitioner tip, not a measured finding.

Evidence and effect sizes: see [reference.md](reference.md).
