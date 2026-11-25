---
name: excel-format
description: |
  Uniformly adjust Excel file formatting — font, size, bold, italic, color, alignment (horizontal/vertical), column width, row height. Supports per-scope application: entire sheet, specified columns/rows, headers, data area, or condition-matched cells.
  统一调整 Excel 文件的格式样式——字体、字号、加粗、斜体、颜色、对齐方式（水平/垂直）、列宽行高。支持按范围应用：整表、指定列/行、表头、数据区、或条件匹配的单元格。
  Trigger keywords: "font" "bold" "italic" "center" "align" "column width" "row height" "change style" "format" "beautify"
  触发词包括"字体""加粗""斜体""居中""对齐""列宽""行高""改样式""格式化""美化表格"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Must complete Requirement Parsing→Scout before execution, and Verify after.
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须完成 需求解析→勘察，执行后验证。

# Excel Format Adjustment / Excel 格式调整

## 第零步：需求解析

### 自动识别格式需求 / Auto-detect Format Requirements

从用户原话提取所有已明确的格式参数，只追问没说到的。

| 要素 | 常见表述 | 默认值 |
|------|---------|--------|
| **字体** | "微软雅黑""Arial""Times New Roman" | 不改变 |
| **字号** | "12号""10pt""大一点" | 不改变 |
| **加粗** | "加粗""粗体""bold" | 不改变 |
| **斜体** | "斜体""italic" | 不改变 |
| **颜色** | "红色""蓝色""#FF0000" | 不改变 |
| **水平对齐** | "居中""靠左""靠右""两端对齐" | 不改变 |
| **垂直对齐** | "上下居中""顶部对齐""底部对齐" | 不改变 |
| **列宽** | "列宽15""自适应""自动调整宽度" | 不改变 |
| **行高** | "行高20""自适应" | 不改变 |
| **应用范围** | "表头""全部""E列""第2-10行""数据区" | `all`（整表） |

### 解析示例

| 用户说 | 提取 |
|--------|------|
| "表头加粗居中，字体改成微软雅黑 12号" | 范围=表头, 加粗, 水平居中, 字体=微软雅黑, 字号=12 |
| "全部改成 Arial 10号，金额列右对齐" | 范围=全部+金额列, 字体=Arial, 字号=10, 金额列=右对齐 |
| "标题行加粗，数据区垂直居中" | 表头=加粗, 数据区=垂直居中 |
| "列宽全部自适应" | 全部列, 自适应列宽 |
| "把表格美化一下" | 全部, 用默认美化方案 |

### 默认美化方案（用户只说"美化"时启用）/ Default Beautify Preset

| 区域 | 格式 |
|------|------|
| 表头（第1行） | 加粗、水平居中、垂直居中、Arial 10pt |
| 数据区（第2行起） | 垂直居中、Arial 10pt |
| 所有列 | 自适应列宽 |

## 第一步：勘察

```python
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from openpyxl import load_workbook

FILE = '目标文件.xlsx'

wb = load_workbook(FILE)
ws = wb.active
print(f'工作表: {ws.title}, 行: {ws.max_row}, 列: {ws.max_column}')

# 展示当前样式状态
print('\n=== 当前格式 ===')
for col_idx in range(1, min(ws.max_column + 1, 8)):
    cell = ws.cell(row=1, column=col_idx)
    col_letter = chr(64 + col_idx) if col_idx <= 26 else f'col{col_idx}'
    print(f'  列{col_letter}表头: font={cell.font.name}/{cell.font.size}, '
          f'bold={cell.font.bold}, align={cell.alignment.horizontal}')

# 确认操作范围
print(f'\n格式应用范围: {SCOPE}')
print(f'格式参数: {FORMAT_SPEC}')
```

## 第二步：执行

