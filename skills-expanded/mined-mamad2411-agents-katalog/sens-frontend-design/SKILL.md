---
name: sens-frontend-design
version: 1.0.0
status: stable
created_date: 2026-05-23
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
description: >-
  End-to-end frontend design-to-code workflow for proposal-style projects — show a client a high-fidelity clickable prototype before building production. Three stages (Reference, Anchors, Prototype) across a Target x Direction x Stage matrix, each with explicit inputs, outputs, acceptance and structured hand-off docs instead of black-box AI image generation. For pitching N parallel visual directions, funnelling to one or two picks, then turning mockups into static HTML/CSS for Vercel or a proposal PDF. Triggers: "走 sens 流程 / 3-stage 设计流程 / 给客户出提案原型 / N 方向并行视觉探索 / Reference → Anchors → Prototype / 客户提案 demo 不上线".
---

# sens-frontend-design — 3-Stage 提案型前端工作流

> 设计的不是"一个网站",是"一份让客户能直观看见、横向对比、最终拍板的可交付物"。
> 工作流核心:把模糊的"设计 + 出图 + 落码"拆成 3 个 stage,每个 stage 有结构化文档承接,中间不靠口头交接、不靠 AI 黑盒一把梭。

---

## 1. 何时用这个 skill

✅ **用它**:
- 项目要给客户/老板看高保真原型,但**不上真实后端**
- 需要并行探索 **2-4 个视觉方向**,让客户横向对比后选 1-2 个落地
- 同一项目要同时设计 **2 个独立 target**(例:对外官网 + 对内系统)
- 想用 AI 出图,但担心组件漂移 / 风格不一致 / 数据占位混乱
- 最终交付物形态是 **静态 HTML/CSS 原型**(能部署 Vercel、能截图进 PDF)

❌ **不用它**:
- 单方向、单 target、不需要客户拍板的内部工具(直接用 `anchor-prototype-wave` 或 `frontend-design`)
- 已有 Figma / DESIGN.md 截图(直接用 `image-to-code-skill`)
- 探索期还没定方向(先用 `prototyping-ui-directions`)
- 真实生产 Next.js / React 项目(用 `frontend-design@claude-plugins-official`)

### 触发场景速查

| 用户话语 | 此 skill 入口 |
|---|---|
| "给客户出一份提案原型" | Stage 0 装配 |
| "我要并行做 4 个方向给客户挑" | Stage 1 多方向 |
| "客户官网 + 内部系统都要设计" | 两个 target |
| "AI 出图后怎么落码" | Stage 2 → Stage 3 |
| "设计文档怎么组织才不乱" | 直接套全套模板 |

---

## 2. 顶层框架:三维矩阵

```
                       Stage 1               Stage 2                Stage 3
                       Reference             Anchors                Prototype
                       (视觉规格)             (AI 生图)               (代码落地)
TARGET A
  Direction 1     ──>  DIRECTION.md     ──>  PROMPTS.md + PNG  ──>  HTML/CSS
  Direction 2     ──>  ...              ──>  ...               ──>  ...
  Direction N     ──>  ...              ──>  ...               ──>  ...
TARGET B
  Direction 1     ──>  ...              ──>  ...               ──>  ...
  ...
```

**三维**:Target(产品形态) × Direction(视觉方向) × Stage(产出阶段)

### 三条铁律

1. **同 target 内 N 方向共用同一份 `PAGE-WORKFLOW.md`** — 客户才能横向 1:1 对比
2. **不同 target 视觉完全独立** — 受众期待不同(老师用的后台 ≠ 家长看的官网)
3. **Stage 之间是漏斗** — N 方向并行 Stage 1+2 → 客户选 1-2 个 → Stage 3 只落选中的

---

## 3. 推荐目录结构

