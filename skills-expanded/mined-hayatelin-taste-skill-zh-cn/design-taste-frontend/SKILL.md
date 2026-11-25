---
name: design-taste-frontend
description: 防止 AI 味（anti-slop）的前端设计 skill，适用于 landing page、作品集与改版案。Agent 会先读懂需求、推断正确的设计方向，并产出不像套模板的接口。适用时采用真实的设计系统、改版案先做盘点审计、发布前运行严格的 pre-flight 检查。Anti-slop frontend skill for landing pages, portfolios, and redesigns.
---

# tasteskill：Anti-Slop 前端设计 Skill

> 适用范围：landing page、作品集（portfolio）、改版（redesign）。不适用于 dashboard、数据表格、多步骤产品 UI。
> 以下每条规则都是**情境式的**，没有任何一条会自动触发。先读懂需求，再挑出真正适用的部分。

---

## 0. 需求推断（BRIEF INFERENCE：动手前先读懂现场）

在碰代码或调整任何参数之前，先**推断用户真正想要什么**。大多数 LLM 设计产出之所以糟糕，是因为模型直接跳到缺省美学，而不是先读懂现场。

### 0.A 先读这些信号
1. **页面类型**——landing page（SaaS / 消费性 / agency / 活动）、作品集（开发者 / 设计师 / 创意工作室）、改版（保留 vs 全面翻新）、editorial / 博客。
2. **用户用到的氛围词**——“minimalist”、“calm”、“Linear 风”、“Awwwards”、“brutalist”、“premium consumer”、“Apple 感”、“playful”、“serious B2B”、“editorial”、“agency 味”、“glassy”、“dark tech”。
3. **参考信号**——用户附的 URL、贴的截屏、点名的产品、正在竞争的品牌。
4. **受众**——B2B 采购委员会 vs. 有设计品味的消费者 vs. 快速扫过作品集的招募主管。美学由受众决定，不是由你的品味决定。
5. **既有的品牌资产**——logo、色彩、字体、摄影。对改版案来说，这些是起始素材，不是可有可无的输入（见第 11 节）。
6. **隐性限制**——无障碍优先的受众、公部门、受监管产业、以信任为先的电商、儿童产品。这些限制**凌驾于**美学偏好之上。

### 0.B 产出前先给一行“设计判读”（Design Read）
在写任何代码之前，先用一行话陈述：**“我把这个案子读作：给〈受众〉的〈页面类型〉，采用〈氛围〉语汇，倾向〈设计系统或美学家族〉。”**

判读范例：
- *“我把这个案子读作：给技术买家的 B2B SaaS landing page，采用 Linear 风的 minimalist 语汇，倾向 Tailwind utilities + Geist + 克制的动态。”*
- *“我把这个案子读作：给招募主管看的个人设计师作品集，采用 editorial / kinetic-type 语汇，倾向原生 CSS + scroll-driven animation + 客制字体排版。”*
- *“我把这个案子读作：公部门服务网站改版，采用以信任为先的语汇，倾向 GOV.UK Frontend 或 USWDS。”*

### 0.C 需求模糊时，问一个问题，不要用猜的
只问**一个**厘清问题——绝不一次丢一堆问题——而且只在设计判读真的出现分歧时才问。范例：*“这个应该偏 Linear 式的干净，还是 Awwwards 式的实验性？”*

如果能从上下文有把握地推断出来，就**不要问**。直接声明设计判读然后继续。

### 0.D 反缺省纪律（Anti-Default Discipline）
不要缺省使用：AI 紫渐层、深色 mesh 上置中的 hero、三张等宽 feature card、到处套 generic glassmorphism、满页无限循环微动画、Inter + slate-900。这些是 LLM 的默认值。要根据设计判读，刻意伸手越过它们。

---

## 1. 三个转盘（THE THREE DIALS：核心设置）

完成设计判读后，设置三个转盘（dial）。下面所有布局（layout）、动态、密度的决策都由这三个值把关。

* **`DESIGN_VARIANCE: 8`**——1 = 完美对称，10 = 艺术式混乱
* **`MOTION_INTENSITY: 6`**——1 = 静态，10 = 电影感 / 物理仿真
* **`VISUAL_DENSITY: 4`**——1 = 美术馆 / 留白通透，10 = 驾驶舱 / 数据密集

**基准值：**`8 / 6 / 4`。除非设计判读另有指示，否则使用这组。不要调用户来改这个文件——调整值的覆写在对话中进行。

### 1.A 转盘推断（设计判读 → 转盘值）
| 信号 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| “minimalist / clean / calm / editorial / Linear 风” | 5-6 | 3-4 | 2-3 |
| “premium consumer / Apple 感 / 奢华 / 品牌向” | 7-8 | 5-7 | 3-4 |
| “playful / wild / Dribbble / Awwwards / 实验性 / agency” | 9-10 | 8-10 | 3-4 |
| “landing page / 作品集 / 行销网站（缺省）” | 7-9 | 6-8 | 3-5 |
| “信任为先 / 公部门 / 受监管 / 无障碍关键” | 3-4 | 2-3 | 4-5 |
| “改版——保留” | 比照现况 | +1 | 比照现况 |
| “改版——翻新” | +2 | +2 | 比照现况 |

### 1.B 使用情境缺省组
| 使用情境 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing（SaaS，主流） | 7 | 6 | 4 |
| Landing（Agency / 创意） | 9 | 8 | 3 |
| Landing（Premium consumer） | 7 | 6 | 3 |
| 作品集（设计师 / 工作室） | 8 | 7 | 3 |
| 作品集（开发者） | 6 | 5 | 4 |
| Editorial / 博客 | 6 | 4 | 3 |
| 公部门服务 | 3 | 2 | 5 |
| 改版——保留 | 比照 | 比照+1 | 比照 |
| 改版——翻新 | +2 | +2 | 比照 |

### 1.C 转盘如何驱动输出
把这些值（或用户覆写后的值）当作全域变量。本文档各处的交叉引用都指向这些确切的变量名称——绝不要自创别名，例如 `LAYOUT_VARIANCE` 或 `ANIM_LEVEL`。

---

## 2. 需求 → 设计系统对照表

有了设计判读（第 0 节）和转盘值（第 1 节）后，挑选正确的基础。已有官方包的东西不要自己发明 CSS；也不要把美学潮流假装成官方系统。

### 2.A 何时该用真正的设计系统（使用官方包）
| 需求读起来像…… | 使用 | 原因 |
|---|---|---|
| Microsoft / 企业 SaaS / dashboard | `@fluentui/react-components` 或 `@fluentui/web-components` | 官方 Fluent UI、Microsoft tokens、无障碍已做好 |
| Google 风 UI、Material 味的产品 | `@material/web` + Material 3 tokens | 官方包，可通过 Material Theming 客制主题 |
| IBM 风 B2B / 企业分析 | `@carbon/react` + `@carbon/styles` | 官方 Carbon，成熟的数据密度模式 |
| Shopify 应用接口 | `polaris.js` web components / Polaris React | Shopify admin UI 的必要选择 |
| Atlassian / Jira 风产品 | `@atlaskit/*` + `@atlaskit/tokens` | 官方 Atlassian DS |
| GitHub 风开发工具 / 社群页 | `@primer/css` 或 `@primer/react-brand` | 官方 Primer；行销页用 Brand 变体 |
| 英国公部门服务 | `govuk-frontend` | 法规 / 监理上的预期 |
| 美国公部门 / 信任为先 | `uswds` | 同上 |
| 快速的在地商家 / agency MVP | Bootstrap 5.3 | 无聊、快速、能用 |
| 现代化无障碍 React 基础 | `@radix-ui/themes` | Primitives + 打磨过的主题 |
| 组件要自己掌控的现代 SaaS | shadcn/ui（`npx shadcn@latest add ...`） | 代码归你所有、容易客制；绝不以缺省状态发布 |
| Tailwind 基底的现代 SaaS / AI 行销页 | Tailwind v4 utilities + `dark:` variant | 独立开发者与小团队的缺省选择 |

**诚实规则：**如果需求读起来就是上面某个系统，就安装并使用**官方**包。不要手刻重现它的 CSS。也不要导入某系统的 tokens 却覆写掉九成。

**一个项目一个系统。**不要在同一棵组件树里混用 Fluent React 和 Carbon。不要把 shadcn/ui 组件汇进 Material 3 应用。

### 2.B 当需求是一种美学、而不是一个系统时
以下这些方向**没有单一官方包**。用原生 CSS + Tailwind + 有维护的组件库来实现。在代码注释里诚实标明哪些是借用的灵感、哪些是官方素材。

| 美学 | 诚实的实现方式 |
|---|---|
| Glassmorphism /“毛玻璃” | `backdrop-filter`、多层边框、highlight 叠层。为 `prefers-reduced-transparency` 提供实色 fallback。 |
| Bento（Apple 风磁砖格） | CSS Grid 搭配混合尺寸的格子。没有哪个函数库独占这个模式。 |
| Brutalism | 原生 CSS、monospace、粗犷边框。没有函数库。 |
| Editorial / 杂志风 | 衬线字体、非对称 grid、大量留白（whitespace）。没有函数库。 |
| Dark tech / 黑客风 | Mono + 霓虹强调色、终端机母题。没有函数库。 |
| Aurora / mesh 渐层 | SVG 或多层 radial gradient。没有函数库。 |
| Kinetic typography | 原生 CSS 动画、scroll-driven animation、滚动劫持用 GSAP。没有函数库。 |
| **Apple Liquid Glass** | Apple 只为 Apple 平台撰写文档。**没有官方的 `liquid-glass.css`。**Web 实现是用 `backdrop-filter` + 多层边框 + highlight 做的近似。务必清楚标示为近似。 |

---

## 3. 缺省架构与惯例

除非设计判读选了真正的设计系统（第 2.A 节），否则以下是缺省：

### 3.A 技术堆栈
* **框架：**React 或 Next.js。缺省使用 Server Components（RSC）。
  * **RSC 安全守则：**全域状态只能在 Client Components 里运作。在 Next.js 中，把 provider 包进一个 `"use client"` 组件。
  * **交互隔离：**任何用到 Motion、scroll listener 或指针物理效果的组件，都必须是顶端标了 `'use client'` 的独立叶节点组件。Server Components 只负责渲染静态布局。
* **样式：** **Tailwind v4**（缺省）。只有当既有项目要求时才用 Tailwind v3。
  * v4 注意：`postcss.config.js` 里不要用 `tailwindcss` plugin，改用 `@tailwindcss/postcss` 或 Vite plugin。
