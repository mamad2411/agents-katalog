---
name: wps-batch-convert
description: |
  文档批量格式转换。把一个文件夹里的Word全转文本、Excel全导出CSV、
  Markdown转Word，支持docx/txt/xlsx/csv/md等格式批量互转，一次搞定。
  用于帮助用户批量转换文档格式。当用户提到批量转换、格式转换、导出时触发。
  Batch converts documents between formats (docx/pdf/xlsx/csv/md).
license: MIT
user-invocable: true
argument-hint: '[源格式] [目标格式] [文件/文件夹]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 文档批量转换
  description_zh: 把文件夹里的docx转txt、xlsx导出csv等，支持多种格式批量互转
  tags:
    - 转换
    - 批量
    - PDF
    - 格式
    - WPS
  version: 1.0.1
  license: MIT
---

# 批量格式转换工具

一个文件夹 → 全部转换 → 输出到目标文件夹。

## When to Use

- 批量将Word转PDF
- Excel批量导出CSV
- Markdown转Word
- 整个文件夹的格式转换
- 用户说"批量转PDF""全部导出为CSV"

## When NOT to Use

- PDF内容提取 → 使用 `wps-pdf-extract`
- PDF合并拆分 → 使用 `wps-pdf-merge-split`

## 支持的转换路径

| 源格式 | 目标格式 | 工具 |
|--------|----------|------|
| .docx | .pdf | python-docx + reportlab 或 WPS CLI |
| .docx | .txt | python-docx |
| .xlsx | .csv | openpyxl |
| .csv | .xlsx | openpyxl |
| .pptx | .pdf | python-pptx + WPS CLI |
| .md | .docx | markdown + python-docx |
| .txt | .docx | python-docx |

## 工作流程

### Step 1: 确认转换需求

- 源格式和目标格式
- 文件列表或文件夹路径
- 输出位置

### Step 2: 批量转换

```python
from docx import Document
from openpyxl import load_workbook
import csv
import os
import glob as glob_mod
import subprocess

class BatchConverter:
    """批量格式转换器"""

    @staticmethod
    def docx_to_txt(docx_path, output_path=None):
        """Word转纯文本"""
        doc = Document(docx_path)
        text = '\n'.join(para.text for para in doc.paragraphs)
        if not output_path:
            output_path = os.path.splitext(docx_path)[0] + '.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return output_path

    @staticmethod
    def xlsx_to_csv(xlsx_path, output_path=None, sheet_name=None):
        """Excel转CSV"""
        wb = load_workbook(xlsx_path, read_only=True)
        ws = wb[sheet_name] if sheet_name else wb.active
        if not output_path:
            output_path = os.path.splitext(xlsx_path)[0] + '.csv'
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            for row in ws.iter_rows(values_only=True):
                writer.writerow(row)
        wb.close()
        return output_path

    @staticmethod
    def csv_to_xlsx(csv_path, output_path=None):
        """CSV转Excel"""
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        wb = Workbook()
        ws = wb.active
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row_idx, row in enumerate(reader, 1):
                for col_idx, val in enumerate(row, 1):
                    ws.cell(row=row_idx, column=col_idx, value=val)
                if row_idx == 1:
                    for col_idx in range(1, len(row) + 1):
                        ws.cell(row=1, column=col_idx).font = Font(bold=True)
        if not output_path:
            output_path = os.path.splitext(csv_path)[0] + '.xlsx'
        wb.save(output_path)
        return output_path

    @staticmethod
    def md_to_docx(md_path, output_path=None):
        """Markdown转Word"""
        doc = Document()
        with open(md_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('# '):
                    doc.add_heading(line[2:], level=1)
                elif line.startswith('## '):
                    doc.add_heading(line[3:], level=2)
                elif line.startswith('### '):
                    doc.add_heading(line[4:], level=3)
                elif line.startswith('- '):
                    doc.add_paragraph(line[2:], style='List Bullet')
                elif line.strip():
                    doc.add_paragraph(line)
        if not output_path:
            output_path = os.path.splitext(md_path)[0] + '.docx'
        doc.save(output_path)
        return output_path

    @staticmethod
    def batch_convert(source_dir, source_ext, target_ext, output_dir=None):
        """批量转换文件夹"""
        if not output_dir:
            output_dir = os.path.join(source_dir, f'converted_{target_ext}')
        os.makedirs(output_dir, exist_ok=True)

        converter_map = {
            ('.docx', '.txt'): BatchConverter.docx_to_txt,
            ('.xlsx', '.csv'): BatchConverter.xlsx_to_csv,
            ('.csv', '.xlsx'): BatchConverter.csv_to_xlsx,
            ('.md', '.docx'): BatchConverter.md_to_docx,
        }

        func = converter_map.get((source_ext, target_ext))
        if not func:
            raise ValueError(f'不支持 {source_ext} → {target_ext} 转换')

        files = glob_mod.glob(os.path.join(source_dir, f'*{source_ext}'))
        results = []
        for f in files:
            basename = os.path.splitext(os.path.basename(f))[0]
            out = os.path.join(output_dir, f'{basename}{target_ext}')
            func(f, out)
            results.append(out)

        return results
```

### Step 3: 交付

1. 转换后的文件输出到指定目录
2. 报告转换结果（成功/失败数量）
3. 提示不支持的转换路径和替代方案

## 示例

```bash
# 批量Word转文本
/wps-batch-convert 把docs文件夹里所有docx转成txt

# Excel转CSV
/wps-batch-convert 把所有xlsx导出为csv

# Markdown转Word
/wps-batch-convert 把notes.md转成Word文档

# 批量处理
/wps-batch-convert reports文件夹里的所有csv转成xlsx
```
