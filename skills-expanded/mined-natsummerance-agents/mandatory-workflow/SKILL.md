---
name: mandatory-workflow
description: |
  当用户需要了解或使用 Superpowers 的 7 步强制工作流时调用此 skill。适用于所有软件开发任务，包括新功能开发、Bug 修复、重构任务。不适用于：一次性脚本、纯艺术性代码、紧急 hotfix。关键 trigger 信号："7 steps"、"mandatory workflow"、"brainstorming"、"writing-plans"、"subagent-driven-development"、"test-driven-development"、"requesting-code-review"、"finishing-branch"。
source_book: 《Superpowers》 obra
source_project: obra/superpowers
source_chapter: The Basic Workflow / How it works
tags: [framework, workflow, mandatory]
related_skills: []
---

# Mandatory 7-Step Workflow

## R (Reading) - 原文引用

> "The Basic Workflow: 1. brainstorming - Activates before writing code... 2. using-git-worktrees... 3. writing-plans... 4. subagent-driven-development or executing-plans... 5. test-driven-development... 6. requesting-code-review... 7. finishing-a-development-branch..."

> "The agent checks for relevant skills before any task. Mandatory workflows, not suggestions."

## I (Interpretation) - 方法论骨架

Mandatory 7-Step Workflow 是 Superpowers 的核心框架，定义了从需求理解到完成交付的完整流程：

1. **brainstorming**：激活于写代码前，通过问题细化需求，分块展示设计供验证
2. **using-git-worktrees**：激活于设计批准后，创建隔离工作区，验证测试基线
3. **writing-plans**：激活于设计批准后，将工作分解为 2-5 分钟的小任务
4. **subagent-driven-development / executing-plans**：激活于计划后，分派子 Agent 或批量执行
5. **test-driven-development**：激活于实现中，强制执行 RED-GREEN-REFACTOR
6. **requesting-code-review**：激活于任务间，按严重性报告问题
7. **finishing-a-development-branch**：激活于任务完成，验证测试，清理工作区

关键特点是：**每个步骤在特定时机自动激活**，不是建议而是强制工作流。Agent 在执行任何任务前都会检查相关 skills。

## A1 (Past Application) - 书中作者用过的案例

在 Superpowers 的设计理念中，这个 7 步工作流是核心架构。作者 Jesse Vincent 强调，一旦用户说"go"，系统就会自动按照这个流程执行，不需要用户做任何特殊操作。这是 Superpowers 与传统编码助手的关键区别。

## A2 (Future Trigger) - 何时调用

**调用时机**：
- 用户需要了解 Superpowers 的完整工作流程
- 用户想确认某个步骤是否必须执行
- 用户遇到流程中断或跳过步骤的问题
- 用户需要调试为什么某个 skill 没有触发

**不调用时机**：
- 单一小任务（不需要完整工作流）
- 一次性脚本（不需要严格流程）
- 紧急 hotfix（没有时间走完整流程）

**与相邻 skill 的区分**：
- 与 `subagent-driven-development` 的区别：mandatory-workflow 描述整体流程框架；SDD 是第 4 步的具体实现模式
- 与 `git-worktree-isolation` 的关系：git-worktree-isolation 是第 2 步的具体实现

**关键 trigger 信号**：用户提到"7 steps"、"mandatory workflow"、"brainstorming"、"writing-plans"、"subagent-driven-development"、"test-driven-development"、"requesting-code-review"、"finishing-branch"等关键词。

## E (Execution) - 可执行步骤

1. **确认当前所处步骤**：识别用户当前处于 7 步工作流的哪一步
   - 完成标准：已对照 7 步定义给出唯一的当前步骤编号，并列出判定依据

2. **检查前置条件**：确认上一步骤已完成且通过验证
   - 完成标准：前置步骤均有完成证据（产物或验证记录）；任一缺失则回到该步骤补齐，不允许跳过

3. **激活对应 skill**：根据当前步骤激活相应的 skill（如 brainstorming、writing-plans 等）
   - 完成标准：目标 skill 的名称与激活时机均已写明，且与步骤编号一一对应

4. **执行该步骤的核心逻辑**：按照该 skill 的定义执行
   - 完成标准：按被激活 skill 自身的完成标准逐条核验通过

5. **验证完成标准**：确认该步骤已完成，可以进入下一步
   - 完成标准：本步骤的完成标准全部满足并留有核对记录，得到进入下一步的放行结论

6. **记录进度**：更新 PIPELINE_STATE.md 或类似状态文件
   - 完成标准：状态文件中当前步骤已标记完成、下一步骤已标记待办，时间戳为本次更新时间

**判停条件**：当前步骤完成且通过验证，或用户明确要求停止/跳过。

## B (Boundary) - 边界意识

**不适用的场景**：
- 单一小任务：不需要完整 7 步工作流，可以直接执行
- 探索性编程：brainstorming 和 writing-plans 可能过于严格
- 紧急 hotfix：没有时间走完整流程，需要快速响应

**作者的盲点**：
- **流程刚性**：7 步工作流对于小型项目可能过于繁琐，缺乏灵活性
- **步骤依赖**：如果某一步骤失败（如 brainstorming 无法细化需求），整个流程可能卡住
- **自动化程度**：虽然声称"自动激活"，但实际实现可能依赖特定编码 Agent 的支持
