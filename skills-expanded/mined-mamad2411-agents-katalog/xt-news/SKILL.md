---
name: xt-news
description: Crypto news and XT announcements. Use when the user asks about the latest news/flash updates, why a coin went up or down, XT listing/delisting/maintenance announcements, whether a coin is listed on XT, or market sentiment and buzz. No API Key required.
---

# News and Announcements

Obtained via the `xt-tradekit` MCP tools. XT announcements are official data; flash updates and sentiment come from TradeKit aggregated public information sources (media names may be kept in the output; other exchanges are not involved).

## Intent Routing

| User intent | Tool combination |
|---------|---------|
| Latest news / what's big today | `market_news` (lang per the user's language) |
| News about a specific coin | `market_news` (keyword=coin name) |
| Why it went up/down (event attribution) | `market_news` (keyword) + `xt_futures_klines` (locate the anomaly time) + `market_recent_liquidations` |
| Latest XT announcements / listings / delistings / maintenance | `xt_announcements` (locale per the user's language) |
| Whether a coin is listed on XT / find an announcement | `xt_announcement_search` (keyword=coin name) |
| Market sentiment / how's the buzz | `market_sentiment_snapshot` + `market_fear_greed` |

## Event Attribution Flow ("why did it surge/crash")

1. Use `xt_futures_klines` to locate the time window of the anomaly (find a high-volume large green/red candle).
2. Use `market_news` (keyword=coin name) to find news near the anomaly time.
3. Use `market_recent_liquidations` + `market_open_interest` to see whether it was driven by leveraged liquidations.
4. Output: anomaly time → candidate causes (ranked by temporal correlation) → supporting data; if no clear cause is found, state honestly "No clear news-driven cause; more likely capital-flow/technical behavior."

## Guidelines

- **Separate facts from opinions**: official announcements and time-stamped news are facts; sentiment indices and buy/sell ratios are derived indicators, labeled as "sentiment signals".
- Note the publish time for news items; keep original titles when quoting, without exaggeration.
- When the user asks in Chinese: use `locale=zh-cn` for announcements and `lang=zh` for flash updates; otherwise use English sources.
- For announcement questions, prefer `xt_announcement_search` over paging through the list.
- Always end with: "The above is aggregated information and does not constitute investment advice."

## Output Guidelines

- News list: time + title + one-line summary, with an optional link; no more than 10 items.
- Announcements: title + time + link, with listing/delisting items highlighted.

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
