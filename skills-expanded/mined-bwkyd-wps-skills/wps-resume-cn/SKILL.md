---
name: wps-resume-cn
description: |
  中式简历生成。生成带照片栏、政治面貌、民族的中国式简历Word文档，
  经典表格/简约现代/校招清新/高管精英四种模板，STAR法则帮你写工作经历。
  用于帮助用户生成简历。当用户提到简历、求职、CV时触发。
  Chinese-style resume generator with photo placeholder and multiple templates.
license: MIT
user-invocable: true
argument-hint: '[个人信息/目标岗位]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 中式简历生成
  description_zh: 生成带照片栏的中国式简历，支持经典表格、简约现代等模板
  tags:
    - 简历
    - 求职
    - python-docx
    - WPS
    - HR
  version: 1.0.1
  license: MIT
---

# 中式简历生成器

输入个人信息 → 生成排版精美的中国式求职简历（.docx）。

## When to Use

- 用户需要制作求职简历
- 用户说"帮我写/做一份简历"
- 用户需要简历模板
- 用户需要优化已有简历的排版

## When NOT to Use

- 需要英文/国际格式简历 → 使用 `wps-docx-writer`
- 需要写求职信/Cover Letter → 使用 `wps-docx-writer`

## 模板风格

```text
┌───────────────────────────────────────────┐
│        简历模板选择                        │
├───────────────────────────────────────────┤
│  [1] 📋 经典表格式  传统中国式表格简历     │
│  [2] 📄 简约现代式  左右分栏+色块装饰     │
│  [3] 🎓 校招清新式  适合应届生+浅色系     │
│  [4] 💼 高管精英式  深色侧边栏+极简       │
└───────────────────────────────────────────┘
```

## 工作流程

### Step 1: 收集信息

**基本信息（必填）：**
- 姓名
- 联系方式（手机号、邮箱）
- 求职意向（目标岗位）

**中国特色字段（酌情填写）：**
- 性别、出生年月
- 民族、政治面貌
- 籍贯、现居城市
- 最高学历、毕业院校
- 婚姻状况（可选）

**内容板块：**
- 教育背景（学校、专业、时间、GPA）
- 工作经历（公司、职位、时间、职责和成果）
- 项目经验（项目名、角色、技术栈、成果）
- 技能特长
- 证书荣誉
- 自我评价

### Step 2: 优化内容

**简历写作原则：**

```text
✅ 用数字量化成果：
  ❌ "提升了用户体验"
  ✅ "优化用户注册流程，转化率提升32%，日均注册量从500增至660"

✅ 用STAR法则写经历：
  Situation（背景）→ Task（任务）→ Action（行动）→ Result（成果）

✅ 动词开头：
  负责、主导、设计、开发、优化、推动、达成、搭建、统筹、协调

❌ 避免：
  - 空泛描述（认真负责、吃苦耐劳）
  - 无关经历
  - 错别字
  - 超过2页
```

### Step 3: 生成 .docx 文件

```bash
pip install python-docx 2>/dev/null || pip3 install python-docx 2>/dev/null
```

**排版规范：**

```text
纸张：A4
页边距：上下2cm，左右2cm（紧凑排版）
照片位：右上角，25mm × 35mm（一寸照）
姓名：22pt 黑体
模块标题：14pt 黑体，带下划线或色块
正文：11pt 宋体，行距1.3倍
时间线：右对齐，灰色
总长度：1页（应届生），1-2页（有经验者）
```

**经典表格式模板结构：**

