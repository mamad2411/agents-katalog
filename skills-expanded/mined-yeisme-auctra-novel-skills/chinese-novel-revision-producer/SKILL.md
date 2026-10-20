---
name: chinese-novel-revision-producer
description: Use when planning or executing Chinese novel revision passes across structure, continuity, retention, dialogue, style, Auctra review handling, and export readiness.
---

# 中文小说修订制片

组织多轮修订，不把所有问题混在一次“润色”里处理。

## 输入

- 小说草稿、项目圣经、大纲、读者反馈、review 结果、目标发布/导出格式。
- 用户指定的保留内容、修改范围、截止时间和 Auctra 项目上下文。

## 输出

- 修订路线图：结构、连续性、留存、对白、文风、导出前检查。
- 每轮任务清单、阻塞项、接受/拒绝建议和 handoff。
- 最终风险报告和下一步命令建议。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一修订报告、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 blocking、needs_revision、pass、deferred 判定和 Auctra review/export 门禁时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要把章节候选稿按章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和 risk_flags 转成可执行修订任务时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：修订需要重排章节、场景卡、章尾钩子或 continuity delta 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-climax-payoff.md`：修订高潮、伏笔回收和情绪结算时读取。

## 工作流

1. 先分诊问题：结构性、事实性、节奏性、语言性、格式性。
2. 对单章候选稿先读取章节验收门禁，确认章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和 risk_flags。
3. 按高风险到低风险排序，不先润色会被重写的段落。
4. 需要时调用连续性、留存、对白、节奏、文风和章节验收技能。
5. Auctra 项目中使用 `auctra review` 处理候选稿，不自动 accept。
6. 导出前检查未解决阻塞、字数、标题、格式和证据。

## 质量门槛

- 修订路线要说明每一轮的目标、输入、输出和验收。
- 不把“整体润色”当成结构修复。
- 单章修订必须保留章节验收维度，不能只输出泛泛改稿建议。
- 导出前必须标明 blocking、deferred 和用户需确认事项。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。
- 自然度相关修订候选必须携带 finding refs 和 guard refs；不引用 `auctra chapter naturalness` receipt 与 guard 的泛泛改稿不算一轮修订。
- 每轮修订用 `auctra chapter draft diff <chapter-id|candidate-id> --json` 的 resolved/persisted/introduced 输出，配对 before/after receipts 作为 lineage 证据；缺 diff 与 receipt 证据时不声称修复完成。
- 自然度正文修改只经 `auctra chapter naturalness patch-check`/`patch-apply` 进入 successor draft：patch 绑定 candidate/receipt/policy/guard digest，只改 finding 授权 span；不绕过 patch 服务、不改 guard 命中句、不直接写 canonical。
- `auctra chapter naturalness` 的 findings 带 role（narration/dialogue）时，修订候选引用 finding refs 要连同 role 标注，并用 `auctra chapter draft diff` 的 `role_groups` 定位问题层；role 不扩大 patch 授权 span，也不构成绕过 guard 的理由。
- 跨项目复用声音策略走 `auctra voice strategy export --to`（目标已存在即失败，不覆盖）和 `auctra voice strategy import --from`（同名不同 digest 拒绝）；策略资产只提供特征与节奏约束，引用它不豁免上面的 patch/guard 流程。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 检查 `references/chinese-novel-revision-gates.md` 中的结构、连续性、留存、对白、文风和 Auctra 门禁。
- 如涉及 Auctra，说明是否已运行 review/export；未运行时不能声称完成。
- 确认延期项被明确写成 deferred，而不是遗漏。
