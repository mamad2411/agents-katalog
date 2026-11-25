---
name: design-taste-frontend-v1
description: 原始 v1 版 taste-skill，为依赖其精确行为的项目保留。目前缺省版本是 `design-taste-frontend`（v2 实验版），属于大幅改写。只有在需要完全向下兼容时才使用这个 v1 安装名称。
---

# High-Agency Frontend Skill（高自主性前端 Skill）

## 1. 现行基准设置（ACTIVE BASELINE CONFIGURATION）
* DESIGN_VARIANCE: 8（1=完美对称，10=艺术性混沌）
* MOTION_INTENSITY: 6（1=静态/无动效，10=电影级/魔法物理）
* VISUAL_DENSITY: 4（1=美术馆/空灵，10=飞机驾驶舱/数据密集）

**AI 指令：**所有产出的标准基准严格设置为这些值（8、6、4）。不要要求用户编辑此文件。除此之外，永远听从用户：根据他们在对话 prompt 中明确要求的内容，动态调整这些值。以这些基准值（或用户覆写后的值）作为全域变量，驱动第 3 到第 7 节的具体逻辑。

## 2. 缺省架构与惯例（DEFAULT ARCHITECTURE & CONVENTIONS）
除非用户明确指定不同的技术堆栈，否则遵守以下结构性约束以维持一致性：

* **依赖包验证【强制】：**在 import 任何第三方函数库（例如 `framer-motion`、`lucide-react`、`zustand`）之前，你必须先检查 `package.json`。如果包不存在，你必须在提供代码之前先输出安装指令（例如 `npm install package-name`）。**绝不**假设函数库已存在。
* **框架与交互性：**React 或 Next.js。缺省使用 Server Components（`RSC`）。
    * **RSC 安全守则：**全域状态只能在 Client Components 中运作。在 Next.js 中，把 provider 包进一个 `"use client"` 组件里。
    * **交互性隔离：**如果第 4 或第 7 节（Motion/Liquid Glass）激活，该交互 UI 组件必须抽出成独立的叶节点组件，并在文件最顶端加上 `'use client'`。Server Components 只能负责渲染静态布局。
* **状态管理：**孤立的 UI 使用本地 `useState`/`useReducer`。全域状态只用来避免深层 prop-drilling。
* **样式策略：**90% 的样式使用 Tailwind CSS（v3/v4）。
    * **TAILWIND 版本锁定：**先检查 `package.json`。不要在 v3 项目中使用 v4 语法。
    * **T4 设置守则：**v4 项目中，不要在 `postcss.config.js` 使用 `tailwindcss` plugin。改用 `@tailwindcss/postcss` 或 Vite plugin。
* **禁用 EMOJI 政策【关键】：**绝不在代码、标记、文本内容或 alt 文本中使用 emoji。改用高质量图标（Radix、Phosphor）或干净的 SVG 基本图形取代符号。Emoji 一律禁用。
* **响应式与间距：**
  * 统一断点（`sm`、`md`、`lg`、`xl`）。
  * 页面布局用 `max-w-[1400px] mx-auto` 或 `max-w-7xl` 收束。
  * **视口稳定性【关键】：**全高 Hero 区块绝不使用 `h-screen`。永远使用 `min-h-[100dvh]`，避免移动浏览器（iOS Safari）上灾难性的布局跳动。
  * **Grid 优先于 Flex 算式：**绝不使用复杂的 flexbox 百分比运算（`w-[calc(33%-1rem)]`）。永远使用 CSS Grid（`grid grid-cols-1 md:grid-cols-3 gap-6`）创建可靠的结构。
* **图标：**你必须精确使用 `@phosphor-icons/react` 或 `@radix-ui/react-icons` 作为 import 路径（检查已安装版本）。全域统一 `strokeWidth`（例如只用 `1.5` 或 `2.0`）。


## 3. 设计工程指令（偏误修正）
LLM 对特定 UI 陈腔滥调模式有统计性偏误。请主动运用以下工程化规则建构高级接口：

**规则 1：确定性字体排版（Deterministic Typography）**
* **Display/标题：**缺省 `text-4xl md:text-6xl tracking-tighter leading-none`。
    * **反 SLOP：**“高级感”或“创意感”的场合不建议用 `Inter`。强制使用 `Geist`、`Outfit`、`Cabinet Grotesk` 或 `Satoshi` 塑造独特个性。
    * **技术类 UI 规则：**Dashboard/软件 UI 严禁使用衬线字体（Serif）。这类情境只能使用高端无衬线（Sans-Serif）配对（`Geist` + `Geist Mono` 或 `Satoshi` + `JetBrains Mono`）。
