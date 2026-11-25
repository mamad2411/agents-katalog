---
name: okr-review-score
description: Score DoWithOKR outcomes through upper-level reviews, evidence-based KR scoring, role results, and final GM result.
---

# OKR Review Score

## 前置条件

- 需要：已生成的状态看板和角色树（`.okr/status.md` 和 `.okr/active.md` 存在）。
- 缺失处理：
  - 缺少状态看板 → 提示先运行 `okr-planner`。
  - 缺少角色树 → 提示先运行 `okr-role-splitter`。

## 前置读取

- 读取 `.okr/status.md`。
  - 文件不存在 → 提示用户先运行 `okr-planner` 生成看板。
- 读取 `.okr/active.md`，提取角色树和上下级关系（确定谁给谁评分）。
- 读取 `.okr/evidence/` 目录下所有证据文件，汇总每个 KR 的证据清单。
- 可选：读取 `.okr/reviews/` 目录，检查是否已有历史评分记录。
- 可选：读取 `.okr/wisdom/` 目录下角色 wisdom 文件，作为评分时的参考上下文（如历史评分趋势、已知的角色能力水平）。

## 执行规则

- 用户可主动触发评分复盘。
- 评分采用上级给直接下级打分。
- 评分必须绑定证据和差距说明。
- 每个角色的 Objective 得分默认取 KR 平均分。
- GM 最终 R 由产品线 R、技术线 R、证据质量和甲方验收结论共同决定。

## 执行步骤

1. 读取角色树，建立评分关系：
   - GM 评分 PD 产品总监和 ArchD 技术总监。
   - PD 产品总监评分 PM 产品经理、UI 设计师、TW 文档专家/DX。
   - ArchD 技术总监评分 BE 后端、FE 前端、QA 测试、DevOps 发布、SEC 安全等技术角色。
2. 读取每个角色 KR 的状态和证据：
   - 从 `.okr/status.md` 获取状态和进展。
   - 从 `.okr/evidence/{KR-ID}.md` 获取证据清单。
   - 验证证据文件格式是否符合 `../../references/evidence-spec.md` 规范。
3. 验证证据有效性（参考 `../../references/evidence-spec.md` 验证规则）：
   - 交叉比对证据与 KR 验收标准，判断证据是否充分覆盖验收要求。
   - 检查证据路径是否指向实际存在的文件（可疑证据降低可信度）。
   - 检查证据类型与角色职责是否匹配（如 BE 后端开发工程师应有代码和测试证据）。
   - 标记证据不足的 KR：状态为"已完成"但无证据 → 标记为"待验证"。
   - 标记证据可疑的 KR：证据路径不存在或类型不匹配 → 提示需要补充。
4. 为每个 KR 评分：
   - 0.0：无进展，无证据。
   - 0.3：有探索但未形成有效交付。
   - 0.7：基本达成且证据可信。
   - 1.0：完全达成并超过验收预期。
   - 每个评分必须附带证据引用和差距说明。
5. 汇总角色 Objective 得分：
   - 每个角色 O 得分 = 其 KR 平均分。
6. 汇总线级 R：
   - 产品线 R = PD 产品总监 O 得分（含 PM、UI、TW 下级平均）。
   - 技术线 R = ArchD 技术总监 O 得分（含 BE、FE、QA、DevOps、SEC 下级平均）。
7. 计算 GM 最终 R：
   - GM 最终 R = 产品线 R × 40% + 技术线 R × 60%。
8. 生成复盘结论和下一轮建议。
9. 生成价值总结（参考 `../../references/score-review-template.md` 的价值总结区块）：
   - 回答：本次交付创造了什么业务/技术/用户价值？
   - 回答：团队的哪些能力得到了提升？（量化对比）
   - 回答：有哪些可复用的洞察？（有效实践 + 陷阱警示 + 流程改进）
   - 回答：下次应该在哪里投入更多？
10. 写入评分记录（含价值总结）。
11. 经验提炼（参考 `../../references/wisdom-spec.md`）：
    - 分析本次评分结果：哪些 KR 得分高/低？原因是什么？
    - 提取可复用的经验：什么做法有效？什么是陷阱？
    - 为每个参与角色更新 wisdom 文件：
      - 追加反思记录（Cycle N 标题 + 教训 + 改进 + 效果）。
      - 更新专业知识（如果发现新的有效实践）。
      - 更新项目上下文（如果项目信息有变化）。
    - 更新 `.okr/wisdom/team.md`：提炼团队级别的协作经验。
    - wisdom 文件不存在时自动创建（含 frontmatter 和空区块）。

## 输出格式

使用 `../../references/score-review-template.md`。

必须包含：

- OKR 评分复盘
- 上级评分
- 角色 R
- GM 最终 R
- 价值总结（交付价值、能力提升、关键洞察、投入建议）
- 下一轮建议

## 异常处理

- 某个 KR 无证据但状态为"已完成"：将评分标记为"待验证"，建议补充证据后重新评分。
- 角色树中某个角色无任何 KR 执行记录：评分为 0.0，说明"未参与本轮交付"。
- 用户对评分有异议：允许手动调整分数，但必须附带调整理由。

## 周期归档与清理

评分复盘完成后，执行周期归档，为下一轮 OKR 腾出干净的工作区。

### 归档步骤

1. 创建归档目录 `.okr/archive/<YYYY-MM-DD>-cycle/`（日期为当天）。
   - 同一天多次归档时追加序号：`<YYYY-MM-DD>-cycle-2/`。
2. 将以下文件移入归档目录：
   - `active.md` → `archive/<date>-cycle/active.md`
   - `status.md` → `archive/<date>-cycle/status.md`
   - `evidence/` 目录整体 → `archive/<date>-cycle/evidence/`
   - `reviews/` 目录整体 → `archive/<date>-cycle/reviews/`
3. 为归档目录中的 `active.md` 和 `status.md` 追加归档 frontmatter：
   - `archived_at: <YYYY-MM-DD>`
   - `archived_reason: cycle-complete`
4. 生成归档摘要文件 `archive/<date>-cycle/summary.md`：
   - GM 最终 R 分数
   - 甲方需求摘要（一句话）
   - KR 完成统计（已完成/总数）
   - 参与角色列表

### 清理步骤

归档完成后，清空工作区状态文件：

1. 删除 `.okr/active.md`。
2. 删除 `.okr/status.md`。
3. 删除 `.okr/evidence/` 目录（已归档）。
4. 删除 `.okr/reviews/` 目录（已归档）。
5. **保留** `.okr/wisdom/` — 角色经验跨周期积累，不清理。
6. **保留** `.okr/archive/` — 历史归档，不清理。

### 用户确认

- 归档和清理前必须向用户展示归档摘要并请求确认。
- 用户拒绝归档时，跳过归档和清理步骤，仅保留评分结果。

## 产出写入

- 创建 `.okr/reviews/<今天日期>.md`：
  - 写入 frontmatter：`act: <当前交付幕>`、`last_updated`。
  - 写入上级评分表、汇总和结论。
- 更新 `.okr/status.md`：
  - 将已评分 KR 的进展字段更新为评分分数。
  - 更新 frontmatter：`last_updated`、`updated_by: okr-review-score`。
- 创建或更新 `.okr/wisdom/{role}.md`（参考 `../../references/wisdom-spec.md`）：
  - 为每个参与角色写入经验提炼结果。
  - 更新 frontmatter 的 `updated` 和 `cycles_completed`。
- 创建或更新 `.okr/wisdom/team.md`：
  - 写入团队级别的协作经验。
- 执行周期归档与清理（见上方"周期归档与清理"章节）。
