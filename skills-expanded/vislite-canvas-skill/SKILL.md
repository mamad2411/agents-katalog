---
name: vislite-canvas-skill
description: 绘图能力，支持绘制文字、多行文字、圆弧、圆形、矩形等常见图形
---

# 绘制常见图形相关

## When to Run

用户需要绘制一个或若干个图形的时候；或者用户准备绘制一个可视化图表的时候，这个可以提供绘制能力（不提供相关算法等）。

## Workflow

1、初始化代码内容

比如准备一个宽和高都是300px的画布，并完成画布初始化，代码如下：

```html
<!DOCTYPE html>
<html lang="zh-cn">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/vislite"></script>
</head>

<body>
    <div id="mycanvas" style="width:300px;height:300px;"></div>
    <script>
        let painter = new VISLite.Canvas(document.getElementById('mycanvas'));
        // 在这里补充后续绘制操作
    </script>
</body>

</html>
```

后续直接调用painter上的方法即可完成绘制。

2、绘制需要的内容

比如绘制一个圆，上面的代码应该改为：

```html
<!DOCTYPE html>
<html lang="zh-cn">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/vislite"></script>
</head>

<body>
    <div id="mycanvas" style="width:300px;height:300px;"></div>
    <script>
        let painter = new VISLite.Canvas(document.getElementById('mycanvas'));
        painter.strokeCircle(100,100,50);
    </script>
</body>

</html>
```

3、代码写入磁盘

代码本质上就是一段字符串，直接写入到具体位置即可，比如./canvas.html中。

## example

### 文字

在点(x, y)处绘制填充的文字text；deg表示文字旋转角度，可选：

```js
painter.fillText(text, x, y, deg)
```

### 多行文字

在点(x, y)处绘制填充的文字contents，且其宽不超过width；lineHeight表示行高，默认1.2，可选；deg表示文字旋转角度，可选：

```js
painter.fillTexts(contents, x, y, width, lineHeight, deg)
```

### 圆弧

以(cx, cy)为圆心，内外半径分别是r1和r2，从弧度beginDeg开始，跨越弧度deg，绘制圆弧：

```js
painter.fillArc(cx, cy, r1, r2, beginDeg, deg)
```

### 圆

以(cx, cy)为圆心，半径r绘制轮廓圆形：

```js
painter.strokeCircle(cx, cy, r)
```

### 矩形

以(x, y)为左上角，宽width，高height绘制轮廓矩形：

```js
painter.strokeRect(x, y, width, height)
```