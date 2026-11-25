---
name: wps-pdf-merge-split
description: |
  PDF合并拆分。把好几个PDF合并成一个文件，或者把一个大PDF每页拆开，
  也可以只提取第3-5页、第8页这样的指定页面。支持旋转和重新排序。
  用于帮助用户处理PDF文件。当用户提到PDF合并、PDF拆分、提取页面时触发。
  Merges, splits, extracts, and reorders PDF pages.
license: MIT
user-invocable: true
argument-hint: '[操作类型] [文件路径]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: PDF合并拆分
  description_zh: 合并多个PDF为一个，或按页拆分PDF、提取指定页面
  tags:
    - PDF
    - 合并
    - 拆分
    - 文件处理
    - WPS
  version: 1.0.1
  license: MIT
---

# PDF合并与拆分工具

合并多个PDF / 拆分单个PDF / 提取指定页面。

## When to Use

- 多个PDF合并成一个
- 一个PDF拆分成多个
- 提取PDF中某几页
- 调整PDF页面顺序
- 用户说"把这几个PDF合在一起""把第3-5页提取出来"

## When NOT to Use

- 提取PDF中的文字/表格 → 使用 `wps-pdf-extract`
- PDF加水印 → 使用 `wps-watermark`

## 工作流程

### Step 1: 确认操作

```text
操作类型：
[1] 合并 → 多个PDF → 一个PDF
[2] 拆分 → 一个PDF → 每页一个PDF
[3] 提取 → 一个PDF → 提取指定页
[4] 重排 → 调整页面顺序
[5] 旋转 → 旋转指定页面
```

### Step 2: 执行操作

```python
import fitz  # PyMuPDF
import os
import glob as glob_mod

class PDFTool:
    """PDF合并拆分工具"""

    @staticmethod
    def merge(pdf_paths, output_path):
        """合并多个PDF"""
        result = fitz.open()
        for path in pdf_paths:
            doc = fitz.open(path)
            result.insert_pdf(doc)
            doc.close()
        result.save(output_path)
        result.close()
        return os.path.abspath(output_path)

    @staticmethod
    def split(pdf_path, output_dir):
        """拆分为单页PDF"""
        os.makedirs(output_dir, exist_ok=True)
        doc = fitz.open(pdf_path)
        files = []
        basename = os.path.splitext(os.path.basename(pdf_path))[0]
        for i in range(len(doc)):
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
            out = os.path.join(output_dir, f'{basename}_第{i+1}页.pdf')
            new_doc.save(out)
            new_doc.close()
            files.append(out)
        doc.close()
        return files

    @staticmethod
    def extract_pages(pdf_path, pages, output_path):
        """提取指定页面（pages为列表，从1开始）"""
        doc = fitz.open(pdf_path)
        result = fitz.open()
        for p in pages:
            result.insert_pdf(doc, from_page=p-1, to_page=p-1)
        result.save(output_path)
        result.close()
        doc.close()
        return os.path.abspath(output_path)

    @staticmethod
    def reorder(pdf_path, new_order, output_path):
        """重新排列页面（new_order为页码列表，从1开始）"""
        doc = fitz.open(pdf_path)
        result = fitz.open()
        for p in new_order:
            result.insert_pdf(doc, from_page=p-1, to_page=p-1)
        result.save(output_path)
        result.close()
        doc.close()
        return os.path.abspath(output_path)

    @staticmethod
    def rotate(pdf_path, pages, angle, output_path):
        """旋转指定页面（angle: 90/180/270）"""
        doc = fitz.open(pdf_path)
        for p in pages:
            doc[p-1].set_rotation(angle)
        doc.save(output_path)
        doc.close()
        return os.path.abspath(output_path)

    @staticmethod
    def get_info(pdf_path):
        """获取PDF信息"""
        doc = fitz.open(pdf_path)
        info = {
            'pages': len(doc),
            'title': doc.metadata.get('title', ''),
            'author': doc.metadata.get('author', ''),
            'file_size': os.path.getsize(pdf_path),
        }
        doc.close()
        return info
```

### Step 3: 页码范围解析

```text
支持的页码格式：
  "1,3,5"     → 第1、3、5页
  "1-5"       → 第1到5页
  "1-3,7,9-11" → 第1-3、7、9-11页
  "奇数页"    → 1,3,5,7...
  "偶数页"    → 2,4,6,8...
  "最后3页"   → 倒数3页
```

```python
def parse_pages(page_str, total_pages):
    """解析页码范围"""
    if page_str == '奇数页':
        return list(range(1, total_pages + 1, 2))
    if page_str == '偶数页':
        return list(range(2, total_pages + 1, 2))
    if page_str.startswith('最后'):
        n = int(page_str.replace('最后', '').replace('页', ''))
        return list(range(total_pages - n + 1, total_pages + 1))

    pages = []
    for part in page_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(p for p in pages if 1 <= p <= total_pages))
```

### Step 4: 交付

1. 生成处理后的PDF文件
2. 报告处理结果（页数、文件大小）

## 示例

```bash
# 合并PDF
/wps-pdf-merge-split 把report1.pdf、report2.pdf、report3.pdf合并成一个

# 拆分PDF
/wps-pdf-merge-split 把handbook.pdf每一页拆成单独的文件

# 提取页面
/wps-pdf-merge-split 提取contract.pdf的第3-5页和第8页

# 重新排序
/wps-pdf-merge-split 把presentation.pdf的页面顺序改成 1,3,2,4,5
```