```
{project-root}/Design/
├── README.md                              ← 整体导览(总体思路 + 工作流 + 当前状态)
├── 1.Reference/                           ← Stage 1
│   ├── README.md
│   ├── {target-A}/
│   │   ├── README.md                      ← 4 方向对比 + 选型建议
│   │   ├── 1-{direction-name}/
│   │   │   ├── DIRECTION.md               ← 视觉规格
│   │   │   └── reference.png              ← 参考图
│   │   ├── 2-{direction-name}/
│   │   └── ...
│   └── {target-B}/
│       └── (同结构)
├── 2.Anchors/                             ← Stage 2
│   ├── README.md
│   ├── PROMPTS-SCHEMA.md                  ← (从 skill templates 复制)
│   ├── EXECUTION-WORKFLOW.md              ← (从 skill templates 复制)
│   ├── {target-A}/
│   │   ├── PAGE-WORKFLOW.md               ← 该 target 的共用页面骨架
│   │   ├── 1-{direction-name}/
│   │   │   ├── PROMPTS.md                 ← 按 SCHEMA 写
│   │   │   ├── core-01-xxx.png            ← Phase 1 整页 mockup
│   │   │   ├── core-02-xxx.png
│   │   │   └── ...
│   │   ├── 2-{direction-name}/
│   │   └── ...
│   └── {target-B}/
│       └── (同结构)
└── 3.Prototype/                           ← Stage 3
    ├── README.md
    ├── {target-A}/
    │   ├── BUILD-PROMPT.md                ← 通用规范(target 共享)
    │   ├── 1-{direction-name}/
    │   │   ├── BUILD-PROMPT.md            ← 方向特色补丁
    │   │   ├── index.html, ... .html
    │   │   ├── styles/
    │   │   │   ├── tokens.css
    │   │   │   └── components.css
    │   │   ├── scripts/main.js
    │   │   ├── assets/
    │   │   │   └── images/
    │   │   │       ├── {page-id}/         ← 该页独占素材
    │   │   │       └── shared/            ← 共用素材
    │   │   └── NOTES.md
    │   └── ...
    └── {target-B}/
        └── (同结构)
```

---

## 4. Stage 1 — Reference(视觉规格提炼)

**目的**:把参考图提炼成机器可读的视觉规格,让 Stage 2 + 3 都有 source of truth。

**输入**:
- 用户/设计师选定的参考图(每方向 1 张代表图就够了)
- Target 定位(例:System / Landing / Dashboard)

**产出**:`DIRECTION.md`(每方向一份,字段顺序严格固定)
- 模板见 [`templates/01-DIRECTION-TEMPLATE.md`](templates/01-DIRECTION-TEMPLATE.md)

**关键决策**:
- 每个 target 配几个方向?**建议 3-4 个**(够展示选择空间,又不至于客户选择困难)
- 方向命名:`{编号}-{颜色/词}-{气质}` 例 `2-Blue-School`

**验收**:
- [ ] 同 target 的 N 方向 DIRECTION.md 字段顺序完全一致(便于横向对比)
- [ ] hex 值是从参考图实际吸取/校准过,不凭感觉写
- [ ] 每方向都有"风险点 / 不适合做" — 否则后面会用错地方
- [ ] 不强制具体字体名 — 字体在 Stage 2/3 决定

---

## 5. Stage 2 — Anchors(AI 生图)

**目的**:把视觉规格 × 页面骨架 → AI 出整页 mockup,客户横向对比选方向。

**输入**:
- Stage 1 的 `DIRECTION.md`(每方向)
- `PAGE-WORKFLOW.md`(每 target 一份,定义共用页面骨架 + section + 占位数据)
  - 模板见 [`templates/02-PAGE-WORKFLOW-TEMPLATE.md`](templates/02-PAGE-WORKFLOW-TEMPLATE.md)

**产出**:`PROMPTS.md`(每方向一份,按 schema 强约束)
- Schema 见 [`templates/03-PROMPTS-SCHEMA.md`](templates/03-PROMPTS-SCHEMA.md)
- 包含 4 个固定 H1:Base Style / Phase 1 / Phase 2 / Phase 3

### 3-Phase 漏斗(本工作流核心创新)

```
Phase 1 — Core Pages(N 方向 × M 核心页整页 mockup)
  ↓ 客户横向看,选 1 个方向
Phase 2 — Remaining Pages(只跑选中方向的剩余整页)
  ↓ 客户二轮确认全套
Phase 3 — Per-Page Assets(单组件素材,逐页推进)
  ↓ 前端拿整页 mockup + 该页素材 → 写 HTML
```

**为什么这样分**:
- Phase 1 不全做完所有页面 — 给客户看核心页就够选方向,**省 70% 生图额度**
- Phase 3 **逐页推进、绝不跨页并行** — 同一组件(sidebar/portrait/card)并行跑会出 N 个不同版本,组件漂移就废了

### Asset 9 类 checklist(每页都过一遍,需要写、不需要写 N/A)

1. 真实人物照(透明 PNG)
2. 场景实拍
3. 装饰元素 SVG/PNG
4. Logo / 品牌标识
5. Icons 套件
6. UI mockup PNG
7. Badges / stickers
8. 背景 / 装饰底纹
9. Map / QR / 截图占位

### Asset ID 命名约定

`{方向缩写}-{页面缩写}-{素材语义名}` 例 `bs-home-blue-blob`

