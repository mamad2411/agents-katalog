---
name: sif-mcp-router
description: Route Amazon seller analysis requests to the right SIF MCP tool domain. Use when the user mentions SIF MCP, Amazon traffic diagnosis, 流量下跌, 流量结构, Listing traffic, ASIN sales trend, 关键词需求, keyword competition, 反查关键词, 广告结构, Campaign 贡献, Ad Group 表现, or asks for a data-backed Amazon运营分析 workflow using SIF.
---

# SIF MCP Router

这个 skill 是总入口。目标不是一次把所有工具都打完，而是先判断问题属于哪个域，再进入对应的 1 到 3 个工具组合。

## 触发原则

以下场景优先使用本 skill：

- 用户明确提到 `SIF`、`SIF MCP`
- 用户要做亚马逊运营诊断，但更像“查数 + 判断”而不是泛泛建议
- 用户的问题落在流量、关键词、广告三类中的任意一类
- 用户的问题跨域，比如“流量跌了，是关键词问题还是广告问题”

## 先做路由，再做分析

### 1. 流量 / 销量域

适合：

- 流量涨跌
- 渠道结构变化
- 流量变化是否传导到销量

优先工具：

- `ops_get_asin_traffic_trend`
- `ops_get_asin_traffic_trend_detail`
- `ops_get_listing_traffic_overview`
- `ops_get_listing_traffic_structure`
- `ops_get_asin_sales_trend`

### 2. 反查关键词

适合：

- 这个 ASIN 靠什么词在带量
- 某个 ASIN 在核心词上的竞争位置

优先工具：

- `ops_get_listing_keyword_distribution`
- `market_get_asin_keyword_signals`

### 3. 关键词研究

适合：

- 某个关键词值不值得继续打
- 需求是否在涨
- 竞争是否过挤

优先工具：

- `market_get_keyword_demand`
- `market_get_keyword_history`
- `market_get_keyword_root_trend`
- `market_get_keyword_competition`

约束：

- `market_get_keyword_demand` 当前仅支持美国站

### 4. 广告结构

适合：

- ASIN 广告结构复盘
- Campaign / Ad Group 带量与拖后腿判断
- 广告打法变化复盘

优先工具：

- `ads_get_asin_ad_structure`
- `ads_get_asin_ad_traffic_trend`
- `ads_get_asin_ad_feature_profile`
- `ads_get_asin_campaign_contribution_overview`
- `ads_get_campaign_structure`
- `ads_get_campaign_contribution_breakdown`
- `ads_get_ad_group_keyword_breakdown`

### 5. 异常诊断

适合：

- 流量突然下跌
- 想直接定位广告侧 / 自然侧 / 复合型根因

优先工具：

- `analyze_traffic_anomaly`

关键要求：

- 在提问或调用意图里明确写出工具名 `analyze_traffic_anomaly`

## 工作流

1. 先识别对象是 `ASIN`、`Listing` 还是 `关键词`
2. 再识别问题是“趋势”“结构”“竞争”“根因”哪一类
3. 先用 1 到 3 个最相关工具拿到第一层结论
4. 如果结论仍不足，再向下钻一层，不要一开始全量铺开
5. 输出时明确区分“数据事实”“分析判断”“建议动作”

## 输出格式

默认按以下结构返回：

1. 结论
2. 关键证据
3. 根因或机会判断
4. 本周优先动作
5. 下一步建议补查项

## 参考

需要更细的映射和问法时，再读 `references/tool-routing.md`。
