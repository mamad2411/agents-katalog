---
name: ai-friendly-spec-framework
description: |
  当用户需要编写让 AI 代理能够准确理解的设计规范时使用。触发场景：用户问"如何让 AI 理解我的设计规范？"、"AI 生成的代码总是不符合规范怎么办？"、"如何编写 AI 友好的设计文档？"。不适用于：纯人工阅读的设计规范、非 AI 辅助开发的场景。关键 trigger 信号：AI 友好 / Agent Prompt / Quick Reference / Iteration Guide / AI 生成代码质检。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 9. Agent Prompt Guide
tags: [ai-prompt-engineering, design-spec, agent-workflow, quality-check]
related_skills: [ai-iteration-check-principles, design-token-architecture, chart-type-selection-framework]
---

# AI-Friendly Specification Framework（AI 友好的规范编写框架）

## R (Reading) — 原文引用

> "Quick Reference: ENCY Charts: 8 分类色板, 7 级顺序色板, 3 种卡片类型 (KPI/Micro/Chart), 4 断点, 图表卡片圆角 8px/边框 #E5E6EB/阴影 xs, Tooltip 暗底白字 rgba(29,33,41,0.92), 品牌主色 #2469FF, DIN Alternate 数字字体, 最小卡片 280px, 图表最小高度 200px."

> "Component Prompts: Prompt 1: 生成 KPI 指标卡片组... Prompt 2: 生成多系列柱状图... Prompt 3: 生成仪表盘概览页面..."

> "Iteration Guide: 1. 颜色第一位 2. 卡片是基本单位 3. Tooltip 不离散 4. 数据为空先处理 5. 移动端先考虑 6. 动画不超过 1 秒 7. 单位不可省 8. 图例排序与数据一致 9. 暗色模式双色板 10. 可访问性必检"

## I (Interpretation) — 方法论骨架

这是一个**让 AI 代理能够准确理解并执行设计规范的结构化框架**，通过三件套降低 AI 解析规范的难度：

**三件套架构**：
1. **Quick Reference（快速参考）**：用一句话压缩核心规则
   - 格式："名称: 关键数字/颜色/尺寸, 名称: 关键数字/颜色/尺寸..."
   - 作用：提供压缩版知识，降低 AI 上下文窗口压力
2. **Component Prompts（组件提示词）**：提供典型场景的完整 prompt 模板
   - 包含：布局要求 + 样式细节 + 响应式规则
   - 作用：提供完整上下文，减少 AI 猜测
3. **Iteration Guide（迭代指南）**：列出 AI 生成代码后的检查清单
   - 10 条必检项：覆盖颜色、容器、Tooltip、空数据、移动端、动画、单位、图例、暗色模式、可访问性
   - 作用：提供自检清单，减少人工返工

**核心价值**：
- 降低 AI 误解概率：Quick Reference 提供压缩版知识
- 提高生成质量：Component Prompts 提供完整上下文
- 减少返工次数：Iteration Guide 提供自检清单

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范第 9 章，作者提供了完整的 AI 友好化示例：
- **Quick Reference**：用一句话总结 8 分类色板、7 级顺序色板、3 种卡片类型等核心规则
- **Component Prompts**：提供 5 个典型场景的完整 prompt（KPI 卡片组、多系列柱状图、仪表盘概览、饼图/环形图、时序折线面积图）
- **Iteration Guide**：列出 10 条必检项，如"颜色第一位"、"卡片是基本单位"、"单位不可省"等

这种结构使得 AI 能够快速理解规范并生成符合要求的代码。

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"如何编写让 AI 能理解的设计规范？"
- 前端工程师说"AI 生成的图表样式总是不对，怎么改进？"
- 技术负责人说"我们需要建立 AI 辅助开发的工作流"
- 产品经理问"如何让 AI 自动生成符合品牌规范的 Dashboard？"

**与相邻 skill 的区分**：
- 与 `design-token-architecture` 的区别：本 skill 解决"如何让 AI 理解规范"，后者解决"如何组织 CSS 变量层级"
- 与 `ai-iteration-check-principles` 的区别：本 skill 提供完整的三件套框架，后者仅提供 10 条检查清单（是本 skill 的子集）

