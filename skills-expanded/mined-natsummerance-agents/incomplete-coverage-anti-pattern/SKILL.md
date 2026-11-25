---
name: incomplete-coverage-anti-pattern
description: |
  当需要识别和避免不完整覆盖反模式时使用此 skill。适用于：大变更集审查、多文件 PR 审查等场景。不适用于：小型单一文件修改。关键 trigger 信号：用户提到"遗漏文件"、"偷工减料"、"覆盖不全"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: The Problem with General-Purpose Agents — Incomplete Coverage
tags: [anti-pattern, incomplete-coverage, code-review]
related_skills: [deterministic-engineering-hard-constraints, divide-and-conquer-strategy]
---

# Incomplete Coverage Anti-Pattern（不完整覆盖反模式）

## R (Reading) — 原文引用

> "Incomplete coverage — On larger changesets, agents tend to 'cut corners,' selectively reviewing only some files and missing others."
>
> "The root cause: a purely language-driven architecture lacks hard constraints on the review process."

## I (Interpretation) — 方法论骨架

**核心思想**: 通用 Agent 在大变更集上倾向于"偷工减料"，只审查部分文件而遗漏其他重要文件，根本原因是纯语言驱动架构缺乏硬约束。

**关键特征**:
1. **选择性审查**: Agent 只审查部分文件，遗漏其他重要变更
2. **大变更集触发**: 问题在大型变更集上更明显
3. **根本原因**: 纯语言驱动缺乏对审查过程的硬约束

**解决方案**:
- **Precise file selection**: 精确确定哪些文件需要审查
- **Smart file bundling**: 将相关文件分组为审查单元，确保全覆盖

**与相邻 skill 的区分**: 
- 与 `position-drift-anti-pattern` 的区别：前者关注文件覆盖不全，后者关注位置不准确
- 与 `unstable-quality-anti-pattern` 的区别：前者关注覆盖率，后者关注质量稳定性

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 内部大规模代码审查
- **背景**: 服务数万名开发者，处理数百万代码缺陷
- **问题**: 通用 Agent 在大变更集上"偷工减料"，只审查部分文件
- **应用**: 引入 Precise file selection + Smart file bundling
- **结果**: 审查覆盖率显著提高，无重要文件遗漏

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户抱怨"审查漏掉了重要文件"
- 用户发现"大 PR 中某些文件未被审查"
- 用户遇到"Agent 选择性审查部分文件"
- 用户需要"确保所有重要变更都被审查"

**不应触发的场景**:
- 小型单一文件修改
- 不需要全覆盖的简单任务
- 文件数量很少的场景

**关键 trigger 词**: "遗漏文件"、"偷工减料"、"覆盖不全"、"大变更集"、"选择性审查"

## E (Execution) — 可执行步骤

1. **识别风险**: 检查是否存在大变更集或多文件 PR
   - 完成标准: 给出明确判定结论（是/否属于大变更集场景），附变更文件数量依据
2. **分析原因**: 确认是否是纯语言驱动架构导致的不完整覆盖
   - 完成标准: 归因结论成文，指明覆盖缺陷是否源于缺乏硬约束
3. **应用硬约束**: 引入 Precise file selection 确保所有文件都被考虑
   - 完成标准: 生成文件选择清单，diff 中所有文件均被纳入审查或显式说明排除理由
4. **智能捆绑**: 使用 Smart file bundling 将相关文件分组为审查单元
   - 完成标准: 全部待审文件均归属某个审查单元，无遗漏无重复
5. **验证覆盖**: 检查所有重要文件是否都被审查
   - 完成标准: 覆盖核对表显示重要文件 100% 被审查并留有勾稽记录

**完成标准**: 所有重要文件都被审查，无遗漏

**判停条件**: 连续 5 次大变更集审查无文件遗漏

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 小型单一文件修改
- 不需要全覆盖的简单任务
- 文件数量很少的场景

**作者盲点**:
- **Recall 较低**: 为了精度牺牲召回率，可能仍会漏掉一些真实缺陷
- **性能权衡**: 确保全覆盖可能增加审查时间和 token 消耗
- **过滤策略复杂性**: 需要智能判断哪些文件是"重要"的

**时代局限**:
- 当前架构基于现有 LLM 能力，未来可能需要调整
- 过滤策略依赖于对文件重要性的理解
