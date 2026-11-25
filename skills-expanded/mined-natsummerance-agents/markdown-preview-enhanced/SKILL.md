---
name: markdown-preview-enhanced
description: |
  Markdown 渲染预览增强（VSCode 扩展 Markdown Preview Enhanced 的使用知识）：编辑器内实时预览 .md，
  滚动同步、KaTeX/MathJax 数学排版、mermaid/PlantUML/GraphViz/Vega 等图表渲染、代码块执行（code chunk）、
  reveal.js 演示模式、pandoc/PDF 多格式导出、@import 文件嵌入与自定义 CSS。
  当用户写带公式/图表/可执行代码块的 Markdown 笔记或文档、问「怎么在 VSCode 预览 md」「md 怎么导出 PDF/
  做幻灯片」时使用。
  不适用于：把内容交给 AI 生成设计感成品 HTML 页面（转 agentic-html-editor）。
source_project: shd101wyy/markdown-preview-enhanced
tags: [markdown-preview-enhanced, markdown, vscode, mathjax, mermaid, pandoc, 蒸馏技能]
---

# Markdown Preview Enhanced · Markdown 渲染预览增强

## R (Reading) — 上游原文

> "Markdown Preview Enhanced is an extension that provides you with many useful functionalities such as automatic scroll sync, math typesetting, mermaid, PlantUML, pandoc, PDF export, code chunk, presentation writer, etc."
>
> — 上游 README.md（shd101wyy__markdown-preview-enhanced）

上游 docs/code-chunk.md 对可执行代码块给出格式与警告：「You can configure code chunk options in format of ```lang {cmd=your_cmd opt1=value1 …}」以及「⚠️ Script execution is off by default and needs to be explicitly enabled… Your machine can get hacked if someone makes you open a markdown with malicious code while script execution is enabled.」

docs/presentation.md 说明演示模式：「Markdown Preview Enhanced uses reveal.js to render beautiful presentations.」通过 front-matter 的 `presentation:` 节配置尺寸与主题，用 `<!-- slide -->` 注释分页。

## I (Interpretation) — 方法论骨架

1. **预览即工作台**：ctrl+shift+m 开关预览，默认 live update 边写边渲染；ctrl+shift+s 双向滚动同步让长文档源码与预览位置互跳；esc 呼出侧边 TOC。写作侧的「所见即所得」由它承担，不改变 .md 本身。
2. **数学双引擎**：KaTeX 快但功能子集少，MathJax 全但慢；行内 `$...$`/`\(...\)`、块级 `$$...$$`/`\[...\]` 或 ```math 围栏；引擎与定界符都可在扩展设置里切换，MathJax 配置可用命令面板打开调整。
3. **图表即代码块**：mermaid（三套主题 + 可编辑 init config 与 icon packs）、PlantUML、WaveDrom、GraphViz、Vega/Vega-lite、Ditaa 直接用围栏语法声明渲染；注意部分图表在 PDF/pandoc 导出时表现不佳。
4. **Code Chunk 是可编程文档**：```bash {cmd} / ```python {cmd=true matplotlib=true} 等写法让代码块真正执行并把输出（html/markdown/text/png/none）回填预览；支持 args、stdin、hide、continue=id 跨块续接、$input_file 宏、run_on_save；shift-enter 跑当前块、ctrl-shift-enter 全跑。
5. **演示模式复用同一份 md**：front-matter 的 presentation: 节配置宽高/主题，`<!-- slide -->` 注释分页，底层是 reveal.js——一份笔记同时是讲稿。
6. **导出走三条路**：推荐 Chrome(Puppeteer) 打印 PDF（或浏览器打开手动打印、Prince）；pandoc 导出 docx/beamer/rtf 及参考文献；微信导出适配公众号。导出前可用 Customize Css 的 style.less 定制打印样式。
7. **文件引用与图片流**：@import "file"（兼容 ![]() 与 ![[wikilink]] 语法）把外部文件并入渲染并带缓存刷新按钮；Image Helper 支持粘贴/快速插入/上传图床（imgur、sm.ms），上传记录存 image_history.md。
8. **安全默认关闭执行**：enableScriptExecution 默认 false，打开恶意 md 即执行任意命令是真实风险面；教用户开此选项时必须同时说明风险。

## A1 (Past Application) — 源项目典型应用

### 案例: 数学讲义边写边校
- **输入**: 含大量公式的课程讲义 Markdown
- **做法**: ctrl+shift+m 开预览，行内/块级定界符写公式，KaTeX 引擎即时渲染，滚动同步对照源码修改
- **结果**: 写作与校对同屏完成，无需反复编译 LaTeX 才能看效果

### 案例: 带可执行实验的实验记录
- **输入**: 数据分析笔记，内嵌 python 绘图与 shell 统计命令
- **做法**: 代码块加 {cmd=true}（matplotlib=true 内联图像），shift-enter 逐块执行，hide 隐藏代码只留输出，continue=id 让清洗与绘图共享状态
- **结果**: 文档本身成为可重跑的 notebook 式报告，输出随代码更新

