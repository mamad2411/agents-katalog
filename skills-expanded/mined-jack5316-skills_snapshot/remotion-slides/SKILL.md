---
name: remotion-slides
description: |
  将主题/论文/内容转化为 Reveal.js HTML 演示文稿。
  继承 remotion-video 的内容规划方法论（认知阶梯、场景设计），输出文件夹式 HTML 幻灯片（index.html + images/ + dist/）。
  用户自己上台讲，不需要配音和视频渲染。
  触发词：
  - "做演示文稿"、"Reveal.js 演示"、"HTML 幻灯片"
  - "做幻灯片"、"生成演示"、"演讲幻灯片"
  - "把文章做成幻灯片"、"文章转演示"、"article to slides"
  - "/remotion-slides"
  适用场景：
  - 学术报告演示（论文讲解、开题答辩、毕业答辩）
  - 技术分享演示（架构讲解、方案汇报）
  - 教学课件（概念讲解、公式推导）
  - 会议演示（项目汇报、方案对比）
  - 文章转演示（用户提供 Markdown 文章，保留原有结构和素材）
allowed-tools: Read Write Edit Bash Task Glob Grep WebSearch WebFetch
metadata:
  author: wsy
  version: "2.2.0"
  domain: presentation
---

# Remotion Slides

将主题/论文/内容转化为 **Reveal.js HTML 演示文稿**。输出完整演示文件夹（index.html + 本地图片 + Reveal.js 离线副本），浏览器打开 index.html 即用，zip 打包分发。

## 与相关 Skill 的关系

| Skill | 输入 | 输出 | 动画机制 |
|-------|------|------|----------|
| `remotion-video` | 主题/论文/内容 | MP4 视频 | React 帧动画 |
| `remotion-excalidraw-video` | 同上 | MP4（手绘风） | rough.js + evolvePath |
| `markdown-to-slides` | Markdown 文档 | Markdown 幻灯片（中间格式） | 无动画 |
| **`remotion-slides`（本 skill）** | 主题/论文/内容 | **Reveal.js HTML** | fragments + auto-animate + 增强动画（3b1b/回形针/手绘） |

**与 markdown-to-slides 不同**：
- markdown-to-slides 输出中间 Markdown，需要另一个工具渲染
- remotion-slides 输出**最终 HTML**，打开即用，动画效果内置
- remotion-slides 继承 remotion-video 的内容规划方法论（认知阶梯、场景设计）

## 继承关系

本 skill **继承** remotion-video 的以下方法论（不继承技术栈）：

| 模块 | 来源 | 适用模式 | 说明 |
|------|------|---------|------|
| 认知阶梯 | remotion-video Phase 0 | 标准模式 | L1 故事→L2 概念→L3 细节→L4 数学 |
| 场景设计 | remotion-video Phase 1 | 标准模式 + 文章模式 | 信息密度控制、内容分段 |
| 学术定位 | remotion-video Phase 0 | 标准模式（论文类） | 论文类输入的根基/遗产/竞争分析 |

**不继承**：Remotion 框架、音频系统、渲染管线、项目结构。

> **文章模式说明**：文章模式跳过认知阶梯和学术定位，使用文章自身的叙事结构。场景设计中的信息密度控制仍然适用。

---

## 技术选型

| 决策 | 方案 | 原因 |
|------|------|------|
| 输出格式 | 文件夹（HTML + images/ + dist/） | 离线可用，zip 打包分发 |
| 幻灯片框架 | Reveal.js 5.2.1 本地 dist/ | 离线可用，功能完备 |
| 动画层 | fragments + auto-animate + transitions + 增强动画 | 基础三级 + 3b1b/回形针/手绘增强风格 |
| 图表方案 | 内联 SVG + fragment 分步 | 支持逐步揭示，矢量清晰 |
| 代码高亮 | highlight.js（Reveal 内置插件） | 支持逐行步进 |
| 数学公式 | KaTeX（Reveal 内置插件） | 自动从 CDN 加载 |
| 演讲者备注 | `<aside class="notes">` | 替代视频版的语音旁白 |

### 图片处理策略

所有图片统一保存到 `images/` 目录，HTML 中使用相对路径引用。

| 优先级 | 方式 | 适用场景 | 存储 |
|--------|------|----------|------|
| 1 | 内联 SVG | 图表、流程图、架构图（支持 fragment 动画） | 直接内联于 HTML |
| 2 | **Gemini AI 生成配图** | 概念隐喻、场景类比、抽象可视化（需 API key） | `images/gemini-NN.jpg` |
| 3 | 外部图片文件 | 照片、截图、论文首页 | `images/<name>.jpg` |
| 4 | **Pexels 配图** | 写实照片背景、封面装饰 | `images/pexels-<id>.jpg` |

> 不再使用 base64 编码。所有非 SVG 图片存放在 images/ 目录，相对路径引用。

> **图片获取与嵌入详情**：见 `references/image-sources.md`。包含 Pexels API 调用与下载、Gemini AI 生成流程与提示词约束、论文首页滚动动画的完整实现。Phase 0 标注配图意图和 Phase 2 嵌入图片时加载。

---

## 单页聚焦原则（最高优先级，v1.7 新增）

**核心理念**：每张幻灯片只聚焦一件事。不怕页数多，怕的是单页信息过密。

观众每次看到新页面，注意力自然聚焦。一页放太多东西，注意力分散，什么都记不住。宁可多翻几页，也不要把多个概念塞进一页。同时也避免因单页内容过多导致溢出、排版错乱等技术问题。

