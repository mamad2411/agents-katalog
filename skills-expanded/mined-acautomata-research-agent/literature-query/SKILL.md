---
name: literature-query
description: Query and compare literature across wiki papers — runs the curate predicate. Triggers: 文献查询, 文献检索, 对比论文, 跨论文比较, wiki里有没有, literature query, compare papers, cross-paper.
---

# literature-query — 文献查询与跨论文比较

在 wiki 现有内容上做文献查询和跨论文比较。

## 编排

1. **`curate`** — Wiki 策展、跨论文比较、文献查询（lint / compare / query 模式）。

### Pre-check（main 检索）

用 `wiki_get` 读 wiki 索引定位相关页面，提取关键事实。Wiki 不足时用 browser 补充（arXiv、Scholar），标注来源。

### 运行 curate

在指定范围内执行查询（`query_type: lint | compare | query`）。把目标论文/关键词、wiki 路径、用户原始问题、已读关键事实、网络补充来源传给 `curate`。产出引用 `page_id`、标注 `evidence_level`、矛盾明确标出。

### 完成后

向用户呈现结果，附 page paths 和 `evidence_level` 标签。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| query | 是 | 自然语言问题或比较请求 |
| papers | 否 | 论文标题、wiki 路径或关键词 |
| dimensions | 否 | 比较轴：methods, datasets, metrics, results |

## 输出

- **query**：结构化回答，带引用、证据等级、缺口
- **compare**：对齐表格，每行带 `evidence_level`，矛盾标记
- **lint**：Wiki 质量问题 dashboard，按类型分组，带修复建议

各模式的产出结构以 `curate` predicate 的 `## 查询模式` table 为单一权威来源；若此处的表述与 curate 不一致，以 curate 为准。
