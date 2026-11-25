---
name: report-consulting
description: >
  查询应用中已生成的投研分析报告（analysis_reports）：按账户、类型、时间检索历史报告并引用要点。
  当用户问"之前生成的报告"、"我的分析报告"、"上次那份 XX 报告"、
  或分析时需要引用历史报告结论时，**务必使用此技能**。
version: "1.0.0"
category: report
author: investment-agent
---

# 投研报告查询

## 检索报告

用 `dbQueryTool` 查表 `analysis_reports`（列：account_id, type, title, content, createdAt）：

```json
{"table": "analysis_reports", "orderBy": "created_at", "limit": 20}
```

- 按账户：`{"table": "analysis_reports", "whereColumn": "account_id", "whereValue": 1, "orderBy": "created_at"}`
- 按类型：`whereColumn: "type"`（如组合分析、风险评估等报告类型）。
- 软删除的报告会自动过滤。

## 引用要求

1. 报告内容可能较长：优先引用 title、createdAt、type、结论段落；`content` 过长时提炼，不要整段粘贴。
2. 引用时注明报告生成日期与所属账户，历史结论要和当前数据（`accountBalanceTool`、`stockGetPriceTool` 等）区分时点。
3. 报告结论与当前市场状态冲突时，同时呈现，并默认当前数据为准。

## 生成新报告

Agent 侧没有"生成报告"工具。用户要正式报告时，告知在应用"报告"页面生成；Agent 可以先在对话中完成分析框架（配合 portfolio-management、market-data-lookup 等技能），结果可作为素材。
