---
name: html-artifact
description: Build self-contained HTML files to explain, plan, or review.
version: 1.0.0
author: Anthropic (html-effectiveness gallery, MIT), adapted for Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [html, artifact, explainer, plan, report, code-review, diagram, svg, design, prototype, editor]
    related_skills: [claude-design, popular-web-designs, design-md, excalidraw, p5js]
---

# HTML文档生成技能

当需要生成供人*阅读、分享或交互操作*的文档时——比如概念说明、实施计划、状态/事故报告、代码审查指南、技术或教学用图表、多种设计方案，或是能将结果导出给用户的简易编辑器——该技能可自动生成一个独立的`.html`文件。无需构建步骤、无需依赖项、也无需使用CDN。

一旦文档需要颜色、布局、图表、表格、代码或交互功能，HTML便比Markdown更具优势。它能在任何浏览器中打开，可通过链接分享，即使内容超过100行仍保持可读性，还能承载Markdown无法处理的SVG图表和实时控件。当用户要求“生成HTML文件/文档”，或请求*解释X的工作原理*、*撰写计划/拉取请求/报告*、*绘制图表*、*对比不同选项*，或是*设计交互原型*时——即便用户没有明确提到“HTML”，也应默认使用此技能生成HTML格式的文档。

## 该技能的诞生背景（及其替代了哪些技能）

该技能**取代了**之前的三种技能：`sketch`（用于生成多版本简易HTML原型）、`architecture-diagram`（用于生成深色科技风格的基础设施SVG图）以及`concept-diagrams`（用于生成教学用SVG图）。将它们整合为一个技能是有明确原因的：这三种技能最终生成的*都是同一类文档*——即包含内联CSS和SVG的独立HTML文件——且功能高度重叠（三种“图表”技能、两种“对比方案”路径，还不存在统一的标记系统）。将其合并为一个可切换模式的技能，既消除了“该用哪个技能”的困惑，让所有输出都保持统一的设计风格，又保留了每个技能的独特优势：`sketch`的精确度调节功能与验证机制、`architecture-diagram`的深色基础设施视觉风格，以及`concept-diagrams`的九级教育色彩体系与原型库。

此次整合对系统资源的影响极小：该技能**没有任何依赖项**（无需Node、FFmpeg、Chromium或pip包——它直接生成纯HTML/CSS/SVG文件），因此即便在原本`concept-diagrams`为可选功能的场景中，它也以*默认启用*的形式被集成进来。唯一始终存在的开销只是该技能的一行描述文字，所有参考资料、模板和示例库都会按需加载。`concept-diagrams`之所以是可选的，是因为其应用场景较为小众，并非因为安装成本高——将其升级为通用型、无依赖的集成技能，才是最适合它的归宿。那些需要实际安装复杂工具才能实现的图表功能（例如`hyperframes`：需Node、FFmpeg和Chromium）则仍被保留为可选功能，不会被合并进来。

在以下场景应使用其他技能：需要匹配特定品牌的设计风格→`popular-web-designs`；需要正式的设计标记规范文件→`design-md`；需要设计风格本身即为核心要素的定制化视觉文档→`claude-design`；需要手绘或白板风格的`.excalidraw`文件→`excalidraw`；需要生成动态画布艺术→`p5js`。其余所有可生成为可阅读、可分享的HTML页面的内容，都适合使用此技能。

## 参考文件（按需加载）

- `references/house-style.md`——标准的`:root`标记块、类型系统，以及卡片/表格/提示框/代码块等元素的样式规范。**在创建任何文档之前，请先阅读此文件。**
- `references/examples.md`——20个完整的参考HTML文件（来自Anthropic的html-effectiveness示例库及MIT资源），按不同模式分类，并附有加载这些文件的脚本。可根据任务需求选择相应的文件，通过完整示例来调整文档的设计风格。
- `references/svg-diagrams.md`——手动编写的内联SVG代码：箭头标记、节点组、决策菱形、边关系定义以及坐标网格规范。用于创建流程图、架构图或概念图时参考。
- `references/concept-archetypes.md`——九级教育色彩体系，以及一系列图表原型库（时间轴、树状图、象限图、分层堆叠图、前后对比图、中心辐射图、横截面图）。用于创建教育类或非软件相关的可视化内容时参考。
- `references/dark-tech.md`——深色“基础设施”风格标记变体（保留了旧版`architecture-diagram`的视觉风格）。用于创建云服务/基础设施/系统架构图时参考。
- `references/throwaway-editors.md`——简易编辑器的实现方案，以及能在`file://`协议下正常使用的复制到剪贴板导出功能。当需要生成能将状态反馈给提示词的交互式编辑器时参考。
- `references/fidelity-and-verify.md`——简易版本与演示版之间的精确度调节功能、多版本对比布局，以及强制性的浏览器视觉验证流程。

