---
name: wps-format-fix
description: |
  WPS格式修复医生。WPS打开Office文件格式全乱了？字体变了、表格错位、
  页码不对？自动诊断10种常见兼容问题，一键修复。附字体替换对照表。
  用于帮助用户修复格式兼容问题。当用户提到格式乱了、字体不对、兼容问题时触发。
  WPS/Office format compatibility fixer - diagnoses and repairs common issues.
license: MIT
user-invocable: true
argument-hint: '[问题描述] [文件路径(可选)]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: WPS格式修复
  description_zh: 修复WPS打开Word文件时出现的格式问题，如字体缺失、表格错位等
  tags:
    - 兼容性
    - 格式修复
    - WPS
    - Office
    - 字体
  version: 1.0.1
  license: MIT
---

# WPS 格式兼容性修复

修复 WPS ↔ Microsoft Office 之间互传文档时的各种格式错乱问题。

> **这是 WPS 用户反馈最多的痛点。** 本工具提供系统性的诊断和修复方案。

## When to Use

- 文档在WPS打开后格式错乱
- Word文件发给对方后排版变了
- 字体显示不对/缺失
- 行距、页边距、表格等格式异常
- 用户说"格式乱了""打开变了""兼容性问题"

## When NOT to Use

- 需要从头创建文档 → 使用 `wps-docx-writer`
- 需要公文排版 → 使用 `wps-gongwen`
- 需要校对文字内容 → 使用 `wps-proofread`

## 常见问题诊断表

| 症状 | 原因 | 修复方案 |
|------|------|---------|
| **字体变了/显示方块** | 对方电脑没有该字体 | 字体替换为通用字体 |
| **行距忽大忽小** | WPS和Word的行距计算方式不同 | 统一设置固定行距 |
| **表格超出页面** | 表格宽度计算差异 | 重设表格宽度为百分比 |
| **图片位移/重叠** | 图片锚定方式不同 | 改为嵌入型排列 |
| **页面布局错乱** | 分节符/分页符差异 | 重设页面参数 |
| **页码不连续** | 节设置差异 | 统一节的页码设置 |
| **目录页码错误** | 域代码未更新 | 更新所有域 |
| **SmartArt变形** | WPS渲染差异 | 转换为普通形状 |
| **公式显示异常** | MathType/公式编辑器兼容性 | 转为图片或重新编辑 |
| **批注/修订丢失** | 版本兼容性 | 检查保存格式是否为.docx |

## 工作流程

### Step 1: 诊断问题

**如果用户提供了文件，运行诊断脚本：**

```bash
pip install python-docx 2>/dev/null || pip3 install python-docx 2>/dev/null
```

```python
from docx import Document
from docx.shared import Pt, Mm
from docx.oxml.ns import qn
import os

def diagnose_compat(file_path):
    """诊断文档兼容性问题"""
    doc = Document(file_path)
    issues = []

    # 检查字体
    risky_fonts = set()
    safe_fonts = {'宋体', '黑体', '楷体', '仿宋', '微软雅黑',
                  'Arial', 'Times New Roman', 'Calibri'}

    for para in doc.paragraphs:
        for run in para.runs:
            font_name = run.font.name
            east_asia = None
            rPr = run._element.find(qn('w:rPr'))
            if rPr is not None:
                rFonts = rPr.find(qn('w:rFonts'))
                if rFonts is not None:
                    east_asia = rFonts.get(qn('w:eastAsia'))

            for f in [font_name, east_asia]:
                if f and f not in safe_fonts:
                    risky_fonts.add(f)

    if risky_fonts:
        issues.append(f"⚠️ 发现 {len(risky_fonts)} 种非通用字体：{', '.join(risky_fonts)}")

    # 检查页面设置
    for section in doc.sections:
        if section.page_width != Mm(210) or section.page_height != Mm(297):
            issues.append("⚠️ 页面尺寸非标准A4")

    # 检查表格宽度
    for i, table in enumerate(doc.tables):
        issues.append(f"📊 表格{i+1}：{len(table.rows)}行 × {len(table.columns)}列")

    # 检查图片
    img_count = 0
    for para in doc.paragraphs:
        for run in para.runs:
            if run._element.findall(qn('w:drawing')):
                img_count += 1
    if img_count:
        issues.append(f"🖼️ 包含 {img_count} 张图片（可能有位移风险）")

    return issues
```

**输出诊断报告：**

```text
📋 兼容性诊断报告
═══════════════════════════════════
文件：[文件名]
大小：[XX] KB

🔍 发现的兼容性风险：
┌─────────────────────────────────────┐
│ ⚠️ 字体风险                          │
│   方正小标宋简体 → 对方可能没装        │
│   华文中宋 → Mac有但Windows可能没有    │
│                                      │
│ ⚠️ 行距问题                          │
│   第3-5段使用了"多倍行距"             │
│   建议改为"固定值"以确保兼容          │
│                                      │
│ 📊 表格：2个（需检查宽度）            │
│ 🖼️ 图片：5张（建议改为嵌入型）        │
└─────────────────────────────────────┘

📋 修复建议：
1. 替换非通用字体
2. 统一行距设置
3. 检查表格宽度
4. 图片改为嵌入型排列
```

### Step 2: 执行修复