* **动画：** **Motion**（就是以前的 Framer Motion）。从 `motion/react` 导入（`import { motion } from "motion/react"`）。`framer-motion` 包仍可当作旧别名使用——新代码优先用 `motion/react`。
* **字体：**一律用 `next/font`（Next.js）或自架搭配 `@font-face` + `font-display: swap`。正式环境绝不用 `<link>` 连 Google Fonts。

### 3.B 状态管理
* 孤立的 UI 用本地 `useState` / `useReducer`。
* 全域状态只用来避免深层 prop-drilling——Zustand、Jotai 或 React context。
* **绝不**用 `useState` 追踪由用户输入驱动的连续值（鼠标位置、滚动进度、指针物理、磁性 hover）。改用 Motion 的 `useMotionValue` / `useTransform` / `useScroll`。`useState` 每次变动都会重新渲染整棵 React 树，在移动设备上直接垮掉。

### 3.C 图标
* **允许的函数库（优先级）：**`@phosphor-icons/react`、`hugeicons-react`、`@radix-ui/react-icons`、`@tabler/icons-react`。
* **不建议：**`lucide-react`。只有在用户明确要求、或项目已依赖它时才可接受。
* **绝不手刻 SVG 图标。**缺某个字符（glyph）时，就再装一套函数库或用基本形状组合——不要从零画 icon path。
* **一个项目一个图标家族。**不要在同一棵组件树里混用 Phosphor 和 Lucide。
* **全域统一 `strokeWidth`**（例如 `1.5` 或 `2.0`）。

### 3.D Emoji 政策
在代码、标记与可见文本中缺省不建议使用。以图标库的字符取代符号。**覆写条件：**只有当用户明确要求 playful / 聊天感 / 社群原生的氛围时才允许 emoji——即使如此也要有意图地节制使用。

### 3.E 响应式与布局机制
* 统一断点（`sm 640`、`md 768`、`lg 1024`、`xl 1280`、`2xl 1536`）。
* 用 `max-w-[1400px] mx-auto` 或 `max-w-7xl` 收拢页面布局。
* **窗口稳定性：**全高 Hero 区块**绝不**用 `h-screen`，**一律**用 `min-h-[100dvh]`，避免移动设备上布局跳动（iOS Safari 网址列）。
* **Grid 优先于 Flex 数学：**绝不用复杂的 flexbox 百分比计算（`w-[calc(33%-1rem)]`），一律用 CSS Grid（`grid grid-cols-1 md:grid-cols-3 gap-6`）。

### 3.F 依赖包验证（强制）
导入任何第三方函数库之前，先检查 `package.json`。包不存在时，先输出安装指令。**绝不**假设函数库已存在。

---

## 4. 设计工程指令（偏误矫正）

LLM 缺省会产出陈腔滥调。要主动覆写这些缺省。每条规则都有情境感知的覆写路径。

### 4.1 字体排版（Typography）
* **Display / 标题：**缺省 `text-4xl md:text-6xl tracking-tighter leading-none`。
* **内文 / 段落：**缺省 `text-base text-gray-600 leading-relaxed max-w-[65ch]`。
* **无衬线字体选择：**
  * **不建议当缺省：**`Inter`。优先选 `Geist`、`Outfit`、`Cabinet Grotesk`、`Satoshi`，或符合品牌的衬线字体。
  * **覆写条件：**当用户明确要求中性 / 标准 / Linear 风的感觉，或需求是公部门 / 无障碍优先的网站时，Inter 可以接受。
* **值得记住的搭配：**`Geist` + `Geist Mono`、`Satoshi` + `JetBrains Mono`、`Cabinet Grotesk` + `Inter Tight`、`GT America` + `IBM Plex Mono`。

* **衬线字体纪律（强烈不建议当缺省）：**
  * 衬线字体**强烈不建议作为任何项目的缺省字体。**“感觉有创意 / 高级 / editorial”不是伸手拿衬线字体的理由。Agent 心中“创意需求 = 衬线”的缺省模型，是实测回合中被验出最多次的 AI 特征（AI tell）。
  * **只有以下其中一项明确成立时，衬线字体才可接受：**
    - 品牌需求白纸黑字点名了某个衬线字体，或
    - 美学家族确实是 editorial / 奢华 / 出版 / 手稿 / 传承 / 复古，而且你能说清楚为什么“这个”衬线字体适合“这个”品牌
  * 其他所有情况（创意 agency、设计工作室、现代品牌、premium consumer、作品集、生活风格）**缺省用无衬线 display 字体**（Geist Display、ABC Diatype、Söhne Breit、Cabinet Grotesk Display、Migra Sans、GT Walsheim、Inter Display、PP Neue Montreal）。无衬线 display 字体不“无聊”——它们是缺省，就像黑色是时尚界的缺省一样。
  * **强调规则（相关）：**想强调标题里的某个词（例如 kinetic 式的“and `spatial` design”手法）时，用**同一字体的 italic 或 bold**。不要为了视觉趣味把一个突兀的衬线词塞进无衬线标题（反之亦然）。跨字族强调是外行做法；同字族的 italic / bold 强调才是正解。
  * **明确禁止当缺省：**`Fraunces` 和 `Instrument_Serif`（LLM 最爱的两款 display 衬线字体）。
  * **若衬线确有正当理由**（如上所述，很罕见），从这个池子轮替，不要连续项目重用同一款：PP Editorial New、GT Sectra Display、Cardinal Grotesque、Reckless Neue、Tiempos Headline、Recoleta、Cormorant Garamond、Playfair Display、EB Garamond、IvyPresto、Migra、Editorial Old、Saol Display、Söhne Breit Kursiv、Domaine Display、Canela、Schnyder、Tobias、NB Architekt、ITC Galliard。

* **Italic 下伸部净空（强制）：**Display 字级使用 italic 且单字含下伸部字母（`y g j p q`）时，`leading-[1]` 或 `leading-none` 会裁到下伸部。至少用 `leading-[1.1]`，并在外层元素加 `pb-1` 或 `mb-1` 预留空间。发布前逐一检查 display 标题里的每个 italic 单字。

### 4.2 色彩校准
* 最多 1 个强调色。饱和度缺省 < 80%。
* **紫色守则（THE LILA RULE）：**“AI 紫 / 蓝色光晕”美学不建议当缺省。不要自动加紫色按钮光晕，不要随机的霓虹渐层。用中性基底（Zinc / Slate / Stone）搭配高对比的单一强调色（Emerald、Electric Blue、Deep Rose、Burnt Orange 等）。
* **覆写条件：**如果品牌或需求明确要求紫色 / 紫罗兰 / lila，就拥抱它。但要有意图地运行：一致的调色板、调和过的中性色、克制的渐层。不是 generic 的 AI 渐层垃圾。
* **一个项目一组调色板。**不要在同一个项目里在暖灰和冷灰之间摇摆。
* **色彩一致性锁（强制）：**一旦为页面选定强调色，就要用在**整页**。暖灰网站不会在第 7 个 section 突然冒出蓝色 CTA；玫瑰色系网站的 footer 不会出现蓝绿色状态徽章。选一个强调色，锁住它，发布前逐组件审计。

* **Premium-consumer 调色板禁令（强制，第二常见的 AI 特征）：**
  * 面对 premium-consumer 需求（锅具、wellness、职人、奢华、传承工艺、DTC 居家用品等），LLM 的缺省是**暖米白/奶油 + 黄铜/陶土/牛血红/赭石 + 深咖啡/墨色深色文本**。以下 hex 家族明确禁止作为缺省背景与强调色：
    - 背景：`#f5f1ea`、`#f7f5f1`、`#fbf8f1`、`#efeae0`、`#ece6db`、`#faf7f1`、`#e8dfcb`（全是“暖纸 / 奶油 / 粉笔 / 骨白”）
    - 强调：`#b08947`、`#b6553a`、`#9a2436`、`#9c6e2a`、`#bc7c3a`、`#7d5621`（全是“黄铜 / 陶土 / 牛血红 / 赭石”）
    - 文本：`#1a1714`、`#1a1814`、`#1b1814`（全是“深咖啡 / 暖近黑”）
  * 这组调色板禁止作为 premium-consumer 需求的缺省选择。你发布过的每一个 premium-consumer 网站都用了这组一模一样的调色板，品牌因此变得隐形。
  * **缺省替代方案（轮替使用，不要重复）：**
    - **Cold Luxury：**银灰 + 铬 + 烟灰（想想 Tesla、去掉皮革的 Apple Watch Hermes）
    - **Forest：**深绿 + 骨白 + 琥珀强调（想想 Filson、Patagonia 高端线）
    - **Black and Tan：**真正的 off-black + 暖棕褐，锐利对比，没有米白
    - **Cobalt + Cream：**饱和蓝配单一中性色，没有黄铜
    - **Terracotta + Slate：**暖锈红配冷灰，没有黄铜
    - **Olive + Brick + Paper：**低调橄榄绿加砖红强调
    - **纯单色 + 单一饱和亮点：**off-white + off-black + 一个鲜明强调色（electric blue、emerald、hot pink 等）
  * **调色板轮替规则：**如果你上一个 premium-consumer 项目用了米白+黄铜家族，这一个就**必须**换家族。不要连续两次出同一组暖工艺调色板。
  * **覆写条件：**只有当品牌需求明确点名那些颜色，或品牌识别确实是复古 / 职人 / 暖工艺，而且你能说清楚为什么这组调色板适合这个品牌时，米白+黄铜+深咖啡才可接受。因为“这是锅具需求”就缺省伸手去拿，是被禁止的。

### 4.3 布局多样化
* **反置中偏误（ANTI-CENTER BIAS）：**当 `DESIGN_VARIANCE > 4` 时，避免置中的 Hero / H1 区块。强制改用“Split Screen（50/50）”、“内容靠左 / 资产靠右”、“非对称留白”或 scroll-pinned 结构。
* **覆写条件：**editorial / 宣言式 / 发表公告类需求，消息本身就是设计时，置中 hero 没问题。

### 4.4 材质、阴影、卡片
* 只有当高度（elevation）能传达真实层级时才用卡片。否则用 `border-t`、`divide-y` 或负空间来分组。
* 使用阴影时，把阴影染上背景色相。浅色背景上不要有纯黑 drop shadow。
* 当 `VISUAL_DENSITY > 7`：禁止 generic 卡片容器。数据指标要在素朴的布局里呼吸。
* **形状一致性锁（强制）：**为页面选定**一套**圆角尺度并贯彻到底。选项：全直角（radius 0）、全柔角（radius 12-16px）、全胶囊（交互组件用 full radius）。混合系统只有在有明文规则时才允许（例如“按钮全胶囊、卡片 16px、输入框 8px”），而且该规则要处处遵守。方正布局里冒出圆按钮、或胶囊按钮页面上出现方卡片，就是坏掉的设计。

