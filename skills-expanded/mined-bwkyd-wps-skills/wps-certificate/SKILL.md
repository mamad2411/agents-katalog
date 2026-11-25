---
name: wps-certificate
description: |
  证书奖状批量生成。给一份名单，批量生成荣誉证书、结业证书、聘书、感谢信，
  每人一份独立文件，年终评优、培训结业、表彰活动必备工具。
  用于帮助用户批量生成证书。当用户提到证书、奖状、聘书时触发。
  Batch certificate/award generator from a list of recipients.
license: MIT
user-invocable: true
argument-hint: '[证书类型] [名单/需求]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 证书奖状批量生成
  description_zh: 根据名单批量生成荣誉证书、结业证书、聘书等Word文档
  tags:
    - 证书
    - 奖状
    - 批量
    - python-docx
    - WPS
  version: 1.0.1
  license: MIT
---

# 证书/奖状生成器

名单 + 模板 → 批量生成证书。年终评优、培训结业必备。

## When to Use

- 批量生成荣誉证书/奖状
- 结业证书/培训证书
- 聘书/委任状
- 感谢信/表扬信
- 用户说"帮我做证书""批量生成奖状"

## When NOT to Use

- 普通文档 → 使用 `wps-docx-writer`
- 合同/协议 → 使用 `wps-contract`

## 证书类型

```text
[1] 荣誉证书 → 先进个人/优秀员工/竞赛获奖
[2] 结业证书 → 培训/课程结业
[3] 聘  书 → 聘任职务/顾问
[4] 感谢信 → 感谢合作/捐赠/志愿服务
[5] 表扬信 → 表扬个人/团队
```

## 证书文案模板

```text
荣誉证书：
  [姓名] 同志：
  在 [时间段] [活动/考核] 中表现突出，成绩优异，
  被评为"[荣誉称号]"，特发此证，以资鼓励。
                    [单位名称]
                    [日期]

结业证书：
  兹证明 [姓名] 于 [时间] 参加本单位组织的
  "[培训名称]" 培训，完成全部课程学习，
  考核合格，准予结业。
                    [单位名称]
                    [日期]

聘书：
  [姓名] 先生/女士：
  经研究决定，聘任您为 [职务/职称]，
  聘期自 [起始日期] 至 [终止日期]。
                    [单位名称]（盖章）
                    [日期]
```

## 工作流程

### Step 1: 确认信息

- **证书类型**
- **发证单位**
- **获证人员名单**（Excel/手动输入）
- **证书内容**（荣誉称号/培训名称等）
- **日期**

### Step 2: 生成证书

```python
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from openpyxl import load_workbook
import os

def create_certificate(cert_type, unit_name, recipients, content, date_str,
                       output_dir=None):
    """批量生成证书"""
    output_dir = output_dir or '证书输出'
    os.makedirs(output_dir, exist_ok=True)
    files = []

    templates = {
        '荣誉证书': '在{activity}中表现突出，成绩优异，被评为"{title}"，'
                    '特发此证，以资鼓励。',
        '结业证书': '于{period}参加本单位组织的"{training}"培训，'
                    '完成全部课程学习，考核合格，准予结业。',
        '聘书': '经研究决定，聘任您为{position}，聘期自{start}至{end}。',
    }

    for person in recipients:
        name = person if isinstance(person, str) else person.get('name', '')
        doc = Document()

        # 页面设置（横向A4）
        section = doc.sections[0]
        section.page_width = Cm(29.7)
        section.page_height = Cm(21)
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(4)
        section.right_margin = Cm(4)

        def set_font(run, font_name='楷体', size=16, bold=False, color=None):
            run.font.size = Pt(size)
            run.font.name = font_name
            run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
            run.bold = bold
            if color:
                run.font.color.rgb = RGBColor(*color)

        # 标题
        for _ in range(2):
            doc.add_paragraph()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(cert_type)
        set_font(run, '华文行楷', 36, True, (180, 30, 30))

        doc.add_paragraph()

        # 称呼
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Pt(32)
        p.paragraph_format.line_spacing = Pt(36)
        run = p.add_run(f'{name} 同志：')
        set_font(run, '楷体', 18)

        # 正文
        body_text = templates.get(cert_type, content)
        if isinstance(person, dict):
            body_text = body_text.format(**person)
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Pt(36)
        p.paragraph_format.line_spacing = Pt(36)
        run = p.add_run(f'    {body_text}')
        set_font(run, '楷体', 16)

        # 落款
        for _ in range(3):
            doc.add_paragraph()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = p.add_run(unit_name)
        set_font(run, '楷体', 16)

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = p.add_run(date_str)
        set_font(run, '楷体', 14)

        path = os.path.join(output_dir, f'{cert_type}_{name}.docx')
        doc.save(path)
        files.append(path)

    return files
```

### Step 3: 交付

1. 批量生成每人一份的证书文件
2. 或生成一个文件（每页一张证书）便于连续打印
3. 建议使用A4横向彩色打印

## 示例

```bash
# 批量生成
/wps-certificate 荣誉证书 用employees.xlsx里的名单生成年度优秀员工证书

# 单张
/wps-certificate 聘书 聘任张三为技术顾问

# 结业证书
/wps-certificate 结业证书 给参加Python培训的20个人生成结业证
```
