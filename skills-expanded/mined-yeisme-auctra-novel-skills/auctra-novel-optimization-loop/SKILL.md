---
name: auctra-novel-optimization-loop
description: "Use when turning Auctra-backed Chinese novel review results, chapter defects, user feedback, repeated issues, context packs, ledger deltas, and accepted/rejected candidates into a revision queue, rule proposal, next-run optimization handoff, and Auctra-safe evidence plan."
---

# Auctra 小说优化闭环

把 Auctra 小说工作流从“一次生成候选稿”升级为“生成 -> 审稿 -> 反馈归因 -> 修订队列 -> 规则提案 -> 下一轮上下文优化”。参考 novel-harness 的反馈追踪流程，但所有结构化状态变更都必须通过 Auctra CLI 或应用服务完成。

## 输入

- Auctra 项目路径、review queue、候选稿、审稿报告、章节验收表、用户反馈、被拒绝或 partial 的原因。
- `chinese-novel-context-pack-builder` 的上下文包、`chinese-novel-state-ledger-updater` 的台账建议、`auctra-novel-review-orchestrator` 的 defect register。
- 历史同类问题：重复 AI 味、伏笔断裂、人物状态漂移、章尾钩子弱、信息空转、对话解释化、目标字数和情节点不匹配。

## 输出

- `optimization_report`：本轮问题归因、读者影响、Auctra gate 影响和下一轮目标。
- `revision_queue`：按 blocking、needs_revision、style、continuity、deferred 排序的修订任务。
- `rule_proposals`：重复问题达到阈值时建议追加到对应 skill/reference 的规则提案。
- `next_context_patch`：下一轮上下文包必须加入或收紧的事实、禁写项、风格规则、伏笔提醒。
- `auctra_handoff`：真实命令建议和不能手写的结构化资产边界。

## 参考资料

只在需要对应细节时读取：

- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要修订门禁、blocking / deferred 判定时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要把章节缺陷映射到章节验收维度时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 handoff、risk_flags、continuity_delta 时读取。
- `../chinese-novel-orchestrator/references/auctra-novel-workflow-diagrams.md`：需要用 Mermaid 图展示 review 状态、反馈追踪、规则提案或 Auctra 结构化资产边界时读取。

## 工作流

1. 收集本轮证据：review item、候选稿、审稿报告、用户反馈、上下文包、台账建议。缺少 Auctra 输出时只列建议命令，不声称已读取 queue。
2. 将问题归因到维度：context_missing、planning_gap、draft_execution、continuity_drift、style_ai_taste、hook_pacing、dialogue_exposition、review_gate_gap、user_preference.
3. 建立缺陷登记：每条缺陷必须有证据、读者影响、最小修复动作、owner skill 和建议 review action。
4. 统计重复问题：同类问题未满 3 次只记录；达到 3 次时输出 `rule_proposals`，等待用户确认后才建议更新 skill/reference。
5. 生成修订队列：blocking 先修，continuity 早于 style，读者承诺和章尾钩子早于局部润色。
6. 生成下一轮上下文优化：哪些事实必须进入 context pack，哪些禁写项必须进入 hard_constraints，哪些伏笔要升温或暂缓。
7. 给出 Auctra-safe handoff：保存普通报告、运行 review 命令、准备 partial diff；不自动 accept，不手写结构化状态。

## 报告模板

```markdown
## Auctra 小说优化闭环报告

- project:
- chapter_id:
- review_item_id:
- source_status:
- verdict: continue | revise | reject | wait_for_context

### defect_register

| id | severity | category | issue | evidence | reader_impact | smallest_fix | owner_skill | review_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### revision_queue

| priority | task | owner_skill | input_needed | done_when |
| --- | --- | --- | --- | --- |

### repeated_issue_tracking

| issue_type | count | latest_evidence | threshold | action |
| --- | --- | --- | --- | --- |

### rule_proposals

| target | proposal | reason | requires_user_confirmation |
| --- | --- | --- | --- |

### next_context_patch

### auctra_handoff
```

## Auctra 命令建议

按实际项目能力选择最窄命令，优先机器输出：

```bash
auctra review list --status pending --json
auctra review reject <review-item-id> --reason "<reason>" --json
auctra review partial <review-item-id> --diff <diff-file> --note "<note>" --json
auctra material add --kind note --title "第N章优化闭环报告" --from ./optimization-report.md --json
```

如果 Auctra 缺少“反馈记录”“规则提案”“上下文补丁”这类命令，本技能应把它列为产品缺口，建议在 `cli/auctra` 中新增 CLI/app service，而不是让 agent 手写 `.auctra/**`。

## 边界

- 不自动修改 skill 规则；重复问题达到阈值也必须等待用户确认。
- 不自动 accept/reject/partial Auctra review；只给建议命令。
- 不把用户反馈伪造成平台数据、真实读者反馈或 Auctra evidence。
- 不写完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数。

## 验证

- 检查每个缺陷都有证据、owner skill、最小修复动作和 review action。
- 检查 rule proposal 是否只在同类问题达到阈值时提出，并标记需要用户确认。
- 检查所有命令都是真实 Auctra 命令，且没有要求手写 `.auctra/**`。
