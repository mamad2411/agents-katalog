---
name: wps-thesis
description: |
  毕业论文排版。按高校标准生成论文文档，包含封面、中英文摘要、
  目录、正文章节、参考文献(GB/T 7714)、致谢等完整结构。
  用于帮助学生排版毕业论文。当用户提到论文、毕业论文、论文排版时触发。
  Academic thesis formatter.
license: MIT
user-invocable: true
argument-hint: '[论文标题/内容] [学校名称(可选)]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 毕业论文排版
  description_zh: 按高校标准排版毕业论文，包含封面、摘要、目录、参考文献等
  tags:
    - 论文
    - 毕业论文
    - 学术
    - python-docx
    - WPS
  version: 1.0.2
  license: MIT
---

# 论文排版工具

按高校标准自动排版毕业论文 / 学术论文（.docx）。

> **每个大学生的论文排版噩梦，到此为止。**

## When to Use

- 毕业论文排版（本科/硕士/博士）
- 学术论文/期刊论文格式化
- 论文模板生成
- 已有论文内容需要重新排版

## When NOT to Use

- 一般工作报告 → 使用 `wps-report-writer`
- 公文排版 → 使用 `wps-gongwen`
- 只需要校对内容 → 使用 `wps-proofread`

## 论文通用格式标准

### 页面设置

```text
纸张：A4 (210mm × 297mm)
上边距：30mm
下边距：25mm
左边距：30mm（装订侧加宽）
右边距：20mm
页眉：15mm，含学校名/论文标题
页脚：页码居中，小五号
```

### 字体字号规范

| 元素 | 字体 | 字号 | 说明 |
|------|------|------|------|
| 论文题目 | 黑体 | 小二号(18pt) | 居中，加粗 |
| 章标题（第X章） | 黑体 | 三号(16pt) | 居中，加粗 |
| 节标题（X.X） | 黑体 | 四号(14pt) | 左对齐，加粗 |
| 小节标题（X.X.X） | 黑体 | 小四号(12pt) | 左对齐，加粗 |
| 正文 | 宋体 | 小四号(12pt) | 首行缩进2字符 |
| 摘要标题 | 黑体 | 三号(16pt) | 居中 |
| 摘要内容 | 宋体 | 小四号(12pt) | |
| 关键词 | 黑体+宋体 | 小四号(12pt) | "关键词："黑体，内容宋体 |
| 参考文献 | 宋体 | 五号(10.5pt) | |
| 页眉 | 宋体 | 小五号(9pt) | |
| 页码 | Times New Roman | 小五号(9pt) | |

### 行距

```text
正文：1.5倍行距
摘要：1.5倍行距
参考文献：单倍行距
图表标题：单倍行距
```

## 工作流程

### Step 1: 确认论文信息

**必填信息：**
- **论文题目**（中文 + 英文）
- **作者姓名**
- **学校/院系**
- **专业**
- **指导教师**
- **日期**
- **学位类型**：本科/硕士/博士

**可选信息：**
- 学号
- 分类号
- 密级
- UDC

### Step 2: 论文结构

**标准毕业论文结构：**

```text
[封面]
[独创性声明]
[中文摘要 + 关键词]
[英文摘要 + Keywords]
[目录]
──────────────────
第一章  绪论
  1.1 研究背景
  1.2 研究现状
  1.3 研究内容与方法
  1.4 论文结构
第二章  相关理论与技术
  2.1 ...
第三章  系统设计 / 方法论
  3.1 ...
第四章  实验与分析
  4.1 ...
第五章  总结与展望
  5.1 主要工作总结
  5.2 不足与展望
──────────────────
[参考文献]
[致谢]
[附录]（可选）
[个人简历/发表论文]（硕博）
```

### Step 3: 生成 .docx 文件

```bash
pip install python-docx 2>/dev/null || pip3 install python-docx 2>/dev/null
```

**核心生成逻辑：**

