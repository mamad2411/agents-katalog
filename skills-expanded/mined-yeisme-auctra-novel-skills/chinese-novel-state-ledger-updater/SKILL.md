---
name: chinese-novel-state-ledger-updater
description: "Use when extracting post-chapter Chinese novel state updates from a draft, accepted chapter, review result, or revision: character state, protagonist state, foreshadowing movement, event index, chapter summary, style sample, continuity delta, and Auctra handoff notes without mutating structured state directly."
---

# 中文小说状态台账更新器

在章节生成、修订或验收后，提取应该进入项目记忆的事实变化。参考 novel-harness 的“写后归档”机制，但遵守 Auctra 结构化资产边界：本技能只产出台账更新建议和 handoff，不手写 `.auctra/**`。

## 输入

- 章节候选稿或已接受正文、上一轮上下文包、章节大纲、项目圣经、人物档案、伏笔台账。
- 审稿结果、修订说明、Auctra review action、用户确认的保留/拒绝内容。
- 目标状态：只做建议、准备人工确认、准备 Auctra material/handoff、或导出前连续性检查。

## 输出

- `continuity_delta`：新增事实、修改事实、人物状态变化、资源变化、地点变化、知识边界变化。
- `foreshadowing_delta`：新埋伏笔、推进伏笔、回收伏笔、降温伏笔、超期伏笔。
- `event_index_entry`：本章重大事件、影响范围、后续承诺。
- `chapter_summary`：不超过 200 字的事实摘要。
- `style_sample`：句长、对白比例、动作/心理/说明密度、章尾钩子类型。
- `confirmation_needed`：必须由用户或 Auctra review 确认后才能入台账的项目。

## 参考资料

只在任务需要对应细节时读取：

- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 continuity_delta、handoff、risk_flags 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要判断章节目标、信息增量和人物推进是否足够入账时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要区分 accepted、candidate、deferred 和 blocking 事实时读取。
- `../chinese-novel-orchestrator/references/auctra-novel-workflow-diagrams.md`：需要说明写后台账建议、review 状态和长期事实确认边界时读取。

## 工作流

1. 先确认文本状态：candidate、accepted、partial、rejected、user_pasted 或 unknown。未接受候选稿只能产出待确认台账建议。
2. 从文本中抽取事实变化，不记录泛泛判断。例如记录“林远左臂受伤”，不记录“林远状态很糟”。
3. 按角色、地点、资源、关系、知识边界、伏笔和事件分区。
4. 区分显性事实和推断事实；推断事实默认进入 `confirmation_needed`。
5. 对伏笔标记热度：hot、warm、cold、resolved、overdue。只有产生后果、误导、选择或新信息的触碰才算推进。
6. 生成简短章节摘要和风格样本，供下一次 `chinese-novel-context-pack-builder` 使用。
7. 输出 Auctra handoff：建议如何保存为 material、review note 或后续 CLI 能力缺口；不直接写结构化状态。

## 输出模板

```markdown
## 中文小说写后台账更新建议

- project:
- chapter_id:
- source_status: candidate | accepted | partial | rejected | unknown
- confidence: high | medium | low

### continuity_delta

| 类型 | 条目 | 来源证据 | 状态 | 是否需确认 |
| --- | --- | --- | --- | --- |

### character_state_delta

### foreshadowing_delta

| id | 动作 | 热度 | 证据 | 下一步 |
| --- | --- | --- | --- | --- |

### event_index_entry

### chapter_summary

### style_sample

### confirmation_needed

### handoff
```

## Auctra 轻集成

- 候选稿未被 review accept/partial 前，不建议把事实写入长期台账。
- 可建议保存普通人工报告：

```bash
auctra material add --kind note --title "第N章台账更新建议" --from ./ledger-update.md --json
auctra review list --status pending --json
```

- 如果需要真正更新 Auctra 结构化状态，应新增或使用 Auctra CLI / app service；不要手写 `.auctra/**`、SQLite rows、review decision 或 run evidence。

## 边界

- 不做正文润色，不替代审稿，不自动采纳候选稿。
- 不把 rejected 候选稿中的设定写入长期事实。
- 不伪造 Auctra review action、用户确认或已接受版本。

## 验证

- 检查每个 delta 都有文本证据和 source_status。
- 检查待确认项没有被写成 confirmed。
- 检查章节摘要只记录事实和后果，不夹带评价。
