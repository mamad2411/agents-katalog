---
name: sif-keyword-research
description: Research Amazon keyword demand, competition, and ASIN keyword signals with SIF MCP. Use when the user asks about 关键词需求, keyword demand, keyword lifecycle, 竞争格局, 是否值得打某个词, 词根趋势, ASIN 靠哪些词带量, or wants data-backed keyword opportunity analysis.
---

# SIF 关键词研究

这个 skill 聚焦两类问题：

- 一个关键词本身值不值得做
- 一个 ASIN 靠哪些关键词在带量

## 场景一：研究关键词本身

适合：

- 关键词需求是否在涨
- 这个词处于什么生命周期阶段
- 这个词竞争有多挤
- 词根和精确词哪个更值得投入

优先工具：

- `market_get_keyword_demand`
- `market_get_keyword_history`
- `market_get_keyword_root_trend`
- `market_get_keyword_competition`

约束：

- `market_get_keyword_demand` 当前仅支持美国站

## 场景二：从 ASIN 反查关键词

适合：

- 这个 ASIN 靠哪些词带流量
- 哪些词是真正的核心词
- 它在核心词上的竞争位置如何

优先工具：

- `ops_get_listing_keyword_distribution`
- `market_get_asin_keyword_signals`

## 分析顺序

### 当对象是关键词

1. 先判断需求阶段
2. 再看历史与词根变化
3. 最后评估竞争强度与可进入性

### 当对象是 ASIN

1. 先看词分布
2. 再看各词上的排名与竞争位置
3. 最后筛出最值得跟踪的核心词

## 输出要求

默认输出：

1. 是否值得做
2. 证据
3. 风险点
4. 推荐动作

## 问法模板

```text
帮我判断关键词 "wireless earbuds" 现在是否值得继续重点投入，
需要覆盖需求阶段、历史趋势、词根趋势和竞争格局，
最后直接给结论和动作建议。
```

```text
帮我反查 ASIN B0XXXXXXX 的核心流量词，
看哪些词在带量、哪些词更值得继续跟踪。
```