### 4.5 交互 UI 状态
LLM 缺省只做“静态的成功状态”。一律实现完整循环：
* **Loading：**用符合最终布局形状的 skeleton loader。避免 generic 的圆形 spinner。
* **空状态：**精心构图；指出如何填入内容。
* **错误状态：**清楚、行内显示（表单），或情境式（toast 只用于暂时性消息）。
* **触觉回馈：**在 `:active` 时用 `-translate-y-[1px]` 或 `scale-[0.98]` 仿真实体按压。
* **按钮对比检查（强制，a11y）：**发布任何按钮前，确认按钮文本在按钮背景上可读。白按钮 + 白字、`bg-white` CTA 配 `text-white` 标签、无边框透明按钮直接压在页面背景上 → 全部禁止。审计每个 CTA：对比至少达 WCAG AA（内文 4.5:1，18px+ 大字 3:1）。压在摄影背景上的 ghost button 同样适用（加 backdrop、scrim 或描边）。
* **CTA 按钮换行禁令（强制）：**桌面版按钮文本**必须**单行放得下。像“VIEW SELECTED WORK”这种标签换成 2、3 行，按钮就是坏的。修法二选一：缩短标签（主要 CTA 最多 3 个词，最好 1-2 个），或加宽按钮（不要人为限制 CTA 的 `max-width`）。桌面版 CTA 换行是 Pre-Flight Fail。
* **禁止重复的 CTA 意图（强制）：**同一页有两个相同意图的 CTA 就是 Pre-Flight Fail。相同意图的例子：“Get in touch”+“Contact us”+“Let's talk”+“Start a project”+“Start something”+“Reach out”全是“联系”意图 → 选**一个**标签，整页（nav、hero、footer）都用它。“Try free”+“Get started”+“Sign up free”（全是“注册”意图）和“View work”+“See selected work”+“Browse projects”（全是“作品集”意图）同理。一个意图一个标签。
* **表单对比检查（强制，a11y）：**表单输入框、placeholder 文本、focus ring、辅助文本、错误文本，全部都要对 section 背景通过 WCAG AA 对比。近白表单上的浅色 placeholder、白页面 section 上的白表单、对比灰于 4.5:1 的表单标签 → 全部禁止。发布前审计每个表单。

### 4.6 数据与表单模式
* 标签在输入框**上方**。辅助文本可选但要存在于标记中。错误文本在输入框**下方**。输入区块标准用 `gap-2`。
* 不准用 placeholder 当标签。永远不准。

### 4.7 布局纪律（硬规则。违反任何一条就是发布坏掉的作品）

* **Hero 必须塞进初始窗口。**桌面版标题最多 2 行，副文案最多 **20 个词**且最多 3-4 行，CTA 不滚动就看得到。文案太长时：缩小字级或砍文案。如果 20 个词的副文案讲不清价值主张，那是价值主张不清楚，不是规则太紧。绝不让 hero 溢出、逼用户滚动才找得到 CTA。
* **Hero 字级纪律。**字级和图片尺寸要*一起*规划。hero 资产很大、标题又超过 6 个词时，不要从 `text-7xl/text-8xl` 起手。合理的缺省范围：多数 hero 用 `text-4xl md:text-5xl lg:text-6xl`；只有标题 3-5 个词时才用 `text-6xl md:text-7xl`。4 行的 hero 标题永远是字级错误，不是文案长度错误。
* **Hero 顶部 padding 上限（强制）：**桌面版 hero 顶部 padding 最多 `pt-24`（约 6rem）。再多，hero 内容就会飘到窗口一半的位置，读起来像布局 bug 而不是刻意留白。hero 需要更多呼吸空间时，加大字级或资产尺寸，而不是加顶部 padding。
* **Hero 堆栈纪律（最多 4 个文本元素）。**Hero 是单一时刻，不是功能清单。允许的文本元素，总共最多 4 个：
  1. Eyebrow（小型大写标签）或品牌列（brand strip）或都不要——选零或一个
  2. 标题（最多 2 行，见上）
  3. 副文案（最多 20 个词，最多 4 行）
  4. CTA（1 个主要 + 最多 1 个次要）
  - **Hero 内禁止：**CTA 下方的小 tagline（“Works with GitHub, GitLab, and self-hosted Git”）、信任微条（“Used by engineering teams at...”）、定价预告（“Free for solo, $10/user for teams”）、功能 bullet 清单、社会证明头像列。这些全部移到 hero 正下方的专属 section。
  - 同一个 hero 里如果既有 eyebrow 又有 CTA 下方的 tagline，砍掉 tagline。既有品牌列又有 tagline，砍掉 tagline。每个 hero 最多一个小型文本元素。
* **“Used by”/“Trusted by”logo 墙放在 hero 底下，绝不放进 hero 里。**Hero 属于价值主张和主要 CTA。logo 墙是紧接其下的独立 section。不要把信任 logo 塞进和 hero 文案同一个 flex row。
* **桌面版导览列必须渲染成单行。**在 `lg`（1024px）放不下时，就精简标签、砍次要项目、或改用汉堡菜单。桌面版两行的 nav 是坏掉的设计。
* **导览列高度上限：桌面版最高 80px，缺省 64-72px。**不要那种吃掉 15% 窗口的巨型“agency”nav bar。
* **Bento grid 必须有节奏，不能单边重复。**不要叠 6 个左图右文的 row。变化构图：交错全宽 feature row、非对称磁砖尺寸、垂直断点。
* **Bento 格数规则（强制）：**Bento grid 的格数**正好**等于你有的内容数。3 个项目 → 3 格（1+2、2+1、或非对称三格）。5 个项目 → 5 格（2+3、3+2、hero+4 等）。如果 grid 中间或结尾出现空格，是你规划错了。重塑 grid，不要贴一块空白磁砖。
* **Section 布局重复禁令。**某个布局家族（例如三栏图卡、全宽引言、图文分割）在页面上用过一次后，最多只能出现**一次**。“Selected commissions”不能长得像“What we do”。有 8 个 section 的 landing page 至少要用 4 种不同的布局家族。
* **Zigzag 交错上限（强制）。**“左图右文”接着“左文右图”的 zigzag 布局 = 平庸。同一种图文分割模式最多连续 2 个 section。第 3 个连续的图文分割是 Pre-Flight Fail。用全宽 section、垂直堆栈 section、bento grid、marquee 或不同的布局家族打破模式。
* **Eyebrow 节制（强制，实测中违反率第一名的规则）。**“Eyebrow”是 section 标题上方那行小型大写、宽字距的标签（例如 `FOUR COLORWAYS`、`SELECTED WORK`、`THE HARDWARE`、`Git-native task management`）。典型 CSS 特征：`text-[11px] uppercase tracking-[0.18em]`、`font-mono text-[10.5px] uppercase tracking-[0.22em]`。每个 AI 盖的网站都在**每个** section 标题上放 eyebrow，产生同一种模板化节奏。硬规则：
  - **每 3 个 section 最多 1 个 eyebrow。**Hero 算 1 个。所以 9 个 section 的页面全页最多 3 个 eyebrow。
  - 如果 section A 有 eyebrow，接下来 2 个 section 不能有。
  - **Pre-Flight 检查是机械式的：**统计所有 section 组件里 `uppercase tracking`（或类似的小型大写 mono 标签在标题上方）的出现次数。若次数 > ceil(sectionCount / 3)，输出不合格。
  - **不放 eyebrow 该怎么办：**整个拿掉。标题本身就够了。如果需要为 section 分类，它在页面上的位置已经分类了它；不需要标签。
* **分割式标头禁令（SPLIT-HEADER BAN，强制）。**“左边大标题 + 右边小段说明文”的 section 标头模式（左 col-span-7/8、右 col-span-4/5 飘着一小段内文）**禁止作为缺省**。Section 应该只有一个聚焦的消息。真的同时需要标题和说明段落时，垂直堆栈（标题在上、内文在下、max-width 65ch）。只有存在真正的构图理由时才伸手拿分割式标头（例如右栏承载视觉或交互元素，而不只是填充文本）。
* **Bento 背景多样性（强制）。**Bento 和 feature-grid section 不能是 6 张白底白卡、里面只有文本。任何多格 grid 至少要有 2-3 格具备真正的视觉变化：真实图片、符合品牌的渐层（不是 AI 紫）、图样、或带色背景。奶油底配奶油卡、里面只有字体排版的 bento，就算页面其他地方再好，读起来也是无聊的 AI 缺省。
* **每个 section 的移动设备收合必须明写。**每个多栏布局都要在同一个组件里声明 `< 768px` 的 fallback。不准有“应该没问题，Tailwind 会处理”的假设。

### 4.8 图片与视觉资产策略

Landing page 和作品集是**视觉产品**。只有文本加假截屏 div 的页面就是垃圾（slop）。

**视觉资产的优先级：**
1. **图片生成工具优先。**只要环境里有**任何**图片生成工具（`generate_image`、MCP 图片工具、IDE 内置生成、OpenAI 图片工具等），就**必须**用它产生各 section 专属的资产：hero 摄影、产品照、材质背景、氛围图。依 section 需求以正确长宽比生成。不要因为手刻 CSS 感觉比较快就跳过这步。
2. **真实网络图片其次。**没有生成工具时，用真实摄影来源。可接受的缺省：
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` 作为摄影 placeholder（seed 要描述该 section，例如 `marrow-cookware-kitchen`）
   * 需求提供时，用实际的 stock 或品牌 URL
   * 明确允许时用开放授权来源（Unsplash 直连 URL、Pexels）
3. **最后手段：告诉用户。**两者都不可行时，**不要**用手刻 SVG 插图或 div 拼的“假截屏”填满页面。改留清楚标示的 placeholder 插槽（`<!-- TODO: hero product photo, 1600x1200 -->`），并在回复最后说：*“这个页面在以下位置需要真实图片：〔位置清单〕。请生成或提供。”*

**就算是 minimalist 网站也需要真实图片。**纯文本页面不是 minimalism，是未完成的作品。就算是 editorial 的 Linear 风网站，也至少需要 2-3 张真实图片（hero、一张产品/生活照、一张辅助图）。需求走克制路线就生成黑白 minimalist 摄影；不要因为转盘值低就完全跳过图片。

**社会证明要用真实公司 logo。**需求要求“Trusted by / Used by / Customers”logo 墙时，**不要**缺省排一排纯文本字标（styled 过的 `<span>Acme Co</span>`）。用真实 SVG logo：
* **来源：Simple Icons**（任何颜色都可用 `https://cdn.simpleicons.org/{slug}/ffffff`，或 `simple-icons` npm 包）。涵盖多数知名品牌。
* **替代：devicon** 用于技术栈 logo（`@svgr/cli` 或 CDN）。
* **品牌名是虚构的？那就连 SVG 标志一起虚构。**生成一个简单的 monogram（圆圈里一个字母、双字母连字、抽象字符），以行内 `<svg>` 渲染并配合页面风格。虚构品牌名配纯文本字标看起来很 generic。
* **一律**确保 logo 在亮暗两种模式都能正常渲染（深底白、浅底黑、或单色主题变量）。
* **LOGO-ONLY 规则（强制）：**logo 墙 = 只有 logo，别无其他。**不要**在每个 logo 下方印产业 / 类别标签（不要 `Vercel` 下面写 `hosting`、`Stripe` 下面写 `payments`、`Cloudflare` 下面写 `infra`）。logo 本身就是可信度，标签加不了用户不知道的东西。可选：品牌名当 alt 文本给屏幕阅读器、可选连到品牌网站。仅此而已。

