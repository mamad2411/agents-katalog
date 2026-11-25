---
name: subagent-driven-development
description: |
  当用户需要让编码 Agent 自主处理多个工程任务、并行工作数小时而不偏离计划时调用此 skill。适用于大型功能开发、多任务并行、需要长时间自主工作的场景。不适用于：单一小任务、一次性脚本、紧急 hotfix。关键 trigger 信号："subagent"、"parallel agents"、"autonomous work"、"two-stage review"、"spec compliance"、"code quality review"。
source_book: 《Superpowers》 obra
source_project: obra/superpowers
source_chapter: How it works / The Basic Workflow / What's Inside
tags: [framework, subagent, parallel, review]
related_skills: ["mandatory-workflow"]
---

# Subagent-driven-Development (SDD)

## R (Reading) - 原文引用

> "Next up, once you say 'go', it launches a *subagent-driven-development* process, having agents work through each engineering task, inspecting and reviewing their work, and continuing forward. It's not uncommon for your agent to work autonomously for a couple hours at a time without deviating from the plan you put together."

> "dispatches fresh subagent per task with two-stage review (spec compliance, then code quality)"

## I (Interpretation) - 方法论骨架

Subagent-driven-Development (SDD) 是一种让编码 Agent 自主处理多个工程任务的方法论。其核心是：

1. **分派新鲜子 Agent**：每个工程任务由一个新鲜的子 Agent 处理，避免上下文污染
2. **两阶段审查**：先检查规范合规性（是否按计划实现），再检查代码质量（是否符合最佳实践）
3. **自主工作**：Agent 可以连续工作数小时而不偏离计划，减少人工干预

这种方法的优势在于：通过隔离的子 Agent 保证任务独立性，通过两阶段审查保证质量，通过明确的计划保证方向不偏离。

## A1 (Past Application) - 书中作者用过的案例

在 Superpowers 的基本工作流中，第 4 步明确说明：一旦用户说"go"，系统就会启动 SDD 流程，让 Agent 逐个处理工程任务。作者 Jesse Vincent 指出，这种模式下 Agent 可以自主工作数小时而不偏离计划，这是传统单次对话式开发无法实现的。

## A2 (Future Trigger) - 何时调用

**调用时机**：
- 用户需要处理多个独立的工程任务（如同时修复 5 个 bug、实现 3 个功能）
- 用户希望 Agent 能自主工作数小时而不需要频繁干预
- 用户担心 Agent 会偏离计划或产生上下文污染

**不调用时机**：
- 单一小任务（不需要分派子 Agent）
- 一次性脚本（不需要严格审查）
- 紧急 hotfix（没有时间走完整流程）

**与相邻 skill 的区分**：
- 与 `executing-plans` 的区别：SDD 强调每个任务由独立子 Agent 处理 + 两阶段审查；executing-plans 是批量执行，可能共享上下文
- 与 `dispatching-parallel-agents` 的关系：SDD 是 dispatching-parallel-agents 的具体实现模式，包含两阶段审查机制

**关键 trigger 信号**：用户提到"subagent"、"parallel agents"、"autonomous work"、"two-stage review"、"spec compliance"、"code quality review"等关键词。

## E (Execution) - 可执行步骤

1. **确认计划已批准**：确保 writing-plans 已完成，每个任务有明确的目标、文件路径、验收标准
   - 完成标准：计划文档中每个任务均含目标/文件路径/验收标准三要素，且有用户批准记录；任一任务缺项则退回补齐

2. **分派子 Agent**：为每个任务创建一个新鲜的子 Agent，传入任务描述和计划
   - 完成标准：每个任务对应一个独立子 Agent 会话，其输入包含完整任务描述且互不共享上下文

3. **第一阶段审查（规范合规性）**：子 Agent 完成后，检查实现是否严格按计划执行，是否有遗漏或偏离
   - 完成标准：对照验收标准逐条核对并形成"符合/偏离"清单，偏离项为零才进入第二阶段

4. **第二阶段审查（代码质量）**：检查代码是否符合最佳实践（命名、结构、测试覆盖、性能等）
   - 完成标准：按严重性分级的问题列表已产出，阻断级问题清零，非阻断项有处理决定

5. **汇总结果**：合并所有子 Agent 的输出，生成统一报告
   - 完成标准：报告中每个任务都有独立结论，无任务处于"未审/未知"状态

6. **用户确认**：向用户展示审查结果，询问是否需要调整
   - 完成标准：用户已对统一报告给出接受/调整的明确答复，调整项已登记为新任务

**判停条件**：所有子 Agent 完成且两阶段审查通过，或用户明确要求停止。

## B (Boundary) - 边界意识

**不适用的场景**：
- 单一小任务：不需要分派子 Agent，直接执行即可
- 探索性编程：SDD 依赖明确的计划，不适合探索性工作
- 紧急 hotfix：没有时间走完整流程，需要快速响应

**作者的盲点**：
- **Token 成本**：频繁分派子 Agent 可能导致 token 消耗过高，对于预算有限的项目需谨慎
- **子 Agent 能力差异**：不同子 Agent 可能有不同的能力水平，两阶段审查可能无法完全弥补差距
- **计划质量依赖**：SDD 的效果高度依赖 writing-plans 的质量，如果计划不清晰，子 Agent 可能偏离方向
