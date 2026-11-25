---
name: seed-token-glossary
description: |
  当用户需要了解设计系统中最基础的 CSS 变量层级时使用。触发场景：用户问"什么是 Seed Token？"、"如何组织设计系统的颜色变量？"、"Seed Token 和 Component Token 有什么区别？"。不适用于：单一页面的样式编写、非设计系统级别的变量规划。关键 trigger 信号：Seed Token / 设计系统基础 / CSS 变量原子值。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 0. 品牌配置层 - Seed Token
tags: [design-system, css-variables, seed-token, token-architecture]
related_skills: [design-token-architecture, categorical-palette-glossary]
---

# Seed Token（种子令牌）

## R (Reading) — 原文引用

> ":root { --seed-brand: #4B7AFA; --chart-font-family: 'PingFang SC', ...; --chart-gap: 16px; }"

## I (Interpretation) — 方法论骨架

**定义**：设计系统中最基础的原子级 CSS 变量，作为所有组件样式的源头。Seed Token 不可再分解，是设计系统的"基因"。

**核心特征**：
- **原子性**：不可再分解的基础值（如颜色、字体、间距）
- **全局性**：所有组件共享同一套 Seed Token
- **稳定性**：一旦定义，极少修改

**典型示例**：
- `--seed-brand: #4B7AFA`（品牌主色）
- `--chart-font-family: "PingFang SC", ...`（字体族）
- `--chart-gap: 16px`（基准间距）

**相关概念**：
- Component Token（组件令牌）：基于 Seed Token 组合而成
- Semantic Token（语义令牌）：赋予业务含义的颜色

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范第 0 章，作者定义了完整的 Seed Token 体系，包括品牌色、字体、间距等基础值，所有后续组件样式都基于这些 Seed Token 构建。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"如何组织设计系统的 CSS 变量？"
- 前端工程师说"Seed Token 和 Component Token 有什么区别？"
- 技术负责人问"我们的设计 Token 架构应该怎么设计？"

**关键 trigger 词**：Seed Token / 设计系统基础 / CSS 变量原子值 / Token 层级

## E (Execution) — 可执行步骤

**步骤 1：识别原子值**
- 列出所有不可再分解的基础值：
  - 品牌色：`--seed-brand`
  - 字体族：`--chart-font-family`
  - 基准间距：`--chart-gap`

**步骤 2：定义 Seed Token**
```css
:root {
  /* 品牌色 */
  --seed-brand: #4B7AFA;
  --seed-brand-hover: #3455AD;
  
  /* 字体 */
  --chart-font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  --chart-font-size-sm: 11px;
  --chart-font-size: 12px;
  --chart-font-size-lg: 14px;
  
  /* 间距 */
  --chart-gap: 16px;
  --chart-section-gap: 24px;
}
```

**步骤 3：验证使用**
- 检查所有组件是否引用 Seed Token 而非硬编码值

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 单一页面的快速原型开发
- 非设计系统级别的项目

**相关 skills**：
- `design-token-architecture` — 设计系统 Token 架构
- `categorical-palette-glossary` — 分类色板
