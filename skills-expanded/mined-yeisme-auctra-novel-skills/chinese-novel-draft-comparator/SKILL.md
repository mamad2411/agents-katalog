---
name: chinese-novel-draft-comparator
description: Use when comparing Chinese novel drafts, chapter candidates, accepted versions, outlines, chapter cards, reader contracts, genre promises, or Auctra review candidates to identify concrete gaps, regressions, omissions, and revision opportunities without drafting new prose. Triggers include 小说草稿对比, 候选稿对比, 对比章节卡, 对比旧版, 找不足, 找退步, 找缺口, and revision handoff.
---

# 中文小说草稿对比诊断师

比较小说候选稿与基准材料，找出“哪里没有兑现、哪里比旧版退步、哪里和读者承诺或章节卡冲突”。本技能只做诊断和修订交接，不直接重写正文。

## 输入

- 待比较文本：候选稿、旧版、已接受版本、章节草稿、分卷稿或用户粘贴段落。
- 对比基准：章节卡、章节目标、大纲、读者契约、类型承诺、项目圣经、上一章结尾、下一章承诺、Auctra review item 或 run report。
- 用户目标：找不足、判断是否可采纳、定位退步、比较两个候选、生成修订 handoff。

## 输出

- 对比摘要：基准是否完整、候选稿兑现程度、主要退步、主要新增价值。
- 差距矩阵：目标、冲突、信息、人物、连续性、章尾钩子、类型回报、文风和对白。
- `regression_flags`：旧版有但新版丢失、情绪回报变弱、因果断裂、设定冲突、知识边界泄漏、钩子不可偿还。
- 修订 handoff：交给章节验收、连续性、节奏留存、对白、文风或修订制片的最小下一步。

## 参考资料

只在需要对应细节时读取：

- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和类型回报判定时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 blocking、needs_revision、pass、deferred 判定时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 handoff、risk_flags 和 continuity_delta 时读取。

## 工作流

1. 标记比较对象：`candidate`、`baseline`、`previous_version`、`chapter_card`、`reader_contract`、`genre_contract`。缺少关键基准时降置信度，不编造。
2. 先列可验证事实：候选稿实际发生了什么、人物做了什么选择、读者获得了什么信息、结尾承诺了什么。
3. 按维度比较：
   - 章节目标：候选稿是否兑现章节卡里的状态变化。
   - 冲突升级：压力、代价、选择是否比章首更强。
   - 信息增量：新事实、线索、规则、误导是否清晰且可追踪。
   - 人物推进：选择、关系、信念、资源或伤病状态是否变化。
   - 连续性：时间线、知识边界、世界规则、伏笔和道具是否冲突。
   - 章尾钩子：下一章能否通过行动、发现、选择、反转或情绪后果偿还。
   - 类型回报：是否兑现目标读者的爽点、情绪或题材承诺。
   - 表达质量：对白功能、视角稳定、中文语感、AI 味和跳读风险。
4. 如果有旧版，显式输出 regression：新版新增了什么、删掉了什么、哪些删改破坏了因果、情绪或设定。
5. 给每个问题分级：`blocking`、`needs_revision`、`deferred`、`pass`。blocking 必须是会破坏读者理解、正典事实、人物可信度或 Auctra review gate 的问题。
6. 输出最小修复动作和 owner skill，不把所有问题都交给“润色”。

## 对比报告模板

```markdown
## 中文小说草稿对比诊断

- candidate:
- baseline:
- previous_version:
- comparison_goal:
- verdict: pass | needs_revision | blocking | deferred
- confidence: high | medium | low

### baseline_coverage

| 基准 | 是否可用 | 来源 | 对结论的影响 |
| --- | --- | --- | --- |
| 章节目标 |  |  |  |
| 章节卡 |  |  |  |
| 读者契约 |  |  |  |
| 旧版/已接受版本 |  |  |  |
| 项目圣经/连续性台账 |  |  |  |

### comparison_matrix

| 维度 | 基准要求 | 候选稿表现 | 差距/退步 | 证据 | 等级 | 最小修复动作 | owner_skill |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 章节目标 |  |  |  |  |  |  |  |
| 冲突升级 |  |  |  |  |  |  |  |
| 信息增量 |  |  |  |  |  |  |  |
| 人物推进 |  |  |  |  |  |  |  |
| 连续性 |  |  |  |  |  |  |  |
| 章尾钩子 |  |  |  |  |  |  |  |
| 类型回报 |  |  |  |  |  |  |  |
| 对白/文风 |  |  |  |  |  |  |  |

### regression_flags

- lost_from_previous:
- weaker_than_baseline:
- contradicted_canon:
- deferred_risks:

### handoff

- next_owner:
- smallest_next_action:
- recommended_review_action: accept | reject | partial | no_auctra_action
```

## Auctra 轻集成

- 在 Auctra 项目内，本技能通常由 `auctra-novel-review-orchestrator` 调用。
- 可建议读取上下文：

```bash
auctra review list --status pending --json
auctra chapter context <chapter-id> --json
auctra chapter handoff <chapter-id> --audience agent --json
```

- 不直接执行 `accept`、`reject` 或 `partial`；只给建议和 reason。最终决策必须由 Auctra review 命令或作者执行。

## 边界

- 只做比较、诊断、分级和修订 handoff，不直接改写小说正文，不替作者生成新章节。
- 不把缺少基准材料时的猜测写成确定结论；缺章节卡、旧版、读者契约或项目圣经时必须降低置信度。
- 不手写 `.auctra/**`、SQLite rows、review decision、run evidence 或结构化资产；需要持久化时建议使用 Auctra 命令或保存为普通人工报告。
- 不输出完整思维链、原始提示词、供应商载荷、隐藏系统提示、私密工具参数、真实凭据或未脱敏证据。

## 质量门槛

- 每条差距必须有基准和候选稿证据，不能只写“张力不足”。
- 不把新增内容本身当优点；新增内容必须服务章节目标、人物推进、信息增量或类型回报。
- 旧版对比必须同时列“新版改善”和“新版退步”，避免只找缺点。
- 缺少章节卡、读者契约或旧版时，明确标为 low/medium confidence。
- 不输出完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数。

## 验证

- 检查报告是否包含 baseline coverage、comparison matrix、regression flags 和 handoff。
- 检查每个 blocking 是否有 owner skill 和最小修复动作。
- 检查是否错误建议手写 `.auctra/**`、SQLite rows、review decision 或 run evidence。
