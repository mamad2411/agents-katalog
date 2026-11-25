---
name: chart-type-selection-framework
description: |
  当用户需要为特定数据选择最合适的图表类型时使用。触发场景：用户问"这个数据用什么图表好？"、"如何展示时间序列数据？"、"对比多个类别该用柱状图还是折线图？"。不适用于：纯信息查询、非数据可视化任务。关键 trigger 信号：数据维度（比较/趋势/占比/分布）、数据量大小、展示目的（精确值 vs 趋势感知）。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 4.6 图表类型样式速查表 + 7. Do's and Don'ts
tags: [data-visualization, chart-selection, decision-framework, echarts]
related_skills: [color-palette-principles, responsive-chart-strategy, chart-taboo-principles, kpi-card-design]
---

# Chart Type Selection Framework（图表类型选择决策框架）

## R (Reading) — 原文引用

> "柱状图 (Bar): barWidth: 60%, borderRadius: [4,4,0,0]... 折线图 (Line): lineWidth: 2px, symbol: 'circle', symbolSize: 6... 饼图 (Pie): radius: ['50%','70%']... 面积图 (Area): lineWidth: 0, 渐变 fill opacity: [0.15,0.02]... 散点图 (Scatter): symbolSize: 8, 透明度 0.6... 仪表盘 (Gauge): progress: { width: 8 }... 雷达图 (Radar): lineWidth: 1.5, 填充 opacity: 0.1... 漏斗图 (Funnel): gap: 2px, 标签右对齐"

> "Do's: 饼图扇区不超过 6 个 — 超过时合并为'其他'... 柱状图 Y 轴从 0 开始 — 避免视觉误导"

## I (Interpretation) — 方法论骨架

这是一个**数据特征到图表类型的映射决策框架**，核心思想是根据数据的**维度**（离散/连续）、**关系**（比较/趋势/占比/分布）和**展示目的**（精确值 vs 趋势感知），选择最能准确传达信息的可视化形式。

**决策流程**：
1. **识别数据关系**：是比较、趋势、占比、分布、进度还是流程？
2. **检查数据量**：数据点数量是否超过阈值（如饼图 >6 个扇区）？
3. **应用约束规则**：Y 轴是否从 0 开始？扇区是否需要合并？
4. **选择图表类型**：根据匹配结果选择对应图表
5. **应用样式规范**：使用对应的 barWidth/lineWidth/radius 等参数

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者为 8 种常见图表类型定义了明确的样式参数：
- **柱状图**用于离散类别对比（如"各产品线销售额"），barWidth 60% + 圆角 4px
- **折线图**用于时间序列趋势（如"近 30 天日活"），lineWidth 2px + symbol 6px
- **饼图**用于占比展示（如"市场份额"），半径 50%-70%，扇区 ≤6 个
- **面积图**用于趋势+总量感知（如"累计收入"），渐变填充 opacity 0.15→0.02

每个选择都伴随明确的约束条件（如"饼图扇区不超过 6 个"），确保视觉准确性。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 用户在设计 Dashboard 时纠结"这个指标用柱状图还是折线图？"
- 数据分析师问"我有 10 个类别的销售数据，用什么图表对比最合适？"
- 产品经理说"我想展示用户转化率的各个阶段，应该用漏斗图吗？"
- 开发者问"饼图有 8 个扇区，规范建议怎么处理？"

**与相邻 skill 的区分**：
- 与 `color-palette-principles` 的区别：本 skill 解决"用什么图表"，后者解决"用什么颜色"
- 与 `responsive-chart-strategy` 的区别：本 skill 解决"图表类型选择"，后者解决"不同屏幕尺寸下的布局适配"
- 与 `chart-taboo-principles` 的区别：本 skill 提供正向选择指南，后者提供负面清单（什么不能用）

**关键 trigger 词**：图表类型 / 用什么图 / 柱状图还是折线图 / 饼图扇区太多 / 数据可视化选型

## E (Execution) — 可执行步骤

**步骤 1：识别数据关系**
- 询问用户：数据的核心关系是什么？
  - **比较**：离散类别间的数值对比 → 柱状图
  - **趋势**：时间序列或连续变量变化 → 折线图/面积图
  - **占比**：部分与整体的关系 → 饼图/环形图
  - **分布**：两个变量的相关性 → 散点图
  - **进度**：单一指标的完成度 → 仪表盘
  - **流程**：转化率的阶段分析 → 漏斗图
  - **多维**：多个维度的综合评估 → 雷达图

**步骤 2：检查数据量约束**
- 如果是饼图：扇区数量是否 >6？
  - 是 → 合并尾部小扇区为"其他"
  - 否 → 直接使用
- 如果是折线图：数据点是否 ≥10？
  - 是 → 隐藏 symbol 以保持清晰
  - 否 → 显示 symbol（circle, 6px）

**步骤 3：应用关键约束**
- 柱状图：Y 轴必须从 0 开始（避免视觉误导）
- 饼图：禁用 3D 效果和渐变填充（扭曲比例感知）
- 所有图表：使用品牌分类色板（从 --chart-c-1 开始按序分配）

**步骤 4：生成 ECharts 配置**
- 根据选择的图表类型，应用对应的样式参数：
  ```javascript
  // 柱状图示例
  {
    series: [{
      type: 'bar',
      barWidth: '60%',
      itemStyle: { borderRadius: [4, 4, 0, 0] }
    }]
  }
  
  // 折线图示例
  {
    series: [{
      type: 'line',
      lineStyle: { width: 2 },
      symbol: 'circle',
      symbolSize: dataPoints >= 10 ? 0 : 6
    }]
  }
  ```

**步骤 5：验证输出**
- 检查是否符合 Do's and Don'ts：
  - [ ] 柱状图 Y 轴从 0 开始
  - [ ] 饼图扇区 ≤6 个
  - [ ] 未使用 3D 效果
  - [ ] 颜色来自品牌分类色板

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 数据关系复杂，需要组合图表（如柱状图+折线图双轴）→ 需要更高级的组合策略
- 数据量极大（>10000 点）→ 需要考虑性能优化（降采样、聚合）
- 特殊业务场景（如金融 K 线图、地理热力图）→ 需要专用图表类型

**作者的盲点**：
- 未讨论动态数据更新时的动画策略（增量更新 vs 全量重绘）
- 未说明多语言环境下的字体回退策略
- "饼图扇区不超过 6 个"是经验法则，但未给出合并算法（按值大小？按业务重要性？）

**失败模式警示**：
- **CE2: Y 轴不从零的误导**：截断 Y 轴会放大微小差异，导致用户错误判断
- **CE1: 3D 饼图陷阱**：3D 效果扭曲数据比例感知，必须禁用
- **CE4: 相似色混淆陷阱**：相邻颜色相似度 >80% 会导致色盲用户无法区分

**相关 skills**：
- `color-palette-principles` — 配色原则
- `responsive-chart-strategy` — 响应式策略
- `chart-taboo-principles` — 图表禁忌清单
- `kpi-card-design` — KPI 指标卡设计
