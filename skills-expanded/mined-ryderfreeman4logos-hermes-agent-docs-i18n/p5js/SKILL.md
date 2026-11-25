---
name: p5js
description: "p5.js sketches: gen art, shaders, interactive, 3D."
version: 1.0.0
author: SHL0MS, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative-coding, generative-art, p5js, canvas, interactive, visualization, webgl, shaders, animation]
    related_skills: [ascii-video, manim-video, excalidraw]
---

# p5.js 生产级流水线

## 适用场景

当用户需求涉及以下内容时即可使用：p5.js 绘画、创意编程、生成艺术、交互式可视化、画布动画、基于浏览器的视觉艺术、数据可视化、着色器效果，或任何基于 p5.js 的项目。

## 功能概览

该流水线专为使用 p5.js 创作交互式与生成型视觉艺术而设计。它能生成基于浏览器的绘画作品、生成艺术、数据可视化内容、交互体验、3D 场景、音频响应式视觉效果以及动态图形，并可将成果导出为 HTML、PNG、GIF、MP4 或 SVG 格式。其功能涵盖：2D/3D 渲染、噪声与粒子系统、流场模拟、着色器（GLSL）、像素操作、动态文字设计、WebGL 场景、音频分析、鼠标/键盘交互，以及无头模式下的高分辨率导出。

## 创意准则

这是在浏览器中呈现的视觉艺术。画布是创作媒介，算法则是绘图工具。

**在编写任何代码之前**，先明确创意概念。这件作品想要传达什么？是什么让观众停下滚动？它与普通的代码教程示例有何不同？用户的提示只是起点——需以创意的视野去解读它。

**首次渲染效果必须出色**。作品在首次加载时就必须具有强烈的视觉冲击力。如果看起来像 p5.js 教程练习、默认配置，或是“AI 生成的创意编程作品”，那就说明有误。在发布之前务必重新思考。

**超越参考词汇的局限。** 参考资料中的噪声函数、粒子系统、色彩调色板以及着色器效果仅属于基础词汇库。针对每个项目，应进行组合、叠加与创新。这个资源库就像一盒颜料——由你亲自创作出绝妙的艺术作品。

**主动展现创造力。** 当用户要求“一个粒子系统”时，应为其打造具备群体行为特性、拖尾式残影效果、色彩动态变化的深度雾效，以及会随时间变化的背景噪声场的粒子系统。此外，至少要加入一项用户未明确提出但会令其赏心悦目的视觉细节。

**层次丰富、精心设计。** 每一帧画面都应值得细细品味。绝避免使用单调的纯白色背景，务必构建清晰的构图层次，运用有意图的色彩搭配，并加入只有近距离观察才能发现的微小细节。

**注重整体风格统一性而非功能数量。** 所有元素都必须服务于统一的视觉语言——相同的色温、一致的线条粗细规范、和谐的运动速度。一个包含十种互不相关的特效的草图，远不如一个包含三种协调特效的草图出色。

| 模式 | 输入 | 输出 | 参考文档 |
|------|-------|--------|-----------|
| **生成艺术** | 种子值 / 参数 |  procedural视觉作品（静态或动态） | `references/visual-effects.md` |
| **数据可视化** | 数据集 / API | 交互式图表、图形及自定义数据展示 | `references/interaction.md` |
| **交互式体验** | 无（由用户操作） | 鼠标/键盘/触摸操控的绘图功能 | `references/interaction.md` |
| **动画/动态图形** | 时间轴 / 分镜脚本 | 带时间序列控制的动画、动态排版及过渡效果 | `references/animation.md` |
| **3D场景** | 概念描述 | WebGL几何体、光照效果、摄像机设置及材质参数 | `references/webgl-and-3d.md` |
| **图像处理** | 图像文件 | 像素操作、滤镜应用、马赛克效果及点彩风格处理 | `references/visual-effects.md` § 像素操作 |
| **音频响应式** | 音频文件 / 麦克风 | 基于声音生成的视觉效果 | `references/interaction.md` § 音频输入 |

