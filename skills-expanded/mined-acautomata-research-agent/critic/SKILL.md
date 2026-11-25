---
name: critic
description: Analyze a paper from a reviewer's perspective — find problems, weak claims, research gaps. Stands alone (no orchestrator wraps it). Triggers: 问题分析, 找论文弱点, 审稿式分析, critic, reviewer critique, 审稿质疑.
---

# critic — 审稿式问题与主张分析（独立 predicate）

## Mission

基于 Wiki 条目和实验提取文档（`extract` 产出），从审稿视角分析论文的 claim-机制-证据链，发现潜在问题、证据不足和研究空缺，产出结构化问题分析文档（§0–§7）。

**独立 predicate**：`critic` 不被任何 orchestrator 包裹。操作者或 main 直接调用它获取"这篇论文有什么问题"。下游 `design`（验证设计）消费 critic 的产出。

## When to use

- 用户问"这篇论文有什么弱点 / 问题""审稿人会质疑什么"
- 为 `design`（验证实验设计）准备问题列表
- 识别可转化为验证实验的质疑

不要用于：实验提取（`extract`）、验证设计（`design`）。

## 输入

| 材料 | 必需 |
|------|------|
| Wiki 条目 | 是 |
| 实验提取文档（`extract` 产出） | 是 |
| 论文原文（PDF/URL） | 推荐 |

## 工作原则

- 围绕"贡献 claim — 方法机制 — 实验现象 — 审稿式质疑 — 潜在研究空缺"展开
- 质疑必须具体：说明对象、依据和可能影响
- 优先保留"具体、重要、紧迫、可验证"的问题
- 区分：已有较强证据支持 / 实验间接暗示 / 仍需后续验证
- 结论强度与证据强度匹配，不强推断
- 推测标明"合理推测，仍需验证"；材料不足标明"现有材料不足以确认，但值得后续验证"

## 审稿式质疑类型

创新性、重要性、证据充分性、baseline、消融、泛化性、鲁棒性、效率与代价、可复现性。

## 输出结构

严格按 §0–§7 输出为一份完整 md，先写到 `raw/sources/<slug>.md`，然后调用 `ingest`（传入该 md 文件路径，`page_type: analysis`）统一写入 wiki；**不直接调用 `wiki_apply` 建页**（在 `# Title` 下空一行加 `` `category: critic` `` 作为可机读类别标识，供外部统计脚本提取）：

```markdown
# {{论文标题}}：审稿式现有方法问题分析

`category: critic`

## 0. 文档定位
## 1. 方法机制、实验支撑与关键前提
  ### 1.1 方法与实验的整体对应关系
  ### 1.2 方法可能依赖的关键前提
## 2. 核心贡献声明与审稿式质疑（3–5 个 claim）
## 3. 潜在问题分析（按重要性/紧迫性/可验证性排序）
## 4. 验证候选问题与优先级（筛选 2–4 个最值得优先验证的）
## 5. 可能形成的研究空缺方向
## 6. 新增来源与 Wiki 回写建议
## 7. 简短结论（150–200 字）
```

## 完成门禁

- >= 1 个有证据可追溯性的具体问题
- 区分三类证据强度
- 产出 md 已经 `ingest` 写入 wiki（含 wiki 路径），且本 skill 未直接调 `wiki_apply` 建页
- 产出 md 在 `# Title` 下空一行包含 `` `category: critic` ``（作为可机读类别标识，供外部统计脚本提取）
