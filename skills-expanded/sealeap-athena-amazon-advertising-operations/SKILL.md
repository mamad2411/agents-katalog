---
name: sealeap-athena-amazon-advertising-operations
description: "处理 Amazon Ads 账户授权、广告报表、专项洞察和广告管理任务。先区分分析与实际变更，再按已有权限执行相应操作并核对结果。"
---

# Amazon 广告报表、诊断与管理

处理 Amazon Ads 账户授权、广告报表、专项洞察和广告管理任务。先区分分析与实际变更，再按已有权限执行相应操作并核对结果。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon Ads 账户授权检查](references/capabilities/amazon-ads-auth/workflow.md) | 先读取既有连接的非敏感状态；需要新授权时通过官方流程绑定明确账户，再回读身份 |
| [Amazon Ads 广告管理](references/capabilities/amazon-ads-management/workflow.md) | 先读广告实体与同窗报表，形成出价、预算或状态差异，执行已授权对象并回读 |
| [Amazon Ads 经营报表](references/capabilities/amazon-ads-report/workflow.md) | 优先读取同口径已有报告；必要时按授权创建报表任务，追踪任务 ID 后下载并核对总量 |
| [Amazon Ads 广告专项洞察](references/capabilities/amazon-ads-insights/workflow.md) | 确认当前支持的专项报告类型与资格，读取或创建报告并核对分片字段和总量 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。报表、专项洞察和广告变更分模式；广告 API 与 SP-API 的授权独立。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