## 技术架构

每个项目仅需一个独立的HTML文件，无需任何构建步骤。

| 层级 | 工具 | 功能 |
|-------|------|------|
| 核心层 | p5.js 1.11.3（CDN版） | 画布渲染、数学运算、变换操作及事件处理 |
| 3D层 | p5.js WebGL模式 | 3D几何体、摄像机控制、光照效果及GLSL着色器 |
| 音频层 | p5.sound.js（CDN版） | FFT频谱分析、音量检测、麦克风输入及振荡器功能 |
| 导出层 | 内置的`saveCanvas()` / `saveGif()` / `saveFrames()`函数 | 支持输出PNG、GIF格式图像及帧序列 |
| 视频捕获层 | CCapture.js（可选） | 实现稳定的固定帧率视频捕获（支持WebM、GIF格式） |
| 无界面渲染层 | Puppeteer + Node.js（可选） | 自动化高分辨率渲染，通过ffmpeg生成MP4文件 |
| SVG输出层 | p5.js-svg 1.6.0（可选） | 用于打印的矢量图形输出——需基于p5.js 1.x版本 |
| 自然媒体模拟层 | p5.brush（可选） | 支持水彩、炭笔、钢笔等绘画效果——需基于p5.js 2.x版本及WEBGL技术 |
| 纹理效果层 | p5.grain（可选） | 添加电影颗粒感及纹理叠加效果 |
| 字体支持层 | Google Fonts / `loadFont()`函数 | 支持通过OTF/TTF/WOFF2格式导入自定义字体 |

### 版本说明

默认使用**p5.js 1.x**（1.11.3版本），该版本稳定性高、文档完善，且兼容的库种类最为丰富。除非项目需要2.x版本的功能，否则建议继续使用此版本。

**p5.js 2.x**（2.2+版本）新增了以下功能：用`async setup()`替代原有的`preload()`函数、OKLCH/OKLAB颜色模式、`splineVertex()`函数、着色器`.modify()`接口、可变字体支持、`textToContours()`函数以及指针事件处理功能。若要使用p5.brush，必须使用2.x版本。更多详情请参阅`references/core-api.md`中关于p5.js 2.0的章节。

## 工作流程

所有项目均遵循相同的6阶段处理流程：

```
CONCEPT → DESIGN → CODE → PREVIEW → EXPORT → VERIFY
```

1. **概念构思** — 阐述创意愿景：整体氛围、色彩体系、动态表现手法，以及该作品的独特之处。  
2. **设计规划** — 选择模式、画布尺寸、交互方式、色彩方案及导出格式，并将概念转化为具体的技术决策。  
3. **代码实现** — 编写一个包含内联 p5.js 代码的 HTML 文件，其结构应为：全局变量 → `preload()` → `setup()` → `draw()` → 辅助函数 → 类 → 事件处理程序。  
4. **预览检查** — 在浏览器中打开文件，验证视觉效果。在目标分辨率下进行测试，并检查性能表现。  
5. **导出输出** — 通过不同方式保存成果：使用 `saveCanvas()` 导出 PNG 格式，`saveGif()` 导出 GIF 格式，`saveFrames()` 结合 ffmpeg 导出 MP4 格式；对于批量无界面处理，则可使用 Puppeteer 工具。  
6. **最终确认** — 确认输出结果是否符合最初的创意构思？在预定的展示尺寸下是否具有足够的视觉冲击力？是否值得装框展示？  

## 创意方向

### 审美维度

