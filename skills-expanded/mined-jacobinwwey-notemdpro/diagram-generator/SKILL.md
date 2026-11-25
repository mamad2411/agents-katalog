---
name: diagram-generator
description: Generate source-grounded diagrams with explicit relationships and capability-checked exports.
---

# Diagram generator

## English

Canonical action: `generate-diagram`; accept `generate-experimental-diagram` as an alias. `preview-diagram` requires an available host renderer.

1. Read the full authorized source. Identify required concepts, source references, ownership hierarchy and explicit directed predicates. Keep a coverage inventory.
2. Select an available target. Mermaid text is supported by the bundled validator; Drawnix, SVG and PDF need an actual host adapter. Never claim an unavailable format was exported.
3. Keep hierarchy separate from cross-branch relationships. Preserve all required nodes and source-supported relations, including reciprocal and distinct predicates. Do not invent edges merely to connect isolated concepts.
4. Prefer deterministic renderer placement: closely related blocks should be nearer; route from boundaries, reserve label space and reduce crossings/overlap. Never delete content to improve geometry. Revalidate coverage after any reorder.
5. Validate canonical source before preview/export. For a host SVG-to-PDF path, require sanitized SVG, resolved style/inheritance support, valid dimensions/viewBox, proportional page-size limits and a nonempty parseable PDF. Preserve source plus intermediate artifacts and report the failing stage when unsupported or unsuccessful.

Use [workflow-runner](../workflow-runner/SKILL.md) for complete diagnostics. A successful text generation does not establish rendered export success.

## 中文

规范操作名为 `generate-diagram`，接受 `generate-experimental-diagram` 兼容别名。`preview-diagram` 需要实际可用的宿主渲染器。

1. 阅读完整的已授权来源，整理必要概念、来源引用、归属层级和显式有向谓词，保留覆盖清单。
2. 选择可用目标。随附验证器支持 Mermaid 文本；Drawnix、SVG 和 PDF 需要真实宿主适配器，不得把不可用格式报告为已导出。
3. 分离层级与跨分支关系，保留全部必要节点及来源支持的关系，包括反向关系和不同谓词。不得为了连接孤立概念而虚构连线。
4. 优先使用确定性渲染排布：紧密关联块相邻，连接节点边界，预留标签空间，减少交叉与重叠。不得删除内容改善几何效果；重排后重新验证覆盖。
5. 预览/导出前验证规范源。宿主 SVG 到 PDF 路径应支持净化、样式/继承解析、有效尺寸/viewBox、等比例页面尺寸限制，以及非空且可解析的 PDF。保留源与中间产物，能力不支持或失败时报告具体阶段。

完整诊断遵循 [workflow-runner](../workflow-runner/SKILL.md)。文本生成成功不代表渲染导出成功。
