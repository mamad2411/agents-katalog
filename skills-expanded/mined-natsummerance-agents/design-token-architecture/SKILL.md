---
name: design-token-architecture
description: |
  当用户需要设计或维护一套设计系统的 CSS 变量架构时使用。触发场景：用户问"如何组织设计系统的颜色变量？"、"如何实现多主题切换？"、"Seed Token 和 Component Token 有什么区别？"。不适用于：单一页面的样式编写、非设计系统级别的变量规划。关键 trigger 信号：设计系统 / Token 架构 / 多主题支持 / CSS 变量层级。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 0. 品牌配置层 + 2. Color Palette & Roles
tags: [design-system, css-variables, token-architecture, theming]
related_skills: [color-palette-principles, consistency-principles, responsive-chart-strategy]
---

# Design Token Architecture（设计系统 Token 架构）

## R (Reading) — 原文引用

> ":root { --seed-brand: #4B7AFA; --chart-font-family: 'PingFang SC', ...; --chart-card-bg: #FFFFFF; --chart-card-radius: 8px; }"

> "[data-theme='dark'] { --chart-bg: #17171A; --chart-card-bg: #1D1D21; --chart-card-border: #2E2E32; }"

> "语义色: --chart-success: #00B42A; --chart-warning: #FF7D00; --chart-danger: #F53F3F; --chart-info: #2469FF"

## I (Interpretation) — 方法论骨架

这是一个**三层级的设计 Token 架构**，从基础种子（Seed）到组件（Component）再到语义（Semantic），确保设计一致性、可维护性和主题切换能力。

**三层架构**：
1. **Seed Token（种子层）**：最基础的原子值，不可再分解
   - 品牌色、字体族、基准间距
   - 特点：全局共享、极少修改
2. **Component Token（组件层）**：基于 Seed 组合成的组件样式
   - 卡片背景/圆角/阴影、坐标轴颜色、Tooltip 样式
   - 特点：复用 Seed、面向具体组件
3. **Semantic Token（语义层）**：赋予业务含义的颜色
   - 成功/警告/危险/信息、阈值线/平均线/基线
   - 特点：承载业务逻辑、与文化习惯一致

**核心价值**：
- **一致性**：所有组件共享同一套 Token，避免样式冲突
- **可维护性**：修改 Seed Token 即可全局更新
- **主题切换**：通过 `[data-theme="dark"]` 覆盖 Token 实现暗色模式

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了完整的 Token 体系：
- **Seed Token**：`--seed-brand: #4B7AFA`（品牌主色）、`--chart-font-family`（字体族）、`--chart-gap: 16px`（基准间距）
- **Component Token**：`--chart-card-bg: #FFFFFF`（卡片背景）、`--chart-grid-line: #F2F3F5`（网格线）、`--chart-tooltip-bg: rgba(29,33,41,0.92)`（Tooltip 背景）
- **Semantic Token**：`--chart-success: #00B42A`（成功）、`--chart-target-line: #F53F3F`（目标线）

暗色主题通过 `[data-theme="dark"]` 选择器覆盖关键 Token，实现一键切换。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"如何组织设计系统的 CSS 变量？"
- 前端工程师说"我们需要支持亮色/暗色双主题，怎么设计 Token？"
- 产品经理问"为什么修改品牌色后所有按钮都变了？"
- 技术负责人说"我们的设计 Token 太混乱了，需要重构"

**与相邻 skill 的区分**：
- 与 `color-palette-principles` 的区别：本 skill 解决"如何组织变量层级"，后者解决"如何选择配色方案"
- 与 `ai-friendly-spec-framework` 的区别：本 skill 是设计系统的基础架构，后者是让 AI 理解规范的方法论

**关键 trigger 词**：Token 架构 / CSS 变量层级 / 多主题支持 / Seed Token / 设计系统重构

## E (Execution) — 可执行步骤

**步骤 1：定义 Seed Token（种子层）**
- 列出所有不可再分解的基础值：
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

**步骤 2：定义 Component Token（组件层）**
- 基于 Seed 组合成组件样式：
  ```css
  :root {
    /* 卡片 */
    --chart-card-bg: #FFFFFF;
    --chart-card-radius: 8px;
    --chart-card-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    
    /* 坐标轴 */
    --chart-grid-line: #F2F3F5;
    --chart-axis-label: #86909C;
    
    /* Tooltip */
    --chart-tooltip-bg: rgba(29, 33, 41, 0.92);
    --chart-tooltip-text: #FFFFFF;
  }
  ```

**步骤 3：定义 Semantic Token（语义层）**
- 赋予业务含义的颜色：
  ```css
  :root {
    --chart-success: #00B42A;
    --chart-warning: #FF7D00;
    --chart-danger: #F53F3F;
    --chart-info: #2469FF;
    
    /* 阈值线 */
    --chart-target-line: #F53F3F;
    --chart-average-line: #86909C;
  }
  ```

**步骤 4：实现主题切换**
- 通过 `[data-theme="dark"]` 覆盖关键 Token：
  ```css
  [data-theme="dark"] {
    --chart-bg: #17171A;
    --chart-card-bg: #1D1D21;
    --chart-card-border: #2E2E32;
    --chart-grid-line: #2E2E32;
    --chart-tooltip-bg: rgba(255, 255, 255, 0.95);
    --chart-tooltip-text: #1D2129;
  }
  ```

**步骤 5：验证 Token 使用**
- 检查所有组件是否正确使用 Token：
  - [ ] 未硬编码颜色值（如 `#4B7AFA` → `var(--seed-brand)`）
  - [ ] 组件样式引用 Component Token
  - [ ] 业务状态引用 Semantic Token
  - [ ] 暗色主题下所有 Token 正确覆盖

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 单一页面的快速原型开发（直接写样式更快）
- 非设计系统级别的项目（无需多层 Token 架构）
- 需要支持 3+ 主题的场景（可能需要更复杂的 Token 管理工具）

**作者的盲点**：
- 未讨论 Token 的版本管理和向后兼容性
- 未说明如何在大型团队中同步 Token 变更
- 未提及 Token 的自动化测试策略（如视觉回归测试）

**失败模式警示**：
- **Token 泄漏**：Component Token 直接引用其他 Component Token，导致循环依赖
- **主题不完整**：暗色主题仅覆盖部分 Token，导致样式不一致
- **硬编码残留**：部分组件仍使用硬编码颜色，破坏 Token 体系

**相关 skills**：
- `color-palette-principles` — 配色原则
- `consistency-principles` — 一致性至上原则
- `responsive-chart-strategy` — 响应式策略