**手刻插图：**
* 来自函数库的 SVG 图标：可以（见第 3.C 节）。
* 手刻装饰性 SVG（客制插图、logo、标志）：**强烈不建议**，绝不当缺省。只有以下情况可接受：
  - 需求明确要求（“帮我画一个 SVG logo”）
  - 是单一、简单的几何标志（一个方形、一个圆形、display 字体的字标）
  - 你对输出质量有信心

**Div 拼的假截屏是禁止的。**用 `<div>` 矩形拼出来的“手工产品预览”——假任务清单、假 dashboard、假终端机窗口——就是 AI 特征。需要展示产品时：
* 有真实截屏 URL 就用
* 用图片工具生成一张
* 用真实组件预览（页面里放一个真的迷你版 UI）
* 或干脆跳过预览，改用 editorial 摄影

**Hero 需要真实视觉。**文本 + 渐层色块不是 hero——是 placeholder。

### 4.9 内容密度

Landing page 靠的是**第一印象**，不是全文精读。狠心地砍。

* **每个 section 的缺省内容形状：**短标题（≤ 8 个词）+ 短副段落（≤ 25 个词）+ 一个视觉资产**或**一个 CTA。再多的东西都必须以该 section 的任务来合理化。
* **不准有数据倾倒式 section。**行销页上 20 列的出版品表格、30 列的奖项清单、巨型定价矩阵 = 用错布局。改用：
  - 前 3-5 个亮点 +“View full list”链接
  - Marquee / carousel 呈现广度
  - 数据本身就是产品的话，另开一页
* **长清单需要的是不同的 UI 组件，不是更长的清单。**缺省的 `<ul>` bullet / `divide-y` row 是偷懒的选择。超过 5 个项目时，改用以下之一：
  - 两栏分割搭配分组项目
  - 每项配图 + 标签的卡片 grid
  - 项目可分类就用 tabs / accordion
  - 水平 scroll-snap 胶囊
  - 广度型清单（见证、logo、能力）用 carousel
  - “很多但不需要个别注意的东西”用 marquee
  10 列规格表、每列下面一条 hairline，是**最糟的**缺省。要嘛把列分成 2-3 块、用稀疏的分隔线，要嘛改成一卡一规格的布局。
* **规格表特别注意（Marrow 锅具模式）。**每列都加 `border-b` 的长产品规格表，是 AI 面对锅具 / 硬件 / 服饰 / 职人商品需求的缺省。禁止。具体替代方案：
  - **两栏卡片 grid：**每个规格一张卡，含规格名、数值（大型 display 数字）、一行“为什么重要”的内文。桌面两栏、移动一栏。
  - **Scroll-snap 水平胶囊：**每个规格一颗胶囊，用户可滑动浏览。
  - **分组成块：**把 10 个规格分成 3 个逻辑群（例如“Materials”、“Cooking”、“Warranty”），每群配**一条**柔和分隔线和群标题。
  - **主打 vs 其余：**3-4 个主打规格做成大型 display 磁砖，其余收在“View full specifications”的 disclosure 里。

* **文案自我审计（COPY SELF-AUDIT，发布前强制）：**声明任何任务完成之前，重读页面上每一条可见字符串（标题、副标、eyebrow、按钮标签、内文、图说、alt 文本、footer 文本、错误消息）。标记任何符合以下情况的字符串：
  - **文法坏掉**（“free on its past”、“two plans but one is honest”、脱离语境的“to put it on the table”）
  - **指涉不明**（没有前文的“we plan to stay that way”）
  - **听起来像 AI 幻觉**（可爱但错误的双关、不成立的强行比喻、“elegant nothing”式的空话）
  - **读起来像 LLM 在装深沉**（被动攻击式的谦逊、假工匠标签、故作诗意的 micro-meta）
  改写每条被标记的字符串。不确定某字符串是否说得通时，换成平实的功能性句子。AI 生成的卖萌文案比无聊文案更糟。
* **假精确数字要被标记。**像 `92%`、`4.1×`、`48k`、`5.8 mm`、`13.4 lb` 这类数字必须：
  - 来自真实数据（需求、品牌准则、公开指标）——可以
  - 明确标示为 mock（`<!-- mock -->`、“example”、“sample data”）——可以
  - AI 自己发明的规格美学——禁止。不要伪造品牌没有宣称的工程精确度。
* **一页一种文案语域（register）。**不要在同一个构图里混用技术 mono（“47 tasks · 0.6 ctx-switches/day”）、editorial 散文和行销重拳，除非品牌声音明确要求。

### 4.10 引言与见证（Testimonials）

* 引言本文**最多 3 行**。绝不 6 行。原始引言更长 → 剪短。landing page 的引言是片段，不是完整评论。
* 字级非常小时（例如 footer 式见证），行数上限可以稍微放宽。精神是：“一眼看完”。
* 引言文本里**不用 em-dash** 当设计花招（长停顿、kinetic em-dash、em-dash 当 bullet）。见第 9.G 节——em-dash 全面禁止。
* 署名：姓名 + 职称 +（可选）公司。绝不只有名字（“- Sarah”）。
* 引号：用真正的印刷引号（" "）或干脆不用。不用直立的 ASCII 引号（"）。

### 4.11 页面主题锁（亮 / 暗模式一致性）

一页只有**一个**主题。Section 不准反转。

* 页面是暗模式，**所有** section 都是暗模式。不准在暗色 section 之间夹一个亮色暖纸 section（反之亦然）。用户不该在滚动途中觉得走进了另一个网站。
* 例外：需求明确要求“Color Block Story”或“滚动切换主题”的手法，**且**那是刻意的构图（一次完整的主题切换配强力转场，不是随机交错）时，每页允许一次。
* 缺省行为：在页面层级选定亮、暗或自动（`prefers-color-scheme`）然后锁住。同一主题家族内的 section 层级背景色调制化没问题（`bg-zinc-950` 旁边放 `bg-zinc-900`）；在 `bg-zinc-950` 的页面中间翻成 `bg-amber-50` 就是坏掉。
* 使用内置主题机制的设计系统（Radix Themes、shadcn/ui 的 `<Theme>`）时，在 `layout.tsx` 或页面根节点设置主题**一次**。不准让个别 section 覆写。

---

## 5. 情境感知的主动性

这些是工具，不是缺省。设计判读需要时才用。**没有任何一项会自动触发。**

* **Liquid Glass / Glassmorphism：**适合 premium consumer、Apple 系、奢华品牌或媒体叠层氛围。不适合 dashboard、公部门或“无聊 B2B”。使用时要超越单纯的 `backdrop-blur`：加 1px 内边框（`border-white/10`）和细微内阴影（`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`）做出实体边缘折射感。在 `prefers-reduced-transparency` 下提供实色 fallback。
* **磁性微物理（Magnetic Micro-physics）：**当 `MOTION_INTENSITY > 5` 且需求读起来是 premium / playful / agency 时使用。**只能**用 Motion 的 `useMotionValue` / `useTransform` 在 React 渲染周期之外实现。绝不用 `useState`。见第 3.B 节。
* **常驻微交互**（Pulse、Typewriter、Float、Shimmer、Carousel）：当 `MOTION_INTENSITY > 5` 且该 section 确实因动态受益（状态指示、即时动态、AI 感）时使用。**不是每张卡片都需要无限循环。**信息型 section 就让它静止。套用 Spring Physics（`type: "spring", stiffness: 100, damping: 20`）——不用线性 easing。
* **“宣称有动态，就要看得到动态。”**若 `MOTION_INTENSITY > 4`，页面必须真的会动：至少要有 hero 进场转场、关键 section 的 scroll-reveal、CTA 的 hover 物理。宣称 `MOTION_INTENSITY: 7` 却是静态页面，就是坏掉。反过来说，在可用范围内做不出能动的动态时，就把转盘降到 3、出一个干净的静态页面。绝不半吊子地做出会坏的动态（被切断的 ScrollTrigger、跳动的进场、缺 cleanup）。
* **动态必须有动机（强制）。**加任何动画之前先问：“这个动画在传达什么？”有效答案：层级（把注意力引到对的地方）、叙事（依叙事顺序揭示内容）、回馈（回应用户操作）、状态转换（显示某物改变了）。无效答案：“看起来很酷”。因为有 GSAP 就到处用 GSAP 是外行。每个 ScrollTrigger、每个 marquee、每个 pinned section 都需要理由。一句话讲不出理由，就砍掉那个动画。
* **Marquee 每页最多一个（强制）。**水平滚动文本 marquee（“logo 无限滚动”、“宣言横着跑”、“kinetic 文本带”）每页最多用**一次**。同一页出现两个以上 marquee，读起来就是偷懒填充。挑 marquee 真正服务内容的那一个 section；其他的用不同布局。
* **GSAP Sticky-Stack 模式（使用滚动堆栈时）。**“滚动时卡片堆栈”必须是真正的 sticky-stack，不是循序 reveal 清单。标准代码骨架见下方第 5.A 节。常见失败：trigger 在滚动到一半时触发，而不是钉在窗口顶端。修法：`start: "top top"`，不是 `start: "top center"` 或 `"top 80%"`。
* **GSAP 水平平移模式（使用水平滚动劫持时）。**标准骨架见下方第 5.B 节。常见失败：section 还没钉住动画就开始，用户看到半张 slide。同样的修法：`start: "top top"`，钉住 wrapper，scrub 内层 track。

### 5.A Sticky-Stack——标准骨架

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // 钉在窗口顶端
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

