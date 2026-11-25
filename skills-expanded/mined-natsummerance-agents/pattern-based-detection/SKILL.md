---
name: pattern-based-detection
description: |
  当用户询问"如何识别 AI 痕迹"、"有哪些 AI 写作特征"或"如何系统化检测 AI 生成文本"时调用此 skill。不适用于：纯创意写作评估、非文本类内容分析。关键 trigger 信号：AI 痕迹、AI 写作特征、35 patterns、Wikipedia Signs of AI writing、模式检测。
source_book: Humanizer Blader
source_project: blader/humanizer
source_chapter: Introduction / pattern list section
tags: [ai-detection, pattern-matching, wikipedia-patterns]
related_skills: ["two-pass-rewriting", "voice-matching"]
---

# SKILL.md - Pattern-Based Detection（基于模式的 AI 痕迹检测）

## R (Reading) - 原文引用

> "Humanizer uses 35 patterns from Wikipedia's [\"Signs of AI writing\"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup."

## I (Interpretation) - 方法论骨架

**核心思想**：使用 35 个来自 Wikipedia 的模式来识别和移除 AI 生成的文本特征。这些模式涵盖夸大重要性、过度使用的 AI 词汇、格式问题、结构逻辑问题等多个类别，为系统化检测 AI 痕迹提供了标准化框架。

**关键要素**：
1. **35 Patterns**: 来自 Wikipedia 的标准化模式列表
2. **Categorized**: 按类别分组（夸大重要性、AI 词汇、格式问题、结构逻辑、Chatbot 特征、填充词）
3. **Maintained by WikiProject AI Cleanup**: 由维基百科项目持续维护

## A1 (Past Application) - 书中作者用过的案例

Humanizer 的核心就是基于这 35 个模式进行 AI 痕迹检测。README 中详细列出了所有模式及其 Before/After 对比示例，如：
- Pattern 1: Inflated importance and legacy（夸大重要性和遗产）
- Pattern 7: Overused AI words（过度使用的 AI 词汇）
- Pattern 14: Em/en dashes（破折号滥用）
- Pattern 20: Chatbot text left in the answer（Chatbot 文本残留）

这种基于模式的检测方法确保了系统化和标准化的 AI 痕迹识别。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户想知道如何识别 AI 生成的文本
- 用户想了解有哪些常见的 AI 写作特征
- 用户想建立系统化的 AI 痕迹检测方法
- 用户想学习 Wikipedia 的 35 个模式

**与相邻 skill 的区分**：
- 与 `two-pass-rewriting` 的区别：pattern-based-detection 关注**识别 AI 痕迹**，而 two-pass-rewriting 关注**去痕流程**。前者是检测阶段，后者是重写阶段。
- 与 `voice-matching` 的区别：pattern-based-detection 关注**通用模式检测**，而 voice-matching 关注**个性化风格匹配**。前者是标准化方法，后者是个性化调整。

## E (Execution) - 可执行步骤

1. **了解 35 个模式**
   - 阅读 Wikipedia 的"Signs of AI writing"页面
   - 理解每个模式的含义和示例
   - 掌握模式的分类（6 个类别）
   - 完成标准: 能复述 6 个类别名称，并为每个类别举出至少一个具体模式

2. **应用模式检测**
   - 逐段检查文本是否包含 AI 痕迹
   - 标记出符合模式的段落
   - 记录检测到的模式类型
   - 完成标准: 输出检测报告，含命中模式编号、原文引用与所在位置

3. **评估检测结果**
   - 统计检测到的模式数量
   - 分析哪些类别的模式最频繁
   - 确定需要重点改进的方面
   - 完成标准: 有各类别命中次数统计与优先改进项排序

4. **制定去痕策略**
   - 根据检测结果确定优先级
   - 选择适合的去痕方法
   - 准备进入两遍重写流程
   - 完成标准: 形成书面去痕优先级清单，并确认转入 two-pass-rewriting 阶段

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯创意写作评估（可能需要保留某些 AI 特征）
- 非文本类内容分析（如代码、数据、图像）
- 快速原型验证（不需要完整检测）

**作者的盲点**：
- Blader 假设 35 个模式足以覆盖所有 AI 痕迹，但实际上可能还有未发现的特征
- humanizer 缺少对模式权重的说明，所有模式同等重要可能不合理
- 没有提到如何更新模式列表以应对新的 AI 写作特征