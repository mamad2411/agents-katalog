---
name: executing-plans
description: 当有已编写的实现计划需要在独立会话中执行时使用，包含评审检查点
---

# 执行计划

<HARD-GATE>
在执行任何实现任务之前，必须确认当前在 worktree 独立分支上工作（非 main/master）。
如果不在 worktree 中，必须先调用 using-git-worktrees skill 创建隔离工作空间。
禁止在 main/master 分支上直接执行实现计划。
</HARD-GATE>

## 概述

加载计划、批判性评审、执行所有任务、完成后汇报。

**开始时声明：**"我正在使用 executing-plans skill 来实现这个计划。"

**注意：** 在支持子代理的平台上（如 Claude Code 或 Codex）运行时，工作质量会显著提高。如果子代理可用，请使用 subagent-driven-development 代替此 skill。

## 流程

### 步骤 1：加载并评审计划

1. 读取计划文件
2. 批判性评审——识别计划中的任何问题或疑虑
3. 如有疑虑：在开始前向用户提出
4. 如无疑虑：创建 TodoWrite 并继续

### 步骤 2：执行任务

对每个任务：

1. 标记为进行中（in_progress）
2. 严格按照每一步执行（计划已拆分为细粒度步骤）
3. 按规定运行验证
4. 标记为已完成（completed）

### 步骤 3：完成开发

所有任务完成并验证通过后：

- 声明："我正在使用 finishing-a-development-branch skill 来完成这项工作。"
- **必须调用的子 skill：** 使用 finishing-a-development-branch
- 按照该 skill 的流程验证测试、展示选项、执行选择

## 何时停下来寻求帮助

**在以下情况下立即停止执行：**

- 遇到阻塞（缺少依赖、测试失败、指令不明确）
- 计划存在严重缺陷导致无法开始
- 不理解某条指令
- 验证反复失败

**宁可询问确认，也不要猜测。**

## 何时回到前面的步骤

**在以下情况下回到评审（步骤 1）：**

- 用户根据你的反馈更新了计划
- 基本方案需要重新思考

**不要强行通过阻塞点** — 停下来询问。

## 要点

- 先批判性评审计划
- 严格按照计划步骤执行
- 不要跳过验证
- 计划中提到的 skill 要实际调用
- 遇到阻塞时停止，不要猜测
- 未经用户明确同意，不要在 main/master 分支上开始实现

## 集成

**必需的工作流 skill：**

- **using-git-worktrees** — 必须：开始前搭建隔离工作空间
- **writing-plans** — 创建此 skill 执行的计划
- **finishing-a-development-branch** — 所有任务完成后收尾开发工作
