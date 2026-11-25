---
name: no-collaboration-guidance
description: |
  当用户完成个人项目后不知道如何在团队中协作、缺乏 Git 工作流知识，或在真实团队环境中不知所措时调用此 skill。不适用于：纯个人练习、不需要团队协作的场景。关键 trigger 信号：团队协作、Git worktree、版本控制、协作开发、团队环境、多人项目。
source_book: App Ideas Collection Florin Pop
source_project: florinpop17/app-ideas
source_chapter: N/A (absence of content)
tags: [anti-pattern, collaboration-gap, git-workflow, team-environment]
related_skills: ["no-systematic-methodology", "no-testing-guidance"]
---

# SKILL.md - No Collaboration Guidance（缺少协作指导）

## R (Reading) - 原文引用

> (README 中完全没有提到 Git worktrees、团队协作或版本控制最佳实践)

## I (Interpretation) - 方法论骨架

**核心问题**：App Ideas Collection 假设学习者独立完成项目，没有提供任何关于团队协作、Git 工作流或版本控制最佳实践的指导。学习者在真实团队环境中可能不知所措，无法将个人项目经验转化为团队协作能力。

**反模式特征**：
1. **孤立开发**：学习者习惯独自完成整个项目，不理解团队协作流程
2. **缺乏 Git 工作流知识**：不知道如何使用分支策略、代码审查或合并请求
3. **无法适应团队环境**：个人项目经验无法直接转化为团队协作能力
4. **版本控制混乱**：没有系统的版本管理习惯，导致代码冲突或丢失

**根本原因**：app-ideas 假设"个人完成项目就是目标"，但没有考虑真实软件开发是团队协作的过程。

## A1 (Past Application) - 书中作者用过的案例

App Ideas Collection 的 89 个项目都设计为个人独立完成：
- 没有提到 Git worktrees 或分支策略
- 没有提供代码审查或合并请求的指导
- 没有建议如何与团队成员协作开发

这种缺失导致学习者可能完成了 Instagram Clone 或 Chat App，但在真实团队项目中不知道如何与他人协作。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户完成个人项目后想知道如何在团队中协作
- 用户缺乏 Git 工作流知识，不知道如何管理分支
- 用户在真实团队环境中不知所措
- 用户想学习如何将个人项目经验转化为团队协作能力
- 用户想了解现代软件开发的协作流程

**与相邻 skill 的区分**：
- 与 `no-systematic-methodology` 的区别：no-collaboration-guidance 是**具体的协作盲点**，而 no-systematic-methodology 是**整体学习框架的缺失**。前者更具体，后者更宏观。
- 与 `no-testing-guidance` 的区别：no-collaboration-guidance 关注**团队协作能力**，而 no-testing-guidance 关注**代码质量验证**。两者互补：一个确保能与他人合作，一个确保代码正确。

## E (Execution) - 可执行步骤

1. **识别反模式症状**
   - 询问用户是否有团队协作经验
   - 检查用户是否了解 Git 工作流（分支策略、合并请求等）
   - 评估用户是否能清晰描述自己在团队中的角色
   - 完成标准：三项检查均已获得用户的明确回答，并形成"具备/缺失"二值结论的症状清单

2. **引入协作思维**
   - 解释现代软件开发是团队协作的过程，不是个人英雄主义
   - 强调 Git 工作流的重要性（如 Git Flow、GitHub Flow）
   - 介绍代码审查的价值和质量保障作用
   - 完成标准：用户能用自己的话复述一种工作流（Git Flow 或 GitHub Flow）的核心分支规则与代码审查的作用

3. **建立协作习惯**
   - 学习使用 Git worktrees 进行隔离开发
   - 实践分支策略（feature branches、develop branch、main branch）
   - 参与开源项目或团队项目获取实际经验
   - 完成标准：用户在练习仓库完成至少一次"feature 分支开发 → 发起合并请求"全流程，期间无直接提交 main 的操作

4. **避免常见陷阱**
   - 不要直接在 main 分支上开发新功能
   - 不要忽视代码审查反馈
   - 不要害怕寻求帮助或讨论技术方案
   - 完成标准：用户给出的后续开发计划中不含"直接改 main/忽略审查反馈"类行为，且对三条陷阱各列出一条对应的规避动作

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯个人练习（不需要团队协作）
- 一次性脚本或原型验证
- 用户已经有丰富的团队协作经验
- 用户只需要单个项目建议，不需要协作指导

**作者的盲点**：
- Florin Pop 假设"个人完成项目就是目标"，但没有考虑真实软件开发是团队协作的过程
- app-ideas 缺少对 Git 工作流、代码审查和团队协作的任何提及
- 这种"个人优先于团队"的思路可能导致学习者在真实工作环境中难以适应，无法将个人技能转化为团队价值
