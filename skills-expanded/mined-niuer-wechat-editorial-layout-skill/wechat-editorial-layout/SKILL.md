---
name: wechat-editorial-layout-skill
description: 将中文文章的 Markdown、Word 或纯文本整理为可直接粘贴到微信公众号编辑器的 HTML，并生成带一键复制功能的预览页。适用于公众号排版、微信文章排版、中文文章转公众号 HTML，以及需要简约极客编辑风的任务。不要用于普通网页、营销落地页或仅改写文案。
---

# 公众号文章排版

将用户提供的文章转换为微信公众号正文 HTML。保留原文观点、事实、语气和内容顺序，只做必要的结构整理与排版。

## 执行步骤

### 1. 准备文章

- Markdown：直接使用。
- Word `.docx`：运行 `python3 scripts/extract_docx.py INPUT.docx -o article.md`。
- 纯文本：整理为 Markdown，不补写原文没有的事实。
- PDF 或网页：先使用可靠工具提取为 Markdown。

用户没有提供文章时，索要正文。完整保留原文中的作者署名、来源、链接、图片、专有名词和数字。

### 2. 规范 Markdown

先阅读 [references/editorial-theme.md](references/editorial-theme.md)，再按以下规则整理：

- `#` 仅作为文章标题和文件名依据，不进入正文 HTML。
- 主章节使用 `##`，细分内容使用 `###`。
- 只在语义需要时拆分过长段落，不改变原文意思和顺序。
- 核心判断可用 `**文字**` 标记；每段最多一处，全文最多五处。
- 引用使用 `>`，代码使用 Markdown 围栏代码块，图片使用 `![说明](路径或 URL)`。
- 文末来源使用“相关链接：”“参考链接：”或“引用链接：”；每组先写说明文案，下一行单独写原始 URL。
- 不确定的内容保持原文或标记待核实，不编造信息和链接。

### 3. 生成并校验

运行：

```bash
python3 scripts/render_wechat.py article.md -o article-wechat.html
python3 scripts/validate_wechat.py article-wechat.html
```

校验结果必须为 `PASS: 0 errors`。如有错误，修复后重新生成并校验。

### 4. 生成预览

运行：

```bash
python3 scripts/wrap_preview.py article-wechat.html
```

预览文件为 `article-wechat-preview.html`。复制按钮只属于预览页面，不进入公众号正文。

## 交付标准

- 严格使用 [references/editorial-theme.md](references/editorial-theme.md) 规定的视觉样式；正文从标题后的第一段或第一个章节开始，不生成文章主标题、标题横线、标题占位、作者简介或公众号自带组件。
- 文末链接放在结尾分割线之后，并保持“说明文案：”换行接 URL 的结构。
- 正文为单个根 `<section>` 片段，不包含 `html`、`head`、`body`、`style`、`script`、`class` 或 `id`；使用内联样式，不依赖外部字体、样式表或脚本。
- 不使用公众号不兼容的标签和效果；复杂表格改为适合窄屏阅读的列表。
- 交付干净正文 HTML 和预览 HTML；校验必须通过，并说明仍待补充的图片或事实。
