---
name: stitch-design-taste
description: 给 Google Stitch 用的语意化设计系统 skill。产出对 agent 友善的 DESIGN.md 文件，强制运行高端、反平庸的 UI 标准——严格的字体排版、校准过的色彩、不对称布局、恒常运作的微动态，以及硬件加速的性能。
---

# Stitch Design Taste — 语意化设计系统 Skill

## 概观
这个 skill 会产出针对 Google Stitch 界面生成优化的 `DESIGN.md` 文件。它把经过实战验证的反平庸（anti-slop）前端工程指令，翻译成 Stitch 原生的语意化设计语言——用描述性的自然语言规则搭配精确的数值，让 Stitch 的 AI agent 能够解读并产出高端、不平庸的接口。

产出的 `DESIGN.md` 是提示 Stitch 生成新界面时的 **single source of truth**，确保新界面符合一套经过策展、高自主性的设计语言。Stitch 通过 **“视觉描述（Visual Descriptions）”**，搭配具体的色彩值、字体规格与组件行为来理解设计。

## 前置条件
- 可通过 [labs.google/stitch](https://labs.google/stitch) 访问 Google Stitch
- 选用：Stitch MCP Server，用于与 Cursor、Antigravity 或 Gemini CLI 做程序化集成

## 目标
产出一份 `DESIGN.md`，编码以下内容：
1. **视觉氛围** — 调性、密度与设计哲学
2. **色彩校准** — 中性色、强调色，以及附上 hex 码的禁用手法
3. **字体架构** — 字体堆栈、级距层级与反面手法
4. **组件行为** — 按钮、卡片、输入字段及其交互状态
5. **布局原则** — 网格系统、间距哲学、响应式策略
6. **动态哲学** — 动画引擎规格、弹簧物理、恒常运作的微交互
7. **反面手法** — 明确列出被禁用的 AI 设计老套路

## 分析与综整指引

### 1. 定义氛围
评估目标项目的意图。从品味光谱中挑选具界面感的形容词：
- **密度（Density）：** “Art Gallery Airy”（1–3）→“Daily App Balanced”（4–7）→“Cockpit Dense”（8–10）
- **变异度（Variance）：** “Predictable Symmetric”（1–3）→“Offset Asymmetric”（4–7）→“Artsy Chaotic”（8–10）
- **动态（Motion）：** “Static Restrained”（1–3）→“Fluid CSS”（4–7）→“Cinematic Choreography”（8–10）

缺省基准：Variance 8、Motion 6、Density 4。依用户描述的 vibe 动态调整。

### 2. 对应色盘
每个颜色都要提供：**描述性名称** ＋ **Hex 码** ＋ **功能角色**。

**强制限制：**
- 最多 1 个强调色。饱和度低于 80%
- “AI 紫／蓝霓虹”美学严格禁用——不要紫色按钮光晕，不要霓虹渐层
- 使用绝对中性的基底（Zinc／Slate），搭配高对比的单一强调色
- 整份输出固定一套色盘——不要在暖灰与冷灰之间摇摆
- 绝对不要用纯黑（`#000000`）——请用 Off-Black、Zinc-950 或 Charcoal

### 3. 创建字体排版规则
- **Display／标题：** 收紧字距、控制级距。不要用吼的。层级靠字重与颜色创建，而不是只靠字级放到很大
- **Body：** 放松的行高，每行最多 65 个字符
- **字体选择：** 高端／创意情境禁用 `Inter`。强制使用有独特个性的字体：`Geist`、`Outfit`、`Cabinet Grotesk` 或 `Satoshi`
- **衬线禁令：** 通用衬线字体（`Times New Roman`、`Georgia`、`Garamond`、`Palatino`）一律禁用。编辑风／创意情境若需要衬线，只能用有辨识度的现代衬线：`Fraunces`、`Gambarino`、`Editorial New` 或 `Instrument Serif`。仪表板与软件 UI 中永远禁用衬线
- **仪表板限制：** 只使用无衬线配对（`Geist` ＋ `Geist Mono`，或 `Satoshi` ＋ `JetBrains Mono`）
- **高密度覆写：** 当密度超过 7，所有数字都必须使用等宽字体

### 4. 定义 Hero 区块
Hero 是第一印象，必须有创意、有冲击力，绝不能平庸：
- **行内图像字体排版（Inline Image Typography）：** 把小张、贴合情境的照片或视觉元素直接嵌在标题的字词或字母之间。图片以字高行内排列、带圆角，充当视觉标点。这是招牌创意手法
- **不重叠：** 文本绝对不能叠在图片或其他文本之上。每个元素都占据自己干净的空间区域
- **不要填充文本：** “Scroll to explore”、“Swipe down”、滚动箭头图标、跳动的 chevron 一律禁用。内容本身就该把用户吸进去
- **不对称结构：** 变异度超过 4 时，置中的 Hero 布局一律禁用
- **CTA 克制：** 最多一个主要 CTA。不要放次要的“Learn more”链接

### 5. 描述组件样式
针对每一类组件，描述形状、颜色、阴影深度与交互行为：
- **按钮：** active 状态要有实体按压般的回馈。不要霓虹外光晕。不要自订鼠标光标
- **卡片：** 只在“高度差能传达层级”时才使用。阴影要调成呼应背景色相。高密度布局请用 border-top 分隔线或负空间取代卡片
- **输入／表单：** 标签在输入框上方，辅助文本选用，错误消息在下方。使用标准的间距
- **加载状态：** 骨架加载（skeletal loader）要符合布局尺寸——不要通用的圆形转圈
- **空状态：** 用编排过的构图说明如何填入数据
- **错误状态：** 清楚的行内错误反馈

### 6. 定义布局原则
- 元素不得重叠——每个元素都占据自己清楚的空间区域。不要用绝对定位堆栈内容
- 变异度超过 4 时，置中的 Hero 区块一律禁用——强制使用分割界面、靠左对齐，或不对称留白
- 通用的“三张等宽卡片横排”功能列一律禁用——请用两栏 Zig-Zag、不对称网格或水平滚动
- CSS Grid 优先于 Flexbox 运算——绝对不要用 `calc()` 百分比的偏方
- 用 max-width 限制布局宽度（例如 1400px 置中）
- 满版高度区块必须用 `min-h-[100dvh]`——绝对不要用 `h-screen`（iOS Safari 会出现灾难性跳动）

### 7. 定义响应式规则
每个设计都必须在所有 viewport 上正常运作：
- **Mobile-First 收合（< 768px）：** 所有多栏布局都收合成单栏。没有例外
- **不得水平滚动：** 移动设备上出现水平溢出属于重大失败
- **字级缩放：** 标题通过 `clamp()` 缩放。内文最小 `1rem`／`14px`
- **触摸目标：** 所有交互元素的点击区至少 `44px`
- **图片行为：** 行内字体排版图片（夹在字词之间的照片）在移动设备上改为堆栈到标题下方
- **导览：** 桌机水平导览在移动设备上收合成干净的菜单
- **间距：** 垂直区块间距等比缩小（`clamp(3rem, 8vw, 6rem)`）

### 8. 编码动态哲学
- **缺省弹簧物理：** `stiffness: 100, damping: 20`——高端、有重量的手感。不要线性缓动
- **恒常微交互：** 每个 active 的组件都应该有无限循环状态（Pulse、Typewriter、Float、Shimmer）
- **交错编排：** 清单绝不瞬间全部挂载——用串连延迟做出瀑布式揭露
- **性能：** 只通过 `transform` 与 `opacity` 做动画。绝对不要动 `top`、`left`、`width`、`height`。颗粒／噪点滤镜只能挂在固定的伪元素上

### 9. 列出反面手法（AI 破绽）
把这些以明确的“NEVER DO”规则写进 DESIGN.md：
- 任何地方都不要 emoji
- 不要用 `Inter` 字体
- 不要用通用衬线字体（`Times New Roman`、`Georgia`、`Garamond`）——需要时只用有辨识度的现代衬线
- 不要用纯黑（`#000000`）
- 不要霓虹／外光晕阴影
- 不要过饱和的强调色
- 大标题不要用过多的渐层文本
- 不要自订鼠标光标
- 元素不得重叠——永远保持干净的空间分隔
- 不要三栏等宽卡片布局
- 不要罐头姓名（“John Doe”、“Acme”、“Nexus”）
- 不要假的整数（`99.99%`、`50%`）
- 不要 AI 文案老套字眼（“Elevate”、“Seamless”、“Unleash”、“Next-Gen”）
- 不要填充式 UI 文本：“Scroll to explore”、“Swipe down”、滚动箭头、跳动的 chevron
- 不要用会失效的 Unsplash 链接——请用 `picsum.photos` 或 SVG 头像
- 不要置中的 Hero 区块（高变异度项目）

## 输出格式（DESIGN.md 结构）

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
（描述调性、密度、变异度与动态强度，要有界面感。
范例：“A restrained, gallery-airy interface with confident asymmetric layouts
and fluid spring-physics motion. The atmosphere is clinical yet warm — like a
well-lit architecture studio.”）

## 2. Color Palette & Roles
- **Canvas White** (#F9FAFB) — 主要背景表面
- **Pure Surface** (#FFFFFF) — 卡片与容器填色
- **Charcoal Ink** (#18181B) — 主要文本，Zinc-950 的深度
- **Muted Steel** (#71717A) — 次要文本、说明、metadata
- **Whisper Border** (rgba(226,232,240,0.5)) — 卡片边框、1px 结构线
- **[Accent Name]** (#XXXXXX) — 单一强调色，用于 CTA、active 状态、focus ring
（最多 1 个强调色。饱和度 < 80%。不要紫色／霓虹。）

## 3. Typography Rules
- **Display：** [Font Name] — 收紧字距、控制级距、以字重驱动层级
- **Body：** [Font Name] — 放松行高、65ch 最大宽度、中性的次要色
- **Mono：** [Font Name] — 用于代码、metadata、时间戳、高密度数字
- **禁用：** Inter、高端情境下的通用系统字体。仪表板中禁用衬线字体。

## 4. Component Stylings
* **按钮：** 扁平、无外光晕。active 时有 -1px 位移的实体感。主要按钮用强调色填满，次要用 ghost／outline。
* **卡片：** 大方的圆角（2.5rem）。扩散式的微弱阴影。只在高度差服务于层级时使用。高密度情境：改用 border-top 分隔线。
* **输入字段：** 标签在上、错误在下。focus ring 使用强调色。不要浮动标签。
* **加载器：** 骨架微光（skeletal shimmer），完全贴合布局尺寸。不要圆形转圈。
* **空状态：** 编排过的插画式构图——不要只写“No data”。

## 5. Layout Principles
（网格优先的响应式架构。Hero 区块使用不对称分割。
768px 以下严格收合为单栏。以 max-width 限制宽度。
不要 flexbox 百分比运算。内部 padding 大方。）

## 6. Motion & Interaction
（所有交互元素采用弹簧物理。交错串连的揭露。
active 的仪表板组件有恒常微循环。只用硬件加速的
transform。CPU 吃重的动画隔离在独立的 Client Component 中。）

## 7. Anti-Patterns (Banned)
（明确列出禁用手法：不要 emoji、不要 Inter、不要纯黑、
不要霓虹光晕、不要三栏等宽网格、不要 AI 文案老套字眼、
不要罐头占位姓名、不要失效的图片链接。）
```

## 最佳实践
- **要有描述性：** 写“Deep Charcoal Ink (#18181B)”，不要只写“深色文本”
- **要讲功能：** 说明每个元素是做什么用的
- **要一致：** 整份文档使用相同的术语
- **要精确：** 在括号中附上确切的 hex 码、rem 值与像素值
- **要有立场：** 这不是中立的模板——它强制运行一套特定的高端美学

## 成功要诀
1. 从氛围开始——先理解 vibe，再细究 token
2. 找出模式——辨识一致的间距、尺寸与样式
3. 用语意思考——依用途命名颜色，不要只依外观
4. 考虑层级——记录视觉重量如何传达重要性
5. 把禁令写进去——反面手法和正面规则一样重要

## 常见陷阱
- 使用未经转译的技术术语（写“rounded-xl”而不是“大方的圆角”）
- 省略 hex 码，或只给描述性名称
- 忘记写设计元素的功能角色
- 氛围描述太笼统
- 忽略反面手法清单——正是这些东西让产出显得高端
- 退回到通用的“安全”设计，而不是贯彻这套策展过的美学
