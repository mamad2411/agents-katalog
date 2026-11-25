---
name: sealeap-athena-tiktok-content-management
description: "处理 TikTok 内容账户的授权、视频管理及视频商品关系。用于已授权内容账号操作，与 TikTok Shop 的账户和权限分别核对。"
---

# TikTok 内容账户与视频管理

处理 TikTok 内容账户的授权、视频管理及视频商品关系。用于已授权内容账号操作，与 TikTok Shop 的账户和权限分别核对。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [TikTok 内容账户 账户授权检查](references/capabilities/tiktok-content-auth/workflow.md) | 先读取既有连接的非敏感状态；需要新授权时通过官方流程绑定明确账户，再回读身份 |
| [TikTok 内容账户 视频管理](references/capabilities/tiktok-content-video/workflow.md) | 核对视频及商品关系，准备内容或状态变更预览，执行授权操作并查看发布状态 |
| [TikTok 内容账户 视频商品关系](references/capabilities/tiktok-content-video-products/workflow.md) | 读取视频商品列表与权限，核对商品可售状态后准备绑定或移除草稿 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。内容账号授权与 TikTok Shop 授权独立；视频发布/关联按实际权限执行。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
