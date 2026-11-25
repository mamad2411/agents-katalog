---
name: ingest
description: Unified wiki write entry — ingest a paper PDF into an evidence-traceable paper page, OR write an already-prepared markdown file into the wiki. Triggers: 入库, ingest paper, add to wiki, 写入 wiki, 把这份文档入库, 存进 wiki.
argument-hint: <pdf-path-or-url> | <md-file-path>
---

# ingest — 统一 wiki 写入口（隔离 subagent + 官方流水线）

## Mission

把所有准备好的内容统一写入 wiki，确保每条持久 claim 可追溯到来源。这是研究 wiki 的唯一整页写入口，支持两个分支：

- **PDF 入库分支**：研究论文 PDF → 符合 wiki 规范的 11 节结构化论文页（证据可追溯）。
- **md 写入分支**：把一份已准备好的 markdown 文件（分析文档、比较页、idea card 等）写入 wiki。

**始终以隔离 subagent 运行**：本 predicate 声明它始终在隔离 subagent（spawn self）内执行——**所有写入分支都隔离**。无论由单篇 `ingest`、`paper-ingest`、`paper-read`、`paper-batch-ingest` 触发，还是由 `extract`/`critic`/`design`/`spec`/`audit`/`ideate` 备好 md 后调用，main 一律 spawn 一个 isolated subagent 跑本 skill —— PDF 全文与 md 内容都永不进 main context。隔离语义由本 predicate 自带，orchestrator 与调用方自动继承，无需各自声明。**每次写入 spawn 一个隔离 subagent**，不做批量复用。

## 前置条件

- 依赖 **memory-wiki 插件已启用**。`openclaw wiki` CLI（`wiki ingest` / `wiki compile` / `wiki lint`）与 `wiki_apply` / `wiki_lint` / `wiki_search` / `wiki_get` 工具由该插件提供，默认可能未启用；未启用时本 skill 的入库步骤不可用。启用插件 / 改 `openclaw.json` 属独立 runtime 配置变更（需重启 gateway），不在本 skill 职责内。

## When to use

- 新论文 PDF 需要加入 wiki（PDF 入库分支）
- 用户请求"入库这篇论文""加入 wiki""整理这篇论文"
- `raw/inbox/` 中有待处理的论文
- 其它 predicate 已备好一份 md，需要写入 wiki（md 写入分支）——`extract`/`critic`/`design`/`spec`/`audit`/`ideate`/`curate` 等产出整页时统一经本 skill 写入

不要用于：文献查询、跨论文比较、wiki 质量审计（那是 `curate`）；对已有页面的窄更新（直接 `wiki_apply`，不经本 skill）。

## 核心原则

- Raw sources 不可变；不修改 `raw/` 下原始文件
- Wiki 受证据约束，不发明不存在的知识；每条持久 claim 追溯到论文页章节和原始来源
- 走官方 memory-wiki 流水线建页，不做 freeform page surgery

## 语言

- Wiki 正文中文；论文元数据（标题/作者/DOI/arXiv/代码链接）保留原文。

## 职责边界

**做（PDF 入库分支）：**

- 捕获 raw source（PDF），规范命名移入 `raw/sources/`（不可变保留）
- 提取全文，仅作撰写页面的工作材料（不入库、不灌满 vault）
- 组装 11 节论文页 md，staged 到 `raw/sources/<slug>.md`
- 经官方流水线入库：`openclaw wiki ingest <staged md>` → `openclaw wiki compile`
- 跑 `wiki_lint` 校验；成功后删除 staged md，返回 wiki 路径 + `evidence_level`
- 更新 wiki 索引和日志（窄更新，经 `wiki_apply`）

**做（md 写入分支）：**

- 接收一份已备好的 md（`raw/sources/<slug>.md`，由调用方 staged）
- 按 `page_type` 校验 frontmatter 与结构；缺失必填 frontmatter 时补齐或返回具体缺失项
- 经官方流水线入库：`openclaw wiki ingest <md>` → `openclaw wiki compile`
- 跑 `wiki_lint` 校验；成功后删除 staged md，返回 wiki 路径
- 更新 wiki 索引和日志（窄更新，经 `wiki_apply`）

**不做：**

- 不回答文献查询 / 跨论文比较 / wiki 质量 lint（那是 `curate`）
- 不做实验深度提取（那是 `extract`）、问题分析（`critic`）、验证设计（`design`）——这些 predicate 备好 md 后交本 skill 写入
- **所有整页写入统一经本 skill 的官方流水线**；本 skill 与调用方都**不用 `wiki_apply` 从零建整页**——那是 freeform page surgery，违背官方定位。`wiki_apply` 仅用于对已有页面的窄更新（synthesis/metadata）与 index/log 更新

## 输入

两个分支二选一（`pdf_path` 与 `md_path` 至少其一）：

