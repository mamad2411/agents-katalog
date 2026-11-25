---
name: minimalist-ui
description: 干净的编辑风（editorial）接口。暖色调单色（warm monochrome）色盘、字体排版对比、扁平 bento grid、低饱和粉彩色。不用渐层、不用厚重阴影。
---

# Protocol：Premium Utilitarian Minimalism UI 架构师

## 1. Protocol 总览
名称：Premium Utilitarian Minimalism & Editorial UI
说明：一套高端的前端工程指令，用来产出高度精致、极简到底、“文档感（document-style）”的网页接口，类似顶级 workspace 平台的风格。本 protocol 严格运行高对比的暖色调单色色盘、量身打造的字体排版阶层、讲究的结构性大尺度留白（macro-whitespace）、bento grid 布局，以及搭配刻意选用之低饱和粉彩点缀色的超扁平组件架构。它主动排除一般常见的 generic SaaS 设计潮流。

## 2. 绝对负面约束（禁用元素）
AI 必须严格避免以下常见的网页开发缺省做法：
- 不准使用“Inter”、“Roboto”或“Open Sans”字体。
- 不准使用泛用的细线条 icon 库，例如“Lucide”、“Feather”或标准“Heroicons”。
- 不准使用 Tailwind 缺省的厚重阴影（例如 `shadow-md`、`shadow-lg`、`shadow-xl`）。阴影必须几乎不存在，或大幅客制成超柔和扩散、低不透明度（< 0.05）。
- 不准在大面积元素或 section 使用鲜艳主色背景（例如不要有亮蓝、亮绿或亮红的 hero section）。
- 不准使用渐层、荧光色或 3D glassmorphism（仅允许 navbar 的细微模糊效果）。
- 不准对大型容器、卡片或主要按钮使用 `rounded-full`（胶囊形）。
- 不准在代码、标记、文本内容、标题或 alt 文本中的任何地方使用 emoji。改用正式的 icon 或干净的 SVG 基本图形。
- 不准使用“John Doe”、“Acme Corp”或“Lorem Ipsum”这类泛用占位名称。改用贴近情境的真实内容。
- 不准使用 AI 文案陈腔滥调：“Elevate”、“Seamless”、“Unleash”、“Next-Gen”、“Game-changer”、“Delve”。写直白、具体的语言。

## 3. 字体排版架构
接口必须仰赖极端的字体排版对比与高级字体选择，来创建编辑风的质感。
- 主要无衬线字体（内文、UI、按钮）：使用干净、几何或有个性的系统原生字体。目标：`font-family: 'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`。
- 编辑风衬线字体（hero 标题与引言）：目标：`font-family: 'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`。套用紧凑字距（`letter-spacing: -0.02em` 到 `-0.04em`）与紧凑行高（`1.1`）。
- 等宽字体（代码、按键、中继数据）：目标：`font-family: 'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`。
- 文本颜色：内文绝不能用纯黑（`#000000`）。使用近黑／炭灰色（`#111111` 或 `#2F3437`），并搭配宽松的 `line-height`（`1.6`）确保易读性。次要文本使用柔和灰（`#787774`）。

## 4. 色盘（暖色调单色 + 局部粉彩点缀）
颜色是稀缺资源，只用于语意表达或细微点缀。
- 画布／背景：纯白 `#FFFFFF`，或暖骨白／米白 `#F7F6F3` / `#FBFBFA`。
- 主要表面（卡片）：`#FFFFFF` 或 `#F9F9F8`。
- 结构性边框／分隔线：超浅灰 `#EAEAEA` 或 `rgba(0,0,0,0.06)`。
- 点缀色：仅使用高度去饱和、洗白感的粉彩色，用在 tag、行内代码背景或细微的 icon 背景。
  - 淡红：`#FDEBEC`（文本：`#9F2F2D`）
  - 淡蓝：`#E1F3FE`（文本：`#1F6C9F`）
  - 淡绿：`#EDF3EC`（文本：`#346538`）
  - 淡黄：`#FBF3DB`（文本：`#956400`）

## 5. 组件规格
- Bento Box 功能格（feature grid）：
  - 采用不对称的 CSS Grid 布局。
  - 卡片边框必须精确为 `border: 1px solid #EAEAEA`。
  - border-radius 必须俐落：最多 `8px` 或 `12px`。
  - 内距必须充裕（例如 `24px` 到 `40px`）。
