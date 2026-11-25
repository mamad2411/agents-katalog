---
name: MarkItDown
description: 将各种文档格式转换为 Markdown。当用户要求读取、解析 doc、docx、pdf、xls、xlsx、ppt、pptx 等 Office 文档时使用。
allowed-tools: Bash(markitdown *), Bash(libreoffice *)
---

# MarkItDown 文档转换

使用 `markitdown` 命令将文档转换为 Markdown 格式。

## 依赖安装

### markitdown

要求 Python 3.10+，根据需要选择安装：

```bash
# 按需安装特定格式支持
pip install 'markitdown[pdf]'           # PDF
pip install 'markitdown[docx]'          # Word
pip install 'markitdown[pptx]'          # PowerPoint
pip install 'markitdown[xlsx]'          # Excel
pip install 'markitdown[xls]'           # 旧版 Excel

# 安装全部支持（推荐）
pip install 'markitdown[all]'
```

其他可选依赖：`[outlook]`、`[audio-transcription]`、`[youtube-transcription]`

### LibreOffice

用于转换旧版 Office 格式（.doc, .ppt）：

```bash
# Homebrew 安装
brew install --cask libreoffice

# 或手动下载 dmg 安装
# https://www.libreoffice.org/download/download/
```

## 直接支持的格式

| 格式 | 说明 |
|------|------|
| `.docx` | Word 文档 |
| `.xls` / `.xlsx` | Excel 表格 |
| `.pptx` | PowerPoint 演示文稿 |
| `.pdf` | PDF 文档 |

## 需要先转换的格式

旧版 Office 格式需要用 `libreoffice` 转换后再读取：

| 格式 | 转换命令 |
|------|----------|
| `.doc` | `libreoffice --headless --convert-to docx file.doc` |
| `.ppt` | `libreoffice --headless --convert-to pptx file.ppt` |

## 使用方法

### 直接读取

```bash
markitdown /path/to/file.docx
markitdown /path/to/file.pdf
markitdown /path/to/file.xlsx
```

### 旧版格式先转换再读取

```bash
# 转换（建议用 --outdir 指定输出目录）
libreoffice --headless --convert-to docx --outdir /path/to/output /path/to/file.doc

# 读取转换后的文件
markitdown /path/to/output/file.docx
```

### 输出到文件

```bash
markitdown file.pdf -o output.md
```

## 示例

用户说："帮我读取 `<源文件路径>`"

执行步骤：
1. 先转换：`libreoffice --headless --convert-to docx --outdir <输出文件目录> <源文件路径>`
2. 再读取：`markitdown <输出文件目录>/<文件名>.docx`

返回的内容就是转换后的 Markdown 文本，可以直接阅读和分析。
