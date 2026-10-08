---
name: consensus
description: Find stocks with consensus sentiment across multiple finance YouTubers. Use when looking for stocks that multiple bloggers agree on (bullish or bearish).
---

# Consensus Stock Finder

Find stocks with consensus sentiment across multiple finance YouTubers.

## Triggers

- "找共识股票"
- "大家都看好什么"
- "哪些股票被一致看好"
- "consensus stocks"
- "what does everyone agree on"
- `/consensus`

## Instructions

When the user wants to find consensus stocks (stocks that multiple bloggers agree on), follow these steps:

1. **Get Daily Summary**
   Call `get_daily_summary` to identify the current hot tickers and overall market sentiment.

2. **Analyze Top Tickers**
   For each ticker mentioned frequently in the summary, call `get_ticker_sentiment` to get detailed sentiment breakdown by blogger.

3. **Identify Consensus**
   Find stocks where:
   - 3+ bloggers have the same sentiment (bullish or bearish)
   - No strong opposing views exist

4. **Present Results**
   Format the output as:

   ```
   ## 共识看涨 🟢

   ### TICKER1
   - 看涨博主 (X位): 博主A, 博主B, 博主C
   - 关键观点: [摘要主要看涨理由]

   ### TICKER2
   ...

   ## 共识看跌 🔴

   ### TICKER3
   - 看跌博主 (X位): 博主D, 博主E
   - 关键观点: [摘要主要看跌理由]

   ## 分歧较大 ⚠️
   [列出多空分歧明显的股票]
   ```

## Tool Sequence

1. `get_daily_summary` → Get overview
2. `get_ticker_sentiment(ticker)` → For each hot ticker (up to 10)
3. Analyze and present consensus

## Notes

- Focus on actionable consensus, not just popularity
- Highlight when there's strong disagreement (potential controversy)
- Include the number of bloggers agreeing on each position
