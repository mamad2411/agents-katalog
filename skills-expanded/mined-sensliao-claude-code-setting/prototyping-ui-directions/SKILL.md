---
name: prototyping-ui-directions
description: Create non-production UI/UX direction prototypes from product ideas, including HTML/React mocks, palette and token candidates, visual variants, comparison reports, and review-ready prototype packages.
type: orchestrator
version: 1.0.0
stages: 4
output: per-variant prototype package — HTML/React mocks + palette.json + token-candidates + comparison report
---

# Prototyping UI Directions — 主入口

> **干什么的**：把一个产品 idea 做成 **non-production UI/UX direction prototypes** — 包括 HTML/React mocks、palette 与 token 候选、视觉 variant、direction 对比报告，最终打包成 **review-ready prototype packages** 供决策审阅。
>
> **不干什么**：不写最终生产代码、不做组件库实施、不做测试 / 合流 / 部署。Prototype 是用来**做方向决策**的，不是用来直接上线的。后半段交给用户自己的工程流程。

> **在 UIUX 调度引擎里的位置（v1.0 升产，2026-06-10）**：本 skill 是 [`uiux-product-orchestrator` 组合引擎](../uiux-product-orchestrator/references/combination-policy.md) **P1 EXPLORE 阶段的承重 owner** —— 负责"先出几版给用户挑"。三条硬约束:
> 1. **参考接地是上游硬前置**:进 EXPLORE 前必须有 `design/grounding.md`（P0 GROUND 产物）。本地 58 品牌 DESIGN.md（**直接读语料根** `<LOCAL_ROOT>/awesome-design-md/design-md/<slug>/DESIGN.md`，查找表见 [`local-template-index.md`](../uiux-product-orchestrator/references/local-template-index.md)）+ 产品 archetype 的 `reference-anchors.md` 优先，本地无品类匹配才走 web。**不接地不出 variant**（根治凭空生造）。
> 2. **产品 archetype 已全建成**（v1.0）:`canvas` / `landing-marketing` / `data-dashboard` / `game-style` / `bubble-physics` / `creative-eye` / `narrative-scrolly` 七型齐备。Stage 0 按产品类型加载,variant 必须套对应 archetype 的 pattern + reference-anchors。
> 3. **红队 gate（Stage 3）单 agent 模式**:显式路由 `taste-skill` 当 anti-slop 守门人，不假设独立 red-team owner 存在。

## 调用即做的两件事

每次本 skill 被触发：

### 1. 读 state

```
Read state/checkpoint.json
```

文件不存在 = 还没开过 idea intake → 进 Stage 0。

### 2. 派路由

按下表决定下一步：

| 当前状态 | 下一步 |
|---------|--------|
| `current_stage = -1` (未初始化) | 进 `workflows/stage0-idea-intake.md` |
| `stage_0` 未完成 | 继续 Stage 0 |
| `stage_0 gate_passed`，`stage_1` 未开始 | 用户确认后进 Stage 1 |
| `stage_1` 进行中 | 路由到 `workflows/stage1-reference-acquisition.md` |
| `stage_1 gate_passed`，`stage_2` 未开始 | 进 Stage 2 |
| `stage_2` 进行中 | 路由到 `workflows/stage2-research-analysis.md` |
| `stage_2 gate_passed`，`stage_3` 未开始 | 进 Stage 3 |
| `stage_3` 进行中 | 路由到 `workflows/stage3-prototype-package.md` |
| `stage_3 gate_passed` | 报告 done，等用户开新轮或下载产物 |

## 4 阶段一览

