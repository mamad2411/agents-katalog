---
name: dividend-value-screener
description: Use this skill for a structured checklist of common value and dividend-quality screening criteria (P/E, dividend yield, payout ratio, debt/equity, dividend growth streak) applied to stocks or ETFs a user is evaluating. Trigger on "dividend screener", "value stock screen", "is this a good dividend stock", "yield trap", "payout ratio check". This skill structures the screening criteria; it does not fetch live fundamental data.
---

# Dividend / Value Screener

## Overview

"Is this a good dividend stock?" needs more than a high yield number — a very high yield is often a warning sign (a "yield trap": price has fallen because the market expects a cut), not a bargain. This skill supplies the standard checklist of value/dividend-quality criteria and their common pitfalls, to apply against fundamental data the user provides or fetches separately.

**Not financial advice.** This is a screening framework, not a buy recommendation — passing every criterion here doesn't guarantee a good investment, and failing one doesn't automatically disqualify a stock.

## When to use

- ประเมินหุ้นปันผลว่ามีสัญญาณ yield trap หรือไม่
- คัดกรองหุ้น value ด้วยเกณฑ์มาตรฐาน (P/E, D/E, payout ratio)
- Reviewing whether a dividend growth streak is intact and the payout ratio still looks sustainable

## When NOT to use

- The task is a momentum/breakout swing-trade screen — this is a fundamentals-based value/income screen, structurally different from [uptrend-analyzer](../uptrend-analyzer/SKILL.md)'s technical criteria
- No fundamental data is available and the user won't supply any — this skill needs P/E, yield, payout ratio, etc. as inputs; it doesn't fetch them

## Core knowledge

**Core checklist**:

| Metric | What it checks | Common pitfall |
|---|---|---|
| Dividend yield | Income relative to price | A yield much higher than the stock's own history or its sector peers is a warning sign, not automatically a bargain — check *why* it's high before treating it as attractive |
| Payout ratio (dividend ÷ earnings) | Sustainability of the dividend | A payout ratio near or above 100% (paying out more than earned) is fragile — a cut is more likely under any earnings pressure. Note: payout ratio can look distorted for REITs/MLPs where GAAP earnings differ structurally from distributable cash flow — use the sector-appropriate cash-flow metric instead of raw payout ratio for those |
| Dividend growth streak | Consistency of dividend policy over time | A long streak is a positive signal about management discipline, but a streak alone doesn't guarantee it continues — check whether recent increases have been token-sized (e.g. $0.01) as a sign of strain |
| P/E ratio | Price relative to earnings | Compare within the same sector — "cheap" and "expensive" P/E norms vary enormously by industry; a low P/E can also mean the market correctly expects declining earnings, not that the stock is undervalued |
| Debt/Equity | Balance-sheet leverage | High leverage isn't automatically bad (capital-intensive sectors like utilities/REITs normally run higher D/E), but it does reduce a company's flexibility to maintain the dividend through a downturn — again, compare within sector |

**Yield-trap pattern**: yield rose mainly because price fell (not because the dividend grew), payout ratio is stretched, and there's been recent negative earnings/guidance news. All three together is a stronger warning than any one alone.

## Common mistakes

1. Ranking candidates by yield alone without checking payout ratio or the reason the yield is elevated.
2. Comparing P/E or D/E across different sectors as if the same numeric threshold means the same thing everywhere.
3. Treating a long dividend-growth streak as a guarantee the streak continues, ignoring recent signs of strain (token increases, deteriorating payout ratio).
4. Applying standard payout-ratio logic to REITs/MLPs without adjusting for their structurally different earnings-vs-cash-flow relationship.
5. Screening on trailing (historical) fundamentals only, with no check on forward guidance or recent trend direction.

## Known limitations

- This skill does not fetch live fundamental data (P/E, yield, payout ratio, debt/equity) — the user or another tool must supply current figures.
- Sector-appropriate thresholds for each metric aren't fixed here (they vary too much by industry to assert one number) — compare candidates within their own sector, not against a single universal cutoff.
- Passing this checklist is a starting filter, not a complete investment thesis — it doesn't replace reading the actual filings, earnings calls, or industry context.
