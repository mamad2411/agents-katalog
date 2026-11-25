---
name: review-profile-training-assets
description: 训练资产生成。用于在基础资料包完成后，按科目特点生成单元总结、易混淆点、引申知识和题型模板，尤其适合数学、离散数学、论文阅读等需要深度训练的资料包。
---

# Review Profile Training Assets

你负责在已有基础资料包上生成“训练资产”。这不是 `/review-init` 的必选阶段，而是资料包已经有 `subject.md`、`knowledge_index.json`、`chapters/`、`exam_points/` 后的增强阶段。

## 核心原则

- 先判断科目的真实训练任务，再决定模板形态。
- 不要把数学模板硬套到所有科目。
- 不要大规模重写基础章节材料，除非用户明确要求。
- 所有写入必须通过 `review_profile_write`，且只能写 draft。
- 如果用户正在修订 active profile，必须先让 `/review-fix` 创建 revision draft，再写入训练资产。

## 输入资料

优先读取：

- `subject.md`：科目目标、考试风格、题型偏好。
- `knowledge_index.json`：章节、知识点、误区、题型建议。
- `chapters/`：定义、推导、案例、证明、代码或论证材料。
- `exam_points/`：考试导向摘要。
- `quality_report.md`：已有缺口和低置信度项。

## 输出目录

根据资料包需要生成以下可选目录：

```text
unit_summaries/
misconceptions/
extensions/
problem_templates/
```

目录职责：

- `unit_summaries/`：每章知识结构、关键链路、复习顺序。
- `misconceptions/`：易混淆点、反例、判断陷阱、常见错误路径。
- `extensions/`：重要引申知识、常见变形、跨章节联系。
- `problem_templates/`：题型或任务模板，用于生成更像真题/训练题的复习问题。

## 题型模板启发式

`problem_templates/` 不是固定表格。每个模板必须说明：

- 这个题型或任务如何识别。
- 适用条件或触发场景。
- 解题步骤、证明路线、分析框架或作答流程。
- 常见变形。
- 易错点或失败模式。
- rubric 或质量判断标准。
- 出题生成启发式。

保留可机器读取 frontmatter：

```markdown
---
id: stable-template-id
name: 模板名称
knowledge_points: [kp_id]
difficulty: M-U
question_styles: [calculation, proof]
status: active
---
```

## 科目适配

- 数学/离散数学：计算、推导、证明、步骤诊断、变式题、反例构造。
- 编程：代码阅读、调试、接口设计、边界条件、复杂度分析。
- 文科/社科：概念辨析、论点重构、材料分析、证据评价。
- 论文阅读：研究问题、方法比较、实验设计、贡献与局限、复现实验检查。
- 语言学习：语境选择、表达替换、语法诊断、翻译与改写。

## 推荐流程

1. 读取目标章节和相关知识点。
2. 判断该章最适合的训练任务。
3. 先生成 `unit_summaries/`，建立知识结构。
4. 再生成 `misconceptions/` 和 `extensions/`。
5. 最后生成 `problem_templates/`。
6. 更新 `quality_report.md`，加入训练资产覆盖情况。

## 质量报告补充项

在 `quality_report.md` 中增加：

```markdown
## 训练资产覆盖

| 章 | 单元总结 | 易混淆点 | 引申知识 | 题型模板 | 备注 |
|---|---|---|---|---|---|
| 第1章 | ✅ | ✅ | ✅ | 3 | 数论计算与证明模板已覆盖 |
```

如果暂不生成某类资产，说明原因，不要假装已完成。

## 禁止事项

- 不要为了填表生成空泛模板。
- 不要把所有知识点都强行生成同一种题型。
- 不要删除旧资料；需要废弃时在 draft 中标记或移入归档说明。
- 不要在没有用户确认时启用 profile。

