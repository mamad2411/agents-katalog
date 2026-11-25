---
name: english-centric-patterns
description: |
  当用户处理非英文文本、想了解模式列表是否适用于其他语言，或发现去痕效果在非英文文本上不佳时调用此 skill。不适用于：纯英文文本、不需要多语言支持的用户。关键 trigger 信号：非英文、多语言、中文文本、日文文本、模式适用性、语言局限。
source_book: Humanizer Blader
source_project: blader/humanizer
source_chapter: Introduction / pattern list section
tags: [anti-pattern, language-limitation, multilingual, english-centric]
related_skills: ["pattern-based-detection", "preserve-style"]
---

# SKILL.md - English-Centric Patterns（以英文为中心的模式列表）

## R (Reading) - 原文引用

> "Humanizer uses 35 patterns from Wikipedia's [\"Signs of AI writing\"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup."

## I (Interpretation) - 方法论骨架

**核心问题**：Humanizer 的 35 个模式主要来自 Wikipedia 的英文"Signs of AI writing"页面，可能不适用于其他语言的 AI 写作特征。这种"以英文为中心"的设计限制了其在多语言环境中的适用性。

**反模式特征**：
1. **非英文文本的去痕效果可能不佳**：模式主要针对英文 AI 写作特征
2. **缺乏对其他语言 AI 写作特征的覆盖**：如中文、日文、韩文等
3. **可能误导用户认为去痕是通用的**：实际上可能只适用于英文
4. **文化差异未考虑**：不同语言的写作习惯和文化背景不同

**根本原因**：humanizer 依赖 Wikipedia 的英文模式列表，没有考虑多语言环境的差异化需求。

## A1 (Past Application) - 书中作者用过的案例

README 中提到的 35 个模式都来自 Wikipedia 的英文页面，示例也都是英文文本（如里斯本旅行文本）。没有提到：
- 如何处理中文、日文、韩文等非英文文本
- 其他语言的 AI 写作特征是否与英文相同
- 是否需要为不同语言定制模式列表

这种缺失导致用户在处理非英文文本时可能遇到去痕效果不佳的问题。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户处理非英文文本（如中文、日文、韩文）
- 用户想了解模式列表是否适用于其他语言
- 用户发现去痕效果在非英文文本上不佳
- 用户想建立多语言的 AI 痕迹检测方法

**与相邻 skill 的区分**：
- 与 `pattern-based-detection` 的区别：english-centric-patterns 关注**语言局限性**，而 pattern-based-detection 关注**通用模式检测**。前者是局限性警示，后者是正面指导。
- 与 `preserve-style` 的区别：english-centric-patterns 关注**多语言适配问题**，而 preserve-style 关注**风格保持**。前者是语言层面，后者是风格层面。

## E (Execution) - 可执行步骤

1. **识别语言类型**
   - 确认文本的语言类型（英文、中文、日文等）
   - 评估当前模式列表是否适用于该语言
   - 检查是否有针对该语言的特定 AI 写作特征
   - 完成标准: 已输出文本语言判定，并给出"当前模式列表适用/部分适用/不适用"的明确结论

2. **评估去痕效果**
   - 对非英文文本应用去痕后，检查效果是否满意
   - 如果不满意，分析哪些模式不适用
   - 记录不适用的模式和原因
   - 完成标准: 产出不适用的模式清单，每条模式均附具体原因

3. **寻找替代方案**
   - 查找针对该语言的 AI 写作特征研究
   - 寻找其他工具或方法处理非英文文本
   - 考虑手动调整去痕策略
   - 完成标准: 至少列出一条可立即执行的替代方案或手动调整策略

4. **反馈和改进**
   - 向 humanizer 开发者反馈多语言支持需求
   - 参与 WikiProject AI Cleanup 的多语言扩展工作
   - 分享自己的经验和发现
   - 完成标准: 已形成可提交的反馈或经验记录（issue/社区帖子/笔记）

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯英文文本
- 不需要多语言支持的用户
- 用户只处理英文内容
- 快速原型验证（不需要精细多语言调整）

**作者的盲点**：
- Blader 假设 35 个英文模式足以覆盖所有语言的 AI 写作特征，但实际上不同语言可能有不同的特征
- humanizer 缺少对多语言支持的任何提及或计划
- 没有提到如何为不同语言定制模式列表