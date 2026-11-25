---
name: wps-ppt-polish
description: |
  PPT一键美化。PPT内容写好了但排版一言难尽？帮你诊断字体混乱、
  颜色太多、对齐不整齐等问题，一键批量统一字体配色，还能批量删动画。
  用于帮助用户提升PPT视觉质量。当用户提到PPT美化、PPT太丑、排版不整齐时触发。
  PPT beautification tool - batch fixes fonts, colors, and alignment.
license: MIT
user-invocable: true
argument-hint: '[PPT文件路径/问题描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: PPT美化
  description_zh: 检查PPT的排版问题，统一字体、配色和对齐方式
  tags:
    - PPT
    - 美化
    - 排版
    - 配色
    - WPS
  version: 1.0.1
  license: MIT
---

# PPT美化与优化工具

诊断PPT问题 → 一键批量修复 → 专业级视觉效果。

> 内容写好了，排版却一言难尽？交给我。

## When to Use

- PPT做完了但不好看
- 字体/颜色/对齐混乱需要统一
- 需要批量修改所有幻灯片格式
- 用户说"PPT太丑了""帮我美化一下"

## When NOT to Use

- 从零创建PPT → 使用 `wps-ppt-gen`
- 只需要大纲 → 使用 `wps-ppt-outline`

## PPT常见问题诊断

```text
🔴 严重问题
  · 字体不统一（宋体+黑体+楷体混用）
  · 文字溢出文本框
  · 图片变形拉伸
  · 元素互相遮挡

🟡 排版问题
  · 元素不对齐
  · 间距不一致
  · 页边距太小/太大
  · 内容过多（一页>7行文字）

🔵 美观问题
  · 配色超过4种
  · 背景花哨
  · 动画过多
  · 字号不规范
```

## 工作流程

### Step 1: 诊断PPT

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from collections import Counter
import os

def diagnose_ppt(ppt_path):
    """诊断PPT问题"""
    prs = Presentation(ppt_path)
    issues = []

    fonts_used = Counter()
    colors_used = Counter()
    total_slides = len(prs.slides)

    for slide_num, slide in enumerate(prs.slides, 1):
        text_count = 0
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.name:
                            fonts_used[run.font.name] += 1
                        if run.font.color and run.font.color.rgb:
                            colors_used[str(run.font.color.rgb)] += 1
                    text_count += len(para.text)

            # 检查图片是否变形
            if shape.shape_type == 13:  # Picture
                if hasattr(shape, 'image'):
                    w_ratio = shape.width / shape.height
                    # 原始比例检查
                    if abs(w_ratio - 1.33) > 0.5 and abs(w_ratio - 1.78) > 0.5:
                        issues.append(f"P{slide_num}: 图片可能变形")

        if text_count > 500:
            issues.append(f"P{slide_num}: 文字过多({text_count}字)")

    # 字体统一性
    if len(fonts_used) > 3:
        issues.append(f"使用了{len(fonts_used)}种字体，建议≤3种")

    # 颜色统一性
    if len(colors_used) > 6:
        issues.append(f"使用了{len(colors_used)}种颜色，建议≤5种")

    return {
        'total_slides': total_slides,
        'fonts': dict(fonts_used.most_common(10)),
        'colors': dict(colors_used.most_common(10)),
        'issues': issues,
    }
```

### Step 2: 批量修复

**Python-pptx批量修复：**

```python
def polish_ppt(ppt_path, output_path, config=None):
    """批量美化PPT"""
    default_config = {
        'title_font': '微软雅黑',
        'body_font': '微软雅黑',
        'title_size': Pt(28),
        'body_size': Pt(18),
        'primary_color': '2C3E50',
        'accent_color': '3498DB',
    }
    cfg = {**default_config, **(config or {})}
    prs = Presentation(ppt_path)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        # 统一字体
                        if shape == slide.shapes.title:
                            run.font.name = cfg['title_font']
                            run.font.size = cfg['title_size']
                            run.font.bold = True
                        else:
                            run.font.name = cfg['body_font']
                            if not run.font.size or run.font.size < Pt(14):
                                run.font.size = cfg['body_size']

    prs.save(output_path)
    return os.path.abspath(output_path)
```

**JSA宏批量修复（在WPS中直接运行）：**

```javascript
// JSA: PPT批量统一字体和字号
function PolishPresentation() {
    var pres = Application.ActivePresentation;
    var titleFont = "微软雅黑";
    var bodyFont = "微软雅黑";
    var titleSize = 28;
    var bodySize = 18;
    var fixCount = 0;

    for (var i = 1; i <= pres.Slides.Count; i++) {
        var slide = pres.Slides.Item(i);
        for (var j = 1; j <= slide.Shapes.Count; j++) {
            var shape = slide.Shapes.Item(j);
            if (shape.HasTextFrame) {
                var tf = shape.TextFrame.TextRange;
                for (var k = 1; k <= tf.Paragraphs().Count; k++) {
                    var para = tf.Paragraphs(k);
                    var font = para.Font;

                    if (j === 1) { // 假定第一个shape是标题
                        font.Name = titleFont;
                        font.NameFarEast = titleFont;
                        font.Size = titleSize;
                        font.Bold = true;
                    } else {
                        font.Name = bodyFont;
                        font.NameFarEast = bodyFont;
                        if (font.Size < 14) {
                            font.Size = bodySize;
                        }
                    }
                    fixCount++;
                }
            }
        }
    }
    Application.alert("已修复 " + fixCount + " 个文本段落\n共 "
        + pres.Slides.Count + " 页");
}

// JSA: 删除所有动画效果（精简版）
function RemoveAllAnimations() {
    var pres = Application.ActivePresentation;
    var count = 0;
    for (var i = 1; i <= pres.Slides.Count; i++) {
        var timeline = pres.Slides.Item(i).TimeLine;
        var seq = timeline.MainSequence;
        while (seq.Count > 0) {
            seq.Item(1).Delete();
            count++;
        }
    }
    Application.alert("已删除 " + count + " 个动画效果");
}
```

### Step 3: 配色方案推荐

```text
商务蓝（推荐）：
  主色 #2C3E50  文字/标题
  强调 #3498DB  重点/图表
  辅助 #ECF0F1  背景/底色
  点缀 #E74C3C  警示/重点数据

科技紫：
  主色 #2D1B69  标题
  强调 #7C3AED  重点
  辅助 #F3F0FF  背景
  点缀 #06B6D4  数据

简约灰：
  主色 #1A1A2E  标题
  强调 #16213E  内容
  辅助 #F5F5F5  背景
  点缀 #E94560  重点
```

### Step 4: 交付

1. 输出诊断报告（问题列表+严重程度）
2. 生成修复后的PPT文件
3. 或提供JSA宏代码在WPS中直接运行

## 排版黄金法则

```text
1. 字体≤3种（标题1种+正文1种+英文1种）
2. 颜色≤4种（主色+强调+辅助+点缀）
3. 每页≤7行文字，每行≤25字
4. 字号：标题28-36pt，正文18-24pt，注释≥14pt
5. 所有元素对齐（用参考线）
6. 留白≥30%（不要塞满）
7. 图片不变形（锁定比例缩放）
```

## 示例

```bash
# 诊断问题
/wps-ppt-polish 帮我看看这个PPT有什么排版问题 report.pptx

# 批量修复
/wps-ppt-polish 把所有字体统一成微软雅黑，配色用商务蓝

# 精简动画
/wps-ppt-polish 把PPT里的动画都去掉，太花哨了
```
