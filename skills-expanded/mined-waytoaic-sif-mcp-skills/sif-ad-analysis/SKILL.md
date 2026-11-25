---
name: sif-ad-analysis
description: Analyze Amazon ad structure and contribution with SIF MCP. Use when the user asks for 广告结构复盘, ad structure, Campaign contribution, Ad Group performance, ASIN 广告趋势, 投放节奏变化, or wants to know which campaign or ad group is bringing traffic or dragging performance.
---

# SIF 广告分析

这个 skill 专门处理广告结构、分层贡献和投放节奏变化。

## 适用问题

- ASIN 最近广告结构怎么变了
- 哪个 Campaign 在带量
- 哪个 Campaign 或 Ad Group 在拖后腿
- 最近广告打法是否发生变化
- 是否需要从 ASIN 层往下钻到 Campaign / Ad Group 层

## 分层工具路径

### ASIN 层

- `ads_get_asin_ad_structure`
- `ads_get_asin_ad_traffic_trend`
- `ads_get_asin_ad_feature_profile`
- `ads_get_asin_ad_historical_feature_profile`
- `ads_get_asin_ad_window_feature_profile`
- `ads_get_asin_campaign_contribution_overview`
- `ads_get_asin_campaign_changes`

### Campaign 层

- `ads_get_campaign_structure`
- `ads_get_campaign_traffic_trend`
- `ads_get_campaign_contribution_breakdown`

### Ad Group 层

- `ads_get_ad_group_traffic_trend`
- `ads_get_ad_group_keyword_breakdown`

## 推荐分析顺序

1. 先在 ASIN 层看整体结构和趋势
2. 找出贡献最高和变化最大的 Campaign
3. 再向下看该 Campaign 内部哪个 Ad Group 或关键词在驱动变化
4. 输出保留、扩量、收缩、观察四类动作

## 输出要求

默认输出：

1. 广告结构结论
2. 主要贡献者
3. 主要拖累项
4. 投放节奏变化
5. 本周动作建议

## 问法模板

```text
帮我拆 ASIN B0XXXXXXX 最近 30 天的广告结构，
从 ASIN、Campaign、Ad Group 三层看谁在带量、谁在掉量，
最后给我保留、放大、收缩三类动作建议。
```