| Dimension | Options | Reference |
|-----------|---------|-----------|
| **Color system** | HSB/HSL, RGB, named palettes, procedural harmony, gradient interpolation | `references/color-systems.md` |
| **Noise vocabulary** | Perlin noise, simplex, fractal (octaved), domain warping, curl noise | `references/visual-effects.md` § Noise |
| **Particle systems** | Physics-based, flocking, trail-drawing, attractor-driven, flow-field following | `references/visual-effects.md` § Particles |
| **Shape language** | Geometric primitives, custom vertices, bezier curves, SVG paths | `references/shapes-and-geometry.md` |
| **Motion style** | Eased, spring-based, noise-driven, physics sim, lerped, stepped | `references/animation.md` |
| **Typography** | System fonts, loaded OTF, `textToPoints()` particle text, kinetic | `references/typography.md` |
| **Shader effects** | GLSL fragment/vertex, filter shaders, post-processing, feedback loops | `references/webgl-and-3d.md` § Shaders |
| **Composition** | Grid, radial, golden ratio, rule of thirds, organic scatter, tiled | `references/core-api.md` § Composition |
| **Interaction model** | Mouse follow, click spawn, drag, keyboard state, scroll-driven, mic input | `references/interaction.md` |
| **Blend modes** | `BLEND`, `ADD`, `MULTIPLY`, `SCREEN`, `DIFFERENCE`, `EXCLUSION`, `OVERLAY` | `references/color-systems.md` § Blend Modes |
| **Layering** | `createGraphics()` offscreen buffers, alpha compositing, masking | `references/core-api.md` § Offscreen Buffers |
| **Texture** | Perlin surface, stippling, hatching, halftone, pixel sorting | `references/visual-effects.md` § Texture Generation |

### 项目专属定制规则

切勿使用默认配置。针对每个项目，需遵循以下原则：
- **自定义色彩方案** —— 绝不能直接使用 `fill(255, 0, 0)` 这类原始颜色值，而应采用由3至7种颜色构成的精心设计的色彩组合。
- **自定义线条粗细体系** —— 薄线用于细节装饰（粗细为0.5），中等粗细用于构建结构（1-2），粗线用于突出重点（3-5）。
- **背景处理方式** —— 不能使用简单的 `background(0)` 或 `background(255)`，而应采用带有纹理、渐变或分层效果的背景。
- **动态变化节奏** —— 不同元素需具有不同的运动速度：主要元素以1倍速呈现，次要元素为0.3倍速，背景元素则为0.1倍速。
- **至少一种创新元素** —— 可包含自定义粒子行为、新颖的噪声应用方式，或独特的交互响应机制。

### 项目特有的创新设计

对于每个项目，至少需实现以下一项创新：
- 与项目氛围相匹配的自定义色彩方案（而非预设方案）；
- 独特的新型噪声场组合（例如卷曲噪声+域变形+反馈效果）；
- 自定义的粒子行为（包括自定义力场、自定义轨迹及自定义生成方式）；
- 用户未提出但能提升作品表现力的交互机制；
- 能够构建视觉层次感的构图技巧。

### 参数设计理念

参数应源自算法逻辑，而非通用菜单选项。需思考：“*该*系统有哪些属性是可调节的？”

**优秀的参数**能够展现算法的独特特性：
- **数量** — 粒子、分支或单元的数量（用于控制密度）  
- **尺度** — 噪声频率、元素大小及间距（用于控制纹理质感）  
- **速率** — 速度、生长速率或衰减速度（用于控制能量强度）  
- **阈值** — 行为发生变化的临界点（用于增强戏剧性效果）  
- **比例** — 各种力量之间的平衡关系（用于实现和谐统一）  

**不良参数**是指那些与算法逻辑无关的通用控制项：  
- “color1”、“color2”、“size”等——缺乏上下文则毫无意义  
- 用于控制无关效果的切换开关  
- 仅能改变外观而无法影响行为的参数  

每个参数都应改变算法的*运作逻辑*，而不仅仅是其*视觉表现*。例如，能够调整噪声阶数的“湍流”参数是合理的；而仅能改变`ellipse()`函数半径的“粒子大小”滑块则显得过于浅显。  

## 工作流程

### 第一步：明确创意构想

