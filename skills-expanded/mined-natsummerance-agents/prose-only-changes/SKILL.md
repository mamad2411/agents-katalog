---
name: prose-only-changes
description: |
  当用户询问"去痕是否会破坏文件结构"、"代码和数据是否安全"或"如何只修改散文部分"时调用此 skill。不适用于：纯文本文件、不需要保留结构的场景、用户希望全面重写的场景。关键 trigger 信号：只修改散文、保留代码、保留数据、frontmatter、link targets、文件结构安全。
source_book: Humanizer Blader
source_project: blader/humanizer
source_chapter: Usage section / file humanization
tags: [prose-only, file-safety, code-preservation, data-preservation]
related_skills: ["no-fabrication", "preserve-style"]
---

# SKILL.md - Prose-Only Changes（只修改散文）

## R (Reading) - 原文引用

> "Point it at a file and it changes only the prose, leaving code, data, frontmatter, and link targets alone."

## I (Interpretation) - 方法论骨架

**核心思想**：指向文件时，Humanizer 只更改散文，保留代码、数据、frontmatter 和链接目标。这种"精准修改"原则确保不会意外破坏文件的结构或功能。

**关键要素**：
1. **Only Prose**: 只修改散文部分（自然语言文本）
2. **Leave Code Alone**: 保留代码块不变
3. **Leave Data Alone**: 保留数据部分不变
4. **Leave Frontmatter Alone**: 保留 frontmatter（如 YAML frontmatter）不变
5. **Leave Link Targets Alone**: 保留链接目标（URL）不变

## A1 (Past Application) - 书中作者用过的案例

README 中明确说明了 Humanizer 在处理文件时的行为：
- 如果指向 `docs/launch-post.md`，Humanizer 只会修改其中的散文部分
- 代码块（如 ```python ... ```）保持不变
- 数据部分（如表格、JSON）保持不变
- Frontmatter（如 `--- title: ... ---`）保持不变
- 链接目标（如 `[link](https://example.com)` 中的 URL）保持不变

这种设计确保了去痕不会影响文件的功能性内容，只优化可读性部分。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户担心去痕会破坏文件结构
- 用户想了解代码和数据是否安全
- 用户想只修改散文部分而不影响其他内容
- 用户处理包含混合内容的文件（如 Markdown 文件包含代码、数据、链接）

**与相邻 skill 的区分**：
- 与 `no-fabrication` 的区别：prose-only-changes 关注**文件结构安全**，而 no-fabrication 关注**事实准确性**。前者是结构保障，后者是内容保障。
- 与 `preserve-style` 的区别：prose-only-changes 关注**只修改散文**，而 preserve-style 关注**保持作者风格**。前者是范围限制，后者是风格调整。

## E (Execution) - 可执行步骤

1. **识别文件类型**
   - 确认文件是否包含混合内容（散文 + 代码 + 数据 + frontmatter + 链接）
   - 常见文件类型：Markdown、Jupyter Notebook、HTML 等
   - 完成标准: 已列出文件包含的内容区块清单（散文/代码/数据/frontmatter/链接）

2. **标记非散文部分**
   - 识别代码块（如 ``` ... ```）
   - 识别数据部分（如表格、JSON、CSV）
   - 识别 frontmatter（如 `--- ... ---`）
   - 识别链接目标（如 `[text](url)` 中的 url）
   - 完成标准: 全部代码块、数据、frontmatter、链接目标已在修改前定位并登记

3. **应用去痕到散文部分**
   - 只对自然语言文本应用 35 个模式
   - 跳过所有非散文部分
   - 确保不修改代码、数据、frontmatter、链接目标
   - 完成标准: 改动仅落在散文段落，非散文区域零变更（diff 可证）

4. **验证文件完整性**
   - 检查代码块是否保持不变
   - 检查数据部分是否保持不变
   - 检查 frontmatter 是否保持不变
   - 检查链接目标是否保持不变
   - 完成标准: 四类非散文区块逐一比对通过，文件结构与功能完整性确认

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯文本文件（没有混合内容）
- 不需要保留结构的场景（用户希望全面重写）
- 用户明确要求修改代码注释或其他非散文部分
- 快速原型验证（不需要精细范围控制）

**作者的盲点**：
- Blader 假设所有文件都有清晰的"散文"和"非散文"边界，但实际上某些文件可能边界模糊（如代码注释中的自然语言）
- humanizer 缺少对"散文"的精确定义（什么是散文？代码注释算不算？）
- 没有提到如何处理嵌入式内容（如 HTML 中的 JavaScript）