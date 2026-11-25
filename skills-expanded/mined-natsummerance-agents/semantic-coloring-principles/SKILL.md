---
name: semantic-coloring-principles
description: |
  当用户需要为数据赋予业务含义的颜色时使用。触发场景：用户问"成功/失败应该用什么颜色？"、"KPI 上涨用绿色还是红色？"、"如何设计告警系统的颜色？"。不适用于：纯装饰性配色、无业务含义的数据系列。关键 trigger 信号：语义色 / 业务含义 / 成功失败 / 告警颜色 / KPI 趋势。
source_book: 《ENCY-charts 数据可视化设计规范》 ENCY Design Team
source_chapter: 2.3 语义色 + 4.2 KPI Card + 7. Do's and Don'ts
tags: [semantic-colors, business-meaning, status-indicators, accessibility]
related_skills: [categorical-palette-glossary, clarity-first-principles, kpi-card-glossary]
---

# Semantic Coloring Principles（语义化配色原则）

## R (Reading) — 原文引用

> "语义色: --chart-success: #00B42A; --chart-warning: #FF7D00; --chart-danger: #F53F3F; --chart-info: #2469FF"

> "阈值/标记色: --chart-target-line: #F53F3F; --chart-average-line: #86909C; --chart-baseline: #E5E6EB"

> "KPI Card: .kpi-card__trend--up { color: var(--chart-success); } .kpi-card__trend--down { color: var(--chart-danger); }"

## I (Interpretation) — 方法论骨架

这是**将颜色与业务状态映射的设计原则**，确保用户能够通过颜色快速理解数据的业务含义。

**四条子原则**：
1. **业务含义映射原则**：颜色必须承载业务语义（成功/警告/危险/信息）
2. **文化一致性原则**：遵循目标用户的文化习惯（如红色=危险/下跌，绿色=成功/上涨）
3. **色盲友好原则**：不依赖单一颜色传达信息，配合图标/文字辅助
4. **阈值可视化原则**：用特定颜色标记关键阈值线（如目标线用红色）

**核心价值**：
- 快速理解：用户通过颜色立即判断业务状态
- 减少认知负荷：无需阅读文字即可获取关键信息
- 跨文化一致：遵循通用文化习惯，降低学习成本

## A1 (Past Application) — 书中作者用过的案例

在 ENCY-charts 规范中，作者定义了完整的语义色体系：
- **四态颜色**：成功（#00B42A 绿）、警告（#FF7D00 橙）、危险（#F53F3F 红）、信息（#2469FF 蓝）
- **KPI 趋势**：上涨用绿色（--chart-success），下跌用红色（--chart-danger）
- **阈值线**：目标线用红色（--chart-target-line），平均线用灰色（--chart-average-line）
- **辅助编码**：趋势标识同时使用颜色 + 箭头图标，确保色盲用户可理解

## A2 (Future Trigger) — 何时调用此 skill

**调用场景**：
- 设计师问"告警系统应该用什么颜色？"
- 产品经理说"KPI 上涨用绿色还是红色？不同文化习惯不一样"
- 前端工程师问"如何设计阈值线的颜色？"
- 测试人员说"色盲用户反馈无法区分状态，怎么办？"

**与相邻 skill 的区分**：
- 与 `categorical-palette-glossary` 的区别：本 skill 解决"有业务含义的颜色"，后者解决"区分数据系列的颜色"
- 与 `clarity-first-principles` 的区别：本 skill 专注配色的语义映射，后者关注整体清晰度

**关键 trigger 词**：语义色 / 业务含义 / 成功失败颜色 / 告警颜色 / KPI 趋势色 / 阈值线颜色

## E (Execution) — 可执行步骤

**步骤 1：定义四态语义色**
- 根据业务需求和文化习惯定义：
  ```css
  :root {
    --chart-success: #00B42A;  /* 成功/上涨/正常 */
    --chart-warning: #FF7D00;  /* 警告/注意 */
    --chart-danger: #F53F3F;   /* 危险/下跌/异常 */
    --chart-info: #2469FF;     /* 信息/中性 */
  }
  ```
- 文化适配：
  - 中国市场：红色=下跌/危险，绿色=上涨/成功（股市习惯）
  - 欧美市场：绿色=上涨/成功，红色=下跌/危险（通用习惯）
  - 如有多地区用户，提供配置项允许切换

**步骤 2：定义阈值标记色**
- 为关键阈值线定义专用颜色：
  ```css
  :root {
    --chart-target-line: #F53F3F;   /* 目标线（红色，强调） */
    --chart-average-line: #86909C;  /* 平均线（灰色，中性） */
    --chart-baseline: #E5E6EB;      /* 基线（浅灰，参考） */
  }
  ```

**步骤 3：应用语义色到组件**
- KPI 趋势标识：
  ```css
  .kpi-card__trend--up {
    color: var(--chart-success);  /* 绿色 */
  }
  .kpi-card__trend--down {
    color: var(--chart-danger);   /* 红色 */
  }
  ```
- 告警状态：
  ```html
  <span class="status-badge status-success">正常</span>
  <span class="status-badge status-warning">警告</span>
  <span class="status-badge status-danger">异常</span>
  ```

**步骤 4：添加辅助编码（色盲友好）**
- 不依赖单一颜色，配合图标或文字：
  ```html
  <!-- 错误做法：仅用颜色 -->
  <span style="color: green;">↑ 5%</span>
  
  <!-- 正确做法：颜色 + 图标 + 文字 -->
  <span class="trend-up">
    <svg class="icon-arrow-up"></svg>
    ↑ 5%
  </span>
  ```
- 验证工具：使用 Coblis 色盲模拟器检查可区分性

**步骤 5：验证语义色使用**
- 检查清单：
  - [ ] 所有状态都有对应的语义色
  - [ ] 文化习惯一致（如红色=危险）
  - [ ] 有色盲友好的辅助编码（图标/文字）
  - [ ] 对比度 ≥4.5:1
  - [ ] 未滥用语义色（仅用于有业务含义的场景）

## B (Boundary) — 边界与盲点

**什么时候不适用**：
- 纯装饰性配色（如图表美化、艺术可视化）
- 无业务含义的数据系列（应使用分类色板）
- 特殊行业规范（如医疗、航空有专用颜色标准）

**作者的盲点**：
- 未讨论多文化环境下的颜色冲突解决方案
- 未说明语义色的数量限制（超过 4 态是否还可管理？）
- 未提及动态主题下的语义色适配（如暗色模式是否需要调整饱和度？）

**失败模式警示**：
- **文化冲突**：在中国用红色表示上涨（违反股市习惯），导致用户困惑
- **过度使用**：将语义色用于无业务含义的场景，稀释其语义价值
- **单一编码**：仅依赖颜色传达状态，色盲用户无法理解

**相关 skills**：
- `categorical-palette-glossary` — 分类色板
- `clarity-first-principles` — 清晰性优先原则
- `kpi-card-glossary` — KPI 指标卡
