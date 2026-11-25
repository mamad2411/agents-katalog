---
name: sealeap-athena-shopee-account-management
description: "处理 Shopee 账户健康、授权检查、商户与店铺资料、公共参数和事件订阅配置，按目标模式核对读写权限与生效状态。"
---

# Shopee 账户、店铺与事件配置

处理 Shopee 账户健康、授权检查、商户与店铺资料、公共参数和事件订阅配置，按目标模式核对读写权限与生效状态。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Shopee 账户健康](references/capabilities/shopee-account-account-health/workflow.md) | 读取健康与违规记录，按时限和业务影响排序并准备证据补正 |
| [Shopee 账户授权检查](references/capabilities/shopee-account-auth/workflow.md) | 先读取既有连接的非敏感状态；需要新授权时通过官方流程绑定明确账户，再回读身份 |
| [Shopee 商户资料](references/capabilities/shopee-account-merchant/workflow.md) | 读取商户资料与获准店铺映射，核对权限和对象后准备目标变更 |
| [Shopee 平台公共参数](references/capabilities/shopee-account-public/workflow.md) | 读取当前公开时间、地区、语言或基础枚举，记录版本和使用范围 |
| [Shopee 事件订阅管理](references/capabilities/shopee-account-push/workflow.md) | 核对当前订阅与事件 schema，准备授权配置，检查签名、重放和去重处理 |
| [Shopee 店铺资料](references/capabilities/shopee-account-shop/workflow.md) | 读取当前店铺资料并校对身份，生成资料变更预览，按授权更新回读 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。账户健康、商户/店铺资料与事件订阅按模式处理，配置写入保留授权。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
