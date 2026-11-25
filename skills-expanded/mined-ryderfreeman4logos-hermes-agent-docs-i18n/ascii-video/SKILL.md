---
name: ascii-video
description: "ASCII video: convert video/audio to colored ASCII MP4/GIF."
version: 1.0.0
author: SHL0MS, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ASCII, Video, FFmpeg, Terminal-Art]
    related_skills: []
---

# ASCII视频制作流程

## 适用场景

当用户请求生成以下内容时即可使用：ASCII视频、文字艺术视频、终端风格视频、字符艺术动画、复古风格文本可视化、ASCII格式的音频可视化效果、将视频转换为ASCII艺术、矩阵风格特效，或任何形式的动态ASCII输出内容。

## 功能说明

该流程可处理各类格式的ASCII艺术视频，能够将视频、音频、图片或生成式输入转换为带颜色的ASCII字符视频输出（支持MP4、GIF及图像序列格式）。主要功能包括：视频转ASCII转换、随音频变化的音乐可视化效果、生成式ASCII艺术动画、视频与音频同步的混合效果、文本/歌词叠加功能，以及实时终端渲染。

## 创意准则

这属于视觉艺术范畴，ASCII字符只是表现媒介，而电影级质量才是标准。

在编写任何一行代码之前，首先需明确创意概念：整体氛围是怎样的？要讲述怎样的视觉故事？为何这个项目能与其他ASCII视频作品区分开来？用户的提示仅是起点，应以富有创意的视角去解读，而非机械地照搬文字内容。

**初次渲染的结果就必须达到卓越水准**，无需经过多次修改即可呈现出令人惊艳的视觉效果。如果输出结果显得千篇一律、缺乏层次，或是类似“AI生成的ASCII艺术”，那就说明思路有误——在最终交付之前，务必重新审视创意概念。

**超越参考词汇的局限。** 参考资料中的效果目录、着色器预设和调色板库仅作为基础词汇使用。针对每个项目，应将这些元素进行组合、修改，甚至创造全新的视觉模式。这些目录就好比画具箱——而你才是执笔作画的艺术家。

**主动发挥创造力。** 当项目需求超出参考范围时，及时扩展相关技能的词汇库。如果现有资源无法满足创意构想，那就自行打造所需效果。务必加入至少一个用户虽未要求但会倍感惊喜的视觉元素——无论是转场效果、特殊特效，还是能提升整体品质的色彩选择。

**注重整体美学而非技术完美度。** 视频中的所有场景都应通过统一的视觉语言紧密相连——相同的色温、协调的角色色调、一致的运动表现手法。即便技术上毫无瑕疵，但若每个场景都使用截然不同的效果，依然属于美学上的失败。

**内容丰富、层次分明且经过精心设计。** 每一帧画面都应值得细细品味。杜绝单调的纯黑色背景，始终采用多网格构图，确保每个场景都有独特变化，并且色彩运用必须充满意图性。

| 模式 | 输入 | 输出 | 参考文档 |
|------|-------|--------|-----------|
| **视频转ASCII** | 视频文件 | 原始视频的ASCII格式再现 | `references/inputs.md` § 视频采样 |
| **音频驱动型** | 音频文件 | 基于音频特征生成的视觉内容 | `references/inputs.md` § 音频分析 |
| **生成型** | 无（或种子参数） | 程序化生成的ASCII动画 | `references/effects.md` |
| **混合型** | 视频 + 音频 | 带有音频驱动型叠加效果的ASCII视频 | 参考上述两类输入的文档 |
| **歌词/文本型** | 音频 + 文本/SRT文件 | 带有视觉效果的时间同步文本 | `references/inputs.md` § 文本/歌词处理 |
| **TTS旁白型** | 文本引语 + TTS API | 包含打字效果的旁白或引语视频 | `references/inputs.md` § TTS集成 |

## 技术栈

每个项目仅包含一个独立的Python脚本，无需GPU支持。

| 层级 | 工具 | 用途 |
|------|-------|---------|
| 核心层 | Python 3.10+、NumPy | 数学运算、数组操作、向量化效果处理 |
| 信号处理层 | SciPy | FFT变换、峰值检测（音频模式） |
| 图像处理层 | Pillow (PIL) | 字体光栅化、帧解码、图像读写 |
| 视频处理层 | ffmpeg（命令行工具） | 解码输入文件、编码输出文件、音频混音 |
| 并行处理层 | concurrent.futures | 支持多工作线程进行批量或片段渲染 |
| TTS处理层 | ElevenLabs API（可选） | 生成旁白视频片段 |
| 可选扩展层 | OpenCV | 视频帧采样、边缘检测 |

