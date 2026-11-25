---
name: agent-prompt-guide-glossary
description: |
  当用户需要了解如何让 AI 代理理解设计规范的方法论时使用。触发场景：用户问"什么是 Agent Prompt Guide？"、"如何让 AI 生成符合规范的代码？"、"Quick Reference 和 Component Prompts 是什么？"。不适用于：纯人工阅读的设计规范、非 AI 辅助开发的场景。关键 trigger 信号：Agent Prompt / Quick Reference / Component Prompts / Iteration Guide / AI 友好规范。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 9. Agent Prompt Guide
tags: [ai-prompt-engineering, agent-workflow, design-spec, quality-check]
related_skills: [ai-friendly-spec-framework, ai-iteration-check-principles]
---

# Agent Prompt Guide（AI 代理提示指南）

## R (Reading) — 原文引用

> "Quick Reference: ENCY Charts: 8 分类色板, 7 级顺序色板, 3 种卡片类型 (KPI/Micro/Chart), 4 断点..."
> "Component Prompts: Prompt 1: 生成 KPI 指标卡片组... Prompt 2: 生成多系列柱状图..."
> "Iteration Guide: 1. 颜色第一位 2. 卡片是基本单位 3. Tooltip 不离散..."

## I (Interpretation) — 方法论骨架

**定义**：一套让 AI 代理能够准确理解并执行设计规范的结构化文档，包含 Quick Reference、Component Prompts 和 Iteration Guide 三部分。

**核心组成**：
1. **Quick Reference（快速参考）**：用一句话总结核心规则（压缩版知识）
2. **Component Prompts（组件提示词）**：提供典型场景的完整 prompt 模板
3. **Iteration Guide（迭代指南）**：列出 AI 生成代码后的 10 条检查清单

**核心价值**：
- 降低 AI 误解概率
- 提高生成代码质量
- 减少人工返工次数

**适用场景**：
- 面向 AI 的设计规范编写
- Design System 文档的 AI 友好化改造
- AI 辅助开发的工作流优化

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范第 9 章，作者提供了完整的 AI 友好化示例，包括 Quick Reference、5 个 Component Prompts 和 10 条 Iteration Guide 检查项。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"如何让 AI 理解我的设计规范？"
- 前端工程师说"AI 生成的代码总是不符合规范，怎么办？"

**关键 trigger 词**：Agent Prompt / Quick Reference / Component Prompts / Iteration Guide / AI 友好规范

## E (Execution) — 可执行步骤

**步骤 1**：编写 Quick Reference（一句话总结核心规则）
**步骤 2**：编写 Component Prompts（典型场景的完整 prompt）
**步骤 3**：编写 Iteration Guide（10 条必检项）
**步骤 4**：整合三件套到规范文档
**步骤 5**：测试 AI 生成效果并迭代

## B (Boundary) — 边界与盲点

**不适用场景**：
- 纯人工阅读的设计规范
- 非 AI 辅助开发的场景

**相关 skills**：
- `ai-friendly-spec-framework` — AI 友好的规范编写框架
- `ai-iteration-check-principles` — AI 迭代检查原则
