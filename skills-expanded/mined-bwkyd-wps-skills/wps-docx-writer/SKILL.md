---
name: wps-docx-writer
description: |
  Word文档生成。用python-docx生成各类Word文档，
  支持标题、正文、表格、图片、页眉页脚等元素。
  用于帮助用户生成Word文档。当用户提到Word、docx、文档时触发。
  Word document generator using python-docx.
license: MIT
user-invocable: true
argument-hint: '[文档类型] [内容描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: Word文档生成
  description_zh: 用python-docx生成Word文档，支持标题、正文、表格、图片等
  tags:
    - Word
    - docx
    - python-docx
    - 文档生成
    - WPS
  version: 1.0.3
  license: MIT
---

# Word 文档生成器

使用 python-docx 生成各类规范的中文 .docx 文档，兼容 WPS Office 和 Microsoft Word。

## When to Use

- 用户需要生成 Word/docx 文档
- 用户需要创建合同、报告、简历、论文、方案等
- 用户需要批量生成文档或填充模板
- 用户说"帮我写一份XX"且不是公文场景

## When NOT to Use

- 党政机关公文 → 使用 `wps-gongwen`
- WPS宏脚本开发 → 使用 `wps-jsa-macro`
- 纯文本/Markdown文档 → 直接编写

## 支持的文档类型

| 类型 | 典型场景 | 模板特征 |
|------|---------|---------|
| **合同/协议** | 劳动合同、租赁合同、保密协议、合作协议 | 甲乙方信息、条款编号、签章区 |
| **报告** | 工作报告、调研报告、分析报告、可行性报告 | 封面、目录、章节标题、图表 |
| **简历** | 中式求职简历 | 照片位、个人信息表、工作经历 |
| **方案/计划** | 项目方案、实施计划、营销方案 | 背景、目标、步骤、预算 |
| **论文** | 毕业论文、学术论文 | 封面、摘要、关键词、参考文献 |
| **信函** | 商业函件、邀请函、感谢信 | 抬头、正文、落款 |
| **表格文档** | 考勤表、登记表、审批表 | 多列表格、合并单元格 |

## 工作流程

### Step 1: 需求确认

确认以下信息：

- **文档类型**：合同/报告/简历/方案/论文/信函/其他
- **主要内容**：核心内容描述
- **特殊要求**：页面方向、字体偏好、是否需要封面/目录等

### Step 2: 内容撰写

根据文档类型撰写内容，遵循中文商务/学术写作规范。

### Step 3: 生成 .docx 文件

**先确保依赖已安装：**
```bash
pip install python-docx 2>/dev/null || pip3 install python-docx 2>/dev/null
```

**使用以下核心代码框架：**

