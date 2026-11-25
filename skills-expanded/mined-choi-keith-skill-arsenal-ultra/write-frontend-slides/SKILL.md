---
name: write-frontend-slides
description: 从零开始，或通过转换 PowerPoint 文件，创建富有动画效果的 HTML 演示文稿。适用于用户想要制作演示文稿、把 PPT/PPTX 转成网页，或为演讲/路演创建幻灯片。帮助非设计师通过视觉探索而非抽象选择，来发现自己的审美偏好。
metadata:
  context_weight: heavy
---

# 前端幻灯片

创建零依赖、富有动画效果的 HTML 演示文稿，并且完全在浏览器中运行。

## 核心原则

1. **零依赖** — 使用单个 HTML 文件，内嵌 CSS/JS。无需 npm，也无需构建工具。
2. **展示胜于解释** — 生成可视化预览，而不是抽象选择。人们通过观看来发现自己真正想要什么。
3. **独特设计** — 避免普通的“AI 垃圾感”。每一份演示文稿都必须有定制感。
4. **渐进式披露** — 先阅读轻量的样式索引。对于加粗模板，先用小型预览卡片展示样式，在用户选择模板后再加载完整的 `design.md`。
5. **固定 16:9 舞台（不可妥协）** — 每份演示文稿都使用 1920×1080 的幻灯片画布，并整体缩放到视口。幻灯片必须在所有屏幕上保持 16:9，包括手机。不要为了适配设备而重排内容。

## 设计审美

你容易倾向于生成过于通用、像“发布流式内容”那样的输出。在前端设计中，这会产生用户称之为“AI 垃圾感”的审美。要避免这种情况：要打造富有创意、独特且令人惊喜的前端体验。

重点关注：

- 字体排版：选择美观、独特且有辨识度的字体。避免像 Arial、Inter 这类过于通用的字体，而要选择能提升前端审美的独特字体。
- 色彩与主题：坚持统一且有辨识度的审美。使用 CSS 变量保持一致性。主色和明显的强调色通常比平淡均匀的配色更有冲击力。可以从 IDE 主题和文化审美中获取灵感。
- 动效：为特效和微交互使用动画。优先使用纯 CSS 的 HTML 方案；若可用则使用 React 的 Motion 库。把重点放在高影响时刻：一次精心编排的页面加载和分层揭示（`animation-delay`）比零散的微交互更能带来愉悦感。
- 背景：塑造氛围和层次，而不是默认使用纯色。可以叠加 CSS 渐变、几何图案，或添加与整体审美匹配的环境效果。

避免通用的 AI 生成审美：

- 过度使用的字体家族（Inter、Roboto、Arial、系统字体）
- 老生常谈的配色方案（尤其是白底紫渐变）
- 过于可预测的版式和组件模式
- 缺乏上下文特色的“模板化”设计

要富有创意地进行解读，并做出让人感觉真正为上下文量身定制的意外选择。可以在浅色和深色主题、不同字体、不同审美之间切换。不过你仍然容易在不同生成结果中收敛到相似选择（例如 Space Grotesk）。要避免这种情况：关键在于跳出常规思维！

## 固定舞台规则

这些规则适用于每一份演示文稿中的每一张幻灯片：

- 每份演示文稿都需要一个填满浏览器窗口的视口包装层。
- 每张幻灯片都要在固定的 1920×1080 舞台内编写。
- 舞台会统一缩放以适配视口。它可以出现留白或柱状留白，但不能重新排布内容。
- 不要使用响应式断点来为手机重新安排幻灯片内容。
- 使用 1920×1080 设计尺寸下的固定内部尺寸。
- 幻灯片可见性必须由 `.active` / `.visible` 控制，并通过 `viewport-base.css` 中的 `visibility`、`opacity`、`pointer-events` 来切换。不要使用 `display: none` / `display: block` 进行切换；后续布局类如 `.slide-content { display: flex; }` 可能会覆盖这些状态并让所有幻灯片同时可见。
- 仅在舞台外的非幻灯片 UI，或在完全舞台不切实际的小型回退预览中使用 `clamp()`。
- 包含 `prefers-reduced-motion` 的支持。
- 不要直接否定 CSS 函数（`-clamp()`、`-min()`、`-max()` 会被静默忽略）——请改用 `calc(-1 * clamp(...))`。

**生成时，请阅读 `viewport-base.css`，并将其完整内容包含到每份演示文稿中。**

### 内容密度模式

