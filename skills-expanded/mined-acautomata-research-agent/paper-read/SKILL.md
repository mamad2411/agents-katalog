---
name: paper-read
description: Deeply read a paper in one flow — ingest into the wiki, then extract its experiments (ingest → extract). Triggers: 深读论文, 精读这篇, paper-read, deep read.
---

# paper-read — 论文深读（入库 + 实验提取）

一次性深读一篇论文：入库后做深度实验提取。main 是唯一 context，连续传递，无 cross-agent handoff。

## 编排

1. **`ingest`** — PDF → 结构化 wiki 论文页面，经 `ingest` 统一写入 wiki。
2. **`extract`** — 基于 wiki 页面 + 论文原文，产出实验提取文档（备好 md 经 `ingest` 写入 wiki）。文档覆盖主结果、消融、现象、证据充分性四个维度的关键发现，未提供信息一律标注。

### Pre-check

用 `wiki_search` 检查论文是否已入库。已入库且页面完整则跳过 `ingest`，直接 `extract`。

### 完成后

呈现实验提取的关键发现（主结果、消融、现象、证据充分性），附 wiki 路径。建议下一步：`critic`（问题分析）、`paper-validate`（验证设计）。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| PDF path or URL | 是 | 绝对路径或可访问 URL |
| Title | 推荐 | 缺省时从 PDF 提取 |
| Wiki page（已入库时） | 否 | 已有 page 可跳过 `ingest` |
