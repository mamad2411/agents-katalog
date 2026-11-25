---
name: consistency-principles
description: |
  当用户需要确保多个图表或组件的样式统一时使用。触发场景：用户问"如何让所有图表看起来像一个整体？"、"不同页面的图表样式不一致怎么办？"、"如何建立统一的图表样式规范？"。不适用于：单一图表的设计、故意追求多样性的艺术性可视化。关键 trigger 信号：样式统一 / 一致性 / 跨图表 / 品牌规范 / Token 复用。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 1. Visual Theme & Atmosphere + 3. Typography Rules + 7. Do's and Don'ts
tags: [design-consistency, style-unification, brand-identity, token-reuse]
related_skills: [clarity-first-principles, design-token-architecture, semantic-coloring-principles]
---

# Consistency Principles（一致性至上原则）

## R (Reading) — 原文引用

> "一致: 跨图表类型保持色彩/字体/间距统一... Do's: 始终使用品牌分类色板 — 图表系列颜色从 --chart-c-1 开始按序使用... Don'ts: 不要使用超过 2 种字重在图表中 — 保持视觉一致性"

> "Typography Rules: 图表中不使用超过 2 种字重组合... KPI 数值使用粗体 600，其余文本使用 Regular 400"

> "Component Stylings: 所有图表卡片使用相同的圆角/边框/阴影（border-radius: 8px, border: 1px solid #E5E6EB, box-shadow: 0 1px 4px rgba(0,0,0,0.04)）"

## I (Interpretation) — 方法论骨架

这是设计系统的**核心支柱**：通过统一的视觉语言降低用户的认知成本，提升品牌识别度。

**三个维度的一致性**：
1. **色彩一致性**：所有图表使用同一套分类色板（从 --chart-c-1 开始按序分配）
2. **字体一致性**：图表中不超过 2 种字重组合（600 用于主数据，400 用于辅助信息）
3. **间距一致性**：使用统一的间距系统（--chart-spacing-xs/sm/md/lg/xl/2xl）

**核心价值**：
- 降低认知成本：用户无需重新学习每种图表的样式
- 提升品牌识别度：统一的视觉语言强化品牌形象
- 简化开发维护：一套 Token 服务所有图表

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者通过以下方式确保一致性：
- **色彩**：定义 18 色分类色板（--chart-c-1 到 --chart-c-18），所有图表按序使用
- **字体**：仅使用 2 种字重（600 用于 KPI Value 和 Title，400 用于其他文本），数字使用 DIN Alternate 等宽字体
- **间距**：定义 7 级间距系统（4px/8px/12px/16px/20px/24px/32px），所有组件共享
- **组件样式**：所有图表卡片使用相同的圆角（8px）、边框（1px solid #E5E6EB）、阴影（0 1px 4px rgba(0,0,0,0.04)）

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"如何让 Dashboard 中的所有图表看起来像一个整体？"
- 前端工程师说"不同页面的图表样式不一致，怎么统一？"
- 产品经理问"为什么我们的图表看起来不像一个产品？"
- 技术负责人说"需要建立统一的图表样式规范"

**与相邻 skill 的区分**：
- 与 `clarity-first-principles` 的区别：本 skill 解决"多个图表之间的统一性"，后者解决"单个图表的清晰度"
- 与 `design-token-architecture` 的区别：本 skill 提供一致性原则，后者提供 Token 组织架构

**关键 trigger 词**：样式统一 / 一致性 / 跨图表 / 品牌规范 / Token 复用 / 看起来不像一个产品

## E (Execution) — 可执行步骤

**步骤 1：统一色彩系统**
- 定义品牌分类色板（18 色）：
  ```css
  :root {
    --chart-c-1:  #4B7AFA;  /* 主色 */
    --chart-c-2:  #44C2FD;
    --chart-c-3:  #FFCE0E;
    /* ... 共 18 色 */
  }
  ```
- 强制规则：
  - 所有图表必须从 --chart-c-1 开始按序使用
  - 禁止硬编码颜色值（如 `#4B7AFA` → `var(--chart-c-1)`）
  - 相邻颜色相似度 ≤80%（色盲用户可区分）

**步骤 2：统一定义字体层级**
- 定义 9 种字体层级，但仅使用 2 种字重：
  ```css
  /* 600 字重（主数据） */
  .chart-card__title { font-size: 14px; font-weight: 600; }
  .kpi-card__value { font-size: 28px; font-weight: 600; }
  
  /* 400 字重（辅助信息） */
  .axis-label { font-size: 11px; font-weight: 400; }
  .legend { font-size: 12px; font-weight: 400; }
  ```
- 数字专用字体：
  ```css
  .kpi-card__value {
    font-family: var(--chart-number-font); /* DIN Alternate */
    font-variant-numeric: tabular-nums;
  }
  ```

**步骤 3：统一间距系统**
- 定义 7 级间距：
  ```css
  :root {
    --chart-spacing-xs: 4px;
    --chart-spacing-sm: 8px;
    --chart-spacing-md: 12px;
    --chart-spacing:   16px;   /* 基准 */
    --chart-spacing-lg: 20px;
    --chart-spacing-xl: 24px;
    --chart-spacing-2xl: 32px;
  }
  ```
- 强制规则：
  - 所有组件间距必须使用 Token，禁止硬编码
  - 图表卡片间距基准为 16px（--chart-spacing）
  - 区块间距为 24px（--chart-spacing-xl）

**步骤 4：统一组件样式**
- 定义标准图表卡片样式：
  ```css
  .chart-card {
    background: var(--chart-card-bg);
    border: var(--chart-card-border);       /* 1px solid #E5E6EB */
    border-radius: var(--chart-card-radius); /* 8px */
    box-shadow: var(--chart-card-shadow);    /* 0 1px 4px rgba(0,0,0,0.04) */
    padding: var(--chart-card-padding);      /* 16px */
  }
  ```
- 所有图表类型（柱状图、折线图、饼图等）必须包裹在此容器中

**步骤 5：验证一致性**
- 视觉审查：
  - [ ] 所有图表使用相同的色板
  - [ ] 所有图表使用相同的字体层级
  - [ ] 所有图表卡片样式一致
  - [ ] 间距符合 7 级系统
- 自动化检查：
  ```javascript
  // 扫描 CSS 文件，查找硬编码颜色值
  const hardCodedColors = css.match(/#[0-9A-Fa-f]{6}/g);
  if (hardCodedColors.length > 0) {
    console.warn('发现硬编码颜色:', hardCodedColors);
  }
  ```

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 特殊营销活动（需要突破常规设计吸引眼球）
- A/B 测试（需要对比不同样式的效果）
- 多品牌产品（不同子品牌需要不同的视觉语言）

**作者的盲点**：
- 未讨论如何在保持一致性的同时允许适度的个性化
- 未说明如何处理历史遗留的不一致样式（重构策略）
- 未提及国际化环境下的字体一致性挑战

**失败模式警示**：
- **过度一致**：所有图表完全相同，失去区分度
- **Token 泄漏**：部分组件仍使用硬编码值，破坏一致性
- **版本不同步**：不同团队使用的 Token 版本不一致

**相关 skills**：
- `clarity-first-principles` — 清晰性优先原则
- `design-token-architecture` — 设计系统 Token 架构
- `semantic-coloring-principles` — 语义化配色原则
