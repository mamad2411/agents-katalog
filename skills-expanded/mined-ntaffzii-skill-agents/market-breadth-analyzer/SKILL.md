---
name: market-breadth-analyzer
description: Use this skill to score market breadth (the percentage of a stock universe trading above a moving average) from a plain CSV of tickers/prices/moving averages, with no market-data API required. Trigger on "market breadth", "% of stocks above 200-day MA", "breadth score", "how many stocks are participating", "is this rally broad or narrow". If the user wants a live number pulled from a real-time data feed rather than a CSV they already have, this skill still applies — just have them export/paste the data first, since this skill doesn't fetch prices itself.
---

# Market Breadth Analyzer

## Overview

A cap-weighted index (S&P 500, Nasdaq) can rise while most individual stocks fall — a handful of large names carry the average. Breadth measures actual participation: what fraction of a universe is trading above a given moving average. This skill computes that from a CSV the user already has (or pastes), so it works with **no paid market-data API**.

**Not financial advice.** This is a descriptive statistic over data you supply. A single breadth reading in isolation is a weak signal — see Known limitations.

## When to use

- เช็คว่าตลาดกำลังขึ้นแบบกว้าง (broad) หรือขึ้นแค่ไม่กี่ตัว (narrow)
- Scoring a watchlist or index-constituent CSV for % above 50-day/200-day moving average
- Part of a daily/weekly market-regime check (pairs naturally with [uptrend-analyzer](../uptrend-analyzer/SKILL.md) and [exposure-coach](../exposure-coach/SKILL.md))

## When NOT to use

- The user wants an actual buy/sell signal from one breadth reading — breadth informs market posture, it is not a trade trigger on its own
- No price/MA data is available at all and the user isn't willing to supply even a rough CSV — this skill has nothing to compute on

## Core knowledge

**Definition**: breadth % = (number of tickers with price > moving average) / (total tickers with valid data) × 100. Most common MA choices: 50-day (shorter-term participation) and 200-day (longer-term trend participation).

**Rough interpretation bands** (starting heuristic, not calibrated — tune against your own universe's history):

| Breadth % | Reading |
|---|---|
| ≥ 70% | Broad participation |
| 50-69% | Moderate participation |
| 30-49% | Narrow participation |
| < 30% | Weak participation |

**Data-quality handling**: rows with missing or non-numeric price/MA values are **excluded and reported**, not silently treated as "below the MA" — folding bad data into the score in either direction would quietly bias the result.

## Common mistakes

1. Treating a single breadth reading as a standalone buy/sell signal instead of one input to overall market posture.
2. Silently dropping rows with bad data instead of excluding-and-reporting them — this can shift the percentage without anyone noticing.
3. Comparing breadth readings computed against different MAs (50-day vs. 200-day) as if they measure the same thing — always state which MA a given percentage refers to.
4. Assuming `price == ma` counts as "above" — this implementation uses strict `>`, so an exact match counts as not-above; be explicit about that boundary when reporting results.

## Code

`breadth.py` — no dependencies:

- `compute_breadth(rows, price_field="price", ma_field="ma200")` → `BreadthResult(total, above, below, excluded, pct_above)`
- `compute_breadth_from_csv(csv_text, ...)` → same, from raw CSV text (header row required)
- `classify_breadth(pct_above)` → one of the four bands above

Run `python3 breadth.py` for the self-test.

## Known limitations

- Interpretation bands are a generic starting heuristic — different universes (small-cap vs. large-cap, different sectors) behave differently at the same percentage; recalibrate against history before treating a threshold as meaningful.
- This skill does not fetch data. The user (or another tool/skill) must supply the CSV; accuracy of the output is only as good as the input.
- A rising breadth percentage and a falling index (or vice versa) is itself informative (a breadth divergence) — this skill reports the raw number, not divergence detection; that's a manual read on top of the output.
