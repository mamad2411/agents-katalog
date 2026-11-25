---
name: no-fabrication
description: |
  当用户询问"去痕后是否会改变事实"、"如何确保真实性"或"AI 是否会编造内容"时调用此 skill。不适用于：创意写作、虚构内容生成、不需要事实准确性的场景。关键 trigger 信号：不编造、事实准确性、name/number/date/quote、来自源或作者、真实性。
source_book: Humanizer Blader
source_project: blader/humanizer
source_chapter: Introduction / no fabrication section
tags: [no-fabrication, factual-accuracy, truthfulness, source-verification]
related_skills: ["show-your-work", "preserve-style"]
---

# SKILL.md - No Fabrication（不编造事实）

## R (Reading) - 原文引用

> "It does not make things up. A name, number, date, quote, citation, or other factual detail must come from the source or the writer."
> 
> "Details such as the month and neighborhood need to come from the writer. If they are missing, Humanizer should ask instead of making them up."

## I (Interpretation) - 方法论骨架

**核心思想**：Humanizer 不编造事实，所有名称、数字、日期、引用、引文或其他事实细节必须来自源或作者。如果缺失，应该询问而不是编造。这种"不编造"原则确保去痕后的文本保持真实性。

**关键要素**：
1. **No Making Things Up**: 明确声明不编造任何内容
2. **Factual Details Must Come From Source**: 名称、数字、日期、引用等必须来自源或作者
3. **Ask Instead of Making Up**: 如果细节缺失，应该询问而不是编造

## A1 (Past Application) - 书中作者用过的案例

README 中明确强调了不编造事实的原则，并在里斯本旅行文本案例中展示了这一点：
- Before 版本包含"last October"、"Alfama"、"Graça"等具体细节
- After 版本保留了这些细节，没有添加或删除任何事实信息
- 如果原始文本缺少某些细节（如具体月份），Humanizer 应该询问而不是编造

这种设计确保了去痕后的文本在移除 AI 痕迹的同时保持事实准确性。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户担心去痕后会改变事实
- 用户想确保去痕后的文本保持真实性
- 用户想了解 AI 是否会编造内容
- 用户有严格的事实准确性要求（如新闻、学术写作）

**与相邻 skill 的区分**：
- 与 `show-your-work` 的区别：no-fabrication 关注**事实准确性**，而 show-your-work 关注**透明化流程**。前者是内容保障，后者是过程透明。
- 与 `preserve-style` 的区别：no-fabrication 关注**事实不编造**，而 preserve-style 关注**风格保持**。前者是真实性保障，后者是个性化保障。

## E (Execution) - 可执行步骤

1. **识别事实细节**
   - 标记文本中的所有名称、数字、日期、引用、引文
   - 确认这些细节是否来自源或作者
   - 检查是否有缺失的细节
   - 完成标准: 全部事实细节已汇成清单，缺失项单独标出

2. **验证事实来源**
   - 对于每个事实细节，确认其来源
   - 如果来源不明，标记为需要验证
   - 如果细节缺失，准备询问用户
   - 完成标准: 每条事实细节均已标注来源（源文本/作者/待询问）三类之一

3. **去痕时保持事实**
   - 在应用 35 个模式时，确保不改变事实细节
   - 只修改表达方式，不修改内容
   - 如果模式应用可能导致事实变化，跳过该模式
   - 完成标准: 重写前后逐条比对事实清单零篡改，被跳过的模式已记录

4. **询问缺失细节**
   - 如果发现缺失的细节（如具体月份、地点）
   - 向用户询问这些信息
   - 不要自行编造或猜测
   - 完成标准: 已就缺失细节向用户发出明确提问，回答中未引入任何新事实

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 创意写作（可以虚构内容）
- 虚构内容生成（不需要事实准确性）
- 用户明确要求添加某些细节
- 快速原型验证（不需要严格事实核查）

**作者的盲点**：
- Blader 假设所有用户都需要严格的事实准确性，但实际上某些场景（如创意写作）可能需要虚构
- humanizer 缺少对事实验证机制的具体说明（如何确认细节来自源或作者）
- 没有提到如何处理模糊或不确定的事实（如"大约"、"可能"等表述）