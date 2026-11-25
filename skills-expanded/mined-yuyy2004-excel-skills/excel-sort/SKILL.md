---
name: excel-sort
description: |
  Sort Excel data by specified column(s). Supports single or multi-column sort, ascending/descending, numeric/date/text sorting.
  对 Excel 数据按指定列排序，支持单列或多列排序、升序/降序、数值/日期/文本排序。
  Trigger keywords: "sort" "ascending" "descending" "sort by column" "from small to large" "newest first"
  触发词包括"排序""升序""降序""按xx列排列""从小到大""从新到旧"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Must scout and confirm sort column and range before execution, and verify correct order after.
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须勘察确认排序列和范围，执行后验证顺序正确。

# Excel Sort / Excel 排序

## 第零步：需求解析

| 要素 | 常见表述 | 默认值 |
|------|---------|--------|
| **排序列** | "按公开日排序""E列排序" | 必须明确 |
| **方向** | "从小到大""升序""asc" → asc；"从大到小""降序""desc" → desc | `asc` |
| **多列排序** | "先按A列再按B列" | 按优先级排列 |
| **数据范围** | 默认包含表头行（第1行），自动识别数据区 | 有表头 |

### 解析示例

| 用户说 | 提取 |
|--------|------|
| "按公开日升序排列" | 列=公开日, asc |
| "按金额从大到小排序" | 列=金额, desc |
| "先按类别排，再按日期排" | 列=[类别,日期], 默认asc |

## 第一步：勘察

```python
from openpyxl import load_workbook

FILE = '目标文件.xlsx'
wb = load_workbook(FILE)
ws = wb.active
print(f'{ws.max_row}行 x {ws.max_column}列')

# 定位排序列
print('\n=== 表头 ===')
for col_idx in range(1, ws.max_column + 1):
    h = ws.cell(row=1, column=col_idx).value
    if h:
        print(f'  列{col_idx}: {h}')

# 确认数据类型
sort_col = None  # 排序列号
print(f'\n排序列数据样本:')
for row in [2, 3, 4, ws.max_row // 2, ws.max_row]:
    v = ws.cell(row=row, column=sort_col).value
    print(f'  行{row}: {type(v).__name__} = {repr(v)[:40]}')

wb.close()
```

## 第二步：执行

**策略：大文件统一走「读格式→pandas处理→刷回格式」三步。**

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from copy import copy

FILE = '目标文件.xlsx'
SORT_COLS = [('列名或列号', 'asc')]  # asc/desc
HEADER_ROW = 1

# ====== 第一步：读取格式 ======
print('① 读取格式...')
wb = load_workbook(FILE)
ws = wb.active

header_formats, data_formats, col_widths = {}, {}, {}
for col in range(1, ws.max_column + 1):
    header_formats[col] = {
        'font': copy(ws.cell(row=HEADER_ROW, column=col).font),
        'alignment': copy(ws.cell(row=HEADER_ROW, column=col).alignment),
        'fill': copy(ws.cell(row=HEADER_ROW, column=col).fill),
    }
    data_formats[col] = {
        'font': copy(ws.cell(row=HEADER_ROW + 1, column=col).font),
        'alignment': copy(ws.cell(row=HEADER_ROW + 1, column=col).alignment),
        'fill': copy(ws.cell(row=HEADER_ROW + 1, column=col).fill),
    }
    col_letter = chr(64 + col) if col <= 26 else ''
    if col_letter and col_letter in ws.column_dimensions:
        col_widths[col] = ws.column_dimensions[col_letter].width

freeze = ws.freeze_panes
col_names = [ws.cell(row=HEADER_ROW, column=c).value for c in range(1, ws.max_column + 1)]
wb.close()

# ====== 第二步：pandas 排序 ======
print('② 排序...')
df = pd.read_excel(FILE)

# 列名归一化
sort_by = []
ascending = []
for spec, direction in SORT_COLS:
    name = col_names[spec - 1] if isinstance(spec, int) else spec
    sort_by.append(name)
    ascending.append(direction == 'asc')

df = df.sort_values(by=sort_by, ascending=ascending)
print(f'已排序: {list(zip(sort_by, ["asc" if a else "desc" for a in ascending]))}')

# ====== 第三步：写回 + 轻量格式 ======
print('③ 写回并恢复关键格式...')
df.to_excel(FILE, index=False)

wb = load_workbook(FILE)
ws = wb.active

# 核心格式（始终恢复，秒级）
for col in range(1, ws.max_column + 1):
    cl = chr(64 + col) if col <= 26 else ''
    if col in header_formats:
        hf = header_formats[col]
        c = ws.cell(row=HEADER_ROW, column=col)
        c.font, c.alignment, c.fill = hf['font'], hf['alignment'], hf['fill']
    if cl and col in col_widths and col_widths[col]:
        ws.column_dimensions[cl].width = col_widths[col]

# 数据格式：仅小文件(<1万行)逐格恢复
if ws.max_row <= 10000 and data_formats:
    for row in range(HEADER_ROW + 1, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            if col in data_formats:
                df2 = data_formats[col]
                c = ws.cell(row=row, column=col)
                c.font, c.alignment, c.fill = df2['font'], df2['alignment'], df2['fill']

if freeze: ws.freeze_panes = freeze
wb.save(FILE)
print('完成')
```

## 第三步：验证

```python
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb.active

for col_idx, direction in sort_specs:
    print(f'\n验证列{col_idx} ({direction}):')
    prev = None
    ok = True
    for row in range(HEADER_ROW + 1, min(HEADER_ROW + 20, ws.max_row + 1)):
        v = ws.cell(row=row, column=col_idx).value
        if prev is not None and v is not None:
            if direction == 'asc' and v < prev:
                print(f'  ❌ 行{row}: {v} < {prev}')
                ok = False
            elif direction == 'desc' and v > prev:
                print(f'  ❌ 行{row}: {v} > {prev}')
                ok = False
        if v is not None:
            prev = v
        print(f'  行{row}: {v}')
    print(f'  {"✅" if ok else "❌"}')

wb.close()
```

## 注意事项

1. **None 值**始终排到最后（无论升序降序）
2. **表头**不参与排序，固定在原位
3. **公式列排序**会导致引用错乱——勘察时检查排序列是否为公式，如是则先转为值再排
4. **格式保留 vs 速度**：
   - < 1万行：默认保留全部格式（几秒）
   - 1万~5万行：保留格式（~1分钟）
   - \> 5万行：**询问用户**——「格式保留需要约 N 分钟，是否保留原格式？」
5. **列内格式差异**：格式以数据首行为模板统一应用。如列内格式不一致，统一后会丢失差异
6. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
