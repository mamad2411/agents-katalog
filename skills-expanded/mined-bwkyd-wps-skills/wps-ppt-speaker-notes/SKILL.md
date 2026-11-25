---
name: wps-ppt-speaker-notes
description: |
  PPT演讲稿生成。PPT内容写好了但不知道上台怎么讲？帮你根据每页内容
  自动生成演讲稿写入备注区，标注每页讲多久，还有开场过渡结尾的话术建议。
  用于帮助演讲者准备演讲内容。当用户提到演讲稿、PPT备注、怎么讲PPT时触发。
  Generates speaker notes for each PPT slide with timing estimates.

license: MIT
user-invocable: true
argument-hint: "[PPT文件路径/演讲需求]"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
metadata:
  author: BWKYD
  version: 1.0.0
  title: PPT演讲备注
  description_zh: 为每页PPT生成演讲备注，包含讲解要点和建议时长
  tags:
    - PPT
    - 演讲
    - 备注
    - 演讲稿
    - WPS
  license: MIT
---

# PPT演讲备注生成器

PPT内容 → 逐页演讲稿 → 写入备注区 → 自信开讲。

> PPT做好了，但不知道怎么讲？交给我。

## When to Use

- PPT做好了需要准备演讲稿
- 需要给每页PPT写备注
- 演讲前需要理清讲解逻辑
- 用户说"帮我写演讲稿""这个PPT怎么讲"

## When NOT to Use

- 制作PPT → 使用 `wps-ppt-gen`
- PPT大纲 → 使用 `wps-ppt-outline`

## 演讲备注结构

```text
每页备注包含：
┌─────────────────────────────┐
│ 【开场/过渡】               │
│ "接下来我们看一下..."       │
│                             │
│ 【核心要点】                │
│ · 要点1 — 展开说明          │
│ · 要点2 — 数据支撑          │
│ · 要点3 — 案例/故事         │
│                             │
│ 【过渡到下一页】            │
│ "那么基于这个情况..."       │
│                             │
│ ⏱ 建议时长：1.5分钟         │
└─────────────────────────────┘
```

## 工作流程

### Step 1: 读取PPT内容

```python
from pptx import Presentation
from pptx.util import Inches, Pt
import os

def read_ppt_content(ppt_path):
    """读取PPT每页内容"""
    prs = Presentation(ppt_path)
    slides_content = []

    for i, slide in enumerate(prs.slides, 1):
        content = {'page': i, 'title': '', 'texts': [], 'has_chart': False,
                   'has_table': False, 'has_image': False}

        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if text:
                        if shape == slide.shapes.title:
                            content['title'] = text
                        else:
                            content['texts'].append(text)
            if shape.has_chart:
                content['has_chart'] = True
            if shape.has_table:
                content['has_table'] = True
            if shape.shape_type == 13:
                content['has_image'] = True

        slides_content.append(content)

    return slides_content


def write_speaker_notes(ppt_path, notes_list, output_path=None):
    """将演讲备注写入PPT"""
    prs = Presentation(ppt_path)

    for i, slide in enumerate(prs.slides):
        if i < len(notes_list):
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = notes_list[i]

    if not output_path:
        base, ext = os.path.splitext(ppt_path)
        output_path = f'{base}_with_notes{ext}'
    prs.save(output_path)
    return os.path.abspath(output_path)
```

### Step 2: 生成演讲备注

根据每页内容生成结构化演讲稿：

```text
演讲备注生成原则：
1. 开场白 — 不要直接念标题，用过渡语引入
2. 展开 — 每个要点用1-2句话解释
3. 数据/图表 — 描述趋势和关键数字，不要逐行念
4. 故事/案例 — 在关键页面穿插真实案例
5. 过渡 — 每页结尾自然过渡到下一页
6. 时间 — 标注建议时长，确保总时长合理
```

### Step 3: 演讲技巧备注

```text
封面页：自我介绍 + 今天讲什么 + 为什么重要（30秒）
数据页：先说结论 → 再指数据 → 解释含义（勿逐行念数字）
对比页：先说差异 → 再说原因 → 引出建议
总结页：回顾3个核心要点 → 明确下一步 → 感谢+Q&A
```

### Step 4: 交付

1. 生成含备注的PPT文件（备注写入每页Notes区域）
2. 或输出演讲稿文本（可打印带在手边）
3. 标注每页建议时长和总时长

## 示例

```bash
# 生成备注
/wps-ppt-speaker-notes 帮我给report.pptx每页写演讲备注

# 指定时长
/wps-ppt-speaker-notes 20分钟的演讲，帮我分配每页时间并写讲稿

# 输出文本
/wps-ppt-speaker-notes 把演讲稿导出为文本方便打印
```
