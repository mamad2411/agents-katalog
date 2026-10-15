---
name: graphical-abstract
description: |
  学术论文摘要结构图(Graphical Abstract/TOC图)创建助手。支持多种工具：Python (matplotlib/PIL/drawsvg)、HTML/CSS/SVG、TikZ/LaTeX、Figma MCP、Banana Pro MCP、Plotly+Kaleido。集成2025-2026最新设计趋势（扁平化、Glassmorphism、等轴测、动画化）和无障碍设计指南。当用户需要：(1) 绘制论文摘要图/TOC图、(2) 创建研究流程示意图、(3) 设计期刊投稿用的图形摘要、(4) 制作学术海报的核心图示时触发。关键词：graphical abstract、摘要图、TOC图、流程图、示意图、机制图、架构图。
license: Complete terms in LICENSE.txt
---

# 摘要结构图创建助手

创建高质量的学术论文图形摘要(Graphical Abstract)和目录图(TOC)。

## 工具选择指南

| 场景 | 推荐工具 | 优势 |
|-----|---------|------|
| 包含数据图表 | Python matplotlib | 数据与示意图无缝结合 |
| 矢量绘图 | **drawsvg** | 纯Python矢量，精确控制 |
| 复杂流程/架构 | HTML/SVG | 灵活布局，易于迭代 |
| LaTeX论文配套 | TikZ | 风格统一，矢量输出 |
| 交互式/动画 | **Plotly + Kaleido** | 导出高质量静态图或HTML |
| 精美设计稿 | **Figma MCP** | 专业设计，协作方便 |
| 快速原型 | **Banana Pro MCP** | AI辅助生成，速度快 |

## 期刊尺寸规范（2025-2026最新）

```python
# 常见期刊Graphical Abstract尺寸（更新版）
JOURNAL_SIZES = {
    # 单位: pixels (300 DPI) 或 mm
    'cell': (1800, 1200),       # Cell系列: 1800x1200 px, 300 DPI
    'nature': (180, 180),        # Nature: 180x180 mm (正方形)
    'science': (900, 600),       # Science: 宽高比3:2
    'elsevier': (531, 300),      # Elsevier: 531x300 px (5x3 cm @300DPI)
    'acs': (3.25, 1.75),         # ACS: 3.25x1.75 inches
    'jacs': (3.25, 1.75),        # JACS: 同ACS规范
    'wiley': (500, 250),         # Wiley: 宽高比2:1
    'rsc': (560, 280),           # RSC: 8x4 cm @300DPI
    'angew': (180, 90),          # Angewandte Chemie: 180x90 mm
    'advanced_materials': (180, 90),  # Advanced Materials: 180x90 mm
    'pnas': (1500, 600),         # PNAS: 约1500x600 px
    'lancet': (1800, 900),       # The Lancet: 1800x900 px
    'plos_one': (2400, 2400),    # PLOS ONE: 最大2400x2400 px, 正方形
}

# 通用尺寸 (inches)
SIZES_INCH = {
    'landscape': (8, 4),        # 横向 2:1
    'square': (6, 6),           # 正方形
    'wide': (10, 4),            # 超宽 5:2
}
```

## 设计原则

1. **视觉流向**: 左→右 或 上→下，符合阅读习惯
2. **信息层次**: 3-5个关键步骤，不超过7个元素
3. **色彩统一**: 使用2-3种主色，保持一致性
4. **留白充足**: 元素间距 ≥ 元素尺寸的20%
5. **字体清晰**: 最小字号12pt，Sans-serif字体

## 2025-2026 设计趋势

### 扁平化设计（Flat Design）
```python
# 扁平风格：无阴影、纯色块、清晰边界
FLAT_COLORS = {
    'primary': '#2196F3',    # Material Blue
    'secondary': '#4CAF50',  # Material Green
    'accent': '#FF5722',     # Material Deep Orange
    'background': '#FAFAFA', # 近白背景
    'text': '#212121',       # 深灰文字
}

flat_box_style = {
    'boxstyle': 'square,pad=0.1',
    'facecolor': FLAT_COLORS['primary'],
    'edgecolor': 'none',     # 无边框
    'linewidth': 0,
}
```

### 渐变玻璃态效果（Glassmorphism）
```python
# Glassmorphism: 磨砂玻璃效果（适合HTML/SVG方案）
GLASSMORPHISM_CSS = """
.glass-box {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
}
.glass-background {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
"""
```

