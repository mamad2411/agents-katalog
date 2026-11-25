---
name: wps-ppt-gen
description: |
  PPT生成。根据主题生成完整的PPT文件，
  包含封面、目录、内容页、总结页，支持多种风格。
  用于帮助用户生成PPT演示文稿。当用户提到PPT、演示文稿、幻灯片时触发。
  PPT presentation generator using python-pptx.
license: MIT
user-invocable: true
argument-hint: '[主题/场景] [页数(可选)]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: PPT生成
  description_zh: 根据主题生成完整的PPT文件，包含封面、目录、内容页和总结页
  tags:
    - PPT
    - 演示
    - python-pptx
    - WPS
    - 幻灯片
  version: 1.0.2
  license: MIT
---

# WPS PPT 生成器

从主题大纲 → 自动生成完整的精美 PPT（.pptx）。

## When to Use

- 用户需要制作PPT/演示文稿
- 用户说"帮我做一个PPT"
- 用户需要述职报告/项目汇报/产品介绍/培训课件等PPT
- 用户有内容大纲想转成PPT

## When NOT to Use

- 只需要PPT大纲不需要文件 → 使用 `wps-ppt-outline`
- 已有PPT需要美化 → 使用 `wps-ppt-polish`
- 需要教学课件特殊排版 → 使用 `wps-courseware`

## 风格选择菜单

```text
┌─────────────────────────────────────────────┐
│        WPS PPT 风格选择                      │
├─────────────────────────────────────────────┤
│                                             │
│  [1] 📊 简约商务  白底+深色文字+蓝色强调    │
│  [2] 🚀 科技风    深色底+渐变+几何元素       │
│  [3] 🏛️ 党政风    红色主调+庄重+国徽元素     │
│  [4] 📚 教育风    清新+活泼配色+图文混排     │
│  [5] 🎨 创意风    大图背景+极简文字          │
│  [6] 📈 数据风    图表为主+数据驱动          │
│                                             │
│  输入编号或风格名称选择                      │
└─────────────────────────────────────────────┘
```

## 工作流程

### Step 1: 确认需求

- **主题**：PPT的主题是什么？
- **场景**：述职/汇报/产品/培训/竞标/其他？
- **页数**：期望多少页？（默认15-20页）
- **风格**：从上方菜单选择（默认简约商务）
- **特殊要求**：是否需要图表？是否有固定模板？

### Step 2: 生成大纲

根据场景生成PPT结构大纲：

**述职报告（推荐15-20页）：**
```text
1. 封面（标题+姓名+部门+日期）
2. 目录
3-4. 工作回顾（KPI完成情况）
5-7. 重点项目（每项1-2页）
8-9. 数据成果（图表页）
10-11. 经验总结与反思
12-13. 下阶段计划
14. 需要的支持
15. 感谢页
```

**项目汇报（推荐12-15页）：**
```text
1. 封面
2. 目录
3. 项目背景
4-5. 项目目标与范围
6-8. 实施进展（里程碑）
9-10. 关键成果/数据
11. 风险与问题
12. 下一步计划
13. 时间表
14. 资源需求
15. Q&A
```

**产品介绍（推荐10-15页）：**
```text
1. 封面（产品名+Slogan）
2. 痛点/市场背景
3. 解决方案概览
4-6. 核心功能（每项1页）
7. 竞品对比
8-9. 客户案例/数据
10. 定价方案
11. 合作流程
12. 联系方式
```

### Step 3: 生成 .pptx 文件

**确保依赖：**
```bash
pip install python-pptx 2>/dev/null || pip3 install python-pptx 2>/dev/null
```

**核心代码框架：**

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Mm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