- 主要 CTA（按钮）：
  - 实心背景 `#111111`，文本 `#FFFFFF`。
  - 轻微的 border-radius（`4px` 到 `6px`）。不加 box-shadow。
  - hover 状态应是细微的颜色变化到 `#333333`，或微缩放 `transform: scale(0.98)`。
- Tag 与状态徽章：
  - 胶囊形（`border-radius: 9999px`），极小字级（`text-xs`），大写加宽字距（`letter-spacing: 0.05em`）。
  - 背景必须使用前述定义的低饱和粉彩色。
- 手风琴（FAQ）：
  - 拿掉所有容器外框。项目之间只用 `border-bottom: 1px solid #EAEAEA` 分隔。
  - 开合状态用干净、锐利的 `+` 与 `-` icon。
- 按键微型 UI：
  - 用 `<kbd>` 标签把快捷键渲染成实体按键：`border: 1px solid #EAEAEA`、`border-radius: 4px`、`background: #F7F6F3`，并使用等宽字体。
- 仿 OS 窗口外框（Faux-OS Window Chrome）：
  - 仿真软件界面时，包在一个极简容器内，顶部白色横条放三颗浅灰小圆点（重现 macOS 窗口控制钮）。

## 6. Icon 与影像指令
- 系统 icon：使用“Phosphor Icons（Bold 或 Fill 字重）”或“Radix UI Icons”，营造技术感、笔画略粗的美学。所有 icon 的笔画粗细必须统一。
- 插画：单色、粗犷的连续线条墨水速写，置于白色背景上，搭配单一偏移的几何形状并填入低饱和粉彩色。
- 摄影：使用高质量、去饱和的暖色调影像。套用细微叠层（`opacity: 0.04` 的暖色颗粒）让照片融入单色色盘。绝不使用过饱和的 stock 照片。找不到真实素材时，使用可靠的占位图，如 `https://picsum.photos/seed/{context}/1200/800`。
- Hero 与 section 背景：section 不应显得空洞扁平。使用极低不透明度的细微全宽背景影像、柔和的放射状光斑（暖色调 `radial-gradient`、`opacity: 0.03`），或极简的几何线条纹样来增加深度，同时不破坏干净的美学。

## 7. 细微动态与微动画
动态应该“隐形”——存在但绝不抢戏。目标是安静的高级感，不是炫技。
- 滚动进场：元素进入 viewport 时轻柔淡入。使用 `translateY(12px)` + `opacity: 0`，在 `600ms` 内以 `cubic-bezier(0.16, 1, 0.3, 1)` 完成。使用 `IntersectionObserver`，绝不使用 `window.addEventListener('scroll')`。
- Hover 状态：卡片以超细微的阴影变化擡升（`box-shadow` 从 `0 0 0` 过渡到 `0 2px 8px rgba(0,0,0,0.04)`，历时 `200ms`）。按钮在 `:active` 时以 `scale(0.98)` 回应。
- 交错进场：清单与 grid 项目以阶梯延迟进场（`animation-delay: calc(var(--index) * 80ms)`）。绝不一次全部挂载。
- 背景环境动态：可选。单一、移动极慢的放射状渐层色块（`animation-duration: 20s+`、`opacity: 0.02-0.04`）在 hero section 后方漂移。必须套在 `position: fixed; pointer-events: none` 图层上。绝不放在会滚动的容器上。
- 性能：只通过 `transform` 与 `opacity` 做动画。不使用会触发 layout 的属性（`top`、`left`、`width`、`height`）。`will-change: transform` 节制使用，且只用在正在动的元素上。

## 8. 运行 Protocol
接到撰写前端代码（HTML、React、Tailwind、Vue）或设计布局的任务时：
1. 先创建大尺度留白。section 之间使用大量垂直内距（例如 Tailwind 的 `py-24` 或 `py-32`）。
2. 将主要文本内容宽度限制在 `max-w-4xl` 或 `max-w-5xl`。
3. 立刻套用客制的字体排版阶层与单色色彩变量。
4. 确保每张卡片、每条分隔线与边框都严格遵守 `1px solid #EAEAEA` 规则。
5. 为所有主要内容区块加上滚动进场动画。
6. 确保 section 通过影像、环境渐层或细微纹理具有视觉深度——不要空洞扁平的背景。
7. 产出的代码要原生体现这种高级、不杂乱的编辑风美学，无需手动调整。
