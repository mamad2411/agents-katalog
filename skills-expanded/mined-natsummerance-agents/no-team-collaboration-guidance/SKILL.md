---
name: no-team-collaboration-guidance
description: |
  当用户完成个人技能后不知道如何在团队中协作、缺乏 Git 工作流知识，或在真实团队环境中不知所措时调用此 skill。不适用于：纯个人练习、不需要团队协作的场景。关键 trigger 信号：团队协作、Git worktree、版本控制、协作开发、团队环境、多人项目。
source_book: Agent Skills Addy Osmani
source_project: addyosmani/agent-skills
source_chapter: N/A (absence of content)
tags: [anti-pattern, collaboration-gap, git-workflow, team-environment]
related_skills: ["no-systematic-methodology", "faster-is-safer"]
---

# SKILL.md - No Team Collaboration Guidance（缺少团队协作指导）

## R (Reading) - 原文引用

> (README 中完全没有提到 Git worktrees、团队协作或版本控制最佳实践)

## I (Interpretation) - 方法论骨架

**核心问题**：Agent Skills 假设用户独立使用 AI 编码助手，没有提供任何关于团队协作、Git 工作流或版本控制最佳实践的指导。用户在真实团队环境中可能不知所措，无法将个人技能经验转化为团队协作能力。

**反模式特征**：
1. **孤立开发**：用户习惯独自完成整个项目，不理解团队协作流程
2. **缺乏 Git 工作流知识**：不知道如何使用分支策略、代码审查或合并请求
3. **无法适应团队环境**：个人技能经验无法直接转化为团队协作能力
4. **版本控制混乱**：没有系统的版本管理习惯，导致代码冲突或丢失

**根本原因**：agent-skills 假设"个人完成技能就是目标"，但没有考虑真实软件开发是团队协作的过程。

## A1 (Past Application) - 书中作者用过的案例

Agent Skills 的 24+ 个技能都设计为个人独立完成：
- 没有提到 Git worktrees 或分支策略
- 没有提供代码审查或合并请求的指导
- 没有建议如何与团队成员协作开发

这种缺失导致用户可能完成了 `/spec` 或 `/build` 技能，但在真实团队项目中不知道如何与他人协作。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户完成个人技能后想知道如何在团队中协作
- 用户缺乏 Git 工作流知识，不知道如何管理分支
- 用户在真实团队环境中不知所措
- 用户想学习如何将个人技能经验转化为团队协作能力
- 用户想了解现代软件开发的协作流程

**与相邻 skill 的区分**：
- 与 `no-systematic-methodology` 的区别：no-team-collaboration-guidance 是**具体的协作盲点**，而 no-systematic-methodology 是**整体学习框架的缺失**。前者更具体，后者更宏观。
- 与 `faster-is-safer` 的区别：no-team-collaboration-guidance 关注**团队协作能力**，而 faster-is-safer 关注**部署频率和风险**。两者互补：一个确保能与他人合作，一个确保快速安全交付。

## E (Execution) - 可执行步骤

1. **识别反模式症状**
   - 询问用户是否有团队协作经验
   - 检查用户是否了解 Git 工作流（分支策略、合并请求等）
   - 评估用户是否能清晰描述自己在团队中的角色
   - 完成标准: 三项症状核查完成，输出明确的差距清单

2. **引入协作思维**
   - 解释现代软件开发是团队协作的过程，不是个人英雄主义
   - 强调 Git 工作流的重要性（如 Git Flow、GitHub Flow）
   - 介绍代码审查的价值和质量保障作用
   - 完成标准: 用户能复述至少一种分支策略及代码审查的作用

3. **建立协作习惯**
   - 学习使用 Git worktrees 进行隔离开发
   - 实践分支策略（feature branches、develop branch、main branch）
   - 参与开源项目或团队项目获取实际经验
   - 完成标准: 用 worktree 或 feature branch 独立完成一次隔离开发练习并合并

4. **避免常见陷阱**
   - 不要直接在 main 分支上开发新功能
   - 不要忽视代码审查反馈
   - 不要害怕寻求帮助或讨论技术方案
   - 完成标准: 对照陷阱清单自查通过，无直接提交 main 等违规操作

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯个人练习（不需要团队协作）
- 一次性脚本或原型验证
- 用户已经有丰富的团队协作经验
- 用户只需要单个技能建议，不需要协作指导

**作者的盲点**：
- Addy Osmani 假设"个人完成技能就是目标"，但没有考虑真实软件开发是团队协作的过程
- agent-skills 缺少对 Git 工作流、代码审查和团队协作的任何提及
- 这种"个人优先于团队"的思路可能导致用户在真实工作环境中难以适应，无法将个人技能转化为团队价值