* **内文/段落：**缺省 `text-base text-gray-600 leading-relaxed max-w-[65ch]`。

**规则 2：色彩校准（Color Calibration）**
* **限制：**最多 1 个强调色（Accent Color）。饱和度 < 80%。
* **紫色禁令（THE LILA BAN）：**“AI 紫/蓝”美学严格禁用。不要紫色按钮光晕，不要霓虹渐层。使用绝对中性的基底（Zinc/Slate），搭配高对比、单一的强调色（例如 Emerald、Electric Blue 或 Deep Rose）。
* **色彩一致性：**整份输出坚持同一套色盘。同一个项目内不要在暖灰与冷灰之间摇摆。

**规则 3：布局多样化（Layout Diversification）**
* **反置中偏误：**当 `DESIGN_VARIANCE > 4` 时，置中的 Hero/H1 区块严格禁用。强制采用“Split Screen”（50/50）、“左对齐内容/右对齐素材”或“非对称留白”结构。

**规则 4：材质、阴影与“反卡片滥用”**
* **DASHBOARD 强化：**当 `VISUAL_DENSITY > 7` 时，泛用的卡片容器严格禁用。改用 `border-t`、`divide-y` 做逻辑分组，或纯粹以负空间（negative space）处理。除非功能上真的需要高度感（z-index），数据指标应该自由呼吸，而不是被框起来。
* **运行方式：**只有当高度感（elevation）能传达层级时才使用卡片。使用阴影时，将其染上背景色调。

**规则 5：交互式 UI 状态**
* **强制产出：**LLM 天生只产“静态”的成功状态。你必须实现完整的交互循环：
  * **加载中：**与布局尺寸相符的 skeleton loader（避免泛用的圆形 spinner）。
  * **空状态（Empty States）：**构图优美的空状态，指引用户如何填入数据。
  * **错误状态：**清楚的行内错误反馈（例如表单）。
  * **触觉回馈：**在 `:active` 时使用 `-translate-y-[1px]` 或 `scale-[0.98]` 仿真实体按压，传达成功/动作。

**规则 6：数据与表单模式**
* **表单：**Label 必须位于 input 上方。辅助文本可有可无，但应存在于标记中。错误文本放 input 下方。input 区块统一使用 `gap-2`。

## 4. 创意主动性（反 Slop 实现）
为了主动对抗千篇一律的 AI 设计，系统性地把以下高端程序概念实现为你的基准：
* **“Liquid Glass”折射：**需要 glassmorphism 时，不要只做 `backdrop-blur`。加上 1px 内边框（`border-white/10`）与细微的内阴影（`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`）仿真实体边缘折射。
* **磁吸微物理（若 MOTION_INTENSITY > 5）：**实现会微微被鼠标光标吸引的按钮。**关键：**磁吸 hover 或连续动画绝不使用 React `useState`。只能使用 Framer Motion 的 `useMotionValue` 与 `useTransform`，在 React 渲染循环之外运作，避免移动设备上的性能崩溃。
* **恒动微交互（Perpetual Micro-Interactions）：**当 `MOTION_INTENSITY > 5` 时，在标准组件（头像、状态点、背景）中嵌入连续、无限循环的微动画（Pulse、Typewriter、Float、Shimmer、Carousel）。所有交互元素套用高级 Spring 物理（`type: "spring", stiffness: 100, damping: 20`）——不使用线性 easing。
* **布局转场（Layout Transitions）：**永远利用 Framer Motion 的 `layout` 与 `layoutId` prop，实现流畅的重排、缩放与跨状态的共享元素转场。
* **交错编排（Staggered Orchestration）：**清单或网格不要瞬间挂载。使用 `staggerChildren`（Framer）或 CSS 级联（`animation-delay: calc(var(--index) * 100ms)`）制造依序瀑布式显现。**关键：**使用 `staggerChildren` 时，父层（`variants`）与子层必须位于同一棵 Client Component 树中。若数据是异步取得，将数据以 props 传入集中式的父层 Motion 包装组件。

## 5. 性能护栏（PERFORMANCE GUARDRAILS）
* **DOM 成本：**颗粒/噪音滤镜只能套用在 fixed、pointer-event-none 的伪元素上（例如 `fixed inset-0 z-50 pointer-events-none`），绝不能套在会滚动的容器上，以避免持续的 GPU 重绘与移动设备性能劣化。
* **硬件加速：**绝不对 `top`、`left`、`width`、`height` 做动画。动画只通过 `transform` 与 `opacity`。
* **Z-Index 克制：**绝不无故滥用 `z-50` 或 `z-10`。z-index 只用于系统性的图层情境（Sticky 导览列、Modal、Overlay）。

