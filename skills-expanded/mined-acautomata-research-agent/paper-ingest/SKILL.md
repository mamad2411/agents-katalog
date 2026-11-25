---
name: paper-ingest
description: Ingest a paper into the wiki and verify quality (ingest → curate). Triggers: 入库, add to wiki, 文献笔记, 整理这篇论文.
---

# paper-ingest — 论文入库 + 质量校验

入库一篇论文到 wiki 并做质量校验。

## 编排

1. **`ingest`** — PDF → 结构化 wiki 论文页面（证据可追溯），经 `ingest` 统一写入 wiki。
2. **`curate`**（lint 模式）— 对新页面做质量检查：frontmatter、`evidence_level`、Results 具体数字、孤立链接、矛盾、index。

### Pre-check

用 `wiki_search` 检查已有条目（已存在且未要求重入库则跳过）；确认有 PDF 路径或 URL。

### 完成后

- curate 通过：汇报 wiki 路径、`evidence_level`、关键元数据；建议下一步（`paper-read` / `literature-query` / `brainstorm`）。
- curate 发现阻塞问题：汇报问题，不自动重跑 `ingest`。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| PDF path or URL | 是 | 绝对路径或可访问 URL |
| Title | 推荐 | 缺省时从 PDF 提取 |
| User notes | 否 | 关注区域或特殊指令 |
