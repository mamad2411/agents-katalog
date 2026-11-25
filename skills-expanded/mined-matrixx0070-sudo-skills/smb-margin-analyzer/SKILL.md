---
name: smb-margin-analyzer
version: 1.0.0
description: Break down unit economics per product or service, rank by contribution, and model pricing scenarios before the owner commits.
author: matrixx0070
tags: [small-business, margin, pricing, unit-economics, profitability, break-even]
capabilities: []
---

# Margin Analyzer

## When to use
Use this when the owner suspects some offerings carry the business while others quietly bleed, or when a price/cost change is on the table and they want the effect modeled first. Good for "which products actually make money?" and "if I raise this 10%, what happens?"

**Not for:** publishing or changing prices (that's the owner's call, downstream); full campaign planning (use smb-run-campaign); tax or bookkeeping cleanup (use smb-month-end-prep).

## Method
1. **List offerings in scope.** Capture unit price and units sold for the period. If data isn't connected, ask the owner for the short list that matters most.
2. **Assign direct costs.** Per unit: materials, direct labor, processor fees, shipping. If a cost is unknown, mark it estimated rather than skipping it.
3. **Compute unit economics.** Gross profit per unit, gross margin %, and total contribution (margin/unit × units) per offering.
4. **Rank two ways.** By total contribution and by margin %. Decision point: an item can be low-margin but high-contribution (keep, optimize) or high-margin but trivial volume (fine, don't over-invest). Flag negative-margin items explicitly.
5. **Run scenarios on selected items.** Model +/- price and cost changes. Show new margin and the break-even volume shift — how much volume you can lose before the change stops paying.
6. **Recommend.** Price, bundle, or discontinue moves with projected margin impact. Do not change prices; that decision affects customers and revenue and is the owner's to approve.

## Example
Owner sells a $40 gift box (cost $31, 200/mo) and $18 candles (cost $6, 90/mo). Boxes: $9/unit margin (22.5%), $1,800 contribution. Candles: $12/unit (66.7%), $1,080. Scenario — raise box to $45: margin jumps to $14 (31%). Break-even: sales can fall from 200 to 129/mo before contribution drops below today's $1,800. Recommendation (for approval): raise boxes, promote candles harder.

## Pitfalls
- Counting only COGS and forgetting processor fees and shipping — the true margin is thinner than it looks.
- Killing a "low-margin" item that's actually a top contributor by dollars, or a loss leader that drives attached sales.
- Modeling a price rise with zero demand sensitivity; always state the volume you can afford to lose.
- Treating estimated costs as facts — label assumptions so the owner can correct them.

## Output format
- **Period / offerings covered.**
- **Unit economics table:** offering | price | unit cost | gross profit/unit | margin % | total contribution.
- **Ranking:** top contributors; thin/negative-margin flags.
- **Pricing scenarios:** offering | change modeled | new margin | break-even volume shift.
- **Recommendations (for owner approval)** with the assumption each rests on.

## Reference

### Core formulas
- **Gross profit / unit** = price − variable cost per unit (materials + direct labor + processor fee + shipping/packaging).
- **Contribution margin / unit** = price − *all* variable costs (same as gross profit/unit when only variable costs are direct). This is the dollars each sale contributes toward fixed costs and profit.
- **Contribution margin %** = contribution margin/unit ÷ price.
- **Total contribution** = contribution margin/unit × units sold.
- **Break-even units** = fixed costs ÷ contribution margin/unit.
- **Break-even revenue** = fixed costs ÷ contribution margin %.
- **New break-even after a price/cost change** — recompute contribution margin/unit, then solve for the units needed to hold today's total contribution: `units_needed = current_total_contribution ÷ new_contribution_per_unit`. The gap between that and today's volume is the demand you can afford to lose.
- **Markup vs margin (don't confuse them):** margin % = (price − cost) ÷ price; markup % = (price − cost) ÷ cost. A 50% markup is only a 33% margin. To hit a target margin M, price = cost ÷ (1 − M).

### Processor and hidden variable costs to always include
Card processing typically runs ~2.6-3.5% + $0.10-0.30 per transaction (higher for keyed/online, AmEx, and marketplaces). Marketplace/platform fees can be 10-30% of price. Also fold in: shipping and packaging, payment-plan/BNPL fees, returns/refund reserve (model as an expected % of sales), free-shipping thresholds, and per-order pick/pack labor. Skipping these is the single most common reason a "healthy" margin is actually thin.

### Gross-margin benchmark ranges (directional, verify against your own books)
| Business type | Typical gross margin |
|---------------|----------------------|
| Restaurants / food service | 60-70% food GM, but ~3-9% *net* after labor & rent |
| Retail (general merchandise) | 25-50% |
| Grocery / high-volume | 10-25% |
| Ecommerce / DTC products | 30-50% |
| SaaS / software | 70-90% |
| Professional & personal services | 50-70%+ (labor is the main cost) |
| Construction / contracting | 15-30% |
| Manufacturing | 25-45% |

Use these to sanity-check, not to set targets — a business well below its band has a pricing or cost problem worth naming; well above may have room to invest in growth.

### Decision guide: keep, fix, promote, or cut
- **High margin % + high contribution $:** your stars. Protect availability, feature them, don't over-discount.
- **Low margin % + high contribution $:** volume workhorses. Attack unit cost before touching price; small margin gains scale hugely.
- **High margin % + low contribution $:** niche/premium. Fine to keep; don't over-invest chasing volume.
- **Low margin % + low contribution $:** candidates to reprice, bundle, or discontinue — *unless* it's a proven loss leader driving attached sales (check the attach rate before cutting).
- **Negative margin:** stop the bleed. Reprice, re-source, or discontinue. Flag explicitly and quantify the monthly loss.

### Pricing-scenario checklist
For every modeled change state: (1) the new contribution margin/unit and %, (2) the new break-even volume and the % of current volume you can lose, (3) a demand-sensitivity assumption (best/expected/worst unit change), and (4) second-order effects — cannibalization of other items, attach-rate loss, competitor price gaps, and customer-perception risk. A 10% price rise on a 30%-margin item can absorb roughly a 25% volume drop before contribution falls; on a 60%-margin item it tolerates far less volume loss to stay ahead. Always label every estimated cost or elasticity as an assumption the owner can correct.