class PPTGenerator:
    """中式PPT生成器"""

    # 预置风格配色
    THEMES = {
        'business': {
            'name': '简约商务',
            'bg': RGBColor(0xFF, 0xFF, 0xFF),
            'title': RGBColor(0x1F, 0x38, 0x64),
            'accent': RGBColor(0x2B, 0x57, 0x9A),
            'text': RGBColor(0x33, 0x33, 0x33),
            'light': RGBColor(0xE8, 0xEE, 0xF7),
            'title_font': '微软雅黑',
            'body_font': '微软雅黑',
        },
        'tech': {
            'name': '科技风',
            'bg': RGBColor(0x0A, 0x1A, 0x2F),
            'title': RGBColor(0xFF, 0xFF, 0xFF),
            'accent': RGBColor(0x00, 0xD4, 0xFF),
            'text': RGBColor(0xCC, 0xCC, 0xCC),
            'light': RGBColor(0x15, 0x2A, 0x45),
            'title_font': '微软雅黑',
            'body_font': '微软雅黑',
        },
        'gov': {
            'name': '党政风',
            'bg': RGBColor(0xFF, 0xFF, 0xFF),
            'title': RGBColor(0xCC, 0x00, 0x00),
            'accent': RGBColor(0xCC, 0x00, 0x00),
            'text': RGBColor(0x33, 0x33, 0x33),
            'light': RGBColor(0xFF, 0xE8, 0xE8),
            'title_font': '方正小标宋简体',
            'body_font': '仿宋_GB2312',
        },
        'edu': {
            'name': '教育风',
            'bg': RGBColor(0xFF, 0xFF, 0xFF),
            'title': RGBColor(0x2E, 0x75, 0xB6),
            'accent': RGBColor(0x4C, 0xAF, 0x50),
            'text': RGBColor(0x33, 0x33, 0x33),
            'light': RGBColor(0xE3, 0xF2, 0xFD),
            'title_font': '微软雅黑',
            'body_font': '微软雅黑',
        },
    }

    def __init__(self, theme='business', widescreen=True):
        self.prs = Presentation()
        self.theme = self.THEMES.get(theme, self.THEMES['business'])

        # 宽屏16:9（默认）或4:3
        if widescreen:
            self.prs.slide_width = Mm(338.67)
            self.prs.slide_height = Mm(190.5)
        else:
            self.prs.slide_width = Mm(254)
            self.prs.slide_height = Mm(190.5)

        self.slide_width = self.prs.slide_width
        self.slide_height = self.prs.slide_height

    def add_bg(self, slide, color=None):
        """设置幻灯片背景色"""
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color or self.theme['bg']

    def add_shape(self, slide, left, top, width, height, color=None):
        """添加色块装饰"""
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left, top, width, height
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = color or self.theme['accent']
        shape.line.fill.background()
        return shape

    def add_text_box(self, slide, left, top, width, height, text,
                     font_size=18, font_color=None, font_name=None,
                     bold=False, alignment=PP_ALIGN.LEFT):
        """添加文本框"""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.color.rgb = font_color or self.theme['text']
        p.font.name = font_name or self.theme['body_font']
        p.font.bold = bold
        p.alignment = alignment
        return txBox

    def add_cover(self, title, subtitle='', author='', date=''):
        """封面页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # 空白
        self.add_bg(slide)

        # 左侧装饰条
        self.add_shape(slide, Mm(0), Mm(0), Mm(12), self.slide_height)

        # 标题
        self.add_text_box(
            slide, Mm(30), Mm(50), Mm(280), Mm(50), title,
            font_size=36, font_color=self.theme['title'],
            font_name=self.theme['title_font'], bold=True,
            alignment=PP_ALIGN.LEFT
        )

        # 副标题
        if subtitle:
            self.add_text_box(
                slide, Mm(30), Mm(105), Mm(280), Mm(30), subtitle,
                font_size=20, font_color=self.theme['accent']
            )

        # 作者+日期
        info = f'{author}    {date}' if author else date
        if info.strip():
            self.add_text_box(
                slide, Mm(30), Mm(150), Mm(280), Mm(20), info,
                font_size=14, font_color=self.theme['text']
            )

    def add_toc(self, items):
        """目录页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self.add_bg(slide)

        self.add_text_box(
            slide, Mm(30), Mm(15), Mm(100), Mm(20), '目录',
            font_size=28, font_color=self.theme['title'],
            font_name=self.theme['title_font'], bold=True
        )

        # 装饰线
        self.add_shape(slide, Mm(30), Mm(40), Mm(60), Mm(2))

        for i, item in enumerate(items):
            y = Mm(55 + i * 22)
            # 序号
            num_shape = self.add_shape(
                slide, Mm(30), y, Mm(10), Mm(10),
                self.theme['accent']
            )
            num_shape.text_frame.paragraphs[0].text = str(i + 1).zfill(2)
            num_shape.text_frame.paragraphs[0].font.size = Pt(11)
            num_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            num_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

            # 标题
            self.add_text_box(
                slide, Mm(48), y, Mm(250), Mm(15), item,
                font_size=16, bold=False
            )

    def add_content_slide(self, title, bullets, note=''):
        """内容页（标题+要点列表）"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self.add_bg(slide)

        # 标题区
        self.add_shape(slide, Mm(0), Mm(0), self.slide_width, Mm(40),
                       self.theme['light'])
        self.add_text_box(
            slide, Mm(30), Mm(8), Mm(280), Mm(25), title,
            font_size=24, font_color=self.theme['title'],
            font_name=self.theme['title_font'], bold=True
        )

        # 要点列表
        for i, bullet in enumerate(bullets):
            y = Mm(55 + i * 25)
            # 圆点
            self.add_shape(slide, Mm(30), y + Mm(4), Mm(4), Mm(4),
                          self.theme['accent'])
            # 文本
            self.add_text_box(
                slide, Mm(40), y, Mm(270), Mm(20), bullet,
                font_size=16
            )

    def add_thank_slide(self, text='感谢聆听', subtext='THANK YOU'):
        """感谢页"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self.add_bg(slide)

        self.add_text_box(
            slide, Mm(0), Mm(60), self.slide_width, Mm(40), text,
            font_size=44, font_color=self.theme['title'],
            font_name=self.theme['title_font'], bold=True,
            alignment=PP_ALIGN.CENTER
        )
        self.add_text_box(
            slide, Mm(0), Mm(110), self.slide_width, Mm(20), subtext,
            font_size=18, font_color=self.theme['accent'],
            alignment=PP_ALIGN.CENTER
        )

    def save(self, filename):
        self.prs.save(filename)
        return os.path.abspath(filename)
```

### Step 4: 交付

1. 生成 .pptx 文件
2. 告知页数和文件大小
3. 提示用WPS演示打开
4. 可根据反馈调整内容或风格

## 排版黄金法则

```text
1. 每页核心信息不超过3点
2. 标题不超过15字
3. 正文字号不小于18pt
4. 每页文字不超过100字
5. 留白 ≥ 40%
6. 配色不超过3种
7. 字体不超过2种
8. 图片和文字比例 6:4 或 7:3
```

## 示例

```bash
# 生成述职报告PPT
/wps-ppt-gen 2026年Q1述职报告，销售部张三，科技风

# 生成产品介绍PPT
/wps-ppt-gen 新产品"智慧办公系统"介绍PPT，15页，简约商务风

# 生成培训课件
/wps-ppt-gen Python入门培训课件，教育风
```

## 参考

PPT设计原则详见 [reference/ppt-design-rules.md](reference/ppt-design-rules.md)。