### 工具选择速查

| 素材类型 | 推荐工具 |
|---|---|
| 整页 mockup | Midjourney v6.1 / GPT-image-1 |
| 真实人物透明 PNG | MJ + remove.bg |
| 装饰 SVG / icons | 手写 SVG / Iconify |
| UI mockup(浏览器框 / 卡片) | Figma 手作 + 导出 |
| 占位 Logo / wordmark | 手写 SVG |

---

## 6. Stage 3 — Prototype(HTML 代码落地)

**目的**:把 Stage 2 选中方向的 PNG → 可点击静态 HTML 原型。

**输入**:
- Stage 2 选中方向的 Phase 1 + 2 整页 PNG
- Stage 2 该方向的 Phase 3 素材
- Stage 1 的 `DIRECTION.md`(最终色板/字体来源)

**产出**:两份 BUILD-PROMPT 拆分
- **`{target}/BUILD-PROMPT.md`(通用,target 共享)** — 见 [`templates/04-BUILD-PROMPT-TEMPLATE.md`](templates/04-BUILD-PROMPT-TEMPLATE.md)
- **`{target}/{direction}/BUILD-PROMPT.md`(方向特色补丁)** — 见 [`templates/05-DIRECTION-PATCH-TEMPLATE.md`](templates/05-DIRECTION-PATCH-TEMPLATE.md)

### 技术栈硬规则(适合"提案 demo"场景)

```
✅ 纯 HTML5 + Tailwind CDN + Google Fonts link + vanilla JS
❌ React / Vue / Next / 任何构建工具 / TS / SCSS / UI 库
```

**理由**:静态 HTML 任何人能开 / 能拖到 Vercel / 3 年后还能跑。

### Design tokens 强约束

- 所有 hex / spacing / font-size **必须**用 `--token` 引用
- 禁止 HTML 内联硬编码
- 间距强制走 8 倍数(`--space-1` 到 `--space-32`)
- Section padding / container / 卡片 padding / 文字纵向间距 / 按钮规格 / 表单字段 — 都给硬规格表,不允许"看起来差不多"

### 数据三等级(解决"哪些占位、哪些真实"的核心问题)

| 等级 | 标注 | 含义 |
|---|---|---|
| 🟢 REAL | 默认不标 | 业务真实数据,**不准改** |
| 🟡 PLACEHOLDER | `<!-- PLACEHOLDER: ... -->` | 等客户提供,占位文本明显 |
| 🔴 LOREM | `<!-- LOREM: ... -->` | 纯撑布局,客户应明白是假 |

### 嵌图两阶段

- **第一版**:Phase 1 整页 PNG 直接 `<img>` 嵌入对应 section → 客户看到完整页面
- **第二版**(客户确认方向后):重写为纯 HTML/CSS 复刻,装饰/人物换成 Phase 3 跑出来的单组件 PNG

---

## 7. 跨 Stage 编排原则(本 skill 最有价值的部分)

1. **"PAGE-WORKFLOW 共用 + DIRECTION 独立"的解耦**
   - PAGE-WORKFLOW.md 决定**结构骨架**(哪些页 / 每页哪些 section / section 占位数据)
   - DIRECTION.md 决定**视觉外套**(色 / 字 / 形 / 阴影)
   - PROMPTS.md = PAGE-WORKFLOW × DIRECTION 的笛卡尔积
   - N 方向并行时:同 page 在 N 方向间结构 1:1 对得上,只换"外套"

2. **三 Phase 漏斗,不一次烧光生图额度**

3. **Asset 一次生成 + 跨页复用**
   - `Used on Page(s)` 字段列全部使用方
   - 共用素材在第一次出现的 page 之下,落 `shared/`
   - 不准重复跑同一素材的多个版本

4. **"通用 BUILD-PROMPT + 方向特色补丁"二层结构**
   - 80% 共性放通用规范
   - 20% 方向独有放补丁
   - 每次开始一个方向的 prototype,把"通用 + 补丁 + 该方向 Phase 1 PNG"一起喂给 code AI

5. **数据三等级注释贯穿始终**

6. **同步产物落盘规范**
   ```
   Phase 1+2 整页 mockup → 2.Anchors/{target}/{direction}/{page-id}.png
   Phase 3 单组件素材    → 3.Prototype/{target}/{direction}/assets/images/{page-id}/
   共用素材              → 3.Prototype/{target}/{direction}/assets/images/shared/
   ```

---

## 8. 使用方法:在新项目里装这一套

### Step 1 — 装配目录

