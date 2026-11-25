---
name: no-systematic-methodology
description: |
  当用户安装了 humanizer 技能但仍感到迷茫、不知道如何系统提升识别 AI 痕迹的能力，或随机应用模式缺乏连贯的去痕策略时调用此 skill。不适用于：已有明确去痕计划的用户、只需要单个模式建议的场景。关键 trigger 信号：迷茫、不知道下一步、随机应用模式、缺乏系统性、完成去痕但没进步。
source_book: Humanizer Blader
source_project: blader/humanizer
source_chapter: Introduction / problem statement
tags: [anti-pattern, systematic-learning, methodology-gap]
related_skills: ["no-progress-tracking", "pattern-based-detection"]
---

# SKILL.md - No Systematic Methodology（缺乏系统性方法论）

## R (Reading) - 原文引用

> "Humanizer uses 35 patterns from Wikipedia's [\"Signs of AI writing\"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup."

## I (Interpretation) - 方法论骨架

**核心问题**：Humanizer 只提供了 35 个模式列表，但没有提供系统性的学习方法论。用户可能安装了技能，但仍然不知道如何系统地提升识别 AI 痕迹的能力或选择下一个要学习的模式。

**反模式特征**：
1. **随机应用模式**：用户根据兴趣或难度随机选择模式，缺乏连贯的去痕策略
2. **完成去痕但不确定是否掌握**：没有明确的模式评估标准
3. **无法将模式经验转化为可迁移的识别能力**：每个模式都是孤立的练习

**根本原因**：humanizer 是一个模式集合，而不是一个结构化的学习框架。它提供了内容，但没有提供方法论。

## A1 (Past Application) - 书中作者用过的案例

Humanizer 本身就是一个典型案例：它列出了 35 个模式，按类别分组，但没有提供：
- 如何选择模式的系统性方法
- 如何评估自己是否真正掌握了某个模式
- 如何将模式经验转化为可迁移的识别能力

这种"只是模式列表"的设计导致用户可能完成多个模式的练习，但仍然不知道自己的真实水平或下一步该做什么。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户完成了几个模式的练习，但仍感到迷茫，不知道下一步该做什么
- 用户随机应用模式，缺乏连贯的去痕策略
- 用户想知道自己是否真正提升了识别 AI 痕迹的能力
- 用户想建立系统性的学习方法，而不是随机练习

**与相邻 skill 的区分**：
- 与 `no-progress-tracking` 的区别：no-systematic-methodology 是**整体学习框架的缺失**，而 no-progress-tracking 是**具体进度追踪机制的缺失**。前者更宏观，后者更具体。
- 与 `pattern-based-detection` 的区别：no-systematic-methodology 是**反模式警示**（指出 humanizer 的缺陷），而 pattern-based-detection 是**正面指导**（提供基于模式的检测）。两者互补：先识别问题，再应用解决方案。

## E (Execution) - 可执行步骤

1. **识别反模式症状**
   - 询问用户是否随机应用模式
   - 检查用户是否有明确的去痕目标
   - 评估用户是否能清晰描述自己的识别能力提升
   - 完成标准: 三项问询均有答案，能明确判断用户是否随机选模式、有无去痕目标

2. **引入系统性方法论**
   - 基于 6 个模式类别建立学习路径（夸大重要性 → AI 词汇 → 格式问题 → 结构逻辑 → Chatbot 特征 → 填充词）
   - 为每个类别设定明确的模式学习目标
   - 建立模式之间的依赖关系
   - 完成标准: 输出覆盖 6 个类别的学习路径，类别间依赖关系已成文

3. **建立反馈循环**
   - 定期回顾已完成的模式练习
   - 评估是否真正掌握了该类别的模式
   - 根据反馈调整下一个模式的选择
   - 完成标准: 每个类别有掌握度评估结论，下一个模式的选择有明确依据

4. **避免随机选择**
   - 不要仅凭兴趣选择模式
   - 确保每个模式都有明确的学习目标
   - 将模式串联成连贯的学习路径
   - 完成标准: 当前及后续至少 3 个模式的选取理由均可追溯到学习路径

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 用户已经有明确的学习计划或课程大纲
- 用户只是为了兴趣而练习，不追求系统性提升
- 用户只需要单个模式建议，不需要整体框架

**作者的盲点**：
- Blader 假设"提供模式列表"就足以帮助用户提升识别能力，但实际上用户更需要的是方法论
- humanizer 缺少对学习路径、模式评估和反馈循环的设计
- 这种"内容优先于方法"的思路可能导致用户完成多个模式练习但仍感到迷茫