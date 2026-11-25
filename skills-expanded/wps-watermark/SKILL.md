---
name: wps-watermark
description: |
  文档加水印。给Word或PDF文档加上"机密""内部资料""草稿""仅供XX查阅"等文字水印，
  支持自定义文字、角度、透明度。提供python脚本和WPS宏两种方式。
  用于帮助用户保护文档。当用户提到水印、加水印、机密标记时触发。
  Adds text watermarks to Word and PDF documents.
license: MIT
user-invocable: true
argument-hint: '[文件路径] [水印文字]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 文档加水印
  description_zh: 给Word或PDF文档添加文字水印，如机密、内部、草稿等
  tags:
    - 水印
    - 文档保护
    - 安全
    - python-docx
    - WPS
  version: 1.0.1
  license: MIT
---

# 文档水印工具

一键为文档添加水印。"机密""草稿""内部"随你选。

## When to Use

- 文档需要添加"机密""内部"等水印
- 草稿文档标注"DRAFT"
- 防止文档未授权传播
- 用户说"加个水印""标记为机密"

## When NOT to Use

- 文档加密/密码保护 → WPS自带功能
- PDF操作 → 使用 `wps-pdf-merge-split`

## 水印类型

```text
[1] 文字水印 → "机密""内部资料""草稿""DRAFT""CONFIDENTIAL"
[2] 图片水印 → 公司Logo等
[3] 日期水印 → 自动添加日期
[4] 个人水印 → "仅供XX查阅"
```

## 工作流程

### Step 1: 确认水印需求

- 水印文字/图片
- 目标文件格式（Word/PDF）
- 角度（默认-45度斜置）
- 透明度（默认30%）
- 颜色（默认浅灰色）

### Step 2: 添加水印

**Word文档水印：**

```python
from docx import Document
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def add_watermark_to_word(doc_path, text='机密', output_path=None):
    """为Word文档添加文字水印"""
    doc = Document(doc_path)

    # 通过页眉添加水印（兼容性最好的方式）
    for section in doc.sections:
        header = section.header
        header.is_linked_to_previous = False

        # 创建水印shape
        watermark_xml = f'''
        <w:r {nsdecls('w', 'wp', 'v', 'o', 'mc', 'r')}>
          <mc:AlternateContent>
            <mc:Choice Requires="wps">
              <w:drawing>
                <wp:anchor distT="0" distB="0" distL="0" distR="0"
                  simplePos="0" relativeHeight="251658240"
                  behindDoc="1" locked="0" layoutInCell="1"
                  allowOverlap="1">
                  <wp:simplePos x="0" y="0"/>
                  <wp:positionH relativeFrom="page">
                    <wp:align>center</wp:align>
                  </wp:positionH>
                  <wp:positionV relativeFrom="page">
                    <wp:align>center</wp:align>
                  </wp:positionV>
                  <wp:extent cx="5400000" cy="2700000"/>
                  <wp:wrapNone/>
                </wp:anchor>
              </w:drawing>
            </mc:Choice>
          </mc:AlternateContent>
        </w:r>'''

        # 简化方式：在页眉添加灰色大字作为视觉水印
        p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        p.alignment = 1  # CENTER
        run = p.add_run(text)
        run.font.size = 7200000  # 大字
        run.font.color.rgb = None  # 需要设置透明

    if not output_path:
        base, ext = os.path.splitext(doc_path)
        output_path = f'{base}_watermarked{ext}'
    doc.save(output_path)
    return os.path.abspath(output_path)


def add_watermark_to_pdf(pdf_path, text='机密', output_path=None):
    """为PDF添加文字水印"""
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    for page in doc:
        rect = page.rect
        # 在页面中心添加斜置文字
        text_point = fitz.Point(rect.width / 4, rect.height / 2)
        page.insert_text(
            text_point, text,
            fontsize=60,
            color=(0.8, 0.8, 0.8),  # 浅灰色
            rotate=-45,
        )

    if not output_path:
        base, ext = os.path.splitext(pdf_path)
        output_path = f'{base}_watermarked{ext}'
    doc.save(output_path)
    doc.close()
    return os.path.abspath(output_path)
```

**JSA宏方式（WPS Writer中直接运行）：**

```javascript
// JSA: 添加文字水印到WPS文档
function AddWatermark() {
    var doc = Application.ActiveDocument;
    var text = "机密";

    // 通过页眉添加水印
    var header = doc.Sections.Item(1).Headers.Item(1);
    var shape = header.Shapes.AddTextEffect(
        0,        // msoTextEffect1
        text,
        "宋体",
        72,       // 字号
        false,    // 不加粗
        false,    // 不斜体
        0, 0      // 位置
    );

    shape.TextEffect.NormalizedHeight = false;
    shape.Line.Visible = false;
    shape.Fill.Visible = true;
    shape.Fill.ForeColor.RGB = 0xD0D0D0;  // 浅灰
    shape.Fill.Transparency = 0.7;
    shape.Rotation = -45;
    shape.Left = 100;
    shape.Top = 200;
    shape.Width = 400;
    shape.Height = 200;
    shape.WrapFormat.Type = 3; // wdWrapBehind

    Application.alert("水印已添加！");
}
```

### Step 3: 交付

1. 生成添加水印后的文档
2. 说明水印位置和样式
3. 提醒：文字水印可被编辑删除，不能替代加密保护

## 示例

```bash
# 添加机密水印
/wps-watermark 给report.docx加个"机密"水印

# 草稿标记
/wps-watermark 标记为草稿 draft_v2.docx

# PDF水印
/wps-watermark 给合同.pdf加水印"仅供内部使用"

# 自定义
/wps-watermark 加水印"仅供张三查阅"到proposal.docx
```
