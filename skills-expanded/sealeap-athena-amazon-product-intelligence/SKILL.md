---
name: sealeap-athena-amazon-product-intelligence
description: "核对 Amazon 商品详情，比较竞品规格，分析当前与历史价格、排名和销量估计。用于已知 ASIN 的深入拆解与多源校准。"
---

# Amazon 商品情报与竞品比较

核对 Amazon 商品详情，比较竞品规格，分析当前与历史价格、排名和销量估计。用于已知 ASIN 的深入拆解与多源校准。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon 商品页面核对](references/capabilities/amazon-page-detail/workflow.md) | 读取当前可见价格、规格、变体、卖点与配送信息，保留页面观察条件 |
| [Amazon 商品结构化分析](references/capabilities/amazon-structured-product-detail/workflow.md) | 将商品详情、变体和分析报告拆成一方事实与第三方估计并统一单位 |
| [Amazon 竞品对比](references/capabilities/amazon-competitor-compare/workflow.md) | 对齐变体、规格和期间后比较商品、需求及流量差异 |
| [Amazon 价格排名快照](references/capabilities/amazon-price-rank-snapshot/workflow.md) | 获取价格、排名与商品事实，区分报价来源、条件和观察时点 |
| [Amazon 价格排名历史](references/capabilities/amazon-price-rank-history/workflow.md) | 对齐历史价格、排名和销量估计，保留原频率与缺失段 |
| [Amazon 销量估计核验](references/capabilities/amazon-sales-estimate-check/workflow.md) | 使用已验证估算接口并与同窗其他来源核对偏差 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。详情、比较、当前/历史价格排名与销量校准分别读取对应参考文件。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
