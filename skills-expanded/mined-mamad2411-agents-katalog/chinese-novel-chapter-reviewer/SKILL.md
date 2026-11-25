---
name: chinese-novel-chapter-reviewer
description: Use when reviewing a Chinese novel chapter candidate against chapter goal, conflict escalation, information gain, character movement, continuity delta, chapter-end hook, and risk flags before accepting it as publishable or handing it to revision.
---

# 中文小说章节验收编辑

把章节候选稿变成可验收对象，而不是只说“不错”“再润色”。本技能负责检查单章是否完成本章目标、是否推进冲突和人物、是否释放足够信息、是否留下可偿还钩子，并把问题转成可执行的 revision handoff。

## 输入

- 章节候选稿、章节大纲、场景卡、项目圣经、上一章结尾和下一章承诺。
- 本章目标、目标字数、类型契约、读者承诺、必须保留/禁止改动的情节。
- 连续性台账、伏笔台账、人物状态、知识边界、用户或 Auctra review 反馈。

## 输出

- 章节验收表：`pass` / `needs_revision` / `blocking` / `deferred`。
- 逐项判定：章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子、字数和类型回报。
- `risk_flags`：目标未完成、冲突无升级、信息空转、人物原地踏步、连续性冲突、钩子不可偿还、剧透越界、AI 味、Auctra 状态待确认。
- 修订 handoff：交给 `chinese-novel-revision-producer`、`chinese-novel-continuity-editor`、`chinese-novel-hook-pacing-editor`、`chinese-novel-dialogue-editor` 或 `chinese-novel-style-polisher` 的下一步。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一验收报告、handoff、continuity_delta 和 risk_flags 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要章节目标、冲突升级、信息增量、人物推进、连续性 delta 和章尾钩子的验收矩阵时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要把验收结果归入 blocking、needs_revision、pass 或 deferred 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要核对章节模板、场景卡字段或章尾钩子是否完整时读取。

## 工作流

1. 对齐验收基线：先确认本章目标、读者承诺、类型回报、上一章遗留问题和下一章承诺。
2. 如果任务重点是比较候选稿与章节卡、旧版、已接受版本或读者契约，先交给 `chinese-novel-draft-comparator` 产出差距矩阵，再基于矩阵做章节验收。
3. 逐项检查章节结构：开场压力、场景转折、冲突升级、信息增量、人物状态变化、情绪回报和章尾钩子。
4. 检查连续性 delta：新增事实、人物状态、伏笔、知识边界、资源变化和未回收问题是否可落台账。
5. 给每项标记 `pass`、`needs_revision`、`blocking` 或 `deferred`，并说明影响用户阅读的具体后果。
6. 输出修订 handoff：结构问题交 revision producer，事实冲突交 continuity，留存和钩子交 hook-pacing，对白交 dialogue，文风交 style。

## 质量门槛

- 验收必须引用章节里的具体段落、场景或台账项，不用泛泛评价替代证据。
- 每个 `blocking` 都必须给出阻塞原因和最小修复动作；每个 `deferred` 都必须说明为什么可延期。
- 不把文风喜好升级成结构阻塞，也不把连续性矛盾降级为润色建议。
- 章尾钩子必须可偿还：下一章能通过行动、发现、选择、反转或情绪后果接住。
- 未运行 Auctra review 时，不声称章节已通过项目审稿。

## Auctra 轻集成

- 普通单章验收可直接输出 Markdown 验收表。
- Auctra 项目内可建议先运行 `auctra review` 生成候选稿审阅结果，再把本技能验收意见作为人工复核或 revision handoff。
- 不自动 accept review，不覆盖正文，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 边界

- 不直接重写整章；需要重写时交给 `chinese-novel-revision-producer` 或 `chinese-novel-chapter-writer`。
- 不伪造读者反馈、平台数据、Auctra review 结果或人工验收记录。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入验收报告。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 检查验收表是否覆盖章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和 risk_flags。
- 检查每个问题是否有 owner skill 和最小修复动作。
- 有章节文件时可运行 `python3 novel-writing/chinese-novel-orchestrator/scripts/check_chinese_chapter_wordcount.py <chapter.md> 3000`。
- 未满足 blocking 项时，不能把章节候选稿说成最终可发布稿。
