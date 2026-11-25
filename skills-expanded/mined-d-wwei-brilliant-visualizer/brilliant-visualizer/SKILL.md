---
name: brilliant-visualizer
description: >
  Use when an article needs illustrations, diagrams, or images. Analyzes article content,
  identifies illustration points, routes to the best engine (Mermaid, D2, AI generation,
  stock photos, HTML rendering), and generates or searches for matching visuals.
  Standalone or integrated as a stage in great-writer pipeline.
triggers:
  # Chinese
  - 配图
  - 插图
  - 加图
  - 给文章配图
  - 生成插图
  - 画个图
  - 流程图
  - 架构图
  - 思维导图
  - 封面图
  - 题图
  - 搜图
  - 找图
  # English
  - visualize
  - illustrate
  - add illustrations
  - add images
  - diagram
  - flowchart
  - architecture diagram
  - cover image
  - generate image
  - find images
---

# Brilliant Visualizer — 文章智能配图

分析文章内容，识别配图位置，选择最佳引擎，生成或搜索配图。

## 工作模式

两步走: **分析 → 确认 → 生成**

```
输入文章 → 分析器扫描 → 输出配图方案表 → 用户确认/修改 → 逐个生成 → 插入文章
```

## 调用方式

```bash
visualize article.md              # 完整流程: 分析 + 生成
visualize --analyze-only          # 仅分析，不生成
visualize --engine mermaid        # 仅生成 Mermaid 图表
visualize --engine ai-image       # 仅生成 AI 图片
visualize --engine stock-photo    # 仅搜索图库
```

不同 Agent 平台的命令前缀：
- **Claude Code**: `/visualize`
- **Codex / Gemini CLI / 其他**: 按该平台的 skill 调用方式

被 great-writer 调用时，在 Draft 和 Review 之间自动插入:
```
Research → Draft → [Visualize] → Review → Humanize → Finalize
```

---

## 阶段一: 分析

### 1. 读取文章

支持输入:
- Markdown 文件路径
- 剪贴板/粘贴的 Markdown 内容
- 当前会话中 great-writer 刚完成的草稿

### 2. 扫描与识别

逐段扫描文章，识别以下配图点:

| 信号 | 配图类型 | 默认引擎 |
|------|---------|---------|
| 流程描述、步骤列表、决策分支 | 流程图 | mermaid |
| API 调用链、请求/响应、系统交互 | 时序图 | mermaid |
| 数据模型、表结构、实体关系 | ER 图 | mermaid |
| 状态转换、生命周期 | 状态图 | mermaid |
| 项目计划、时间线、里程碑 | 甘特图 | mermaid |
| 分类、层次、知识结构 | 思维导图 | mermaid |
| 系统架构、微服务拓扑、部署 | 架构图 | architecture |
| 数据对比、性能指标、统计 | 对比图/信息图 | html-render |
| 抽象概念、隐喻、需要视觉化 | 概念图 | ai-image |
| 人物、场景、真实环境 | 场景图 | stock-photo |
| 文章首图/封面 | 封面图 | ai-image |

### 3. 输出配图方案表

```markdown
## 配图方案

| # | 位置 | 类型 | 引擎 | 描述 | 优先级 |
|---|------|------|------|------|--------|
| 1 | 标题后 | 封面图 | ai-image | 主题概念图，科技感风格 | 必要 |
| 2 | §2 后 | 架构图 | mermaid | 微服务拓扑，3 个核心服务 | 必要 |
| 3 | §3 后 | 流程图 | mermaid | 用户注册→激活→首次使用 | 必要 |
| 4 | §5 后 | 对比图 | html-render | 新旧方案性能指标 | 建议 |
| 5 | §6 结尾 | 氛围图 | stock-photo | 团队协作场景 | 可选 |

确认后开始生成？可修改/删除/新增任意配图点。
```

用户可以:
- 确认全部 → 进入生成阶段
- 修改某行的引擎或描述
- 删除不需要的行
- 新增遗漏的配图点

---

## 阶段二: 生成

### 1. 环境检查

生成前自动检查所需工具:

```bash
# 按需检查
command -v mmdc 2>/dev/null   # Mermaid CLI
command -v d2 2>/dev/null     # D2
command -v dot 2>/dev/null    # Graphviz
```

未安装 → 提示安装命令，不自动装。
AI 后端 → 检查环境变量，未配置则跳过该后端。

### 2. 按优先级生成

顺序: 必要 → 建议 → 可选

