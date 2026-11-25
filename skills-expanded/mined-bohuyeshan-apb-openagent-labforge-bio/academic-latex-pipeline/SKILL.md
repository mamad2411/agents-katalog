---
name: academic-latex-pipeline
description: LaTeX project initialization, compilation pipeline (xelatex/bibtex/biber), Chinese template (ctex), error log parsing, and PDF output
tool_type: cli
primary_tool: texlive + xelatex
---

# Academic LaTeX Pipeline

LaTeX 项目初始化、编译管线、中文模板支持。

## Prerequisites

| 工具 | 检查命令 | 用途 |
|------|----------|------|
| TeX Live | `xelatex --version` | LaTeX 编译 |
| biber | `biber --version` | 参考文献处理（推荐） |
| bibtex | `bibtex --version` | 参考文献处理（备选） |

## 项目初始化

### 中文论文模板（ctex）

```latex
% main.tex
\documentclass[UTF8,a4paper,12pt]{ctexart}
\usepackage{geometry}
\geometry{left=3.17cm, right=3.17cm, top=2.54cm, bottom=2.54cm}
\usepackage{setspace}
\onehalfspacing
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{refs.bib}

\title{论文标题}
\author{作者}
\date{}

\begin{document}
\maketitle

\section{引言}
引用示例\cite{key2024}。

\printbibliography
\end{document}
```

### 学位论文模板

```latex
\documentclass[UTF8,a4paper,12pt,openright]{ctexbook}
\usepackage{geometry}
\geometry{left=3.17cm, right=3.17cm, top=2.54cm, bottom=2.54cm}
\usepackage{setspace}
\onehalfspacing
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{refs.bib}

\begin{document}
\frontmatter
\include{chapters/abstract}

\mainmatter
\include{chapters/introduction}
\include{chapters/methods}
\include{chapters/results}
\include{chapters/conclusion}

\backmatter
\printbibliography
\include{chapters/appendix}
\end{document}
```

## 编译管线

### 标准 xelatex 编译（推荐）

```bash
# 第一次编译
xelatex -interaction=nonstopmode main.tex
# 处理参考文献
biber main
# 第二次编译（完善引用）
xelatex -interaction=nonstopmode main.tex
# 第三次编译（最终交叉引用）
xelatex -interaction=nonstopmode main.tex
```

### 一键编译脚本

```bash
# build.sh / build.ps1
function Build-LaTeX {
    param($Name = "main")
    xelatex -interaction=nonstopmode "$Name.tex"
    biber "$Name"
    xelatex -interaction=nonstopmode "$Name.tex"
    xelatex -interaction=nonstopmode "$Name.tex"
}
Build-LaTeX
```

### latexmk 自动编译（推荐）

```bash
# .latexmkrc 配置
latexmk -xelatex main.tex
```

简洁版 `.latexmkrc`：
```perl
$pdf_mode = 5;  # xelatex
$bibtex_use = 2;  # biber
```

## 错误排查

### 常见错误

| 错误信息 | 原因 | 解决 |
|----------|------|------|
| `! LaTeX Error: File ctexart.cls not found` | 未安装 ctex 宏包 | `tlmgr install ctex` |
| `! Package biblatex Error: Style 'gb7714-2015' not found` | 未安装 biblatex-gb7714-2015 | `tlmgr install biblatex-gb7714-2015` |
| `! Undefined control sequence` | 缺少宏包或命令拼写 | 检查宏包引入和命令名 |
| `! Package inputenc Error: Unicode character` | 编码问题 | 使用 `xelatex` 而非 `pdflatex` |
| `! I can't find file 'main.bbl'` | 忘记运行 biber/bibtex | 运行 `biber main` |
| `Runaway argument?` | 花括号不匹配 | 检查 `{}` 配对 |

### 中文支持检查

```bash
# ctex 宏包
kpsewhich ctexart.cls

# 中文字体
fc-list :lang=zh

# GB/T 7714 参考文献样式
kpsewhich gb7714-2015.bbx
```

## 参考文献格式支持

| 格式 | 后端 | 宏包 |
|------|------|------|
| GB/T 7714-2015 | biber | `biblatex-gb7714-2015` |
| GB/T 7714-2015 | bibtex | `gbt7714` |
| 其他 CSL 格式 | — | 使用 Pandoc citeproc 转换 |

### 与 BibTeX 配合

```bash
# 从 Zotero/Papis 导出 .bib 文件
papis export --all --format bibtex > refs.bib

# LaTeX 中使用
% \addbibresource{refs.bib}  % biblatex
% \bibliography{refs}        % natbib
```

## MD → LaTeX 转换

当需要从 Markdown 转到 LaTeX 时：

```bash
pandoc paper.md -o paper.tex --top-level-division=section
```

**注意**：Pandoc 生成的 LaTeX 需要手动调整中文支持。

## 工具检查

```bash
# 检查 TeX Live
xelatex --version && biber --version

# 检查中文支持
tlmgr list --only-installed | Select-String "ctex"

# 检查 GB/T 7714 样式
tlmgr list --only-installed | Select-String "gb7714"
```
