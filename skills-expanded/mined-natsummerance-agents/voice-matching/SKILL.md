---
name: voice-matching
description: |
  当用户询问"如何让去痕后的文本更像自己写的"、"如何匹配作者风格"或"如何保持个人写作特色"时调用此 skill。不适用于：技术文档、中立参考文本、不需要个性化风格的场景。关键 trigger 信号：声音匹配、作者风格、写作样本、rhythm、word choice、personal style。
source_book: Humanizer Blader
source_chapter: Usage section / voice matching example
tags: [voice-matching, style-preservation, personal-writing, writing-sample]
related_skills: ["preserve-style", "two-pass-rewriting"]
---

# SKILL.md - Voice Matching（声音匹配）

## R (Reading) - 原文引用

> "If you provide a writing sample, Humanizer follows that sample instead of its default style rules."
> 
> "Humanizer follows the sample's rhythm, word choice, punctuation, and deliberate quirks."

## I (Interpretation) - 方法论骨架

**核心思想**：如果提供写作样本，Humanizer 遵循该样本的节奏、用词、标点和刻意怪癖，而不是其默认样式规则。这种"声音匹配"功能让去痕后的文本更贴近作者的真实风格。

**关键要素**：
1. **Writing Sample**: 用户提供 2-3 段自己的写作作为样本
2. **Rhythm**: 跟随样本的节奏（句子长度、段落结构）
3. **Word Choice**: 跟随样本的用词偏好
4. **Punctuation**: 跟随样本的标点习惯
5. **Deliberate Quirks**: 跟随样本的刻意怪癖（如特定的表达方式）

## A1 (Past Application) - 书中作者用过的案例

README 中提供了声音匹配的使用示例：
```
/humanizer

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now humanize this text:
[paste AI text to humanize]
```

Humanizer 会分析样本的节奏、用词、标点和刻意怪癖，然后在去痕时遵循这些特征，而不是使用默认样式规则。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户想让去痕后的文本更像自己写的
- 用户想保持个人写作特色
- 用户有现成的写作样本可以提供
- 用户对默认样式规则不满意

**与相邻 skill 的区分**：
- 与 `preserve-style` 的区别：voice-matching 是**主动提供写作样本来匹配风格**，而 preserve-style 是**被动保持作者风格**（个人写作保持风格，技术文本保持中立）。前者更主动，后者更被动。
- 与 `two-pass-rewriting` 的区别：voice-matching 关注**风格匹配**，而 two-pass-rewriting 关注**去痕流程**。前者是风格调整，后者是质量控制。

## E (Execution) - 可执行步骤

1. **准备写作样本**
   - 选择 2-3 段自己的写作作为样本
   - 确保样本代表自己的真实风格
   - 样本应包含不同的句子结构和用词

2. **提供样本给 Humanizer**
   - 在 `/humanizer` 命令后粘贴样本
   - 明确说明这是用于声音匹配的样本
   - 然后粘贴需要去痕的 AI 文本

3. **验证匹配效果**
   - 检查第一次重写结果是否匹配自己的风格
   - 如果不满意，提供更详细的样本或反馈
   - 确认最终版本符合自己的期望

4. **迭代优化**
   - 根据反馈调整样本选择
   - 尝试不同的样本组合
   - 找到最佳的声音匹配效果

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 技术文档（需要保持中立和平淡）
- 中立参考文本（不需要个性化风格）
- 用户没有现成的写作样本
- 用户希望使用默认样式规则

**作者的盲点**：
- Blader 假设所有用户都有现成的写作样本，但实际上某些用户可能没有
- humanizer 缺少对样本质量的评估机制（样本是否足够代表性）
- 没有提到如何处理样本与 AI 文本风格差异过大的情况
