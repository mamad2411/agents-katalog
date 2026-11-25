---
name: deck-web-converter
description: |
  将pitch deck PPT(.pptx)或PDF(.pdf)转换为精美的、响应式的、自包含HTML演示文稿。适合通过邮件、微信、二维码或浏览器分享路演材料，无需文件附件。
  Use when: "BP转网页", "PPT转HTML", "pitch deck online", "商业计划书在线演示", "把PPT变成网页", "生成HTML版BP", "pdf to html presentation", "网页版PPT", "在线演示文稿".
  输出单个离线可用的.html文件，支持幻灯片导航、键盘控制和移动端响应式。Cross-references: pitch-deck-creator, business-plan-ppt.
  Built by UniqueClub 🌐 https://uniqueclub.ai
license: MIT
---

# Deck Web Converter

> 将pitch deck文件(.pptx或.pdf)转换为精美的、响应式的单文件HTML演示文稿。

## When to Use

Use this skill when:
- 用户已有 `.pptx` 或 `.pdf` 文件，需要将其转为可分享的网页
- 用户需要通过邮件、微信、二维码或浏览器分享路演材料
- 用户需要在手机上查看PPT
- 用户需要在线演示文稿而非文件附件

Do NOT use this skill if:
- 用户需要从零创建BP → use `pitch-deck-creator` instead
- 用户需要编辑源PPT内容 → 先编辑再转换
- 输入文件缺失或不可读 → 询问正确的文件路径

Typical triggers:
- 「把PPT转成网页」「BP在线演示」「生成HTML版PPT」
- 「pitch deck转链接」「要在手机里看的PPT」「网页版路演材料」
- "convert pitch to web", "PPT to HTML", "share presentation online"

## Workflow

本工作流遵循六步推进法，共6个步骤：
1. **探查 (Probe)**：动手前先完整读取全部输入，确认目标和约束。
2. **约束 (Constrain)**：验证输入完整性，设定边界和不可降级的交付标准，受阻时换通道。
3. **证据 (Evidence)**：每个数字必须来自输入、具体信源或可复现计算，收集支撑数据。
4. **执行 (Execute)**：调用脚本/API/生成内容，先给影响与结论，再给行动和必要证据。
5. **验证 (Verify)**：用"可能失败"的动作验证——不同于生成路径的方式回读输出。
6. **交付 (Deliver)**：返回结果，清理临时文件。

### Step 1: 探查 (Probe)
确认输入文件路径。支持格式：
- `.pptx` — PowerPoint文件
- `.pdf` — PDF文件

如用户未提供文件路径，主动询问。

### Step 2: 约束 (Constrain)
设定输出边界：
- 输出必须为**单个自包含HTML文件**，零外部依赖
- 输出HTML必须保存到与输入文件相同目录，使用相同基础名 + `_presentation.html`
- 保留源文件全部文字内容，不摘要或省略
- 中文字符必须正确渲染
- 受阻时换通道（如依赖缺失时生成脚本并指导用户安装），不降级交付物

### Step 3: 证据 (Evidence)
从源文件提取全部内容作为证据：
- **.pptx文件**：使用 `python-pptx` 提取所有幻灯片内容——文字、形状、表格、图片（base64编码）、布局信息和颜色
- **.pdf文件**：使用 `pymupdf` (fitz) 提取每页的文字、图片（base64）和页面结构
- 每个幻灯片的内容均来自源文件提取，不编造

### Step 4: 执行 (Execute)
生成并执行Python脚本，提取内容并生成完整HTML。先给影响与结论，再给行动和必要证据。

#### HTML输出规范

**架构**：
- 单个 `.html` 文件，完全自包含（CSS + JS内联，图片为base64 data URI）
- 无CDN链接、无外部字体、无外部JS——100%离线可用
- 使用系统字体：`-apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif`

