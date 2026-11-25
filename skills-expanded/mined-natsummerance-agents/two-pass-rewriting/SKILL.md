---
name: two-pass-rewriting
description: |
  当用户询问"如何确保去痕质量"、"去痕流程是什么"或"如何看到中间结果"时调用此 skill。不适用于：一次性快速去痕、不需要透明化的场景。关键 trigger 信号：去痕流程、两遍重写、first rewrite、critique、显示工作过程、透明化。
source_book: Humanizer Blader
source_chapter: Introduction / workflow description
tags: [rewriting-process, two-pass, transparency, quality-assurance]
related_skills: ["pattern-based-detection", "show-your-work"]
---

# SKILL.md - Two-Pass Rewriting（两遍重写流程）

## R (Reading) - 原文引用

> "It makes a first pass without treating the original structure as fixed. Then it checks the draft against those patterns and the original claims before rewriting whatever still needs work."
> 
> "When you paste text, Humanizer shows its work before giving you the final version. You see the first rewrite and a short critique of anything that still sounds artificial."

## I (Interpretation) - 方法论骨架

**核心思想**：先进行第一次重写（不将原始结构视为固定），然后对照模式和原始声明检查草稿，最后重写仍需改进的部分。这种"先重写再批评"的流程确保最终输出质量，同时让用户看到工作过程。

**关键要素**：
1. **First Pass**: 第一次重写，不将原始结构视为固定
2. **Check Against Patterns**: 对照 35 个模式和原始声明检查草稿
3. **Critique**: 对仍听起来人工的内容进行简短批评
4. **Final Rewrite**: 重写仍需改进的部分

## A1 (Past Application) - 书中作者用过的案例

Humanizer 的工作流程就是典型的两遍重写：
1. 用户粘贴文本
2. Humanizer 进行第一次重写
3. 显示第一次重写结果和对仍听起来人工的内容的简短批评
4. 用户可以看到中间结果并提出反馈
5. Humanizer 进行最终重写并给出最终版本

这种流程确保了去痕质量的透明化和可解释性。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户想知道如何确保去痕质量
- 用户想了解去痕的完整流程
- 用户想看到中间结果并提出反馈
- 用户想建立透明化的去痕工作流

**与相邻 skill 的区分**：
- 与 `pattern-based-detection` 的区别：two-pass-rewriting 关注**去痕流程**，而 pattern-based-detection 关注**AI 痕迹识别**。前者是执行阶段，后者是检测阶段。
- 与 `show-your-work` 的区别：two-pass-rewriting 是**具体的两遍重写机制**，而 show-your-work 是**更广泛的透明化原则**。前者是后者的具体实现。

## E (Execution) - 可执行步骤

1. **第一次重写**
   - 不将原始结构视为固定
   - 应用 35 个模式进行初步去痕
   - 生成第一次重写结果

2. **对照检查**
   - 对照 35 个模式检查草稿
   - 对照原始声明检查事实准确性
   - 识别仍需改进的部分

3. **生成批评**
   - 对仍听起来人工的内容进行简短批评
   - 指出具体的问题和改进建议
   - 展示给用户等待反馈

4. **最终重写**
   - 根据批评和用户反馈进行最终重写
   - 确保所有 AI 痕迹已移除
   - 保持事实准确性和作者风格

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 一次性快速去痕（不需要中间结果）
- 不需要透明化的场景（用户只关心最终结果）
- 实时去痕需求（没有时间进行两遍流程）

**作者的盲点**：
- Blader 假设所有用户都想看到中间结果，但实际上某些用户可能只需要最终版本
- humanizer 缺少对跳过第一遍直接生成最终版本的选项
- 没有提到如何配置批评的详细程度
