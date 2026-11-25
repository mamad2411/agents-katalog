---
name: wiki-core
description: Core operating rules for the student knowledge wiki. This skill should be used whenever working inside an Obsidian vault that contains a wiki/ folder with hot.md, or when the user mentions ingest, lint, review, exam-prep, or asks to build/maintain their course knowledge base. Loads the three-layer architecture, token budget rules, and bilingual page formats. Always loads first.
---

# Student LLM Wiki — Core

你是学生知识库维护者。读 `raw/`，写 `wiki/`。永不改 `raw/`。
You maintain a student knowledge wiki. Read `raw/`, write `wiki/`. Never modify `raw/`.

## 三层架构 Architecture

```
raw/{course}/    ← Layer 1: 只读课件 Read-only slides
wiki/            ← Layer 2: 你维护的知识 Knowledge you maintain
  hot.md         ←   上下文缓存(≤500词) Context cache, READ FIRST
  index.md       ←   总目录 Master catalog
  overview.md    ←   跨课程综述 Cross-course synthesis
  log.md         ←   操作日志(追加) Append-only log
  courses/       ←   课程MOC
  concepts/      ←   概念页(核心) Concept pages
  sources/       ←   来源页
  exam-prep/     ←   练习题
raw/.manifest.json  ← 去重追踪 Dedup tracker
(这些skill是 Layer 3 — 操作规则)
```

## Token预算规则（最高优先级 TOP PRIORITY）

违反这些规则会浪费用户额度。它们高于所有其他规则。
Violating these wastes the user's quota. They override all other rules.

1. **每次session首先只读 `wiki/hot.md`**（≤500词）。若含所需上下文，不再读其他页
2. **需要更多上下文才读 `wiki/index.md`**，从中定位页面
3. **每次ingest最多读3-5个已有页面**。超过5个=读得太广
4. **局部编辑，不全文重写**。改一个字段不要重写整页
5. **wiki页面100-300行**。超300行拆分
6. **批量操作时 index/hot/log 最后更新一次**，不是每源更新一次

## 语言 Language

中英双语。标题"中文 English"。`[[链接]]` 用英文+连字符（如 `[[Gradient-Descent]]`）。

## 概念页格式 Concept Page Format

文件: `wiki/concepts/{English-Name}.md`
```yaml
---
tags: [concept, {domain}]
courses: [COMP6713]
confidence: low|medium|high
last_reviewed: YYYY-MM-DD
created_at: YYYY-MM-DD
---
```
章节: 直觉 Intuition（费曼风格）→ 详细解释 Detailed → [图解 Diagram，可选，见 wiki-diagram skill] → 为什么重要 Why → 连接 Connections（含跨课程）→ 来源 Sources → 待解决 Open Questions

## 课程总览页格式 Course Overview Format

文件: `wiki/courses/{COURSE}-overview.md`，frontmatter: `tags: [course-overview, {course-code}]` + `course: {COURSE-CODE}` + `updated: YYYY-MM-DD`
章节: 综述 Summary（一句话）→ 概念图谱 Concept Map（`[[链接]]` 列表）→ 薄弱环节（Dataview: confidence=low）→ 来源（Dataview: sources by course tag）

## 来源页格式 Source Page

文件: `wiki/sources/{name}.md`
```yaml
---
tags: [source, {course-code}]
course: {COURSE-CODE}
ingested: YYYY-MM-DD
source_file: raw/{course}/{filename}
---
```
章节: 关键要点(3-5) → 图表描述(标注是否建议用 Mermaid 重绘，见 wiki-diagram skill) → 新概念列表 → 更新了哪些页面

## Hot Cache 内容

每次操作完更新 `wiki/hot.md`（≤500词）：最近3个来源 / 最近概念 / 当前薄弱概念 / 待办

## 域规则 Domain Rules

- 数学: LaTeX + 直觉解释每个符号
- 安全 COMP4337: 攻防配对，lab验证标 ✅
- ML COMP9417: 适用场景 + 对比 + bias-variance特性
- NLP COMP6713: 架构描述 + 预训练/微调/推理区分
- 分析 INFS5730: SAS VTA步骤 + 数据类型

## 绝对规则 Hard Rules

1. 永不改 raw/
2. 一概念一页，费曼风格
3. 跨课程连接是最大价值
4. 不确定标 confidence:low
5. Token预算规则高于一切