```python
import time
t0 = time.time()
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill

# ===== 用户配置 =====
FILE = '目标文件.xlsx'
SCOPE = 'all'           # 'all' / 'header' / 'data' / 'columns' / 'rows' / 'range'

# 字体配置（None = 不改变）
FONT_NAME = 'Arial'     # None 或字体名
FONT_SIZE = 10          # None 或数字
FONT_BOLD = None        # True / False / None
FONT_ITALIC = None      # True / False / None
FONT_COLOR = None       # 'FF0000'(红) / '000000'(黑) / None

# 对齐配置（None = 不改变）
H_ALIGN = None          # 'center' / 'left' / 'right' / 'justify' / None
V_ALIGN = None          # 'center' / 'top' / 'bottom' / None

# 列宽行高（None = 不改变）
COL_WIDTH = None        # 数字 或 'auto'（自适应）
ROW_HEIGHT = None       # 数字 或 'auto'

# 范围限定
HEADER_ROW = 1          # 表头行号
DATA_START = 2          # 数据起始行
TARGET_COLS = None      # None=全部列, [1,2,5]=指定列
TARGET_ROWS = None      # None=全部行(配合SCOPE), [(2,10)]=指定行范围
# ====================

wb = load_workbook(FILE)
ws = wb.active

def build_font():
    """构建字体对象"""
    kwargs = {}
    if FONT_NAME is not None: kwargs['name'] = FONT_NAME
    if FONT_SIZE is not None: kwargs['size'] = FONT_SIZE
    if FONT_BOLD is not None: kwargs['bold'] = FONT_BOLD
    if FONT_ITALIC is not None: kwargs['italic'] = FONT_ITALIC
    if FONT_COLOR is not None: kwargs['color'] = FONT_COLOR
    return Font(**kwargs) if kwargs else None

def build_alignment():
    """构建对齐对象"""
    kwargs = {}
    if H_ALIGN is not None: kwargs['horizontal'] = H_ALIGN
    if V_ALIGN is not None: kwargs['vertical'] = V_ALIGN
    return Alignment(**kwargs) if kwargs else None

new_font = build_font()
new_align = build_alignment()

# 确定操作范围
cols_to_process = TARGET_COLS if TARGET_COLS else list(range(1, ws.max_column + 1))

if SCOPE == 'all':
    rows_to_process = range(1, ws.max_row + 1)
elif SCOPE == 'header':
    rows_to_process = [HEADER_ROW]
elif SCOPE == 'data':
    rows_to_process = range(DATA_START, ws.max_row + 1)
elif SCOPE == 'columns':
    rows_to_process = range(1, ws.max_row + 1)
elif SCOPE == 'rows':
    rows_to_process = TARGET_ROWS if TARGET_ROWS else range(1, ws.max_row + 1)

# 应用格式
count = 0
for row in rows_to_process:
    for col in cols_to_process:
        cell = ws.cell(row=row, column=col)
        if new_font:
            # 合并现有字体属性（只覆盖指定项）
            existing = cell.font
            kwargs = {'name': FONT_NAME if FONT_NAME else existing.name,
                      'size': FONT_SIZE if FONT_SIZE else existing.size,
                      'bold': FONT_BOLD if FONT_BOLD is not None else existing.bold,
                      'italic': FONT_ITALIC if FONT_ITALIC is not None else existing.italic,
                      'color': FONT_COLOR if FONT_COLOR else existing.color}
            cell.font = Font(**kwargs)
        if new_align:
            cell.alignment = new_align
        count += 1
    if row % 50000 == 0:
        print(f'  进度: {row}/{ws.max_row}')

print(f'已格式化 {count} 个单元格')

# 列宽
if COL_WIDTH == 'auto':
    # 用 pandas 快速计算每列最大宽度（比 openpyxl 逐格扫快 100 倍）
    import pandas as pd, numpy as np
    from openpyxl.utils import get_column_letter

    df = pd.read_excel(FILE)
    for col_idx in cols_to_process:
        col_name = df.columns[col_idx - 1]
        # 取前 5000 行 + 随机抽样 1000 行估算最大宽度
        sample = df[col_name].dropna().head(5000).astype(str)
        if len(sample) == 0:
            continue
        # 中文字符算 2 宽度，其余算 1
        def char_width(s):
            return sum(2 if ord(c) > 127 else 1 for c in str(s))
        max_len = sample.apply(char_width).max()
        # 表头也参与计算
        header_len = char_width(str(col_name))
        max_len = max(max_len, header_len)
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = min(max_len + 3, 50)
elif COL_WIDTH is not None:
    from openpyxl.utils import get_column_letter
    for col_idx in cols_to_process:
        ws.column_dimensions[get_column_letter(col_idx)].width = COL_WIDTH

# 行高
if ROW_HEIGHT == 'auto':
    for row in rows_to_process:
        ws.row_dimensions[row].height = None  # Excel 自动计算
elif ROW_HEIGHT is not None:
    for row in rows_to_process:
        ws.row_dimensions[row].height = ROW_HEIGHT

print(f'\n保存中...')
wb.save(FILE)
print(f'完成，耗时 {time.time()-t0:.1f}s')
```

## 第三步：验证

```python
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb.active

# 验证表头格式
cell = ws.cell(row=1, column=1)
print(f'表头字体: {cell.font.name}/{cell.font.size}pt')
print(f'表头加粗: {cell.font.bold}')
print(f'表头对齐: {cell.alignment.horizontal}/{cell.alignment.vertical}')

# 验证数据区
cell2 = ws.cell(row=2, column=1)
print(f'数据字体: {cell2.font.name}/{cell2.font.size}pt')

# 验证列宽
if ws.column_dimensions['A'].width:
    print(f'A列宽: {ws.column_dimensions["A"].width}')

wb.close()
print('✅ 验证完成')
```

## 常用预设 / Common Presets

### 专业报表风 / Professional Report
```
FONT_NAME='Arial', FONT_SIZE=10, FONT_BOLD=True(header)
H_ALIGN='center'(header+data), V_ALIGN='center'
COL_WIDTH='auto'
```

### 中文文档风 / Chinese Document
```
FONT_NAME='微软雅黑', FONT_SIZE=11
FONT_BOLD=True(header), H_ALIGN='center'(header)
V_ALIGN='center', COL_WIDTH='auto'
```

### 仅加粗居中表头 / Bold+Center Header Only
```
SCOPE='header', FONT_BOLD=True, H_ALIGN='center', V_ALIGN='center'
```

## 注意事项

1. **列宽自适应**对中文友好（中文字符计 2 宽度），上限 40 字符
2. **字体可用性**取决于 Excel 打开时的系统，Arial/微软雅黑 一般都有
3. **合并单元格**中的格式需单独处理
4. **格式叠加**：None 的参数不会被修改，保留原有格式
5. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