## 流程架构

所有模式均遵循相同的6阶段处理流程：

```
INPUT → ANALYZE → SCENE_FN → TONEMAP → SHADE → ENCODE
```

1. **INPUT** — 加载/解码原始素材（视频帧、音频样本、图像，或无数据）  
2. **ANALYZE** — 提取每帧的特征（音频频段、视频亮度/边缘信息、运动矢量）  
3. **SCENE_FN** — 通过场景函数将内容渲染到像素画布上（格式为`uint8 H,W,3`）。可通过`_render_vf()`函数结合像素混合模式来组合多个字符网格。详情请参阅`references/composition.md`  
4. **TONEMAP** — 基于分位数的自适应亮度标准化处理。相关内容可见`references/composition.md`中的“自适应色调映射”章节  
5. **SHADE** — 通过`ShaderChain`与`FeedbackBuffer`实现后期处理效果。更多信息请参阅`references/shaders.md`  
6. **ENCODE** — 将原始的RGB帧传递给ffmpeg，以实现H.264或GIF格式的编码  

## 创意方向

### 审美维度

| 维度 | 选项 | 参考文档 |
|------|------|----------|
| **字符调色板** | 密度渐变、块状元素、符号、文字字体（片假名、希腊文、如尼文、盲文）、项目专用调色板 | `architecture.md` § 调色板 |
| **颜色策略** | HSV色彩模型、OKLAB/OKLCH色彩模型、离散RGB调色板、自动生成的和谐配色、单色模式、色调参数 | `architecture.md` § 颜色系统 |
| **背景纹理** | 正弦场、fBM噪声、域变形、沃罗诺伊图、反应-扩散模型、元胞自动机、视频素材 | `effects.md` |
| **主要特效** | 环形效果、螺旋效果、隧道效果、漩涡效果、波浪效果、干涉效果、极光效果、火焰效果、SDF函数生成的图案、奇异吸引子效果 | `effects.md` |
| **粒子效果** | 火花、雪花、雨滴、气泡、如尼文符号、轨道运动、群集行为粒子、流场跟随粒子、轨迹效果 | `effects.md` § 粒子效果 |
| **着色器风格** | 复古CRT风格、简洁现代风格、故障艺术风格、电影感风格、梦幻风格、工业风格、迷幻风格 | `shaders.md` |
| **网格密度** | 从xs（8px）到xxl（40px），各图层可独立设置 | `architecture.md` § 网格系统 |
| **坐标空间** | 笛卡尔坐标系、极坐标系、平铺坐标系、旋转坐标系、鱼眼坐标系、莫比乌斯坐标系、域变形坐标系 | `effects.md` § 变换效果 |
| **反馈效果** | 缩放隧道效果、彩虹轨迹效果、幽灵回声效果、旋转曼荼罗效果、颜色演变效果 | `composition.md` § 反馈效果 |
| **遮罩效果** | 圆形遮罩、环形遮罩、渐变遮罩、文本模板遮罩、动态缩放/擦除/溶解遮罩 | `composition.md` § 遮罩效果 |
| **过渡效果** | 渐变切换、擦除过渡、溶解过渡、故障切割过渡、缩放显示过渡、基于遮罩的显示过渡 | `shaders.md` § 过渡效果 |

### 各章节自定义选项

切勿为整个视频使用相同的配置。针对每个片段/场景，应做到：
- **不同的背景效果**（或组合2-3种效果）
- **不同的角色色彩方案**（需与整体氛围相契合）
- **不同的色彩策略**（至少色调要有所区别）
- **调整着色器强度**（在高潮部分增强光晕效果，在安静场景中增加颗粒感）
- 若使用粒子效果，则需采用**不同的粒子类型**

### 为项目量身定制创意

针对每个项目，至少设计以下一项创新内容：
- 与主题相匹配的定制角色色彩方案
- 自定义背景效果（通过组合或修改现有元素实现）
- 定制色彩调色板（选用与品牌或氛围相协调的独立RGB颜色组合）
- 自定义粒子类型集
- 独特的场景过渡方式或视觉亮点

不要仅仅从现有资源库中挑选内容。资源库只是词汇表——而你需要创作属于自己的诗篇。

## 工作流程

### 第一步：明确创意构想

