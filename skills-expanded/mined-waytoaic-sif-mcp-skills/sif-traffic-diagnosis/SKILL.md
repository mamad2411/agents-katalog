---
name: sif-traffic-diagnosis
description: Diagnose Amazon traffic changes with SIF MCP. Use when the user asks why an ASIN or Listing 流量下跌/上涨, wants traffic trend analysis, 流量结构拆解, 自然流和广告流变化, listing traffic overview, or wants to judge whether traffic changes already affected sales.
---

# SIF 流量诊断

这个 skill 只处理流量与销量的诊断，不扩展到选品或完整广告审计。

## 适用问题

- 最近流量为什么跌了
- 自然流和广告流分别怎么变了
- 哪个渠道掉得最明显
- 流量变化是否已经影响销量
- 需要对最近 2 到 8 周做趋势复盘

## 默认工具路径

优先按下面顺序取数：

1. `ops_get_asin_traffic_trend`
2. `ops_get_asin_traffic_trend_detail`
3. `ops_get_listing_traffic_overview`
4. `ops_get_listing_traffic_structure`
5. `ops_get_asin_sales_trend`

如果用户明确要“根因诊断”，额外使用：

- `analyze_traffic_anomaly`

注意：

- 为了让异常诊断更稳，在任务描述里明确写 `analyze_traffic_anomaly`

## 分析顺序

1. 先看总流量是短期波动还是连续下滑
2. 再看是自然流、广告流、品牌流哪个渠道变动最大
3. 再看关键词或渠道拆分，判断是单点丢失还是整体走弱
4. 最后核对销量趋势，确认问题是否已经传导到业务结果

## 输出要求

默认输出 5 段：

1. 当前状态
2. 关键变化
3. 最可能根因
4. 本周优先动作
5. 需要继续监控的指标

## 问法模板

```text
请使用 analyze_traffic_anomaly，
诊断 ASIN B0XXXXXXX 最近 4 周流量下跌的根因，
并结合流量结构和销量趋势给出本周动作。
```
