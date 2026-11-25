---
name: nano-pdf
description: "Edit text in existing PDFs via natural-language prompts."
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Editing, NLP, Productivity]
    homepage: https://pypi.org/project/nano-pdf/
    related_skills: [pdf, ocr-and-documents]
---

# nano-pdf

通过自然语言指令编辑 PDF 文件。只需将工具指向目标页面，并描述需要进行的修改即可。如需处理 PDF 的结构相关操作（合并、拆分、表单处理、水印添加及新建 PDF），请参考 `pdf` 技能；若需从扫描件中提取文本，则可使用 `ocr-and-documents`。 

## 先决条件

```bash
# Install with uv (recommended — already available in Hermes)
uv pip install nano-pdf

# Or with pip
pip install nano-pdf
```

## 使用方法

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## 示例

```bash
# Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"

# Update a date on a specific page
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"

# Fix content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

## 备注

- 页面编号可能因版本不同而采用0基或1基计数——如果编辑时选错了页面，请尝试调整±1后重新操作。
- 编辑完成后务必检查生成的PDF文件（可使用`read_file`命令查看文件大小，或直接打开文件进行确认）。
- 该工具底层基于大型语言模型运行，因此需要API密钥（具体配置信息可查看`nano-pdf --help`）。
- 该工具非常适合文本修改；对于复杂的布局调整，则可能需要采用其他方法。
