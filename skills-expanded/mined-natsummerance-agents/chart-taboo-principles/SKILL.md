---
name: chart-taboo-principles
description: |
  当用户需要避免数据可视化中的常见错误时使用。触发场景：用户问"设计图表时有哪些绝对不能做的事？"、"为什么我的图表看起来不专业？"、"设计评审时应该检查哪些负面清单？"。不适用于：正向的设计指导、艺术性可视化。关键 trigger 信号：设计禁忌 / Don'ts / 负面清单 / 常见错误 / 设计评审检查。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 7. Do's and Don'ts (Don'ts section)
tags: [design-taboos, common-mistakes, negative-checklist, design-review]
related_skills: [clarity-first-principles, consistency-principles, 3d-pie-chart-trap, y-axis-non-zero-trap]
---

# Chart Taboo Principles（图表禁忌原则）

## R (Reading) — 原文引用

> "Don'ts: 1. 不要使用超过 2 种字重在图表中 — 保持视觉一致性 2. 不要在分类色板中使用相似度 >80% 的颜色 — 色盲用户无法区分 3. 不要隐藏轴刻度标签除非空间极度受限 — 总提供至少 3-5 个刻度 4. 不要在饼图中使用 3D 效果或渐变填充 — 扭曲数据比例感知 5. 不要在 Tooltip 中省略数据单位 — 造成歧义 6. 不要在 KPI 卡片中使用装饰性图表 — 微型图表只放于有趋势意义的指标 7. 不要使用纯装饰性网格线 — 仅 Y 轴需要分割线 8. 不要在移动端展示超过 2 列的图表网格 — 信息密度过高"

## I (Interpretation) — 方法论骨架

这是**数据可视化的负面清单**，明确列出 8 条绝对禁止的设计行为，帮助设计师和开发者避免常见陷阱。

**八条禁忌分类**：
1. **视觉一致性类**（#1）：字重不超过 2 种
2. **可访问性类**（#2, #3）：颜色相似度 ≤80%，轴刻度至少 3-5 个
3. **数据真实性类**（#4）：禁用 3D 效果和渐变填充
4. **内容完整性类**（#5, #6）：Tooltip 必须含单位，微型图表必须有意义
5. **视觉噪音类**（#7）：禁用纯装饰性网格线
6. **响应式类**（#8）：移动端不超过 2 列

**核心价值**：
- 快速识别错误：设计评审时逐项检查
- 预防常见问题：新人培训的反面教材
- 自动化 lint：转化为代码检查规则

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范第 7 章，作者明确列出 8 条 Don'ts，并在其他章节提供对应的正确做法：
- **#4 禁用 3D 饼图**：在 4.6 图表类型样式速查表中，饼图定义为纯扁平化（radius: ['50%','70%']），无 3D 效果
- **#1 字重限制**：在 3.3 设计哲学中明确"图表中不使用超过 2 种字重组合"
- **#8 移动端列数**：在 8.1 图表自适应策略中定义 XS 断点（<728px）为 1 列

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"设计评审时应该检查哪些负面清单？"
- 前端工程师说"为什么我的图表看起来不专业？"
- QA 工程师问"如何自动化检查图表设计的常见错误？"
- 新人培训："有哪些绝对不能做的设计行为？"

**与相邻 skill 的区分**：
- 与 `clarity-first-principles` 的区别：本 skill 提供负面清单（什么不能用），后者提供正向指导（应该怎么做）
- 与 `ai-iteration-check-principles` 的区别：本 skill 专注设计禁忌，后者专注 AI 生成代码的质量检查

**关键 trigger 词**：设计禁忌 / Don'ts / 负面清单 / 常见错误 / 设计评审检查 / 3D 饼图 / 字重过多

## E (Execution) — 可执行步骤

**步骤 1：检查字重使用（#1）**
- 扫描 CSS/JS 代码，统计使用的字重数量：
  ```javascript
  const fontWeights = new Set();
  document.querySelectorAll('*').forEach(el => {
    const fw = getComputedStyle(el).fontWeight;
    if (fw !== 'normal' && fw !== '400') {
      fontWeights.add(fw);
    }
  });
  if (fontWeights.size > 2) {
    console.error(`使用了 ${fontWeights.size} 种字重，超过限制的 2 种`);
  }
  ```
- 修复：仅保留 600（主数据）和 400（辅助信息）

