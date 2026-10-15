---
name: yzr-md-to-html
description: |
  当用户想把一份本地 Markdown 文件 / 目录（README / 技术文档 / 笔记 / 论文草稿）转换成
  自包含、双击即可在浏览器打开的本地 HTML 文件时使用本 skill：默认深色阅读主题 + 侧边栏目录
  TOC + 离线代码高亮，公式 / Mermaid 按需挂 CDN，支持 `--template` 自定义模板。
  触发："把这个 README 转成好看的 HTML 发给同事" / "这份设计文档有公式和流程图，导出成能直接
  打开看的网页" / "把 notes/ 目录下的 .md 批量转成 html" / "转成 html 后用 agent-html-drop
  上传分享"。只要用户明确要"本地 .md → 自包含 HTML 文件"的单向转换——即使没提 skill 名，
  也务必使用本 skill。
  不适用：从零写网页 / 前端页面（走基础工具）、文档站 / 静态站点生成与部署发布（要托管上线
  的在线网页）、Markdown → PDF 或其它格式、HTML → Markdown 反向、实时预览 / 在线编辑器、
  上传到 Outline Wiki（走 yzr-outline-wiki）。
metadata:
  author: Zuoru YANG
  modify time: 2026-08-16
  category: document-conversion
---

把一份本地 Markdown 转成**自包含、双击即可在浏览器浏览**的 HTML 文件。默认套一套
**深色阅读主题**（GitHub-dark 风格，纯深色），自带侧边栏目录 TOC、离线代码
语法高亮（Pygments），并**按需**自动启用数学公式（KaTeX）与 Mermaid 图表——只有源文件
里真出现 `$` 或 mermaid 代码块才会挂对应 CDN，普通文档零额外网络请求。

## 何时不使用

"何时使用 / 不适用"已在 frontmatter description，正文不重抄。本节只补**出路**与**擦边负例**：

- **出路**：上传到 Outline Wiki → 走 `yzr-outline-wiki`（产物形态是 wiki 文档，不是本地 HTML）
- **擦边负例**："转成 html 后上传分享"仍属本 skill（转换 + 上传两段，上传走「上传产物」节）；
  但"搭文档站 / 部署上线"不是——本 skill 产物是本地文件，不生成站点、不做部署；"PDF /
  网页 → Markdown"反向转换同样不是（本 skill 只输出 HTML）

## 输入 / 输出

- **输入**：一个 `.md` 文件，或一个目录（批量转该目录下所有 `*.md`）
- **输出**：单个自包含 `.html`（CSS 与 Pygments 高亮全部内联；KaTeX / Mermaid 按需走 CDN）
- **参数与默认值以 `python3 scripts/md_to_html.py --help` 为单一来源**（argparse 定义，此处不
  重抄）：文件输入默认生成同名 `.html`；目录输入默认就地生成，`--title` 默认取首个 `#`
  一级标题再退回文件名

**自定义模板可用变量**（`--template` 传入的 Jinja2 模板里用，不在 `--help` 范围内）：
`{{ content }}`（正文 HTML）、`{{ toc }}`（目录 HTML）、`{{ styles }}`（默认主题 CSS）、
`{{ pygments_css }}`（代码高亮 CSS）、`{{ title }}`、`{{ lang }}`，
以及布尔开关 `{{ has_math }}` / `{{ has_mermaid }}` / `{{ has_toc }}`（控制是否挂对应 CDN / 侧边栏）。

## 执行原则 / 边界

1. **直接跑脚本，不自创 HTML**：转换逻辑、主题、CDN 挂载都在 `scripts/md_to_html.py`，
   agent 不要现场拼 HTML 或现写 markdown 库调用——保证产物一致、主题统一、扩展行为可预期
2. **按需挂 CDN**：脚本检测到 `$` 才挂 KaTeX、检测到 mermaid 代码块才挂 mermaid.js；
   不要无脑给所有文档挂全套 CDN（普通 README 不该背公式 / 图表的网络请求与加载耗时）
3. **深色主题默认**：默认 GitHub-dark 纯深色；
   要彻底换风格走 `--template` / `--style`
4. **一次一份或一次一目录**：不做跨文档合并；多份想合成一个 HTML 请先拼成一个 `.md`

## 工作流 / 步骤

```text
1. 确认输入 .md 路径（或目录）；首次使用确认依赖已装（见前置条件）
2. 跑脚本：
     python3 yzr-md-to-html/scripts/md_to_html.py <input.md> [-o <output.html>]
   批量：把 <input.md> 换成目录路径即可
3. 把生成的 .html 路径告诉用户（双击即可浏览）
4. 若源文档含公式 / Mermaid，提醒用户首次打开需联网加载 CDN（离线则这两类不渲染，
   代码高亮与基础排版仍正常——Pygments 是离线的）
```

## 上传产物（agent-html-drop MCP）

转换得到的 `.html` 是**本地自包含文件**，双击即可在浏览器打开，本身不需要上传。

若用户想把产物上传 / 分享出去，**仅当 agent 已配置 `agent-html-drop` MCP 服务时**才考虑上传——
直接调用该 MCP 提供的上传工具把 `.html` 推上去即可。当前**不提供**其他上传方式（不经 rsync 推
server、不写部署配置）；`agent-html-drop` 未配置时，把本地 `.html` 路径交给用户自行处理。

## 参考样例

### 样例一：单篇技术文档（最常见）

```bash
python3 yzr-md-to-html/scripts/md_to_html.py docs/design.md
# → 生成 docs/design.html：深色主题 + 侧边栏目录 + 代码高亮
```

### 样例二：带公式和流程图的论文草稿

```bash
python3 yzr-md-to-html/scripts/md_to_html.py draft.md -o draft.html
# draft.md 含 $E=mc^2$ 与 mermaid 块 → 产物自动挂 KaTeX + Mermaid CDN
```

### 样例三：批量转换整个目录

```bash
python3 yzr-md-to-html/scripts/md_to_html.py notes/
# → notes/ 下每个 .md 就地生成同名 .html
```

## 前置条件

- Python ≥ 3.7，无需 pandoc、无需 Node
- Python 依赖清单的**单一来源**：`scripts/md_to_html.py` 的 `DEPENDENCIES` 常量
- 直接跑脚本即可；缺包时脚本报错并列出 `pip install` 命令（不抛裸 ImportError 栈）
