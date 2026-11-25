---
name: responsive-chart-strategy
description: |
  当用户需要为数据可视化产品设计多端适配策略时使用。触发场景：用户问"如何让图表在手机上也能看清？"、"Dashboard 如何适配不同屏幕尺寸？"、"移动端图表交互如何优化？"。不适用于：固定尺寸的嵌入式图表、非响应式应用场景。关键 trigger 信号：响应式 / 多端适配 / 移动端优化 / 断点定义 / 触摸交互。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 5. Layout Principles + 8. Responsive Behavior
tags: [responsive-design, mobile-optimization, chart-layout, breakpoints]
related_skills: [chart-type-selection-framework, design-token-architecture, clarity-first-principles]
---

# Responsive Chart Strategy Framework（响应式图表策略框架）

## R (Reading) — 原文引用

> "断点: XL ≥1920px (3列), L ≥1440px (3列), M ≥1024px (2列), S ≥728px (2列), XS <728px (1列)... 图表高度: XL 240px, L/M 220-240px, S 220px, XS 200px"

> "移动端特殊行为: 柱状图转为水平柱状图 (横向排版更友好), Legend 移至图表底部, Tooltip 固定于底部而非跟随手指, 触摸目标最小 44x44px"

> "ECharts 响应式配置: window.addEventListener('resize', () => { chartInstance.resize({ animation: { duration: 300 } }); });"

## I (Interpretation) — 方法论骨架

这是一个**从桌面到移动端的完整响应式适配框架**，涵盖断点定义、布局重排、交互优化三个层面。

**三层策略**：
1. **断点定义层**：5 个标准断点（XL/L/M/S/XS），每个断点对应不同的图表格列数和图表高度
2. **布局重排层**：根据屏幕宽度自动调整列数，必要时改变图表方向（纵向柱状图→横向柱状图）
3. **交互优化层**：针对移动端特殊优化（Legend 位置、Tooltip 固定、触摸目标尺寸）

**核心价值**：
- 无缝体验：用户在不同设备上获得一致的视觉层次
- 性能优化：移动端减少不必要的装饰元素
- 可用性保障：触摸目标符合人体工程学（≥44x44px）

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了完整的响应式策略：
- **断点系统**：5 个断点（XL≥1920px / L≥1440px / M≥1024px / S≥728px / XS<728px），每个断点对应不同的图表格列数（3/3/2/2/1）和 KPI 卡列数（6/4-5/3-4/2/1）
- **移动端优化**：柱状图转为水平方向、Legend 移至底部、Tooltip 固定于底部、触摸目标最小 44x44px
- **ECharts 配置**：监听 resize 事件，调用 `chartInstance.resize()` 并设置 300ms 动画

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"如何让 Dashboard 在手机上也好看？"
- 前端工程师说"图表在平板上显示太拥挤了，怎么优化？"
- 产品经理问"移动端用户反馈图表看不清，有什么解决方案？"
- 测试人员说"不同屏幕尺寸下图表布局混乱，需要统一策略"

**与相邻 skill 的区分**：
- 与 `chart-type-selection-framework` 的区别：本 skill 解决"不同屏幕下的布局和交互"，后者解决"选择什么图表类型"
- 与 `design-token-architecture` 的区别：本 skill 解决响应式布局，后者解决 CSS 变量层级

**关键 trigger 词**：响应式图表 / 移动端优化 / 断点适配 / 触摸交互 / 多端布局

## E (Execution) — 可执行步骤

**步骤 1：定义断点系统**
- 根据目标设备分布，定义 5 个标准断点：
  ```css
  /* XL: ≥1920px */
  @media (min-width: 1920px) {
    .chart-grid { grid-template-columns: repeat(3, 1fr); }
    .chart-card { min-height: 240px; }
  }
  
  /* L: ≥1440px */
  @media (min-width: 1440px) and (max-width: 1919px) {
    .chart-grid { grid-template-columns: repeat(3, 1fr); }
    .chart-card { min-height: 220px; }
  }
  
  /* M: ≥1024px */
  @media (min-width: 1024px) and (max-width: 1439px) {
    .chart-grid { grid-template-columns: repeat(2, 1fr); }
    .chart-card { min-height: 240px; }
  }
  
  /* S: ≥728px */
  @media (min-width: 728px) and (max-width: 1023px) {
    .chart-grid { grid-template-columns: repeat(2, 1fr); }
    .chart-card { min-height: 220px; }
  }
  
  /* XS: <728px */
  @media (max-width: 727px) {
    .chart-grid { grid-template-columns: 1fr; }
    .chart-card { min-height: 200px; }
  }
  ```

**步骤 2：实现布局重排**
- 使用 CSS Grid 的 `auto-fill` + `minmax` 实现自适应：
  ```css
  .chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--chart-gap);
  }
  ```
- 移动端特殊处理：柱状图转为水平方向
  ```javascript
  const isMobile = window.innerWidth < 728;
  if (isMobile && chartType === 'bar') {
    chartInstance.setOption({
      xAxis: { type: 'value' },
      yAxis: { type: 'category' }
    });
  }
  ```

**步骤 3：优化移动端交互**
- Legend 移至底部：
  ```javascript
  if (isMobile) {
    chartInstance.setOption({
      legend: { bottom: 0, orient: 'horizontal' }
    });
  }
  ```
- Tooltip 固定于底部：
  ```javascript
  if (isMobile) {
    chartInstance.setOption({
      tooltip: { position: ['50%', '90%'] }
    });
  }
  ```
- 触摸目标最小 44x44px：
  ```css
  .legend-item {
    min-width: 44px;
    min-height: 44px;
  }
  ```

**步骤 4：监听 resize 事件**
- 确保图表随容器大小变化自动调整：
  ```javascript
  window.addEventListener('resize', () => {
    chartInstance.resize({
      animation: { duration: 300 }
    });
  });
  ```

**步骤 5：验证响应式效果**
- 在 5 个断点下分别测试：
  - [ ] 图表格列数正确
  - [ ] 图表高度合适
  - [ ] Legend 位置正确（桌面端顶部/右侧，移动端底部）
  - [ ] Tooltip 不超出视口
  - [ ] 触摸目标 ≥44x44px
  - [ ] 横向柱状图在移动端正确显示

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 固定尺寸的嵌入式图表（如邮件中的静态图表）
- 单端应用（仅桌面或仅移动端）
- 需要精确像素控制的打印输出

**作者的盲点**：
- 未讨论超大屏幕（≥3840px 4K）的适配策略
- 未说明横屏/竖屏切换时的动态调整
- 未提及折叠屏等特殊设备的适配

**失败模式警示**：
- **断点过多**：定义超过 7 个断点，导致维护成本过高
- **过度重排**：频繁改变布局导致用户迷失方向
- **触摸目标过小**：Legend 项或 Tooltip 关闭按钮 <44x44px，导致误触

**相关 skills**：
- `chart-type-selection-framework` — 图表类型选择决策框架
- `design-token-architecture` — 设计系统 Token 架构
- `clarity-first-principles` — 清晰性优先原则