## 6. 技术参考（旋钮定义）

### DESIGN_VARIANCE（等级 1-10）
* **1-3（可预测）：**Flexbox `justify-center`、严格的 12 栏对称网格、相等的 padding。
* **4-7（偏移）：**使用 `margin-top: -2rem` 叠合、多样的图片长宽比（例如 4:3 紧邻 16:9）、左对齐标题搭配置中的数据。
* **8-10（非对称）：**Masonry 布局、使用分数单位的 CSS Grid（例如 `grid-template-columns: 2fr 1fr 1fr`）、大面积留白区（`padding-left: 20vw`）。
* **移动设备覆写：**等级 4-10 中，任何 `md:` 以上的非对称布局在 `< 768px` 视口必须强势退回严格的单栏布局（`w-full`、`px-4`、`py-8`），避免水平滚动与布局破损。

### MOTION_INTENSITY（等级 1-10）
* **1-3（静态）：**没有自动动画。只有 CSS `:hover` 与 `:active` 状态。
* **4-7（流畅 CSS）：**使用 `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`。加载动画使用 `animation-delay` 级联。严格聚焦 `transform` 与 `opacity`。`will-change: transform` 节制使用。
* **8-10（高端编舞）：**复杂的滚动触发显现或视差（parallax）。使用 Framer Motion hooks。绝不使用 `window.addEventListener('scroll')`。

### VISUAL_DENSITY（等级 1-10）
* **1-3（美术馆模式）：**大量留白。巨大的区块间距。一切都显得非常昂贵、干净。
* **4-7（日常 App 模式）：**标准 web app 的正常间距。
* **8-10（驾驶舱模式）：**极小的 padding。不用卡片框；只用 1px 线条分隔数据。一切都很紧凑。**强制：**所有数字使用等宽字体（`font-mono`）。

## 7. AI 痕迹（禁用模式）
为了确保输出高级、不落俗套，除非用户明确要求，你必须严格避免以下常见的 AI 设计特征：

### 视觉与 CSS
* **禁止霓虹/外发光：**不要使用缺省的 `box-shadow` 光晕或自动发光。改用内边框或细微的染色阴影。
* **禁止纯黑：**绝不使用 `#000000`。改用 Off-Black、Zinc-950 或 Charcoal。
* **禁止过饱和强调色：**降低强调色饱和度，让它优雅地融入中性色。
* **禁止过度的渐层文本：**大型标题不要使用文本填色渐层。
* **禁止自订鼠标光标：**已经过时，且会摧毁性能与无障碍性。

### 字体排版
* **禁用 Inter 字体：**一律禁止。改用 `Geist`、`Outfit`、`Cabinet Grotesk` 或 `Satoshi`。
* **禁止过大的 H1：**第一个标题不该用吼的。用字重与颜色控制层级，不要只靠巨大的字级。
* **衬线字体限制：**Serif 只能用于创意/编辑类设计。**绝不**在干净的 Dashboard 上使用 Serif。

### 布局与间距
* **对齐与间距要完美：**确保 padding 与 margin 在数学上完美。避免带着别扭空隙的漂浮元素。
* **禁止 3 栏卡片布局：**泛用的“3 张等宽卡片横排”功能列一律禁止。改用 2 栏 Zig-Zag、非对称网格或水平滚动的做法。

### 内容与数据（“Jane Doe”效应）
* **禁止泛用名字：**“John Doe”、“Sarah Chan”、“Jack Su”一律禁止。使用高度创意、听起来真实的名字。
* **禁止泛用头像：**不要用标准 SVG“蛋形”或 Lucide user 图标当头像。使用有创意、可信的照片占位图或特定的风格处理。
* **禁止假数字：**避免可预测的输出如 `99.99%`、`50%` 或阳春的电话号码（`1234567`）。使用有机、带点凌乱感的数据（`47.2%`、`+1 (312) 847-1928`）。
* **禁止新创 Slop 名称：**“Acme”、“Nexus”、“SmartFlow”。发明高级、贴合情境的品牌名称。
* **禁止填充词：**避免 AI 文案陈腔滥调如“Elevate”、“Seamless”、“Unleash”、“Next-Gen”。使用具体的动词。

### 外部资源与组件
* **禁止失效的 Unsplash 链接：**不要使用 Unsplash。使用绝对可靠的占位图，如 `https://picsum.photos/seed/{random_string}/800/600` 或 SVG UI Avatars。
* **shadcn/ui 客制化：**你可以使用 `shadcn/ui`，但绝不能用它泛用的缺省状态。你必须客制化圆角（radii）、颜色与阴影，以符合高端项目美学。
* **正式环境等级的干净度：**代码必须极度干净、视觉震撼、令人难忘，且每个细节都经过精雕细琢。

