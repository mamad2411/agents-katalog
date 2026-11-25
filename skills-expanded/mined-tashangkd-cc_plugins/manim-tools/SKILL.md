---
name: manim-tools
description: Reusable Manim tool functions for quick animation creation. Use when user needs ready-to-use functions for geometric shapes, function plotting, animations, or math formulas. Import: from tools.tools import *. Provides: create_circle(), create_square(), plot_sine(), plot_derivative(), fade_in_transform(), create_formula(), and more.
---

# Manim Tools Library

可复用的 Manim 工具函数库，简化动画代码编写。

## 导入方式

```python
# 导入所有工具
from tools.tools import *

# 或单独导入
from tools.tools import create_circle, plot_sine
```

## 快速开始

### 绘制正弦函数
```python
from tools.tools import *

class SineScene(Scene):
    def construct(self):
        sine = plot_sine(x_range=(-PI, PI), color=BLUE)
        self.play(Create(sine))
```

### 创建几何图形
```python
from tools.tools import *

class GeometryScene(Scene):
    def construct(self):
        circle = create_circle(radius=1, color=BLUE)
        square = create_square(side_length=2, color=RED)
        VGroup(circle, square).arrange(RIGHT)
        self.play(Create(circle), Create(square))
```

### 使用预定义动画
```python
from tools.tools import *

class AnimationScene(Scene):
    def construct(self):
        obj = create_circle()
        self.play(fade_in_transform(obj))
        self.wait()
```

## 工具函数分类

### 几何图形 (Geometric Shapes)

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_circle()` | 创建圆 | `create_circle(radius=1, color=BLUE)` |
| `create_square()` | 创建正方形 | `create_square(side_length=2, color=RED)` |
| `create_triangle()` | 创建三角形 | `create_triangle(side_length=2, color=GREEN)` |
| `create_polygon()` | 创建多边形 | `create_polygon(n_sides=6, color=YELLOW)` |
| `create_arrow()` | 创建箭头 | `create_arrow(start=LEFT, end=RIGHT)` |

### 函数绘图 (Function Plotting)

| 函数 | 描述 | 示例 |
|------|------|------|
| `plot_function()` | 绘制任意函数 | `plot_function(lambda x: x**2)` |
| `plot_sine()` | 绘制正弦函数 | `plot_sine(x_range=(-PI, PI))` |
| `plot_cosine()` | 绘制余弦函数 | `plot_cosine(x_range=(-PI, PI))` |
| `plot_derivative()` | 绘制导数 | `plot_derivative(lambda x: x**2)` |
| `plot_integral()` | 绘制积分面积 | `plot_integral(lambda x: x**2, x_range=(0, 2))` |

### 动画效果 (Animations)

| 函数 | 描述 | 示例 |
|------|------|------|
| `fade_in_transform()` | 淡入动画 | `fade_in_transform(mobject, run_time=1)` |
| `grow_from_center()` | 从中心生长 | `grow_from_center(mobject)` |
| `morph_transform()` | 变形动画 | `morph_transform(mobj1, mobj2)` |
| `rotate_and_scale()` | 旋转缩放 | `rotate_and_scale(mobj, angle=PI, scale=1.5)` |

### 文本公式 (Text & Formulas)

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_formula()` | 创建数学公式 | `create_formula(r"E=mc^2")` |
| `create_title()` | 创建标题 | `create_title("My Animation")` |
| `create_bullet_points()` | 创建列表 | `create_bullet_points(["A", "B", "C"])` |

## 参数说明

### 通用参数
- `color`: 颜色 (BLUE, RED, GREEN, YELLOW, WHITE, etc.)
- `stroke_width`: 边框宽度，默认 4
- `fill_opacity`: 填充透明度，默认 0
- `run_time`: 动画时长（秒），默认 1

### 坐标范围
- `x_range`: 元组 (start, end)，如 (-3, 3)
- `y_range`: 元组 (start, end)，如 (-2, 2)

## 完整示例

```python
from manim import *
from tools.tools import *

class CompleteScene(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(x_range=[-4, 4], y_range=[-2, 2])

        # 绘制函数
        sine = plot_sine(x_range=(-PI, PI), color=BLUE, axes=axes)
        cosine = plot_cosine(x_range=(-PI, PI), color=RED, axes=axes)

        # 创建公式
        formula = create_formula(r"y = \sin(x)")

        # 播放动画
        self.play(Create(axes))
        self.play(Create(sine), Create(cosine))
        self.play(fade_in_transform(formula))
        self.wait()
```

## 更多信息

- 完整 API 文档: `references/api.md`
- 代码示例见 `scripts/tools.py` 源码