在编写任何代码之前，先清晰阐述创意核心要素：
- **氛围/情绪**：希望观众感受到什么？充满活力、宁静沉思、混乱无序、优雅精致，还是阴森恐怖？
- **视觉叙事**：整个视频中会发生什么？逐步营造紧张感？实现形态转变？还是逐渐消散？
- **色彩风格**：偏向暖色调还是冷色调？单色系？霓虹色？大地色系？哪种颜色是主导色？
- **元素质感**：密集的数据点？稀疏的星星？有机形状的点状物？几何图形块？
- **独特之处**：究竟是什么让这个项目与众不同？
- **情感脉络**：各个场景如何层层递进？以活力开场，逐步推向高潮，最终达成圆满结局？
将用户的提示映射为特定的视觉风格。“轻松的低保真可视化效果”与“故障风格的赛博朋克数据流”对各项参数的要求截然不同。

### 第2步：技术设计

- **模式** — 以上6种模式中的其中一种
- **分辨率** — 横屏1920x1080（默认），竖屏1080x1920，正方形1080x1080，帧率为24fps
- **硬件检测** — 自动检测核心数/内存容量，并设定相应的质量配置。详情请参阅 `references/optimization.md`
- **场景分段** — 将时间戳与不同场景功能对应起来，每个场景均可独立设置特效、调色板、颜色及着色器参数
- **输出格式** — MP4（默认），GIF（640x360，帧率为15fps），PNG序列

### 第3步：编写脚本

仅需一个Python文件。各组成部分及参考资料如下：

1. **硬件检测与质量配置** — `references/optimization.md`  
2. **输入加载器** — 视模式而定；参见 `references/inputs.md`  
3. **特征分析器** — 支持音频 FFT、视频亮度分析或合成数据解析  
4. **网格系统与渲染器** — 基于多密度网格并配备位图缓存；详见 `references/architecture.md`  
5. **字符调色板** — 每个项目可配置多个调色板；参见 `references/architecture.md` § 调色板  
6. **颜色系统** — 包含 HSV 颜色模型、离散 RGB 颜色空间以及色彩协调性生成机制；详见 `references/architecture.md` § 颜色  
7. **场景函数** — 每个函数均返回格式为 `canvas (uint8 H,W,3)` 的图像数据；参见 `references/scenes.md`  
8. **色调映射** — 用于实现自适应亮度标准化处理；参见 `references/composition.md`  
9. **着色器管线** — 由 `ShaderChain` 和 `FeedbackBuffer` 共同构成；详见 `references/shaders.md`  
10. **场景表与调度器** — 根据时间顺序关联对应的场景函数及配置参数；参见 `references/scenes.md`  
11. **并行编码器** — 利用 ffmpeg 流处理技术实现多工作线程下的片段渲染  
12. **主程序** — 负责协调整个处理流程的运行  

### 第 4 步：质量验证

- **先测试单帧图像**：在完整渲染之前，先在关键时间点渲染单个帧进行测试  
- **亮度检查**：所有 ASCII 内容的 `canvas.mean()` 值应大于 8；若画面过暗，则需降低伽马值  
- **视觉一致性检查**：所有场景是否呈现出属于同一视频的连贯感？  
- **创意理念匹配度检查**：输出结果是否符合第 1 步设定的创意概念？若效果过于普通，需重新调整设计思路  

## 关键实现注意事项

### 亮度处理 — 应使用 `tonemap()` 函数，而非线性乘法方式

这是最突出的视觉问题。黑色背景上的ASCII字符本身就显得很暗。**绝不要使用 `canvas * N` 这种缩放方式**——它会导致高光部分被截断。应采用自适应色调映射技术：

```python
def tonemap(canvas, gamma=0.75):
    f = canvas.astype(np.float32)
    lo, hi = np.percentile(f[::4, ::4], [1, 99.5])
    if hi - lo < 10: hi = lo + 10
    f = np.clip((f - lo) / (hi - lo), 0, 1) ** gamma
    return (f * 255).astype(np.uint8)
```

处理流程：`scene_fn() → tonemap() → FeedbackBuffer → ShaderChain → ffmpeg`

不同场景的伽马值设置：默认为 0.75，日光效果为 0.55，海报化效果为 0.50，明亮场景则为 0.85。对于暗色图层，请使用 `screen` 混合模式（而非 `overlay`）。

### 字体单元高度

在 macOS 环境下使用 Pillow 时，`textbbox()` 函数返回的高度值可能不准确。建议使用 `font.getmetrics()` 方法：`cell_height = ascent + descent`。更多详情请参阅 `references/troubleshooting.md`。

### ffmpeg 流处理死锁问题

