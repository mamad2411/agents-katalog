---
name: news-sentiment
description: >
  This skill should be used when the user asks about news sentiment,
  media coverage tone, recent headline analysis, financial news sentiment,
  how the press is covering a stock, or news-driven market mood for a
  publicly traded company.
---

# News Sentiment Analysis

## Purpose

Fetch financial news articles for a company published in the past 24 hours and score
each headline for sentiment. Produce a news channel score from -10 (very bearish) to
+10 (very bullish).

## Step 1 — Resolve Ticker and Company Name

If a ticker is provided, confirm the company name via WebSearch:
`{ticker} stock company name site:finance.yahoo.com OR site:stockanalysis.com`

If only a company name is provided, resolve the ticker the same way.

## Step 2 — Read Config for NewsAPI Key

Run:

```bash
cat ${CLAUDE_PLUGIN_ROOT}/config.json 2>/dev/null
```

If the file exists and contains `newsapi.key` (i.e., `config["newsapi"]["key"]`),
proceed to Step 3a. Otherwise proceed to Step 3b (WebSearch fallback).

## Step 3a — Fetch via NewsAPI (key available)

WebFetch the following URL, substituting:
- `{ticker}`: the stock ticker symbol
- `{company_name}`: URL-encoded company name
- `{ISO_24h_ago}`: current UTC time minus 24 hours in format `YYYY-MM-DDTHH:MM:SSZ`
- `{KEY}`: the resolved string value of `config["newsapi"]["key"]`

```
https://newsapi.org/v2/everything?q={ticker}%20OR%20%22{company_name}%22&from={ISO_24h_ago}&sortBy=publishedAt&language=en&pageSize=20&apiKey={KEY}
```

Extract from each article: `title`, `description`, `source.name`, `publishedAt`, `url`.
Use the first 20 results.

## Step 3b — WebSearch Fallback (no key)

Run WebSearch:
`"{company_name}" OR "{ticker}" stock news site:reuters.com OR site:bloomberg.com OR site:seekingalpha.com OR site:finance.yahoo.com`

Extract up to 20 headline + description pairs from search results.
Record source as `"WebSearch"` and note in output: "News via WebSearch — no NewsAPI key configured"

## Step 4 — Score Headlines

For each article headline + description pair, assign a score from -1.0 to +1.0:

- **+0.8 to +1.0**: Record earnings beat, major upgrade, regulatory approval, significant partnership
- **+0.4 to +0.7**: Positive guidance, price target raise, solid quarterly results, market share gains
- **0.0**: Neutral announcements, routine filings, personnel changes with no clear valuation impact
- **-0.4 to -0.7**: Missed estimates, minor regulatory concern, analyst downgrade
- **-0.8 to -1.0**: Major investigation, fraud allegation, severe earnings miss, CEO departure under fire

Score the combination of headline + description together. A positive headline with a
cautionary description should score lower than the headline alone suggests.

## Step 5 — Compute Channel Score

```
news_score = mean(all_headline_scores) × 10
```

Identify the 3 articles with the **highest absolute score value** (strongest signal,
regardless of direction — these are the most signal-rich stories). These are the
"key headlines" to surface in output.

## Step 6 — Handle Low Volume

If fewer than 5 articles were found, add this warning to output:
"⚠️ Low news volume ({n} articles) — score may not be representative"

## Step 7 — Output

Return the following structured result (consumed by sentiment-report and sentiment-analyst):

```
NEWS SENTIMENT RESULT
Ticker: {ticker}
Company: {company_name}
Channel Score: {news_score} / 10
Signal: {label per signal bands below}
Article Count: {n}
Source: {NewsAPI | WebSearch}
Low Volume Warning: {yes | no}

Key Headlines (highest absolute sentiment score):
1. [{score}] "{title}" — {source_name}
   {url}
2. [{score}] "{title}" — {source_name}
   {url}
3. [{score}] "{title}" — {source_name}
   {url}
```

Signal bands:
- score >= +7.0 → Very Bullish
- score >= +3.0 and < +7.0 → Bullish
- score > -3.0 and < +3.0 → Neutral
- score <= -3.0 and > -7.0 → Bearish
- score <= -7.0 → Very Bearish