### 等轴测视图（Isometric Style）
```python
# 等轴测投影参数
import numpy as np

def isometric_transform(x, y, z, scale=1.0):
    """将3D坐标转换为等轴测2D坐标"""
    iso_x = (x - z) * np.cos(np.radians(30)) * scale
    iso_y = (x + z) * np.sin(np.radians(30)) * scale - y * scale
    return iso_x, iso_y

def darken_color(hex_color, factor=0.8):
    """将十六进制颜色加深（用于等轴测图的侧面/底面）
    
    Args:
        hex_color: 十六进制颜色字符串，如 '#4A90D9'
        factor:    加深系数（0-1，越小越暗）
    """
    r, g, b = bytes.fromhex(hex_color[1:])
    r2, g2, b2 = int(r * factor), int(g * factor), int(b * factor)
    return '#{:02x}{:02x}{:02x}'.format(r2, g2, b2)

def draw_iso_box(ax, x, y, z, width, height, depth, color='#4A90D9'):
    """绘制等轴测方块"""
    # 顶面
    top_pts = np.array([
        isometric_transform(x, y+height, z),
        isometric_transform(x+width, y+height, z),
        isometric_transform(x+width, y+height, z+depth),
        isometric_transform(x, y+height, z+depth),
    ])
    # 正面、侧面（颜色深浅区分）
    from matplotlib.patches import Polygon
    top_color = color
    front_color = darken_color(color, 0.8)
    ax.add_patch(Polygon(top_pts, closed=True, facecolor=top_color, edgecolor='white'))
```

### 动画化 Graphical Abstract（HTML方案）
```html
<!-- 支持CSS动画的摘要图（部分期刊接受HTML submission） -->
<style>
@keyframes flow-right {
    0% { opacity: 0; transform: translateX(-20px); }
    100% { opacity: 1; transform: translateX(0); }
}
.step { animation: flow-right 0.8s ease forwards; }
.step:nth-child(1) { animation-delay: 0s; }
.step:nth-child(2) { animation-delay: 0.3s; }
.step:nth-child(3) { animation-delay: 0.6s; }
</style>
```

## 工具一：drawsvg（Python矢量绘图）

```python
# 安装: pip install drawsvg
import drawsvg as draw

def create_svg_abstract(width=800, height=400):
    """使用drawsvg创建矢量摘要图"""
    d = draw.Drawing(width, height, origin='center')

    # 背景
    d.append(draw.Rectangle(-width/2, -height/2, width, height,
                              fill='white'))

    # 渐变定义
    gradient = draw.LinearGradient(0, 0, 1, 0)
    gradient.add_stop(0, '#4A90D9')
    gradient.add_stop(1, '#7B68EE')
    d.append(gradient)

    # 圆角矩形（步骤框）
    def add_step_box(d, x, y, w, h, text, fill=None):
        d.append(draw.Rectangle(x - w/2, y - h/2, w, h,
                                 fill=fill or gradient,
                                 rx=10, ry=10))
        d.append(draw.Text(text, 14, x, y,
                            text_anchor='middle', dominant_baseline='middle',
                            fill='white', font_weight='bold'))

    # 箭头
    def add_arrow(d, x1, y1, x2, y2):
        d.append(draw.Line(x1, y1, x2, y2,
                            stroke='#666', stroke_width=2,
                            marker_end=draw.Marker([-2, -2, 2, 2], '0 0',
                                                   orient='auto')))

    add_step_box(d, -250, 0, 140, 60, 'Input\nData', '#E74C3C')
    add_arrow(d, -175, 0, -100, 0)
    add_step_box(d, 0, 0, 140, 60, 'Processing\nModel', '#3498DB')
    add_arrow(d, 75, 0, 150, 0)
    add_step_box(d, 250, 0, 140, 60, 'Results\nOutput', '#2ECC71')

    return d

# 保存SVG
abstract = create_svg_abstract()
abstract.save_svg('graphical_abstract.svg')
abstract.save_png('graphical_abstract.png')  # 需要 cairo
```

## 工具二：Python方案

### 基础模板

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 字体嵌入（投稿必需）
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def create_graphical_abstract(figsize=(8, 4), dpi=300):
    """创建摘要图画布"""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def add_box(ax, x, y, width, height, text, color='#4A90D9', text_color='white'):
    """添加带文字的方框"""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.05,rounding_size=0.2",
                         facecolor=color, edgecolor='none')
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
            ha='center', va='center', fontsize=10,
            color=text_color, fontweight='bold')

def add_arrow(ax, start, end, color='#333333'):
    """添加箭头"""
    arrow = FancyArrowPatch(start, end,
                            arrowstyle='-|>',
                            mutation_scale=15,
                            color=color, linewidth=2)
    ax.add_patch(arrow)

