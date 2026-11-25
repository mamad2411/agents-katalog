---
name: tooltip-missing-unit-trap
description: |
  当用户在 Tooltip 中省略数据单位时触发，用于警告这会造成歧义。触发场景：用户问"Tooltip 需要显示单位吗？"、"数值 1234 是什么意思？"、"如何避免用户对数据量级的误解？"。不适用于：无单位的纯计数数据。关键 trigger 信号：Tooltip 单位 / 数据单位 / 数值歧义 / 万/亿/元。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 7. Do's #3 + 7. Don'ts #5
tags: [data-visualization, tooltip, unit-display, clarity]
related_skills: [chart-taboo-principles, clarity-first-principles, kpi-card-glossary]
---

# Tooltip Missing Unit Trap（Tooltip 省略单位歧义）

## R (Reading) — 原文引用

> "Do's: Tooltip 包含单位 + 时间 + 值 — 完整上下文帮助用户快速理解"
> "Don'ts: 不要在 Tooltip 中省略数据单位 — 造成歧义"

## I (Interpretation) — 方法论骨架

**核心问题**：缺少单位的数据失去业务含义，用户无法判断数值的量级（是 1234 元还是 1234 万元？），导致误解或需要额外查找上下文。

**失败机制**：
1. **量级不明**：用户无法判断 1234 是 1234 元、1234 万元还是 1234 亿元
2. **决策错误**：基于错误的量级理解做出错误判断
3. **认知负担**：用户需要额外查找上下文才能理解数据

**正确做法**：所有数值显示必须包含单位（万/亿/元/个/人/次/%），Tooltip 应提供完整上下文（名称 + 数值 + 单位 + 时间）。

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者将"Tooltip 包含单位 + 时间 + 值"列为 Do's，将"省略数据单位"列为 Don'ts，强调完整上下文的重要性。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"Tooltip 需要显示单位吗？"
- 产品经理说"用户反馈看不懂这个数值是什么意思"
- 前端工程师问"数值 1234 应该显示为 '1234' 还是 '1234 万元'？"

**关键 trigger 词**：Tooltip 单位 / 数据单位 / 数值歧义 / 万/亿/元 / 完整上下文

## E (Execution) — 可执行步骤

**步骤 1：检查 Tooltip 配置**
- 验证 formatter 是否包含单位：
  ```javascript
  tooltip: {
    formatter: function(params) {
      // 错误做法：仅显示数值
      // return `${params.name}: ${params.value}`;
      
      // 正确做法：包含单位
      return `${params.name}: ${params.value} 万元`;
    }
  }
  ```

**步骤 2：添加完整上下文**
- Tooltip 应包含：名称 + 数值 + 单位 + 时间
  ```javascript
  tooltip: {
    formatter: function(params) {
      return `
        <div>${params.seriesName}</div>
        <div>时间: ${params.name}</div>
        <div>数值: ${params.value} 万元</div>
      `;
    }
  }
  ```

**步骤 3：自动化检查**
- 扫描 Tooltip formatter，查找缺少的单位：
  ```javascript
  const tooltipFormatter = option.tooltip?.formatter?.toString();
  if (tooltipFormatter && !/(万|亿|元|个|人|次|%)/.test(tooltipFormatter)) {
    console.warn('Tooltip 可能缺少单位，请检查');
  }
  ```

**步骤 4：验证用户理解**
- 进行可用性测试：让用户看 Tooltip，问"这个数值是什么意思？"
  - 如果用户能准确说出量级 → 合格 ✓
  - 如果用户困惑或猜错 → 需要添加单位

## B (Boundary) — 边界与盲点

**例外情况**：
- 无单位的纯计数数据（如"用户数: 1234 人"中的"人"可以省略，因为语境明确）
- 百分比数据（% 符号通常已包含在数值中）

**相关 skills**：
- `chart-taboo-principles` — 图表禁忌清单
- `clarity-first-principles` — 清晰性优先原则
- `kpi-card-glossary` — KPI 指标卡
