---
name: subjective-human-sounding
description: |
  当用户对去痕效果不满意、认为仍然"太人工"，或想了解"像人写的"是否有统一标准时调用此 skill。不适用于：对去痕效果满意的用户、不需要讨论主观性的场景。关键 trigger 信号：像人写的、主观性、去痕效果不满意、太人工、统一标准、读者偏好。
source_book: Humanizer Blader
source_chapter: Introduction
tags: [anti-pattern, subjectivity, human-sounding, reader-preference]
related_skills: ["preserve-style", "voice-matching"]
---

# SKILL.md - Subjective "Human-Sounding"（"像人写的"的主观性）

## R (Reading) - 原文引用

> "Humanizer rewrites AI-sounding text so it reads like a person wrote it, without changing what it says."

## I (Interpretation) - 方法论骨架

**核心问题**：Humanizer 假设"像人写的"有一个统一标准，但实际上不同读者对什么样的文本像人写的可能有不同看法。这种主观性可能导致去痕效果不符合某些用户的期望。

**反模式特征**：
1. **用户对去痕效果不满意**：认为仍然"太人工"或"太自然"
2. **缺乏客观标准**：无法用量化指标评估去痕质量
3. **可能过度简化**：35 个模式可能无法覆盖所有读者的偏好
4. **读者偏好差异**：不同文化背景、阅读习惯的读者可能有不同标准

**根本原因**：humanizer 假设存在一个通用的"像人写的"标准，但实际上这是一个高度主观的概念。

## A1 (Past Application) - 书中作者用过的案例

README 中定义了 Humanizer 的目标是"rewrites AI-sounding text so it reads like a person wrote it"，但没有说明：
- 什么是"像人写的"的具体标准
- 如何验证去痕后的文本真的像人写的
- 不同读者可能有不同偏好的处理方式

这种缺失导致用户可能对去痕效果有不同评价，有些人认为很好，有些人认为仍然不够自然。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户对去痕效果不满意，认为仍然"太人工"
- 用户想了解"像人写的"是否有统一标准
- 用户想知道如何处理不同读者的偏好差异
- 用户想建立更客观的去痕质量评估机制

**与相邻 skill 的区分**：
- 与 `preserve-style` 的区别：subjective-human-sounding 关注**去痕效果的主观性**，而 preserve-style 关注**保持作者风格**。前者是评估问题，后者是风格问题。
- 与 `voice-matching` 的区别：subjective-human-sounding 关注**读者偏好的差异**，而 voice-matching 关注**匹配作者风格**。前者是多读者视角，后者是单作者视角。

## E (Execution) - 可执行步骤

1. **识别主观性问题**
   - 询问用户对去痕效果的具体不满
   - 检查用户是否有特定的读者群体
   - 评估用户是否了解不同读者的偏好差异

2. **定义目标读者**
   - 明确去痕后的文本主要给谁看
   - 了解目标读者的阅读习惯和偏好
   - 根据目标读者调整去痕策略

3. **寻求多方反馈**
   - 请多个读者评估去痕效果
   - 收集不同意见并分析共同点
   - 根据反馈调整去痕参数

4. **建立客观评估指标**
   - 虽然"像人写的"是主观的，但可以建立一些客观指标
   - 如句子长度变化、词汇多样性、标点使用频率等
   - 用这些指标辅助主观判断

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 用户对去痕效果满意
- 不需要讨论主观性的场景
- 用户有明确的单一目标读者
- 快速原型验证（不需要精细主观调整）

**作者的盲点**：
- Blader 假设存在一个通用的"像人写的"标准，但实际上这是一个高度主观的概念
- humanizer 缺少对不同读者偏好的任何提及
- 没有提到如何配置去痕强度以适应不同读者的期望
