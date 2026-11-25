---
name: design-system-generator
description: |
  从产品类型与品牌调性推理生成三层 Design Token 系统（primitive→semantic→component），输出 CSS 变量、暗色主题与组件状态规格。触发场景：用户说"给这个 SaaS 后台建一套设计系统"、"生成 design token / CSS 变量"、"色板字号间距圆角体系怎么定"、"要支持暗色模式换肤"。不适用于：单张 banner/社媒素材设计、一次性营销视觉。
source_project: nextlevelbuilder/ui-ux-pro-max-skill
tags: [design-tokens, css-variables, design-system, theming, ui-architecture]
---

# Design System Generator（三层 Design Token 生成器）

## R (Reading) — 源项目核心设计

> "Three-layer token system for scalable, themeable design systems." —— 分层结构为 `Primitive (raw values) ↓ Semantic (purpose aliases) ↓ Component (component-specific)`，"Semantic layer enables theme switching (light/dark)"。
> 最佳实践："Never use raw hex in components - always reference tokens"；"Use HSL format for opacity control"；命名约定 `--{category}-{item}-{variant}-{state}`。

（来源：`cli/assets/skills/design-system/SKILL.md` 与 `cli/assets/skills/design-system/references/token-architecture.md`）

## I (Interpretation) — 方法论骨架

这是一个**从产品定位推导可换肤 token 架构**的方法，核心洞察是：把"值"和"用途"解耦成三层，改主题时只动语义层，组件层永远引用变量而非硬编码。

1. **产品画像先行**：先确定产品类型（SaaS 后台 / 电商 / 作品集）与目标用户气质，决定风格关键词——而不是先挑颜色。
2. **三个设计拨盘量化口味**：variance（克制↔大胆）、motion（静止↔复杂动效）、density（疏朗↔仪表盘密集），各取 1-10，低中高三档分别映射不同风格族。
3. **自底向上三层构造**：
   - Primitive：原始值（`--color-blue-600`、`--space-4`、`--radius-lg`），几乎不变更；
   - Semantic：用途别名（`--color-primary: var(--color-blue-600)`），暗色模式只覆盖这一层；
   - Component：组件级（`--button-bg: var(--color-primary)`），支持单组件定制。
4. **状态矩阵补全**：每个关键属性给出 Default/Hover/Active/Disabled 四态取值（如 Background: primary → primary-dark → primary-darker → muted）。
5. **双格式交付**：CSS 变量文件 + W3C DTCG JSON（`$value`/`$type`），后者供工具链消费。
6. **机器可验证**：生成后扫描源码中的硬编码十六进制值作为合规检查，这是该方法的闭环关键。

## A1 (Past Application) — 源项目的典型应用

### 案例: generate_design_system("SaaS dashboard") 聚合推荐
- **输入**: 产品描述"SaaS dashboard"+ 项目名，可选 persist 落盘。
- **做法**: 上游脚本按固定配额聚合多域搜索（product 取 1 条、style 取 3 条、color 取 5 条、landing 取 2 条、typography 取 2 条），套用 ui-reasoning.csv 的决策规则，产出 16 个语义色槽位（Primary/On Primary/Accent/Background/Card/Muted/Border/Destructive/Ring 等）的完整建议与 CSS 变量定义。
- **结果**: 一份可直接 import 的 token 文件 + 风格/字体配对依据，项目里三个示例工程（saas-landing、healthcare-dashboard、portfolio-dark）即按此流程产出。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 新项目冷启动："从零给我这个产品设计一套颜色/字体/间距体系"。
2. 存量重构："代码里全是写死的 #2563EB，帮我抽成 design token 并支持暗色模式"。
3. 多端一致性："几个页面配色各画各的，需要一个统一 token 来源"。

### 语言信号
- "建一套设计系统 / 设计规范"
- "生成 CSS 变量 / design tokens"
- "怎么支持暗色模式一键换肤"
- "色板、字号阶梯、圆角、阴影这些基础值定一下"

### 与相邻 skill 的区分
- 与 banner-design 的区别：本 skill 产出**跨页面复用的系统性 token 架构**；banner-design 产出**单张特定尺寸的创意素材**。用户要"体系"找这里，要"一张图"找那里。

## E (Execution) — 可执行步骤

1. **产品画像与拨盘确认** — 记录产品类型、目标用户，并与用户确认 variance/motion/density 三档（未确认时默认 5/5/5）。完成标准: 一句话能写出"面向 X 的 Y 类产品，风格档位 (v,m,d)=(?, ?, ?)"。
2. **推导 Primitive 层** — 给出灰阶、品牌主色阶、4px 基准间距梯（--space-1/2/4/6…）、字号阶、圆角阶、阴影阶。完成标准: 每个 primitive 有命名、有值、有注释用途。
3. **映射 Semantic 层** — 把 primitive 别名化为主色/前景/背景/muted/destructive/ring 等槽位，并写出 `.dark` 覆盖块。完成标准: 语义层不含任何裸十六进制值，全部 `var()` 引用；`.dark` 只改语义层。
4. **派生 Component 层与状态矩阵** — 至少覆盖 button/input/card 三类，属性×四态填表。完成标准: 表格无空格，每格均为语义 token 引用。
5. **双格式输出** — 生成 `tokens.css`（分层注释单文件或四文件组织）与 DTCG JSON。完成标准: 两份文件字段一一对应，JSON 通过 `$value/$type` 结构校验。
6. **合规扫描** — 在目标源码目录检查残留硬编码颜色/字号。完成标准: 扫描报告为零硬编码，或逐条列出豁免理由。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- 单张 banner、封面、广告素材的创意设计 → 走 banner-design。
- 图表数据可视化的选型与禁忌审查 → 属于可视化专用技能，本 skill 只提供被其消费的基础色板。
- 组件的业务逻辑实现、交互状态机编码 → 本 skill 止步于视觉规格。

### 已知局限 / 失败模式（≥1条真实的）
- 拨盘拉到极端组合（如 variance=10 + density=10）时，上游风格关键词可能互相冲突，产出需要人工仲裁；
- token 目录来自上游 CSV 语料，时效依赖上游更新，新兴风格可能查不到；
- 合规扫描只能发现"字面硬编码"，对运行时拼接的颜色字符串无法静态检出。

## 相关 skills
- composes-with: banner-design（banner 设计时注入本 skill 产出的品牌 token 保持一致）
- contrasts-with: banner-design（系统性架构 vs 单件创意资产）

---

## 审计信息
- **验证**: V1 ✓ / V2 ✓ / V3 ✓
- **蒸馏时间**: 2026-08-25；**来源**: local `vendor/nextlevelbuilder__ui-ux-pro-max-skill/` 下 `cli/assets/skills/design-system/SKILL.md`、`cli/assets/skills/design-system/references/token-architecture.md`、`src/ui-ux-pro-max/scripts/design_system.py`（前 80 行）、根 `CLAUDE.md`
