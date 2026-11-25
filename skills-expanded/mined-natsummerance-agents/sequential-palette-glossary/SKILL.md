---
name: sequential-palette-glossary
description: |
  当用户需要了解用于表达连续数值/热力/密度的渐变色板时使用。触发场景：用户问"热力图应该用什么颜色？"、"如何展示从低到高的数值变化？"、"顺序色板和分类色板有什么区别？"。不适用于：离散类别的区分（应使用分类色板）、有业务含义的状态色（应使用语义色）。关键 trigger 信号：顺序色板 / 渐变色 / 热力图颜色 / 连续数值。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 2.2 顺序色板
tags: [color-palette, sequential-colors, heatmap, continuous-data]
related_skills: [categorical-palette-glossary, semantic-colors-glossary]
---

# Sequential Palette（顺序色板）

## R (Reading) — 原文引用

> ":root { --chart-seq-1: #E8F3FF; --chart-seq-2: #BEDAFF; ... --chart-seq-7: #1A54D4; }"

## I (Interpretation) — 方法论骨架

**定义**：用于连续数值/热力/密度表达的渐变色板，从浅色到深色表示数值从小到大。

**核心特征**：
- **连续性**：颜色之间平滑过渡，无跳跃
- **单调性**：亮度/饱和度随数值单调变化
- **Perceptual Uniformity**：人眼感知的变化与数值变化一致

**典型示例**：
- `--chart-seq-1: #E8F3FF`（最小值）
- `--chart-seq-4: #5CA8FF`（中间值）
- `--chart-seq-7: #1A54D4`（最大值）

**适用场景**：
- 热力图（Heatmap）
- 地理分布图（Choropleth Map）
- 密度散点图

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了 7 级顺序色板，用于热力图等连续数值表达。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"热力图应该用什么颜色渐变？"
- 前端工程师说"如何展示从低到高的数值变化？"

**关键 trigger 词**：顺序色板 / 渐变色 / 热力图颜色 / 连续数值

## E (Execution) — 可执行步骤

**步骤 1**：根据数值范围映射到 7 级色板
**步骤 2**：确保颜色渐变平滑
**步骤 3**：验证 perceptual uniformity

## B (Boundary) — 边界与盲点

**不适用场景**：
- 离散类别的区分（使用分类色板）
- 有业务含义的状态色（使用语义色）

**相关 skills**：
- `categorical-palette-glossary` — 分类色板
- `semantic-colors-glossary` — 语义色