在编写任何代码之前，先清晰界定以下要素：  
- **氛围与情绪**：希望观众产生何种感受？沉思？振奋？不安？还是愉悦？  
- **视觉叙事**：随着时间推移（或用户交互）会发生什么变化？是构建、衰变、变形还是振荡？  
- **色彩体系**：偏向暖色调还是冷色调？单色系？互补色？哪种颜色为主色调？哪种为点缀色？  
- **形态语言**：有机曲线？锐利几何形状？点状元素？线条？还是多种形式混合？  
- **动态表现**：缓慢漂移？剧烈爆发？有节奏的脉动？还是机械般的精准运动？  
- **独特之处**：究竟是什么让这个作品与众不同？是什么让它成为独一无二的创意？
将用户的提示映射为不同的美学风格。“放松型生成背景”与“故障数据可视化”在各方面都有显著差异。

### 第2步：技术设计

- **模式** — 从上表中的7种模式中选择一种
- **画布尺寸** — 横屏1920x1080、竖屏1080x1920、正方形1080x1080，或自适应尺寸`windowWidth/windowHeight`
- **渲染器** — 默认为`P2D`，如需支持3D效果、着色器及高级混合模式，则使用`WEBGL`
- **帧率** — 交互式场景为60fps，环境动画为30fps，静态生成内容则使用`noLoop()`
- **导出目标** — 浏览器显示、PNG静态图、GIF循环动画、MP4视频或SVG矢量图
- **交互模型** — 被动式（无用户输入）、鼠标驱动、键盘驱动、音频响应式或滚动驱动
- **查看器界面** — 对于交互式生成艺术，可基于`templates/viewer.html`模板开始开发，该模板包含种子导航、参数滑块及下载功能；对于简单草图或视频导出，则可直接使用纯HTML文件

### 第3步：编写代码实现

对于**交互式生成艺术**（如种子探索、参数调整）：从`templates/viewer.html`模板开始。首先仔细阅读模板，保留固定部分（如种子导航和操作按钮），然后替换算法及参数控制逻辑。这样即可实现种子的前进/后退/随机选择/跳转功能、实时更新的参数滑块以及PNG格式的直接下载。

对于**动画、视频导出或简单草图**：直接使用纯HTML文件：