**演示模式**：
HTML应作为基于幻灯片的演示文稿，具备：
- **幻灯片导航**：方向键(← →)、点击或滑动切换
- **幻灯片指示器**：底部圆点显示当前位置
- **进度条**：顶部细条显示演示进度
- **全屏切换**：按钮进入/退出全屏（F键快捷键）
- **幻灯片计数**："3 / 10"指示器
- **平滑过渡**：幻灯片间CSS过渡（滑动或淡入）
- **响应式**：支持桌面、平板和移动端

**视觉设计**：
```
Design tokens:
- Background: linear-gradient(135deg, #0f0f1a, #1a1a2e)  (dark mode default)
- Slide background: #ffffff with subtle shadow
- Primary accent: extract from source file, fallback to #1a73e8
- Text: #202124 (dark), #5f6368 (secondary)
- Slide aspect ratio: 16:9
- Max slide width: 1200px, centered
- Slide padding: 60px
- Border radius: 12px on slide container
- Box shadow: 0 20px 60px rgba(0,0,0,0.3)
```

**HTML模板结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Project Name} — Business Plan</title>
    <style>
        /* Reset + Base styles */
        /* Slide container styles */
        /* Navigation styles */
        /* Responsive breakpoints */
        /* Print styles */
        /* Animation keyframes */
    </style>
</head>
<body>
    <!-- Progress bar -->
    <div class="progress-bar"><div class="progress-fill"></div></div>

    <!-- Slides container -->
    <div class="slides-container">
        <div class="slide active" data-index="0">
            <!-- Slide content reconstructed from source -->
        </div>
        <!-- ... more slides ... -->
    </div>

    <!-- Navigation -->
    <div class="nav-dots">
        <span class="dot active"></span>
        <!-- ... -->
    </div>
    <div class="slide-counter">1 / 10</div>
    <button class="fullscreen-btn" title="Fullscreen (F)">⛶</button>
    <button class="nav-arrow prev" title="Previous (←)">‹</button>
    <button class="nav-arrow next" title="Next (→)">›</button>

    <script>
        // Slide navigation logic
        // Keyboard shortcuts (←, →, F, Escape)
        // Touch/swipe support
        // Fullscreen API
        // Progress bar update
    </script>
</body>
</html>
```

**内容映射规则**：

| Source Element | HTML Rendering |
|---|---|
| Slide title | `<h1>` or `<h2>` with accent underline |
| Subtitle | `<p class="subtitle">` |
| Body text | `<p>` with proper spacing |
| Bullet points | `<ul>` with styled list items |
| Tables | `<table>` with striped rows and hover effects |
| Images | `<img>` with base64 src, responsive sizing |
| Charts/shapes | Describe as styled `<div>` blocks or reconstruct with CSS |
| Stat numbers | Large `<span class="stat">` with label below |
| Cards | `<div class="card">` with shadow and border |
| Timeline | Horizontal flex layout with dots and lines |
| Comparison table | Feature matrix with ✓/✗ icons |

**幻灯片类型特定样式**：
1. **封面**：全出血深色背景、大标题、渐变叠加
2. **痛点**：网格中的彩色卡片
3. **方案**：带图标的功能卡片
4. **商业模式**：带可视化条形的收入分解
5. **产品演示**：居中图片/模型图+标注
6. **竞争分析**：样式化对比表格
7. **Traction**：指标行+时间线可视化
8. **路线图**：带箭头连接的阶段卡片
9. **团队**：一排头像卡片
10. **融资**：关键统计+资金用途条形图

#### Python脚本要求

脚本必须：
1. 接受输入文件路径作为变量或参数
2. 检测文件类型(.pptx或.pdf)并使用适当的提取方式
3. 提取全部文字内容并保留层级（标题vs正文）
4. 提取图片并转换为base64 data URI
5. 对于.pptx：提取形状位置、颜色、字体大小以指导布局
6. 对于.pdf：提取带位置数据的文本块、嵌入图片
7. 生成带内联CSS和JS的完整HTML
8. 正确处理中英文文本
9. 保存输出文件并打印路径
10. 依赖：`python-pptx`、`pymupdf` (fitz)、`base64`、`os`

#### 脚本模板

```python
#!/usr/bin/env python3
"""Deck to HTML Converter by Unique Club"""