```python
from docx import Document
from docx.shared import Pt, Mm, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def create_resume(info, output_path=None):
    """
    info = {
        'name': '张三',
        'phone': '13800138000',
        'email': 'zhangsan@email.com',
        'target': '软件工程师',
        'gender': '男',
        'birth': '1995年6月',
        'ethnicity': '汉族',
        'political': '中共党员',
        'origin': '浙江杭州',
        'city': '上海',
        'education': '硕士',
        'school': '浙江大学',
        'education_list': [
            {'school': '浙江大学', 'major': '计算机科学', 'degree': '硕士',
             'time': '2018.09-2021.06', 'gpa': '3.8/4.0'},
        ],
        'work_list': [
            {'company': 'XX科技有限公司', 'position': '高级工程师',
             'time': '2021.07-至今', 'duties': [
                 '主导核心系统重构，性能提升40%',
                 '带领5人团队完成XX项目',
             ]},
        ],
        'skills': ['Python', 'Java', 'SQL', '项目管理'],
        'certificates': ['PMP', 'CET-6'],
        'self_eval': '5年软件开发经验，擅长系统架构设计...',
    }
    """
    doc = Document()
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

    def set_font(run, name='宋体', size=11, bold=False, color=None):
        run.font.size = Pt(size)
        run.font.name = name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
        run.bold = bold
        if color:
            run.font.color.rgb = color

    def add_section_title(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(title)
        set_font(run, '黑体', 14, True, RGBColor(0x2B, 0x57, 0x9A))
        # 底部线
        pPr = p._element.get_or_add_pPr()
        pBdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'  <w:bottom w:val="single" w:sz="8" w:space="2" '
            f'w:color="2B579A"/>'
            f'</w:pBdr>'
        )
        pPr.append(pBdr)

    # === 姓名 ===
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(info['name'])
    set_font(run, '黑体', 22, True)

    # === 联系信息 ===
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    contact = f"{info.get('phone','')}  |  {info.get('email','')}  |  {info.get('city','')}"
    run = p.add_run(contact)
    set_font(run, '宋体', 10, False, RGBColor(0x66, 0x66, 0x66))

    # === 求职意向 ===
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"求职意向：{info.get('target','')}")
    set_font(run, '宋体', 11, True)

    # === 基本信息表 ===
    if any(info.get(k) for k in ['gender','birth','ethnicity','political','origin','education']):
        add_section_title('基本信息')
        fields = [
            ('性别', info.get('gender','')),
            ('出生年月', info.get('birth','')),
            ('民族', info.get('ethnicity','')),
            ('政治面貌', info.get('political','')),
            ('籍贯', info.get('origin','')),
            ('学历', info.get('education','')),
        ]
        fields = [(k,v) for k,v in fields if v]
        # 两列排列
        table = doc.add_table(rows=(len(fields)+1)//2, cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, (label, value) in enumerate(fields):
            row = i // 2
            col_start = (i % 2) * 2
            cell_l = table.cell(row, col_start)
            cell_v = table.cell(row, col_start + 1)
            cell_l.text = label
            cell_v.text = value
            for c in [cell_l, cell_v]:
                for p in c.paragraphs:
                    for r in p.runs:
                        set_font(r, '宋体', 10.5)

    # === 教育背景 ===
    if info.get('education_list'):
        add_section_title('教育背景')
        for edu in info['education_list']:
            p = doc.add_paragraph()
            run = p.add_run(f"{edu['school']}  |  {edu['major']}  |  {edu['degree']}")
            set_font(run, '宋体', 11, True)
            run2 = p.add_run(f"    {edu['time']}")
            set_font(run2, '宋体', 10, False, RGBColor(0x99, 0x99, 0x99))
            if edu.get('gpa'):
                p2 = doc.add_paragraph()
                run3 = p2.add_run(f"GPA: {edu['gpa']}")
                set_font(run3, '宋体', 10)

    # === 工作经历 ===
    if info.get('work_list'):
        add_section_title('工作经历')
        for work in info['work_list']:
            p = doc.add_paragraph()
            run = p.add_run(f"{work['company']}  |  {work['position']}")
            set_font(run, '宋体', 11, True)
            run2 = p.add_run(f"    {work['time']}")
            set_font(run2, '宋体', 10, False, RGBColor(0x99, 0x99, 0x99))
            for duty in work.get('duties', []):
                p2 = doc.add_paragraph()
                p2.paragraph_format.left_indent = Cm(0.5)
                run3 = p2.add_run(f"• {duty}")
                set_font(run3, '宋体', 10.5)

    # === 技能特长 ===
    if info.get('skills'):
        add_section_title('技能特长')
        p = doc.add_paragraph()
        run = p.add_run('  |  '.join(info['skills']))
        set_font(run, '宋体', 10.5)

    # === 自我评价 ===
    if info.get('self_eval'):
        add_section_title('自我评价')
        p = doc.add_paragraph()
        run = p.add_run(info['self_eval'])
        set_font(run, '宋体', 10.5)

    # 保存
    if not output_path:
        output_path = f"{info['name']}_简历.docx"
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 4: 交付

1. 生成 .docx 文件
2. 提示用WPS打开检查排版
3. 建议：添加一寸照片到预留位置
4. 按需调整内容和格式

## 示例

```bash
# 生成简历模板
/wps-resume-cn 软件工程师，3年经验，硕士，浙江大学

# 从详细信息生成
/wps-resume-cn 张三，男，1995年生，浙大计算机硕士，现在上海做高级工程师，想跳槽

# 应届生简历
/wps-resume-cn 应届生简历，2026届，北京大学，金融学本科，想进银行
```

## 参考

中文排版通用规范见 [../shared/chinese-typesetting.md](../shared/chinese-typesetting.md)。