先询问用户这更像是阅读型演示文稿，还是讲述型演示文稿，然后围绕这个答案设计：

| 密度模式 | 最适合 | 设计行为 |
| ------------- | -------- | --------------- |
| **低密度 / 以讲述为主** | 公共演讲、主题演讲、现场讲解 | 每张幻灯片一个核心观点，字号更大，视觉层级更强，留白更充足，最多 1-3 条要点，必要时增加幻灯片数量 |
| **高密度 / 以阅读为主** | 报告、讲义、异步评审、详细内部文件 | 幻灯片更自包含，使用结构化网格/表格/注释，阅读时可容纳 4-8 条要点或 4-6 张卡片，间距更紧凑但仍保持有意设计 |

仍然遵循基础限制：不能滚动、不能溢出、不能重叠面板，也不能使用低于舒适阅读尺寸的文字。如果内容超过所选密度模式，则应拆分成更多幻灯片，而不是把内容压缩到拥挤不堪。

---

## 阶段 0：识别模式

先判断用户想要什么：

- **模式 A：新建演示文稿** — 从零开始创建。进入阶段 1。
- **模式 B：PPT 转换** — 转换 `.pptx` 文件。进入阶段 4。
- **模式 C：增强优化** — 改进现有 HTML 演示文稿。先阅读和理解，再进行增强。**遵循下面的模式 C 修改规则。**

### 模式 C：修改规则

在增强现有演示文稿时，固定舞台适配是最大的风险：

1. **在添加内容前：** 统计现有元素，并对照密度限制检查。
2. **添加图片时：** 将其放入 1920×1080 的幻灯片画布内。如果当前幻灯片已经接近上限，则拆成两张幻灯片。
3. **添加文字时：** 每张幻灯片最多 4-6 条要点。超出限制时，拆成连续页。
4. **任何修改后都要验证：** 舞台仍保持 16:9，文字不溢出卡片，面板不重叠，并且屏幕截图在 1280×720 和一个手机视口下都看起来正确。
5. **主动重组：** 如果修改会导致溢出，自动拆分内容并告知用户。不要等用户要求后再处理。

**在现有幻灯片中添加图片时：** 先把图片移到新幻灯片，或先减少其他内容。不要在未确认现有内容是否已经填满 1920×1080 舞台时就添加图片。

---

## 阶段 1：内容发现（新建演示文稿）

**一次性询问所有问题**，让用户一次性填写完。如果当前环境提供原生结构化问题界面，就使用它；否则用一条简洁消息一次性提问，并使用清晰编号的选择：

**问题 1 — 目的**（标题："Purpose"）:
这个演示文稿是为了什么？选项：路演稿 / 教学教程 / 会议演讲 / 内部汇报

**问题 2 — 长度**（标题："Length"）:
大约有多少张幻灯片？选项：短 5-10 / 中 10-20 / 长 20+

**问题 3 — 内容**（标题："Content"）:
你是否已经有内容了？选项：内容已准备好 / 粗略笔记 / 只有主题

**问题 4 — 密度**（标题："Density"）:
演示文稿应该有多密？选项：

- "Low density / speaker-led" — 大思想、少文字、更多留白
- "High density / reading-first" — 更自包含的细节，适合异步阅读

**阶段 1 不要询问行内编辑。** 用户在看到草稿前不应该先选择编辑行为。行内编辑是草稿后的附加能力：默认包含，除非用户明确要求锁定/仅导出文件。

记住用户的密度选择。它会影响幻灯片数量、排版尺度、每张幻灯片文字量、版式密度，以及更偏向电影式讲述幻灯片还是自包含阅读幻灯片。

如果用户已有内容，就请他们分享。

### 第 1.2 步：图片评估（如果提供了图片）

如果用户选择了“无图片” → 跳到阶段 2。

如果用户提供了图片文件夹：

1. **扫描** — 列出所有图片文件（.png、.jpg、.svg、.webp 等）
2. **检查每张图片** — 使用代理可用的图像理解能力。如果图像读取不可用，就使用文件名/元数据，并仅在必要时向用户询问说明
3. **评估** — 对每张图片说明它展示了什么、是否可用（以及原因）、它代表什么概念、主要颜色是什么
4. **共同设计大纲** — 精选图片会与文字一起影响幻灯片结构。这不是“先计划幻灯片，再添加图片”——而是从一开始就同时围绕两者进行设计（例如 3 张截图 → 3 张功能幻灯片，1 个 Logo → 标题页/结尾页）
5. **确认大纲**：如有可能，使用相同的结构化问题机制进行确认："Does this slide outline and image selection look right?" 选项：Looks good / Adjust images / Adjust outline

