---
name: sealeap-athena-tiktok-shop-catalog-analytics
description: "处理 TikTok Shop 的账户授权、商品管理和自家店铺经营分析，按市场与当前 schema 核对商品及指标。订单、物流与退款使用履约售后入口。"
---

# TikTok Shop 商品与经营分析

处理 TikTok Shop 的账户授权、商品管理和自家店铺经营分析，按市场与当前 schema 核对商品及指标。订单、物流与退款使用履约售后入口。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [TikTok Shop 账户授权检查](references/capabilities/tiktok-shop-auth/workflow.md) | 先读取既有连接的非敏感状态；需要新授权时通过官方流程绑定明确账户，再回读身份 |
| [TikTok Shop 商品管理](references/capabilities/tiktok-shop-product/workflow.md) | 读取商品现状与当前类目 schema，生成字段级变更预览，验证后执行授权范围并回读 |
| [TikTok Shop 经营分析](references/capabilities/tiktok-shop-analytics/workflow.md) | 获取正式分析或导出表，对齐订单、商品、内容与归因窗口，再解释经营变化 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。保留店铺主体、地区、商品 schema 和经营指标口径。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
