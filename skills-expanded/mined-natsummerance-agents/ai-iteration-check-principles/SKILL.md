---
name: ai-iteration-check-principles
description: |
  当用户需要检查 AI 生成的数据可视化代码是否符合规范时使用。触发场景：用户问"AI 生成的图表代码有问题吗？"、"如何自动化检查图表质量？"、"AI 生成的代码需要人工 Review 哪些点？"。不适用于：人工编写的代码审查、非图表类的代码检查。关键 trigger 信号：AI 生成代码质检 / Iteration Guide / 10 条检查项 / 自动化验证。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 9. Agent Prompt Guide - Iteration Guide
tags: [ai-quality-check, code-review, iteration-guide, automation]
related_skills: [ai-friendly-spec-framework, chart-taboo-principles, clarity-first-principles]
---

# AI Iteration Check Principles（AI 迭代检查原则）

## R (Reading) — 原文引用

> "Iteration Guide: 1. 颜色第一位 — 生成图表前先确认用哪种色板（分类/顺序/语义） 2. 卡片是基本单位 — 所有图表必须包裹在 .chart-card 容器中 3. Tooltip 不离散 — 确保 Tooltip 始终指向数据且不超出视口 4. 数据为空先处理 — 检测空数据时自动渲染空状态占位，不渲染空白图表 5. 移动端先考虑 — 优先使用 grid-auto-rows + minmax 实现灵活布局 6. 动画不超过 1 秒 — animationDuration 默认 800ms，首次加载可设 0 7. 单位不可省 — 所有数值显示必须包含单位 (万/亿/元/个/人/次) 8. 图例排序与数据一致 — Legend 顺序严格匹配数据系列顺序 9. 暗色模式双色板 — 检测 [data-theme='dark'] 时切换暗色主题色板 10. 可访问性必检 — 色盲友好、对比度 ≥4.5:1、键盘可操作"

## I (Interpretation) — 方法论骨架

这是**AI 生成代码后的 10 条必检清单**，用于快速识别常见问题并指导迭代优化。

**十条检查项分类**：
1. **配色类**（#1, #9）：颜色选择是否正确，暗色模式是否适配
2. **结构类**（#2, #4）：容器是否正确，空数据是否处理
3. **交互类**（#3, #5）：Tooltip 是否正常，移动端是否优化
4. **性能类**（#6）：动画时长是否合理
5. **内容类**（#7, #8）：单位是否完整，图例顺序是否正确
6. **可访问性类**（#10）：是否符合无障碍标准

**核心价值**：
- 快速定位问题：10 条检查项覆盖 80% 常见错误
- 减少人工返工：自动化检查替代人工 Review
- 持续改进：每次迭代后重新检查，直到全部通过

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范第 9 章，作者将这 10 条检查项作为 AI 生成代码后的必检清单。例如：
- **颜色第一位**：AI 生成柱状图前，必须先确认使用分类色板（--chart-c-1, --chart-c-2...）而非随机颜色
- **卡片是基本单位**：所有 ECharts 实例必须包裹在 `.chart-card` 容器中，应用统一的圆角/边框/阴影
- **单位不可省**：KPI 数值必须显示为 "1234 万元" 而非 "1234"

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 开发者问"AI 生成的图表代码需要检查哪些点？"
- QA 工程师说"需要建立图表质量的自动化检查流程"
- 技术负责人问"如何减少 AI 生成代码的返工次数？"
- 设计师说"AI 生成的样式总是不对，怎么改进？"

**与相邻 skill 的区分**：
- 与 `ai-friendly-spec-framework` 的区别：本 skill 仅提供 10 条检查清单，后者提供完整的三件套框架（Quick Reference + Component Prompts + Iteration Guide）
- 与 `chart-taboo-principles` 的区别：本 skill 提供正向检查项，后者提供负面清单（什么不能用）

**关键 trigger 词**：AI 生成代码质检 / Iteration Guide / 10 条检查项 / 自动化验证 / 图表质量检查

## E (Execution) — 可执行步骤

