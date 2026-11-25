---
name: wps-courseware
description: |
  教学课件制作。老师和培训师的做课件助手，按照"导入→新授→练习→总结"的
  教学设计结构自动生成课件PPT，帮你拆解知识点、设计互动环节、生成练习题。
  用于帮助教师快速制作课件。当用户提到课件、教学PPT、培训材料时触发。
  Courseware maker for teachers with structured lesson design.
license: MIT
user-invocable: true
argument-hint: '[学科/课题/年级]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 教学课件制作
  description_zh: 按教学结构生成课件PPT，包含导入、新授、练习、总结等环节
  tags:
    - 课件
    - 教学
    - 教育
    - PPT
    - WPS
  version: 1.0.1
  license: MIT
---

# 课件制作工具

教学目标 → 知识点拆解 → 结构化课件 → 含互动和练习。

> 让老师专注教学设计，排版交给工具。

## When to Use

- 教师制作教学课件
- 企业培训师做培训PPT
- 需要含练习题/互动环节的课件
- 用户说"帮我做个课件""这节课怎么讲"

## When NOT to Use

- 普通工作汇报PPT → 使用 `wps-ppt-gen`
- 只需PPT大纲 → 使用 `wps-ppt-outline`

## 课件结构（教学设计五步法）

```text
┌─ 导入（5min）── 情境/问题/故事引入
│
├─ 新授（15-20min）── 知识点讲解+案例
│  ├─ 知识点1 → 概念 → 示例 → 小结
│  ├─ 知识点2 → 概念 → 示例 → 小结
│  └─ 知识点3 → 概念 → 示例 → 小结
│
├─ 练习（10min）── 课堂练习+互动
│  ├─ 基础题（巩固）
│  ├─ 提高题（应用）
│  └─ 拓展题（创新）
│
├─ 总结（5min）── 知识框架回顾
│
└─ 作业（课后）── 布置任务
```

## 工作流程

### Step 1: 确认课件信息

- **学科/主题**：什么课
- **年级/对象**：学生or员工
- **课时**：一节课/两节课
- **教学目标**：学完要掌握什么
- **重难点**：哪些需要重点讲

### Step 2: 知识点拆解

将主题拆分为3-5个知识点，每个知识点：
- 概念定义（是什么）
- 原理解释（为什么）
- 案例示例（怎么用）
- 易错点（注意什么）

### Step 3: 生成课件PPT

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

def create_courseware(info, knowledge_points, output_path=None):
    """生成教学课件"""
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # 配色
    PRIMARY = RGBColor(0x1A, 0x73, 0xE8)
    DARK = RGBColor(0x20, 0x20, 0x20)
    LIGHT_BG = RGBColor(0xF0, 0xF4, 0xF8)

    def add_slide(title, content_items, slide_type='content'):
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
        # 标题
        txBox = slide.shapes.add_textbox(
            Inches(0.8), Inches(0.4), Inches(11), Inches(1))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = PRIMARY

        # 内容
        y = Inches(1.8)
        for item in content_items:
            txBox = slide.shapes.add_textbox(
                Inches(1.2), y, Inches(10), Inches(0.6))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = item
            p.font.size = Pt(20)
            p.font.color.rgb = DARK
            y += Inches(0.7)

        return slide

    # 封面
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    txBox = slide.shapes.add_textbox(
        Inches(2), Inches(2.5), Inches(9), Inches(1.5))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = info['title']
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.alignment = PP_ALIGN.CENTER

    sub = tf.add_paragraph()
    sub.text = f"{info.get('subject','')}  {info.get('grade','')}"
    sub.font.size = Pt(20)
    sub.font.color.rgb = DARK
    sub.alignment = PP_ALIGN.CENTER

    # 教学目标页
    add_slide('教学目标', [
        f"知识目标：{info.get('knowledge_goal', '掌握核心概念')}",
        f"能力目标：{info.get('ability_goal', '能够运用所学解决问题')}",
        f"情感目标：{info.get('emotion_goal', '培养学习兴趣')}",
        f"重点：{info.get('key_point', '')}",
        f"难点：{info.get('difficulty', '')}",
    ])

    # 知识点页
    for i, kp in enumerate(knowledge_points, 1):
        add_slide(f"{i}. {kp['title']}", kp.get('points', []))
        if kp.get('example'):
            add_slide(f"案例：{kp['title']}", kp['example'])

    # 练习页
    add_slide('课堂练习', [
        '1. （基础题）...',
        '2. （提高题）...',
        '3. （拓展题）...',
    ])

    # 总结页
    add_slide('课堂小结', [
        f"核心知识点：{len(knowledge_points)}个",
    ] + [f"  {i+1}. {kp['title']}" for i, kp in enumerate(knowledge_points)])

    if not output_path:
        output_path = f"{info['title']}_课件.pptx"
    prs.save(output_path)
    return os.path.abspath(output_path)
```

### Step 4: 课件设计规范

```text
字体：标题32pt 正文20-24pt（教室投影要大）
每页文字≤5行（学生注意力有限）
配图多文字少（视觉化教学）
每15分钟一个互动点（保持注意力）
颜色≤3种（不分散注意力）
动画：适度使用逐条显示（控制教学节奏）
```

### Step 5: 交付

1. 生成课件PPT文件
2. 包含教学目标、知识点、练习、总结完整结构
3. 建议教学时间分配

## 示例

```bash
# 制作课件
/wps-courseware 帮我做一个初中数学"一元二次方程"的课件，2课时

# 培训课件
/wps-courseware Excel基础操作培训课件，面向新员工，1小时

# 指定结构
/wps-courseware 高中英语阅读理解技巧，重点讲略读和精读
```