## 8. 创意军火库（高端灵感）
不要缺省产出泛用 UI。从这座高端概念库中取材，确保输出在视觉上震撼且令人难忘。适当时机，复杂的 scrolltelling 用 **GSAP（ScrollTrigger/Parallax）**、3D/Canvas 动画用 **ThreeJS/WebGL**，而不是阳春的 CSS 动效。**关键：**绝不在同一棵组件树中混用 GSAP/ThreeJS 与 Framer Motion。UI/Bento 交互缺省用 Framer Motion。GSAP/ThreeJS 只用于独立的整页 scrolltelling 或 canvas 背景，并以严格的 useEffect cleanup 区块包装。

### 标准 Hero 范式
* 别再做深色图片上的置中文本了。试试非对称 Hero 区块：文本干净地靠左或靠右对齐。背景使用高质量、切题的图片，并带着细腻的风格化淡出（依 Light 或 Dark 模式，优雅地暗化或亮化融入背景色）。

### 导览与菜单
* **Mac OS Dock 放大效果：**贴齐边缘的导览列；图标在 hover 时流畅缩放。
* **磁吸按钮（Magnetic Button）：**会实际被光标吸过去的按钮。
* **Gooey Menu：**子项目像黏稠液体般从主按钮分离出来。
* **Dynamic Island：**药丸形 UI 组件，会变形以显示状态/通知。
* **情境式放射菜单（Contextual Radial Menu）：**在点击座标精确展开的圆形菜单。
* **悬浮快速拨号（Floating Speed Dial）：**FAB 弹开成一条弧线排列的次要动作。
* **Mega Menu 展开：**全屏幕下拉列表，交错淡入复杂内容。

### 布局与网格
* **Bento Grid：**非对称、砖块式的分组（例如 Apple 控制中心）。
* **Masonry 布局：**列高不固定的交错网格（例如 Pinterest）。
* **Chroma Grid：**网格边框或砖块带着细微、持续变动的色彩渐层。
* **Split Screen Scroll：**滚动时屏幕两半往相反方向滑动。
* **Curtain Reveal：**Hero 区块随滚动像布幕一样从中间拉开。

### 卡片与容器
* **Parallax Tilt Card：**追踪鼠标座标的 3D 倾斜卡片。
* **Spotlight Border Card：**卡片边框在光标下方动态发亮。
* **Glassmorphism Panel：**真正的磨砂玻璃，带内折射边框。
* **Holographic Foil Card：**hover 时流转的虹彩光泽反射。
* **Tinder Swipe Stack：**可以实际滑掉的卡片堆栈。
* **Morphing Modal：**按钮无缝展开成自己的全屏幕对话框容器。

### 滚动动画
* **Sticky Scroll Stack：**卡片黏在顶端，实体般层层堆栈。
* **Horizontal Scroll Hijack：**垂直滚动转换为流畅的水平艺廊平移。
* **Locomotive Scroll Sequence：**影格率直接绑定滚动条的视频/3D 串行。
* **Zoom Parallax：**中央背景图随滚动无缝放大/缩小。
* **Scroll Progress Path：**随用户滚动自行描绘的 SVG 矢量线条或路径。
* **Liquid Swipe Transition：**像黏稠液体般擦过屏幕的页面转场。

### 艺廊与媒体
* **Dome Gallery：**宛如全景穹顶的 3D 艺廊。
* **Coverflow Carousel：**中央聚焦、两侧向后倾斜的 3D 轮播。
* **Drag-to-Pan Grid：**可朝任意方向自由拖曳的无边界网格。
* **Accordion Image Slider：**窄长的直/横向图片条，hover 时完全展开。
* **Hover Image Trail：**鼠标身后留下一串弹出/淡出的图片轨迹。
* **Glitch Effect Image：**hover 时短暂的 RGB 信道偏移数字失真。

### 字体排版与文本
* **Kinetic Marquee：**无尽的文本跑马灯，随滚动反转方向或加速。
* **Text Mask Reveal：**巨型字体排版作为透明窗口，透出视频背景。
* **Text Scramble Effect：**加载或 hover 时的黑客任务式字符解码。
* **Circular Text Path：**沿旋转圆形路径弯曲排列的文本。
* **Gradient Stroke Animation：**描边文本，渐层沿笔画持续流动。
* **Kinetic Typography Grid：**一格格字母闪避光标或随之旋转的网格。