**步骤 1：检查颜色选择（#1, #9）**
- [ ] 生成图表前确认使用正确的色板（分类/顺序/语义）
- [ ] 暗色模式下正确切换色板（检测 `[data-theme="dark"]`）
- 自动化检查：
  ```javascript
  // 扫描 CSS，查找硬编码颜色值
  const hasHardCodedColors = css.includes('#4B7AFA') && !css.includes('var(--chart-c-1)');
  if (hasHardCodedColors) {
    console.error('发现硬编码颜色，应使用 Token');
  }
  ```

**步骤 2：检查容器结构（#2, #4）**
- [ ] 所有图表包裹在 `.chart-card` 容器中
- [ ] 空数据时渲染空状态占位（"暂无数据"或骨架屏），而非空白图表
- 自动化检查：
  ```javascript
  // 检查 ECharts 实例是否有父容器 .chart-card
  const chartContainer = document.querySelector('.echarts-container');
  if (!chartContainer.closest('.chart-card')) {
    console.error('图表未包裹在 .chart-card 容器中');
  }
  ```

**步骤 3：检查交互行为（#3, #5）**
- [ ] Tooltip 始终指向数据且不超出视口
- [ ] 移动端使用响应式布局（grid-auto-rows + minmax）
- 手动测试：
  - 鼠标悬停数据点，检查 Tooltip 位置
  - 缩小浏览器窗口到 <728px，检查布局重排

**步骤 4：检查性能配置（#6）**
- [ ] animationDuration ≤1000ms（默认 800ms）
- [ ] 首次加载时 animationDuration 设为 0（避免闪烁）
- 自动化检查：
  ```javascript
  const option = chartInstance.getOption();
  if (option.animationDuration > 1000) {
    console.warn('动画时长超过 1 秒，建议设为 800ms');
  }
  ```

**步骤 5：检查内容完整性（#7, #8）**
- [ ] 所有数值显示包含单位（万/亿/元/个/人/次）
- [ ] Legend 顺序严格匹配数据系列顺序
- 自动化检查：
  ```javascript
  // 检查数值是否包含单位
  const valueElements = document.querySelectorAll('.kpi-value');
  valueElements.forEach(el => {
    if (!/\d+\s*(万|亿|元|个|人|次)/.test(el.textContent)) {
      console.warn('数值缺少单位:', el.textContent);
    }
  });
  ```

**步骤 6：检查可访问性（#10）**
- [ ] 色盲友好（不依赖单一颜色传达信息）
- [ ] 对比度 ≥4.5:1
- [ ] 键盘可操作（Tab 键可聚焦图表元素）
- 自动化工具：
  - 使用 axe-core 进行无障碍审计
  - 使用 Coblis 色盲模拟器检查

**步骤 7：生成检查报告**
- 汇总所有检查结果：
  ```
  ✅ 颜色选择正确
  ✅ 容器结构正确
  ❌ Tooltip 超出视口（需修复）
  ✅ 空数据处理正确
  ...
  通过率: 9/10 = 90%
  ```
- 如果通过率 <100%，返回 AI 重新生成并指定失败项

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 人工编写的代码审查（需要更全面的检查清单）
- 非图表类的代码检查
- AI 已经经过充分训练，能稳定生成合格代码的场景

**作者的盲点**：
- 未讨论如何将 10 条检查项转化为自动化测试用例
- 未说明检查失败的优先级排序（哪些必须修复，哪些可以容忍）
- 未提及不同图表类型的特殊检查项（如饼图需额外检查扇区数量）

**失败模式警示**：
- **检查项过多**：超过 15 条检查项，导致 AI 难以全部满足
- **检查项模糊**：如"美观性良好"无法自动化验证
- **误报率高**：自动化检查工具过于严格，标记大量非问题

**相关 skills**：
- `ai-friendly-spec-framework` — AI 友好的规范编写框架
- `chart-taboo-principles` — 图表禁忌清单
- `clarity-first-principles` — 清晰性优先原则
