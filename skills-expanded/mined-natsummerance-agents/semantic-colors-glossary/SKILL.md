---
name: semantic-colors-glossary
description: |
  当用户需要了解具有业务含义的颜色（成功/警告/危险/信息）时使用。触发场景：用户问"成功状态应该用什么颜色？"、"KPI 上涨用绿色还是红色？"、"告警系统的颜色怎么设计？"。不适用于：纯装饰性配色、无业务含义的数据系列（应使用分类色板）。关键 trigger 信号：语义色 / 成功失败颜色 / 告警颜色 / KPI 趋势色。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 2.3 语义色
tags: [semantic-colors, status-indicators, business-meaning, accessibility]
related_skills: [semantic-coloring-principles, categorical-palette-glossary]
---

# Semantic Colors（语义色）

## R (Reading) — 原文引用

> ":root { --chart-success: #00B42A; --chart-warning: #FF7D00; --chart-danger: #F53F3F; --chart-info: #2469FF; }"

## I (Interpretation) — 方法论骨架

**定义**：具有明确业务含义的颜色，用于传达状态、趋势或阈值信息。

**核心特征**：
- **业务映射**：颜色与业务状态一一对应（成功/警告/危险/信息）
- **文化一致性**：遵循目标用户的文化习惯（如红色=危险）
- **辅助编码**：不依赖单一颜色，配合图标/文字辅助理解

**典型示例**：
- `--chart-success: #00B42A`（成功/上涨）
- `--chart-warning: #FF7D00`（警告）
- `--chart-danger: #F53F3F`（危险/下跌）
- `--chart-info: #2469FF`（信息/中性）

**适用场景**：
- KPI 指标卡的趋势标识
- 告警系统的状态展示
- 阈值线的视觉标记

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了四态语义色，并在 KPI 卡片中使用绿色表示上涨、红色表示下跌。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"成功状态应该用什么颜色？"
- 产品经理说"KPI 上涨用绿色还是红色？"

**关键 trigger 词**：语义色 / 成功失败颜色 / 告警颜色 / KPI 趋势色

## E (Execution) — 可执行步骤

**步骤 1**：根据业务需求和文化习惯定义四态颜色
**步骤 2**：配合图标/文字辅助理解（色盲友好）
**步骤 3**：验证对比度 ≥4.5:1

## B (Boundary) — 边界与盲点

**不适用场景**：
- 纯装饰性配色
- 无业务含义的数据系列（使用分类色板）

**相关 skills**：
- `semantic-coloring-principles` — 语义化配色原则
- `categorical-palette-glossary` — 分类色板
