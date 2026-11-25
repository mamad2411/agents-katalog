---
name: frontend-brand
description: 为已有前端项目做品牌视觉交付：Logo 生图提示词包（prompt 交付，用户自选模型生图）、OG 社交分享图（1200x630 代码渲染）、Landing page 设计（调度 graphite landing 骨架）。当用户说「做个 logo」「设计 logo」「生成 OG 图/分享图」「做落地页/landing」「品牌视觉」时触发。基于项目既有设计体系提取品牌基因（brand-profile.md），不凭空设计。与 brandkit（纯出图引擎）分工：本 skill 交付工程集成的 prompt 包与代码产物，需要直接生成品牌板图片时可转 brandkit。
---

# frontend-brand · 品牌视觉交付入口

## Mandate

为**已有前端项目**做品牌视觉交付——先从项目既有设计体系里提取品牌基因（`brand-profile.md`），再据此产出三类**工程集成物**：Logo 生图提示词包、OG 社交分享图、Landing page。不凭记忆手搓一套新视觉，也不产出与项目现有 token 打架的东西。

**何时触发本 skill**：用户说「做个 logo」「设计 logo」「生成 OG 图 / 分享图」「做落地页 / landing」「品牌视觉」。

**不替代什么**：
- **与 brandkit 分工**：本 skill 交付**工程集成的 prompt 包与代码产物**（可接线、可复现、标题文字精确）；用户要的是直接落地的**品牌板 / 视觉世界图片**时，转 `brandkit`（纯出图引擎），不要在这里硬凑出图。
- **与 frontend-launch 分工**：OG meta 接线、favicon、sitemap、SEO 落地归 `frontend-launch`；本 skill 只做到「产物落约定路径」为止。

## 库根与前置（先确认这一步）

- 库根：`~/frontier`；本 skill 的 references 根 `~/frontier/skills/frontend-brand/references/`。
- 三个交付模块各挂一份 reference（`logo-prompts.md` / `og-image.md` / `landing.md`），完整路径见「工作流五步」的路由表。
- **与 frontend-launch 的交接单源**：两 skill 经消费方项目的 `docs/brand/brand-profile.md` 交接品牌基因——**谁先跑谁生成**，之后**已存在则复用不覆盖**；用户可显式要求重建。提取逻辑的正文在下文「brand-profile 提取步骤」，frontend-launch 指向本节、不复制正文。
- **库缺失时的行为**：若 `~/frontier` 不存在，**停下来问用户库的位置**（本地路径或 git 地址），不要自行猜测路径、不要跳过、不要临时另起一套体系。拿到位置后把下文所有 `~/frontier` 替换为实际库根再继续。

## 工作流五步

每步给出「判断依据」与「产出」，逐步推进，不跳步。

### 1. 确保 brand-profile 存在

- **判断依据**：查消费方 `docs/brand/brand-profile.md`。存在且色值未漂移 → 复用；不存在 → 按下文「brand-profile 提取步骤」生成；用户要求重建 → 重跑提取覆盖旧档。
- **产出**：一份可用的 `brand-profile.md`——本 session 后续所有模块的**唯一事实源**。

### 2. 按用户诉求路由模块

- **判断依据**：按用户要什么查下表，只读命中的那一份 reference，别三份全读。

| 用户诉求 | 读哪份 reference（完整路径） | 什么时候读 |
| --- | --- | --- |
| Logo / 品牌标记 | `~/frontier/skills/frontend-brand/references/logo-prompts.md` | 要 logo 概念与生图提示词包时 |
| OG 图 / 社交分享图 | `~/frontier/skills/frontend-brand/references/og-image.md` | 要 1200x630 社交分享图时 |
| Landing page | `~/frontier/skills/frontend-brand/references/landing.md` | 要营销落地页时（调度 graphite landing 骨架） |

- **产出**：确定要执行的模块及其 reference 路径。

### 3. 执行模块产出

- **判断依据**：严格按命中 reference 的步骤执行；reference 里的模型能力矩阵**只是路由起点**，选模型 / 参数前以官方文档现查为准（见「坑位沉淀」）。
- **产出**：logo prompt 包 / OG 模板 + 成图 / landing 页，取决于命中的模块。

### 4. 产物落项目约定路径

- **判断依据**：按下文「产物路径」表把每类产物写到项目约定位置，不散落、不改名。
- **产出**：产物就位，`git status` 可见。

### 5. 提示后续

- **判断依据**：本 skill 到「产物落地」为止；OG meta 接线、favicon、sitemap、SEO 归 `frontend-launch`。
- **产出**：一句「后续接线 / SEO 走 frontend-launch」的收尾提示，别让用户以为 OG 图放好文件就自动生效。

## brand-profile 提取步骤

这是 frontend-brand 与 frontend-launch **共用的先决逻辑**，正文在此、可独立执行；frontend-launch 指向本节而不复制。两条路径按项目形态二选一，末尾都要问用户两个问题，最后写出固定的九节 `brand-profile.md`。

### 快速路径（graphite 项目）

读三处，抽字段：