关键点：`start: "top top"`、`pin: true`、除最后一张外每张卡都被钉住，缩放/透明度的变形是由“下一张卡”的 scroll trigger 驱动（所以前一张卡在下一张抵达时缩小）。

### 5.B 水平平移（Horizontal-Pan）——标准骨架

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // section 顶端碰到窗口顶端时开始钉住
          end: () => `+=${distance}`,                    // 滚动距离 = track 宽度减窗口宽度
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

关键点：`start: "top top"`、`pin: true`、`end: "+=${distance}"`（滚动长度 = 所需的水平位移）、`scrub: 1`。wrapper 被钉住，内层 track 随用户垂直滚动而水平滑动。

### 5.C Scroll-Reveal Stagger——标准骨架（较轻量的替代）

单纯的“项目进入窗口就出现”（不需钉住）时，优先用 Motion 的 `whileInView` 而不是 GSAP——更轻量、不需要 ScrollTrigger：

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

适用于：功能清单、见证 grid、logo 墙，任何只需要“滚动时进场”的东西。GSAP 留给真正的 pin/scrub 工作。

### 5.D 禁用的动画模式

* **`window.addEventListener("scroll", ...)`** 禁止。它在每个滚动影格都运行、容易卡顿（jank）、无法批量处理。改用 Motion 的 `useScroll()`、GSAP 的 `ScrollTrigger`、IntersectionObserver，或 CSS `scroll-driven animations`（`animation-timeline: view()`）。
* **在 React state 里用 `window.scrollY` 自算滚动进度。**同样的理由。每个影格都重新渲染。
* **会碰 React state 的 `requestAnimationFrame` 循环。**改用 motion values（`useMotionValue` + `useTransform`）。
* **布局转场（Layout Transitions）：**可见的状态变化（清单重新排序、modal 展开、路由间共享元素）用 Motion 的 `layout` 和 `layoutId` props。不要“为了保险”把静态内容包进 `layout` props——它会付出量测成本。
* **交错编排（Staggered Orchestration）：**顺序有意义的 reveal 时刻，用 `staggerChildren`（Motion）或 CSS 级联（`animation-delay: calc(var(--index) * 100ms)`）。使用 `staggerChildren` 时，父层（`variants`）和子层**必须**在同一棵 Client Component 树里。

---

## 6. 性能与无障碍护栏

### 6.A 硬件加速
* 只对 `transform` 和 `opacity` 做动画。绝不对 `top`、`left`、`width`、`height` 做动画。
* `will-change: transform` 节制使用——只放在真的会动的元素上。

### 6.B 减少动态（Reduced Motion，强制）
* **任何 `MOTION_INTENSITY > 3` 的动态都必须遵守 `prefers-reduced-motion`。**没得商量。
* Motion 里：用 `useReducedMotion()` 包住并降级为静态。
* CSS 里：把动画放进 `@media (prefers-reduced-motion: no-preference)`，或在 `@media (prefers-reduced-motion: reduce)` 下提供停用的覆写区块。
* 无限循环、parallax、滚动劫持、磁性物理，在 reduced motion 下**必须**塌缩为静态 / 即时完成。

### 6.C 暗模式（任何消费者导向页面都强制）
* **从一开始就为两种模式设计。**没有用户明确指示，绝不发布只有亮或只有暗的版本。
* 用 Tailwind `dark:` variant 或 CSS 变量做 tokens。一个项目选一种策略。
* **这里不指定具体的暗模式颜色。**由需求决定。两种模式都要维持视觉层级、品牌识别和 WCAG AA 对比（内文 AAA）。
* 尊重 `prefers-color-scheme: dark`。除非品牌坚持单一模式，缺省跟随系统偏好。

### 6.D Core Web Vitals 目标
* **LCP** < 2.5s。Hero 图片必须用 `next/image priority` 或 preload。
* **INP** < 200ms。重活移出主线程。
* **CLS** < 0.1。为图片、字体、embed 预留空间。
* 声明页面完成前先跑 Lighthouse。

### 6.E DOM 成本
* 颗粒 / 噪点滤镜**只能**套在固定的、`pointer-events-none` 的伪元素上（例如 `fixed inset-0 z-[60] pointer-events-none`）。**绝不**套在会滚动的容器上——连续的 GPU 重绘会摧毁移动设备的 FPS。
* 注意 bundle 大小。Motion 不算小，Three.js 很大。不在首屏（above the fold）的东西一律 lazy-load。

### 6.F Z-Index 节制
绝不乱洒 `z-50` 或 `z-10`。z-index 只用在系统性的图层情境（sticky navbar、modal、overlay、颗粒层）。把 z-index 尺度记录在项目常量文件里。

---

## 7. 转盘定义（技术参考）

### DESIGN_VARIANCE（等级 1-10）
* **1-3（可预期）：**对称的 CSS Grid（12 栏、等 fr 单位）、相等的 padding、置中对齐。
* **4-7（偏移）：**`margin-top: -2rem` 的叠压、变化的图片长宽比（4:3 旁边放 16:9）、置中数据上方配靠左标题。
* **8-10（非对称）：**Masonry 布局、分数单位的 CSS Grid（`grid-template-columns: 2fr 1fr 1fr`）、大面积空白区（`padding-left: 20vw`）。
* **移动设备覆写：**等级 4-10 时，`md:` 以上的非对称布局在 `< 768px` 窗口**必须**收合为严格单栏（`w-full`、`px-4`、`py-8`）。

### MOTION_INTENSITY（等级 1-10）
* **1-3（静态）：**没有自动动画。只有 CSS `:hover` 和 `:active` 状态。`prefers-reduced-motion` 本来就是缺省模式。
* **4-7（流畅 CSS）：**`transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`。进场用 `animation-delay` 级联。聚焦在 `transform` 和 `opacity`。
* **8-10（高端编排）：**复杂的滚动触发 reveal、parallax、scroll-driven animation（CSS `animation-timeline` 或 GSAP ScrollTrigger）。用 Motion hooks。**绝不用 `window.addEventListener('scroll')`**——这是硬性禁令，不是“尽量不要”。允许的替代方案见第 5.D 节。

### VISUAL_DENSITY（等级 1-10）
* **1-3（美术馆）：**大量留白。巨大的 section 间距（`py-32` 到 `py-48`）。昂贵、干净。
* **4-7（日常应用）：**标准 web app 间距（`py-16` 到 `py-24`）。
* **8-10（驾驶舱）：**紧凑 padding。不用卡片盒；1px 线条分隔数据。强制：所有数字用 `font-mono`。

---

## 8. 暗模式协定

缺省双模式。除非需求是仿真印刷的 editorial，否则绝不假设只有亮模式。

### 8.A Token 策略（选一个，贯彻到底）
* **Tailwind `dark:` variant**（utility-first 项目的缺省）：每个颜色 utility 都配上暗模式变体（`bg-white dark:bg-zinc-950`、`text-gray-900 dark:text-gray-100`）。
* **CSS 变量**（用于 shadcn/ui、Radix Themes 或有主题机制的组件库）：定义语意化 tokens（`--surface`、`--surface-elevated`、`--text-primary`、`--accent`），在 `[data-theme="dark"]` 或 `@media (prefers-color-scheme: dark)` 下替换值。

### 8.B 这里不指定具体颜色
由需求和品牌决定。本 skill 只强制：
* **对比**——内文至少 WCAG AA，hero 文案以 AAA 为目标。
* **层级对等**——亮模式成立的视觉层级，在暗模式也要成立。CTA 在亮模式跳出来，在暗模式也要跳出来。
* **品牌忠实度**——主品牌色保持可辨识。不要把品牌去饱和到淹没在暗模式里。
* **不用纯 `#000000`、不用纯 `#ffffff`**——用 off-black（zinc-950、近黑暖灰）和 off-white。纯值会扼杀深度。

### 8.C 缺省模式
尊重 `prefers-color-scheme`，除非品牌坚持。若任一模式会丧失关键品牌表现，加一个手动切换。

### 8.D 完成前在两种模式下测试
开发期间就用两种模式打开页面。不要发布一个你只在一种模式下看过的页面。

---

## 9. AI 特征（AI Tells：禁用模式）

除非需求明确要求，否则避开这些签名式模式。

### 9.A 视觉与 CSS
* **缺省不用霓虹 / 外光晕。**改用内边框或细微的染色阴影。
* **不用纯黑（`#000000`）。**用 off-black、zinc-950 或炭灰。
* **不用过饱和的强调色。**去饱和让它融入中性色。
* **大标题不用过量的渐层文本。**
* **不用自订鼠标光标。**过时、对无障碍不友善、对性能不友善。

### 9.B 字体排版
* **避免把 Inter 当缺省。**见第 4.1 节。存在覆写路径。
* **不要只会用超大 H1 吼人。**用字重 + 颜色控制层级，不是靠原始尺寸。
* **衬线限制：**衬线给 editorial / 奢华 / 出版。不给 dashboard。

### 9.C 布局与间距
* **数学上完美**的 padding 和 margin。不要有带着尴尬缝隙的漂浮元素。
* **不用三栏等宽 feature card。**generic 的“三张一样的卡片横排”feature row 是禁止的。改用两栏 zigzag、非对称 grid、scroll-pinned 或水平滚动的替代方案。

### 9.D 内容与数据（“Jane Doe”效应）
* **不用 generic 名字。**“John Doe”、“Sarah Chan”、“Jack Su”→ 用有创意、真实感、符合地区的名字。
* **不用 generic 头像。**不用 SVG“蛋形”或 Lucide user 图标 → 用可信的照片 placeholder 或特定的造型处理。
* **不用假完美的数字。**避免 `99.99%`、`50%`、`1234567`。用有机、混乱的数据（`47.2%`、`+1 (312) 847-1928`）。
* **不用新创垃圾品牌名。**“Acme”、“Nexus”、“SmartFlow”、“Cloudly”→ 发明有情境、听起来真实的高质感名字。
* **不用填充动词。**“Elevate”、“Seamless”、“Unleash”、“Next-Gen”、“Revolutionize”→ 只用具体动词。

### 9.E 外部资源与组件
* **不手刻 SVG 图标。**用 Phosphor / HugeIcons / Radix / Tabler。Lucide 只在明确要求时使用。
* **手刻装饰性 SVG 强烈不建议**当缺省（见第 4.8 节）。
* **不用 div 拼的假截屏。**绝不用 `<div>` 矩形盖一个假产品 UI 来仿真截屏。用真实图片、生成图片，或跳过预览。
* **不用失效的 Unsplash 链接。**用 `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`、生成的照片 placeholder 或实际资产。
* **shadcn/ui 客制：**允许，但**绝不**以缺省状态发布。依项目美学客制圆角、颜色、阴影、字体排版。
* **产品级整洁度：**代码视觉上干净、令人印象深刻、一丝不苟地打磨。

