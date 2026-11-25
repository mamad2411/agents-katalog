---
name: manim-generator
description: Generate Manim Python code from natural language descriptions. Use when user asks to create mathematical animations, visualize functions, plot graphs, or generate scene code for Manim. Handles: function plotting (sin, cos, derivative, integral), geometric shapes (circle, square, triangle), animations (transform, fade, morph), and math formulas (LaTeX).
---

# Manim Code Generator

将自然语言描述转换为完整的 Manim Scene 代码。

## Quick Start

```
用户描述 → 选择模式 → 生成代码 → 输出到文件
```

## 代码生成模式

### 模式 1: 函数可视化
**触发词**: "绘制函数", "函数图像", "plot function"

```python
from manim import *

class FunctionScene(Scene):
    def construct(self):
        # 使用 FunctionGraph 或 ParametricFunction
        func = FunctionGraph(lambda x: np.sin(x), x_range=[-PI, PI])
        self.play(Create(func))
```

### 模式 2: 几何图形
**触发词**: "画圆", "正方形", "三角形", "几何图形"

```python
from manim import *

class GeometryScene(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED)
        self.play(Create(circle), Create(square))
```

### 模式 3: 动画变换
**触发词**: "变成", "变形", "移动", "旋转", "缩放"

```python
from manim import *

class TransformScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.play(Transform(circle, square))
```

### 模式 4: 数学公式
**触发词**: "公式", "LaTeX", "数学表达式"

```python
from manim import *

class FormulaScene(Scene):
    def construct(self):
        formula = MathTex(r"\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
        self.play(Write(formula))
```

## 常用 Mobject 类型

| 类别 | Mobject | 用途 |
|------|---------|------|
| 几何 | Circle, Square, Triangle, Rectangle, RegularPolygon | 基本图形 |
| 函数 | FunctionGraph, ParametricFunction | 函数图像 |
| 文本 | Text, Tex, MathTex | 文字和公式 |
| 箭头 | Arrow, Vector, DoubleArrow | 指向标记 |
| 坐标 | NumberPlane, Axes | 坐标系 |

## 常用 Animation 类型

| 动画 | 效果 |
|------|------|
| Create | 逐笔画创建 |
| Write | 书写效果 |
| FadeIn | 淡入 |
| Transform | 变形变换 |
| Rotate | 旋转 |
| Scale | 缩放 |
| MoveToEdge | 移动到边缘 |

## 代码模板

### 基础场景模板
```python
from manim import *

class SceneName(Scene):
    def construct(self):
        # Your animation code here
        pass
```

### 函数图像模板
```python
from manim import *
import numpy as np

class FunctionPlot(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-2, 2])
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        self.play(Create(axes), Create(graph))
```

## 生成代码时的注意事项

1. **导入完整**: 始终包含 `from manim import *` 和 `import numpy as np`
2. **类名规范**: 使用 PascalCase，如 `SineWaveScene`
3. **坐标理解**: 默认 4:3 宽高比，中心为 (0, 0)
4. **颜色选择**: 使用预定义颜色 (BLUE, RED, GREEN, YELLOW, WHITE)
5. **时间控制**: 使用 `self.wait()` 添加停顿

## 参考更多模式

详见 `references/patterns.md` 获取更多场景模式和完整示例。