```
Stage 0 — Idea Intake             产物：idea-brief.md
  │  跟用户聊：要做什么类型产品？氛围？参考方向？
  │  选 dimension 重点（视觉/交互/动画/视角/响应式/a11y）
  │  选是否加载 product archetype（canvas / dashboard / landing / ...）
  ↓
Stage 1 — Reference Acquisition   产物：reference/<vendor>/* + reference-manifest.md
  │  跟用户敲定要研究的具体参考清单
  │  skill 自己跑 git clone / 截图 / 抓 wiki，落到 reference/ 下
  │  写 manifest 注明每个 reference 的来源 + license + 研究意图
  ↓
Stage 2 — Research & Analysis     产物：research/{cross-ref.md, direction-candidates.md}
  │  从每个 reference 提取选中 dimension 上的 pattern / palette / typography / motion
  │  整理 cross-reference matrix
  │  收敛出 N 个 direction 候选（≥3，每个含调色板 + 风格基调 + 关键 pattern）
  ↓
Stage 3 — Prototype Package Generation
                                  产物：prototypes/variant-<N>/{index.html|tsx, palette.json, token-candidates.*, surface-*.html|tsx, readme.md}
                                  + comparison-report.md (variant 横向比较)
   并行跑每个 direction
   每 variant 输出 prototype package：
     - index.html (或 index.tsx)  主入口（产品门面 prototype）
     - palette.json              调色板（机器可读）
     - palette.html              调色板可视化
     - token-candidates.{css,json}  完整 design token 候选（color + type + spacing + radius + motion）
     - surface-*.html (或 .tsx)  关键 surface 的 mock（HTML 或 React 任选）
     - readme.md                 design rationale + dimension 决策 + borrowing
   附加一份 prototypes/comparison-report.md：variant 横向对比，给评审人看
   红队（推荐 companion skill: taste-skill）
   用户验收 = review-ready
```

## 不做的事（保护边界）

1. **不写生产代码** — 输出物到 HTML 样本为止
2. **不做组件库 / element contract / token pipeline** — 那是另一个 skill 的事
3. **不替用户选** — 参考清单、direction 数量、product archetype 都由用户拍板
4. **不偷偷 clone reference** — 每个 git clone 都必须在 Stage 1 跟用户确认过
5. **不写到主产品代码库** — 所有产物只落在本 skill 输出目录或用户指定路径

## Product Archetype 库（可选加载）

`templates/product-archetypes/` 下是**可扩展知识库**。Stage 0 决定要不要加载。

**七型全部建成（v1.0 升产，2026-06-10）** —— 每型含 `README` + `patterns-index` + `<type>-rules`（gate 形式）+ `layout-engines` + `motion-tokens` + `interaction` + **`reference-anchors.md`（真实标杆站点，供 P0 GROUND 接地消费）**:

| Archetype | 适用 | 锚定标杆(reference-anchors) |
|---|---|---|
| `canvas/` | 节点 / 白板 / 流程编辑器 | tldraw / Excalidraw / n8n / Dify / Flowise |
| `landing-marketing/` | 营销 / 转化着陆页 | Linear / Stripe / Vercel / Raycast / Framer / Clerk / Resend |
| `data-dashboard/` | 数据密集 dashboard / B2B 后台 | Vercel / Linear / Stripe / PostHog / Grafana / Datadog |
| `game-style/` | 游戏化 / 趣味交互 | Duolingo / Apple Fitness / Headspace / Robinhood / Finch |
| `bubble-physics/` | 物理 / 弹性 / 碰撞 | iMessage / Dynamic Island / Framer Motion / react-spring / Matter.js |
| `creative-eye/` | 跟随 / 注视 / 拟人创意 | Active Theory / Locomotive / lenis / Cuberto / Codrops |
| `narrative-scrolly/` | 长篇滚动叙事 / 编辑 | NYT Snow Fall / Pudding / Bloomberg / Apple AirPods / Stripe Press |

**每个 archetype 提供 STRUCTURE,不提供 L3 视觉皮肤**(详各 README 的「与 L3 的组合关系」段:NEVER 进 `l3_style` enum)。Stage 0 按产品类型加载对应 archetype;"都不像"→ 跳过 archetype,纯用通用 dimension 框架。

**扩展规则**：碰到七型不覆盖的新产品类型，照 `canvas/` 的文件结构(patterns / rules / layout-engines / motion-tokens / interaction / reference-anchors)新建一个即可。

## 通用 Dimension 框架

不论加不加载 archetype，所有产品都按以下 dimension 分析（Stage 0 让用户选权重）：

- **Visual** — palette / typography / hierarchy / texture
- **Interaction** — 核心动作语义、状态切换、键盘可达性
- **Motion** — duration / easing / 优先动效场景
- **Perspective** — 信息架构 / 用户视角 / 主路径
- **Accessibility** — WCAG AA / 减动效 / 键盘 / 屏读
- **Responsive** — breakpoints / 触屏 / 密度切换

