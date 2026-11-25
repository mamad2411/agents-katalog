---
name: discounts
description: Use when deciding how to word, size, or display a price discount, sale price, coupon, or markdown for an online store — e.g. "should this be 25% off or $15 off", "how do I show the sale price", "is 60% off too much", "what kind of coupon code should we send", "how do I write the promo banner".
---

# Discounts

Turn a planned discount into the exact numbers and wording that make it look biggest and most credible. The same discount can be expressed several ways; people react to the size of the numeral they see, not the arithmetic, and very large discounts read as a quality warning.

## When to use

- Choosing between percentage-off and amount-off
- Writing the sale badge, strikethrough price, banner, or email subject for a markdown
- Sizing a discount (how deep is too deep)
- Choosing the format of a coupon code (store-wide vs product-specific)
- Deciding whether to add a time limit

## When not to use

- Setting the full price itself (digits, endings) → the `pricing` skill
- Promotions that aren't price cuts (gifts, bundles, pre-orders, special days) → the `promotions` skill

## Inputs

Collect, or state your assumption:

- Full price `P` and either the sale price `S` or the discount `D` (`D = P − S`). `P` must be a price you actually charged for a reasonable period before the sale — if it wasn't, there is no discount to frame.
- Currency
- Scope: one product, one brand/category, or the whole store
- Where it appears: product page, banner, coupon code, email
- Reason for the sale (seasonal, clearance, launch, customer birthday) — if none, say so
- Audience gender mix, if known (affects price color only)

## Procedure

1. **Check the reference price is genuine.** Showing a struck-through or "was" price that was never really charged is deceptive pricing (US FTC guides, UK CMA, and the EU rule that a "was" price must be the lowest price of the prior 30 days). Confirm `P` was the real selling price before continuing; if you're unsure of the local rule, say so.
2. **Compute the three numbers.** `D = P − S`; `off% = D / P`; `higher% = D / S`. Example: P = 90, S = 60 → D = 30, off% = 33%, higher% = 50%.
3. **Check the depth.** If `off% > 40%`, warn: discounts this deep signal low quality, and at 60%+ they tend to reduce sales, especially for lesser-known brands or products whose quality is hard to judge before buying. Propose capping at 40% and adding a gift or bundle instead (see `promotions`). Exception: explicit clearance or shutdown, stated as the reason.
4. **Pick amount vs percentage by the numeral of the full price.** If `P ≥ 100` in the currency's units → show the **amount** off ("$120 off"). If `P < 100` → show the **percentage** off. The rule is about the size of the printed number, so it holds in any currency.
5. **If percentage: recalculate against the sale price.** State the discount as "was X% higher" where `X = higher%`, because `D / S > D / P`. Cap: if `higher% > 100%`, people ignore the "100" and read only the remainder, so fall back to plain "`off%` off" or the amount.
6. **Keep the price ending consistent.** The sale price should end the way the full price ends ($26.75 → $16.75, not $16.99). If `S` doesn't, adjust `S` to the nearest value with the same ending and recompute step 2. Always show the full price next to the sale price so the subtraction is easy.
7. **Coupons.** Store-wide or most-of-store coupon → **percentage** off ("everything 15% off"), which invites "the more I spend, the more I save". Product- or brand-specific coupon → **amount** off ("$2 off Gillette razors"), which makes the loss of not using it concrete. Send store-wide coupons to segments likely to buy new items, not to hoard. The evidence doesn't give a coupon size; apply the depth check from step 3 to the coupon, and if a coupon can stack on top of a marked-down item, apply it to the combined discount.
8. **Phrase the condition before the reward.** "Spend $100 and get $20 off", not "Get $20 off when you spend $100". The offer then reads as a reward, not a restriction. †
9. **Time limit, if any.** A time limit is fine and should be short (24–48 h), tied to a stated reason (seasonal, birthday), and carry a timezone. Online, time limits mostly raise awareness and visits rather than immediate sales, so don't rely on the deadline alone. Never limit by quantity ("only 500 left"): people who miss out get angry and switch brands; time limits don't cause this.
10. **Price color.** If the audience is mostly men *and* the purchase is routine (the effect disappears when people scrutinize the price, as for expensive or important buys), show *all* prices in red; men judged red prices as much better value, women were unaffected. Mixed red/black backfires, so it's all or nothing.

## Output

| Item | Value |
|---|---|
| Full price | $90.00 |
| Sale price | $60.00 |
| Display | ~~$90.00~~ **$60.00** — was 50% higher |
| Badge / subject line | "Cyber Monday: was 50% higher — ends Monday 23:59 PT" |
| Coupon (if any) | Store-wide → `CYBER15` = 15% off everything |
| Warnings | none / depth > 40% / higher% > 100% |
| Why | one line per choice, citing the rule |

## Common mistakes

- Choosing "$30 off" on a $90 item because "a dollar figure feels concrete" — under 100, the percentage is the bigger numeral. Use 33% off, or better, "was 50% higher".
- Rejecting a 60% discount only on margin grounds — the bigger problem is that it signals poor quality and can cut sales.
- Rounding the sale price to .99 when the full price ends in .00 or .75 — keep the endings the same.
- Treating a countdown as the main sales driver online — it drives clicks and opens, not purchases.
- Using "only N left" for urgency — quantity scarcity angers the people who miss out.
- Striking through a price that was never actually charged — that's deceptive pricing, not a discount.

## Quick reference

| Situation | Do |
|---|---|
| Full price ≥ 100 | Amount off |
| Full price < 100 | Percentage off, stated as "was X% higher" (X = D/S) |
| D/S > 100% | Plain "% off" or amount |
| Discount > 40% | Warn; cap or swap for a gift/bundle |
| Store-wide coupon | % off |
| Product/brand coupon | Amount off |
| Sale price ending | Same as full price |
| Wording | Condition first, then reward |
| Urgency | Short time limit with a reason and timezone; never a unit cap |
| Mostly male audience, routine purchase | All prices red |

† No primary citation on file for this rule — a practitioner tip, not a measured finding.

Evidence and effect sizes: see [reference.md](reference.md).