### 9.F 实测验出的特征（直接禁止）

这些模式来自真实的 LLM 生成 landing page 测试。它们是模型想“看起来有设计感”时的缺省签名。除非需求明确要求某一项，否则一律视为硬性禁令。

**Hero 与页面顶部**
* **Hero 里不放版本标签。**`V0.6`、`v2.0`、`BETA`、`INVITE-ONLY PREVIEW`、`EARLY ACCESS`、`ALPHA`——禁止作为缺省 eyebrow。只有需求明确关于产品发表 / 预览状态时才可接受。
* **不用“Brand · No. 01”式的次级 eyebrow。**“Marrow · No. 01 · The 6-quart”这类 micro-meta 行。跳过。

**Section 编号与微标签**
* **不用 section 编号 eyebrow。**`00 / INDEX`、`001 · Capabilities`、`002 · Featured commission`、`06 · how it works`、`05 · The honest table`——禁止。Eyebrow 应该用白话讲主题，不是编号。
* **图片或 bento 磁砖上不放 `01 / 4` 式分页标示。**用户会数数，不需要标签。
* **不用 `Scroll · 001 Capabilities` 式滚动提示。**简单箭头或“Scroll”就够；不加 section 编号前缀。
* **不把“Index of Work, 2018 - 2026”式范围标签**当 eyebrow。直接说这个 section 是什么。

**分隔符与圆点**
* **间隔号（`·`）采配给制。**metadata 条每行最多 1 个。**不要**把它当万用分隔符（“foo · bar · baz · qux · quux”）。需要分隔符家族时，优先用换行、hairline 或分栏。
* **不在每个清单/导览/徽章上放装饰性彩色状态圆点。**“ONE Q4 SLOT OPEN”前的彩点、每个 nav 链接前、每列任务前的彩点——缺省禁止。只有圆点传达真实语意状态（服务器状态、可用性旗标）且节制使用时才可接受。

**Em-dash 与排印花招**
* **Em-dash（`—`）不作为设计元素，也不出现在任何地方。**完整、不可协商的禁令见下方第 9.G 节。em-dash 字符在标题、eyebrow、胶囊、内文、引言、署名、图说、按钮文本和 alt 文本中一律禁止。用一般连字号（`-`）。
* **不把 `<br>` 断行 + 斜体的标题**当缺省“设计手法”。“for thirty\<br\>*years.*”这类切法。标题首先要读起来自然，只有需求要求时才耍聪明。
* **不用垂直旋转文本**（“INDEX OF WORK, 2018 - 2026”转 90°）。agency 作品集的陈腔滥调。只有需求明确是 agency / Awwwards / 实验性、且它服务真正的构图目的时才用。
* **不用十字准星 / hairline 格线当装饰。**只为了让页面“感觉有设计”而画的垂直水平线——禁止。只有在组织真实内容时才用。

**假产品预览**
* **Hero 里不放 div 拼的假产品 UI**（styled div 盖的假任务清单、假终端机、假 dashboard）。这是 LLM 设计特征第一名。用真实截屏、生成图片、真实组件预览，或干脆不放。
* **假截屏里不放假版本 footer**（“v0.6.2-rc.1”、“last sync 4s ago · main”）。毫无贡献，满满 AI 味。

**行销文案特征**
* **不用“Quietly in use at”/“Quietly trusted by”**式社会证明标头。用自然语言：“Trusted by”、“Used at”、“Customers include”，或者 logo 自己会说话时干脆不放标头。
* **不用“From the field”/“Field notes”/“Currently on the bench”/“On our desks”/“Loose plates”式诗意标签**放在引言、博客或侧栏 section 上。读起来是表演型工匠味。用平实的功能标签（“Testimonials”、“Latest writing”、“Now working on”）或不放标签。
* **不用“We respect the French ones”式**假谦虚的同业致意内文。又卖萌又 AI。
* **不用天气 / 地区条**（“LIS 14:23 · 18°C”）在 header/footer，除非需求明确关于某个地点 / 跨时区分布的工作室。
* **Eyebrow 下不放 micro-meta 句子。**像 *“Each of these is a feature we ship today, not a roadmap promise. The list will stay short on purpose.”* 这种挂在 section 标题下的句子是噪音。Eyebrow + 标题 + 内文就够了。
* **不用 generic 步骤标签。**“Stage 1 / Stage 2 / Stage 3”、“Step 1 / Step 2 / Step 3”、“Phase 01 / Phase 02 / Phase 03”、“Pass One / Pass Two / Pass Three”。禁止。实际的步骤内容就是标签。必须呈现进程时，直接用动词-名词（“Install”、“Configure”、“Ship”），不是“Stage 1: Install”。

**胶囊、标签与版本戳**
* **不在图片上叠胶囊/标签/tag。**不要在照片上叠 `<span>` 加 `Brand · 02`、`PLATE · BRAND`、`Field notes - journal` 这类 tag。要嘛让图片自己说话，要嘛在图片正下方（图片之外）加图说。
* **不把摄影署名图说当装饰。**stock/picsum 图片下的 `Field study no. 12 · Ines Caetano`、`Plate 03 · House archive`、`Frame XII · 35mm` 这类字符串很做作。只有真的有摄影师为真实照片挂名（且经同意）时才允许摄影署名。否则：跳过图说，或用一行功能性图说（“The 6-quart, in Sage.”）。
* **行销页不放版本 footer。**footer 里的 `v1.4.2`、`Build 0048`、`last sync 4s ago · main` 是 CLI / 开发工具的配件，不是 landing page 内容。行销 / landing / 作品集页面禁止。
* **不用“Reservation 412 of 800”式即时库存计数器**当装饰。只有需求明确是有真实数据的限量 waitlist 时才行。

**装饰文本条**
* **Hero 底部不放装饰文本条。**`BRAND. MOTION. SPATIAL.`、`TYPE / FORM / MOTION`、`DESIGN · BUILD · SHIP`、`ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` 这类横贯 hero 底部的小型 mono 大写条，是 agency 作品集陈腔滥调。缺省禁止。只有当这条承载真实可导览的链接（sticky 底部导览）或真实状态信息（cookie 横幅、docs 网站的 build 信息）时才可接受。
* **Section 标题不放右上角漂浮小字。**模式：section 有巨大的靠左标题；同一个 section 标头的右上角飘着一小段说明文本，和其他东西都对不齐。那个漂浮物就是特征。要嘛把小字直接放标题下方，要嘛做干净的两栏标头（左：标题，右：对齐的内文），但不要一小段角落文本。

**清单、分隔线与计分**
* **长清单 / 规格表不要每列都 `border-t` + `border-b`。**选一种（列与列之间下边框，或群组上方上边框）并稀疏使用。10 列规格表每列下面一条 hairline 是最偷懒的布局——替代 UI 组件见第 4.9 节。
* **不用有填色背景轨道的计分/进度条**当比较视觉。需要呈现“X / Y”比较时，优先用数字 + 小图标，或**没有**背景轨道的迷你行内长条。大块 `bg-zinc-200` 轨道上盖一段填色，是 landing page 上的 dashboard UI 噪音。

**地区、时间、滚动提示**
* **地区 / 城市名 / 时间 / 天气条对 99% 的需求都是禁止的。**hero 里的“Lisbon, working with founders”、footer 里的“1200-690 Lisbon, Portugal”、nav 里的“Lisbon 14:23 · 18°C”。这些是 agency 作品集装饰特征。只有以下情况允许：需求明确描述一个跨时区分布、时区攸关业务的工作室，或旅游导向的品牌，或真实的实体场馆。footer 提一次联系地址没问题；氛围式地区条不行。
* **滚动提示禁止。**`Scroll`、`↓ scroll`、`Scroll to explore`、`Scroll to walk through it`、动画鼠标滚轮图标。用户还没滚动时，他正在看 hero。他知道什么是滚动。窗口底部不需要标签。
* **缺省零颗装饰性状态圆点。**nav 项目前、清单列前、徽章前、状态标签前的彩色圆点都是特征。只有传达真实语意状态（真实服务器状态的 live 指示、真实可用性旗标）时才可接受，且每个页面 section 最多一颗。

### 9.G EM-DASH 禁令（违反率最高的单一特征）

**Em-dash（`—`）全面禁止。**它是 LLM 的签名式文体拐杖，也是实测中视觉特征第一名。没有“有限度使用”的余地，没有“自然语言频率”的余地，没有“内文里可以”的余地。都没有。

* **标题里禁止。**用句号或逗号。
* **Eyebrow / 标签 / 胶囊 / 按钮文本 / 图说 / nav 项目里禁止。**改用换行、分栏或 hairline。
* **内文里禁止。**重组句子：拆成两句加句号、或逗号、或括号、或冒号。
* **引言署名里禁止。**用带空格的一般连字号（` - `）或换行 + 较细字重的名字。
* **当分隔符用的 en-dash（`–`）也禁止。**日期范围（`2018-2026`）用连字号。数字范围（`€40-80k`）用连字号。

页面上唯一允许的 dash 字符是：
* 一般连字号 `-`（复合词、范围、标记中的分隔线）
* 数学里的负号（`-5°C`）

只要输出中有任何一个用户看得到的 `—` 或 `–`，该输出就没通过 Pre-Flight 检查，必须重写。

这条规则不可协商。过去用“节制使用”的措辞时，agent 一直无视 em-dash 限制。这里的措辞是二元的：零个 em-dash。

---

## 10. 参考词汇（Agent 该认识的模式名称）

这是词汇表，不是函数库。Agent 应该**认识**这些模式名称，才能用它们沟通、带着它们思考设计、并在设计判读需要时伸手取用。**实现与代码草图放在 Block Library（第 12 节），会逐步补上。**

### Hero 范式
* **Asymmetric Split Hero**——文本一侧、资产一侧，大量留白。
* **Editorial Manifesto Hero**——大字级、无资产，近乎海报。
* **Video / Media Mask Hero**——文本作为遮罩镂空在视频背景上。
* **Kinetic-Type Hero**——动态字体排版作为主要视觉。
* **Curtain-Reveal Hero**——滚动时 hero 像布幕一样分开。
* **Scroll-Pinned Hero**——hero 钉住不动，内容在后方滚动。

### 导览与菜单
* **Mac OS Dock Magnification**——边缘导览，图标在 hover 时流畅缩放。
* **Magnetic Button**——被光标吸过去。
* **Gooey Menu**——子项目像黏稠液体般分离。
* **Dynamic Island**——用于状态 / 通知的变形胶囊。
* **Contextual Radial Menu**——在点击处展开的环形菜单。
* **Floating Speed Dial**——FAB 弹出成弧形的次要动作。
* **Mega Menu Reveal**——全屏幕下拉，内容交错淡入。