**预览中的 Logo：** 如果识别到可用的 Logo，就将其以 base64 嵌入到阶段 2 的每个样式预览中——用户会看到他们的品牌以三种不同方式呈现。

---

## 阶段 2：风格发现

**这是“展示胜于解释”的阶段。** 大多数人无法用语言准确表达设计偏好。

### 第 2.0 步：直接生成 3 个风格预览

基于用途、受众、情绪和内容密度，生成 3 个不同的单张幻灯片 HTML 预览，展示字体、颜色、动画和整体审美。

不要询问用户是否需要选项或预设选择器。默认的探索体验始终是视觉对比。

如果用户已经给出风格线索，就使用它；如果没有，就根据场合、受众、内容和 stakes 推断可能的情绪。保持选项足够多样，让用户能够通过视觉反应，而不需要提前表达品味。

如果用户明确指定了预设或加粗模板，就把它作为一个选项，并围绕它生成其余预览槽位。

阅读 [STYLE_PRESETS.md](STYLE_PRESETS.md) 以获取安全的预设候选。如果 [bold-template-pack/selection-index.json](bold-template-pack/selection-index.json) 存在，也读取这个紧凑索引，但暂时不要读取任何 `design.md` 文件。

| 情绪 | 推荐预设 |
| ------------------- | -------------------------------------------------- |
| 震撼/自信 | Bold Signal, Electric Studio, Dark Botanical |
| 兴奋/充满活力 | Creative Voltage, Neon Cyber, Split Pastel |
| 平静/专注 | Notebook Tabs, Paper & Ink, Swiss Modern |
| 灵感/感动 | Dark Botanical, Vintage Editorial, Pastel Geometry |

**预览组合规则：**

- 默认生成 3 个预览：1 个来自 `STYLE_PRESETS.md` 的安全预设，至少 1 个来自 `bold-template-pack/selection-index.json` 的加粗模板，以及 1 个 wildcard。
- wildcard 可以是第二个加粗模板，也可以是自生成的自定义设计。选择最能为用户的场合、受众、情绪和内容创造最强对比的那个。
- 不要强迫每个富有表现力的选项都来自模板库。如果简报具有比现有模板更清晰、更具体的设计机会，就用 wildcard 槽位自由设计。
- 对于保守或高风险的演示文稿，让安全预设显得特别克制；选择一个更正式的加粗模板；将 wildcard 设计为另一个克制的模板，或者一个看起来权威而非装饰性的自定义设计。
- 对于富有表现力的演示文稿，让安全预设作为可读的后备；选择一个强烈的加粗模板；将 wildcard 设计为大胆、具有情境感且与另外两个预览明显不同的方案。
- 如果加粗模板的匹配度较弱，就使用 wildcard 作为自定义设计，或者回退到另一个安全预设，而不是勉强使用模板。

**自定义 wildcard 设计规则：**

- 遵循上文的“设计审美”部分：不要使用通用的“AI 垃圾感”，不要使用默认字体/颜色/版式选择，不要使用白底紫渐变的陈词滥调，也不要使用像仪表盘/卡片那样的模板化设计。
- 与用户声明的场合、受众、情绪/气质和内容密度相匹配。自定义设计应该是为这份演示文稿量身打造的，而不只是“好看”。
- 形成清晰的视觉主张：独特的排版、明确调色、可识别的布局系统，以及一个强烈的氛围或图形元素。
- 保证它适合完整演示文稿。预览必须暗示一个可以扩展为章节、内容、引述、对比和收尾页的设计系统。
- 使用固定的 1920×1080 舞台规则，并通过与其他选项相同的预览真实性检查。
- 永远不要在幻灯片上渲染 "custom"、"wildcard"、"AI-generated" 或设计流程标签。

**加粗模板选择规则：**

- 根据 `mood`、`tone`、`best_for`、`avoid_for`、`formality`、`density` 和 `scheme`，将用户目的与情绪相匹配。
- 将 `best_for` 视为软信号，而不是严格的行业过滤条件。
- 保持三个预览彼此真正不同。
- 选出候选加粗模板后，只阅读这些候选模板中 `preview.md` 文件中的内容，读取位置来自 selection index 中的 `preview_md` 路径。
- 仅将 `preview.md` 用于标题页预览。不要在用户选定最终模板前读取完整的 `design.md` 文件。
- 除非最终选择的 `design.md` 缺少关键实现细节，否则不要读取或复制 `template.html`。

