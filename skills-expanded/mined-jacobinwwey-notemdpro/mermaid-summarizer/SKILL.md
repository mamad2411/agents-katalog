---
name: mermaid-summarizer
description: Summarize a source document as a valid Mermaid hierarchy without losing required concepts.
---

# Mermaid summarizer

## English

Read the complete authorized document and identify its core concepts and ownership hierarchy. Use a Mermaid mindmap for a genuine hierarchy; use [diagram-generator](../diagram-generator/SKILL.md) when explicit cross-branch relations need a different diagram family.

Generate a single fenced Mermaid block with a `mindmap` declaration and consistent indentation. Parentheses are valid shape syntax: a root may be `root(("Title"))`. Preserve labels and required concepts; do not delete punctuation or relationships merely to pass parsing. Track any deliberate summarization separately from syntax repair.

Validate with [mermaid-healer](../mermaid-healer/SKILL.md). Keep the original output if an unknown family or ambiguous incomplete block needs review. Report source coverage and unresolved errors through [workflow-runner](../workflow-runner/SKILL.md). Successful Mermaid text generation does not prove that a host rendered or exported it.

## 中文

阅读完整的已授权文档，确定核心概念及归属层级。真正的层级适合 Mermaid mindmap；跨分支的显式关系需要其他图形类型时，使用 [diagram-generator](../diagram-generator/SKILL.md)。

生成单个 Mermaid 围栏代码块，包含 `mindmap` 声明并使用一致缩进。圆括号是有效形状语法，根节点可以写作 `root(("Title"))`。保留标签及必要概念，不得为了通过解析而删除标点或关系。将有意的内容摘要与语法修复分别记录。

使用 [mermaid-healer](../mermaid-healer/SKILL.md) 验证。遇到未知类型或含义不明确的未闭合代码块时，保留原输出供审阅。通过 [workflow-runner](../workflow-runner/SKILL.md) 报告来源覆盖和未解决错误。Mermaid 文本生成成功不代表宿主已完成渲染或导出。