**关键 trigger 词**：AI 友好规范 / Agent Prompt / Quick Reference / Component Prompts / Iteration Guide / AI 生成代码质检

## E (Execution) — 可执行步骤

**步骤 1：编写 Quick Reference（快速参考）**
- 用一句话总结核心规则，格式为"名称: 值, 名称: 值..."
- 示例：
  ```
  ENCY Charts: 8 分类色板, 7 级顺序色板, 3 种卡片类型 (KPI/Micro/Chart), 
  4 断点, 图表卡片圆角 8px/边框 #E5E6EB/阴影 xs, 
  Tooltip 暗底白字 rgba(29,33,41,0.92), 品牌主色 #2469FF
  ```
- 原则：只保留最关键的数字和颜色，省略次要细节

**步骤 2：编写 Component Prompts（组件提示词）**
- 为每个典型场景编写完整的 prompt 模板
- 必须包含：
  - 布局要求（Grid 列数、间距）
  - 样式细节（颜色、字体、圆角、阴影）
  - 响应式规则（断点适配）
- 示例（KPI 卡片组）：
  ```
  基于 ENCY Charts 设计系统，生成一组 KPI 指标卡片（4-6个）。
  使用 Grid 布局，卡片包含：label (12px/#86909C), value (28px/600),
  trend indicator (11px, up=#00B42A, down=#F53F3F)。
  支持响应式：XL 6列 / L 4列 / M 3列 / S 2列 / XS 1列。
  每个卡片可选嵌入 40px 高的 Micro Chart (迷你折线图)。
  ```

**步骤 3：编写 Iteration Guide（迭代指南）**
- 列出 10 条必检项，每条必须是可执行的检查点
- 示例：
  1. 颜色第一位 — 生成图表前先确认用哪种色板（分类/顺序/语义）
  2. 卡片是基本单位 — 所有图表必须包裹在 .chart-card 容器中
  3. Tooltip 不离散 — 确保 Tooltip 始终指向数据且不超出视口
  4. 数据为空先处理 — 检测空数据时自动渲染空状态占位
  5. 移动端先考虑 — 优先使用 grid-auto-rows + minmax 实现灵活布局
  6. 动画不超过 1 秒 — animationDuration 默认 800ms
  7. 单位不可省 — 所有数值显示必须包含单位 (万/亿/元/个/人/次)
  8. 图例排序与数据一致 — Legend 顺序严格匹配数据系列顺序
  9. 暗色模式双色板 — 检测 [data-theme="dark"] 时切换暗色主题色板
  10. 可访问性必检 — 色盲友好、对比度 ≥4.5:1、键盘可操作

**步骤 4：整合三件套到规范文档**
- 将 Quick Reference 放在文档顶部，作为快速参考
- 将 Component Prompts 放在中间，作为典型场景示例
- 将 Iteration Guide 放在末尾，作为质检清单
- 确保三者之间的一致性（Quick Reference 中的规则在 Component Prompts 中体现，在 Iteration Guide 中检查）

**步骤 5：测试 AI 生成效果**
- 使用 Component Prompts 让 AI 生成代码
- 使用 Iteration Guide 逐项检查生成结果
- 记录失败案例，优化 Quick Reference 和 Component Prompts
- 迭代直到 AI 生成合格率 ≥80%

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 纯人工阅读的设计规范（无需考虑 AI 解析能力）
- 规范内容极其简单（无需 Quick Reference 压缩）
- AI 已经经过充分训练，能完美理解原始规范

**作者的盲点**：
- 未讨论不同 AI 模型（GPT-4 vs Claude vs Gemini）的解析差异
- 未说明如何处理规范的版本更新（AI 缓存了旧版 Quick Reference）
- 未提及多语言规范的 AI 友好化策略

**失败模式警示**：
- **Quick Reference 过度压缩**：丢失关键信息，导致 AI 误解
- **Component Prompts 不够典型**：覆盖场景不全，AI 遇到新场景仍会出错
- **Iteration Guide 不可执行**：检查项过于抽象，无法自动化验证

**相关 skills**：
- `ai-iteration-check-principles` — AI 迭代检查原则（本 skill 的子集）
- `design-token-architecture` — 设计系统 Token 架构
- `chart-type-selection-framework` — 图表类型选择决策框架