## 模板

- `templates/base.html`——包含统一设计风格`<style>`块的文档框架。
- `templates/diagram.html`——双模式图表容器（支持浅色教育风格和深色基础设施风格CSS，包含箭头标记、节点/边类）。在指定位置插入您的SVG文件即可。
- `templates/editor.html`——简易编辑器的基本结构（状态处理→渲染→导出）。

可通过`skill_view(name="html-artifact", file_path="templates/base.html")`命令加载相应模板。

## 工作流程

1. **选择模式**：根据需求匹配对应的文档类型——说明文、计划书、报告、代码审查内容、图表、多种设计方案或编辑器。模式决定了应使用哪种模板、参考哪些资料，以及以哪个示例作为参考。
2. **每次都先阅读匹配的示例**：html-effectiveness示例库中的20个文件是该技能的核心参考依据；文字描述虽能介绍这些示例，但完整示例所呈现的内容密度、排版间距和结构，是任何总结都无法替代的。在开始编写任何内容之前，请先阅读相关示例。
   ```
   terminal: bash scripts/fetch-examples.sh      # idempotent: clones if missing, else pulls
   read_file references/examples/<file-for-your-mode>.html
   ```
`references/examples.md` 中列出了各模式对应的文件映射关系（例如代码审查对应 `03-code-review-pr.html`，流程图对应 `13-flowchart-diagram.html`，编辑器相关内容对应 `18-editor-triage-board.html`）。请至少阅读与你的任务最相关的那个示例；如果需要结合多种模式，则阅读两个示例。仅当真正出现获取失败（无网络连接）时，才可仅参考精简后的模式参考资料——请注意，此时你是在没有示例辅助的情况下进行操作。

3. **确定呈现精度。** 是用于临时探索的简易版本，还是用于正式展示的高质量成果？请参阅 `references/fidelity-and-verify.md`。无需对快速生成的对比内容过度美化，也绝不能提交粗制滥造的报告。

4. **从模板与统一风格开始。** 加载 `templates/base.html`（或 `diagram.html`/`editor.html`）以及 `references/house-style.md`。复用 `:root` 定义的色彩变量——切勿为每个文件单独创建新的配色方案。参照第2步中阅读过的示例结构进行编写，根据实际内容进行调整，而非直接复制。

5. 使用 `write_file` 函数来生成最终文件。所有样式需内联处理：在 `<head>` 中放置一个 `<style>` 标签，在 `</body>` 之前最多放置一个 `<script>` 标签。禁止使用 `<link>` 标签，不得引入外部字体（应使用操作系统自带的字体栈），不可使用 CDN，也不能通过 `<img src>` 引用远程URL的图片。所有图形都应为内联SVG或CSS格式。

6. 尽量避免使用JavaScript，并确保其存在时仍能保持良好表现。首选不使用任何JavaScript。若确实需要，应将其限制为小型原生IIFE函数，且即便关闭JavaScript，页面也应能正常显示核心内容（如原生的 `<details>` 组件、锚点导航、默认激活的标签页/节点等）。

7. 进行视觉验证。打开文件并截取屏幕截图——相关验证流程可见于 `references/fidelity-and-verify.md`。对于SVG图表而言，此步骤是必做的，因为手动设置的坐标在内容修改后可能会发生变化（如节点重叠、箭头方向错误）。

8. 告知用户文件的绝对路径，以便其直接打开文件。同时可说明是否存在交互控件或导出按钮。

## 核心原则

**统一的设计系统，基于token驱动。** 主色调为暖米色（`--ivory`），接近黑色的墨水色为 `--slate`，点缀色为赤陶色（`--clay`），成功或新增内容用橄榄绿表示，整体采用渐变的暖灰色调。所有模式均遵循相同的语义规范：**赤陶色代表焦点/需关注的内容，橄榄绿代表成功/新增内容，铁锈色代表错误/已删除内容，燕麦色代表中性填充色，灰度500号色代表次要文本及箭头**。颜色引用时必须以 `var(--…)` 的形式出现。

