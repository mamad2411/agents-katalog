---
name: wps-poetry
description: |
  诗词精美排版。把古诗词、现代诗、对联排成精美的Word文档，
  华文行楷大字、古风配色、充分留白，可直接打印装裱。教学展示活动布置也好用。
  用于帮助用户排版诗词。当用户提到诗词、古诗、对联、书法排版时触发。
  Chinese poetry typesetting - elegant formatting for printing and display.
license: MIT
user-invocable: true
argument-hint: '[诗词内容/排版需求]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 诗词排版
  description_zh: 将古诗词排版成可打印的精美文档，支持横排、对联、现代诗格式
  tags:
    - 诗词
    - 排版
    - 书法
    - 文化
    - WPS
  version: 1.0.1
  license: MIT
---

# 诗词排版工具

诗词 → 精美排版 → 可打印/装裱级别的文档。

> 小众但有趣：让诗词以最美的姿态呈现。

## When to Use

- 古诗词精美排版打印
- 对联排版
- 教学材料中的诗词展示
- 文化活动用诗词海报底稿
- 用户说"帮我排版这首诗""做个对联"

## When NOT to Use

- 普通文档排版 → 使用 `wps-docx-writer`
- 公文 → 使用 `wps-gongwen`

## 排版样式

```text
[1] 经典横排 → 居中、留白、印章装饰
[2] 竖排古风 → 从右到左、竖排文字
[3] 对联格式 → 上联+下联+横批
[4] 现代诗 → 左对齐、错落有致
[5] 书法练字 → 田字格/米字格
```

## 工作流程

### Step 1: 确认诗词内容和排版需求

- 诗词全文（含标题、作者）
- 排版样式
- 用途（打印/展示/教学）

### Step 2: 生成排版

```python
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

def create_poetry_doc(title, author, lines, style='经典横排',
                      output_path=None):
    """生成诗词排版文档"""
    doc = Document()
    section = doc.sections[0]

    def set_font(run, name='华文行楷', size=18, bold=False, color=None):
        run.font.size = Pt(size)
        run.font.name = name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
        run.bold = bold
        if color:
            run.font.color.rgb = RGBColor(*color)

    if style == '经典横排':
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(5)
        section.bottom_margin = Cm(5)
        section.left_margin = Cm(5)
        section.right_margin = Cm(5)

        # 大量留白后开始
        for _ in range(4):
            doc.add_paragraph()

        # 标题
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(24)
        run = p.add_run(title)
        set_font(run, '华文行楷', 28, color=(0x8B, 0x45, 0x13))

        # 作者
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(36)
        run = p.add_run(f'【{author}】')
        set_font(run, '楷体', 14, color=(0x80, 0x80, 0x80))

        # 诗句
        for line in lines:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = Pt(42)
            run = p.add_run(line)
            set_font(run, '华文行楷', 22, color=(0x33, 0x33, 0x33))

    elif style == '对联格式':
        section.page_width = Cm(29.7)  # 横向
        section.page_height = Cm(21)
        section.top_margin = Cm(3)
        section.left_margin = Cm(4)
        section.right_margin = Cm(4)

        # 横批
        if len(lines) >= 3:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(48)
            run = p.add_run(lines[2])  # 横批
            set_font(run, '华文隶书', 36, True, color=(0xCC, 0x00, 0x00))

        doc.add_paragraph()

        # 上下联（使用表格模拟左右对称）
        table = doc.add_table(rows=1, cols=3)
        table.alignment = 1  # CENTER

        if len(lines) >= 2:
            # 上联（右）
            cell = table.cell(0, 2)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(lines[0])
            set_font(run, '华文行楷', 28, color=(0x8B, 0x00, 0x00))

            # 下联（左）
            cell = table.cell(0, 0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(lines[1])
            set_font(run, '华文行楷', 28, color=(0x8B, 0x00, 0x00))

    elif style == '现代诗':
        section.top_margin = Cm(4)
        section.left_margin = Cm(6)
        section.right_margin = Cm(4)

        for _ in range(3):
            doc.add_paragraph()

        # 标题
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(18)
        run = p.add_run(title)
        set_font(run, '微软雅黑', 22, True, color=(0x2C, 0x3E, 0x50))

        # 作者
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(30)
        run = p.add_run(author)
        set_font(run, '微软雅黑', 11, color=(0x99, 0x99, 0x99))

        # 诗行
        for line in lines:
            if line.strip() == '':
                doc.add_paragraph()  # 空行
            else:
                p = doc.add_paragraph()
                p.paragraph_format.line_spacing = Pt(32)
                run = p.add_run(line)
                set_font(run, '华文楷体', 14, color=(0x33, 0x33, 0x33))

    if not output_path:
        output_path = f'{title}_排版.docx'
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成精美排版的诗词文档
2. 建议用较好的纸张打印
3. 字体说明（如果用户电脑没有华文行楷等字体）

## 示例

```bash
# 古诗排版
/wps-poetry 帮我排版李白的《将进酒》，经典横排风格

# 对联
/wps-poetry 上联：春风得意马蹄疾 下联：一日看尽长安花 横批：金榜题名

# 现代诗
/wps-poetry 帮我排版海子的《面朝大海春暖花开》
```