**预览真实性规则（不可妥协）：**

- 每个样式预览都必须看起来像用户演示文稿中的真正第一张幻灯片，而不是诊断卡片。
- 不要在幻灯片上渲染内部工作流文本：不要出现 `preview`、`generated from`、`preview.md`、`template`、`preset`、`style option`、`Option A/B/C`、文件名、路径或源文档标签。
- 不要在幻灯片上渲染模板名或 slug 名。模板/样式名称只出现在发给用户的消息中。
- 不要把用户需求说明作为幻灯片内容，例如 "sharp and provocative"、"safe option"、"bold option"、"for internal sharing" 或 "audience: ..."，除非用户明确希望这些措辞出现在演示文稿中。
- 如果幻灯片需要边框或控件，请使用真实的演示文稿控件：演示文稿标题、章节标题、日期、作者、公司、页码，或用户材料中的真实内容短语。
- 在打开预览前，先检查可见文本，如果有任何内部元数据，就进行修改。

将预览保存到 `.frontend-slides/slide-previews/`（`style-a.html`、`style-b.html`、`style-c.html`）。每个文件都应是自包含且紧凑的，展示一张带动画的标题页。

自动为用户打开每个预览。

### 第 2.1 步：用户选择

提问（标题："Style"）：
你更喜欢哪一个风格预览？选项：Style A: [名称] / Style B: [名称] / Style C: [名称] / Mix elements

如果选择 "Mix elements"，再询问具体细节。

---

## 阶段 3：生成演示文稿

使用阶段 1 的内容（文字，或文字 + 精选图片）和阶段 2 的风格，生成完整演示文稿。

如果提供了图片，阶段 1.2 的大纲已经将其纳入设计；如果没有图片，CSS 生成的视觉效果（渐变、形状、图案）也能提供视觉吸引力——这是一条完全受支持的一等路径。

在整个演示文稿中应用用户的密度选择：

- **低密度 / 以讲述为主：** 使用更多幻灯片、每张更少信息。优先使用大标题、短语、视觉隐喻、章节节奏、引述/陈述页，以及更适合演讲者的节奏。
- **高密度 / 以阅读为主：** 让每张幻灯片更自包含。使用结构化网格、对比表格、带注释的图表、说明文字和简洁解释。保持层级清晰，使它看起来像精心设计，而不是把文档直接贴到幻灯片上。

如果用户的需求是混合型，就选择更接近的一种模式，而不是发明中间方案：现场说服观众默认采用低密度；异步传播或详细审阅默认采用高密度。

不要让高密度变成视觉杂乱。如果某张高密度幻灯片开始溢出，就拆分或重新设计成更清晰的结构。

如果用户选择了 `bold-template-pack` 中的加粗模板，在生成前先读取该模板完整的 `design.md`。不要读取其他加粗模板。把 `design.md` 当作设计配方：

- 保留它的字体、调色板、装饰语汇、间距节奏和组件语法。
- 无论源模板最初使用的是 `deck-stage.js` 还是 viewport-fluid CSS，都将最终演示文稿生成为固定的 1920×1080 舞台，并统一缩放到视口。
- 将 `design.md` 中的 viewport-fluid 数值视为设计比例，转化为 1920×1080 舞台坐标。不要把它们保留为最终演示文稿中的实时视口重排规则。
- 输出为单个自包含的 Frontend Slides HTML 文件。
- 不要复制演示示例内容，也不要过度模仿源模板。
- 只有在所选模板的 `design.md` 缺少关键实现细节时，才把 `template.html` 作为最后的实现参考。
- 生成后，验证渲染结果中的内容溢出和面板重叠。仅靠 `scrollHeight` 检查并不够，因为网格面板可能彼此覆盖。

如果用户选择了自生成的自定义 wildcard，就把该预览的 CSS 和版式视为设计配方：

- 保留它的字体、调色板、装饰语汇、间距节奏、网格逻辑和组件语法。
- 将同样的视觉系统扩展到整个演示文稿。用户一旦选择了自定义方向，就不要切换回预设或加粗模板。
- 从该系统中设计缺失的幻灯片版式，而不是从其他风格中引入模式。
- 保持输出为固定舞台、单文件，并像其他演示文稿一样进行视觉验证。

**生成前，先阅读这些辅助文件：**