import os
import sys
import base64

def extract_from_pptx(filepath):
    """Extract slide content from a .pptx file."""
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    # ... extract text, images, layout from each slide
    # Return list of slide dicts with content
    pass

def extract_from_pdf(filepath):
    """Extract page content from a .pdf file."""
    import fitz  # pymupdf
    # ... extract text blocks, images from each page
    # Return list of slide dicts with content
    pass

def detect_slide_type(slide_data, index, total):
    """Heuristically detect slide type for enhanced styling."""
    # Cover (first slide), Fundraising (last slide), etc.
    pass

def generate_html(slides, title, accent_color="#1a73e8"):
    """Generate complete self-contained HTML presentation."""
    # Build CSS, HTML slides, JS navigation
    pass

def main():
    input_file = INPUT_FILE  # Set by the skill
    ext = os.path.splitext(input_file)[1].lower()

    if ext == ".pptx":
        slides = extract_from_pptx(input_file)
    elif ext == ".pdf":
        slides = extract_from_pdf(input_file)
    else:
        print(f"Unsupported format: {ext}")
        sys.exit(1)

    title = os.path.splitext(os.path.basename(input_file))[0]
    html = generate_html(slides, title)

    output_file = os.path.splitext(input_file)[0] + "_presentation.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML presentation generated: {output_file}")

if __name__ == "__main__":
    main()
```

### Step 5: 验证 (Verify)
用不同于生成路径的方式回读输出：
- 在浏览器中打开HTML，确认所有幻灯片正确渲染
- 测试键盘导航(← →)、全屏(F)、滑动操作
- 确认所有文字内容与源文件一致，无遗漏
- 验证中文字符正确渲染
- 检查响应式布局在移动端正常
- 确认文件大小合理（<10MB，除非源文件有很多大图片）
- 测试打印功能（包含@media print样式）

### Step 6: 交付 (Deliver)
返回结果，清理临时文件：
1. 告知用户输出文件路径
2. 说明可直接在浏览器中打开
3. 提及键盘快捷键：← →导航，F全屏
4. 提供文件路径便于复制分享
5. 如用户要求，可生成二维码供移动端访问

## Output

### 输出约束
- 单个HTML文件，完全自包含，零外部依赖
- 文件大小应合理（<10MB，除非源文件有很多大图片）
- 必须在Chrome、Safari、Firefox、Edge中正常工作
- 必须可打印（包含@media print样式）
- 保留源文件全部文字内容——不摘要或省略
- 中文字符必须正确渲染

### 输出文件命名
输出HTML保存到与输入文件相同目录，使用相同基础名 + `_presentation.html`。

## Guardrails

**Anti-patterns**
- NEVER 输出非自包含HTML——禁止外部CDN链接
- Do NOT 省略幻灯片或摘要内容——保留源文件全部文字
- Do NOT 在源文件含大图片(>2MB每张)时不警告用户HTML可能很大
- NEVER 将HTML保存到与输入文件不同的目录或使用不同基础名
- Do NOT 在依赖缺失时放弃——生成脚本并指导用户安装所需依赖

**Constraints**
- 输出必须为单个 `.html` 文件
- 支持 `.pptx` 和 `.pdf` 两种输入格式
- 依赖 `python-pptx` 和 `pymupdf`，缺失时指导安装
- 图片以base64 data URI内联
- 使用系统字体，不依赖外部字体
- 16:9幻灯片宽高比，最大宽度1200px居中

## Related Skills

- **pitch-deck-creator** — 从零创建专业pitch deck，然后转换为HTML完成从创建到分享的完整工作流
- **business-plan-ppt** — 创建18页中国风格商业计划书PPT，再用本技能转为网页分享
- **fundraising-bp-planner** — 在创建和转换deck前先梳理融资BP大纲

## About UniqueClub

This skill is part of the UniqueClub founder toolkit.
🌐 https://uniqueclub.ai
📂 https://github.com/wulaosiji/founder-skills