# 使用示例
fig, ax = create_graphical_abstract()
add_box(ax, 0.5, 2, 2, 1, 'Input\nData', '#E74C3C')
add_arrow(ax, (2.7, 2.5), (3.3, 2.5))
add_box(ax, 3.5, 2, 2, 1, 'Model', '#3498DB')
add_arrow(ax, (5.7, 2.5), (6.3, 2.5))
add_box(ax, 6.5, 2, 2, 1, 'Output', '#2ECC71')
plt.savefig('graphical_abstract.png', bbox_inches='tight', pad_inches=0.1)
```

### 复杂布局模板

```python
def create_pipeline_abstract():
    """创建流水线式摘要图"""
    fig = plt.figure(figsize=(10, 5), dpi=300)

    # 使用GridSpec灵活布局
    gs = fig.add_gridspec(2, 4, hspace=0.3, wspace=0.3)

    # 顶部：主流程
    ax_main = fig.add_subplot(gs[0, :])
    ax_main.axis('off')

    # 底部：细节面板
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax3 = fig.add_subplot(gs[1, 2])
    ax4 = fig.add_subplot(gs[1, 3])

    return fig, (ax_main, ax1, ax2, ax3, ax4)
```

## 工具三：Plotly + Kaleido 方案

```python
# 安装: pip install plotly kaleido
import plotly.graph_objects as go

def create_plotly_abstract(title="Research Overview"):
    """使用Plotly创建可交互摘要图，并导出为高质量静态图"""
    fig = go.Figure()

    # 添加矩形框
    for i, (label, color, x) in enumerate([
        ('Input\nData', '#E74C3C', 0.1),
        ('Processing', '#3498DB', 0.4),
        ('Results', '#2ECC71', 0.7),
    ]):
        fig.add_shape(type="rect",
                      x0=x, y0=0.3, x1=x+0.2, y1=0.7,
                      fillcolor=color, line_color="white",
                      opacity=0.9)
        fig.add_annotation(x=x+0.1, y=0.5, text=label,
                           showarrow=False, font=dict(color='white', size=14))

    # 添加箭头
    for x in [0.32, 0.62]:
        fig.add_annotation(x=x+0.04, y=0.5, ax=x, ay=0.5,
                           xref='paper', yref='paper',
                           axref='paper', ayref='paper',
                           arrowhead=2, arrowsize=1.5,
                           arrowcolor='#666')

    fig.update_layout(
        width=900, height=450,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        title=dict(text=title, x=0.5)
    )

    # 导出为高质量PNG（需要kaleido）
    fig.write_image('graphical_abstract.png', scale=2)
    # 导出为PDF（矢量）
    fig.write_image('graphical_abstract.pdf')
    # 导出为HTML（交互式）
    fig.write_html('graphical_abstract.html')

    return fig