在项目根目录运行:
```bash
mkdir -p Design/{1.Reference,2.Anchors,3.Prototype}
```

按 §3 推荐结构建子目录。

### Step 2 — 复制模板

从 skill 的 `templates/` 把 4 份核心文件复制到项目:
```
templates/01-DIRECTION-TEMPLATE.md       → 复制 N 份到 1.Reference/{target}/{direction}/DIRECTION.md
templates/02-PAGE-WORKFLOW-TEMPLATE.md   → 复制 1 份到 2.Anchors/{target}/PAGE-WORKFLOW.md
templates/03-PROMPTS-SCHEMA.md           → 复制到 2.Anchors/PROMPTS-SCHEMA.md(整 target 共享)
templates/04-BUILD-PROMPT-TEMPLATE.md    → 复制 1 份到 3.Prototype/{target}/BUILD-PROMPT.md
templates/05-DIRECTION-PATCH-TEMPLATE.md → 复制 N 份到 3.Prototype/{target}/{direction}/BUILD-PROMPT.md
templates/06-EXECUTION-WORKFLOW.md       → 复制到 2.Anchors/EXECUTION-WORKFLOW.md(运行手册)
```

### Step 3 — 填充内容

按 stage 顺序填:
1. Stage 1 — 给每方向找参考图、填 DIRECTION.md
2. Stage 2 — 填 PAGE-WORKFLOW(target 共用)、填每方向 PROMPTS.md、跑 Phase 1 生图
3. 客户看 Phase 1 grid → 选方向
4. Stage 2 续 — 跑选中方向 Phase 2
5. Stage 3 — 跑 Phase 3 素材(逐页)+ 写 HTML(逐页)

### Step 4 — 跑 EXECUTION-WORKFLOW 的 step-by-step

详见 [`templates/06-EXECUTION-WORKFLOW.md`](templates/06-EXECUTION-WORKFLOW.md)。

---

## 9. 时间预估模板

| 阶段 | 工作量 | 周期 |
|---|---|---|
| Stage 1 写 DIRECTION.md(N 方向 × 2 target) | 8-12 份文档 | 2-3 天 |
| Stage 2 Phase 1 跑生图 + 拼 grid | ~48 张图 | 2-3 天 |
| 客户审 Phase 1 + 反馈 | — | 3-5 天 |
| Stage 2 Phase 2 跑选中方向 | ~12 张 | 1-2 天 |
| 客户二轮审 + 反馈 | — | 2-3 天 |
| Stage 3 Phase 3 + 落 HTML(逐页) | 每页 4-8h | 2-4 周 |
| 最终 prototype 整合 + QA | — | 3-5 天 |
| **总计** | | **4-6 周** |

---

## 10. 与其他 skills 的关系

| Skill | 关系 |
|---|---|
| `prototyping-ui-directions` | 上游 — 方向都没定时先用这个出 variant 探索 |
| `image-to-code-skill` | 替代品 — 已有 Figma/截图时用它 |
| `anchor-prototype-wave` | 下游 — 客户拍板后,大规模产 prototype 时用它 |
| `frontend-design@claude-plugins-official` | 替代品 — 真实生产项目用它,本 skill 是提案场景 |
| `gsd-ui-phase` | 协同 — GSD 流程里到 UI phase 时,本 skill 可作为产出 |
| `luxury-editorial-site-builder` | 替代品 — 单 brand landing page 用它,本 skill 是多方向多页 |

---

## 11. 反模式(常见翻车,不要这么做)

- ❌ 不同 target 用同一份 PAGE-WORKFLOW(老师后台 ≠ 家长官网,期待差太远)
- ❌ N 方向 DIRECTION.md 字段顺序不一致(横向无法对比)
- ❌ Phase 1 把所有页都跑出来(烧额度,客户根本看不完)
- ❌ Phase 3 跨页并行跑(组件漂移)
- ❌ tokens.css 之外还有硬编码 hex(后期 rename 噩梦)
- ❌ Header / Footer 在每个 page 里改一遍(应该完全复制粘贴)
- ❌ 把 PROMPTS.md 的示例数据当 LOREM 改掉(那是 REAL)
- ❌ Stage 3 用 React / Next / 构建工具(本工作流要求纯静态)
- ❌ AI 出图后直接交客户(应该先内部审 + 拼 grid)

---

## 12. 一句话总结

> 这不是"做一个网站",是**"做一份让客户能看懂、能对比、能拍板的可交付物"**。
> 三个 Stage、两层文档、三种数据等级、四方向并行、三 Phase 漏斗 — 都是为这个目标服务的。
