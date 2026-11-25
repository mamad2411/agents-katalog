---
name: auto-build-mode
description: |
  当用户询问"如何平衡自动化与安全性"、"能否一次性实现所有任务"或"如何提高开发效率"时调用此 skill。不适用于：需要频繁人工干预的场景、高风险项目、需求不明确的场景。关键 trigger 信号：auto-build、自动化、一次性实现、效率提升、自主运行。
source_book: Agent Skills Addy Osmani
source_project: addyosmani/agent-skills
source_chapter: Commands section / auto-build description
tags: [automation, efficiency, auto-build, safety]
related_skills: ["spec-driven-development", "test-driven-development"]
---

# SKILL.md - Auto-build Mode（自动构建模式）

## R (Reading) - 原文引用

> "**`/build auto`** generates the plan and implements every task in a single approved pass — you approve the plan once, then it runs autonomously."
> 
> "It removes the human stepping *between* tasks, not the verification: every task is still test-driven and committed individually, and it pauses on failures or risky steps."

## I (Interpretation) - 方法论骨架

**核心思想**：生成计划并一次性实现所有任务，用户只需批准一次计划，然后自主运行。每个任务仍然是测试驱动和单独提交的，遇到失败或风险步骤会暂停。这种模式平衡了自动化与安全性。

**关键要素**：
1. **Single approved pass**: 用户只需批准一次计划
2. **Autonomous execution**: 自主运行，移除任务之间的人工干预
3. **Still test-driven**: 保留测试驱动环节，不跳过验证
4. **Pauses on failures**: 遇到失败或风险步骤会暂停

## A1 (Past Application) - 书中作者用过的案例

Agent Skills 的 `/build auto` 模式是一个实际案例，展示了如何平衡自动化与安全性。Addy Osmani 特别强调："It removes the human stepping *between* tasks, not the verification"，即移除了人工干预但保留了验证环节。

这种设计使得 AI agents 能够高效工作，同时保证代码质量和安全性。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户想提高开发效率，减少人工干预
- 规格说明已明确，计划已生成
- 用户信任 AI 助手的能力，愿意授权自主运行
- 项目风险可控，有完善的测试保护

**与相邻 skill 的区分**：
- 与 `spec-driven-development` 的区别：auto-build-mode 关注**自动化实现**，而 spec-driven-development 关注**需求明确化**。前者是执行阶段，后者是定义阶段。
- 与 `test-driven-development` 的区别：auto-build-mode 是自动化模式（但仍保留 TDD），而 test-driven-development 是手动编写测试和实现。前者更高效，后者更灵活。

## E (Execution) - 可执行步骤

1. **生成计划**
   - 基于规格说明生成详细计划
   - 将工作分解为小且原子的任务
   - 为每个任务定义验收标准
   - 完成标准: 计划覆盖规格说明全部条目，且每个任务都带可判定的验收标准

2. **用户批准计划**
   - 展示完整计划供用户审查
   - 用户批准后开始自主运行
   - 明确告知用户何时会暂停
   - 完成标准: 留存用户明确批准的记录，暂停触发条件已向用户说明

3. **自主执行**
   - 按顺序执行每个任务
   - 每个任务仍然测试驱动和单独提交
   - 遇到失败或风险步骤立即暂停
   - 完成标准: 每个任务先有失败测试再有实现，commit 与任务一一对应

4. **处理暂停**
   - 向用户报告暂停原因
   - 等待用户决策（继续/修改/放弃）
   - 根据用户指令继续执行或调整计划
   - 完成标准: 每次暂停都有原因报告和对应的用户决策结果记录

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 需求不明确，需要频繁调整
- 高风险项目，需要严格人工审查
- 探索性编程，路径不确定
- 用户希望保持完全控制

**作者的盲点**：
- Addy Osmani 假设用户愿意授权自主运行，但实际上某些团队可能有严格的变更管理要求
- agent-skills 缺少对"风险步骤"的具体定义，可能导致误判
- 没有提到如何配置自动化级别（如完全自主 vs 半自主）