### 主要内容 vs 辅助元素

| 类别 | 定义 | 示例 |
|------|------|------|
| **主要内容**（每页限 1 种） | 承载核心信息的内容块 | 列表、SVG 图表、引用块、大数字、AI 配图、代码块、公式推导 |
| **辅助元素**（不受限） | 标注性、装饰性的附属信息 | 短标题、1-2 句说明文字、来源标注、趋势 badge、装饰性背景图（opacity≤0.25） |

### 内容类型互斥规则

每张幻灯片只能有 **一种主要内容**（标题和辅助元素除外）：

| 主要内容 | 可搭配的辅助元素 | ❌ 不可同时出现的主要内容 |
|----------|-----------------|------------------------|
| 列表（≤3 条） | 短标题 + 1 行说明 | 图表、引用、大段文字、配图 |
| SVG 图表 | 短标题 + 1 行说明 | 列表、引用、大段文字 |
| 引用块 | 短标题 + 1 行评论 | 列表、图表、大段文字 |
| 大数字（data-impact） | 短标题 + 趋势 badge + 来源 | 列表、图表、引用 |
| AI 配图（Gemini） | 短标题 + 1-2 句说明 | 列表、图表、引用 |
| 代码块 | 短标题 | 列表、图表、引用 |
| 公式推导 | 短标题 + 结论公式 | 列表、大段文字 |

### 豁免清单

以下幻灯片不受单页聚焦约束：

| 豁免类型 | 说明 |
|----------|------|
| 论文展示页（Paper-01/02/End） | 设计目标是展示论文元数据，auto-animate 过渡是核心功能 |
| 对比模式（comparison） | 对比本身是一个认知单元；但对比 + 独立 SVG = 两个焦点，需拆分 |
| 装饰性背景图 | `data-background-opacity` ≤ 0.25 的 Pexels 背景不算主要内容 |

### 拆分优于压缩

当一张幻灯片内容超出「一件事」时，**必须拆分为多张**。禁止以下「压缩」手段：

| ❌ 禁止 | ✅ 应该 |
|---------|---------|
| 缩小字体以塞下更多内容 | 拆分为 2 张幻灯片 |
| 减少行间距 / 边距 | 每页保持舒适留白 |
| 去掉动画以节省空间 | 保持动画，让内容逐步呈现 |
| 删减内容以适应单页 | 保持内容完整，分布到多页 |

**示例**：

| 原始规划 | ❌ 压缩做法 | ✅ 拆分做法 |
|----------|-----------|-----------|
| 3 个风险 + 2 个建议 | 全部塞进 1 页 | 风险 1 页 + 建议 1 页 |
| Big Five 对比 + 16P 结果 | 全部塞进 1 页 | Big Five 1 页 + 16P 1 页 |
| 4 个论据 | 全部塞进 1 页 | 论据 1-2 一页 + 论据 3-4 一页 |
| 5 个未来方向 | 全部塞进 1 页 | 方向 1-3 一页 + 方向 4-5 一页 |

### 翻页节奏与页数指导

每页停留时间约 30-60 秒。页数不设上限，内容决定页数。

| 演讲时长 | 推荐幻灯片数 | 每页平均时间 |
|----------|-------------|-------------|
| 5 分钟 | 8-12 张 | 25-37 秒 |
| 10 分钟 | 16-24 张 | 25-37 秒 |
| 15 分钟 | 24-32 张 | 28-37 秒 |
| 20 分钟 | 32-40 张 | 30-37 秒 |

**注意**：以上数字包含 fragment 动画步骤。实际「点击次数」会更多（每页 3-5 次点击），观众感受到的节奏是流畅的。

### 纲要化内容规则（v2.1 新增）

幻灯片正文**只放关键词/短语**，详细叙述全部进 speaker notes：

| 元素 | 屏上最大字数 | 超出处理 |
|------|------------|---------|
| 列表项 `<li>` | **8 中文字** | 提炼关键词，原文进 notes |
| 引用 `<blockquote>` | **20 中文字** | 提炼金句，完整引用进 notes |
| 段落 `<p>`（非 notes） | **15 中文字** | 仅允许短标注/图说 |
| 高亮框内文字 | **12 中文字** | 精简或拆页 |

**豁免**：封面副标题（≤15 字）、代码块、data-impact 上下文行（≤15 字）。

### image-showcase 布局规则（v2.1 新增）

image-showcase 模式下：
- 图片占据 **70%+** 幻灯片高度（使用 `r-stretch` 或 `max-height: 480px`）
- 图说/标注仅 **1 行 ≤ 12 中文字**
- **禁止**同页放 blockquote、列表、多行段落
- 竖版图片（如手机截图）：加 `max-height: 500px; width: auto` 防溢出

### blockquote 长度上限（v2.1 新增）

| 内容类型 | 上限 | 超出处理 |
|----------|------|---------|
| blockquote 可见文字 | **20 中文字** | 提炼金句上屏，完整引用进 speaker notes |

---

## 参考文档