**步骤 2：检查颜色相似度（#2）**
- 计算相邻颜色的相似度（使用 CIEDE2000 色差公式）：
  ```javascript
  function colorSimilarity(color1, color2) {
    // 简化版：计算 RGB 欧氏距离
    const r1 = parseInt(color1.slice(1,3), 16);
    const g1 = parseInt(color1.slice(3,5), 16);
    const b1 = parseInt(color1.slice(5,7), 16);
    const r2 = parseInt(color2.slice(1,3), 16);
    const g2 = parseInt(color2.slice(3,5), 16);
    const b2 = parseInt(color2.slice(5,7), 16);
    const distance = Math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2);
    return 1 - distance / 441.67; // 归一化到 0-1
  }
  
  const similarity = colorSimilarity('#4B7AFA', '#5C8BFB');
  if (similarity > 0.8) {
    console.error('颜色相似度过高，色盲用户无法区分');
  }
  ```
- 修复：替换为差异更大的颜色

**步骤 3：检查轴刻度标签（#3）**
- 统计轴刻度数量：
  ```javascript
  const yAxisTicks = document.querySelectorAll('.y-axis .tick');
  if (yAxisTicks.length < 3) {
    console.warn('Y 轴刻度少于 3 个，可能导致读数困难');
  }
  ```
- 修复：调整 `splitNumber` 或 `interval` 确保至少 3-5 个刻度

**步骤 4：检查 3D 效果（#4）**
- 扫描 ECharts 配置，查找 3D 相关属性：
  ```javascript
  if (option.series.some(s => s.shading === 'lambert' || s.dimension === 3)) {
    console.error('发现 3D 效果，应使用纯扁平化设计');
  }
  ```
- 修复：移除 `shading`、`light` 等 3D 属性

**步骤 5：检查 Tooltip 单位（#5）**
- 验证 Tooltip 内容是否包含单位：
  ```javascript
  const tooltipText = getTooltipContent();
  if (!/\d+\s*(万|亿|元|个|人|次|%)/.test(tooltipText)) {
    console.warn('Tooltip 缺少单位，可能造成歧义');
  }
  ```
- 修复：在 formatter 中添加单位

**步骤 6：检查装饰性图表（#6）**
- 审查 KPI 卡片中的微型图表：
  - 是否有明确的趋势意义？
  - 还是仅为装饰？
- 修复：移除无意义的微型图表，或替换为有意义的趋势数据

**步骤 7：检查装饰性网格线（#7）**
- 扫描 ECharts 配置，查找不必要的网格线：
  ```javascript
  if (option.xAxis.splitLine?.show) {
    console.warn('X 轴不应显示分割线，仅 Y 轴需要');
  }
  ```
- 修复：设置 `xAxis.splitLine.show: false`

**步骤 8：检查移动端列数（#8）**
- 在 <728px 宽度下检查图表格列数：
  ```css
  @media (max-width: 727px) {
    .chart-grid {
      grid-template-columns: 1fr !important; /* 强制 1 列 */
    }
  }
  ```
- 修复：确保移动端不超过 2 列

**步骤 9：生成检查报告**
- 汇总所有检查结果：
  ```
  ❌ 使用了 3 种字重（超过限制的 2 种）
  ✅ 颜色相似度合格
  ✅ 轴刻度数量合格
  ❌ 发现 3D 饼图效果
  ...
  通过率: 6/8 = 75%
  ```
- 优先修复高危项（#4 3D 效果、#2 颜色相似度）

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 艺术性可视化（如数据艺术、信息海报）
- 特殊行业需求（如金融 K 线图需要 3D 效果）
- 故意追求多样性的营销活动

**作者的盲点**：
- 未讨论某些禁忌的例外情况（如在什么情况下可以使用 3D 效果）
- 未说明如何将 8 条禁忌转化为自动化 lint 规则
- 未提及历史遗留的不合规设计如何处理（重构优先级）

**失败模式警示**：
- **过度严格**：将所有设计选择都列为禁忌，导致设计师束手束脚
- **误报率高**：自动化检查工具过于敏感，标记大量非问题
- **忽视上下文**：不考虑业务场景，机械地应用禁忌清单

**相关 skills**：
- `clarity-first-principles` — 清晰性优先原则
- `consistency-principles` — 一致性至上原则
- `3d-pie-chart-trap` — 3D 饼图陷阱（具体反例）
- `y-axis-non-zero-trap` — Y 轴不从零的误导（具体反例）