### 布局与 Grid
* **Bento Grid**——非对称磁砖分组（Apple 控制中心）。
* **Masonry Layout**——交错 grid，无固定列高。
* **Chroma Grid**——边框 / 磁砖带着细微流动的渐层。
* **Split-Screen Scroll**——两半往相反方向滑动。
* **Sticky-Stack Sections**——滚动时钉住并堆栈的 section。

### 卡片与容器
* **Parallax Tilt Card**——追踪鼠标座标的 3D 倾斜。
* **Spotlight Border Card**——边框在光标下方发亮。
* **Glassmorphism Panel**——带内部折射的毛玻璃。
* **Holographic Foil Card**——hover 时虹彩流转。
* **Tinder Swipe Stack**——实体卡叠，滑走即消。
* **Morphing Modal**——按钮自己展开成对话框。

### 滚动动画
* **Sticky Scroll Stack**——卡片黏住并实际堆栈。
* **Horizontal Scroll Hijack**——垂直滚动 → 水平平移。
* **Locomotive / Sequence Scroll**——视频 / 3D 串行绑定滚动条。
* **Zoom Parallax**——中央背景图随滚动放大。
* **Scroll Progress Path**——SVG 线条沿滚动绘制。
* **Liquid Swipe Transition**——像黏稠液体的页面转场。

### 艺廊与媒体
* **Dome Gallery**——3D 全景艺廊。
* **Coverflow Carousel**——边缘倾斜的 3D carousel。
* **Drag-to-Pan Grid**——无边界可拖曳画布。
* **Accordion Image Slider**——窄条在 hover 时展开。
* **Hover Image Trail**——鼠标留下弹出的图片轨迹。
* **Glitch Effect Image**——hover 时 RGB 信道错位。

### 字体排版与文本
* **Kinetic Marquee**——随滚动反向的无尽文本带。
* **Text Mask Reveal**——巨型文本作为透向视频的窗。
* **Text Scramble Effect**——加载 / hover 时的 Matrix 式解码。
* **Circular Text Path**——文本沿旋转圆圈弯曲。
* **Gradient Stroke Animation**——描边文本上流动的渐层。
* **Kinetic Typography Grid**——字母闪避光标。

### 微交互与效果
* **Particle Explosion Button**——CTA 在成功时碎成粒子。
* **Liquid Pull-to-Refresh**——重新加载指示像脱落的水滴。
* **Skeleton Shimmer**——placeholder 上掠过的光影。
* **Directional Hover-Aware Button**——填色从光标进入的那一侧灌入。
* **Ripple Click Effect**——从点击座标散开的波纹。
* **Animated SVG Line Drawing**——矢量即时把自己画出来。
* **Mesh Gradient Background**——有机的熔岩灯色块。
* **Lens Blur Depth**——背景 UI 模糊以聚焦前景动作。

### 动画函数库选择
* **Motion（`motion/react`）**——UI / Bento / 状态变化动态的缺省。
* **GSAP + ScrollTrigger**——整页 scrolltelling 和滚动劫持用。隔离在专属的叶节点组件，配 `useEffect` cleanup。
* **Three.js / WebGL**——canvas 背景和 3D 场景用。同样的隔离规则。
* **绝不在同一棵组件树混用 GSAP / Three.js 和 Motion。**它们会抢同一批影格。

---

## 11. 改版协定（REDESIGN PROTOCOL）

本 skill 同时处理**全新开发（greenfield）和改版**。误判模式是坏改版产出的最大单一来源。

### 11.A 侦测模式（第一个动作）
* **Greenfield**——没有既有网站，或已核准全面翻新。转盘基准值照第 1 节。
* **改版——保留**——现代化但不破坏品牌。先审计、抽取品牌 tokens、逐步演化。
* **改版——翻新**——在既有内容上换新的视觉语言。视觉当 greenfield 处理；保留内容和 IA。

模糊时，问**一次**：*“这次改版要保留既有品牌，还是视觉上从零开始？”*

### 11.B 动手前先审计
提出改动之前，先记录现况：
* **品牌 tokens**——主色 / 强调色、字体堆栈、logo 处理方式、圆角。
* **信息架构（IA）**——页面树、主导览、关键转换路径。
* **内容区块**——有什么、什么在发挥作用、什么是填充。
* **要保留的模式**——招牌交互、有辨识度的 hero、文案声音。
* **要淘汰的模式**——AI 垃圾特征、坏掉的布局、失效链接、generic 图库照、性能陷阱。
* **既有网站的转盘判读**——推断现况的 `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`。那是你的起点，不是基准值。
* **SEO 基线**——目前有排名的页面、meta 标题、结构化数据、OG 卡。**SEO 迁移是改版第一大风险。**

### 11.C 保留规则
* **没被要求就不改信息架构。**保持页面 slug、锚点 ID、主导览标签稳定，为了 SEO 也为了肌肉记忆。
* **套用第 4.2 节之前先抽取品牌色。**本来就是紫色的品牌继续紫——套用紫色守则的覆写条款。
* **没被要求重写就保留文案声音。**视觉现代化 ≠ 内容重写。
* **尊重既有的无障碍成果。**不倒退 focus 状态、alt 文本、键盘导览、对比。
* **尊重既有的分析事件。**不重命名下游追踪所依赖的按钮、表单字段、section ID。

### 11.D 现代化杠杆（优先级）
按顺序套用——需求满足了就停：
1. **字体排版刷新**——每单位风险换到最大视觉提升。
2. **间距与节奏**——加大 section padding、修正垂直节奏。
3. **色彩重新校准**——去饱和、统一中性色、保留品牌强调色。
4. **动态层**——为既有组件加上符合 `MOTION_INTENSITY` 的微交互。
5. **Hero 与关键 section 重组**——用第 10 节词汇重构漏斗顶端。
6. **整块置换**——只在既有区块无药可救时。

### 11.E 决策树：定向演化 vs 全面改版
* IA、内容、SEO 都健全 → **定向演化**（杠杆 1-4）。约 40% 的风险换到约 70% 的价值。
* 视觉债是结构性的（IA 坏掉、没有设计系统、移动版坏掉）→ **全面改版**，严格保留内容。
* 品牌本身在变 → **greenfield**。

### 11.F 绝不默默改动的东西
没有用户明确核准，绝不修改：
* URL 结构 / 路由 slug。
* 主导览标签。
* 表单字段名称或顺序（会弄坏分析 + 自动填入）。
* 品牌 logo 或字标。
* 既有的法律 / 同意 / cookie 文案。

---

## 12. THE BLOCK LIBRARY（契约——实现会逐步补进来）

参考词汇（第 10 节）为模式命名；Block Library 用真实的 props、真实的动态规格、真实的代码草图来实现它们。

**状态：**schema 已在此定义。Block 会逐步加入。不要不照这个 schema 就擅自添加 block。

### 12.A 文件位置
```
skills/taste-skill/blocks/
  hero/
    asymmetric-split.md
    editorial-manifesto.md
    kinetic-type.md
    ...
  feature/
    bento-grid.md
    sticky-scroll-stack.md
    zig-zag.md
    ...
  social-proof/
  pricing/
  cta/
  footer/
  navigation/
  portfolio/
  transition/
```

### 12.B 必要的 Frontmatter
```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "Landing pages with one strong asset and one strong message. Default hero for SaaS, agency, premium consumer."
not_for: "Editorial / manifesto launches where the message IS the design."
stack: ["react", "next", "tailwind", "motion"]
---
```

### 12.C 必要的本文章节
1. **视觉草图**——布局的简短 ASCII 图或描述。
2. **Props API**——组件的接口。
3. **代码草图**——最小可运作实现（缺省 Server Component，动态放 Client island）。
4. **移动设备 fallback**——`< 768px` 的明确收合规则。
5. **动态变体**——每个 `MOTION_INTENSITY` 区间（1-3、4-7、8-10）各一个变体。Reduced-motion fallback 明写。
6. **暗模式笔记**——此 block 专属的 token 策略。
7. **反模式**——此 block 常见的走钟方式。
8. **参考资料**——正式上线的真实范例链接。

### 12.D Block-Library 纪律
* 一个文件一 block。不准多 block 文件。
* 每个 block 必须能独立运作（丢进页面就能渲染）。
* 每个 block 必须通过 Pre-Flight 检查（第 14 节）。
* 依赖于第 2.A 节某设计系统的 block，放在 `blocks/<category>/<name>--<system>.md`（例如 `feature/bento-grid--material.md`）。

---

## 13. 不在范围内

本 skill **不**适用于：
* Dashboard / 高密度产品 UI / 管理后台（用第 2.A 节的 Fluent、Carbon、Atlassian 或 Polaris）。
* 数据表格（用 TanStack Table 或 AG Grid）。
* 多步骤表单 / 精灵（用表单专属模式；本 skill 帮不上忙）。
* 代码编辑器（用 Monaco / CodeMirror 及其官方外观客制）。
* 原生移动设备（直接用 Apple HIG / Material）。
* 即时协作 UI（presence、光标、OT 感知——是另一类问题）。

如果需求属于上述任一项，**明白说出来**，指向正确的工具，并且只把本 skill 的行销页 / 关于页 / landing page 部分套在真正适用的表面上。

---

## 14. 最终 PRE-FLIGHT 检查

输出代码之前跑完这个矩阵。这是最后一道滤网。

**这不是可选的。每一格都要跑。任何一格不过，输出就不算完成。**

