---
name: hyperframes
description: Render MP4/WebM videos from HTML compositions.
version: 1.0.0
author: heygen-com
license: Apache-2.0
platforms: [linux, macos, windows]
prerequisites:
  commands: [node, ffmpeg, npx]
metadata:
  hermes:
    tags: [creative, video, animation, html, gsap, motion-graphics]
    related_skills: [manim-video, meme-generation]
    category: creative
    requires_toolsets: [terminal]
---

# HyperFrames

HTML 是视频内容的真实来源。一个合成内容由一个包含用于控制时序的 `data-*` 属性的 HTML 文件、用于实现动画的 GSAP 时间轴，以及用于控制外观的 CSS 组成。HyperFrames 引擎会逐帧捕获页面内容，并使用 FFmpeg 将其编码为 MP4/WebM 格式。

**与 `manim-video` 的区别：** 对于数学或几何演示内容（如方程、3B1B 风格的图表），请使用 `manim-video`；而对于动态图形、带字幕的出镜讲解、产品展示、社交媒体贴片、着色器过渡效果，以及任何基于真实视频/音频素材的内容，则应使用 `hyperframes`。

## 适用场景

- 用户希望从文本、脚本或网站生成渲染后的视频
- 动态标题卡、底部信息栏或排版式开场动画
- 带字幕的旁白视频（文本转语音与字幕同步至波形）
- 随音频变化的视觉效果（节奏同步、频谱条、脉冲光效）
- 场景间的过渡效果（渐变淡入、擦除、着色器变形、白色闪过）
- 社交媒体风格贴片（Instagram/TikTok/YouTube 风格）
- 网站到视频的转换流程（捕获网址并生成宣传视频）
- 任何需要以确定性方式渲染为视频文件的 HTML/CSS/JS 动画

**不推荐用于以下场景：**
- 纯数学或方程动画（→ 使用 `manim-video`）
- 图像生成或表情包制作（→ 使用 `meme-generation` 或图像模型）
- 实时视频会议或流媒体传输

## 快速参考

```bash
npx hyperframes init my-video               # scaffold a project
cd my-video
npx hyperframes lint                        # validate before preview/render
npx hyperframes preview                     # live-reload preview (long-lived server, port 3002)
npx hyperframes render --output final.mp4   # render to MP4
npx hyperframes doctor                      # diagnose environment issues
```

