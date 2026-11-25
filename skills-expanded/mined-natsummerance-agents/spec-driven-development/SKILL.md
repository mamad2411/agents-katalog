---
name: spec-driven-development
description: |
  当用户询问"我应该先写什么"、"如何明确需求"或"如何避免盲目编码"时调用此 skill。不适用于：纯信息查询、已有明确规格说明的场景、快速原型验证。关键 trigger 信号：规格说明、spec、需求明确化、先写什么、避免盲目编码。
source_book: Agent Skills Addy Osmani
source_project: addyosmani/agent-skills
source_chapter: Commands table / DEFINE phase
tags: [spec-driven, requirements, define-before-code]
related_skills: ["test-driven-development", "auto-build-mode"]
---

# SKILL.md - Spec-Driven Development（规格说明驱动开发）

## R (Reading) - 原文引用

> "DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP"
> 
> "/spec | Define what to build | Spec before code"

## I (Interpretation) - 方法论骨架

**核心思想**：在写代码之前先定义规格说明（Spec before code）。这种"规格先行"的方法确保开发者明确知道要构建什么，避免盲目编码和需求蔓延。

**关键要素**：
1. **DEFINE 阶段**: 明确要构建什么，细化需求
2. **Spec before code**: 先写规格说明再写代码
3. **需求明确化**: 通过问题细化需求，分块展示设计供验证

## A1 (Past Application) - 书中作者用过的案例

Agent Skills 的 6 阶段开发生命周期中，DEFINE 是第一个阶段，对应 `/spec` 命令。Addy Osmani 强调"Spec before code"作为核心原则，确保 AI 编码助手在写代码之前先明确需求。

这种设计使得 AI agents 能够遵循标准化的工作流程，避免盲目编码和需求理解偏差。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户不确定应该先写什么
- 用户需求模糊，需要明确化
- 用户想避免盲目编码和需求蔓延
- 用户想建立系统化的需求定义流程

**与相邻 skill 的区分**：
- 与 `test-driven-development` 的区别：spec-driven-development 关注**需求明确化**（写代码前），而 test-driven-development 关注**代码正确性验证**（写代码时）。两者互补：先明确需求，再测试驱动实现。
- 与 `auto-build-mode` 的区别：spec-driven-development 是手动定义规格，而 auto-build-mode 是自动生成计划并实现。前者更灵活，后者更高效。

## E (Execution) - 可执行步骤

1. **明确要构建什么**
   - 询问用户的核心需求和目标
   - 识别关键功能和边界条件
   - 明确验收标准
   - 完成标准: 核心需求、边界条件、验收标准三项全部记录且无缺项

2. **编写规格说明**
   - 描述功能需求
   - 定义接口和数据结构
   - 列出约束条件和非功能性需求
   - 完成标准: 规格说明文档含功能需求、接口/数据结构、约束与非功能需求四部分

3. **验证规格说明**
   - 与用户确认规格是否准确
   - 检查是否有遗漏或歧义
   - 确保规格可测试
   - 完成标准: 用户明确确认规格准确，每条需求均可映射为至少一个测试用例

4. **进入下一阶段**
   - 规格确认后进入 PLAN 阶段
   - 将规格分解为小且原子的任务
   - 开始测试驱动实现
   - 完成标准: 任务分解完成且每个任务可追溯到规格条目，首个失败测试就绪

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯信息查询（如"这个 API 怎么用"）
- 已有明确规格说明的场景
- 快速原型验证（不需要完整规格）
- 探索性编程（需求可能频繁变化）

**作者的盲点**：
- Addy Osmani 假设所有项目都需要完整规格说明，但实际上某些场景（如原型验证）可能不需要
- agent-skills 缺少对规格说明模板或最佳实践的具体指导
- 没有提到如何迭代更新规格说明以应对需求变化