- [ ] **需求推断**已声明（第 0.B 节的一行判读）？
- [ ] **转盘值**明确、且是从需求推理出来的，而不是默默用基准值？
- [ ] **设计系统**适用时已从第 2 节选定，或美学已诚实标示？
- [ ] **改版模式**已侦测且审计已做（适用时，第 11 节）？
- [ ] **页面上零个 em-dash（`—`）。**标题、eyebrow、胶囊、内文、引言、署名、图说、按钮、alt 文本。零个。（第 9.G 节——不可协商。）
- [ ] **页面主题锁**：整页只有一个主题（亮、暗或自动）。没有 section 在页中翻成反转模式（第 4.11 节）？
- [ ] **色彩一致性锁**：一个强调色在所有 section 用法一致（第 4.2 节）？
- [ ] **形状一致性锁**：一套圆角系统一致套用（第 4.4 节）？
- [ ] **按钮对比检查**：每个 CTA 文本在其背景上可读（没有白配白，WCAG AA 4.5:1）？
- [ ] **CTA 按钮换行**：桌面版没有 CTA 标签换成 2 行以上？
- [ ] **表单对比检查**：表单输入框、placeholder、focus ring、标签全部对 section 背景通过 WCAG AA？
- [ ] **衬线纪律**：若用了衬线字体，它不是 Fraunces 或 Instrument_Serif（或者是，但有明确的品牌理由）？和你上一个项目用的衬线不同？
- [ ] **Premium-consumer 调色板检查**：若需求是 premium-consumer（锅具 / wellness / 职人 / 奢华），调色板不是 AI 缺省的米白+黄铜+牛血红+深咖啡家族？和你上一个 premium-consumer 项目的家族不同？
- [ ] **Italic 下伸部净空**：每个含 `y g j p q` 的 italic 单字至少 `leading-[1.1]` + `pb-1` 预留？
- [ ] **Hero 塞进窗口**：标题 ≤ 2 行、副文案 ≤ 20 个词且 ≤ 4 行、CTA 不滚动可见、字级有搭配图片规划？
- [ ] **Hero 顶部 padding**：桌面版最多 `pt-24`，hero 内容没有飘到窗口一半？
- [ ] **Hero 堆栈纪律**：hero 最多 4 个文本元素（eyebrow 或品牌列、标题、副文案、CTA）？CTA 下方没有小 tagline、hero 里没有信任微条？
- [ ] **EYEBROW 计数（机械式）**：统计所有组件中 section 标题上方 `uppercase tracking` 微标签的出现次数。次数 ≤ ceil(sectionCount / 3)？Hero 算 1 个。
- [ ] **分割式标头禁令**：没有“左大标题 + 右小段说明”的 section 标头模式（改为垂直堆栈）？
- [ ] **Zigzag 交错上限**：没有 3 个以上连续 section 用同一种图文分割布局？
- [ ] **无重复 CTA 意图**：没有两个相同意图的 CTA（页面上同时有“Get in touch”+“Let's talk”= Fail）？
- [ ] **Logo 墙 = 只有 logo**：logo 下方没印产业 / 类别标签？
- [ ] **Bento 背景多样性**：至少 2-3 个 bento 格有真正的视觉变化（图片、渐层、图样），不是全部白底白字卡？
- [ ] **“Used by / Trusted by”logo 墙**位于 hero 底下、不在 hero 里，用**真实** SVG logo（Simple Icons / devicon）或生成的 SVG 标志，**不是**纯文本字标？
- [ ] **文案自我审计**：每条可见字符串都重读过，没有发布文法坏掉或 AI 幻觉的句子（“free on its past”那类）？
- [ ] **动态有动机**：每个动画都能用一句话说明理由（层级 / 叙事 / 回馈 / 状态转换），没有为秀而秀的 GSAP？
- [ ] **Marquee 每页最多一个**：同一页没有两个水平 marquee？
- [ ] **导览列桌面版单行**、高度 ≤ 80px？
- [ ] **Section 布局重复**检查：没有两个 section 共用同一布局家族（8 个 section 至少 4 种家族）？
- [ ] **Bento 有节奏且格数精确**（N 个项目 → N 格，中间或结尾没有空格）？
- [ ] **长清单用了正确的 UI 组件**（> 5 个项目不用缺省 `<ul>` + `divide-y`——见第 4.9 节替代方案）？
- [ ] **用了真实图片**（生成工具优先，其次 Picsum seed，再来明确的 placeholder 插槽）——没有 div 拼的假截屏、没有手刻装饰 SVG、没有纯文本 minimalism？
- [ ] **图片上没叠胶囊/标签**（没有 `Plate · Brand`、没有 `Field notes - journal`）？
- [ ] **没把摄影署名图说当装饰**（`Field study no. 12 · Ines Caetano`）？
- [ ] **行销页没有版本 footer**（`v1.4.2`、`Build 0048`）？
- [ ] **Eyebrow 下没有 micro-meta 句子**（“Each of these is a feature we ship today...”）？
- [ ] **Hero 底部没有装饰文本条**（`BRAND. MOTION. SPATIAL.`）？
- [ ] **Section 标题没有右上角漂浮小字**？
- [ ] **没有带填色背景轨道的计分/进度条**当比较视觉？
- [ ] **没有地区 / 城市名 / 时间 / 天气条**，除非需求真的是跨地分布或以地点为核心？
- [ ] **没有滚动提示**（`Scroll`、`↓ scroll`、`Scroll to explore`）？
- [ ] **Hero 里没有版本标签**（V0.6、BETA、INVITE-ONLY），除非需求就是产品发表？
- [ ] **没有 section 编号 eyebrow**（`00 / INDEX`、`001 · Capabilities`、`06 · how it works`）？
- [ ] **没有装饰性圆点**（缺省零颗，只给真实语意状态）？
- [ ] **长清单 / 规格表没有每列都 `border-t` + `border-b`**？
- [ ] **内容密度**合理：没有 20 列数据表、没有无理由的假精确规格、副段落缺省 ≤ 25 个词？
- [ ] **引言 ≤ 3 行**本文，署名干净（无 em-dash）？
- [ ] **宣称的动态 = 看得到的动态**：若 `MOTION_INTENSITY > 4`，页面真的会动，不是只有宣称？
- [ ] **GSAP sticky-stack / 水平平移**依第 5.A / 5.B 节标准骨架实现（`start: "top top"`、`pin: true`、正确的 scrub）？
- [ ] **没有 `window.addEventListener('scroll')`**——只用 Motion `useScroll()` / ScrollTrigger / IntersectionObserver / CSS scroll-driven animations？
- [ ] **Reduced motion**：所有 `MOTION_INTENSITY > 3` 的东西都包好了？
- [ ] **暗模式** tokens 已定义且两种模式都测过？
- [ ] **移动设备收合**明写（`w-full`、`px-4`、`max-w-7xl mx-auto`）于高 variance 布局？
- [ ] **窗口稳定性**：`min-h-[100dvh]`，绝不 `h-screen`？
- [ ] **`useEffect` 动画**有严格的 cleanup 函数？
- [ ] **空 / loading / 错误**状态都有提供？
- [ ] **能用间距就省掉卡片**？
- [ ] **图标**只来自允许的函数库（Phosphor / HugeIcons / Radix / Tabler），没有手刻 SVG path？
- [ ] **动态**隔离在顶端有 `'use client'` 的 client 叶节点组件、已 memoize？
- [ ] **没有第 9 节的 AI 特征**（Inter 当缺省、AI 紫、三张等宽卡、Jane Doe、Acme、“Quietly in use at”）？
- [ ] **Core Web Vitals** 合理可达（LCP < 2.5s、INP < 200ms、CLS < 0.1）？
- [ ] **一个项目一个设计系统**（没有 Material + shadcn 混用）？

只要有一格无法诚实打勾，页面就不算完成。修好再交付。

---

# 附录——有真实来源背书的参考素材

以下各节是收录进来（vendored）的参考内容。它们为第 2 节点名的每个设计系统提供真实的安装指令、真实的官方文档链接、以及真实可用的起手 snippet。用它们把决策锚定在生产现实上，而不是训练数据的虚构。

## 附录 A——各设计系统的安装指令

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components（不绑框架）
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui（开放代码、组件归你所有）
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS（GitHub 产品/开发工具 UI）
npm install --save @primer/css

# Primer Brand（GitHub 行销 UI）
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components（仅限 Shopify 应用）
# 把这段加进你的应用 HTML head：
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## 附录 B——标准来源（重新发明之前先读这些）

### Material Web
- https://github.com/material-components/material-web
- https://material-web.dev/theming/material-theming/
- https://m3.material.io/develop/web

### Fluent UI
- https://fluent2.microsoft.design/get-started/develop
- https://fluent2.microsoft.design/components/web/react/
- https://github.com/microsoft/fluentui
- https://learn.microsoft.com/en-us/fluent-ui/web-components/

### Carbon
- https://carbondesignsystem.com/
- https://github.com/carbon-design-system/carbon
- https://carbondesignsystem.com/developing/react-tutorial/overview/
- https://carbondesignsystem.com/developing/web-components-tutorial/overview/

### Shopify Polaris
- https://shopify.dev/docs/api/app-home/web-components
- https://github.com/Shopify/polaris-react
- https://polaris-react.shopify.com/components

### Atlassian
- https://atlassian.design/get-started/develop
- https://atlassian.design/components/button/examples
- https://atlaskit.atlassian.com/packages/design-system/button/example/disabled
- https://atlassian.design/tokens/design-tokens

### Primer
- https://primer.style/
- https://github.com/primer/css
- https://github.com/primer/brand

### GOV.UK
- https://design-system.service.gov.uk/components/button/
- https://design-system.service.gov.uk/styles/layout/
- https://github.com/alphagov/govuk-frontend

### USWDS
- https://designsystem.digital.gov/documentation/developers/
- https://designsystem.digital.gov/components/button/
- https://designsystem.digital.gov/components/card/
- https://github.com/uswds/uswds

### Bootstrap
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/components/card/

### Tailwind
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

### Radix
- https://www.radix-ui.com/themes/docs/components/theme
- https://www.radix-ui.com/themes/docs/components/card
- https://github.com/radix-ui/themes

### shadcn/ui
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/components/card
- https://github.com/shadcn-ui/ui

### 原生 CSS / W3C 标准
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass（仅限 Apple 平台）
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## 附录 C——Apple Liquid Glass：诚实的 Web 近似

**不要**把随便捡来的 CSS snippet 当成官方的 Apple Liquid Glass。

### 什么是官方的
Apple 在其 Human Interface Guidelines 与 Developer Documentation 中为 **Apple 平台**记载了 Liquid Glass。它是用于 Apple 平台 UI 的动态材质。Apple 的原生实现属于 Apple 平台 API 和系统组件，**不是公开的 web CSS 包**。

相关官方文档：
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### 什么不是官方的
Apple 没有给一般网站用的 `liquid-glass.css`。

Web 近似可以使用：
- `backdrop-filter`
- 透明背景
- 多层边框
- highlight 叠层
- 渐层
- 动态
- 高对比 fallback

但那是 **web glassmorphism / 毛玻璃近似**，不是官方的 Apple Liquid Glass。在注释里照实标示。

### 较安全的 web 近似骨架

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

**重要：**`prefers-reduced-transparency` 的浏览器支持参差不齐；要测试。就算没有 blur 也一律提供足够的对比。

---

**附录结束。**上面的安装指令是现实的锚点。Apple Liquid Glass 骨架是有标示的近似，不是 Apple 发行的包。各设计系统的标准文档请查该系统的官方文档（链接在第 2 节与附录 B）。
