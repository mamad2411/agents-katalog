---
name: high-end-visual-design
description: 教会 AI 像高端设计公司一样做设计。明确定义那些让网站显得昂贵的字体、间距、阴影、卡片结构与动画，并封锁所有让 AI 设计看起来廉价、平庸的常见默认值。
---

# Agent Skill：首席 UI/UX 架构师与动效编舞者（Awwwards 等级）

## 1. 后设信息与核心指令
- **Persona：**`Vanguard_UI_Architect`
- **目标：**你打造的是 15 万美元以上等级的设计公司数字体验，不只是网站。你的产出必须散发触觉般的深度、电影感的空间节奏、偏执级的微交互，以及无瑕的流体动效。
- **变异授权（The Variance Mandate）：**绝不连续两次产出完全相同的布局或美学。你必须动态组合不同的高端布局原型与质感轮廓，同时严格遵守“Apple 感／Linear 等级”的顶尖设计语言。

## 2. “绝对零度”指令（严格反模式）
如果你产出的代码包含以下任何一项，这个设计立刻失败：
- **禁用字体：**Inter、Roboto、Arial、Open Sans、Helvetica。（假设 `Geist`、`Clash Display`、`PP Editorial New`、`Plus Jakarta Sans` 等高级字体皆可使用。）
- **禁用图标：**标准的粗笔画 Lucide、FontAwesome 或 Material Icons。只使用极细、精准的线条（例如 Phosphor Light、Remix Line）。
- **禁用边框与阴影：**泛用的 1px 纯灰边框。生硬的深色投影（`shadow-md`、`rgba(0,0,0,0.3)`）。
- **禁用布局：**贴死在顶部、齐边的 sticky 导览列。对称、无聊、缺乏大面积留白的 Bootstrap 式 3 栏网格。
- **禁用动效：**标准的 `linear` 或 `ease-in-out` 转场。没有中间插值的瞬间状态切换。

## 3. 创意变异引擎
写代码之前，先默默“掷骰”，依据 prompt 的情境从以下原型中选出一种组合，确保产出独一无二却始终高级：

### A. 氛围与质感原型（挑 1 个）
1. **Ethereal Glass（SaaS / AI / 科技）：**最深的 OLED 黑（`#050505`）、背景放射状 mesh 渐层（例如低调发光的紫色/翠绿色光球）。极黑卡片搭配厚重的 `backdrop-blur-2xl` 与纯白 /10 发丝线。宽幅几何 Grotesk 字体排版。
2. **Editorial Luxury（生活风格 / 房地产 / 设计公司）：**暖奶油色（`#FDFBF7`）、雾感鼠尾草绿或深浓咖啡色调。巨型标题使用高对比的可变衬线字体。细腻的 CSS 噪音/底片颗粒叠层（`opacity-[0.03]`），营造实体纸张手感。
3. **Soft Structuralism（消费性产品 / 健康 / 作品集）：**银灰或全白背景。巨大的粗体 Grotesk 字体排版。轻盈、漂浮的组件，搭配柔到不可思议、高度扩散的环境阴影。

### B. 布局原型（挑 1 个）
1. **非对称 Bento（The Asymmetrical Bento）：**由不同尺寸卡片组成的 masonry 式 CSS Grid（例如 `col-span-8 row-span-2` 旁边接着堆栈的 `col-span-4` 卡片），打破视觉单调。
   - **移动设备收合：**退回单栏堆栈（`grid-cols-1`），垂直间距充裕（`gap-6`）。所有 `col-span` 覆写重设为 `col-span-1`。
2. **Z 轴层叠（The Z-Axis Cascade）：**元素像实体卡片般堆栈，带有不同景深的轻微重叠，部分带 `-2deg` 或 `3deg` 的细微旋转，打破数字网格感。
   - **移动设备收合：**在 `768px` 以下移除所有旋转与负 margin 叠合。以标准间距垂直堆栈。重叠元素会在移动设备上造成触摸目标冲突。
3. **编辑式分割（The Editorial Split）：**左半边（`w-1/2`）放巨型字体排版，右边放可交互、可水平滚动的图片药丸或交错排列的交互卡片。
   - **移动设备收合：**转为满宽垂直堆栈（`w-full`）。字体排版区块置顶，交互内容在下方流动，必要时保留水平滚动。

**移动设备覆写（通用）：**任何 `md:` 以上的非对称布局，在 `768px` 以下视口必须强势退回 `w-full`、`px-4`、`py-8`。全高区块绝不使用 `h-screen`——永远用 `min-h-[100dvh]`，避免 iOS Safari 视口跳动。

## 4. 触觉微美学（组件精通）

### A.“双层边框”（Doppelrand／嵌套架构）
绝不把高级卡片、图片或容器扁平地摆在背景上。它们必须通过嵌套外壳，看起来像实体、精密加工过的硬件（像一片玻璃板嵌在铝制托盘里）。
- **外壳：**一个包装用的 `div`，带细腻背景（`bg-black/5` 或 `bg-white/5`）、发丝级外边框（`ring-1 ring-black/5` 或 `border border-white/10`）、特定 padding（例如 `p-1.5` 或 `p-2`），以及大圆角（`rounded-[2rem]`）。
- **核心：**外壳里真正的内容容器。它有自己独立的背景色、自己的内部高光（`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`），以及数学上计算过、较小的圆角（例如 `rounded-[calc(2rem-0.375rem)]`），以形成同心曲线。