单个HTML文件，结构如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Project Name</title>
  <script>p5.disableFriendlyErrors = true;</script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>
  <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/addons/p5.sound.min.js"></script> -->
  <!-- <script src="https://unpkg.com/p5.js-svg@1.6.0"></script> -->  <!-- SVG export -->
  <!-- <script src="https://cdn.jsdelivr.net/npm/ccapture.js-npmfixed/build/CCapture.all.min.js"></script> -->  <!-- video capture -->
  <style>
    html, body { margin: 0; padding: 0; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
<script>
// === Configuration ===
const CONFIG = {
  seed: 42,
  // ... project-specific params
};

// === Color Palette ===
const PALETTE = {
  bg: '#0a0a0f',
  primary: '#e8d5b7',
  // ...
};

// === Global State ===
let particles = [];

// === Preload (fonts, images, data) ===
function preload() {
  // font = loadFont('...');
}

// === Setup ===
function setup() {
  createCanvas(1920, 1080);
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  colorMode(HSB, 360, 100, 100, 100);
  // Initialize state...
}

// === Draw Loop ===
function draw() {
  // Render frame...
}

// === Helper Functions ===
// ...

// === Classes ===
class Particle {
  // ...
}

// === Event Handlers ===
function mousePressed() { /* ... */ }
function keyPressed() { /* ... */ }
function windowResized() { resizeCanvas(windowWidth, windowHeight); }
</script>
</body>
</html>
```

核心实现模式：
- **种子化随机数生成**：为确保结果可复现，始终使用 `randomSeed()` + `noiseSeed()` 方法
- **颜色模式**：通过 `colorMode(HSB, 360, 100, 100, 100)` 实现直观的颜色控制
- **状态分离**：将参数存储在 CONFIG 中，颜色定义在 PALETTE 中，可变状态则放在全局变量中
- **基于类的实体**：将粒子、智能体及图形视为具有 `update()` 和 `display()` 方法的类
- **离屏缓冲区**：利用 `createGraphics()` 实现分层合成、轨迹效果及遮罩功能

### 第4步：预览与迭代优化

- 直接在浏览器中打开HTML文件——进行基础草图设计时无需服务器
- 若需从本地文件加载图像或字体，可使用 `scripts/serve.sh` 或 `python -m http.server` 命令
- 通过Chrome开发者工具的“性能”标签页检测是否达到60帧/秒的流畅度
- 应在目标导出分辨率下进行测试，而不仅仅是依据窗口尺寸判断
- 不断调整参数，直至视觉效果与第1步设定的概念完全一致

### 第5步：导出成品

| 格式 | 方法 | 命令 |
|------|------|------|
| **PNG** | 在 `keyPressed()` 函数中使用 `saveCanvas('output', 'png')` | 按 ‘s’ 键保存 |
| **高分辨率 PNG** | 使用 Puppeteer 无头模式捕获 | `node scripts/export-frames.js sketch.html --width 3840 --height 2160 --frames 1` |
| **GIF** | `saveGif('output', 5)` —— 捕获 N 秒内容 | 按 ‘g’ 键保存 |
| **帧序列** | `saveFrames('frame', 'png', 10, 30)` —— 以 30fps 捕获 10 秒内容 | 接着执行 `ffmpeg -i frame-%04d.png -c:v libx264 output.mp4` |
| **MP4** | 使用 Puppeteer 捕获帧并配合 ffmpeg 处理 | `bash scripts/render.sh sketch.html output.mp4 --duration 30 --fps 30` |
| **SVG** | 使用 p5.js-svg 函数创建画布 `createCanvas(w, h, SVG)` | `save('output.svg')` |

### 第 6 步：质量验证

- **是否符合设计理念？** 将生成结果与初始创意概念进行对比。如果看起来过于普通，需返回第 1 步重新开始。
- **分辨率检查**：在目标显示尺寸下图像是否清晰？是否存在锯齿现象？
- **性能检查**：在浏览器中能否保持 60fps 的帧率？（动画的最低要求为 30fps）
- **颜色检查**：各颜色搭配是否协调？需在亮色和暗色显示器上分别测试。
- **边缘情况处理**：在画布边缘、尺寸调整时，以及运行 10 分钟后，效果如何？

## 关键实现注意事项

### 性能优化 —— 先禁用 FES

Friendly Error System（友好错误系统）会增加高达 10 倍的额外开销。在所有实际使用的脚本中都应将其禁用。

```javascript
p5.disableFriendlyErrors = true;  // BEFORE setup()

function setup() {
  pixelDensity(1);  // prevent 2x-4x overdraw on retina
  createCanvas(1920, 1080);
}
```

在涉及大量循环的计算任务（如粒子效果、像素操作）中，建议使用 `Math.*` 函数而非 p5 的封装函数——这样能显著提升运行速度。

```javascript
// In draw() or update() hot paths:
let a = Math.sin(t);          // not sin(t)
let r = Math.sqrt(dx*dx+dy*dy); // not dist() — or better: skip sqrt, compare magSq
let v = Math.random();        // not random() — when seed not needed
let m = Math.min(a, b);       // not min(a, b)
```

绝不在 `draw()` 函数内部使用 `console.log()`，也严禁在 `draw()` 中操作 DOM。详情请参阅 `references/troubleshooting.md` 中的“性能”部分。

### 始终采用种子化随机性

每一个生成的草图都必须具备可复现性——相同的种子，必然产生相同的输出。

```javascript
function setup() {
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  // All random() and noise() calls now deterministic
}
```

在生成内容时切勿使用 `Math.random()`，它仅适用于对性能要求极高的非可视化代码。处理视觉元素时则应始终使用 `random()` 函数。如需随机种子，可设置：`CONFIG.seed = floor(random(99999))`。

### 生成艺术平台支持（fxhash / Art Blocks）

对于生成艺术平台，应使用该平台提供的确定性随机数生成器来替代 p5 的 PRNG：

```javascript
// fxhash convention
const SEED = $fx.hash;              // unique per mint
const rng = $fx.rand;               // deterministic PRNG
$fx.features({ palette: 'warm', complexity: 'high' });

// In setup():
randomSeed(SEED);   // for p5's noise()
noiseSeed(SEED);

// Replace random() with rng() for platform determinism
let x = rng() * width;  // instead of random(width)
```

请参阅 `references/export-pipeline.md` 中的“平台导出”部分。

### 颜色模式——使用 HSB

对于生成式艺术而言，HSB（色调、饱和度、亮度）比 RGB 更易于操作：

```javascript
colorMode(HSB, 360, 100, 100, 100);
// Now: fill(hue, sat, bri, alpha)
// Rotate hue: fill((baseHue + offset) % 360, 80, 90)
// Desaturate: fill(hue, sat * 0.3, bri)
// Darken: fill(hue, sat, bri * 0.5)
```

切勿直接硬编码原始的 RGB 值。应先定义调色板对象，再通过程序化方式生成各种变体。详情请参阅 `references/color-systems.md`。

### 噪声效果——多频段处理，而非原始值

使用原始的 `noise(x, y)` 函数会生成平滑的斑点状图案。通过叠加不同频段的噪声，即可获得更自然的纹理效果：

```javascript
function fbm(x, y, octaves = 4) {
  let val = 0, amp = 1, freq = 1, sum = 0;
  for (let i = 0; i < octaves; i++) {
    val += noise(x * freq, y * freq) * amp;
    sum += amp;
    amp *= 0.5;
    freq *= 2;
  }
  return val / sum;
}
```

若需呈现流畅自然的视觉效果，可使用**域变形**技术：将噪声输出值重新作为噪声输入坐标使用。详情请参阅 `references/visual-effects.md`。

### 图层功能必备的 createGraphics() 方法

单次渲染方式会导致画面显得单调乏味。建议使用离屏缓冲区来进行图像合成：

```javascript
let bgLayer, fgLayer, trailLayer;
function setup() {
  createCanvas(1920, 1080);
  bgLayer = createGraphics(width, height);
  fgLayer = createGraphics(width, height);
  trailLayer = createGraphics(width, height);
}
function draw() {
  renderBackground(bgLayer);
  renderTrails(trailLayer);   // persistent, fading
  renderForeground(fgLayer);  // cleared each frame
  image(bgLayer, 0, 0);
  image(trailLayer, 0, 0);
  image(fgLayer, 0, 0);
}
```

### 性能优化——尽可能采用向量化处理

p5.js的绘图调用成本较高。在处理成千上万个粒子时：

```javascript
// SLOW: individual shapes
for (let p of particles) {
  ellipse(p.x, p.y, p.size);
}

// FAST: single shape with beginShape()
beginShape(POINTS);
for (let p of particles) {
  vertex(p.x, p.y);
}
endShape();

// FASTEST: pixel buffer for massive counts
loadPixels();
for (let p of particles) {
  let idx = 4 * (floor(p.y) * width + floor(p.x));
  pixels[idx] = r; pixels[idx+1] = g; pixels[idx+2] = b; pixels[idx+3] = 255;
}
updatePixels();
```

请参阅 `references/troubleshooting.md` 中的“性能”部分。

### 多个草图的实例模式

全局模式会占用 `window` 资源。在正式环境中，建议使用实例模式：

```javascript
const sketch = (p) => {
  p.setup = function() {
    p.createCanvas(800, 800);
  };
  p.draw = function() {
    p.background(0);
    p.ellipse(p.mouseX, p.mouseY, 50);
  };
};
new p5(sketch, 'canvas-container');
```

当需要在同一页面上嵌入多个草图或与各类框架集成时，此选项为必选。

### WebGL 模式注意事项

- `createCanvas(w, h, WEBGL)` — 原点位于中心，而非左上角
- Y轴方向相反（在WEBGL中正Y值表示向上，而在P2D中表示向下）
- 若需获得类似P2D的坐标系，需使用`translate(-width/2, -height/2)`
- 每次执行变换操作前后都应使用`push()`/`pop()` — 否则矩阵栈会在无声无息中溢出
- 应在`rect()`/`plane()`之前调用`texture()`，而非之后
- 自定义着色器：需使用`createShader(vert, frag)` — 建议在多种浏览器上测试

### 导出 — 键盘绑定约定

每个草图都应在`keyPressed()`函数中包含以下内容：

```javascript
function keyPressed() {
  if (key === 's' || key === 'S') saveCanvas('output', 'png');
  if (key === 'g' || key === 'G') saveGif('output', 5);
  if (key === 'r' || key === 'R') { randomSeed(millis()); noiseSeed(millis()); }
  if (key === ' ') CONFIG.paused = !CONFIG.paused;
}
```

### 无界面视频导出——使用 noLoop() 函数

通过 Puppeteer 进行无界面渲染时，该代码示例在初始化阶段**必须**调用 `noLoop()` 函数。如果不使用此函数，p5 的绘制循环会持续运行，从而导致截图速度变慢——此时代码执行速度会远远超过截图速度，进而出现帧数缺失或重复的情况。

```javascript
function setup() {
  createCanvas(1920, 1080);
  pixelDensity(1);
  noLoop();                    // capture script controls frame advance
  window._p5Ready = true;      // signal readiness to capture script
}
```

随附的 `scripts/export-frames.js` 脚本会检测 `_p5Ready` 状态，并在每次捕获时调用一次 `redraw()` 函数，从而实现精确的 1:1 帧对应关系。详情请参阅 `references/export-pipeline.md` 中的“确定性捕获”部分。

对于多场景视频，建议采用逐片段处理架构：为每个场景创建一个独立的 HTML 文件，分别进行渲染，最后使用 `ffmpeg -f concat` 工具将它们合并。相关说明可见 `references/export-pipeline.md` 中的“逐片段架构”部分。

### Agent 工作流程

在编写 p5.js 程序时，请遵循以下步骤：

1. **编写 HTML 文件** —— 创建一个独立的文件，将所有代码直接写在文件中。
2. **在浏览器中打开** —— 在 macOS 上使用 `open sketch.html`，在 Linux 上使用 `xdg-open sketch.html`。
3. **本地资源**（如字体、图片）需要通过服务器提供：在项目目录中运行 `python -m http.server 8080`，然后访问 `http://localhost:8080/sketch.html`。
4. **导出 PNG/GIF 格式** —— 按前述方法添加 `keyPressed()` 快捷键，并告知用户需要按下的按键。
5. **无界面模式导出** —— 使用命令 `node scripts/export-frames.js sketch.html --frames 300` 实现自动帧捕获（程序必须使用 `noLoop()` 和 `_p5Ready` 函数）。
6. **渲染为 MP4 格式** —— 运行命令 `bash scripts/render.sh sketch.html output.mp4 --duration 30`。
7. **迭代优化** —— 修改 HTML 文件后，用户只需刷新浏览器即可查看更改效果。
8. **按需加载参考资料** —— 在开发过程中，可根据需要使用 `skill_view(name="p5js", file_path="references/...")` 函数来加载特定的参考文件。

## 性能目标

| 指标 | 目标值 |
|------|--------|
| 帧率（交互模式） | 持续保持 60fps |
| 帧率（动画导出模式） | 最低 30fps |
| 粒子数量（P2D 形状） | 在 60fps 下为 5,000–10,000 个 |
| 粒子数量（像素缓冲区） | 在 60fps 下为 50,000–100,000 个 |
| 画布分辨率 | 导出时最高可达 3840×2160，交互模式为 1920×1080 |
| 文件大小（HTML 格式） | < 100KB（不含 CDN 库文件） |
| 加载时间 | 到显示第一帧的时间需小于 2秒 |

## 参考资料

| File | Contents |
|------|----------|
| `references/core-api.md` | Canvas setup, coordinate system, draw loop, `push()`/`pop()`, offscreen buffers, composition patterns, `pixelDensity()`, responsive design |
| `references/shapes-and-geometry.md` | 2D primitives, `beginShape()`/`endShape()`, Bezier/Catmull-Rom curves, `vertex()` systems, custom shapes, `p5.Vector`, signed distance fields, SVG path conversion |
| `references/visual-effects.md` | Noise (Perlin, fractal, domain warp, curl), flow fields, particle systems (physics, flocking, trails), pixel manipulation, texture generation (stipple, hatch, halftone), feedback loops, reaction-diffusion |
| `references/animation.md` | Frame-based animation, easing functions, `lerp()`/`map()`, spring physics, state machines, timeline sequencing, `millis()`-based timing, transition patterns |
| `references/typography.md` | `text()`, `loadFont()`, `textToPoints()`, kinetic typography, text masks, font metrics, responsive text sizing |
| `references/color-systems.md` | `colorMode()`, HSB/HSL/RGB, `lerpColor()`, `paletteLerp()`, procedural palettes, color harmony, `blendMode()`, gradient rendering, curated palette library |
| `references/webgl-and-3d.md` | WEBGL renderer, 3D primitives, camera, lighting, materials, custom geometry, GLSL shaders (`createShader()`, `createFilterShader()`), framebuffers, post-processing |
| `references/interaction.md` | Mouse events, keyboard state, touch input, DOM elements, `createSlider()`/`createButton()`, audio input (p5.sound FFT/amplitude), scroll-driven animation, responsive events |
| `references/export-pipeline.md` | `saveCanvas()`, `saveGif()`, `saveFrames()`, deterministic headless capture, ffmpeg frame-to-video, CCapture.js, SVG export, per-clip architecture, platform export (fxhash), video gotchas |
| `references/troubleshooting.md` | Performance profiling, per-pixel budgets, common mistakes, browser compatibility, WebGL debugging, font loading issues, pixel density traps, memory leaks, CORS |
| `templates/viewer.html` | Interactive viewer template: seed navigation (prev/next/random/jump), parameter sliders, download PNG, responsive canvas. Start from this for explorable generative art |

## 创意发散模式（仅当用户要求生成实验性、创意性或独特的输出时使用）

若用户希望获得具有创意、实验性质、出人意料或非传统风格的输出，请在编写代码之前选择最合适的策略，并详细规划其执行步骤。

- **概念融合**——适用于用户希望将两种元素结合或打造混合美学风格的情况  
- **SCAMPER变换法**——适用于用户希望对已有的生成艺术模式进行创新改造的情形  
- **关联迁移**——适用于用户仅给出一个核心概念并希望对其进行拓展探索的情况（例如“围绕‘时间’主题创作内容”）

### 概念融合
1. 确定两种截然不同的视觉系统（例如粒子物理与手写风格）  
2. 建立两者之间的对应关系（将粒子视为墨滴，力场对应笔压，场域则对应字母形态）  
3. 有选择地进行融合——仅保留那些能产生有趣视觉效果的对应关系  
4. 将融合后的效果编码为一个整体系统，而非并排呈现的两个独立系统  

### SCAMPER变换法
对已有的生成艺术模式（如流场、粒子系统、L系统、元胞自动机）进行系统性改造：
- **替换**：用文本字符替代圆形元素，用渐变替代线条  
- **组合**：将两种模式融合在一起（例如流场与沃罗诺伊图结合）  
- **调整**：将二维模式应用于三维场景中  
- **修改**：夸大比例或扭曲坐标空间  
- **重新定义用途**：将物理模拟用于字体设计，或将排序算法用于色彩处理  
- **去除元素**：移除网格、颜色或对称性元素  
- **反向操作**：倒序运行模拟过程，或反转参数空间
### 距离关联机制
1. 以用户的概念为核心（例如“孤独”）。
2. 在三种不同距离层面生成关联内容：
   - 近距离（显而易见）：空荡的房间、独自一人、寂静的氛围。
   - 中等距离（富有趣味）：鱼群中逆流而游的那一条鱼、没有通知的手机、地铁车厢之间的间隙。
   - 远距离（抽象概念）：质数、渐近曲线、凌晨3点的颜色。
3. 重点打造中等距离层面的关联内容——这类关联既具体到可被形象化，又出人意料且充满趣味。