```python
from docx import Document
from docx.shared import Pt, Mm, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

class DocxWriter:
    """通用中文docx文档生成器"""

    # 预置样式
    STYLES = {
        'title':    {'font': '方正小标宋简体', 'size': 22, 'bold': True,  'align': 'CENTER'},
        'heading1': {'font': '黑体',           'size': 18, 'bold': True,  'align': 'LEFT'},
        'heading2': {'font': '黑体',           'size': 16, 'bold': True,  'align': 'LEFT'},
        'heading3': {'font': '黑体',           'size': 14, 'bold': True,  'align': 'LEFT'},
        'body':     {'font': '仿宋_GB2312',    'size': 12, 'bold': False, 'align': 'JUSTIFY'},
        'body_song':{'font': '宋体',           'size': 12, 'bold': False, 'align': 'JUSTIFY'},
        'small':    {'font': '宋体',           'size': 10.5,'bold': False, 'align': 'LEFT'},
        'footer':   {'font': '宋体',           'size': 9,  'bold': False, 'align': 'CENTER'},
    }

    def __init__(self, page='A4', orientation='portrait', margins=None):
        self.doc = Document()
        section = self.doc.sections[0]

        # 页面设置
        if orientation == 'landscape':
            section.orientation = WD_ORIENT.LANDSCAPE
            section.page_width = Mm(297)
            section.page_height = Mm(210)
        else:
            section.page_width = Mm(210)
            section.page_height = Mm(297)

        # 边距（默认普通边距）
        m = margins or {'top': 25.4, 'bottom': 25.4, 'left': 31.8, 'right': 31.8}
        section.top_margin = Mm(m['top'])
        section.bottom_margin = Mm(m['bottom'])
        section.left_margin = Mm(m['left'])
        section.right_margin = Mm(m['right'])

    def add_text(self, text, style='body', space_before=0, space_after=0,
                 first_indent=None, line_spacing=None, color=None):
        """添加格式化段落"""
        s = self.STYLES.get(style, self.STYLES['body'])
        p = self.doc.add_paragraph()
        p.alignment = getattr(WD_ALIGN_PARAGRAPH, s['align'])
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if line_spacing:
            p.paragraph_format.line_spacing = Pt(line_spacing)
        if first_indent is not None:
            p.paragraph_format.first_line_indent = Pt(first_indent)
        elif style == 'body' or style == 'body_song':
            p.paragraph_format.first_line_indent = Pt(s['size'] * 2)

        run = p.add_run(text)
        run.font.size = Pt(s['size'])
        run.font.name = s['font']
        run._element.rPr.rFonts.set(qn('w:eastAsia'), s['font'])
        run.bold = s['bold']
        if color:
            run.font.color.rgb = RGBColor(*color)
        return p

    def add_table(self, headers, rows, col_widths=None, style='Table Grid'):
        """添加表格"""
        table = self.doc.add_table(rows=1 + len(rows), cols=len(headers), style=style)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # 表头
        for i, header in enumerate(headers):
            cell = table.rows[0].cells[i]
            cell.text = header
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(10.5)
                    run.font.name = '黑体'
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

        # 数据行
        for r_idx, row_data in enumerate(rows):
            for c_idx, cell_text in enumerate(row_data):
                cell = table.rows[r_idx + 1].cells[c_idx]
                cell.text = str(cell_text)
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in paragraph.runs:
                        run.font.size = Pt(10.5)
                        run.font.name = '宋体'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

        # 列宽
        if col_widths:
            for i, width in enumerate(col_widths):
                for row in table.rows:
                    row.cells[i].width = Mm(width)

        return table

    def add_page_break(self):
        """添加分页符"""
        self.doc.add_page_break()

    def add_cover(self, title, subtitle=None, org=None, date_str=None):
        """添加封面页"""
        # 上方留白
        for _ in range(6):
            self.doc.add_paragraph()

        self.add_text(title, 'title', space_after=20)
        if subtitle:
            self.add_text(subtitle, 'heading1', space_after=40)
        if org:
            self.add_text(org, 'heading2', space_after=10)
        if date_str:
            self.add_text(date_str, 'heading2')

        self.add_page_break()

    def add_toc_placeholder(self):
        """添加目录占位（需在WPS中更新域）"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('目  录')
        run.font.size = Pt(22)
        run.font.name = '黑体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        run.bold = True

        p2 = self.doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run('（请在WPS中右键此处 → 更新域 → 更新整个目录）')
        run2.font.size = Pt(10.5)
        run2.font.name = '宋体'
        run2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run2.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

        self.add_page_break()

    def save(self, filename):
        """保存文档"""
        self.doc.save(filename)
        return os.path.abspath(filename)
```

### Step 4: 各文档类型具体指引

#### 合同/协议

```text
结构：
  合同编号
  合同标题
  甲乙方信息（名称、地址、法定代表人、联系方式）
  鉴于条款（背景）
  正文条款（逐条编号）
  违约责任
  争议解决（仲裁/诉讼、管辖地）
  其他约定
  签署栏（甲方签章、乙方签章、日期）

注意：
  - 条款编号使用"第X条"格式
  - 金额须同时标注大小写
  - 日期格式：XXXX年XX月XX日
  - 签署栏左右分列（甲方左、乙方右）
```

#### 报告

```text
结构：
  封面（标题、编制单位、日期）
  目录
  正文章节（一、二、三…）
  结论/建议
  附件/附录

注意：
  - 章节标题层级清晰
  - 数据用表格或列表呈现
  - 图表需编号和标题
```

#### 简历（中式）

```text
结构：
  标题栏（姓名、照片位）
  基本信息表（性别、出生年月、民族、政治面貌、籍贯、学历、联系方式）
  求职意向
  教育背景
  工作经历
  项目经验
  技能特长
  自我评价

注意：
  - 照片位右上角 35mm×45mm
  - 基本信息用表格排列
  - 控制在1-2页
```

### Step 5: 交付

1. 生成 .docx 文件
2. 告知文件路径和大小
3. 提示用WPS打开检查
4. 按需调整

## 示例

```bash
# 生成一份劳动合同
/wps-docx-writer 合同 生成一份劳动合同，甲方为XX科技有限公司，合同期限3年

# 生成一份带封面的项目报告
/wps-docx-writer 报告 编写一份2026年Q1项目进度报告，需要封面和目录

# 生成一份中式简历
/wps-docx-writer 简历 生成一份软件工程师求职简历模板
```

输出：在当前目录生成对应的 `.docx` 文件，用WPS打开即可编辑。

## 格式参考

中文排版通用规范见 [../shared/chinese-typesetting.md](../shared/chinese-typesetting.md)。
python-docx 高级用法见 [reference/python-docx-advanced.md](reference/python-docx-advanced.md)。