| 文件 | 内容 | 何时加载 |
|------|------|---------|
| `templates/base.html` | Reveal.js HTML 模板（本地路径，离线版骨架） | Phase 2 生成 HTML 时 |
| `references/animation-mapping.md` | Remotion 动画 → Reveal.js 映射表 | Phase 1 设计动画时 |
| `references/slide-patterns.md` | 10 种幻灯片模式（含 HTML 代码模板） | Phase 1-2 设计和生成时 |
| `references/theme-presets.md` | Quarto Light 主题定义 + 安全色板 | Phase 2 生成 CSS 时 |
| `references/svg-diagram-guide.md` | 内联 SVG 图表制作 + fragment 动画 | Phase 2 制作图表时 |
| `references/enhanced-animations.md` | 3b1b/回形针/手绘增强动画 CSS + SVG 模板 | Phase 1-2 设计增强动画时 |
| `references/image-sources.md` | Pexels/Gemini AI/论文展示的完整实现 | Phase 0 配图意图 + Phase 2 嵌入时 |
| `references/article-mode.md` | 文章模式完整步骤 A-F + 调和方案 | Phase 0 文章模式时 |
| `references/technical-rules.md` | Fragment/字体/溢出/SVG 规则 + 验证清单 | Phase 2 生成 + Phase 3 验证时 |

---

## 工作流（4 Phase）

### 输入模式路由（Phase 0 入口）

Phase 0 根据输入类型进入不同分支：

| 输入类型 | 判断依据 | 进入模式 |
|----------|---------|---------|
| 主题关键词 | 用户给出主题，无完整文本 | **标准模式**（下方 Phase 0） |
| 学术论文 | PDF/arxiv 链接/论文结构 | **标准模式** + 论文展示（Paper-01/02/End） |
| **用户的 Markdown 文章** | 用户提供完整 Markdown 文本，明确说"我的文章"/"把这篇文章做成幻灯片" | **文章模式**（见 `references/article-mode.md`） |

**判断原则**：当用户提供一篇完整的、有自身叙事结构的 Markdown 文章时，进入文章模式。文章模式的核心目标是**尊重原文结构和表达**，而非重新构建叙事。

---

### Phase 0（标准模式）：内容分析与结构设计

**继承自 remotion-video Phase 0-1**，适配幻灯片场景：

1. 分析输入内容（主题/论文/文章）
2. 提取关键信息（论文：标题、作者、机构、期刊、DOI）
3. 学术定位（论文类输入时）：
   - 学术根基：本研究建立在哪些基础工作之上？
   - 学术遗产：后续有哪些工作引用了本研究？
   - 竞争方案：同期有哪些替代方法？
4. 构建认知阶梯：
   - L1 故事与直觉：为什么这个问题重要？（生活类比、痛点）
   - L2 概念与逻辑：系统如何工作？（输入→输出、模块交互）
   - L3 细节与实现：关键技术细节（算法、工程技巧）
   - L4 数学与严谨：核心公式推导（边界条件、证明）
5. 规划幻灯片结构：将内容拆分为 slide sections
   - **单页聚焦检查**：每张 slide 必须能用一句话概括其焦点。如果写不出一句话，说明内容过多，需拆分
   - **内容类型互斥检查**：每张 slide 只能有一种主要内容（列表 OR 图表 OR 引用 OR 大数字 OR 配图）。如有两种以上主要内容，必须拆分
   - 不怕 slide 数量多——30 张聚焦的幻灯片优于 18 张拥挤的幻灯片
   - 可使用垂直幻灯片（nested `<section>`）做可选深入内容
6. **标注配图意图**（v1.6 新增）：为每张幻灯片标注配图意图（`process`/`architecture`/`comparison`/`data`/`math`/`concept`/`metaphor`/`scene`/`title`/无），确定视觉来源（内联 SVG / Gemini AI / Pexels / 无）
   - `concept`、`metaphor`、`scene` 意图优先使用 Gemini AI 配图（如有 API key）
   - 全篇 Gemini AI 配图不超过 3 张
   - 无 API key 时降级为 Pexels 照片或纯 SVG
7. 为每张幻灯片**初步**分配动画模式和增强风格（Phase 1 细化）
   - 根据内容类型自动分配风格（见「动画风格系统」一节）
   - 大部分幻灯片使用默认 Quarto Light，仅特定内容使用增强风格

**输出**：`plan.md`（幻灯片规划文档）

```markdown
# 演示文稿规划

## 基本信息
- 主题：xxx
- 预计幻灯片数：N
- 基础主题：Quarto Light
- 增强风格：按内容自动分配（3b1b 暗色 / 回形针数据 / 手绘白板 / 默认 Quarto Light）
- 预计演讲时长：X 分钟
- 语言：简体中文（默认，无特殊声明时一律使用）/ 其他（仅当用户明确声明时）

## 幻灯片列表

### Slide 01: 封面
- 焦点：展示论文/演讲标题与作者信息
- 模式：title-slide
- 风格：默认（Quarto Light）
- 内容：标题、作者、日期
- 动画：fade-in fragments

### Slide 02: 问题引入
- 焦点：为什么这个问题值得关注
- 模式：progressive-reveal
- 风格：默认
- 内容：3 个要点逐步展示（≤3 条）
- 演讲者备注：先提问引发思考...

### Slide 03: 核心概念（数学推导 A）
- 焦点：[单一概念/公式]
- 模式：math-blackboard / path-trace
- 风格：3b1b（白底）
- 内容：一个公式推导步骤 + SVG 路径绘入动画
- 演讲者备注：...

### Slide 04: 核心概念（数学推导 B）
- 焦点：[下一个概念/公式]
- 模式：同上
- 内容：承接上页，展示下一步推导

### Slide 05: 数据对比
- 焦点：某个关键指标的冲击力
- 模式：data-impact
- 风格：回形针数据
- 内容：一个大数字 + 趋势 badge + 来源
- 演讲者备注：...

### Slide 06: 直觉解释
- 焦点：用直觉理解核心机制
- 模式：hand-drawn-diagram
- 风格：手绘白板
- 内容：一个手绘流程图
- 演讲者备注：...

### Slide 07: 核心隐喻
- 焦点：通过隐喻理解抽象概念
- 模式：image-showcase
- 配图意图：`metaphor`
- 视觉来源：Gemini AI 配图
- 内容：AI 配图 + 1-2 句说明
- 演讲者备注：...
```

