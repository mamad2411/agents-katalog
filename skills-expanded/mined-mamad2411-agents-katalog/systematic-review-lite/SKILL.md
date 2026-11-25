---
name: systematic-review-lite
description: 轻量系统综述与文献筛选工作流：纳入/排除标准、题录筛选记录、PRISMA 流程意图与检查项摘要。与 literature（写作与引用）互补；不替代正式 PRISMA 全文指南。适用于「系统综述」「PRISMA」「纳入排除」「筛选流程图」等场景。
---

# 系统综述与筛选（轻量）

## 与 `literature` 的分工

| 能力 | 使用技能 |
|------|----------|
| 多库导出、合并题录、去重、综述段落、`\cite`、BibTeX | `literature` |
| **研究问题、PICO/PCC、纳入排除标准、筛选阶段计数、PRISMA 检查清单、筛选日志** | **本技能（systematic-review-lite）** |

执行写作类任务前，若用户需要「可重复报告」的筛选过程，先读本技能再衔接 `literature`。

## 何时使用

- 用户提到系统综述、PRISMA、纳入/排除标准、标题摘要筛选、全文筛选、研究空白（gap）。
- 需要说明「检索到多少条、剔除多少条、最终纳入多少条」并绘制或描述 PRISMA 式流程图（可配合 `svg-flowchart` 生成 SVG）。

## 工作流程（建议）

1. **明确综述类型与问题**：范围综述 / 系统综述 / 映射研究等；用 PICO（或人文社科变体）写清问题。
2. **撰写纳入与排除标准**：人群、干预/暴露、结局、研究设计、语言、时间窗等；见 [references/screening-log-template.md](references/screening-log-template.md)。
3. **记录检索与导出**：数据库名、检索式、日期、导出条数；题录合并与去重见 `literature` 的 [multi-source-retrieval.md](../literature/references/multi-source-retrieval.md)。
4. **分阶段筛选**：标题摘要 → 全文 → 数据提取；每阶段记录**纳入 / 排除**人数及**排除原因**（编码）。
5. **PRISMA 对齐**：按 [references/prisma-checklist.md](references/prisma-checklist.md) 自查；正文或附录中报告各阶段数量。
6. **流程图**：手绘或借助 `svg-flowchart` 绘制 PRISMA 2020 结构意图图；正式投稿以目标期刊模板为准。

## 参考文档

- [references/prisma-checklist.md](references/prisma-checklist.md)：PRISMA 2020 相关检查项摘要（非全文替代）
- [references/screening-log-template.md](references/screening-log-template.md)：筛选日志与排除原因编码模板

## 重要声明

- 本技能提供**方法学骨架与记录模板**，不能替代领域专家、图书管理员或伦理审查。
- 完整 PRISMA 说明见 [PRISMA 官方网站](http://www.prisma-statement.org/) 及期刊要求；引用指南时以官方版本为准。