`preview` 是一个**长期运行**的 Next.js 服务器，用于保持 Chrome 渲染工作进程处于激活状态。使用完毕后务必将其停止（详见[清理指南](#cleanup)）——若忘记关闭 `preview`，那些闲置的 `chrome-headless-shell` 工作进程仍会继续运行。在无 GPU 的主机环境（如 WSL、容器及 CI 环境）中，这些进程会通过软件 WebGL（swiftshader）持续占用每个 CPU 核心资源。

渲染参数：`--quality draft|standard|high` · `--fps 24|30|60` · `--format mp4|webm` · `--docker`（确保结果可复现）· `--strict`。

完整的 CLI 参考文档：[references/cli.md](references/cli.md)。

## 设置（仅需执行一次）

```bash
bash "$(dirname "$(find ~/.hermes/skills -path '*/hyperframes/SKILL.md' 2>/dev/null | head -1)")/scripts/setup.sh"
```

该脚本的功能如下：
1. 检查系统是否已安装 Node.js 22 及以上版本以及 FFmpeg（如未安装则会输出修复指南）。
2. 全局安装 `hyperframes` CLI（命令为 `npm install -g hyperframes@>=0.4.2`）。
3. 通过 Puppeteer 预缓存 `chrome-headless-shell` —— 这是通过 Chrome 的 `HeadlessExperimental.beginFrame` 捕获方式实现最佳渲染效果所必需的步骤。
4. 运行 `npx hyperframes doctor` 命令并输出检测结果。

如果设置过程中出现故障，请参阅 [references/troubleshooting.md](references/troubleshooting.md) 文档。

## 执行步骤

### 1. 编写 HTML 之前的规划

在动手编写代码之前，需先从宏观层面明确以下内容：
- **内容框架** —— 故事情节、关键节点、情感节奏
- **结构设计** —— 分镜布局、轨道类型（视频/音频/叠加层）及时长
- **视觉风格** —— 颜色方案、字体选择以及整体动效风格（夸张/电影感/流畅/科技风）
- **核心画面** —— 对于每个场景而言，指所有元素同时最清晰可见的那一帧。这正是你需要首先设计的静态布局。

**视觉风格确认机制（强制要求）。** 在编写任何分镜的 HTML 代码之前，必须先确定视觉风格。切勿使用默认或通用的颜色值来创建分镜（如使用 `#333`、`#3b82f6` 或 Roboto 字体，均表明此步骤已被跳过）。请按以下顺序进行确认：

1. **项目根目录下存在 `DESIGN.md` 文件？** → 直接沿用该文件中规定的颜色、字体、动画规则以及“禁忌事项”要求。
2. **用户已指定风格名称**（例如“Swiss Pulse”、“深色科技风”、“奢侈品牌风”）？→ 生成一份简洁的 `DESIGN.md` 文件，内容包括 `## Style Prompt`、`## Colors`（3-5种带用途说明的十六进制颜色值）、`## Typography`（1-2种字体系列）以及 `## What NOT to Do`（3-5项应避免的设计误区）。
3. **以上情况均不符合？** → 在生成任何 HTML 内容之前，先询问用户三个问题：
   - 氛围风格？（充满活力 / 电影感 / 流畅自然 / 科技感 / 混乱无序 / 温暖舒适）
   - 背景采用浅色还是深色？
   - 是否有指定的品牌颜色、字体或视觉参考？

   根据用户的回答后再生成 `DESIGN.md` 文件。所有设计元素的颜色方案与字体选择都必须有明确的来源，要么来自 `DESIGN.md`，要么遵循用户的具体指示。

### 2. 框架搭建

```bash
npx hyperframes init my-video --non-interactive
```

模板选项包括：`blank`、`warm-grain`、`play-mode`、`swiss-grid`、`vignelli`、`decision-tree`、`kinetic-type`、`product-promo`、`nyt-graph`。若需选择特定模板，可输入 `--example <名称>`；若要为动画添加媒体素材，则可使用 `--video clip.mp4` 或 `--audio track.mp3`。

### 3. 动画前的布局设计

首先编写**标题页框架**的静态 HTML+CSS 代码——此时暂无需使用 GSAP。`.scene-content` 容器需通过 `display:flex` + `gap` 属性将整个场景填满（`width:100%; height:100%; padding:Npx`）。应利用内边距将内容向内挤压，切勿在内容容器上使用 `position: absolute; top: Npx` 的方式定位（否则当内容高度超过剩余空间时会导致内容溢出）。

只有在标题页框架的样式确定无误后，才能添加 `gsap.from()` 动画实现内容进入效果（动画效果为**移动到**CSS定义的位置），以及使用 `gsap.to()` 动画实现内容离开效果（动画效果为**从**该位置移动出去）。

有关完整的数据属性结构及布局规则，请参阅 [references/composition.md](references/composition.md) 文档。

### 4. 使用 GSAP 进行动画制作

每个动画组合都必须满足以下要求：
- 注册对应的时间轴：`window.__timelines["<composition-id>"] = tl`
- 初始化时处于暂停状态：`gsap.timeline({ paused: true })`——播放控制权由播放器掌握
- 设置有限的重复次数（禁止使用 `repeat: -1`，否则会干扰捕获引擎的正常运行）。重复次数的计算公式为：`repeat: Math.ceil(duration / cycleDuration) - 1`。
- 确保动画结果可预测——不得使用 `Math.random()`、`Date.now()` 或基于实际时间的逻辑。如需模拟随机效果，可使用带种子值的伪随机数生成器。
- 动画构建过程需同步进行——在创建时间轴时不可使用 `async`/`await`、`setTimeout` 或 Promise 机制。
核心的 GSAP API（包括动画过渡、缓动函数、错开动画效果以及时间轴功能）的相关信息，请参阅 [references/gsap.md](references/gsap.md)。

### 5. 场景之间的切换

多场景组合必然需要使用切换效果。相关规则如下：
1. **场景之间必须始终使用切换效果**——禁止直接跳转。
2. **每个场景元素都必须添加进入动画**（使用 `gsap.from(...)`）。
3. **除最后一个场景外，严禁使用离开动画**——因为切换过程本身即视为离开动画。
4. 最后一个场景可以选择渐隐消失。

如需安装各种着色器切换效果（如 `flash-through-white`、`liquid-wipe` 等），可运行命令 `npx hyperframes add <transition-name>`。完整的切换效果列表可通过 `npx hyperframes add --list` 查看。

### 6. 音频、字幕、文本转语音、音频响应式效果及高亮显示

- **音频**：必须使用独立的 `<audio>` 元素处理（视频则需设置为 `muted playsinline` 属性）。
- **文本转语音**：可使用命令 `npx hyperframes tts "脚本文本" --voice af_nova --output narration.wav` 进行转换。如需查看可用的语音列表，可运行 `--list`。语音标识的首字母代表了对应语言（`a`/`b` 表示英语，`e` 表示西班牙语，`f` 表示法语，`j` 表示日语，`z` 表示普通话等）——命令行工具会自动检测语音合成器的区域设置，如需手动指定则可使用 `--lang` 参数。若需处理非英语语言的文本转语音功能，系统上需预先安装 `espeak-ng` 工具。
- **字幕生成：** 使用命令 `npx hyperframes transcribe narration.wav` 即可获得单词级的文字转录结果。可根据转录内容的风格选择相应的字体风格（如激情型、商务型、教程型、叙事型或社交型——详情请参阅 `references/features.md` 中的表格）。**语言规则：** 除非确认音频为英语，否则绝不可使用 `.en` 后缀的耳语风格模型——这类模型会试图翻译非英语音频而非进行转录。每个字幕组在动画过渡结束后，都必须通过代码 `tl.set(el, { opacity: 0, visibility: "hidden" }, group.end)` 显式将其隐藏，否则这些字幕组的内容将会泄露并显示在后续的字幕组中。

- **音频驱动的视觉效果：** 需先提取音频中的不同频段（低音、中音、高音），然后通过 `tl.call(draw, [], f / fps)` 结合 `for` 循环在时间轴上逐帧生成视觉效果——单一的长时间过渡动画无法对音频做出响应。可将低音映射为 `scale` 动画以实现脉冲效果，高音映射为 `textShadow`/`boxShadow` 动画以营造发光效果，而整体音量则可映射为 `opacity`、`y` 值或 `backgroundColor`。应避免使用千篇一律的均衡器条式视觉效果，而要让内容主导视觉呈现，让音频驱动其动态变化。

- **标记式高亮效果：** 用于强调文本的高亮、圆形标注、爆裂效果、涂鸦效果及草图风格效果均基于确定的 CSS+GSAP 技术实现——详情请参阅 `references/features.md#marker-highlighting`。此类效果支持完全搜索功能，且不使用带动画效果的 SVG 过滤器。
- **场景切换：** 所有多场景合成内容都必须使用切换效果（禁止直接跳转）。可从CSS基础切换效果中选择（如推入式滑动、模糊渐变、缩放过渡、错位分块），或通过 `npx hyperframes add` 命令引入着色器切换效果（如“白色闪光过渡”、“液体擦除效果”、“交叉变形”、“色彩分离”等）。相关效果风格与参数说明请参阅 `references/features.md#transitions` 文件。同一合成内容中不得同时使用CSS切换效果和着色器切换效果。

### 7. 代码检查、验证、检测、预览与渲染

```bash
npx hyperframes lint              # catches missing data-composition-id, overlapping tracks, unregistered timelines
npx hyperframes validate          # WCAG contrast audit at 5 timestamps
npx hyperframes inspect           # visual layout audit — overflow, off-frame elements, occluded text
npx hyperframes preview           # live browser preview
npx hyperframes render --quality draft --output draft.mp4    # fast iteration
npx hyperframes render --quality high --output final.mp4     # final delivery
```

`hyperframes validate` 会采样每个文本元素背后的背景像素，并对对比度低于 4.5:1（大字体则为 3:1）的情况发出警告。`hyperframes inspect` 则是用于布局检查的工具——它会在不同时间点加载页面，从而检测出静态检查工具无法发现的缺陷（例如在 4.5 秒时标题才超出安全区域、当标题为最长版本时卡片内容溢出、某个元素被过渡效果遮盖等）。尤其建议对包含对话框、卡片、字幕或密集排版的页面使用 `inspect` 工具进行检测。

### 8. 网站转视频（如用户提供网址）

请按照 [references/website-to-video.md](references/website-to-video.md) 中的七步流程将网页转换为视频：捕获 → DESIGN.md → SCRIPT.md → 分镜脚本 → 组合页面 → 渲染 → 输出。

## 清理工作

`render` 是一次性操作（完成后工作进程会立即退出）。而 `preview` 则并非如此——它会持续运行一个后台的 Next.js 服务器，使 Chrome 工作进程保持活跃状态，直到你手动停止它。绝不能让预览进程一直运行：在无 GPU 的服务器上，每个闲置的工作进程都会占用一个 CPU 核心，若预览窗口长时间打开，就会累积多个占用核心的进程。

当用户完成查看后（或在开始新的预览之前），请及时停止预览进程：

```bash
pkill -f "hyperframes.*preview"     # the Studio server (frees port 3002)
pkill -f chrome-headless-shell      # its render workers; only safe if nothing else uses them
```

如果不确定其他工具是否使用了 `chrome-headless-shell`，可先执行以下命令进行检查：`pgrep -af chrome-headless-shell`。处理因进程卡住而导致大量空闲工作进程占用 CPU 的情况时，也可采用相同方法——详情请参阅 [references/troubleshooting.md](references/troubleshooting.md#runaway-cpu-from-leftover-preview-workers)。

## 常见问题

- **未停止 `preview` 服务**——该服务会长期运行并维持 Chrome 工作进程；在 WSL、容器或 CI 环境中，这些空闲工作进程会各自占用一个 CPU 核心（用于运行软件级 WebGL）。任务完成后务必停止该服务——详情请参阅 [Cleanup](#cleanup) 部分。

- **出现 “`HeadlessExperimental.beginFrame' wasn't found” 错误**——Chromium 147 及更高版本已移除此协议。请确保使用的是 `hyperframes@>=0.4.2` 版本（该版本会自动检测并回退到截图模式）。作为临时解决方案，可设置 `export PRODUCER_FORCE_SCREENSHOT=true`。更多详情请参阅 [hyperframes#294](https://github.com/heygen-com/hyperframes/issues/294) 以及 [references/troubleshooting.md](references/troubleshooting.md)。

- **使用系统自带的 Chrome（而非 `chrome-headless-shell`）**——会导致渲染过程卡住约 120 秒后超时。请运行 `npx puppeteer browsers install chrome-headless-shell`（setup.sh 脚本已包含此操作）。`hyperframes doctor` 命令可显示将使用的二进制文件。

- **任何地方出现 `repeat: -1` 参数**——都会导致捕获引擎失效。务必设置一个有限的重复次数。

- **对在页面加载后才出现的剪辑元素使用 `gsap.set()`**——此时该元素尚不存在。应在时间轴上、且在该剪辑的 `data-start` 属性指定的时间点或之后，使用 `tl.set(selector, vars, timePosition)` 方法进行操作。
- **内容文本中的 `<br>`** — 强制换行无法考虑渲染后的字体宽度，因此应采用自然换行后再使用 `<br>` 进行二次换行。建议使用 `max-width` 属性来实现文本换行。例外情况：那些刻意将每个单词单独占一行的简短显示标题。
- **动画化 `visibility` 或 `display` 属性** — GSAP 无法对这些属性进行过渡动画处理。应使用 `autoAlpha` 属性（可同时控制可见性和透明度）。
- **调用 `video.play()` 或 `audio.play()` 方法** — 播放功能由框架统一管理，切勿自行调用这些方法。
- **异步构建时间轴** — 页面加载后，捕获引擎会同步读取 `window.__timelines` 数据。因此绝不能将时间轴的构建过程封装在 `async`、`setTimeout` 或 Promise 中。
- **被 `<template>` 包裹的独立 `index.html` 文件** — 该文件会隐藏浏览器中的所有内容。只有通过 `data-composition-src` 加载的**子组合**才会使用 `<template>` 标签。
- **用视频替代音频** — 应始终使用已静音的 `<video>` 元素，并搭配独立的 `<audio>` 元素。

## 验证流程

在渲染前后需执行以下检查：

1. **代码检查、验证与布局检测通过**：运行 `npx hyperframes lint --strict && npx hyperframes validate && npx hyperframes inspect`（代码检查可发现结构问题，验证功能可检测对比度问题，布局检测则能发现视觉排版或溢出问题——如出现警告，请参阅 troubleshooting.md 文档）。
2. **动画协调性检查** — 对于新创建的组合或进行了重大动画修改的情况，需运行动画映射工具。执行 `npx hyperframes init` 可将相关技能脚本复制到项目中，此时路径为项目本地路径。
   ```bash
   node skills/hyperframes/scripts/animation-map.mjs <composition-dir> \
     --out <composition-dir>/.hyperframes/anim-map
   ```
该工具会输出一个包含多项信息的 `animation-map.json` 文件，其中包括每个过渡动画的摘要、ASCII格式的甘特图时间线、元素错开检测结果、无动画区域信息（持续时间超过1秒的区域）、元素生命周期数据，以及各类状态标记（如 `offscreen`、`collision`、`invisible`、`paced-fast` <0.2秒、`paced-slow` >2秒）。请仔细查看这些摘要与标记，针对每一项问题进行修正或给出合理解释；若只是细微调整，则可直接跳过。

3. **文件存在且大小非零：** 执行命令 `ls -lh final.mp4`。
4. **视频时长与 `data-duration` 匹配：** 执行命令 `ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 final.mp4`。
5. **视觉检查：** 提取中间帧进行查看，命令为 `ffmpeg -i final.mp4 -ss 00:00:05 -vframes 1 preview.png`。
6. **确认是否存在音频（如预期中应有音频）：** 执行命令 `ffprobe -v error -show_streams -select_streams a -of default=nw=1:nk=1 final.mp4 | head -1`。

如果 `hyperframes render` 命令执行失败，请运行 `npx hyperframes doctor` 并在提交问题报告时附上该命令的输出结果。

## 参考资料

- [composition.md](references/composition.md) — 数据属性、时间轴规范、不可违背的规则以及排版与资源相关规则  
- [cli.md](references/cli.md) — 所有 CLI 命令（init、capture、lint、validate、inspect、preview、render、transcribe、tts、doctor、browser、info、upgrade、benchmark）  
- [gsap.md](references/gsap.md) — 用于 HyperFrames 的 GSAP 核心 API（动画过渡、缓动函数、错开播放、时间轴控制及 matchMedia 功能）  
- [features.md](references/features.md) — 字幕功能、文本转语音、音频响应式处理、标记高亮显示以及过渡效果（按需加载）  
- [website-to-video.md](references/website-to-video.md) — 七步式的网站转视频处理流程  
- [troubleshooting.md](references/troubleshooting.md) — OpenClaw 相关解决方案、环境变量设置以及常见的渲染错误处理方法
