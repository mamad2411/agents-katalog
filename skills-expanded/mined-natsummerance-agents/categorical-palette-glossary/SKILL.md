---
name: categorical-palette-glossary
description: |
  当用户需要了解用于区分不同数据系列的配色方案时使用。触发场景：用户问"多系列图表应该用什么颜色？"、"分类色板是什么？"、"如何为饼图的各个扇区配色？"。不适用于：连续数值的热力图（应使用顺序色板）、有业务含义的状态色（应使用语义色）。关键 trigger 信号：分类色板 / 多系列配色 / 饼图颜色 / 数据系列区分。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 2.1 图表分类色板
tags: [color-palette, categorical-colors, data-series, chart-design]
related_skills: [sequential-palette-glossary, semantic-colors-glossary]
---

# Categorical Palette（分类色板）

## R (Reading) — 原文引用

> ":root { --chart-c-1: #4B7AFA; --chart-c-2: #44C2FD; --chart-c-3: #FFCE0E; ... --chart-c-18: #F2AEBA; }"

## I (Interpretation) — 方法论骨架

**定义**：用于区分不同系列/分类数据的颜色集合，按优先级排列（从 --chart-c-1 到 --chart-c-18）。

**核心特征**：
- **离散性**：每个颜色代表一个独立的类别
- **可区分性**：相邻颜色相似度 ≤80%，色盲用户可区分
- **有序性**：按视觉权重排序（主色优先）

**典型示例**：
- `--chart-c-1: #4B7AFA`（主色 / 第 1 系列）
- `--chart-c-2: #44C2FD`（第 2 系列）
- `--chart-c-3: #FFCE0E`（第 3 系列）

**适用场景**：
- 多系列柱状图/折线图
- 饼图/环形图的扇区着色
- Legend 中的颜色标识

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了 18 色分类色板，所有多系列图表按序使用这些颜色。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"多系列柱状图应该用什么颜色？"
- 前端工程师说"饼图的各个扇区怎么配色？"

**关键 trigger 词**：分类色板 / 多系列配色 / 饼图颜色 / 数据系列区分

## E (Execution) — 可执行步骤

**步骤 1**：从 --chart-c-1 开始按序分配颜色给各数据系列
**步骤 2**：确保相邻颜色相似度 ≤80%
**步骤 3**：验证色盲友好性

## B (Boundary) — 边界与盲点

**不适用场景**：
- 连续数值的热力图（使用顺序色板）
- 有业务含义的状态色（使用语义色）

**相关 skills**：
- `sequential-palette-glossary` — 顺序色板
- `semantic-colors-glossary` — 语义色