```

## 工具四：HTML/SVG方案

适合复杂交互式设计，可导出为PNG/PDF。

```html
<!DOCTYPE html>
<html>
<head>
<style>
.ga-container {
  width: 1800px;
  height: 1200px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 40px;
  font-family: 'Arial', sans-serif;
}
.ga-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}
.ga-box {
  width: 280px;
  height: 180px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.ga-arrow {
  font-size: 48px;
  color: #666;
}
.step1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.step2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.step3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.ga-label {
  font-size: 18px;
  color: #333;
  font-weight: 500;
}
</style>
</head>
<body>
<div class="ga-container">
  <div class="ga-step">
    <div class="ga-box step1">Input<br/>Data</div>
    <div class="ga-label">Step 1</div>
  </div>
  <div class="ga-arrow">→</div>
  <div class="ga-step">
    <div class="ga-box step2">Processing<br/>Model</div>
    <div class="ga-label">Step 2</div>
  </div>
  <div class="ga-arrow">→</div>
  <div class="ga-step">
    <div class="ga-box step3">Results<br/>Output</div>
    <div class="ga-label">Step 3</div>
  </div>
</div>
</body>
</html>
```

使用Playwright截图导出：
```python
from playwright.sync_api import sync_playwright

def export_html_to_image(html_path, output_path, width=1800, height=1200):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(f'file://{html_path}')
        page.screenshot(path=output_path, type='png')
        browser.close()
```

## 工具五：TikZ/LaTeX方案

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows.meta,positioning,shadows}

\begin{document}
\begin{tikzpicture}[
    node distance=2.5cm,
    box/.style={
        rectangle, rounded corners=8pt,
        minimum width=3cm, minimum height=1.5cm,
        text centered, font=\sffamily\bfseries,
        drop shadow, text=white
    },
    arrow/.style={-{Stealth[length=8pt]}, thick, color=gray}
]

% 定义颜色
\definecolor{step1}{HTML}{E74C3C}
\definecolor{step2}{HTML}{3498DB}
\definecolor{step3}{HTML}{2ECC71}

% 节点
\node[box, fill=step1] (input) {Input\\Data};
\node[box, fill=step2, right=of input] (model) {Model};
\node[box, fill=step3, right=of model] (output) {Output};

% 箭头
\draw[arrow] (input) -- (model);
\draw[arrow] (model) -- (output);

\end{tikzpicture}
\end{document}
```

## 工具六：Figma MCP集成

当安装了Figma MCP服务器时，可直接调用Figma API创建设计。

### 使用流程

1. 确认MCP连接：检查Figma MCP是否可用
2. 创建设计文件：使用MCP工具创建新文件
3. 添加元素：通过API添加形状、文本、箭头
4. 导出图片：导出为PNG/PDF格式

### 常用MCP调用模式

```
# 创建新文件
figma_create_file(name="Graphical Abstract", width=1800, height=1200)

# 添加矩形
figma_create_rectangle(x=100, y=400, width=300, height=200,
                       fill_color="#4A90D9", corner_radius=12)

# 添加文本
figma_create_text(x=250, y=500, text="Input Data",
                  font_size=24, font_weight="bold", color="#FFFFFF")

# 添加箭头
figma_create_arrow(start_x=420, start_y=500, end_x=520, end_y=500)

# 导出
figma_export(format="png", scale=2)
```

## 工具七：Banana Pro MCP集成

Banana Pro提供AI辅助图像生成能力。

### 使用场景

- 生成背景插图
- 创建图标元素
- 风格化处理

### 调用模式

```
# 生成科研风格背景
banana_generate(prompt="scientific abstract background, minimalist,
                blue gradient, molecular structure silhouette",
                width=1800, height=1200, style="academic")

# 生成图标
banana_generate(prompt="flat icon of neural network, white background,
                simple geometric style", width=200, height=200)
```

## 配色方案

```python
# 学科专用配色
PALETTES = {
    'cs_ai': ['#4A90D9', '#7B68EE', '#00CED1', '#FF6B6B', '#48D1CC'],
    'biology': ['#27AE60', '#E74C3C', '#3498DB', '#F39C12', '#9B59B6'],
    'chemistry': ['#1ABC9C', '#E67E22', '#3498DB', '#E74C3C', '#9B59B6'],
    'physics': ['#2C3E50', '#3498DB', '#E74C3C', '#F39C12', '#1ABC9C'],
    'medical': ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#95A5A6'],
}

# 渐变色对
GRADIENTS = {
    'blue': ('#667eea', '#764ba2'),
    'pink': ('#f093fb', '#f5576c'),
    'cyan': ('#4facfe', '#00f2fe'),
    'orange': ('#fa709a', '#fee140'),
    'green': ('#38ef7d', '#11998e'),
}

# 色盲友好配色（无障碍设计）
COLORBLIND_SAFE = {
    'blue': '#0077BB',
    'orange': '#EE7733',
    'green': '#009988',
    'red': '#CC3311',
    'purple': '#AA3377',
    'grey': '#BBBBBB',
}
```

## 无障碍设计指南

### 色盲友好配色原则
```python
# 避免仅用颜色区分信息，同时使用形状/纹理/标签
# 避免红绿配色（红绿色盲最常见）

# 验证色彩对比度（WCAG AA标准：对比度 ≥ 4.5:1）
def check_contrast(hex1, hex2):
    """简单对比度检查"""
    def relative_luminance(hex_color):
        r, g, b = [int(hex_color[i:i+2], 16)/255 for i in (1, 3, 5)]
        rgb = [c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
               for c in [r, g, b]]
        return 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]

    L1 = relative_luminance(hex1)
    L2 = relative_luminance(hex2)
    ratio = (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)
    return ratio  # ≥ 4.5 符合WCAG AA
```

### 高对比度文本
- 深色背景上使用白色或浅色文字
- 浅色背景上使用黑色或深色文字
- 最小字号：正文 ≥ 12pt，标注 ≥ 8pt

### Alt Text 建议
```
# 提交期刊时，为图形摘要提供文字描述（Alt Text）
# 格式示例：
alt_text = """
Graphical abstract showing a three-step workflow:
(1) Input data (blue box, left): raw experimental measurements;
(2) Processing model (gray box, center): machine learning algorithm;
(3) Results output (green box, right): predicted outcomes with 95% CI.
Arrows indicate data flow from left to right.
"""
```

## 输出检查清单

- [ ] 尺寸符合目标期刊要求
- [ ] DPI ≥ 300（线图600 DPI）
- [ ] PDF/EPS已设置 `fonttype=42` 确保字体嵌入
- [ ] 文字清晰可读（缩小50%后仍可辨认）
- [ ] 色彩对比度足够（≥ 4.5:1，WCAG AA）
- [ ] 色盲友好（不依赖红绿色差传达关键信息）
- [ ] 无版权问题的图标/素材
- [ ] 文件格式正确（通常PNG/TIFF/PDF）
- [ ] 提供图形摘要的文字描述（Alt Text）
