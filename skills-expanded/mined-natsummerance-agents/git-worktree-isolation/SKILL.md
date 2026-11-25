---
name: git-worktree-isolation
description: |
  当用户需要在不影响主分支的情况下并行开发多个功能、创建隔离工作区、或验证干净的测试基线时调用此 skill。适用于大型功能开发、实验性变更、需要隔离的测试环境。不适用于：单一小修改、不需要 Git 的项目、紧急 hotfix。关键 trigger 信号："git worktree"、"isolated workspace"、"parallel branches"、"clean test baseline"、"new branch"。
source_book: 《Superpowers》 obra
source_project: obra/superpowers
source_chapter: The Basic Workflow / What's Inside
tags: [framework, git, isolation, parallel]
related_skills: ["mandatory-workflow"]
---

# Git Worktree Isolation

## R (Reading) - 原文引用

> "using-git-worktrees - Activates after design approval. Creates isolated workspace on new branch, runs project setup, verifies clean test baseline."

## I (Interpretation) - 方法论骨架

Git Worktree Isolation 是一种使用 Git worktrees 创建隔离工作区的方法论。其核心是：

1. **隔离工作区**：在新分支上创建工作区，不影响主分支或其他开发者的工作
2. **项目设置**：自动运行项目初始化脚本，确保环境一致
3. **验证测试基线**：确认测试套件在干净状态下通过，排除环境干扰

这种方法的优势在于：通过 Git worktrees 实现真正的隔离（而非简单的分支切换），保证每个功能开发的独立性，同时通过验证测试基线确保问题不是由环境引起的。

## A1 (Past Application) - 书中作者用过的案例

在 Superpowers 的基本工作流中，第 2 步明确说明：设计批准后，系统会激活 using-git-worktrees skill，创建隔离工作区并验证测试基线。这是确保后续开发在一个干净、可预测的环境中进行的關鍵步骤。

## A2 (Future Trigger) - 何时调用

**调用时机**：
- 用户需要在不影响主分支的情况下并行开发多个功能
- 用户需要创建实验性变更，可能失败但不想污染主分支
- 用户需要验证测试基线是否干净，排除环境干扰
- 用户提到"git worktree"、"isolated workspace"、"parallel branches"等关键词

**不调用时机**：
- 单一小修改（不需要隔离工作区）
- 不需要 Git 的项目（如纯前端原型）
- 紧急 hotfix（没有时间创建工作区）

**与相邻 skill 的区分**：
- 与 `mandatory-workflow` 的关系：git-worktree-isolation 是 mandatory-workflow 第 2 步的具体实现
- 与 `subagent-driven-development` 的区别：git-worktree-isolation 关注代码隔离；SDD 关注任务分派和审查

**关键 trigger 信号**：用户提到"git worktree"、"isolated workspace"、"parallel branches"、"clean test baseline"、"new branch"等关键词。

## E (Execution) - 可执行步骤

1. **确认设计已批准**：确保 brainstorming 和 design chunking 已完成，用户已签字确认
   - 完成标准：存在用户对设计方案的明确批准记录（消息引用或状态文件标记），缺失则停下询问

2. **创建新分支**：基于当前主分支创建新分支（如 `feature/xxx`）
   - 完成标准：`git branch` 输出中新分支存在且基于最新主分支创建，命名符合 `feature/xxx` 约定

3. **创建 worktree**：使用 `git worktree add <path> <branch>` 创建隔离工作区
   - 完成标准：`git worktree list` 中能看到新 worktree 条目，目录已生成且指向新分支

4. **运行项目设置**：执行项目初始化脚本（如 `npm install`、`pip install -r requirements.txt` 等）
   - 完成标准：初始化脚本以退出码 0 结束，依赖清单与主工作区一致

5. **验证测试基线**：运行测试套件，确认所有测试通过
   - 完成标准：测试套件完整跑完且全部通过；若有失败，先判定为环境问题并记录，不带病开工

6. **记录状态**：更新项目状态文件，标记工作区已就绪
   - 完成标准：状态文件中新增了 worktree 路径、分支名、基线测试结果的条目

**判停条件**：worktree 创建成功且测试基线验证通过，或用户明确要求停止。

## B (Boundary) - 边界意识

**不适用的场景**：
- 单一小修改：不需要隔离工作区，直接在当前分支修改即可
- 不需要 Git 的项目：如纯前端原型、笔记项目等
- 紧急 hotfix：没有时间创建工作区，需要快速响应

**作者的盲点**：
- **Git 知识门槛**：using-git-worktrees 需要一定的 Git 知识，对新手不友好
- **磁盘空间消耗**：每个 worktree 都会占用磁盘空间，长期积累可能导致空间不足
- **worktree 管理复杂度**：多个 worktree 并存时，切换和管理可能变得复杂
