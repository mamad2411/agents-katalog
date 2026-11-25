---
name: excalidraw
description: "Hand-drawn Excalidraw JSON diagrams (arch, flow, seq)."
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Excalidraw, Diagrams, Flowcharts, Architecture, Visualization, JSON]
    related_skills: []

---

# Excalidraw 图表生成技能

通过编写标准的 Excalidraw 元素 JSON 并将其保存为 `.excalidraw` 文件来创建图表。这些文件可直接拖放到 [excalidraw.com](https://excalidraw.com) 进行查看和编辑。无需账户、无需 API 密钥，也无需任何渲染库——仅需 JSON 即可。

## 适用场景

用于生成架构图、流程图、时序图、概念图等各类图表对应的 `.excalidraw` 文件。这些文件既可在 excalidraw.com 上直接打开，也可通过上传方式获取可分享的链接。

## 工作流程

1. **加载该技能**（您已经完成此步骤）
2. **编写元素 JSON**——即一组 Excalidraw 元素对象
3. 使用 `write_file` 函数保存文件，从而生成 `.excalidraw` 文件
4. 如需获取可分享的链接，可通过终端运行 `scripts/upload.py` 选择上传文件

### 图表保存方法

将元素数组封装在标准的 `.excalidraw` 格式中，再使用 `write_file` 函数进行保存：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "hermes-agent",
  "elements": [ ...your elements array here... ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

可保存至任意路径，例如 `~/diagrams/my_diagram.excalidraw`。

### 上传以生成可分享链接

通过终端运行上传脚本（该脚本位于该技能的 `scripts/` 目录中）：

```bash
python skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw
```

该功能会将内容上传至 excalidraw.com（无需注册账号），并生成一个可分享的链接。使用时需要安装 `cryptography` pip 包（可通过 `pip install cryptography` 安装）。

---

## 元素格式参考

### 所有元素均需包含的字段
`type`、`id`（唯一字符串）、`x`、`y`、`width`、`height`

### 可省略的默认值（系统会自动应用）
- `strokeColor`：`"#1e1e1e"`
- `backgroundColor`：`"transparent"`
- `fillStyle`：`"solid"`
- `strokeWidth`：`2`
- `roughness`：`1`（手绘风格）
- `opacity`：`100`

画布背景为白色。

### 元素类型

**矩形**：
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }
```
- 使用 `roundness: { "type": 3 }` 可设置圆角效果。
- 使用 `backgroundColor: "#a5d8ff"` 和 `fillStyle: "solid"` 可实现填充效果。

**椭圆**：
```json
{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Diamond**：
```json
{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**带标签的形状（容器绑定）**——用于创建与特定形状关联的文本元素：

> **警告：** 请勿在形状上使用 `"label": { "text": "..." }` 这种格式。这不是 Excalidraw 的有效属性，系统会直接忽略该设置，从而导致形状显示为空白。您必须采用下述的容器绑定方式。

该形状需要一个名为 `boundElements` 的列表来指定文本内容，而文本元素则需包含一个指向对应形状的 `containerId` 属性：
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }] },
{ "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,
  "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Hello", "autoResize": true }
```
- 支持在矩形、椭圆和菱形上使用  
- 当设置 `containerId` 后，Excalidraw 会自动将文本居中  
- 文本的 `x`/`y`/`width`/`height` 值为近似值——Excalidraw 会在加载时重新计算这些数值  
- `originalText` 的内容必须与 `text` 完全一致  
- 必须始终指定 `fontFamily: 1`（即 Virgil/手写体风格字体）  

**带标签的箭头**——采用相同的容器绑定方式：
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow",
  "boundElements": [{ "id": "t_a1", "type": "text" }] },
{ "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,
  "text": "connects", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "a1", "originalText": "connects", "autoResize": true }
```

**独立文本**（仅标题与注释——不含容器）：
```json
{ "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20,
  "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Hello", "autoResize": true }
```
- `x` 表示左侧边缘坐标。若希望文本在 `cx` 位置居中，则公式为：`x = cx - (text.length * fontSize * 0.5) / 2`
- 请勿依赖 `textAlign` 或 `width` 属性来定位文本

**箭头**：
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow" }
```
- `points`：以元素坐标 `x`、`y` 为基准的 `[dx, dy]` 偏移量  
- `endArrowhead`：`null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`  
- `strokeStyle`：`"solid"`（默认值）| `"dashed"` | `"dotted"`  

### 箭头绑定（将箭头连接到形状上）

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,
  "points": [[0,0],[150,0]], "endArrowhead": "arrow",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
```

`fixedPoint`坐标：`top=[0.5,0]`、`bottom=[0.5,1]`、`left=[0,0.5]`、`right=[1,0.5]`

### 绘制顺序（层序）
- 数组顺序即层序（第一个元素在最底层，最后一个元素在最上层）
- 绘制顺序应为：背景区域 → 图形元素 → 其对应的文本 → 箭头标识 → 下一个图形元素
- 错误做法：先绘制所有矩形，再绘制所有文本，最后绘制所有箭头
- 正确做法：bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
- 文本元素应始终紧接在其所在图形元素之后放置

### 尺寸规范

**字体大小：**
- 正文、标签及描述文字的最小字体大小为 **16** 
- 标题和章节标题的最小字体大小为 **20**
- 仅用于少量次要注释的文字，最小字体大小为 **14**
- 绝不可使用小于14的字体大小

**元素尺寸：**
- 带标签的矩形或椭圆的最小尺寸为120×60
- 各元素之间至少需保留20-30像素的间距
- 建议使用较少但较大的元素，而非大量微小的元素

### 颜色方案

完整的颜色表请参阅 `references/colors.md`。以下为快速参考表：

| 用途 | 填充颜色 | 十六进制值 |
|-----|-----------|-----------|
| 主要内容/输入区域 | 浅蓝色 | `#a5d8ff` |
| 成功状态/输出结果 | 浅绿色 | `#b2f2bb` |
| 警告信息/外部资源 | 浅橙色 | `#ffd8a8` |
| 处理中/特殊状态 | 浅紫色 | `#d0bfff` |
| 错误状态/严重问题 | 浅红色 | `#ffc9c9` |
| 备注/决策信息 | 浅黄色 | `#fff3bf` |
| 存储数据/数据元素 | 浅青色 | `#c3fae8` |

### 实用建议
- 在整个图表中统一使用上述颜色方案
- **文本对比度至关重要**——切勿在白色背景上使用浅灰色文字。白色背景上的文本最小颜色应为 `#757575`
- 文本中不要使用表情符号，因为它们无法在Excalidraw的字体中正确显示
- 关于深色模式下的图表设置，请参阅 `references/dark-mode.md`
- 更多示例可查看 `references/examples.md`