### 输出语言规则（强制，最高优先级）

**无特殊说明时，一律使用简体中文**。无论用户输入的内容是中文、英文还是其他语言，幻灯片的所有可见文本（标题、正文、列表、引用、SVG 文字、演讲者备注）默认使用简体中文。

**仅当用户明确声明目标语言时**（如"用英文"、"output in English"、"日本語で"），按声明执行。

| 情况 | 输出语言 |
|------|----------|
| 用户未指定语言（任何输入语言） | **简体中文** |
| 用户声明"用英文" | 英文 |
| 用户声明其他语言 | 按声明执行 |

**⚠️ 常见错误**：输入英文论文/文章时，容易不自觉地用英文写幻灯片内容。必须主动翻译为简体中文。

---

### Phase 0（文章模式）：结构保真转换

**适用条件**：用户提供自己撰写的 Markdown 文章，要求转换为幻灯片。

**核心理念**：文章已经是作者反复锤炼的成品，目标是**忠实保留原文结构和表达**，而非重新构建叙事。跳过认知阶梯和学术定位，使用文章自身的叙事结构。

> **完整流程**：见 `references/article-mode.md`。包含步骤 A-F（Markdown 结构解析、图片资源校验、章节→幻灯片映射、内容保真规则、配图意图标注、plan.md 输出）及与现有规则（列表条数、单页聚焦、视觉多样性）的调和方案。

---

### Phase 0.5：内容密度审计（v2.1 新增）

plan.md 完成后、HTML 生成前，逐张检查：
1. 每个可见文本 ≤ 8 字（列表项）/ ≤ 15 字（段落）/ ≤ 20 字（引用）？
2. 每张只有一种主要内容？
3. blockquote ≤ 20 字？
4. image-showcase 无段落/列表竞争？
5. 符合 SVG 转换模式的已标记为 SVG？

**不通过则修改 plan.md 后再进入 Phase 1。**

---

### Phase 1：视觉设计

1. **加载 Quarto Light 主题**（加载 `references/theme-presets.md`）——Quarto Light 为基础主题
2. **加载增强动画参考**（加载 `references/enhanced-animations.md`）——确定哪些幻灯片使用 3b1b/回形针/手绘增强风格
3. **细化动画模式**：加载 `references/slide-patterns.md`，为每张幻灯片确定最终动画模式（含增强模式）
4. **确定增强风格分配**：根据「动画风格系统」中的内容类型→风格映射表，为每张幻灯片确认最终风格
5. 为需要图表的幻灯片**设计 SVG 规格说明**（元素列表、坐标、绘制顺序）
   - 加载 `references/svg-diagram-guide.md` 获取模板
   - 使用增强风格的 SVG 图表须遵循对应风格的色板和动画规范
6. 为代码幻灯片规划步进高亮（行号范围、步骤数）
7. 决定背景设置（`data-background-color`、`data-background-image`）
   - 3b1b 风格：`data-background-color="#1a1a2e"`
   - 回形针风格：`data-background-color="#f5f5f5"`
   - 手绘风格：`data-background-color="#fffef9"`
   - 默认 Quarto Light：白色背景（无需设置）
8. **视觉模式交替检查**：审查相邻幻灯片不得使用相同视觉模式（如连续两张 bullet list、连续两张 quote-card），如有重复，调整其中一张为不同模式。**不可连续两张暗色背景幻灯片**
9. 编写所有幻灯片的演讲者备注

### Phase 2：HTML 生成