| Field | Required | Description |
|-------|----------|-------------|
| `pdf_path` | PDF 分支必填 | 源 PDF 路径（`raw/inbox/` 或 `raw/sources/`）或可访问 URL |
| `md_path` | md 分支必填 | 已备好的 md 文件路径（调用方 staged 到 `raw/sources/<slug>.md`） |
| `page_type` | md 分支必填 | 页面类型（`paper` / `analysis` / `comparison` / `idea-card`），对应 `references/page-templates.md` 的同名页面结构，决定 frontmatter 与模板校验；由产出该 md 的 predicate 指定 |
| `target_domain` | 推荐 | 论文/页面所属领域子树 |
| `evidence_level` | 否（PDF 分支） | 基于 PDF 访问程度（全文提取成功默认 `full-paper`）|

## 执行流程

按分支选择流程：**PDF 入库分支**走 Capture → Extract → Create → Ingest → Verify；**md 写入分支**跳过 Capture/Extract/Create，直接 Validate → Ingest → Verify。

### PDF 入库分支

#### 1. Capture
捕获 raw source，规范命名移入 `raw/sources/`（PDF 不可变保留，供溯源与重放入库）。验证文件存在、可读、非空。失败重试一次。

#### 2. Extract
提取全文。**仅作撰写页面的工作材料**——不入库、不作为持久页面内容。验证文本长度足够、包含论文结构。失败尝试替代方法一次。

#### 3. Create（组装 + staged）
按论文页模板（见 `references/page-templates.md`）组装 11 节论文页 markdown，staged 到 `raw/sources/<slug>.md`，供 `wiki ingest` 消费。填写全部通用 frontmatter 与论文专属 frontmatter（`paper.*`、`classification.*`、`evidence_level`）。包含全部 11 节：Citation, One-Sentence Contribution, Problem Setting, Method, Experiments, Results, Limitations, Reusable Claims, Connections, Open Questions, Provenance。

### md 写入分支

#### 1. Validate（校验已备 md）
读取 `md_path` 指向的已备 md（调用方 staged 到 `raw/sources/<slug>.md`）。验证文件存在、可读、非空；按 `page_type` 校验 frontmatter 必填字段（见 `references/page-templates.md` 的通用 + 对应类型 frontmatter）与结构完整。缺失必填 frontmatter 时补齐或返回具体缺失项。**不改正文内容**——内容由产出它的 predicate 负责。

### 共用：Ingest（官方流水线建页）
`openclaw wiki ingest raw/sources/<slug>.md` 然后 `openclaw wiki compile`，使新页面对 `wiki_search` / `wiki_get` 可见。**这是唯一建页路径**；不经 `wiki_apply` 建页。

### 重入库分支（更新已存在页面）

若 `wiki_search` 发现该页已存在，改为对该页做窄更新（synthesis/metadata），经 `wiki_apply`，**不建重复页**。仅在此分支使用 `wiki_apply`。

### 共用：Verify
跑 `wiki_lint`（结构、provenance gaps、矛盾、open questions）。成功后**删除 staged md**（`raw/sources/<slug>.md`）——wiki 是页面唯一持久副本；PDF 与提取文本按不可变 raw 原则保留（md 写入分支无 PDF，staged md 删除即可）。PDF 分支返回 wiki 路径 + `evidence_level`；md 分支返回 wiki 路径；失败返回具体原因（PDF 不可读、提取失败、frontmatter 缺失、lint 阻塞等）。

### 更新索引与日志
入库成功后，用 `wiki_apply` 对 wiki index 与 log 做追加式窄更新（见 `references/wiki-conventions.md` 的 index/log 规则）。

## 完成门禁

**PDF 入库分支：**

- 一个 raw source（PDF）已捕获且不可变保留；一份全文已提取（仅作工作材料）
- 一个论文页已经官方流水线入库（`wiki ingest` + `wiki compile`），对 `wiki_search`/`wiki_get` 可见
- 页面符合论文模板（**>= 100 行**、有 `evidence_level`、Results 为每个 main claim 包含具体数字，无"显著优于 baseline"类定性表述）
- `wiki_lint` 通过；staged md 已删除
- 重入库走 `wiki_apply` 窄更新，未产生重复页
- Wiki 索引和日志已更新
- 返回 wiki 路径 + `evidence_level`（成功）或具体原因（失败）

**md 写入分支：**

- 已备 md 经校验（frontmatter 与结构符合 `page_type`），缺项已补齐或已返回具体缺失
- 页面已经官方流水线入库（`wiki ingest` + `wiki compile`），对 `wiki_search`/`wiki_get` 可见
- `wiki_lint` 通过；staged md 已删除
- 已存在页面走 `wiki_apply` 窄更新，未产生重复页
- Wiki 索引和日志已更新
- 返回 wiki 路径（成功）或具体原因（失败）

## 质量规则

遵循 `references/wiki-conventions.md` 的命名、索引、日志、链接规范。此外：

- 不编造 claim——每条 claim 追溯到论文页章节
- Experiments 必须包含数据集大小、baseline 名称、训练设置（架构/backbone/优化器/lr/batch/epoch/硬件）、评估协议、消融
- Results 必须为每个 main claim 包含具体数字（如 "AUROC 95.12% vs. MCM 86.05%"，不用"显著优于 baseline"）
- 缺失信息标注"原文未报告"
- 更新已有页面优先于创建重复页面
