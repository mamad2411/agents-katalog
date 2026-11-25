---
name: stocktwits-sentiment
description: >
  This skill should be used when the user asks about StockTwits sentiment,
  trader bullish/bearish ratio, StockTwits stream, real-time trader sentiment,
  what traders are saying on StockTwits, or the StockTwits signal for a stock.
---

# StockTwits Sentiment Analysis

## Purpose

Fetch StockTwits sentiment for a ticker by scraping the symbol page, tally
bullish vs bearish self-labeled messages, and produce a channel score from
-10 to +10.

## Step 1 — Fetch Symbol Page

WebFetch the StockTwits symbol page with this prompt:
> "Extract: (1) bullish message count or percentage, (2) bearish message count
> or percentage, (3) total labeled messages, (4) any overall sentiment label
> (e.g. Bullish, Bearish, Extremely Bullish, Extremely Bearish, Neutral),
> (5) up to 2 recent message bodies labeled Bullish and up to 2 labeled Bearish."

```
https://stocktwits.com/symbol/{ticker}
```

If that page returns no useful data, retry with:

```
https://stocktwits.com/symbol/{ticker}/sentiment
```

## Step 2 — Extract Counts or Label

**If raw counts are available** (bullish_count and bearish_count):
- Set `score_method = "ratio"`
- `total_labeled = bullish_count + bearish_count`
- Proceed to Step 3a.

**If only a percentage is available** (e.g. "73% Bullish"):
- Derive counts: `bullish_count = round(pct × total_labeled)`, `bearish_count = total_labeled - bullish_count`
- Set `score_method = "pct-derived"`
- Proceed to Step 3a.

**If only a qualitative label is available** (no counts or percentages):
- Set `score_method = "label-derived"`
- Map label to score and proceed to Step 3b:

| StockTwits Label | stocktwits_score |
|-----------------|-----------------|
| Extremely Bullish | +8.5 |
| Bullish | +5.0 |
| Neutral | 0.0 |
| Bearish | -5.0 |
| Extremely Bearish | -8.5 |

**If the page fails to load, returns an error, or yields no sentiment data:**
Set `stocktwits_available = false`.
Note: "StockTwits: Page unavailable or no sentiment data found"

## Step 3a — Compute Score from Ratio

```
stocktwits_score = (bullish_count - bearish_count) / total_labeled × 10
```

## Step 3b — Score from Label (skip if 3a used)

Use the mapped score from the label table in Step 2. Set `total_labeled = N/A`.

## Step 4 — Sample Messages

Extract the most recent Bullish-labeled message body and most recent
Bearish-labeled message body from the page content. If unavailable, note
"Sample unavailable".

## Step 5 — Output

```
STOCKTWITS SENTIMENT RESULT
Ticker: {ticker}
Channel Score: {stocktwits_score} / 10
Signal: {label per signal bands below}
Score Method: {ratio | pct-derived | label-derived}
Labeled Messages: {total_labeled} ({bullish_count} bullish / {bearish_count} bearish)

Sample Bullish: "{message_body}"
Sample Bearish: "{message_body}"
```

If unavailable:

```
STOCKTWITS SENTIMENT RESULT
Ticker: {ticker}
Channel Score: N/A
Signal: N/A
Note: {reason}
```

Signal bands (applied to stocktwits_score):
- score >= +7.0 → Very Bullish
- score >= +3.0 and < +7.0 → Bullish
- score > -3.0 and < +3.0 → Neutral
- score <= -3.0 and > -7.0 → Bearish
- score <= -7.0 → Very Bearish