- [html-template.md](html-template.md) — HTML 结构和 JS 功能
- [viewport-base.css](viewport-base.css) — 必需的 CSS（需完整包含）
- [animation-patterns.md](animation-patterns.md) — 适配所选情绪的动画参考

**关键要求：**

- 单个自包含的 HTML 文件，所有 CSS/JS 均内联
- 在 `<style>` 块中包含 `viewport-base.css` 的完整内容
- 使用 Fontshare 或 Google Fonts 字体 —— 不要使用系统字体
- 为每个部分添加详细注释
- 每个部分都需要清晰的 `/* === SECTION NAME === */` 注释块

---

## 阶段 4：PPT 转换

在转换 PowerPoint 文件时：

1. **提取内容** — 运行 `python scripts/extract-pptx.py <input.pptx> <output_dir>`（如需要，先安装 `python-pptx`：`pip install python-pptx`）
2. **与用户确认** — 展示提取到的幻灯片标题、内容摘要和图片数量
3. **风格选择** — 进入阶段 2 进行风格发现
4. **生成 HTML** — 按所选风格转换，同时保留所有文字、图片（来自 assets/）、幻灯片顺序和演讲备注（以 HTML 注释形式）

---

## Phase 5: Delivery

1. **Clean up** — Delete `.frontend-slides/slide-previews/` if it exists
2. **Open** — Use `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - File location, style name, slide count
   - Navigation: Arrow keys, Space, swipe/tap if enabled
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - Inline text editing is available: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save
   - Offer the natural post-draft actions: ask for revisions, edit text directly in the browser, or export/share

---

## Phase 6: Share & Export (Optional)

After delivery, **ask the user:** _"Would you like to share this presentation? I can deploy it to a live URL (works on any device including phones) or export it as a PDF."_

Options:

- **Deploy to URL** — Shareable link that works on any device
- **Export to PDF** — Universal file for email, Slack, print
- **Both**
- **No thanks**

If the user declines, stop here. If they choose one or both, proceed below.

### 6A: Deploy to a Live URL (Vercel)

This deploys the presentation to Vercel — a free hosting platform. The link works on any device (phones, tablets, laptops) and stays live until the user takes it down.

**If the user has never deployed before, guide them step by step:**

1. **Check if Vercel CLI is installed** — Run `npx vercel --version`. If not found, install Node.js first (`brew install node` on macOS, or download from https://nodejs.org).

2. **Check if user is logged in** — Run `npx vercel whoami`.
   - If NOT logged in, explain: _"Vercel is a free hosting service. You need an account to deploy. Let me walk you through it:"_
     - Step 1: Ask user to go to https://vercel.com/signup in their browser
     - Step 2: They can sign up with GitHub, Google, email — whatever is easiest
     - Step 3: Once signed up, run `vercel login` and follow the prompts (it opens a browser window to authorize)
     - Step 4: Confirm login with `vercel whoami`
   - Wait for the user to confirm they're logged in before proceeding.

3. **Deploy** — Run the deploy script:

   ```bash
   bash scripts/deploy.sh <path-to-presentation>
   ```

   The script accepts either a folder (with index.html) or a single HTML file.

4. **Share the URL** — Tell the user:
   - The live URL (from the script output)
   - That it works on any device — they can text it, Slack it, email it
   - To take it down later: visit https://vercel.com/dashboard and delete the project
   - The Vercel free tier is generous — they won't be charged

**⚠ Deployment gotchas:**

- **Local images/videos must travel with the HTML.** The deploy script auto-detects files referenced via `src="..."` in the HTML and bundles them. But if the presentation references files via CSS `background-image` or unusual paths, those may be missed. **Before deploying, verify:** open the deployed URL and check that all images load. If any are broken, the safest fix is to put the HTML and all its assets into a single folder and deploy the folder instead of a standalone HTML file.
- **Prefer folder deployments when the presentation has many assets.** If the presentation lives in a folder with images alongside it (e.g., `my-deck/index.html` + `my-deck/logo.png`), deploy the folder directly: `bash scripts/deploy.sh ./my-deck/`. This is more reliable than deploying a single HTML file because the entire folder contents are uploaded as-is.
- **Filenames with spaces work but can cause issues.** The script handles spaces in filenames, but Vercel URLs encode spaces as `%20`. If possible, avoid spaces in image filenames. If the user's images have spaces, the script handles it — but if images still break, renaming files to use hyphens instead of spaces is the fix.
- **Redeploying updates the same URL.** Running the deploy script again on the same presentation overwrites the previous deployment. The URL stays the same — no need to share a new link.

### 6B: Export to PDF

This captures each slide as a screenshot and combines them into a PDF. Perfect for email attachments, embedding in documents, or printing.

**Note:** Animations and interactivity are not preserved — the PDF is a static snapshot. This is normal and expected; mention it to the user so they're not surprised.

1. **Run the export script:**

   ```bash
   bash scripts/export-pdf.sh <path-to-html> [output.pdf]
   ```

   If no output path is given, the PDF is saved next to the HTML file.

2. **What happens behind the scenes** (explain briefly to the user):
   - A headless browser opens the presentation at 1920×1080 (standard widescreen)
   - It screenshots each slide one by one
   - All screenshots are combined into a single PDF
   - The script needs Playwright (a browser automation tool) — it will install automatically if missing

3. **If Playwright installation fails:**
   - The most common issue is Chromium not downloading. Run: `npx playwright install chromium`
   - If that fails too, it may be a network/firewall issue. Ask the user to try on a different network.

4. **Deliver the PDF** — The script auto-opens it. Tell the user:
   - The file location and size
   - That it works everywhere — email, Slack, Notion, Google Docs, print
   - Animations are replaced by their final visual state (still looks great, just static)

**⚠ PDF export gotchas:**

- **First run is slow.** The script installs Playwright and downloads a Chromium browser (~150MB) into a temp directory. This happens once per run. Warn the user it may take 30-60 seconds the first time — subsequent exports within the same session are faster.
- **Slides must use `class="slide"`.** The export script finds slides by querying `.slide` elements. If the presentation uses a different class name, the script will report "0 slides found" and fail. All presentations generated by this skill use `.slide`, so this only matters for externally-created HTML.
- **Local images must be loadable via HTTP.** The script starts a local server and loads the HTML through it (so Google Fonts and relative image paths work). If images use absolute filesystem paths (e.g., `src="/Users/name/photo.png"`) instead of relative paths (e.g., `src="photo.png"`), they won't load. Generated presentations always use relative paths, but converted or user-provided decks might not — check and fix if needed.
- **Local images appear in the PDF** as long as they are in the same directory as (or relative to) the HTML file. The export script serves the HTML's parent directory over HTTP, so relative paths like `src="photo.png"` resolve correctly — including filenames with spaces. If images still don't appear, check: (1) the image files actually exist at the referenced path, (2) the paths are relative, not absolute filesystem paths like `/Users/name/photo.png`.
- **Large presentations produce large PDFs.** Each slide is captured as a full 1920×1080 PNG screenshot. An 18-slide deck can produce a ~20MB PDF. If the PDF exceeds 10MB, ask the user: _"The PDF is [size]. Would you like me to compress it? It'll look slightly less sharp but the file will be much smaller."_ If yes, re-run the export with the `--compact` flag:
  ```bash
  bash scripts/export-pdf.sh <path-to-html> [output.pdf] --compact
  ```
  This renders at 1280×720 instead of 1920×1080, typically cutting file size by 50-70% with minimal visual difference.

---

## Supporting Files

| File                                               | Purpose                                                              | When to Read              |
| -------------------------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| [STYLE_PRESETS.md](STYLE_PRESETS.md)               | 12 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [bold-template-pack/selection-index.json](bold-template-pack/selection-index.json) | Compact bold template metadata for candidate selection | Phase 2 (style selection) |
| [bold-template-pack/templates/*/preview.md](bold-template-pack/templates/) | Lightweight style cards for shortlisted bold title previews | Phase 2 after shortlisting |
| [bold-template-pack/templates/*/design.md](bold-template-pack/templates/) | Detailed design-system docs for the selected bold template only | Phase 3 after user selection |
| [viewport-base.css](viewport-base.css)             | Mandatory fixed-stage CSS — copy into every presentation             | Phase 3 (generation)      |
| [html-template.md](html-template.md)               | HTML structure, JS features, code quality standards                  | Phase 3 (generation)      |
| [animation-patterns.md](animation-patterns.md)     | CSS/JS animation snippets and effect-to-feeling guide                | Phase 3 (generation)      |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction                             | Phase 4 (conversion)      |
| [scripts/deploy.sh](scripts/deploy.sh)             | Deploy slides to Vercel for instant sharing                          | Phase 6 (sharing)         |
| [scripts/export-pdf.sh](scripts/export-pdf.sh)     | Export slides to PDF                                                 | Phase 6 (sharing)         |