**按功能区分三种字体。** 标题使用衬线字体（Georgia系列），正文使用无衬线字体（system-ui），所有标签、代码、数值、辅助线及路径则使用等宽字体。所有字体均为操作系统自带的，无需额外加载。这种“衬线标题+等宽标签+无衬线正文”的组合是该设计体系的标志性特征。

**始终保持自包含性。** 文件在双击后应能在离线状态下正常显示。样式与脚本需内联处理，图形应以内联SVG或CSS形式呈现，绝不能引用远程资源。这是不可妥协的要求——也只有这样，生成的文件才能真正实现共享。

**具备优雅的降级能力。** 优秀的输出成果通常无需JavaScript。即便需要交互功能（如滑块、拖拽、编辑器），页面也应在没有JavaScript的情况下仍能清晰传达内容；同时，从 `file://` 协议的页面中也能正常完成导出功能（相关备用方案见 `references/throwaway-editors.md`）。

**交互式成果应以导出功能作为结尾。** 临时使用的编辑器只有在其能将处理结果导出时才有价值——应提供“复制为Markdown”“复制为JSON”“复制差异内容”“复制提示语”等按钮，将当前状态序列化到剪贴板，以便用户粘贴到下一个提示中继续使用。

## 快速参考——模式与对应输出类型

| 请求类型 | 模式 | 模板文件 | 应阅读的示例 | 关键参考资料 |
|---|---|---|---|---|
| “解释X的工作原理” | 解释类 | base | `14-research-feature-explainer.html` | house-style, svg-diagrams |
| “撰写计划/需求规格” | 规划类 | base | `16-implementation-plan.html` | house-style |
| “状态报告/事件报告” | 报告类 | base | `11-status-report.html`, `12-incident-report.html` | house-style |
| “审查这个PR/代码差异” | 代码审查类 | base | `03-code-review-pr.html`, `17-pr-writeup.html` | house-style（差异部分） |
| “绘制架构图/流程图” | 基础设施图类 | diagram | `13-flowchart-diagram.html`, `04-code-understanding.html` | dark-tech, svg-diagrams |
| “绘制概念图/流程图”（科学、物理、教育领域） | 概念图类 | diagram | `13-flowchart-diagram.html`, `10-svg-illustrations.html` | concept-archetypes, svg-diagrams |
| “展示N种方案并对比选项” | 方案对比类 | base | `01-exploration-code-approaches.html`, `02-exploration-visual-designs.html` | fidelity-and-verify |
| “让我调整/筛选/编辑X并复制结果” | 编辑器类 | editor | `18-editor-triage-board.html`, `19-editor-feature-flags.html`, `20-editor-prompt-tuner.html` | throwaway-editors |

## 常见误区

- **切勿跳过示例参考。** 提升质量的最有效方法就是在编写之前先阅读对应的示例文件（可通过 `bash scripts/fetch-examples.sh` 获取，然后使用 `read_file references/examples/<file>.html` 打开）。文档中的文字说明只是映射关系，而示例才是实际参考范本。仅凭对“优质HTML样式的记忆”来创作，必然会导致输出内容变得千篇一律、缺乏特色。
- **切勿自行创建配色方案。** 应直接复用 `house-style.md` 中定义的 `:root` 颜色变量。为每个文件单独设置配色会破坏整体一致性，而这种一致性正是这些输出成果显得专业的原因。
- **切勿依赖外部库。** 禁止使用Mermaid、D3、Tailwind CDN、Prism或任何网页字体。图表需手动绘制为SVG格式，代码高亮需通过手动添加的 `<span>` 标签实现，颜色主题功能则由预定义的token块承担。
- **切勿忽视对图表的视觉检查。** 手动计算的SVG坐标是导致输出出错的最主要原因——比如箭头出现在空白区域、元素重叠、文本溢出等。在提交之前，务必先截图检查并修复这些问题。
- **若只需静态代码片段，无需添加JavaScript导出功能。** 对于仅包含单个代码片段的输出，直接使用可手动选择的代码块即可实现稳定的“导出”效果。
- **切勿让JavaScript承担展示内容的全部功能。** 如果文本内容仅存在于 `render()` 函数内部，那么关闭JavaScript后页面将一片空白。应将实际内容直接放在HTML中，利用JavaScript来增强显示效果，而非替代内容本身。
