---
name: pdf-table-screenshot
description: |
  从PDF文档的指定章节、页面范围中检测表格，并将每个表格裁剪保存为PNG图片。
  Extract and crop table screenshots from specified chapters, sections, or page ranges in a PDF document.
  Use this skill when the user asks to:
  - "截取PDF中第3章的表格" or "Extract tables from Chapter 3"
  - "把这个PDF第2章的表格截图保存下来"
  - "截图PDF中10-20页的所有表格"
  - "提取PDF表格为图片" or "Save PDF tables as images"
  - "把这个PDF中3.2节的表格截出来"
  - Any request involving PDF table extraction, table screenshot, table cropping, or table image capture
  Features:
  - Chapter/section detection via bookmarks, TOC, or text pattern matching
  - Direct page range specification as fallback
  - Automatic table detection using pdfplumber
  - High-quality table image cropping via PyMuPDF (no Poppler needed)
  - Supports Chinese and English chapter patterns
  - Configurable DPI for output image quality
  - Automatic detection of single/dual-column page layouts
  - Merging of split tables in dual-column PDFs
---

# PDF Table Screenshot

从PDF文档的指定章节或页面范围中自动检测表格，裁剪并保存为PNG图片。

## 工作流程

1. 确认参数：PDF路径、章节/范围、输出目录、DPI（默认200）
2. 安装依赖（如需要）
3. 运行脚本截图表格
4. 向用户报告结果，展示输出图片

## 快速使用

### 按章节截图（自动检测）

```bash
python scripts/pdf_table_screenshot.py "document.pdf" --section "第3章" -o ./output/
python scripts/pdf_table_screenshot.py "document.pdf" --section "Chapter 3" -o ./output/
python scripts/pdf_table_screenshot.py "document.pdf" --section "3.2" -o ./output/
```

### 按页面范围截图

```bash
python scripts/pdf_table_screenshot.py "document.pdf" --pages 10-25 -o ./output/
python scripts/pdf_table_screenshot.py "document.pdf" --pages 5,8,12 -o ./output/
```

### 查看PDF的章节结构

```bash
python scripts/pdf_table_screenshot.py "document.pdf" --list-sections
```

### 查看指定范围内的表格位置

```bash
python scripts/pdf_table_screenshot.py "document.pdf" --list-tables --pages 10-25
python scripts/pdf_table_screenshot.py "document.pdf" --list-tables --section "第3章"
```

### 指定页面布局（双列PDF）

```bash
python scripts/pdf_table_screenshot.py "document.pdf" --pages 5-10 --layout auto -o ./output/
python scripts/pdf_table_screenshot.py "document.pdf" --pages 5-10 --layout double -o ./output/
python scripts/pdf_table_screenshot.py "document.pdf" --pages 5-10 --layout single -o ./output/
```

### 指定DPI和过滤条件

```bash
python scripts/pdf_table_screenshot.py "document.pdf" --section "第2章" --dpi 300 --min-cols 3 -o ./output/
```

### 完整参数

```
positional:  pdf_path          PDF文件路径
--section    SECTION           章节/节标题关键词（支持中文和英文）
--pages      PAGE_RANGE        页面范围，如 "10-25" 或 "5,8,12"
--list-sections                列出PDF中所有可检测的章节标题
--list-tables                  列出指定范围内的所有表格位置
--layout LAYOUT                页面布局: auto(自动检测)/single(单列)/double(双列) (默认: auto)
-o, --output-dir DIR           输出目录（默认：./pdf_tables_output）
--dpi DPI                      输出图片DPI（默认：200）
--padding N                    表格裁剪边距（默认：8 points）
--min-cols N                   最少列数过滤（默认：2）
--min-rows N                   最少行数过滤（默认：2）
--verbose                      详细输出模式
```

## 依赖安装

```bash
pip install pdfplumber PyMuPDF pypdf Pillow
```

无需安装 Poppler。渲染使用 PyMuPDF，无外部系统依赖。

## 章节检测策略

脚本按以下优先级定位章节页面范围：

1. **PDF书签/大纲**：使用pypdf读取PDF outline（最准确）
2. **文本模式匹配**：对书签不可用的PDF，使用正则匹配章节标题
3. **直接页码范围**：用户直接指定 --pages

支持中英文章节标题模式，详见 `references/section_patterns.md`。

## 页面布局处理

脚本支持自动检测和手动指定页面排版格式（单列/双列）：

- **`--layout auto`**（默认）：自动分析文本字符的 x 坐标分布，判断页面是单列还是双列排版
- **`--layout single`**：强制按单列处理
- **`--layout double`**：强制按双列处理，自动合并被拆分到左右两列的表格

**双列模式下的表格合并规则**：
- 左右两个半宽表格的垂直范围重叠 > 50% 时自动合并
- 合并后的表格以页面全宽裁剪，确保内容完整
- `--list-tables` 输出中会标注 `[双列]` 和 `[已合并]`

## 输出文件命名

```
pdf_tables_output/
  table_p15_1.png    # 第15页 第1个表格
  table_p15_2.png    # 第15页 第2个表格
  table_p16_1.png    # 第16页 第1个表格
  tables_summary.json # 表格摘要信息
```

## 与用户交互指南

1. 如果用户未提供PDF路径，询问路径
2. 如果用户说了章节名，用 --section；如果说了页码，用 --pages
3. 如果不确定章节名是否正确，先用 --list-sections 查看
4. 截图完成后，用 Read 工具查看输出图片，向用户展示结果
5. 如果未找到章节，运行 --list-sections 并建议可用选项
6. 如果未检测到表格，建议降低 --min-cols / --min-rows 或扩大范围

## 错误处理

- PDF文件不存在：提示用户检查路径
- 未找到指定章节：列出可用章节供用户选择
- 指定范围内无表格：提示降低过滤阈值或扩大范围
- 依赖缺失：给出 pip install 命令
- 加密PDF：提示需要先解密