### 微交互与特效
* **Particle Explosion Button：**成功时碎裂成粒子的 CTA。
* **Liquid Pull-to-Refresh：**移动设备刷新指示器像脱落的水滴。
* **Skeleton Shimmer：**占位框上流动的光泽反射。
* **Directional Hover Aware Button：**hover 填色从鼠标实际进入的那一侧流入。
* **Ripple Click Effect：**从点击座标精确扩散的视觉波纹。
* **Animated SVG Line Drawing：**即时描绘自身轮廓的矢量图。
* **Mesh Gradient Background：**有机、熔岩灯般流动的色彩团块。
* **Lens Blur Depth：**动态失焦模糊背景 UI 图层，凸显前景动作。

## 9. “MOTION-ENGINE”BENTO 范式
产生现代 SaaS dashboard 或功能区块时，你必须采用以下“Bento 2.0”架构与动效哲学。这超越了静态卡片，强制实现“Vercel 核心 x Dribbble 洁净”、高度依赖恒动物理的美学。

### A. 核心设计哲学
* **美学：**高端、极简、实用。
* **色盘：**背景 `#f9fafb`。卡片纯白（`#ffffff`），搭配 1px 的 `border-slate-200/50` 边框。
* **表面：**所有主要容器使用 `rounded-[2.5rem]`。套用“扩散阴影”（极淡、大范围扩散的阴影，例如 `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`）创造不杂乱的深度。
* **字体排版：**严格使用 `Geist`、`Satoshi` 或 `Cabinet Grotesk` 字体堆栈。标题用细腻的字距（`tracking-tight`）。
* **标签：**标题与说明必须放在卡片**外部下方**，维持干净、艺廊式的呈现。
* **像素级完美：**卡片内部使用充裕的 `p-8` 或 `p-10` padding。

### B. 动画引擎规格（恒动）
所有卡片都必须包含**“恒动微交互”**。遵循以下 Framer Motion 原则：
* **Spring 物理：**不用线性 easing。使用 `type: "spring", stiffness: 100, damping: 20` 营造高级、有重量的手感。
* **布局转场：**大量运用 `layout` 与 `layoutId` prop，确保流畅的重排、缩放与共享元素状态转场。
* **无限循环：**每张卡片都必须有无限循环的“Active State”（Pulse、Typewriter、Float 或 Carousel），确保 dashboard 感觉“活着”。
* **性能：**动态清单包在 `<AnimatePresence>` 中并优化到 60fps。**性能关键：**任何恒动或无限循环动画都必须 memoize（React.memo），并完全隔离在自己微小的 Client Component 中。绝不触发父层布局的重新渲染。

### C. 五大卡片原型（微动画规格）
建构 Bento grid（例如第 1 列 3 栏 | 第 2 列 70/30 分割 2 栏）时，实现这些特定的微动画：
1. **智能清单（The Intelligent List）：**垂直堆栈的项目，带无限自动排序循环。项目用 `layoutId` 互换位置，仿真 AI 即时排定任务优先序。
2. **指令输入框（The Command Input）：**带多段式打字机效果的搜索/AI 输入列。它循环展示复杂的 prompt，包含闪烁光标与带着微光加载渐层的“处理中”状态。
3. **即时状态（The Live Status）：**带“呼吸感”状态指示灯的调度接口。包含一个以“Overshoot”spring 效果弹出的通知徽章，停留 3 秒后消失。
4. **宽幅数据流（The Wide Data Stream）：**数据卡片或指标的水平“无限轮播”。确保循环无缝（使用 `x: ["0%", "-100%"]`），速度要有毫不费力的感觉。
5. **情境 UI／专注模式（The Contextual UI）：**文档查看界面，先交错地醒目标示一段文本，接着让带微图标的浮动操作工具列“飘入”。

## 10. 最终起飞前检查（FINAL PRE-FLIGHT CHECK）
输出前用这个矩阵查看你的代码。这是你套用在逻辑上的**最后**一道滤网。
- [ ] 全域状态是为了避免深层 prop-drilling 而恰当使用，而非随意使用？
- [ ] 高变异度设计是否保证了移动设备的布局收合（`w-full`、`px-4`、`max-w-7xl mx-auto`）？
- [ ] 全高区块是否安全地使用 `min-h-[100dvh]` 而非有 bug 的 `h-screen`？
- [ ] `useEffect` 动画是否都有严格的 cleanup 函数？
- [ ] 是否提供了空状态、加载与错误状态？
- [ ] 能用留白取代卡片的地方是否都省略了卡片？
- [ ] 吃 CPU 的恒动动画是否严格隔离在自己的 Client Components 中？
