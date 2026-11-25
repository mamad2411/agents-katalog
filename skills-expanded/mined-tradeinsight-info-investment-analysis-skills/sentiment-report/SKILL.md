---
name: sentiment-report
description: >
  This skill should be used when the user asks for a full sentiment report,
  comprehensive sentiment analysis, complete sentiment summary, sentiment check,
  overall market mood, how sentiment looks, or explicitly runs /sentiment-report
  for a publicly traded company. Also use when the user asks to "analyze sentiment",
  "run sentiment analysis", or "give me a sentiment overview" for a stock.
---

# Sentiment Report

## Purpose

User-invocable skill (`/sentiment-report`) that dispatches all three sentiment
data channels in parallel using the `Agent` tool, synthesizes a composite score,
and formats the full report with a data source log.

## Step 1 — Resolve Ticker and Company Name

Confirm ticker and company name via WebSearch if needed. Record the current UTC
timestamp for the report header.

## Step 2 — Dispatch Three Skills in Parallel

Use the `Agent` tool to run all three simultaneously:
- Invoke `news-sentiment` for the ticker
- Invoke `reddit-sentiment` for the ticker
- Invoke `stocktwits-sentiment` for the ticker

Do NOT proceed to Step 3 until all three have returned results.

## Step 3 — Collect Channel Scores

From each skill output, extract:
- `news_score`, `article_count`, `news_source`, `low_volume_warning`, `key_headlines`
- `reddit_score`, `wsb_score`, `rstocks_score`, `wsb_post_count`, `rstocks_post_count`, `top_wsb_posts`, `top_rstocks_posts`, `fallback_notes`
- `stocktwits_score`, `bullish_count`, `bearish_count`, `total_labeled`, `sample_bullish`, `sample_bearish`
- Availability flags from each skill

## Step 4 — Compute Composite Score

**Base weights:** News 45%, StockTwits 30%, Reddit 25%

**Re-normalize if a channel is unavailable** (null score). Adjust weights so they
sum to 1.0 across available channels only:

| Available Channels | News weight | StockTwits weight | Reddit weight |
|-------------------|-------------|-------------------|---------------|
| All three | 0.45 | 0.30 | 0.25 |
| News + StockTwits only | 0.60 (45/75) | 0.40 (30/75) | — |
| News + Reddit only | 0.643 (45/70) | — | 0.357 (25/70) |
| StockTwits + Reddit only | — | 0.545 (30/55) | 0.455 (25/55) |
| News only | 1.00 | — | — |
| StockTwits only | — | 1.00 | — |
| Reddit only | — | — | 1.00 |

```
composite = (news_score × w_news) + (stocktwits_score × w_st) + (reddit_score × w_reddit)
```

**If fewer than 2 channels have data:** Do not compute a composite. Output
"⚠️ Insufficient data to compute composite score" and show available channel
results individually.

## Step 5 — Determine Score Label

Apply the standard signal bands to the composite score:
- >= +7.0 → Very Bullish
- >= +3.0 and < +7.0 → Bullish
- > -3.0 and < +3.0 → Neutral
- <= -3.0 and > -7.0 → Bearish
- <= -7.0 → Very Bearish

## Step 6 — Build ASCII Progress Bar

Scale composite (-10 to +10) onto a 20-character bar:
- Use `█` for filled blocks, `░` for empty
- The center 10 characters represent 0. Positive scores fill right; negative fill left.
- Append the numeric score: `{bar}  ({composite_score})`

Examples:
- Score +8.0: `░░░░░░░░░░████████░░  (+8.0)`
- Score -5.0: `░░░░░█████░░░░░░░░░░  (-5.0)`
- Score 0.0:  `░░░░░░░░░░░░░░░░░░░░  (0.0)`

## Step 7 — Format Full Report

Present the report in this exact structure:

```
## Sentiment Analysis: {TICKER} — {Company Name}
*Last 24 hours · As of {UTC timestamp}*

### Composite Sentiment Score

**{composite_score} / 10 — {Label}**

{ASCII bar}

[If total sources < 5: ⚠️ Low data volume ({n} total sources) — composite may not be representative.]

### Channel Breakdown

| Channel | Score | Signal | Volume | Notes |
|---------|-------|--------|--------|-------|
| News | {news_score} | {label} | {n} articles | {top source domains} |
| StockTwits | {st_score} | {label} | {total_labeled} labeled | {bullish}/{bearish} ratio |
| Reddit (WSB) | {wsb_score} | {label} | {n} posts | avg ↑{avg_upvotes} |
| Reddit (r/stocks) | {rs_score} | {label} | {n} posts | avg ↑{avg_upvotes} |

(Use "N/A" in Score column for unavailable channels; explain in Notes)

### Key Headlines (past 24h)

- [{score}] "{title}" — {source}
- [{score}] "{title}" — {source}
- [{score}] "{title}" — {source}

### Notable Reddit Posts

- [WSB · ↑{upvotes}] "{title}" · {Bullish | Neutral | Bearish}
- [WSB · ↑{upvotes}] "{title}" · {Bullish | Neutral | Bearish}
- [r/stocks · ↑{upvotes}] "{title}" · {Bullish | Neutral | Bearish}
- [r/stocks · ↑{upvotes}] "{title}" · {Bullish | Neutral | Bearish}

### StockTwits Sample

- 🟢 Bullish: "{sample_bullish_message}"
- 🔴 Bearish: "{sample_bearish_message}"

---

### Data Source Log
- **News:** {NewsAPI (key configured) | WebSearch fallback} · {n} articles · {domain breakdown}
- **Reddit WSB:** {Direct JSON | sort=new retry | WebSearch fallback | Unavailable} · {n} posts
- **Reddit r/stocks:** {Direct JSON | sort=new retry | WebSearch fallback | Unavailable} · {n} posts
- **StockTwits:** {Direct API | Unavailable} · {total_labeled} labeled messages

---
*For informational purposes only. Not financial advice. Sentiment scores derived
from public sources and AI analysis. Verify independently before making investment decisions.*
```
