---
name: wps-ppt-to-doc
description: |
  PPT转Word文档。把PPT演示文稿的内容整理成结构化的Word文档，
  标题变章节、要点变段落、表格也保留，方便会后分发阅读或归档留存。
  用于帮助用户将PPT转为文档。当用户提到PPT转Word、PPT导出文档时触发。
  Converts PPT presentations to structured Word documents.
license: MIT
user-invocable: true
argument-hint: '[PPT文件路径]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: PPT转Word
  description_zh: 将PPT内容整理成结构化的Word文档，方便分发和归档
  tags:
    - PPT
    - Word
    - 转换
    - 文档
    - WPS
  version: 1.0.1
  license: MIT
---

# PPT转Word工具

PPT → 结构化Word文档。会后分发、归档必备。

## When to Use

- PPT内容需要转为Word文档
- 会议演示材料需要文字版分发
- PPT归档需要可搜索的文档格式
- 用户说"把PPT转成Word""导出PPT文字内容"

## When NOT to Use

- Word转PPT → 使用 `wps-ppt-outline` + `wps-ppt-gen`
- 只需提取文字 → 直接读取PPT文本

## 转换模式

```text
[1] 完整模式 → 标题+内容+图表描述+备注
[2] 精简模式 → 仅标题+要点
[3] 讲义模式 → 含幻灯片缩略描述+详细文字
```

## 工作流程

### Step 1: 读取PPT

```python
from pptx import Presentation
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

def ppt_to_word(ppt_path, mode='完整', output_path=None):
    """PPT转Word"""
    prs = Presentation(ppt_path)
    doc = Document()

    # 页面设置
    section = doc.sections[0]
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

    def set_font(run, name='宋体', size=12, bold=False):
        run.font.size = Pt(size)
        run.font.name = name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
        run.bold = bold

    # 文档标题（使用PPT第一页标题）
    first_title = ''
    if prs.slides:
        for shape in prs.slides[0].shapes:
            if shape.has_text_frame and shape == prs.slides[0].shapes.title:
                first_title = shape.text_frame.text
                break

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(first_title or 'PPT文档内容')
    set_font(run, '黑体', 18, True)
    doc.add_paragraph()

    # 逐页转换
    for i, slide in enumerate(prs.slides):
        slide_title = ''
        slide_texts = []
        has_notes = False
        notes_text = ''

        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    slide_title = shape.text_frame.text.strip()
                else:
                    for para in shape.text_frame.paragraphs:
                        text = para.text.strip()
                        if text:
                            slide_texts.append(text)

        # 备注
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                has_notes = True
                notes_text = notes

        # 写入Word
        if i > 0 or slide_title != first_title:
            # 章节标题
            p = doc.add_paragraph()
            run = p.add_run(f'{slide_title or f"第{i+1}页"}')
            set_font(run, '黑体', 14, True)
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)

        # 内容要点
        for text in slide_texts:
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Pt(24)
            run = p.add_run(text)
            set_font(run, '宋体', 12)

        # 备注（完整模式）
        if mode == '完整' and has_notes:
            p = doc.add_paragraph()
            run = p.add_run(f'【备注】{notes_text}')
            set_font(run, '楷体', 10)

        # 图表标注
        for shape in slide.shapes:
            if shape.has_chart:
                p = doc.add_paragraph()
                run = p.add_run('【此处包含图表】')
                set_font(run, '楷体', 10)
            if shape.has_table:
                # 提取表格数据
                table = shape.table
                doc_table = doc.add_table(rows=len(table.rows),
                                          cols=len(table.columns))
                for ri, row in enumerate(table.rows):
                    for ci, cell in enumerate(row.cells):
                        doc_table.cell(ri, ci).text = cell.text

    if not output_path:
        base = os.path.splitext(os.path.basename(ppt_path))[0]
        output_path = f'{base}_文档版.docx'
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 2: 交付

1. 生成结构化Word文档
2. 保留标题层级和内容要点
3. 标注原PPT中图表/表格位置

## 示例

```bash
# 完整转换
/wps-ppt-to-doc 把quarterly_review.pptx转成Word文档

# 精简版
/wps-ppt-to-doc 只提取PPT的标题和要点到Word

# 讲义
/wps-ppt-to-doc 把培训PPT转成学员讲义
```
