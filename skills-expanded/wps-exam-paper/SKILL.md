---
name: wps-exam-paper
description: |
  试卷排版。按标准格式排版考试试卷，包含密封线、评分栏、题号编排，
  支持选择题、填空题、判断题、简答题等题型。
  用于帮助教师制作考试试卷。当用户提到试卷、考试、出题时触发。
  Exam paper formatter.
license: MIT
user-invocable: true
argument-hint: '[学科/年级/考试类型]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 试卷排版
  description_zh: 按标准格式排版试卷，包含密封线、评分栏、题号等
  tags:
    - 试卷
    - 考试
    - 教育
    - python-docx
    - WPS
  version: 1.0.2
  license: MIT
---

# 试卷生成器

题目 → 规范排版 → 带密封线和评分栏的标准试卷。

> 老师出题最头疼的不是题目本身，而是排版。

## When to Use

- 制作期中/期末考试试卷
- 练习卷/测验卷
- 需要规范的试卷格式（密封线、评分表）
- 用户说"帮我做份试卷""出几道题"

## When NOT to Use

- 课件制作 → 使用 `wps-courseware`
- 普通文档 → 使用 `wps-docx-writer`

## 试卷格式标准

```text
┌──────────────────────────────────────────────┐
│ ┃ 姓   ┃                                    │
│ ┃ 名   ┃  XX学校 2025-2026学年第二学期       │
│ ┃ ：   ┃     【XX学科】期末考试试卷          │
│ ┃      ┃                                    │
│ ┃ 班   ┃  考试时间：120分钟  满分：100分     │
│ ┃ 级   ┃                                    │
│ ┃ ：   ┃  ┌────┬────┬────┬────┬────┬────┐  │
│ ┃      ┃  │题号│ 一 │ 二 │ 三 │ 四 │总分│  │
│ ┃ 学   ┃  ├────┼────┼────┼────┼────┼────┤  │
│ ┃ 号   ┃  │得分│    │    │    │    │    │  │
│ ┃ ：   ┃  └────┴────┴────┴────┴────┴────┘  │
│ ┃      ┃                                    │
│密封线  ┃  一、选择题（每小题3分，共30分）     │
│ ┃      ┃  1. 题目内容                        │
│ ┃      ┃     A. 选项A  B. 选项B              │
│ ┃      ┃     C. 选项C  D. 选项D              │
│ ┃      ┃                                    │
└──────────────────────────────────────────────┘
```

## 支持的题型

```text
[1] 选择题 → A/B/C/D 四选一，可设单选/多选
[2] 填空题 → 下划线留空
[3] 判断题 → 对(√) 错(×)
[4] 简答题 → 留答题空间
[5] 计算题 → 留解题步骤空间
[6] 作文/论述 → 留方格纸区域
[7] 连线题 → 左右匹配
[8] 材料分析 → 阅读材料+问题
```

## 工作流程

### Step 1: 确认试卷信息

- **学校名称**
- **学科/年级**
- **考试类型**（期中/期末/月考/模拟）
- **时间和分值**
- **题型和题量**

### Step 2: 生成试卷

```python
from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

def create_exam_paper(info, sections, output_path=None):
    """
    info = {
        'school': 'XX中学',
        'semester': '2025-2026学年第二学期',
        'subject': '数学',
        'exam_type': '期末考试',
        'duration': 120,
        'total_score': 100,
    }
    sections = [
        {'type': '选择题', 'score_each': 3, 'total': 30, 'questions': [...]},
        {'type': '填空题', 'score_each': 3, 'total': 15, 'questions': [...]},
    ]
    """
    doc = Document()
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(25)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)  # 留密封线空间
    section.right_margin = Mm(20)

    def set_font(run, name='宋体', size=12, bold=False):
        run.font.size = Pt(size)
        run.font.name = name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
        run.bold = bold

    # 标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(info['school'])
    set_font(run, '黑体', 10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"{info['semester']}")
    set_font(run, '宋体', 10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"【{info['subject']}】{info['exam_type']}试卷")
    set_font(run, '黑体', 16, True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        f"考试时间：{info['duration']}分钟    满分：{info['total_score']}分")
    set_font(run, '宋体', 10)

    # 评分表
    num_sections = len(sections)
    table = doc.add_table(rows=2, cols=num_sections + 2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ['题号'] + [f'{"一二三四五六七八九十"[i]}' for i in range(num_sections)] + ['总分']
    for i, h in enumerate(headers):
        table.cell(0, i).text = h
        table.cell(0, i).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.cell(1, 0).text = '得分'
    table.cell(1, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()  # 空行

    # 题目区域
    section_labels = "一二三四五六七八九十"
    q_num = 1
    for idx, sec in enumerate(sections):
        # 大题标题
        p = doc.add_paragraph()
        label = section_labels[idx]
        run = p.add_run(
            f"{label}、{sec['type']}（每小题{sec['score_each']}分，"
            f"共{sec['total']}分）")
        set_font(run, '黑体', 12, True)

        # 题目
        for q in sec.get('questions', []):
            p = doc.add_paragraph()
            run = p.add_run(f"{q_num}. {q.get('stem', '（题目内容）')}")
            set_font(run, '宋体', 11)
            p.paragraph_format.line_spacing = Pt(24)

            if sec['type'] == '选择题' and 'options' in q:
                p = doc.add_paragraph()
                opts = q['options']
                run = p.add_run(
                    f"    A. {opts[0]}    B. {opts[1]}    "
                    f"C. {opts[2]}    D. {opts[3]}")
                set_font(run, '宋体', 11)

            if sec['type'] in ['简答题', '计算题', '论述题']:
                for _ in range(4):
                    doc.add_paragraph()  # 答题空间

            q_num += 1

    if not output_path:
        output_path = f"{info['subject']}{info['exam_type']}试卷.docx"
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成试卷.docx文件
2. 可选：生成答案卷
3. 提醒教师检查题目和分值

## 示例

```bash
# 生成试卷
/wps-exam-paper 帮我做一份初三数学期末试卷，选择题10道填空题5道计算题3道

# 模板
/wps-exam-paper 生成一个空白的语文试卷模板

# 指定题目
/wps-exam-paper 把这些题目排成标准试卷格式
```
