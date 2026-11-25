---
name: sealeap-athena-tiktok-shop-order-fulfillment
description: "处理 TikTok Shop 订单核对、物流配置与轨迹、发货和退货退款，区分查询与实际业务动作，保留店铺权限和回读结果。"
---

# TikTok Shop 订单、物流与售后

处理 TikTok Shop 订单核对、物流配置与轨迹、发货和退货退款，区分查询与实际业务动作，保留店铺权限和回读结果。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [TikTok Shop 订单核对](references/capabilities/tiktok-shop-orders/workflow.md) | 读取订单头与行项目，按订单 ID 对齐支付、费用、取消和履约状态 |
| [TikTok Shop 订单发货](references/capabilities/tiktok-shop-fulfillment/workflow.md) | 读取待发货订单并核对地址/包裹数量；按授权提交发货并回读每件状态 |
| [TikTok Shop 物流配置与轨迹](references/capabilities/tiktok-shop-logistics/workflow.md) | 核对可用物流渠道、费用与限制，读取轨迹并处理授权的配置或单据动作 |
| [TikTok Shop 退货退款](references/capabilities/tiktok-shop-returns-refunds/workflow.md) | 读取售后请求与订单行，核对金额上限、退货与退款状态，准备或执行授权处理 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。查询、发货、退货和退款各有独立执行条件与回读要求。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
