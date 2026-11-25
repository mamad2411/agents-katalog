---
name: smb-price-check
version: 1.0.0
description: Build a margin-by-product table plus three pricing-scenario views (hold, raise, reprice losers) to support a pricing decision.
author: matrixx0070
tags: [pricing, margin, scenarios, finance, strategy, decision]
capabilities: []
---

# Price Check

## When to use
Run this before the owner raises prices, launches a product, or reacts to a cost increase. It turns "should I change my prices?" into a numbers-backed decision the owner makes.

**Not for:** deep unit-economics with break-even modeling (use smb-margin-analyzer); publishing or updating prices in any system — the owner signs off before anything changes.

## Method
1. **Gather inputs.** Each product's price, unit cost, and recent units sold. Pull from connected sales/inventory data, or ask the owner for the short list that matters.
2. **Compute and rank.** Per-product gross margin (dollars and percent); rank by margin and by volume.
3. **Flag outliers.** Items below a healthy margin floor, loss leaders, and high-volume low-margin items where a small change moves the most money. Decision point: prioritize the high-volume low-margin items — that's where a 5% tweak has the biggest dollar impact.
4. **Build three scenario views** over the same products: **Hold** (current prices/margin); **Raise** (across-the-board or targeted increase, with estimated margin gain and a demand-sensitivity caveat); **Reprice losers** (fix only the worst margins, leave winners untouched).
5. **Summarize trade-offs and recommend.** Name a recommended scenario and the assumption it rests on. The owner approves before any price changes anywhere.

## Example
Three products: Mug $12/cost $5/300u; Tee $22/cost $14/180u; Sticker $4/cost $1.20/90u. Margins: Mug 58%, Tee 36%, Sticker 70%. Tee is high-volume low-margin — the lever. Hold: total margin $4,164/mo. Raise Tee to $25: +$540/mo, caveat "demand may soften above $24." Reprice losers: lift Tee to $25 only, leave Mug/Sticker. Recommendation: reprice losers — biggest gain, least risk to bestsellers. Assumption: Tee volume holds within ~10%.

## Pitfalls
- Ranking only by margin % and missing that the low-% product is where the real dollars move.
- Modeling a raise with no demand-sensitivity caveat, so the projection reads as a guarantee.
- Touching bestsellers "for consistency" when repricing only the losers is safer.
- Publishing a price to a live storefront before the owner has signed off.

## Output format
- **Margin table:** product | price | cost | margin $ | margin % | units | margin contribution.
- **Three scenario cards:** Hold / Raise / Reprice losers — each with projected total margin and a one-line trade-off.
- **Recommendation** + the assumption it rests on.
- **Approval note:** no price is published or updated in any system without owner sign-off.

## Reference

### Margin math (get the definitions right before ranking)
- **Gross margin $ = price − unit cost.** **Gross margin % = (price − cost) / price.**
- **Markup ≠ margin.** A 50% markup on a $10 cost = $15 price = only 33% margin. Owners conflate these constantly; always state which you mean.
- **Contribution = margin $ × units.** This is the number that pays the rent. A 36% item selling 180 units contributes more dollars than a 70% item selling 20.
- **Blended margin** across the catalog matters for the P&L; per-item margin matters for the pricing decision.

### Healthy gross-margin benchmarks by category
| Business type | Typical gross margin | Notes |
|---------------|---------------------|-------|
| Restaurant food | 60-70% (food cost 28-35%) | Labor is the real squeeze |
| Cafe / coffee | 70-80% on drinks | Pastry drags the blend |
| Retail / apparel | 50-60% | Keystone (2x cost) is the old default |
| E-commerce physical goods | 40-60% pre-shipping | Watch fulfillment + returns |
| SaaS / digital | 80-90% | Near-zero marginal cost |
| Professional services | 50-70% | "Cost" = loaded labor rate |
| Handmade / craft | 40-55% | Owners routinely underprice their time |
Flag anything materially below its band as a margin-floor breach.

### Elasticity rules of thumb
- **Necessities and habitual buys** (coffee, essentials, subscriptions under ~$15) are *inelastic* — a 5-10% raise rarely dents volume.
- **Discretionary and comparison-shopped goods** (apparel, gifts, electronics) are *elastic* — small raises can move volume noticeably.
- **The 1% rule:** for a typical SMB, a 1% price increase with volume held flat lifts operating profit far more than a 1% volume increase — price is the strongest profit lever.
- **Break-even volume drop for a raise:** you can afford to lose `price-increase% / (margin% + price-increase%)` of units before the raise loses money. Example: 10% raise on a 40% margin item breaks even at ~20% unit loss — so unless demand is very elastic, the raise wins.
- **Anchor and charm pricing:** $99 vs $100 rarely changes SMB volume much; a clearly-communicated value story beats a penny trick.

### Pricing-scenario table (the three views, side by side)
| Scenario | What changes | Upside | Risk |
|----------|-------------|--------|------|
| **Hold** | Nothing | Zero disruption; baseline | Margin erosion if costs rose |
| **Raise** | Across-board or targeted +X% | Largest margin gain | Volume/demand softening; must caveat |
| **Reprice losers** | Fix only sub-floor items | Best gain-per-risk; winners untouched | Slower total lift |
Recommend **reprice losers** as the low-risk default; escalate to a targeted raise on inelastic items when the owner wants more.

### Cost-increase response playbook
When a supplier cost jumps: (1) recompute margin at the new cost, (2) check if the item is still above its floor — if yes, absorbing may protect volume; if no, pass through, (3) prefer a targeted raise on the affected item over a blanket increase, (4) if raising a visible staple, pair it with a value message rather than a silent bump.

### Do-not-touch guardrails
- Never publish or push a price to a live storefront, POS, or invoice template without explicit owner sign-off.
- Never model a raise as a guarantee — every raise line carries a demand-sensitivity caveat.
- Leave bestsellers alone unless the data says otherwise; "consistency" is not a pricing reason.