在运行时间较长的 ffmpeg 进程中，切勿使用 `stderr=subprocess.PIPE` —— 因为缓冲区在达到 64KB 时就会导致死锁。应将错误输出重定向到文件中。相关解决方案请参见 `references/troubleshooting.md`。

### 字体兼容性

并非所有 Unicode 字符都能在所有字体中正常显示。建议在初始化阶段验证字体调色板，逐一渲染每个字符并检查是否有空白输出。更多详情请参阅 `references/troubleshooting.md`。

### 单个片段的处理架构

对于由多个片段组成的视频（如引言、场景、章节等），建议将每个片段单独作为一份剪辑文件进行处理，从而实现并行渲染和有选择性的重新渲染。相关说明请参见 `references/scenes.md`。

## 性能目标

| 组件 | 时间预算 |
|-----------|----------|
| 特征提取 | 1-5毫秒 |
| 效果处理函数 | 2-15毫秒 |
| 字符渲染 | 80-150毫秒（性能瓶颈） |
| 着色器处理流程 | 5-25毫秒 |
| **总耗时** | 约 100-200毫秒/帧 |

## 参考资料

| File | Contents |
|------|----------|
| `references/architecture.md` | Grid system, resolution presets, font selection, character palettes (20+), color system (HSV + OKLAB + discrete RGB + harmony generation), `_render_vf()` helper, GridLayer class |
| `references/composition.md` | Pixel blend modes (20 modes), `blend_canvas()`, multi-grid composition, adaptive `tonemap()`, `FeedbackBuffer`, `PixelBlendStack`, masking/stencil system |
| `references/effects.md` | Effect building blocks: value field generators, hue fields, noise/fBM/domain warp, voronoi, reaction-diffusion, cellular automata, SDFs, strange attractors, particle systems, coordinate transforms, temporal coherence |
| `references/shaders.md` | `ShaderChain`, `_apply_shader_step()` dispatch, 38 shader catalog, audio-reactive scaling, transitions, tint presets, output format encoding, terminal rendering |
| `references/scenes.md` | Scene protocol, `Renderer` class, `SCENES` table, `render_clip()`, beat-synced cutting, parallel rendering, design patterns (layer hierarchy, directional arcs, visual metaphors, compositional techniques), complete scene examples at every complexity level, scene design checklist |
| `references/inputs.md` | Audio analysis (FFT, bands, beats), video sampling, image conversion, text/lyrics, TTS integration (ElevenLabs, voice assignment, audio mixing) |
| `references/optimization.md` | Hardware detection, quality profiles, vectorized patterns, parallel rendering, memory management, performance budgets |
| `references/troubleshooting.md` | NumPy broadcasting traps, blend mode pitfalls, multiprocessing/pickling, brightness diagnostics, ffmpeg issues, font problems, common mistakes |

## 创意发散模式（仅当用户要求生成实验性、创意性或独特的输出时使用）

若用户希望获得具有创意、实验性、惊喜感或非传统风格的输出，请在编写代码之前选择最合适的策略，并详细规划其执行步骤。

- **强制关联法**——适用于用户需要跨领域灵感的情况（如“让整体看起来更自然”、“工业风风格”）
- **概念融合法**——适用于用户指定两种元素进行结合的情况（如“海洋与音乐的融合”、“太空与书法的结合”）
- **迂回策略法**——适用于用户完全开放接受新奇想法的情况（如“给我一个惊喜”、“我从未见过的东西”）

### 强制关联法
1. 选择与目标视觉效果无关的领域（如天气系统、微生物学、建筑学、流体力学、纺织编织）
2. 列出该领域的核心视觉/结构元素（如侵蚀作用→逐渐显现；有丝分裂→分裂复制；编织工艺→交错图案）
3. 将这些元素映射为ASCII字符和动画效果
4. 综合生成——在字符网格中，“侵蚀”或“结晶”会呈现为何种形态？

### 概念融合法
1. 指定两个不同的视觉/概念领域（例如海浪与乐谱）
2. 建立对应关系（波峰=高音符，波谷=休止符，泡沫=断奏）
3. 有选择地融合——保留最有趣的对应关系，舍弃强行关联的部分
4. 挖掘仅在融合状态下才出现的独特特性

### 迂回策略法
1. 想象一个方法：“将错误视为一种隐含的意图” / “运用旧有的思路” / “你的挚友会怎么做？” / “着重强调缺陷” / “将事物颠倒过来” / “只看局部，而非整体” / “反向操作”  
2. 结合当前的 ASCII 动画挑战来解读该指令。  
3. 在编写代码之前，先将这种跳脱常规的思维方式应用到视觉设计中。
