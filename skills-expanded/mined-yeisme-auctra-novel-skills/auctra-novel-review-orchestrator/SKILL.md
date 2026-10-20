---
name: auctra-novel-review-orchestrator
description: Use when coordinating Auctra-backed Chinese novel review workflows, including pending review queue inspection, chapter candidate comparison, defect triage, reviewer-skill dispatch, and accept/reject/partial decision handoff without bypassing Auctra review gates. Triggers include Auctra 小说审稿, pending review, 候选稿审稿, 对比章节卡, 找小说不足, 缺陷矩阵, and review decision handoff.
---

# Auctra 小说审稿编排器

把 Auctra 项目里的小说候选稿审稿做成可追踪工作流：先确认 review queue 和上下文，再分派最小 reviewer skill，最后输出 defect register、修订 owner 和 Auctra 决策建议。本技能不直接改正文，不自动 accept，不手写 `.auctra/**`。

## 输入

- Auctra 项目路径、pending review item、章节 ID、候选稿、章节卡、项目圣经、读者契约、上一章结尾和下一章承诺。
- Auctra 命令输出：`review --json`、`chapter context --json`、`chapter handoff --audience agent --json`、`text run --json` 或用户粘贴的等价材料。
- 用户目标：找不足、比较版本、决定 accept/reject/partial、安排修订、导出前检查。

## 输出

- 审稿编排报告：范围、上下文完整性、风险等级、置信度、blocking/needs_revision/deferred/pass。
- `defect_register`：按读者影响排序的问题清单，包含证据、最小修复动作、owner skill 和建议 review action。
- 分派计划：需要加载 `chinese-novel-context-pack-builder`、`chinese-novel-draft-comparator`、`chinese-novel-chapter-reviewer`、`chinese-novel-continuity-editor`、`chinese-novel-hook-pacing-editor`、`chinese-novel-reader-retention-editor`、`chinese-novel-dialogue-editor`、`chinese-novel-style-polisher`、`chinese-novel-revision-producer`、`chinese-novel-state-ledger-updater` 或 `auctra-novel-optimization-loop` 的哪一个。
- Auctra handoff：下一步真实命令，以及是否建议 `accept`、`reject` 或 `partial`。

## 参考资料

只在需要对应细节时读取：

- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 handoff、risk_flags、continuity_delta 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要单章目标、冲突升级、信息增量、人物推进、章尾钩子门禁时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 blocking、needs_revision、pass、deferred 判定和导出前门禁时读取。
- `../chinese-novel-orchestrator/references/auctra-novel-workflow-diagrams.md`：需要展示 Auctra review 状态机、缺陷登记到优化闭环的 Mermaid 图时读取。

## 工作流

1. 先确认是否处于 Auctra 项目内。需要状态时建议用户或 agent 运行真实命令，优先使用机器输出：

```bash
auctra review list --status pending --json
auctra chapter context <chapter-id> --json
auctra chapter handoff <chapter-id> --audience agent --json
```

2. 建立审稿基线：review item 类型、候选稿、章节目标、章节卡、读者契约、上一章遗留、下一章承诺、已接受版本和相关 run evidence。缺上下文时先交给 `chinese-novel-context-pack-builder` 列出最小缺口。
3. 如果任务包含“对比”“找不足”“比旧版差在哪里”“候选稿是否兑现章节卡”，先分派 `chinese-novel-draft-comparator`。
4. 对单章交付门禁分派 `chinese-novel-chapter-reviewer`；事实、时间线、知识边界和伏笔债务分派 `chinese-novel-continuity-editor`；留存、钩子和节奏分派 `chinese-novel-hook-pacing-editor` 或 `chinese-novel-reader-retention-editor`。
5. 合并各 reviewer 的结果，按读者影响和 Auctra gate 影响排序。不要把文风偏好升级为 blocking；不要把连续性硬矛盾降级为润色建议。
6. 审稿后需要更新人物状态、伏笔或事件索引时，只交给 `chinese-novel-state-ledger-updater` 产出待确认 delta；不要在候选稿未 accept/partial 前写入长期事实。
7. 用户反馈、同类缺陷复现或需要下一轮修订队列时，交给 `auctra-novel-optimization-loop` 产出 defect_register、revision_queue、next_context_patch 和 rule_proposals。
8. 输出 review action 建议：
   - `accept`：无 blocking，关键维度 pass，deferred 有明确后续偿还点。
   - `partial`：候选稿有可采纳段落，但需要人工 diff 或局部替换。
   - `reject`：章节目标缺失、连续性冲突、人物违背设定、钩子不可偿还或类型契约被破坏。
9. 如果需要保存报告，把它作为普通素材或人工报告保存；不要伪造成 Auctra 已完成的 review decision。

## 报告模板

````markdown
## Auctra 小说审稿编排报告

- project:
- review_item_id:
- chapter_id:
- candidate_source:
- baseline:
- verdict: pass | needs_revision | blocking | deferred
- confidence: high | medium | low

### context_check

| 项 | 状态 | 来源 | 缺口 |
| --- | --- | --- | --- |
| 候选稿 |  |  |  |
| 章节目标 |  |  |  |
| 章节卡 |  |  |  |
| 读者契约 |  |  |  |
| 上下章承诺 |  |  |  |
| 已接受版本 |  |  |  |

### defect_register

| id | severity | dimension | issue | evidence | reader_impact | smallest_fix | owner_skill | review_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### reviewer_dispatch

| owner_skill | reason | input_needed | expected_output |
| --- | --- | --- | --- |

### recommended_auctra_actions

```bash
auctra review list --status pending --json
auctra review reject <review-item-id> --reason "<reason>" --json
```
````

## 边界

- 可建议读取：`auctra review list --status pending --json`、`auctra review list --status pending --agent`、`auctra chapter context <chapter-id> --json`、`auctra chapter handoff <chapter-id> --audience agent --json`。
- 可建议决策：`auctra review accept <review-item-id> --note "<note>" --json`、`auctra review reject <review-item-id> --reason "<reason>" --json`、`auctra review partial <review-item-id> --diff <diff-file> --note "<note>" --json`。
- 不建议不存在的命令，不使用 legacy spelling 写新示例。
- 不把审稿报告、完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入 run evidence、review decision、fixtures 或结构化资产。

## 质量门槛

- 每个问题必须绑定候选稿或项目上下文证据；缺材料时降置信度并列待补命令。
- 每个 blocking 必须有最小修复动作、owner skill 和建议 review action。
- `accept` 建议必须明确说明无 blocking；`partial` 必须说明需要的 diff 范围；`reject` 必须给出可执行 reason。
- 未实际运行 Auctra 命令或未看到命令输出时，只能说“建议运行”，不能声称 queue、decision 或 evidence 已更新。

## 验证

- 检查输出是否覆盖上下文完整性、defect register、reviewer dispatch 和 Auctra action。
- 检查所有命令都是真实 Auctra 命令，且包含 `--json` 或 `--agent`。
- 检查没有要求手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。