1. `~/frontier/templates/graphite/declarations/design.md`——色板哲学与 token 分级（必填 / 可调 / 勿改）、soft monochrome 灰阶策略。
2. 消费方 `src/index.css` 顶部两块 token（`:root` 与 `[data-theme='dark']`）——抽**当前实际色值**（项目可能已换过品牌），主色三件套 + 三语义色 + 灰阶特征。**若消费方 `src/index.css` 是 `@import` 转发**（未物理复制骨架、直接引用库内 skeleton 源，如库内 demo 消费方写 `@import '../../skeleton/src/index.css'`），该文件里**没有** `:root` / `[data-theme='dark']` 块——顺 `@import` 读被导入的那个 `index.css`（即 `~/frontier/templates/graphite/skeleton/src/index.css`）取 token，别停在转发文件上误判为「无 token」。
3. `~/frontier/templates/graphite/declarations/craft.md`——密度基调、圆角与描边、动效强度。

### 通用推断路径（非 graphite 项目）

读并抽样推断：

1. tailwind 配置（`tailwind.config.*` 的 `theme.extend.colors` / `borderRadius`）或主 CSS 变量文件——推断**色板与圆角哲学**。若项目既无 tailwind 配置也无 CSS 变量（纯手写色值 / CSS-in-JS），退到组件渲染态抽样主色，并向用户逐项确认色值后写入 profile。
2. 主要组件抽样（按钮 / 卡片 / 输入框）——推断**描边 vs 阴影取向、密度、图形语言**。
3. 字体接法（`@font-face` / `next/font` / CSS `font-family`）——只归纳**风格词**，不照抄字体名。

### 两路都要问用户

以下两项无法从代码推断，**必须问用户**，不要替用户编：

- **产品一句话定位**（做什么、给谁解决什么问题）。
- **目标受众**（谁在用）。

### 固定产出章节（写进 `brand-profile.md`）

按序写九节，缺一不可：

1. **品牌名**
2. **一句话定位**
3. **受众**
4. **色板**——主色、语义色（success / warning / danger）、灰阶特征，**每项带色值**（oklch / hex）。
5. **气质关键词**（3–6 个）
6. **字体风格词**——写 `geometric sans-serif` / `humanist serif` 这类**描述**，**不写具体字体名**。
7. **密度**——紧凑 / 舒适 / 稀疏，含间距基调。
8. **图形语言**——圆角与描边哲学（圆角档位、描边优先还是阴影优先）。
9. **生成方**——生成它的 skill 名（`frontend-brand` 或 `frontend-launch`）与生成日期。

## 产物路径

| 产物 | 约定路径 | 备注 |
| --- | --- | --- |
| brand-profile | `docs/brand/brand-profile.md` | 品牌基因单源；**已存在复用不覆盖**，用户可要求重建 |
| OG 模板 | `docs/brand/og-template.html` | 1200x630 代码渲染模板，可复现、可迭代 |
| OG 图 | `public/og-image.png` | 从模板渲染出的成图，标题文字精确 |
| Logo prompt 包 | 对话输出 + `docs/brand/logo-prompts.md` | 先在对话里交付，同时存档供用户留档迭代 |

## 坑位沉淀（体系性不可犯的错）

初始条目如下，随仓库演进增补：

- **模型矩阵是路由起点、不是终点**：references 里的模型能力矩阵调研于 **2026-07-20**，图像模型迭代很快——选模型 / 定参数前**以官方文档现查为准**，不要把矩阵当长期权威依赖。
- **色值漂移要提示重建**：`brand-profile.md` 的色值与项目 `src/index.css` 当前 token 不一致时（项目换过品牌），**提示用户重建 profile**，别拿旧色值继续往下做。
- **OG 图不走生图**：OG 的标题 / 品牌名文字必须精确，一律**代码渲染**（HTML → PNG），**不用文生图模型**——生图模型出的文字会糊、会错字。
- **SVG 草图不是交付物**：logo 环节的 SVG 只用于**构图沟通**（比例 / 版式讨论），最终 logo 走 prompt 包 + 用户自选模型出图；别把手搓 SVG 当成品交付。
- **禁 emoji**：全部产物（brand-profile、prompt 包、OG 模板、landing）与本 skill 的输出一律不得出现 emoji，用图标组件或纯文字替代。注意 graphite 的 `check:ui` emoji 护栏只扫 `--source` 指定的 `src/` 树；本 skill 产物多落在 `src/` **之外**（`docs/brand/*.html`、`docs/brand/*.md`、项目根 `index.html`、`public/*`），不在自动扫描范围内——这些产物的禁 emoji 靠人工把关，别默认护栏会兜住。

## 库内导航

- 三个模块 reference：`~/frontier/skills/frontend-brand/references/{logo-prompts,og-image,landing}.md`
- 兄弟 skill：`frontend-templates`（选骨架 / 注入设计体系）、`frontend-launch`（接线 / SEO / 部署）
- graphite 事实源（提取快速路径读）：`~/frontier/templates/graphite/declarations/{design,craft}.md` + 消费方 `src/index.css`
