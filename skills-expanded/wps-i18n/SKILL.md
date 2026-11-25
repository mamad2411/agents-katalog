---
name: wps-i18n
description: |
  中英双语文档。把中文文档生成中英双语对照版本，支持段落对照、左右分栏、
  表格对照三种排版模式。合同报告PPT都能做双语版，外企外贸国际合作必备。
  用于帮助用户制作双语文档。当用户提到双语、中英文对照、翻译文档时触发。
  Bilingual document generator - creates Chinese-English parallel documents.
license: MIT
user-invocable: true
argument-hint: '[文件路径/翻译需求]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 中英双语文档
  description_zh: 生成中英文对照文档，支持段落对照和左右分栏两种排版
  tags:
    - 双语
    - 翻译
    - 中英文
    - 国际化
    - WPS
  version: 1.0.1
  license: MIT
---

# 文档中英双语工具

中文文档 → 中英双语对照版。外企、外贸、国际合作必备。

## When to Use

- 需要中英文对照版本的文档
- 合同/报告需要英文版
- 需要双语排版（左中右英）
- 用户说"做个双语版""中英文对照"

## When NOT to Use

- 纯翻译（不需要排版）→ 直接对话翻译
- 校对中文文档 → 使用 `wps-proofread`

## 双语排版模式

```text
[1] 段落对照 → 中文段落下方紧跟英文翻译
[2] 左右分栏 → 左列中文 右列英文
[3] 表格对照 → 中文列 | 英文列
[4] 替换模式 → 生成纯英文版本
```

## 工作流程

### Step 1: 读取源文档

```python
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

def read_document_text(doc_path):
    """读取文档段落"""
    doc = Document(doc_path)
    paragraphs = []
    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append({
                'text': para.text,
                'style': para.style.name,
                'alignment': para.alignment,
            })
    return paragraphs
```

### Step 2: 生成双语文档

```python
def create_bilingual_doc(original_paras, translations, mode='段落对照',
                         output_path=None):
    """生成双语文档"""
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)

    def set_font(run, name, size, bold=False, italic=False):
        run.font.size = Pt(size)
        run.font.name = name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
        run.bold = bold
        run.italic = italic

    if mode == '段落对照':
        for orig, trans in zip(original_paras, translations):
            # 中文段落
            p = doc.add_paragraph()
            if 'Heading' in orig.get('style', ''):
                run = p.add_run(orig['text'])
                set_font(run, '黑体', 14, True)
            else:
                p.paragraph_format.first_line_indent = Pt(24)
                run = p.add_run(orig['text'])
                set_font(run, '宋体', 12)

            # 英文翻译
            p = doc.add_paragraph()
            if 'Heading' in orig.get('style', ''):
                run = p.add_run(trans)
                set_font(run, 'Times New Roman', 14, True, True)
            else:
                p.paragraph_format.first_line_indent = Pt(24)
                run = p.add_run(trans)
                set_font(run, 'Times New Roman', 11, italic=True)
                from docx.shared import RGBColor
                run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

            doc.add_paragraph()  # 段间空行

    elif mode == '表格对照':
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'

        # 表头
        table.cell(0, 0).text = '中文'
        table.cell(0, 1).text = 'English'

        for orig, trans in zip(original_paras, translations):
            row = table.add_row()
            row.cells[0].text = orig['text']
            row.cells[1].text = trans

    if not output_path:
        output_path = '双语文档.docx'
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 翻译质量建议

```text
专业文档翻译注意：
1. 专业术语保持一致（建立术语表）
2. 法律/合同条款需要法律翻译审核
3. 数字、日期格式转换（2026年3月 → March 2026）
4. 货币单位转换标注（人民币/RMB/CNY）
5. 人名地名使用官方翻译
```

### Step 4: 交付

1. 生成双语对照文档
2. 标注需要人工复核的专业术语
3. 建议专业文档由翻译人员审核

## 示例

```bash
# 段落对照
/wps-i18n 给report.docx生成中英双语对照版

# 合同双语
/wps-i18n 把这份合同做成中英文对照格式

# 英文版
/wps-i18n 生成这份产品介绍的英文版本
```
