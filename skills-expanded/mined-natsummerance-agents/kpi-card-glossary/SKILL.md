---
name: kpi-card-glossary
description: |
  当用户需要了解 KPI 指标卡的设计规范时使用。触发场景：用户问"KPI 卡片应该包含哪些元素？"、"如何设计关键业务指标的展示？"、"KPI 数值的字体和样式是什么？"。不适用于：普通数据表格、非关键指标的展示。关键 trigger 信号：KPI 卡片 / 关键指标 / 指标卡设计 / Label Value Trend。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 4.2 KPI 指标卡
tags: [kpi-card, dashboard-design, key-metrics, component-design]
related_skills: [clarity-first-principles, semantic-colors-glossary]
---

# KPI Card（KPI 指标卡）

## R (Reading) — 原文引用

> ".kpi-card__label { font-size: 12px; font-weight: 400; color: var(--chart-axis-label); } .kpi-card__value { font-size: 28px; font-weight: 600; font-family: var(--chart-number-font); font-variant-numeric: tabular-nums; } .kpi-card__trend { font-size: 11px; }"

## I (Interpretation) — 方法论骨架

**定义**：一种特殊的图表容器组件，用于展示关键业务指标的核心数值、趋势和微型图表。

**核心组成**：
- **Label（指标名）**：12px / 400 字重 / #86909C
- **Value（主数值）**：28px / 600 字重 / DIN Alternate 字体 / tabular-nums
- **Trend（趋势标识）**：11px / 颜色编码（绿=涨，红=跌）
- **Micro Chart（可选）**：40px 高的迷你折线图

**典型示例**：
```css
.kpi-card__value {
  font-size: 28px;
  font-weight: 600;
  font-family: var(--chart-number-font);
  font-variant-numeric: tabular-nums;
}
```

**适用场景**：
- Dashboard 顶部的核心指标概览
- 业务报表的关键数据展示
- 实时监控面板的核心指标

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了完整的 KPI 卡片样式，包括 Label/Value/Trend/Micro Chart 四层结构。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"KPI 卡片应该包含哪些元素？"
- 前端工程师说"KPI 数值的字体和样式是什么？"

**关键 trigger 词**：KPI 卡片 / 关键指标 / 指标卡设计 / Label Value Trend

## E (Execution) — 可执行步骤

**步骤 1**：定义四层结构（Label → Value → Trend → Micro Chart）
**步骤 2**：应用样式规范（28px/600/DIN Alternate/tabular-nums）
**步骤 3**：添加趋势标识（绿色上涨，红色下跌）
**步骤 4**：可选嵌入微型图表

## B (Boundary) — 边界与盲点

**不适用场景**：
- 非关键指标的展示
- 普通数据表格

**相关 skills**：
- `clarity-first-principles` — 清晰性优先原则
- `semantic-colors-glossary` — 语义色
