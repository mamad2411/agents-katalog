---
name: academic-md2docx
description: Convert Markdown papers to properly formatted DOCX. Three pipelines: (A) Python direct parse v4 — REF field codes + auto-numbering, recommended for final output; (B) Pandoc — general purpose; (C) HTML intermediate — fallback only.
tool_type: python + cli
primary_tool: python-docx + pandoc
---

# Academic MD → DOCX

Convert Markdown academic papers to properly formatted DOCX files.

## Three Pipelines Overview

| Pipeline | Method | Citations | REF Field Codes | Chinese Formatting | Reliability |
|----------|--------|-----------|-----------------|-------------------|-------------|
| **A. Python Direct (v4)** | python-docx low-level XML | ✅ Word REF field codes | ✅ Full support | ✅ Full control | ⭐⭐⭐⭐⭐ |
| **B. Pandoc Direct** | pandoc --citeproc | ✅ Pandoc citeproc | ❌ Pandoc不支持 | ⚠️ 依赖template.docx | ⭐⭐⭐⭐ |
| **C. HTML Intermediate** | MD→HTML→python-docx | ❌ 易出错 | ❌ 会断 | ⚠️ 手动设置 | ⭐⭐ |

**推荐**：Pipeline A (Python Direct v4) 用于最终论文输出。Pipeline B (Pandoc) 用于快速草稿。**禁止使用 Pipeline C 用于正式输出**——HTML→DOCX 必然出现 XML 映射错误，导致引用和超链接不可用。

---

## Pipeline A: Python Direct v4（推荐用于最终输出）

直接解析 Markdown，用 python-docx 底层 XML 操作生成 DOCX。这是经过生产验证的 v4 方案。

### 核心能力

- **REF field codes**：`{ REF ref-N \h }` 实现 Ctrl+点击跳转（非 HYPERLINK）
- **Word 自动编号**：通过自定义 `word/numbering.xml` 实现 `[1][2][3]` 格式
- **多引用紧贴**：`[5][6]` 无逗号无空格
- **完整中文排版**：宋体/TNR/黑体，14pt，1.5倍行距，0.74cm首行缩进

### 生产参考脚本

```
F:\swxxx\scripts\build_docx_ref_codes.py
```

### Markdown 源文件格式要求

```markdown
# 论文标题

## 正文

研究表明[1]，荞麦基因组[2][3]显示...

## 参考文献

1. LIN H, YAO Y. Haplotype-resolved genomes...[J]. Journal, 2025.
2. 作者A,作者B. 论文标题[D]. 大学, 2024.
```

**关键规则**：
- 引用标记：`[N]` 或 `[N][M]`（多引用紧贴）
- 参考文献：**Markdown 有序列表** `1. ` `2. `（非 `[1]` 手打文本）
- 加粗：`**文字**`
- 图片：`图1 标题` 后跟 `文件：path/to/image.png`

### v4 格式规范摘要

| 元素 | 规范 |
|------|------|
| 正文字体 | 宋体/Times New Roman，14pt |
| 行距 | 1.5倍 |
| 首行缩进 | 0.74cm |
| 一级标题 | 黑体 15pt 加粗 |
| 二级标题 | 黑体 14pt 加粗 |
| 引用上标 | 14pt superscript |
| 图片/表注 | 12pt 居中 |
| 参考文献 | 12pt，Word 自动编号 `[1]` 格式 |
| 页边距 | 上/下 1in，左/右 1.25in |

### 实现核心：REF Field Code

```python
def add_ref_field(paragraph, text, bookmark_name, superscript=False):
    """插入 { REF bookmark_name \\h } Word field code"""
    # 1. 插入 w:fldChar begin
    r1 = OxmlElement('w:r')
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    fld_begin.set(qn('w:dirty'), 'true')
    r1.append(fld_begin)
    paragraph._element.append(r1)

    # 2. 插入 instrText: " REF ref-1 \h "
    r2 = OxmlElement('w:r')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = f' REF {bookmark_name} \\h '
    r2.append(instr)
    paragraph._element.append(r2)

    # 3. 插入 fldChar separate
    ...

    # 4. 插入显示文本（上标 [N]）
    r4 = make_simple_run(text, 14, superscript=True)

    # 5. 插入 fldChar end
    ...
```

### 实现核心：自定义编号格式

通过替换 `word/numbering.xml` 实现 `[1]` 而非 `1.`：

```xml
<w:numbering xmlns:w="...">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>
      <w:lvlText w:val="[%1] "/>  <!-- 关键：编号格式 -->
      <w:ind w:left="0" w:hanging="0"/>  <!-- 紧贴 -->
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
  </w:num>
</w:numbering>
```

### 生成后处理

```python
# 注入 updateFields 标记
with zipfile.ZipFile(tmp_path, 'r') as zin:
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/settings.xml':
                if b'<w:updateFields' not in data:
                    data = data.replace(
                        b'</w:settings>',
                        b'<w:updateFields w:val="true"/></w:settings>'
                    )
            elif item.filename == 'word/numbering.xml':
                data = CUSTOM_NUMBERING_XML
            zout.writestr(item, data)
```

### 文档元数据清理

```python
doc.core_properties.author = ''
doc.core_properties.last_modified_by = ''
# 仅当用户明确指定作者时填写
```

---

## Pipeline B: Pandoc Direct（用于快速草稿）

当不需要 REF field code、不需要自定义编号时的快速输出方案。

```bash
# 基本转换
pandoc paper.md -o paper.docx

# 带引用处理
pandoc paper.md --citeproc --bibliography=refs.bib -o paper.docx

# 带格式模板
pandoc paper.md \
  --reference-doc=template.docx \
  --citeproc \
  --bibliography=refs.bib \
  --csl=gb-t-7714-2015-numeric.csl \
  --number-sections \
  -o paper.docx
```

**注意**：Pandoc 不支持 REF field code，引用为静态文本超链接。

---

## Pipeline C: HTML Intermediate（仅紧急兜底）

```bash
# Pandoc MD→HTML
pandoc paper.md -o paper.html

# Python HTML→DOCX
python scripts/html2docx.py paper.html -o paper.docx
```

**已知问题**：python-docx 无法创建 Word 书签和交叉引用，HTML 中的超链接在转换后可能断裂。**仅当 Pandoc 和 python-docx 低层 XML 都不可用时使用。**

---

## 三管线决策树

```
需要最终论文输出（REF field code + 自动编号）？
  ├─ 是 → Pipeline A (Python Direct v4)
  └─ 需要快速草稿？
       ├─ 需要引用处理 → Pipeline B (Pandoc + citeproc)
       └─ 纯文本 → Pipeline B (Pandoc 基本转换)

Pandoc 和 python-docx 都不可用？
  └─ Pipeline C (HTML 中间) — 但不保证引用可用
```

---

## 依赖

| 管线 | 依赖 | 安装 |
|------|------|------|
| A | python-docx | `pip install python-docx` |
| B | pandoc | https://pandoc.org/installing.html |
| C | pandoc + python-docx | 两者都需要 |

### 工具检查

```python
# 检查 Pipeline A
python -c "from docx import Document; print('OK')"

# 检查 Pipeline B
pandoc --version

# 检查 CSL 文件
ls gb-t-7714-2015-numeric.csl
# 下载：https://github.com/citation-style-language/styles
```
