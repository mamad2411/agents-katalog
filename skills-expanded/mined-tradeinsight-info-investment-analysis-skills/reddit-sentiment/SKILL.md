---
name: reddit-sentiment
description: >
  This skill should be used when the user asks about Reddit sentiment,
  WallStreetBets opinion, r/stocks discussion, retail investor sentiment,
  social media sentiment on Reddit, what Reddit thinks about a stock,
  or whether Reddit is bullish or bearish on a ticker.
---

# Reddit Sentiment Analysis

## Purpose

Fetch top posts mentioning a ticker from r/wallstreetbets and r/stocks (past 24 hours),
score post titles for sentiment using engagement weighting, and produce a Reddit channel
score from -10 to +10.

## Step 1 — Resolve Ticker and Company Name

Confirm both ticker and company name via WebSearch if needed.

## Step 2 — Fetch r/wallstreetbets

WebFetch with required header `User-Agent: sentiment-analysis-skill/1.0`:

```
https://www.reddit.com/r/wallstreetbets/search.json?q={ticker}&sort=hot&t=day&limit=15&restrict_sr=1
```

**If the response is empty, has fewer than 3 posts, or returns a redirect/login page:**
1. Retry with `sort=new` instead of `hot`
2. If still empty, fall back to WebSearch: `site:reddit.com/r/wallstreetbets {ticker}`
   and extract post titles from search snippets. Record: `wsb_fallback = "WebSearch"`
3. If WebSearch also yields nothing, set `wsb_available = false`

Extract per post: `title`, `score` (upvotes), `upvote_ratio`.

## Step 3 — Fetch r/stocks

Same process for:

```
https://www.reddit.com/r/stocks/search.json?q={ticker}&sort=hot&t=day&limit=15&restrict_sr=1
```

Same retry/fallback sequence. Set `rstocks_available = false` if all fail.

## Step 4 — Score Posts

For each post:

**Engagement weight** = `upvote_ratio × log(max(score, 0) + 1)`

If `score <= 0`, `max(score, 0) + 1 = 1`, so `log(1) = 0` — downvoted posts get zero weight.
If all posts in a subreddit have weight 0, use unweighted average instead.

**Sentiment score** (-1.0 to +1.0 per title):
- 🚀 rocket emoji, "moon", "calls", "YOLO", "to the moon" → bullish (+0.6 to +1.0)
- "puts", "crash", "overvalued", "short squeeze" (as threat) → bearish (-0.6 to -1.0)
- "DD" posts, questions, neutral analysis → score on content (−0.3 to +0.3)
- WSB irony ("this is not financial advice", "loss porn") → near 0.0

**Weighted average per subreddit:**

```
weighted_avg = sum(sentiment_i × weight_i) / sum(weight_i)
subreddit_score = weighted_avg × 10
```

**Top 3 posts per subreddit** = the 3 posts with the **highest engagement weight**
(popularity signals community conviction on Reddit; not highest absolute sentiment).

## Step 5 — Compute Reddit Channel Score

```
reddit_score = (wsb_score + rstocks_score) / 2
```

If one subreddit is unavailable, use the other's score directly.
If both are unavailable, set `reddit_available = false`.

## Step 6 — Output

```
REDDIT SENTIMENT RESULT
Ticker: {ticker}
Reddit Channel Score: {reddit_score} / 10
  WSB Score: {wsb_score} / 10 ({wsb_post_count} posts) [or "Unavailable"]
  r/stocks Score: {rstocks_score} / 10 ({rstocks_post_count} posts) [or "Unavailable"]
Signal: {label per signal bands below}
Fallback Notes: {any fallbacks triggered, or "none"}

Top WSB Posts (by engagement weight):
1. [↑{upvotes} | {upvote_ratio}] "{title}" → {Bullish | Neutral | Bearish}
2. ...
3. ...

Top r/stocks Posts (by engagement weight):
1. [↑{upvotes} | {upvote_ratio}] "{title}" → {Bullish | Neutral | Bearish}
2. ...
3. ...
```

Signal bands (applied to reddit_score):
- score >= +7.0 → Very Bullish
- score >= +3.0 and < +7.0 → Bullish
- score > -3.0 and < +3.0 → Neutral
- score <= -3.0 and > -7.0 → Bearish
- score <= -7.0 → Very Bearish
