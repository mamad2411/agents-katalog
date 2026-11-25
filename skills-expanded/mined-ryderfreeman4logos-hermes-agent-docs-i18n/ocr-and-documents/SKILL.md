---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf)."
version: 2.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [pdf, docx, powerpoint]
---

# PDF与文档提取

对于DOCX格式：可参考`docx`技能（用于创建/编辑），或使用`python-docx`库进行结构化读取。
对于PPTX格式：可参考`powerpoint`技能（支持完整的创建/读取/编辑功能）。
对于PDF文档的操作（合并、拆分、处理表单、添加水印及创建新PDF）：请使用`pdf`技能。
该技能可实现**从PDF文档及扫描件中提取文本**的功能。

## 第一步：是否有远程URL？

如果文档存在URL，**请优先尝试使用`web_extract`功能**：

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

该功能通过 Firecrawl 实现 PDF 到 Markdown 的转换，且无需任何本地依赖。

仅在以下情况下才使用本地提取功能：文件位于本地、web_extract 失败，或需要批量处理时。

## 第 2 步：选择本地提取器

| 功能 | pymupdf（约 25MB） | marker-pdf（约 3-5GB） |
|---------|-----------------|---------------------|
| **文本型 PDF** | ✅ | ✅ |
| **扫描版 PDF（OCR）** | ❌ | ✅（支持 90 多种语言） |
| **表格** | ✅（基础功能） | ✅（高精度） |
| **公式 / LaTeX** | ❌ | ✅ |
| **代码块** | ❌ | ✅ |
| **表单** | ❌ | ✅ |
| **删除页眉/页脚** | ❌ | ✅ |
| **识别阅读顺序** | ❌ | ✅ |
| **提取图片** | ✅（嵌入图片） | ✅（结合上下文提取） |
| **图片转文本（OCR）** | ❌ | ✅ |
| **EPUB 格式** | ✅ | ✅ |
| **Markdown 输出格式** | ✅（通过 pymupdf4llm 实现） | ✅（原生输出，质量更高） |
| **安装大小** | 约 25MB | 约 3-5GB（包含 PyTorch 及模型文件） |
| **处理速度** | 即时完成 | 每页约 1-14 秒（CPU），每页约 0.2 秒（GPU） |

**决策建议**：除非需要 OCR、公式解析、表单处理或复杂的布局分析功能，否则建议使用 pymupdf。

如果用户需要 marker 的高级功能，但系统可用磁盘空间不足 5GB：
> “该文档需要通过 OCR 或高级提取功能（marker-pdf）来处理，这需要约 5GB 的空间用于存储 PyTorch 及相关模型。您的系统目前还有 [X]GB 的空闲空间。您可以选择：释放更多空间、提供一个网址以便我使用 web_extract 进行提取，或者尝试使用 pymupdf——它虽能处理文本型 PDF，但无法处理扫描版文档或包含公式的文件。”

---

## pymupdf（轻量级版本）

```bash
pip install pymupdf pymupdf4llm
```

**通过辅助脚本**：
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**内联模式**：
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

## marker-pdf（高质量 OCR）

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**通过辅助脚本**：
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI**（与 marker-pdf 一同安装）：
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

## Arxiv论文集

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## 分割、合并与搜索

pymupdf可直接实现这些功能——您可以使用`execute_code`或内联Python代码来完成操作：

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

无需额外依赖——pymupdf 一个包即可实现文档的分割、合并、搜索以及文本提取功能。

---

## 备注

- 对于网址，`web_extract` 始终是首选方案。
- pymupdf 是最稳妥的默认选择：响应迅速、无需模型、兼容所有环境。
- marker-pdf 适用于 OCR 处理、扫描文档、公式以及复杂布局——仅在必要时安装。
- 这两个辅助脚本均支持 `--help` 参数以查看完整使用说明。
- 首次使用时，marker-pdf 会将约 2.5GB 的模型下载到 `~/.cache/huggingface/` 目录中。
- 处理 Word 文档时：请安装 `python-docx`（相比 OCR 更高效，可直接解析文档结构）。
- 处理 PowerPoint 文件时：请参考 `powerpoint` 技能（该技能基于 python-pptx 开发）。