### 案例: 同一份 md 出幻灯与 PDF
- **输入**: 组会汇报提纲
- **做法**: 加 presentation front-matter 与 `<!-- slide -->` 分页走 reveal.js 演示；同一文件再经 Puppeteer 导出 PDF 存档
- **结果**: 一份源文件两种交付形态，维护成本减半

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 在 VSCode 里写含数学公式/图表/表格的技术笔记或论文草稿，要求实时预览
2. 想让 Markdown 里的代码块真的能跑并把结果留在文档里（notebook 式写作）
3. 要把手头 md 导出成 PDF/Word/Beamer 幻灯或直接变 reveal.js 演示

### 语言信号
- "VSCode 里怎么实时预览 markdown 的数学公式"
- "我想让 md 里的 python 代码块运行并显示图"
- "这份 markdown 怎么导出 PDF / 转成幻灯片"
- "mermaid 流程图在 markdown 里怎么画出来"
- "笔记里的 @import 引用别的 md 文件没生效"

### 与同 agent 兄弟 skill 的区分
- 与 `agentic-html-editor` 的区别一句话：本 skill 是**写作者侧的渲染预览增强**（忠实呈现你写的 md，附公式/图表/代码执行/导出），agentic-html-editor 是**读者侧的 AI 成品生成**（按设计模板产出可直接分发的 HTML 页面）。

## E (Execution) — 可执行步骤

1. **确认写作场景** — 完成标准: 明确文档类型（笔记/讲义/实验记录/汇报）与其依赖能力（数学/图表/code chunk/导出目标）
2. **开启预览与同步** — 完成标准: ctrl+shift+m 预览已打开，live update 或保存触发模式已按用户习惯设定，长文档启用滚动同步
3. **装配所需渲染器** — 完成标准: 数学引擎已选定（KaTeX/MathJax）；mermaid/PlantUML 等围栏渲染正常出图；外部依赖（如 PlantUML 需本地服务、LaTeX 编译需 pdf2svg+引擎）已检查
4. **编写与验证 code chunk** — 完成标准: 用户明确知情后 enableScriptExecution 才开启；chunk 参数（cmd/output/hide/continue）符合 docs 语法且试运行通过
5. **组织结构化元素** — 完成标准: TOC 已生成、@import 引用的外部文件路径有效、图片经 Image Helper 就位且 image_history.md 记录一致
6. **按需导出** — 完成标准: 目标格式管线跑通（Puppeteer PDF/pandoc docx/reveal.js 演示），已知限制核对过（部分图表与 code chunk 不兼容 ebook/pandoc 导出），产物打开验收

## B (Boundary) — 边界

### 不适用场景
- 让 AI 按设计模板生成面向读者的成品 HTML（公众号排版、落地页、海报）→ 转 `agentic-html-editor`
- 需要 WYSIWYG 富文本编辑器或 Notion 类块编辑体验的场景——本 skill 只做源码模式的预览增强
- 非 VSCode/Atom 生态的纯静态站点构建（Hugo/Hexo 渲染管线另有工具链）
- 团队协作文档平台（语雀/Notion/飞书文档）内的公式图表渲染——那些平台有各自的内置方案

### 已知局限 / 失败模式
- 上游仓库仅承载文档，VSCode 扩展源码已迁至 shd101wyy/vscode-markdown-preview-enhanced，issue 与版本查询应去新仓库
- code chunk 不兼容 ebook 导出，且在 pandoc 导出中可能有 bug；部分图表（mermaid/PlantUML 等）在 PDF/pandoc 导出时渲染不佳
- LaTeX/TikZ、gnuplot、erd 等 chunk 依赖本机安装对应程序，缺依赖时报错而非自动降级
- KaTeX 与 MathJax 能力面不同：切换引擎后个别公式宏可能从可渲染变为不支持，长文档换引擎前应全文预览核对

## 相关 skills

- contrasts-with: agentic-html-editor（写作者侧 md 实时预览 vs 读者侧 AI 成品 HTML 生成）
- composes-with: agentic-html-editor（MPE 里校对完稿子 → 兄弟 skill 接手出分发版式）

---

## 审计信息

- **验证**: V1 ✓（README.md 与 docs/usages.md、code-chunk.md、diagrams.md、math.md、presentation.md 在功能清单与快捷键上互证）/ V2 ✓（可回答「KaTeX 和 MathJax 怎么选」「code chunk 如何跨块续接」「为什么脚本执行默认关闭」等新问题）/ V3 ✓（code chunk 参数协议、presentation front-matter、三条导出路线是非常识性工作流）
- **蒸馏时间**: 2026-08-25
- **来源文件清单**: vendor/shd101wyy__markdown-preview-enhanced/{README.md, docs/usages.md, docs/code-chunk.md, docs/diagrams.md, docs/math.md, docs/presentation.md, docs/file-imports.md, docs/pdf.md}
