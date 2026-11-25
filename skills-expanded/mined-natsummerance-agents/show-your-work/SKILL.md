---
name: show-your-work
description: |
  当用户询问"如何理解去痕的逻辑"、"能否看到中间结果"或"去痕过程是否透明"时调用此 skill。不适用于：一次性快速去痕、不需要透明化的场景、只关心最终结果的用户。关键 trigger 信号：显示工作过程、中间结果、透明化、first rewrite、critique、可解释性。
source_book: Humanizer Blader
source_chapter: Introduction / workflow description
tags: [transparency, show-work, intermediate-results, explainability]
related_skills: ["two-pass-rewriting", "no-fabrication"]
---

# SKILL.md - Show Your Work（显示工作过程）

## R (Reading) - 原文引用

> "When you paste text, Humanizer shows its work before giving you the final version. You see the first rewrite and a short critique of anything that still sounds artificial."

## I (Interpretation) - 方法论骨架

**核心思想**：Humanizer 在给出最终版本之前显示其工作过程，让用户看到第一次重写和对仍听起来人工的内容的简短批评。这种"透明化"流程让用户理解去痕的逻辑，并可以提出反馈。

**关键要素**：
1. **Show Before Final**: 在给出最终版本之前显示工作过程
2. **First Rewrite**: 展示第一次重写结果
3. **Short Critique**: 对仍听起来人工的内容进行简短批评
4. **User Feedback**: 允许用户根据中间结果提出反馈

## A1 (Past Application) - 书中作者用过的案例

Humanizer 的工作流程就是典型的显示工作过程：
1. 用户粘贴文本
2. Humanizer 进行第一次重写
3. **显示第一次重写结果**（这是关键步骤）
4. **显示对仍听起来人工的内容的简短批评**（这也是关键步骤）
5. 用户可以看到中间结果并提出反馈
6. Humanizer 进行最终重写并给出最终版本

这种设计确保了去痕过程的透明化和可解释性，用户可以理解为什么某些部分被修改。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户想理解去痕的逻辑
- 用户想看到中间结果并提出反馈
- 用户想知道去痕过程是否透明
- 用户想学习如何识别 AI 痕迹

**与相邻 skill 的区分**：
- 与 `two-pass-rewriting` 的区别：show-your-work 是**透明化原则**，而 two-pass-rewriting 是**具体的两遍重写机制**。前者是更广泛的原则，后者是具体实现。
- 与 `no-fabrication` 的区别：show-your-work 关注**过程透明**，而 no-fabrication 关注**事实准确性**。前者是过程保障，后者是内容保障。

## E (Execution) - 可执行步骤

1. **请求显示工作过程**
   - 在使用 `/humanizer` 时，明确要求显示中间结果
   - 或者使用默认流程（Humanizer 会自动显示）

2. **查看第一次重写**
   - 仔细阅读第一次重写结果
   - 对比原始文本，理解哪些部分被修改
   - 注意修改的原因和逻辑

3. **阅读批评内容**
   - 查看对仍听起来人工的内容的简短批评
   - 理解哪些部分仍需改进
   - 评估批评是否合理

4. **提供反馈**
   - 如果对中间结果不满意，提供具体反馈
   - 指出哪些修改不符合期望
   - 说明希望保持的风格或表达方式

5. **确认最终版本**
   - 在理解工作过程后，确认最终版本
   - 确保最终结果符合期望

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 一次性快速去痕（不需要中间结果）
- 不需要透明化的场景（用户只关心最终结果）
- 实时去痕需求（没有时间查看中间结果）
- 用户信任 Humanizer 的判断，不需要了解细节

**作者的盲点**：
- Blader 假设所有用户都想看到中间结果，但实际上某些用户可能只需要最终版本
- humanizer 缺少对跳过显示工作过程的选项
- 没有提到如何配置批评的详细程度（简要 vs 详细）
