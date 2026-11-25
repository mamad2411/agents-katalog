---
name: market-data-lookup
description: >
  查询市场数据：资产价格与历史走势、资产搜索、个股新闻、公司基本面资料、互联网信息。
  当用户问"XX 现在多少钱"、"XX 走势"、"帮我看看这只股票"、"XX 公司是什么情况"、"最近有什么新闻"，
  或任何需要实时行情/资讯支撑的分析时，**务必使用此技能**取数。
version: "1.0.0"
category: market
author: investment-agent
---

# 行情与资讯查询

## 工具选型（按优先级，逐级降级）

| 需求 | 工具 | 说明 |
|------|------|------|
| 搜索资产（股票/基金/黄金），确认代码与市场 | `searchAssetInfoTool` | 询问资产价格**必须**先走这里 |
| 某标的当前/历史价格 | `stockGetPriceTool` | `stock_code` 如 `AAPL`、`600519`、`0700.HK`；`start_date`/`end_date`（YYYY-MM-DD），默认近 30 天 |
| 个股最新消息、财报、产品动态 | `stockSearchNewsTool` | 参数 `symbol` |
| 公司资料库（财务信息、管理层、季度财报历史） | `stockRecallCompanyInfoTool` | 本地知识库优先，命中就不用上网 |
| 互联网补充信息 | `TravilySearchTool` | 本地工具查不到、或需要市场上额外观点时再用 |

## 流程

1. 用户提到资产但给了名字（"英伟达"）→ 先 `searchAssetInfoTool` 确认代码，再查价格。
2. 价格查询：区间未指定时默认用最近 30 天；用户要更长历史就传 start_date。
3. 分析一只股票：`stockGetPriceTool` + `stockSearchNewsTool` + `stockRecallCompanyInfoTool` 三件套组合，缺信息的部分再 `TravilySearchTool` 补网络信息。
4. 结论中标注数据时点与来源（本地行情 / 知识库 / 互联网搜索）。

## 注意

- 代码格式要与市场匹配：美股 `AAPL`，A 股 `600519`，港股 `0700.HK`。
- 互联网搜索结果可能过时或有误，涉及价格、财务数据时以本地行情工具为准，搜索结果只做背景。
- 深度分析（估值、技术面、风险）的框架请使用对应分析技能（stock-analysis、technical-analysis 等），本技能只负责数据获取。
