---
name: launch-economics
description: 'Judge an indie launch revenue target with verified prices, fees, acquisition scenarios, and executed unit economics.'
---

# Launch economics

Produce a revenue verdict backed by executed math and fetched pages, never training memory.

## Procedure

1. Verify the live price from the product source of truth (site pricing/checkout files, store listing) before using any number. Research notes go stale and invalidate every downstream figure.
2. Collect platform fees and payout terms from official docs via web fetch: transaction rate + fixed fee, payout method/region support, hold period, payout threshold and fee. Record which figures are official vs assumed.
3. Model the real acquisition engine as a funnel with ranges, not a static CPC formula. Organic touches (forum answers, guides, SEO/GEO, manual outreach, marketplace discovery) compound over weeks, with paid spend acting as an amplifier for proven winners only.
4. Execute all unit math with a tool (terminal/python), showing net-per-sale, sales-needed for gross and net targets, and scenario table across channels.
5. Research the marketplace channel in the same pass (commission tiers, review lag, payout hold, attribution rules) and compute sales-needed there separately.
6. Write the verdict to a local dated report file and report the short version in chat: verdict first, blockers, cheapest path to target, stop/continue gate.

Complete the pass only when every reported number traces to a live source or a labeled assumption and the arithmetic reproduces with the recorded inputs.

## Pitfalls

- Never present CPC/CVR expected-value arithmetic as a forecast. Label planning scenarios as scenarios and show the required conversion rate that would make the target hold, so the reader sees why it fails.
- Grep the live pricing surface for the current price on every run. Old research notes routinely cite superseded hypotheses and silently corrupt the math.
- Separate gross revenue, net after platform fees, net after ads, and true profit after tool subscriptions. Mixing them is the most common way a verdict misleads.
- Check payout timing (holds, thresholds, region support) before declaring month-one cash. Sales that pay out next month do not fund this month's costs.
