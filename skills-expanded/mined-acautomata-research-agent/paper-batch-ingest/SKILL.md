---
name: paper-batch-ingest
description: Batch-ingest many papers - trigger the ingest skill once per paper. Triggers: 批量入库, 多篇论文录入, 批量录入论文, batch ingest, ingest multiple papers.
---

# paper-batch-ingest - 多篇论文批量录入

把多篇论文批量录入 wiki。对每篇论文触发一次 `ingest` predicate。隔离语义由 `ingest` predicate 自带（它始终以隔离 subagent 运行，PDF 不进 main context），本 orchestrator 自动继承，**不含任何 spawn 样板**。多篇可并行（受 `maxConcurrent` 限制）。

## 编排

对论文列表中的每篇论文，触发一次 `ingest`（传 `pdf_path` 与 `target_domain`）。`ingest` 自带隔离 subagent 语义，main 触发后由隔离 subagent 实际执行入库并返回 wiki 路径 + `evidence_level`（成功）或具体原因（失败）。

### Pre-check

- 确认论文列表（PDF 路径/URL，每篇一个）。
- 用 `wiki_search` 标记已入库的（默认跳过，除非用户要求重入库）。
- 批量较大时分批触发：同时存活的入库 subagent 受 `maxConcurrent`（默认 8）限制，超过则排队。

### 完成后

汇总每篇结果：

- **成功**：wiki 路径 + `evidence_level`。
- **失败**：论文 + 原因（PDF 不可读、提取失败、lint 阻塞等）。
- **跳过**：已入库且未要求重入库。

失败的列出，可单独重跑该篇 `ingest` 或报告用户。建议下一步：`curate`（lint 模式）批量检查新页面，或 `paper-read` 深读某篇。

## 完成门禁

- 每个输入论文都有且只有一个终态：**成功 / 失败 / 跳过**。
- 每个成功项包含 wiki 路径 + `evidence_level`；每个失败项包含具体原因。
- 已触发的入库全部完成或超时后才汇总，不在部分结果到达时提前结束。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| 论文列表 | 是 | PDF 路径/URL 列表（每篇一行），或一个含论文的目录路径 |
| target_domain | 推荐 | 论文所属领域子树 |
| 重入库已存在 | 否 | 默认跳过已入库；设 true 强制重入库 |
