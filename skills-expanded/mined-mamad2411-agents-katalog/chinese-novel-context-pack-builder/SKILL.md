---
name: chinese-novel-context-pack-builder
description: "Use when preparing a Chinese novel planning, chapter-writing, continuation, revision, or review task by building a minimal context pack from project bible, chapter plan, character state, foreshadowing ledger, chapter summaries, style reference, knowledge boundaries, and Auctra handoff data."
---

# 中文小说上下文包构建器

在写章、续写、规划或审稿前，把“这次不知道就会写错”的信息打包给下游技能。参考 novel-harness 的上下文 Agent 思路，但适配 Yeisme / Auctra：技能负责整理 author-facing context，结构化项目状态仍由 Auctra CLI 或应用服务维护。

## 输入

- 项目圣经、读者契约、章节大纲、场景卡、上一章结尾、下一章承诺。
- 人物状态、角色知识边界、活跃伏笔、事件索引、最近章节摘要、风格参考。
- Auctra 命令输出或等价材料：`chapter context --json`、`chapter handoff --audience agent --json`、`review list --json`、`material list --json`。
- 目标下游：规划、写章、续写、审稿、修订或导出前检查。

## 输出

- 最小上下文包：当前任务、主角状态、出场角色、活跃伏笔、风格参考、硬约束、最小记忆包、知识包/素材缺口。
- 来源表：每条关键事实来自用户指定、已接受章节、项目圣经、Auctra handoff、review 结果或暂定规划。
- 下游 handoff：交给 `chinese-novel-outline-architect`、`chinese-novel-chapter-writer`、`chinese-novel-chapter-reviewer`、`chinese-novel-continuity-editor`、`chinese-novel-revision-producer` 或 `auctra-novel-review-orchestrator` 的输入。
- Auctra 下一步命令建议，只建议真实命令，不声称已执行。

## 参考资料

只在任务需要对应细节时读取：

- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 handoff、continuity_delta、risk_flags 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要把章节目标转成场景卡和写作输入时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review / revision / export gate 语义时读取。
- `../chinese-novel-orchestrator/references/auctra-novel-workflow-diagrams.md`：需要说明写前上下文包如何进入 Auctra 写章/review 流程时读取。

## 工作流

1. 确认目标下游和任务粒度：规划方向、章纲、正文候选、续写、审稿、修订或导出前检查。
2. 收集最小事实，不导出全量百科；只保留会影响本轮角色行为、冲突、信息边界、伏笔偿还或读者承诺的内容。
3. 标记每条事实的来源和确定性：confirmed、accepted、planned、candidate、missing。
4. 筛选活跃伏笔：本章会触碰、误导、回收、压住或超期的伏笔优先。
5. 提取风格参考：最近 3-5 章的句长、对白比例、叙述密度、章尾钩子和平台口味；不要让风格参考覆盖当前章节目标。
6. 输出最小上下文包，并列出缺口。如果缺口影响写作或审稿，先建议补材料或运行 Auctra 命令。
7. 将上下文包交给最小 owner skill，不让写作 skill 自己重新搜索全部资料。

## 上下文包模板

```markdown
## 中文小说上下文包

- project:
- target_skill:
- phase: plan | write | review | revise | export_check
- chapter_id:
- confidence: high | medium | low

### current_task

### protagonist_state

### active_characters

| 角色 | 位置/状态 | 与主角关系 | 本轮知识边界 | 行为约束 |
| --- | --- | --- | --- | --- |

### active_foreshadowing

| id | 埋下位置 | 当前热度 | 本轮用途 | 超期风险 |
| --- | --- | --- | --- | --- |

### recent_summary

### style_reference

### hard_constraints

### minimal_memory_pack

### missing_inputs

### handoff
```

## Auctra 轻集成

- 需要项目状态时，优先建议：

```bash
auctra chapter context <chapter-id> --json
auctra chapter handoff <chapter-id> --audience agent --json
auctra review list --status pending --json
```

- 上下文包可以作为普通 material 或 handoff 文档保存，但不能手写 `.auctra/**`、SQLite rows、run evidence 或 review decision。
- 如果 Auctra 尚无对应命令，只输出“建议补充命令能力”的产品缺口，不伪造命令结果。

## 边界

- 不写正文、不规划剧情、不做审稿结论；只做上下文收集和下游交接。
- 不把未确认资料升级为项目事实。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入上下文包。

## 验证

- 检查上下文包是否足够下游执行，但没有塞入无关百科。
- 检查每条硬约束和关键事实都有来源或标记为 missing。
- 检查 handoff 指向最小 owner skill，并包含下一步真实 Auctra 命令或明确的材料缺口。
