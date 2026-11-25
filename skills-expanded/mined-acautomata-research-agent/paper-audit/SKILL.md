---
name: paper-audit
description: Quality-gate audit of a paper's analysis outputs (extract/critic/design/spec) — runs the audit predicate. Triggers: 质量审计, paper-audit, 审计产出, 流水线审计, 检查这些产出.
---

# paper-audit — 分析链质量审计

对一段论文分析链的产出做只读质量门审计（结构、阶段边界、跨阶段一致性）。

## 编排

1. **`audit`** — 对 extract/critic/design/spec 产出做只读审计（6 维度：结构完整性、字段覆盖、阶段边界、缺失信息标注、证据强度分级、跨阶段一致性），审计报告备好 md 经 `ingest` 写入 wiki。

### Pre-check

确认 wiki 里有待审计产出（至少 `extract`；critic/design/spec 视链长度）。用 `wiki_search` 定位。

### 完成后

呈现：必须修复项（阻塞下游）、建议改进项、总体可用性结论，附 wiki 路径。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| 论文（wiki page） | 是 | 待审计产出的论文 |
| 审计范围 | 否 | 默认全部已有阶段；可指定子集 |
