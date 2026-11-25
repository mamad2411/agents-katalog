---
name: industrial-brutalist-ui
description: 粗犷的机械感接口，把瑞士字体排版印刷风（Swiss typographic print）与军用终端机美学融合在一起。刚性 grid、极端的 type scale 对比、实用主义配色、模拟劣化（analog degradation）效果。适合数据密度高的 dashboard、作品集，或想营造解密蓝图质感的编辑型网站。Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects. For data-heavy dashboards, portfolios, or editorial sites that need to feel like declassified blueprints.
---

# SKILL：Industrial Brutalism & Tactical Telemetry UI

## 1. Skill 基本数据
**名称：** Industrial Brutalism & Tactical Telemetry Interface Engineering
**说明：** 高端的网页接口架构能力，融合二十世纪中期的瑞士字体排版设计（Swiss Typographic design）、工业制造手册，以及复古未来感的航太／军用终端机接口。这门功夫要求你彻底掌握刚性的模块化 grid、极端的字体排版尺度对比、纯粹实用主义的色盘，以及用程序仿真模拟劣化效果（halftone 网点、CRT 扫描线、bitmap dithering 抖动）。目标是打造出散发粗犷功能性、机械精准度与高数据密度的数字环境，并刻意舍弃一般消费级 UI 的惯用模式。

## 2. 视觉原型（Visual Archetypes）
这套设计系统靠融合两种截然不同但高度兼容的视觉典范来运作。**每个项目只挑一种，然后贯彻到底。不要在同一个接口里交替或混用两种模式。**

### 2.1 Swiss Industrial Print（瑞士工业印刷）
源自 1960 年代的企业识别系统与重型机械蓝图。
*   **特征：** 高对比的 light mode（新闻纸／米白纸材质感）。仰赖厚重如磐石的粗黑无衬线字体排版。用可见的分隔线勾勒出毫不留情的结构性 grid。负空间的运用强势而不对称，并以超大尺寸、直接出血到 viewport 边缘的数字或字母点题。大量使用原色红作为警示／点缀色。

### 2.2 Tactical Telemetry & CRT Terminal（战术遥测与 CRT 终端机）
源自机密军用数据库、老式大型主机，以及航太的擡头显示器（HUD）。
*   **特征：** 只用 dark mode。高密度的表格式数据呈现。等宽（monospace）字体排版绝对主导。集成技术性的框饰组件（ASCII 括号、准星）。套用仿真的硬件限制（荧光余晖、扫描线、低比特深度渲染）。

## 3. 字体排版架构
字体排版就是主要的结构与装饰基础建设，影像只是次要的。这套系统要求尺度、字重与间距上都有极端落差。

### 3.1 Macro-Typography（结构性标题）
*   **分类：** Neo-Grotesque／粗黑无衬线。
*   **最佳网页字体：** Neue Haas Grotesk (Black)、Inter (Extra Bold/Black)、Archivo Black、Roboto Flex (Heavy)、Monument Extended。
*   **实现参数：**
    *   **尺度（Scale）：** 用流动字体排版（fluid typography）拉到超大尺寸（例如 `clamp(4rem, 10vw, 15rem)`）。
    *   **字距（Tracking／Letter-spacing）：** 极度紧缩，常常是负值（`-0.03em` 到 `-0.06em`），逼字符挤成实心的建筑式量体。
    *   **行距（Leading／Line-height）：** 高度压缩（`0.85` 到 `0.95`）。
    *   **大小写（Casing）：** 一律全大写，强化结构冲击力。

### 3.2 Micro-Typography（数据与遥测）
*   **分类：** Monospace／技术感无衬线。
*   **最佳网页字体：** JetBrains Mono、IBM Plex Mono、Space Mono、VT323、Courier Prime。
*   **实现参数：**
    *   **尺度：** 固定且小（`10px` 到 `14px`／`0.7rem` 到 `0.875rem`）。
    *   **字距：** 放宽（`0.05em` 到 `0.1em`），仿真机械打字机的间距或终端机的字符矩阵。
    *   **行距：** 标准到偏紧（`1.2` 到 `1.4`）。
    *   **大小写：** 一律全大写。所有 metadata、导览、单元编号与座标都用它。

### 3.3 质地对比（艺术性破坏）
*   **分类：** 高对比衬线体。
*   **最佳网页字体：** Playfair Display、EB Garamond、Times New Roman。
*   **实现参数：** 极度节制地使用。必须经过重度后制（halftone 滤镜、1-bit dithering）来破坏矢量的完美感，跟干净的无衬线体形成质地上的对照。

