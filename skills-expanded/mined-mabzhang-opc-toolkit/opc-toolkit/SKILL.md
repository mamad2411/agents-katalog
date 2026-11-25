---
name: opc-toolkit
description: >
  Intelligently route Chinese brand-marketing work to the correct OPC Toolkit
  workflow and coordinate multiple skills when needed. Use when a request is
  broad, ambiguous, spans several marketing disciplines, explicitly mentions
  OPC Toolkit, or needs help choosing among brief analysis, competitor research,
  consumer insight, campaign planning, social content, platform adaptation,
  platform specifications, proposal writing, and task decomposition. Trigger
  for: $opc-toolkit, OPC工具包, 营销工作流, 不知道用哪个技能, 综合营销任务.
---

# OPC Toolkit — 智能营销路由器

把用户需求路由到最小且足够的营销工作流。不要机械地运行全部技能；先判断任务类型，再选择一个主技能，必要时组合少量子技能。

## 路由规则

| 用户真正要解决的问题 | 主技能 | 可选前置/后续 |
|---|---|---|
| 零散 Brief、聊天记录、会议纪要需要归一 | `$brief-analysis` | 后续 `$task-decomposition` |
| 完整营销全案、比稿、跨模块编排 | `$opc-proposal` | 按需组合研究、提案、任务拆解 |
| 竞品定位、近期动作、内容/KOL/渠道比较 | `$competitor-analysis` | 后续 `$campaign-planning` |
| 目标人群、购买障碍、JTBD、内容触发 | `$consumer-insight` | 后续内容或 Campaign |
| Campaign、节点、新品、创意主题、传播节奏 | `$campaign-planning` | 前置洞察，后续提案 |
| 社媒矩阵、月历、选题、平台分工 | `$social-media-plan` | 后续 `$platform-adaptation` |
| 同一卖点改成不同平台原生版本 | `$platform-adaptation` | 按需核验 `$platform-specs` |
| 尺寸、格式、安全区、广告位要求 | `$platform-specs` | 必须核验当前官方规则 |
| 把已有策略写成客户可读正式方案 | `$marketing-proposal` | 前置研究/策略，后续任务拆解 |
| 把方案变成任务、排期、依赖和验收 | `$task-decomposition` | 通常作为最后一步 |

## 组合工作流

- 完整全案：`brief-analysis → competitor-analysis + consumer-insight → campaign-planning → marketing-proposal → task-decomposition`
- 社媒运营：`brief-analysis → consumer-insight → social-media-plan → platform-adaptation`
- 新品上市：`brief-analysis → competitor-analysis + consumer-insight → campaign-planning → marketing-proposal`
- 已有方案落地：`marketing-proposal` 或直接 `task-decomposition`
- 单一明确任务：只运行对应主技能，不扩张成全案。

当宿主 Agent 不支持显式调用另一个 Skill 时，读取相应技能目录中的 `SKILL.md`，按其流程执行。

## 执行协议

1. 完整读取用户提供的文本和文件，先列出可用输入。
2. 用一句话说明选择的主技能和原因；不要输出冗长的内部推理。
3. 只有缺失信息会改变战略方向、交付边界或造成高风险时才暂停追问。
4. 需求足够明确、用户要求直接开始或缺口可逆时，登记假设并继续。
5. 涉及近期数据、价格、平台规则、竞品动作、达人、法律或合规时，使用当前可用的官方/一手来源核验，并记录日期。
6. 无法联网或缺少一手数据时，明确标记“未验证”，给出验证方法，绝不补造事实。
7. 先给结论和动作，再给证据、假设、来源与风险。
8. 完成前按 `references/quality-gates.md` 自检。

## 冲突处理

- 用户显式点名某个技能时，优先使用该技能。
- 多个技能都可能触发时，选择输出最贴近用户请求的那个；只有交付确实跨阶段时才组合。
- 本地资料与公开资料冲突时，保留冲突并说明用途，不擅自覆盖用户材料。
- 用户要求的格式、语言、长度和文件类型优先于技能默认格式。
- 当前 Agent 缺少浏览器、文件或执行工具时，完成可完成部分并列出受限项。

## 输出最小结构

```markdown
## 路由判断
- 主技能：
- 组合技能（如有）：
- 关键假设/待确认：

## 交付结果
[按主技能的输出结构完成任务]

## 来源与验证
[仅在使用外部信息或存在未验证事项时提供]
```