**根据诊断结果生成修复脚本（python-docx或JSA宏）：**

#### 字体替换修复

```python
# 字体映射表：非通用字体 → 安全替代字体
FONT_MAP = {
    # 公文字体 → 通用替代
    '方正小标宋简体': '华文中宋',
    '方正小标宋_GBK': '华文中宋',
    '仿宋_GB2312': '仿宋',
    '楷体_GB2312': '楷体',

    # Mac专有 → 通用
    'PingFang SC': '微软雅黑',
    '.PingFang SC': '微软雅黑',
    'Hiragino Sans GB': '微软雅黑',
    'STHeiti': '黑体',
    'STSong': '宋体',
    'STKaiti': '楷体',
    'STFangsong': '仿宋',

    # 其他 → 安全回退
    '华文细黑': '微软雅黑',
    '华文楷体': '楷体',
    '华文仿宋': '仿宋',
    '等线': '微软雅黑',
    '等线 Light': '微软雅黑',
}

def fix_fonts(doc, font_map=None):
    """替换文档中的非通用字体"""
    fm = font_map or FONT_MAP
    replaced = {}

    for para in doc.paragraphs:
        for run in para.runs:
            # 替换西文字体
            if run.font.name in fm:
                old = run.font.name
                run.font.name = fm[old]
                replaced[old] = fm[old]

            # 替换东亚字体
            rPr = run._element.find(qn('w:rPr'))
            if rPr is not None:
                rFonts = rPr.find(qn('w:rFonts'))
                if rFonts is not None:
                    ea = rFonts.get(qn('w:eastAsia'))
                    if ea and ea in fm:
                        rFonts.set(qn('w:eastAsia'), fm[ea])
                        replaced[ea] = fm[ea]

    return replaced
```

#### 行距统一修复

```python
def fix_line_spacing(doc, spacing_pt=None):
    """统一行距设置"""
    fixed = 0
    for para in doc.paragraphs:
        pf = para.paragraph_format
        if spacing_pt:
            pf.line_spacing = Pt(spacing_pt)
        elif pf.line_spacing_rule == 5:  # 多倍行距(MULTIPLE)
            pf.line_spacing = Pt(22)  # 改为固定值
            fixed += 1
    return fixed
```

#### 图片排列修复

```python
def fix_image_anchoring(doc):
    """将浮动图片改为嵌入型"""
    # 此操作需要操作底层XML
    # 推荐在WPS中手动操作：右键图片→环绕方式→嵌入型
    pass
```

#### JSA 宏版修复（用户在WPS中运行）

```javascript
/**
 * WPS格式兼容性修复宏
 * 在WPS中运行：开发工具 → 宏编辑器 → 粘贴运行
 */
function FixCompatibility() {
    try {
        var doc = Application.ActiveDocument

        // 1. 字体替换
        var fontMap = {
            '方正小标宋简体': '华文中宋',
            '仿宋_GB2312': '仿宋',
            '楷体_GB2312': '楷体',
            'PingFang SC': '微软雅黑'
        }

        for (var oldFont in fontMap) {
            var find = doc.Content.Find
            find.ClearFormatting()
            find.Replacement.ClearFormatting()
            find.Text = ''
            find.Font.Name = oldFont
            find.Replacement.Text = ''
            find.Replacement.Font.Name = fontMap[oldFont]
            find.Execute(undefined, false, false, false, false,
                         false, true, undefined, true, undefined, 2)
        }

        // 2. 统一行距
        for (var i = 1; i <= doc.Paragraphs.Count; i++) {
            var para = doc.Paragraphs.Item(i)
            if (para.Format.LineSpacingRule == 5) { // wdLineSpaceMultiple
                para.Format.LineSpacingRule = 4 // wdLineSpaceExactly
                para.Format.LineSpacing = 22
            }
        }

        // 3. 更新所有域（修复目录、页码等）
        doc.Fields.Update()

        Application.alert("兼容性修复完成！\n请检查文档排版是否正确。")
    } catch (e) {
        Application.alert("修复出错：" + e.message)
    }
}
```

### Step 3: 预防建议

```text
📌 避免格式兼容性问题的最佳实践：

1. 字体选择：优先使用双方都有的字体
   安全字体：宋体、黑体、楷体、仿宋、微软雅黑
   安全英文：Arial、Times New Roman、Calibri

2. 保存格式：始终保存为 .docx（不要用 .doc）

3. 行距设置：使用"固定值"而非"多倍行距"

4. 图片设置：使用"嵌入型"排列而非"浮动"

5. 表格宽度：使用百分比而非固定磅值

6. 发送前：另存为PDF + 原文件一起发送

7. 嵌入字体：文件→选项→保存→嵌入字体（增加文件体积）
```

## 示例

```bash
# 诊断文件兼容性
/wps-format-fix 检查 report.docx 的兼容性问题

# 修复字体问题
/wps-format-fix 这个文件用WPS打开字体全变了，帮我修复

# 生成修复宏
/wps-format-fix 生成一个WPS宏，统一替换文档中的非通用字体

# 预防建议
/wps-format-fix 我要发一份文档给用Office的同事，怎么避免格式问题
```

## 参考

字体兼容性完整映射表见 [reference/font-compat-map.md](reference/font-compat-map.md)。