详见 `references/analysis-dimensions.md`。

## Companion Skills（接地强制，其余可选增强）

> **v1.0 变更**:参考接地不再是"可选 companion",是 **Stage 1 硬前置**。本地 58 品牌 DESIGN.md 语料 + archetype `reference-anchors.md` 是**必须消费**的接地源(无接地不出 variant);其余仍为可选增强。

| Companion | 角色 | 强制? | 没匹配时的降级 |
|-----------|------|------|--------------|
| 本地 58 品牌 DESIGN.md 语料（**直接读** `…/awesome-design-md/design-md/<slug>/DESIGN.md`） | **Stage 1 主接地源** + Stage 2 token 候选输入 | **强制(本地优先)** | 退 archetype `reference-anchors.md` + web 源 |
| archetype `reference-anchors.md` | **Stage 1 标杆站点接地**(按产品类型) | **强制** | 主线程按品类常识列标杆(弱) |
| `competitive-teardown`(视觉模式) | Stage 1 web 候选发现 + 视觉模式抽取 | 本地无匹配时强制 | design-inspiration MCP / 主线程手写 |
| `grill-with-docs` | Stage 0 压实模糊点 | 可选 | 主线程问答兜底 |
| `taste-skill` | Stage 3 红队 / anti-slop 守门 | 单 agent 模式**显式路由它** | 主线程自审（弱） |
| `frontend-design` | Stage 3 HTML / React mock 写得更有质感 | 可选 | 主线程写基础 HTML/JSX |
| `imagegen-frontend-web` | Stage 1/2 moodboard(grounded in 上面的参考) | 可选(max 档推荐) | 跳过视觉 moodboard |
| Codex 官方 plugin (`/codex:rescue`) | Stage 3 多 variant 并行加速 | 可选 | 顺序生成 / Claude subagent |

> 接地查找表(58 品牌索引 + 历史 token + 字体/主题)详见 [`local-template-index.md`](../uiux-product-orchestrator/references/local-template-index.md)。完整安装指引：见根目录 `README.md` §Companion Skills。

## 触发本 skill 的典型说法

- "帮我做几版前端 prototype / UI direction"
- "出 5 版 dashboard 方向给我评审"
- "我想做个 [节点编辑器 / landing / 游戏化 ...]，参考 [产品 A / B]，先做 mock"
- "从 idea 到 prototype package 走一遍"
- "做几个 variant 让我挑方向"
- "出一份 prototype + token candidates 用来 review"

**不**触发的说法：

- "帮我把这个组件合并到生产" → 那是组件库 / merge 流程的事
- "写测试 / 做 a11y 审查" → 那是 QA skill 的事
- "建 design token pipeline" → 那是 design-system pipeline 的事

## 下游 Handoff

Stage 3 出 review-ready 包后**就停**。用户选定 variant 要走生产，按 `references/skill-routing-matrix.md` §"下游 Handoff" 提示对应下游 skill。当前已挂：

| variant 类型 | 下游 skill |
|--------------|------------|
| editorial-luxury / 高端品牌单页 / 100dvh hero video | `luxury-editorial-site-builder`（跳过其 Phase 0/1，从 Phase 2 真实内容开始） |

本 skill **不自动调用**下游——只在 `comparison-report.md` 末尾给提示。

## 版本

- `1.0.0` (2026-06-10) — 升产：UIUX 调度引擎 P1 EXPLORE 承重 owner；参考接地（本地 58 DESIGN.md 优先 + web）从可选升 Stage 1 硬前置；7 个 product archetype 全建成（canvas / landing-marketing / data-dashboard / game-style / bubble-physics / creative-eye / narrative-scrolly，各带 `reference-anchors.md`）；红队 gate 单 agent 模式显式路由 `taste-skill`。
- `0.2.0-skeleton`（历史，已被 1.0.0 取代）— 主入口 + program-director 完整；4 stage workflow 各一份；当时仅 canvas archetype 完整、其余 archetype 为 stub。**此 stub 状态已在 1.0.0 解决**（七型全建成，各带 `reference-anchors.md`），本行仅留作版本沿革记录。