## 4. 色彩系统
色彩架构毫不妥协。严禁渐层、柔和的 drop shadow 与现代感的半透明效果。颜色是用来仿真实体媒材或原始的发光显示器。

**关键：每个项目只选一种基底（substrate）色盘，并贯彻使用。绝不在同一个接口里混用亮色与暗色基底。**

### 若采 Swiss Industrial Print（Light）：
*   **背景：** `#F4F4F0` 或 `#EAE8E3`（雾面、未漂白的文档用纸）。
*   **前景：** `#050505` 到 `#111111`（碳墨黑）。
*   **点缀色：** `#E61919` 或 `#FF2A2A`（航空／警示红）。这是唯一的点缀色。用于删除线、粗的结构性分隔线，或关键数据的强调。

### 若采 Tactical Telemetry（Dark）：
*   **背景：** `#0A0A0A` 或 `#121212`（关机状态的 CRT。避免纯 `#000000`）。
*   **前景：** `#EAEAEA`（白色荧光）。这是主要的文本颜色。
*   **点缀色：** `#E61919` 或 `#FF2A2A`（航空／警示红）。同一个红，同一套规则。
*   **终端机绿（`#4AF626`）：** 可选。只用在单一个特定的 UI 元素上（例如一个状态指示灯或一个数据读数）——绝不当成通用文本颜色。如果它没有明确的用途，就整个不要用。

## 5. 布局与空间工程
布局必须看起来像经过数学计算设计出来的。它拒绝惯例的网页 padding，改用看得见的分区隔间。

*   **蓝图 Grid：** 严格遵守 CSS Grid 架构。元素不会漂浮；它们精准锚定在 grid 的轨道与交会点上。
*   **可见的分区隔间：** 大量使用实线边框（`1px` 或 `2px solid`）来划分不同的信息区域。水平线（`<hr>`）常常横跨整个容器宽度，用来区隔各个作业单元。
*   **双峰密度（Bimodal Density）：** 布局在两个极端之间摆荡——一边是极高的数据密度（紧密堆栈在一起的等宽 metadata），一边是大片经过计算、用来衬托 macro-typography 的负空间。
*   **几何：** 彻底拒绝 `border-radius`。所有转角都必须是精确的 90 度，以贯彻机械式的刚性。

## 6. UI 组件与符号系统
标准的网页 UI 惯例，一律换成实用主义的工业图形元素。

*   **语法装饰：** 用 ASCII 字符把数据点框起来。
    *   *框饰：* `[ DELIVERY SYSTEMS ]`、`< RE-IND >`
    *   *方向指示：* `>>>`、`///`、`\\\\`
*   **工业标记：** 大量集成注册商标（`®`）、著作权（`©`）与商标（`™`）符号，把它们当成结构性的几何元素，而不是法律声明文本。
*   **技术素材：** 在 grid 交会点放上准星（`+`）、重复的垂直线（条码）、粗的水平警示条纹，以及随机字符串数据（例如 `REV 2.6`、`UNIT / D-01`），来仿真机械正在运转的感觉。

## 7. 质地与后制效果
为了避免设计看起来太纯数字，要通过 CSS 与 SVG 滤镜，把仿真的模拟劣化效果实现进前端。

*   **Halftone 与 1-Bit Dithering：** 把连续色调的影像或大尺寸衬线字体转成点矩阵图样。做法是预先处理影像，或用 CSS `mix-blend-mode: multiply` 叠层搭配 SVG 的放射状网点图样。
*   **CRT 扫描线：** 终端机风格的接口，可对背景套用 `repeating-linear-gradient` 来仿真水平电子束扫描（例如 `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`）。
*   **机械噪音：** 在 DOM 根节点套用一层全域、低不透明度的 SVG 噪音滤镜，让 dark mode 与 light mode 都带有统一的实体颗粒感。

## 8. 网页工程指令
1.  **Grid 决定论：** 用 `display: grid; gap: 1px;` 搭配父子元素对比的背景色，不必写复杂的 border 声明，就能产生数学上完美、细如刀锋的分隔线。
2.  **语意刚性：** 用精确的语意标签（`<data>`、`<samp>`、`<kbd>`、`<output>`、`<dl>`）来建构 DOM，准确反映遥测数据的技术本质。
3.  **Typography Clamping：** CSS `clamp()` 函数只用在 macro-typography 上，确保超大文本能强势缩放，同时在各种 viewport 下都维持结构完整性。
