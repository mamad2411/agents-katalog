---
name: wps-pdf-extract
description: |
  PDF文字表格提取。PDF里的表格死活复制不出来？帮你把PDF中的文字、表格、
  图片提取出来，文字转Word，表格转Excel，图片导出到文件夹。
  用于帮助用户从PDF中提取内容。当用户提到PDF提取、PDF转Word、PDF表格时触发。
  Extracts text, tables, and images from PDFs into editable formats.
license: MIT
user-invocable: true
argument-hint: '[PDF文件路径]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: PDF内容提取
  description_zh: 从PDF中提取文字、表格和图片，转成Word或Excel格式
  tags:
    - PDF
    - 提取
    - 转换
    - 表格
    - WPS
  version: 1.0.1
  license: MIT
---

# PDF内容提取工具

PDF → 提取文字/表格/图片 → 转为可编辑的Word/Excel。

> 告别"PDF里的表格复制不出来"的痛苦。

## When to Use

- 从PDF中提取文字内容
- 提取PDF中的表格到Excel
- 提取PDF中的图片
- PDF转可编辑Word
- 用户说"PDF里的表格怎么弄出来""PDF转Word"

## When NOT to Use

- PDF合并/拆分 → 使用 `wps-pdf-merge-split`
- PDF加水印 → 使用 `wps-watermark`

## 工作流程

### Step 1: 诊断PDF类型

```text
PDF类型判断：
├─ 文字型PDF（可选中文字）→ 直接提取
├─ 扫描型PDF（图片）→ 需要OCR → 提示用户
└─ 混合型（部分文字部分图片）→ 分别处理
```

### Step 2: 提取内容

```python
# 安装依赖
# pip install PyMuPDF pdfplumber python-docx openpyxl

import fitz  # PyMuPDF
import pdfplumber
from docx import Document
from openpyxl import Workbook
import os

class PDFExtractor:
    """PDF内容提取器"""

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def extract_text(self, pages=None):
        """提取全部文字"""
        text = []
        page_range = pages or range(len(self.doc))
        for i in page_range:
            page = self.doc[i]
            text.append(page.get_text())
        return '\n'.join(text)

    def extract_tables(self, pages=None):
        """提取表格（使用pdfplumber）"""
        tables = []
        with pdfplumber.open(self.pdf_path) as pdf:
            page_range = pages or range(len(pdf.pages))
            for i in page_range:
                page_tables = pdf.pages[i].extract_tables()
                for t in page_tables:
                    tables.append({
                        'page': i + 1,
                        'data': t,
                    })
        return tables

    def extract_images(self, output_dir):
        """提取图片"""
        os.makedirs(output_dir, exist_ok=True)
        images = []
        for i, page in enumerate(self.doc):
            for j, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                pix = fitz.Pixmap(self.doc, xref)
                if pix.n < 5:  # GRAY or RGB
                    img_path = os.path.join(output_dir, f'page{i+1}_img{j+1}.png')
                    pix.save(img_path)
                else:  # CMYK
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    img_path = os.path.join(output_dir, f'page{i+1}_img{j+1}.png')
                    pix.save(img_path)
                images.append(img_path)
        return images

    def to_word(self, output_path):
        """转换为Word文档"""
        doc = Document()
        for i, page in enumerate(self.doc):
            if i > 0:
                doc.add_page_break()
            text = page.get_text("blocks")
            for block in sorted(text, key=lambda b: (b[1], b[0])):
                if block[6] == 0:  # text block
                    para = doc.add_paragraph(block[4].strip())
        doc.save(output_path)
        return os.path.abspath(output_path)

    def tables_to_excel(self, output_path):
        """表格导出为Excel"""
        tables = self.extract_tables()
        if not tables:
            return None

        wb = Workbook()
        for idx, table in enumerate(tables):
            ws = wb.active if idx == 0 else wb.create_sheet()
            ws.title = f"表格{idx+1}_P{table['page']}"
            for row_idx, row in enumerate(table['data'], 1):
                for col_idx, cell in enumerate(row, 1):
                    ws.cell(row=row_idx, column=col_idx,
                            value=cell if cell else '')

        wb.save(output_path)
        return os.path.abspath(output_path)

    def close(self):
        self.doc.close()
```

### Step 3: 智能处理

```text
提取策略：
1. 先尝试直接提取文字 → 检查是否有内容
2. 如果文字为空 → 判断为扫描件 → 提示需要OCR
3. 表格优先用pdfplumber → 表格识别率更高
4. 图片用PyMuPDF → 可提取嵌入的原始图片
```

### Step 4: 交付

1. 文字提取 → 输出.docx或.txt
2. 表格提取 → 输出.xlsx（每个表格一个sheet）
3. 图片提取 → 输出到文件夹
4. 报告提取结果（页数、表格数、图片数）

## 常见问题处理

```text
Q: PDF转Word后格式乱了？
A: PDF本质是"画"出来的，不是"排版"出来的。
   完美还原几乎不可能，建议提取文字后重新排版。

Q: 表格提取不完整？
A: 1. 检查PDF中表格是否有完整边框线
   2. 尝试调整pdfplumber的table_settings参数
   3. 无边框表格识别率较低

Q: 中文乱码？
A: 1. PDF可能使用了嵌入字体
   2. 尝试 page.get_text("text") 替代默认模式
   3. 扫描件需要OCR（推荐用WPS自带的OCR功能）
```

## 示例

```bash
# 提取文字
/wps-pdf-extract 把report.pdf的文字提取出来转成Word

# 提取表格
/wps-pdf-extract 提取financial_report.pdf里的所有表格到Excel

# 提取图片
/wps-pdf-extract 把这个PDF里的图片都提取出来
```