```python
from docx import Document
from docx.shared import Pt, Mm, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement
import os

def create_thesis(info, content=None, output_path=None):
    """
    info = {
        'title_cn': '基于深度学习的图像识别系统研究',
        'title_en': 'Research on Image Recognition System Based on Deep Learning',
        'author': '张三',
        'school': 'XX大学',
        'department': '计算机科学与技术学院',
        'major': '计算机科学与技术',
        'advisor': '李四 教授',
        'degree': '硕士',  # 本科/硕士/博士
        'student_id': '2023XXXX',
        'date': '2026年6月',
    }
    """
    doc = Document()

    # 页面设置
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(30)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(30)
    section.right_margin = Mm(20)

    def set_font(run, name='宋体', size=12, bold=False, color=None):
        run.font.size = Pt(size)
        run.font.name = name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
        run.bold = bold
        if color:
            run.font.color.rgb = color

    def add_heading_cn(text, font_name='黑体', size=16, bold=True,
                       align=WD_ALIGN_PARAGRAPH.CENTER):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(18)
        p.paragraph_format.line_spacing = Pt(28)
        run = p.add_run(text)
        set_font(run, font_name, size, bold)
        return p

    def add_body(text, indent=True):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = Pt(22)
        if indent:
            p.paragraph_format.first_line_indent = Pt(24)
        run = p.add_run(text)
        set_font(run, '宋体', 12)
        return p

    # === 封面 ===
    for _ in range(3):
        doc.add_paragraph()

    # 学校名
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(info['school'])
    set_font(run, '华文中宋', 26, True)

    # 学位类型
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    degree_text = {'本科': '本科毕业论文', '硕士': '硕士学位论文',
                   '博士': '博士学位论文'}.get(info['degree'], '学位论文')
    run = p.add_run(degree_text)
    set_font(run, '华文中宋', 22)

    doc.add_paragraph()

    # 论文题目
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(30)
    run = p.add_run(info['title_cn'])
    set_font(run, '黑体', 18, True)

    doc.add_paragraph()

    # 信息表
    fields = [
        ('作    者', info['author']),
        ('学    号', info.get('student_id', '')),
        ('院    系', info.get('department', '')),
        ('专    业', info['major']),
        ('指导教师', info['advisor']),
        ('完成日期', info['date']),
    ]
    for label, value in fields:
        if value:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run1 = p.add_run(f'{label}：')
            set_font(run1, '宋体', 14)
            run2 = p.add_run(value)
            set_font(run2, '宋体', 14)

    doc.add_page_break()

    # === 中文摘要 ===
    add_heading_cn('摘  要', '黑体', 16)
    add_body('（在此输入中文摘要内容，一般300-500字）')
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('关键词：')
    set_font(run, '黑体', 12, True)
    run2 = p.add_run('关键词1；关键词2；关键词3')
    set_font(run2, '宋体', 12)
    doc.add_page_break()

    # === 英文摘要 ===
    add_heading_cn('Abstract', 'Times New Roman', 16)
    add_body('(Type your English abstract here, typically 200-300 words)')
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('Keywords: ')
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.bold = True
    run2 = p.add_run('keyword1; keyword2; keyword3')
    run2.font.size = Pt(12)
    run2.font.name = 'Times New Roman'
    doc.add_page_break()

    # === 目录占位 ===
    add_heading_cn('目  录', '黑体', 16)
    add_body('（请在WPS中插入 → 引用 → 目录 → 自动目录）', False)
    doc.add_page_break()

    # === 正文章节框架 ===
    chapters = [
        ('第一章  绪论', ['1.1 研究背景', '1.2 国内外研究现状',
         '1.3 研究内容与方法', '1.4 论文结构安排']),
        ('第二章  相关理论与技术', ['2.1 （根据论文主题填写）']),
        ('第三章  （核心内容章节）', ['3.1 （根据论文主题填写）']),
        ('第四章  实验与结果分析', ['4.1 实验环境', '4.2 实验设计',
         '4.3 结果与分析']),
        ('第五章  总结与展望', ['5.1 主要工作总结', '5.2 不足与展望']),
    ]

    for chapter_title, sections in chapters:
        add_heading_cn(chapter_title, '黑体', 16)
        for sec in sections:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            run = p.add_run(sec)
            set_font(run, '黑体', 14, True)
            add_body('（在此输入内容）')
        doc.add_page_break()

    # === 参考文献 ===
    add_heading_cn('参考文献', '黑体', 16)
    refs = [
        '[1] 作者. 论文题目[J]. 期刊名, 年, 卷(期): 起止页.',
        '[2] 作者. 书名[M]. 出版地: 出版社, 年.',
        '[3] Author. Title[J]. Journal, Year, Vol(No): Pages.',
    ]
    for ref in refs:
        p = doc.add_paragraph()
        run = p.add_run(ref)
        set_font(run, '宋体', 10.5)
    doc.add_page_break()

    # === 致谢 ===
    add_heading_cn('致  谢', '黑体', 16)
    add_body('（在此输入致谢内容）')

    # 保存
    if not output_path:
        output_path = f"{info['title_cn'][:20]}_论文.docx"
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 4: 交付

1. 生成 .docx 论文框架
2. 提示用户填充各章节内容
3. 提醒在WPS中插入自动目录
4. 建议使用WPS的样式功能维护标题层级

## 参考文献格式（GB/T 7714-2015）

```text
[期刊]  作者. 题名[J]. 刊名, 出版年, 卷(期): 起止页码.
[图书]  作者. 书名[M]. 版次. 出版地: 出版者, 出版年: 页码.
[学位论文] 作者. 题名[D]. 保存地: 保存单位, 年份.
[会议论文] 作者. 题名[C]//会议录. 出版地: 出版者, 年: 页码.
[网络文献] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
[专利]  申请者. 专利名[P]. 专利国: 专利号, 公告日期.
[标准]  标准号. 标准名称[S]. 出版地: 出版者, 年份.
```

## 示例

```bash
# 生成论文模板
/wps-thesis 基于深度学习的图像识别系统研究，硕士论文，浙江大学计算机学院

# 只要框架
/wps-thesis 帮我生成一份本科毕业论文的排版模板，题目是"中小企业数字化转型研究"

# 排版已有内容
/wps-thesis 帮我把 draft.md 的论文内容排版成标准格式的docx
```
