---
name: hot-topics
description: Discover trending topics and sectors being discussed by finance YouTubers. Use when users want to know what's hot in the market.
---

# Hot Topics Tracker

Discover trending topics and sectors being discussed by finance YouTubers.

## Triggers

- "最近热点是什么"
- "大家在讨论什么"
- "hot topics"
- "what's trending"
- "热门话题"
- `/hot-topics`

## Instructions

When the user wants to know current hot topics, follow these steps:

1. **Get All Tickers with Mention Counts**
   Call `list_tickers` to see which stocks are being discussed most.

2. **Get Daily Summary**
   Call `get_daily_summary` to understand the overall market narrative.

3. **Search for Theme Keywords**
   Call `search_viewpoints` with common themes to identify trending topics:
   - "AI" / "人工智能"
   - "财报" / "earnings"
   - "降息" / "rate cut"
   - "芯片" / "semiconductor"
   - Other relevant keywords based on context

4. **Categorize and Rank**
   Group findings by:
   - Sectors (Tech, Finance, Healthcare, etc.)
   - Themes (AI, Earnings, Macro, etc.)
   - Individual hot stocks

5. **Present Results**
   Format the output as:

   ```
   ## 本周热点追踪 🔥

   ### 热门板块
   1. **科技股** - XX 次提及
      - 代表股票: NVDA, AAPL, MSFT
      - 主要话题: AI、云计算

   2. **半导体** - XX 次提及
      - 代表股票: AMD, INTC, TSM
      - 主要话题: 产能、周期

   ### 热门话题
   1. **AI 投资** 🤖
      - 相关股票: NVDA, MSFT, GOOGL
      - 代表观点: "[观点摘要]" — 博主A

   2. **财报季** 📊
      - 关注股票: TSLA, META
      - 代表观点: "[观点摘要]" — 博主B

   ### 本周最热门股票 Top 5
   | 排名 | 股票 | 提及次数 | 主流情绪 |
   |------|------|----------|----------|
   | 1 | NVDA | 45 | 🟢 看涨 |
   | 2 | TSLA | 32 | 🟡 分歧 |
   | ... | ... | ... | ... |

   ### 值得关注的冷门观点
   [列出一些有价值但不热门的独特观点]
   ```

## Tool Sequence

1. `list_tickers` → Get mention counts
2. `get_daily_summary` → Get market overview
3. `search_viewpoints("AI")` + `search_viewpoints("earnings")` + other keywords → In parallel
4. Compile and categorize findings

## Notes

- Focus on what's actually being discussed, not just mentioned
- Highlight emerging themes that may not be mainstream yet
- Include both consensus and contrarian viewpoints