每生成一个:
1. 执行生成 (读取对应 `engines/*.md` 获取引擎规则)
2. 展示预览/结果
3. 用户确认或要求重新生成

### 3. 输出处理

| 引擎 | 输出方式 |
|------|---------|
| mermaid | 内联 \`\`\`mermaid 代码块 (默认) 或渲染为 PNG |
| architecture (D2/Graphviz) | 渲染为 SVG/PNG → `![](images/xxx.svg)` |
| ai-image | 保存 PNG → `![](images/xxx.png)` |
| stock-photo | 下载图片 → `![](images/xxx.jpg)` + 来源注释 |
| html-render | 截图 PNG → `![](images/xxx.png)` |

### 4. 图片目录与命名

```
文章目录/
  article.md
  images/
    cover-ai-20260328-001.png
    arch-mermaid-20260328-002.svg
    flow-mermaid-20260328-003.png
    compare-html-20260328-004.png
    scene-unsplash-20260328-005.jpg
```

命名规则: `{类型}-{引擎}-{日期}-{序号}.{ext}`

图库图片自动附来源:
```markdown
![团队协作](images/scene-unsplash-20260328-005.jpg)
<!-- Photo by John Doe on Unsplash, License: Unsplash License -->
```

---

## 引擎路由

### 按需加载

主 SKILL.md 不包含引擎实现细节。需要某引擎时，读取对应文件:

| 引擎 | 文件 | 何时加载 |
|------|------|---------|
| Mermaid 图表 | `engines/mermaid.md` | 配图方案含 mermaid 类型时 |
| 架构图 (D2/Graphviz) | `engines/architecture.md` | 配图方案含 architecture 类型时 |
| AI 图片生成 | `engines/ai-image.md` | 配图方案含 ai-image 类型时 |
| 图库搜索 | `engines/stock-photo.md` | 配图方案含 stock-photo 类型时 |
| HTML 渲染 | `engines/html-render.md` | 配图方案含 html-render 类型时 |

### 引擎回退链

```
architecture: D2 → Graphviz → Mermaid (graph)
stock-photo:  Unsplash API → Pexels API → Web Search
ai-image:     本地 Flux2 → gpt-image-1 → DALL-E 3 → nanobanana
html-render:  无头浏览器截图 (Puppeteer / Playwright / gstack browse)
mermaid:      mmdc 渲染 → 内联代码块 (无需工具)
```

---

## 配置

所有配置通过环境变量:

```bash
# AI 图片后端优先级 (逗号分隔)
VISUALIZE_AI_BACKEND=flux2,gpt-image-1,dall-e-3,nanobanana

# 本地 Flux2
VISUALIZE_FLUX2_URL=http://192.168.x.x:port/api/generate

# OpenAI (DALL-E 3 + gpt-image-1)
OPENAI_API_KEY=sk-xxx

# nanobanana
NANOBANANA_API_KEY=xxx

# 图库
UNSPLASH_ACCESS_KEY=xxx
PEXELS_API_KEY=xxx

# 图片输出目录 (默认 ./images/)
VISUALIZE_OUTPUT_DIR=./images

# Mermaid 输出模式: inline (默认) | render
VISUALIZE_MERMAID_MODE=inline
```

---

## 与 great-writer 集成

great-writer Draft 完成后，如果文章包含可配图内容，提示:

> "文章初稿已完成。检测到 N 个可配图位置，要调用 visualize 配图吗？"

用户确认后自动执行配图流程，完成后继续 Review 阶段。

## 与 typeset 衔接

配图完成后的 Markdown 直接交给 typeset:
- Mermaid 代码块: typeset 已支持渲染
- 图片文件: typeset 使用 `![](path)` 引用
- 来源注释: typeset 可选择保留或隐藏

---

## 常见问题

**Q: Mermaid 图表用内联还是渲染?**
默认内联 (目标平台支持 Mermaid 渲染时)。如果目标是微信公众号等不支持 Mermaid 的平台，自动切换为渲染 PNG。

**Q: AI 生成的图片风格怎么控制?**
在配图方案表的"描述"列中指定风格关键词 (科技感、手绘、扁平、3D、照片级)。引擎会自动构建对应 prompt。

**Q: 图库搜索支持中文关键词吗?**
支持。引擎会自动将中文关键词翻译为英文进行搜索，同时保留中文作为备选。

**Q: 没有 API key 能用吗?**
可以。图库搜索会 fallback 到 Web Search。AI 生成需要至少一个后端的 API key 或本地 Flux2。Mermaid 和 HTML 渲染不需要 API key。