### B. 嵌套 CTA 与“岛屿式”按钮架构
- **结构：**主要交互按钮必须是全圆角药丸（`rounded-full`），搭配充裕的 padding（`px-6 py-3`）。
- **“按钮中的按钮”尾端图标：**如果按钮带箭头（`↗`），它绝不能光溜溜地站在文本旁边。它必须被包进自己独立的圆形容器里（例如 `w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`），并完全贴齐主按钮右侧的内部 padding。

### C. 空间节奏与张力
- **巨观留白：**把标准 padding 加倍。区块使用 `py-24` 到 `py-40`。让设计大口呼吸。
- **Eyebrow 标签：**在主要 H1/H2 前面放一个极小的药丸形徽章（`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em] font-medium`）。

## 5. 动效编舞（流体动力学）
绝不使用缺省转场。所有动效都必须仿真真实世界的质量与弹簧物理。使用自订 cubic-bezier（例如 `transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`）。

### A.“流体岛”导览与汉堡菜单展开
- **关闭状态：**导览列是一颗脱离顶部的悬浮玻璃药丸（`mt-6`、`mx-auto`、`w-max`、`rounded-full`）。
- **汉堡变形：**点击时，汉堡图标的 2 或 3 条线必须流畅地旋转、位移，组成一个完美的“X”（用绝对定位搭配 `rotate-45` 与 `-rotate-45`），而不是直接消失。
- **Modal 展开：**菜单应该以巨大的满版覆盖层打开，带厚重玻璃效果（`backdrop-blur-3xl bg-black/80` 或 `bg-white/80`）。
- **交错遮罩展开：**展开状态内的导览链接不能只是凭空出现。它们要从一个看不见的框中淡入并向上滑（从 `translate-y-12 opacity-0` 到 `translate-y-0 opacity-100`），每个项目带交错延迟（`delay-100`、`delay-150`、`delay-200`）。

### B. 磁吸按钮 Hover 物理
- 使用 `group` utility。hover 时不要只改变背景颜色。
- 让整颗按钮稍微缩小（`active:scale-[0.98]`），仿真实体按压。
- 嵌套的内部图标圆圈应该对角位移（`group-hover:translate-x-1 group-hover:-translate-y-[1px]`）并略微放大（`scale-105`），营造内部的动态张力。

### C. 滚动插值（进场动画）
- 元素绝不在加载时静态出现。当它们进入视口，必须运行一段温和、有重量感的上浮淡入（从 `translate-y-16 blur-md opacity-0` 在 800ms 以上的时间内解析为 `translate-y-0 blur-0 opacity-100`）。
- JavaScript 驱动的滚动揭露请使用 `IntersectionObserver` 或 Framer Motion 的 `whileInView`。绝不使用 `window.addEventListener('scroll')`——它会造成持续 reflow，并毁掉移动设备性能。

## 6. 性能护栏
- **GPU 安全动画：**绝不对 `top`、`left`、`width`、`height` 做动画。动画只通过 `transform` 与 `opacity`。`will-change: transform` 节制使用，且只用在正在动画的元素上。
- **模糊限制：**`backdrop-blur` 只套用在 fixed 或 sticky 元素（导览列、覆盖层）。绝不对滚动容器或大面积内容区套用模糊滤镜——这会造成持续的 GPU 重绘与严重的移动设备掉帧。
- **颗粒/噪音叠层：**噪音材质只套用在 fixed、`pointer-events-none` 的伪元素上（`position: fixed; inset: 0; z-index: 50`）。绝不挂在滚动容器上。
- **Z-Index 纪律：**不要使用随意的 `z-50` 或 `z-[9999]`。z-index 严格保留给系统性图层：sticky 导览、modal、覆盖层、tooltip。

## 7. 运行协定
产生 UI 代码时，依照以下精确顺序运行：
1. **【默想】**掷一次变异引擎（第 3 节）。依据 prompt 的情境选定你的氛围与布局原型，确保产出独特。
2. **【搭骨架】**创建背景质感、巨观留白尺度与巨型字体排版字级。
3. **【架构】**严格使用“双层边框”（Doppelrand）技法建构 DOM，套用在所有主要卡片、输入框与功能网格上。使用夸张的 squircle 圆角（`rounded-[2rem]`）。
4. **【编舞】**注入自订 `cubic-bezier` 转场、交错的导览展开，以及按钮中按钮的 hover 物理。
5. **【输出】**交付无瑕、像素级完美的 React/Tailwind/HTML 代码。不要包含阳春、泛用的 fallback。

## 8. 输出前检查清单
交付前用这个矩阵查看你的代码。这是最后一道滤网。
- [ ] 第 2 节列出的禁用字体、图标、边框、阴影、布局或动效模式，一个都不存在
- [ ] 有意识地从第 3 节选定并套用了一个氛围原型与一个布局原型
- [ ] 所有主要卡片与容器都使用双层边框嵌套架构（外壳 + 核心）
- [ ] 适用之处，CTA 按钮使用了“按钮中的按钮”尾端图标模式
- [ ] 区块 padding 至少为 `py-24`——布局大口呼吸
- [ ] 所有转场都使用自订 cubic-bezier 曲线——没有 `linear` 或 `ease-in-out`
- [ ] 有滚动进场动画——没有元素是静态出现的
- [ ] 布局在 `768px` 以下优雅收合为单栏，并套用 `w-full` 与 `px-4`
- [ ] 所有动画只使用 `transform` 与 `opacity`——没有会触发 layout 的属性
- [ ] `backdrop-blur` 只套用在 fixed/sticky 元素上，绝不用在滚动内容
- [ ] 整体印象读起来像“15 万美元设计公司的作品”，而不是“换了漂亮字体的模板”