0. **⚠️ 语言确认（必须首先执行）**：读取 `plan.md` 中的"语言"字段。**无特殊声明时一律简体中文**，无论输入内容是什么语言。在后续每张幻灯片的编写中，强制使用确认后的语言。常见陷阱：输入英文论文时，容易不自觉地用英文写内容——必须主动翻译为简体中文。
1. **准备离线资源目录**（离线优先：Phase 2 直接生成完整离线版本）：
   ```bash
   mkdir -p "<output-dir>"/{dist/theme,plugin/notes,fonts,images}
   ```
   - **下载 Reveal.js 5.2.1**：
     ```bash
     CACHE="$HOME/.claude/cache/reveal-5.2.1"
     if [ -d "$CACHE/dist" ]; then
       cp "$CACHE/dist/reset.css" "<output-dir>/dist/"
       cp "$CACHE/dist/reveal.css" "<output-dir>/dist/"
       cp "$CACHE/dist/reveal.js" "<output-dir>/dist/"
       cp "$CACHE/dist/theme/white.css" "<output-dir>/dist/theme/"
       cp "$CACHE/plugin/notes/notes.js" "<output-dir>/plugin/notes/"
     else
       BASE="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1"
       curl -sL "$BASE/dist/reset.css" -o "<output-dir>/dist/reset.css"
       curl -sL "$BASE/dist/reveal.css" -o "<output-dir>/dist/reveal.css"
       curl -sL "$BASE/dist/reveal.js" -o "<output-dir>/dist/reveal.js"
       curl -sL "$BASE/dist/theme/white.css" -o "<output-dir>/dist/theme/white.css"
       curl -sL "$BASE/plugin/notes/notes.js" -o "<output-dir>/plugin/notes/notes.js"
       # 回填缓存
       mkdir -p "$CACHE"/{dist/theme,plugin/notes}
       cp -r "<output-dir>/dist/"* "$CACHE/dist/"
       cp -r "<output-dir>/plugin/"* "$CACHE/plugin/"
     fi
     # 按需复制 highlight/math 插件
     ```
   - **下载 Google Fonts**：
     ```bash
     curl -sL "https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Noto+Sans+SC:wght@400;700&display=swap" \
       -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
       -o "<output-dir>/fonts/fonts.css"
     grep -oP 'url\(\K[^)]+' "<output-dir>/fonts/fonts.css" | while read url; do
       fname=$(echo "$url" | grep -oP '[^/]+$')
       curl -sL "$url" -o "<output-dir>/fonts/$fname"
     done
     # 将 fonts.css 中远程 URL 替换为本地文件名
     sed -i 's|url(https://[^)]*\/\([^/]*\.woff2\))|url(\1)|g' "<output-dir>/fonts/fonts.css"
     ```
   - **下载/复制图片到 images/**：Pexels → 下载；文章原图 → 下载/复制；Gemini → 复制
   - **HTML 中使用本地路径引用所有资源**：
     ```html
     <!-- CSS -->
     <link rel="stylesheet" href="dist/reset.css">
     <link rel="stylesheet" href="dist/reveal.css">
     <link rel="stylesheet" href="dist/theme/white.css">
     <link rel="stylesheet" href="fonts/fonts.css">
     <!-- JS -->
     <script src="dist/reveal.js"></script>
     <script src="plugin/notes/notes.js"></script>
     <!-- 图片 -->
     <img src="images/article-01.png" ...>
     ```
   - **⚠️ 离线优先原则**：Phase 2 生成的 index.html 必须**零外部依赖**，`grep -c 'https://' index.html` 必须为 0
2. 创建 `images/` 目录（已在上一步完成）：确认所有图片已下载到 `images/`
3. 加载 `templates/base.html` 作为骨架
4. 逐张生成幻灯片 HTML（section 元素）
   - 使用增强风格的幻灯片须设置 `data-background-color` 并使用对应命名空间 CSS class（`.s3b1b-*`、`.paperclip-*`、`.handdrawn-*`）
5. 生成自定义 CSS（内联 `<style>` 块）
6. **生成增强动画 CSS**（注入 `{{ENHANCED_CSS}}` 占位符）：
   - 从 `references/enhanced-animations.md` 复制所需的 CSS @keyframes 和组件样式
   - 仅注入实际使用的风格（如无 3b1b 幻灯片则不注入 3b1b CSS）
7. **生成 SVG 滤镜定义**（注入 `{{SVG_DEFS}}` 占位符）：
   - 手绘风格需要 `feTurbulence` + `feDisplacementMap` 滤镜
   - 如无手绘幻灯片则留空
8. 生成内联 SVG 图表（带 fragment class）
   - 3b1b 风格 SVG 使用 `pathLength="1"` + CSS draw-in 动画
   - 手绘风格 SVG 添加 `filter="url(#handdrawn)"` 属性
9. **生成增强 JS**（注入 `{{ENHANCED_JS}}` 占位符）：
   - 回形针数字动画需要 CSS `@property` 支持，可选注入 JS fallback
   - 如无回形针数字动画则留空
10. 组装完整 HTML 文件

**输出**：`~/Downloads/slides-<topic>-<date>/index.html`

### Phase 3：验证与打包

1. 检查所有 fragment 索引连续无缺
2. 检查 auto-animate 配对正确（相邻 section 都有 data-auto-animate）
3. 检查所有 data-id 匹配
4. 检查 SVG 元素不超出 viewBox
5. 检查演讲者备注完整
6. **⚠️ 事实核查（最高优先级，v1.7.1 强化）**：
   - **所有数字、名称、日期、版本号、引用语句**必须回到源材料逐一核实，**禁止凭记忆或推断填写**
   - **模型版本号**：必须从论文原文精确提取，不可使用自己对模型版本的"常识"（论文可能使用比你知识截止日期更新的模型）
   - **协议/方法描述**：必须准确反映论文的方法论，不可用自己理解的"合理流程"替代
   - **引用翻译**：翻译英文论文引语时，必须基于原文逐句翻译，不可意译为"更通顺"但含义不同的版本
   - **统计数据**：只使用论文明确给出的数字，不可从模糊表述（如"millions"）推断具体数值（如"3亿"）
   - **分类/枚举**：论文列出 N 个类别/项目时，幻灯片必须精确反映 N 个，不可增减
   - **推荐使用 Agent 工具**：对于论文类输入，启动专门的验证 Agent 读取原文 PDF，逐张幻灯片核对每一个事实声明
   - **致命错误示例**（v1.7.0 实际事故）：
     | 错误类型 | 具体事例 | 后果 |
     |---------|---------|------|
     | 模型版本凭"常识"填写 | 论文用 GPT-5 class，幻灯片写 GPT-4o | 在讲台上被质疑专业性 |
     | 方法论凭"合理推断" | 论文由研究者当治疗师，幻灯片写 GPT-4o 当治疗师 | 歪曲论文核心设计 |
     | 统计数据凭想象 | 论文说"millions of conversations"，幻灯片写"超过3亿人" | 无法溯源的虚假数据 |
     | 分类数量不核实 | 论文有6个量表类别，幻灯片说"5大类" | 遗漏重要信息 |
     | 引语自由发挥 | 论文原文"gaslighting on industrial scale"，翻译成"心理审讯" | 语义偏差 |
     | 建议内容编造 | 论文3条具体建议被替换为自己编的3条 | 完全背离原文 |
7. **单页聚焦检查**：逐张审查每张幻灯片是否只有一种主要内容。如发现一页同时包含列表+图表、引用+列表等多种主要内容，必须拆分
8. **视觉多样性检查**：扫描相邻幻灯片的模式，确认无连续重复（如连续 bullet list、连续 quote-card）
8. **CSS 清理**：删除 `<style>` 中未被任何元素引用的 class（redesign 后尤其容易遗留）
9. **插件精简**：检查 `Reveal.initialize()` 中加载的插件，移除未实际使用的（如无代码块则不加载 highlight.js，无公式则不加载 math/KaTeX）
10. **⚠️ 自动化安全检查（必须用 Bash/Grep 工具执行，不可跳过）**：
    ```bash
    # 检查 1：fragment grow 是否被滥用（结果必须为 0）
    grep -c "fragment grow" index.html
    # 如果 > 0，逐一检查每处 grow 的文本长度，超过 10 字符的必须替换为 fade-up

    # 检查 2：语言一致性（默认中文时执行）
    # 提取所有 <h2>/<h3> 标题文本，检查是否包含连续英文单词（排除专有名词）
    grep -oP '(?<=<h[23][^>]*>)[^<]+' index.html | grep -P '^[A-Z][a-z]+ [A-Z]?[a-z]+ [a-z]'
    # 如果有匹配，说明标题仍为英文，必须修正

    # 检查 3：speaker notes 语言（默认中文时执行）
    grep -A2 'class="notes"' index.html | grep -P '^\s+[A-Z][a-z]+ [a-z]+ [a-z]'
    # 如果有匹配，说明演讲者备注仍为英文，必须修正

    # 检查 4：SVG 彩色节点内文字颜色（结果必须为 0）
    # 快速检测：SVG 内不应出现 fill="#555555" 或 fill="#495057" 或 fill="#222222"
    # 手动审查：逐个 SVG 图表，确认每个 <text> 的 fill 是否与其所在背景匹配

    # 检查 5：暗色主题残留色（结果必须为 0）
    grep -cP '#e5e7eb|#fcd34d|rgba\(255,255,255|#58C4DD|#FF6B6B|#83C167|#1a1a2e|#0f0f1a|#0d1117' index.html
    # 如果 > 0，逐一检查每处上下文并修正
    ```
11. 提示用户在浏览器中打开验证（按 S 键查看演讲者视图）

> **完整技术规则与验证清单**：见 `references/technical-rules.md`。Phase 2 生成 HTML 和 Phase 3 验证时必须加载。涵盖：Fragment 规则与逐步揭示、动画效果目录、字体/对比度/溢出安全、SVG 规则、Auto-animate、代码步进、布局辅助类、已知限制、全部验证清单。

---

## 动画风格系统（v1.5 新增，v1.5.1 修订）

**统一使用 Quarto Light 白色背景**。三种增强风格仅继承动画效果和 CSS 类，**不切换背景色**。

### 三种增强风格（均在白色背景上）

| 风格 | 背景色 | 适用内容 | CSS 命名空间 | 来源 |
|------|--------|----------|-------------|------|
| **3b1b Math** | **`#ffffff`（白色）** | 数学推导、公式、几何、算法可视化 | `.s3b1b-*` | remotion-video |
| **回形针 Data** | `#f5f5f5`（浅灰） | 数据冲击、对比、统计、来源引用 | `.paperclip-*` | remotion-video |
| **手绘 Whiteboard** | `#fffef9`（暖白） | 直觉解释、流程图、思维导图、标注 | `.handdrawn-*` | remotion-excalidraw-video |

**⚠️ 禁止暗色背景**：不使用 `#1a1a2e`、`#0f0f1a`、`#0d1117` 等暗色。3b1b 动画效果（drawIn、glowPulse）在白色背景上同样有效，公式用 `#f0f7ff` 浅蓝框 + `#2a76dd` 边框替代暗色黑板感。

### 3b1b 风格 Quarto Light 适配色板

原 3b1b 暗色主题的颜色需要映射到 Quarto Light 安全色：

| 用途 | ❌ 暗色主题原色 | ✅ Quarto Light 替代 |
|------|---------------|---------------------|
| 主 accent | `#58C4DD`（亮青） | `#2a76dd`（蓝） |
| 强调/高亮 | `#fcd34d`（金色） | `#e67e22`（橙） |
| 正文文字 | `#e5e7eb`（浅灰） | `#333333`（深灰） |
| 副文字 | `rgba(255,255,255,0.7)` | `#495057`（中灰） |
| 错误/警告 | `#FF6B6B`（亮红） | `#c82333`（深红） |
| 成功/正确 | `#83C167`（亮绿） | `#1e7e34`（深绿） |
| 公式框背景 | 暗色底 | `#f0f7ff` + `border: #2a76dd` |
| SVG 网格线 | `rgba(255,255,255,0.05)` | 不需要（白底自然干净） |

### 内容类型 → 风格自动分配

| 内容类型 | 配图意图 | 推荐风格 | 视觉来源 |
|----------|---------|---------|----------|
| 公式推导、数学证明 | `math` | 3b1b 动画（白底） | 内联 SVG（drawIn） |
| 算法步骤、几何图形 | `process` | 3b1b 动画（白底） | 内联 SVG（pathLength） |
| 关键数字、性能指标 | `data` | 回形针数据 | CSS 计数动画 |
| 方案对比、数据图表 | `comparison` | 回形针数据 | 内联 SVG 对比条 |
| 直觉解释、类比 | `concept` | 手绘白板 / **Gemini AI** | SVG 手绘 或 AI 配图 |
| 流程图、思维导图 | `architecture` | 手绘白板 | 内联 SVG（feTurbulence） |
| **抽象概念可视化** | **`concept`** | **默认** | **Gemini AI 配图** |
| **隐喻/类比图** | **`metaphor`** | **默认** | **Gemini AI 配图** |
| **场景/故事性插图** | **`scene`** | **默认** | **Gemini AI 配图** 或 Pexels |
| 封面、目录、总结 | `title` | 默认 Quarto Light | Pexels 背景 |
| 文字列表、引用、代码 | — | 默认 Quarto Light | 无配图 |

**配图意图词汇表**（Phase 0 规划时标注）：

| 意图 | 含义 | 典型实现 |
|------|------|---------|
| `process` | 流程/步骤/管线 | 内联 SVG flowchart + Fragment |
| `architecture` | 系统组件/层级 | 内联 SVG hub-spoke / layered |
| `comparison` | A vs B 对比 | 内联 SVG side-by-side + Fragment |
| `data` | 数据趋势/统计 | 回形针 bar/counter 动画 |
| `math` | 公式推导/证明 | 3b1b drawIn + KaTeX |
| `concept` | 抽象概念可视化 | **Gemini AI 生成** |
| `metaphor` | 隐喻/类比表达 | **Gemini AI 生成** |
| `scene` | 场景/故事性画面 | **Gemini AI** 或 Pexels 照片 |
| `title` | 封面/总结装饰 | Pexels 背景图 |

### 风格混合规则

1. **每张幻灯片只能使用一种风格**，不可在同一张上混合 3b1b + 手绘
2. **手绘风格幻灯片全篇不超过 3 张**（feTurbulence 性能考量）
3. **增强风格幻灯片总占比不超过 40%**，大部分应为默认 Quarto Light
4. **禁止 `has-dark-background` CSS 规则**——不再需要暗色主题颜色合约

### 文字→SVG 转换标准（v2.1 新增）

Phase 0 规划时，对每张纯文字 slide 检测以下模式，命中任一 → **必须转 SVG**，关键词列表是后备方案：

| 内容模式 | 转为 SVG 类型 |
|----------|-------------|
| 3+ 步骤流程 | 流程图（diagram-build） |
| 实体间消息传递 | 消息流/序列图 |
| 2+ 并列选项（含失败路径） | 分支路径图 |
| 前后转变 | 转换箭头图 |
| 时间线演变 | 时间轴 |
| 两类对比 | 双栏对比图 |

### 颜色合约

统一使用 Quarto Light 安全色板，详见 `references/theme-presets.md`。所有文字/SVG 颜色必须在白色背景上满足 WCAG AA 对比度（≥4.5:1）。

---

## 输出目录（双版本交付，离线优先）

每次生成幻灯片，**必须同时交付两个版本**。Phase 2 **首先生成离线版**（完整自包含），Phase 4 再从离线版**做减法**派生 CDN 版。

### 离线版本（Phase 2 直接产出，tar.gz 打包发送）

Phase 2 直接生成的完整自包含文件夹，`grep -c 'https://' index.html` 必须为 0：

```
~/Downloads/slides-<topic>-<YYYYMMDD>/
├── index.html              # 主演示文稿（所有路径指向本地）
├── plan.md                 # Phase 0 规划文档
├── dist/                   # Reveal.js 5.2.1 核心
│   ├── reset.css
│   ├── reveal.css
│   ├── reveal.js
│   └── theme/
│       └── white.css
├── plugin/                 # Reveal.js 5.2.1 插件（按需）
│   ├── notes/notes.js
│   ├── highlight/          # 仅当有代码块时
│   └── math/               # 仅当有公式时
├── fonts/                  # 离线字体
│   ├── fonts.css           # @font-face 声明（本地路径）
│   └── *.woff2             # Source Sans Pro + Noto Sans SC
└── images/                 # 所有图片的本地副本
    ├── pexels-<id>.jpg
    ├── gemini-01.jpg
    ├── article-01.png
    └── paper-page-01.png
```

### CDN 版本（Phase 4 从离线版做减法派生）

Phase 4 Step 3 从离线版 index.html 复制一份，将本地路径替换为 CDN URL。部署到 Cloudflare 的**只有 index.html 一个文件**。

**⚠️ 两个版本的 index.html 路径对比**：

| 资源 | 离线版（Phase 2 产出） | CDN 版（Phase 4 派生） |
|------|----------------------|---------------------|
| Reveal.js CSS/JS | `dist/reveal.js` 等 | `https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/...` |
| 字体 | `fonts/fonts.css` | `https://fonts.googleapis.com/...` |
| 图片 | `images/<name>.<ext>` | `https://pub-xxx.r2.dev/<sha1>.<ext>` |
| 外部依赖 | **0**（零外部请求） | 需联网 |

---

## Phase 4：交付与部署（v2.2 重构，离线优先）

**核心理念**：Phase 2 生成的 index.html 已经是**完整离线版**（所有资源本地引用），Phase 4 的任务是：先交付离线版，再从离线版**做减法**派生 CDN 版部署。

> 做减法（本地路径 → CDN URL）比做加法（CDN → 下载回本地）更简单、更可靠。

### Step 1：打包离线版并发送 Telegram（最高优先级）

**用户最先拿到可用的离线包**，不需要等 R2 上传和 Cloudflare 部署。

```bash
# 验证离线完整性
grep -c 'https://' "<output-dir>/index.html"  # 必须为 0

# 打包（排除临时目录）
cd <parent-dir>
tar czf /tmp/slides-<topic>-offline.tar.gz \
  --exclude='.wrangler' --exclude='archive' \
  -C slides-<topic>-<date> .

# 发送到 Telegram
eval "$(grep '^export ' ~/.config/secrets.zsh)"
curl -s -F chat_id=<YOUR_CHAT_ID> \
  -F document=@"/tmp/slides-<topic>-offline.tar.gz" \
  -F caption="<topic> 演示文稿 — 完全离线版
解压后双击 index.html 即可使用，无需联网
含：Reveal.js 5.2.1 + 图片 + 字体 + N张幻灯片" \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument"
```

### Step 2：上传图片到 R2 CDN

将 `images/` 目录中的图片上传到 R2，获取公开 URL，为 CDN 版做准备。

**图片来源分类**：

| 图片来源 | 处理方式 |
|----------|---------|
| 文章原图（已有 R2 URL） | **记录原始 R2 URL**，无需重复上传 |
| Pexels 下载图 | 计算 SHA1，上传到 R2，获取新 URL |
| Gemini AI 生成图 | 计算 SHA1，上传到 R2，获取新 URL |
| 论文截图 | 计算 SHA1，上传到 R2，获取新 URL |

**上传脚本**（使用 boto3）：

```python
import boto3, hashlib, json, os
from pathlib import Path

s3 = boto3.client("s3",
    endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
    aws_access_key_id=os.environ["R2_ACCESS_KEY"],
    aws_secret_access_key=os.environ["R2_SECRET_KEY"],
    region_name="auto"
)

def upload_to_r2(file_path):
    data = Path(file_path).read_bytes()
    sha1 = hashlib.sha1(data).hexdigest()
    ext = Path(file_path).suffix.lstrip(".")
    key = f"{sha1}.{ext}"
    try:
        s3.head_object(Bucket=os.environ["BUCKET_NAME"], Key=key)
    except:
        s3.put_object(
            Bucket=os.environ["BUCKET_NAME"], Key=key, Body=data,
            ContentType=f"image/{ext}", CacheControl="public, max-age=31536000, immutable"
        )
    return f"{os.environ['PUBLIC_URL']}/{key}"
```

**R2 缓存更新**：上传后同步更新 `~/.cloudflare-pages/r2-cache.json`。

### Step 3：派生 CDN 版 index.html（做减法）

从离线版 index.html **复制一份**，将本地路径替换为远程 URL：

| 查找（本地路径） | 替换为（远程 URL） |
|-----------------|-------------------|
| `<link rel="stylesheet" href="fonts/fonts.css">` | `<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">` |
| `href="dist/reset.css"` | `href="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/dist/reset.css"` |
| `href="dist/reveal.css"` | `href="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/dist/reveal.css"` |
| `href="dist/theme/white.css"` | `href="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/dist/theme/white.css"` |
| `src="dist/reveal.js"` | `src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/dist/reveal.js"` |
| `src="plugin/notes/notes.js"` | `src="https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/plugin/notes/notes.js"` |
| 每个 `images/<name>.<ext>` | 对应的 R2 URL `https://pub-xxx.r2.dev/<sha1>.<ext>` |

同时在 `<head>` 中添加 Google Fonts preconnect：
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

**CDN 版验证**：`grep -c 'images/' cdn-index.html` 必须为 0（所有本地图片路径已替换）。

### Step 4：部署到 Cloudflare Pages

调用 cloudflare-pages-deployer skill 部署 **CDN 版 index.html**（单文件）：

1. 清理旧部署目录：`rm -rf ~/.cloudflare-pages/site/slides/<topic>/*`
2. 复制 CDN 版：`cp cdn-index.html ~/.cloudflare-pages/site/slides/<topic>/index.html`
3. 更新 manifest + 重新生成首页
4. 执行 `wrangler pages deploy`

### Step 5：发送在线版链接到 Telegram

```
在线版已部署：
https://<your-domain>/slides/<topic>/
```

### 降级策略

| 场景 | 处理 |
|------|------|
| R2 凭据缺失 | 跳过 Step 2-4，仅发送 tar.gz（Step 1 已完成） |
| Cloudflare 凭据缺失 | 跳过 Step 4，仅发送 tar.gz + R2 图片已上传 |
| 单张图片上传失败 | CDN 版保留该图的本地路径，其他图正常替换，日志警告 |
| Telegram 发送失败 | 重试一次，仍失败则输出本地路径让用户手动获取 |
