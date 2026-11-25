---
name: curate
description: Curate the research wiki — lint, compare papers, answer literature queries. Triggers: wiki lint, wiki 质量检查, wiki 策展, curate, wiki 维护.
---

# curate — wiki 策展、质量 lint、跨论文比较、文献查询

## Mission

让研究 wiki 保持高质量：识别矛盾、缺口、过时页面、孤立节点；基于现有 wiki 内容执行跨论文比较和文献查询。不摄入新论文，不执行原始研究。

## When to use

- 用户问"wiki 里有没有 X""对比这几篇论文""查一下某篇论文"
- 需要 wiki 质量检查 / lint dashboard
- 跨论文方法、数据集、指标比较

不要用于：摄入新论文（那是 `ingest`）、实验深度提取（`extract`）、问题分析（`critic`）。

## 核心原则

- 只读现有 wiki（可写回修复 metadata），不修改 `raw/` 原始文件
- 每次 lint / compare / query 必须引用具体页面 ID 或路径
- 区分 `evidence_level`：abstract-only / skimmed / full-paper / reproduced
- 矛盾和不兼容明确记录，不擦除旧 claim
- 数量化：具体数字优于定性描述
- 中文呈现，保留原始标题、DOI、arXiv、代码链接原文

## 职责边界

**做：**

- 跑 wiki lint 并整理 dashboard
- 通过 `wiki_apply` 修复 metadata 缺失、补全 `evidence_level`、修正 frontmatter（**已有页面的窄更新**）
- 跨论文方法 / 数据集 / 基准比较，生成对比表
- 文献查询：基于 wiki 现有内容回答问题，标注引用
- 识别孤立页面、孤儿节点、过时 superseded 页面
- 建议页面合并、拆分、重命名（不直接执行破坏性操作）

**新建持久页面**：当 compare / query 产出**新的持久比较页或分析页**时，不用 `wiki_apply` 建整页——备好该页 md 写到 `raw/sources/<slug>.md`，交 `ingest`（`page_type`: 比较页 `comparison`、分析页 `analysis`）统一写入。

**不做：**

- 摄入新论文 / 提取 PDF 全文（那是 `ingest`）
- 实验提取 / 问题分析 / 验证设计 / idea 生成（那是 `extract`/`critic`/`design`/`ideate`）

## Lint 检查项

每次 lint 覆盖：缺 `evidence_level` 的论文页、缺 frontmatter 必填字段、无 paper page 的 raw source、孤立页面（无入站链接）、矛盾 claim、过时 superseded 页面、重复或错放的页面、跨领域错位。

## 查询模式

| 模式 | 产出 |
|------|------|
| `lint` | Wiki 质量问题 dashboard，按类型分组，带修复建议 |
| `compare` | 对齐表格（方法/数据集/指标/结果），每行带 `evidence_level`，矛盾标记 |
| `query` | 结构化回答，带引用、证据等级、识别的缺口 |

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| `query` | 是（query/compare） | 自然语言问题或比较请求 |
| `papers` | 否 | 论文标题、wiki 路径或关键词 |
| `dimensions` | 否（compare） | 比较轴：methods, datasets, metrics, results |

Wiki 不足时可用 browser 补充（arXiv、Scholar），但标注来源与 `evidence_level`。

## 完成门禁

- 每条结论引用 `page_id` 或路径，标注 `evidence_level`
- 矛盾点明确标出，不擦除旧 claim

按分支的可验证标准：

- `lint`：输出 dashboard，列出每类问题的数量和修复优先级；未修复项必须附 reason
- `compare`：表格每行必须包含 method / dataset / metric / result 四列；矛盾单元格以 ⚠️ 加粗标记；未覆盖维度注明 absence
- `query`：回答必须包含 cited `page_id` 列表 + `evidence_level` 分布摘要；明确列举 1–3 个已识别缺口（哪怕结论是"无缺口"）
