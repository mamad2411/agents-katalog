---
name: unstable-quality-anti-pattern
description: |
  当需要识别和避免质量不稳定反模式时使用此 skill。适用于：代码审查质量波动、提示微调导致结果变化等场景。不适用于：质量稳定的场景。关键 trigger 信号：用户提到"质量波动"、"提示微调"、"难以调试"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: The Problem with General-Purpose Agents — Unstable Quality
tags: [anti-pattern, unstable-quality, debugging]
related_skills: [deterministic-engineering-hard-constraints, template-engine-over-language-driven]
---

# Unstable Quality Anti-Pattern（质量不稳定反模式）

## R (Reading) — 原文引用

> "Unstable quality — Natural-language-driven Skills are hard to debug, and review quality fluctuates significantly with minor prompt variations."
>
> "The root cause: a purely language-driven architecture lacks hard constraints on the review process."

## I (Interpretation) — 方法论骨架

**核心思想**: 通用 Agent 的审查质量随提示微小变化而显著波动，自然语言驱动的 Skills 难以调试，根本原因是纯语言驱动架构缺乏稳定性保障。

**关键特征**:
1. **质量波动**: 审查质量随提示微小变化而显著波动
2. **难以调试**: 自然语言驱动的 Skills 难以定位问题根源
3. **根本原因**: 纯语言驱动缺乏硬约束和稳定性保障

**解决方案**:
- **Fine-grained rule matching**: 基于模板引擎的细粒度规则匹配，提高稳定性
- **Scenario-tuned prompts**: 深度优化的场景化提示模板，减少波动

**与相邻 skill 的区分**: 
- 与 `incomplete-coverage-anti-pattern` 的区别：前者关注质量稳定性，后者关注文件覆盖不全
- 与 `position-drift-anti-pattern` 的区别：前者关注质量波动，后者关注位置精度

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 内部审查质量优化
- **背景**: 通用 Agent 的审查质量随提示微小变化而波动
- **问题**: 难以调试和优化，质量不稳定影响开发者信任
- **应用**: 引入 Fine-grained rule matching + Scenario-tuned prompts
- **结果**: 审查质量显著提高且稳定，不再随提示微小变化而波动

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户抱怨"审查质量随提示变化而波动"
- 用户发现"难以调试和优化自然语言驱动的 Skills"
- 用户遇到"质量不稳定影响开发者信任"
- 用户需要"确保审查质量稳定可预测"

**不应触发的场景**:
- 质量已经稳定的场景
- 不需要调试和优化的简单任务
- 提示本身已经很优化的场景

**关键 trigger 词**: "质量波动"、"提示微调"、"难以调试"、"不稳定"、"自然语言驱动"

## E (Execution) — 可执行步骤

1. **识别风险**: 检查是否存在质量波动问题
   - 完成标准: 用同一提示多次运行并留存结果差异记录，给出有/无波动的结论
2. **分析原因**: 确认是否是纯语言驱动架构导致的质量不稳定
   - 完成标准: 归因结论成文，指明波动是否源于缺乏硬约束与稳定机制
3. **应用细粒度规则匹配**: 引入 Fine-grained rule matching，基于模板引擎提高稳定性
   - 完成标准: 规则匹配模块接入审查流程，关键步骤不再依赖自由文本判断
4. **优化提示模板**: 使用 Scenario-tuned prompts，深度优化场景化提示
   - 完成标准: 各审查场景提示模板定稿并通过试运行
5. **验证效果**: 测试审查质量是否稳定，不再随提示微小变化而波动
   - 完成标准: 提示微扰实验显示多次运行结果保持一致，波动消除

**完成标准**: 审查质量稳定，连续多次审查结果一致，不再随提示微小变化而波动

**判停条件**: 连续 10 次审查质量无显著波动，开发者信任度显著提高

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 质量已经稳定的场景
- 不需要调试和优化的简单任务
- 提示本身已经很优化的场景

**作者盲点**:
- **模板维护成本**: 需要持续维护和更新规则模板和提示模板
- **灵活性牺牲**: 细粒度规则匹配可能限制某些边缘场景的处理能力
- **优化复杂度**: 深度优化提示模板需要大量实验和数据分析

**时代局限**:
- 当前架构基于现有 LLM 能力，未来可能需要调整
- 提示优化依赖于对模型行为的深入理解
