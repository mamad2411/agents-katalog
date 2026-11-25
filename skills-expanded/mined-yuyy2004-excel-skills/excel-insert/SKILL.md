---
name: excel-insert
description: |
  Safely insert rows or columns in Excel files. Supports inserting columns to the left/right of specified columns, or rows above/below specified rows. Custom header naming and fill content supported.
  在 Excel 文件中安全插入行或列。支持在指定列的左侧/右侧插入列，或在指定行的上方/下方插入行。可自定义表头命名和填充内容。
  Trigger keywords: "insert column" "add column" "insert row" "add row" "new column"
  触发词包括"插入列""加一列""新增列""左边加列""右边加列""插入行""加一行""上面加行""下面加行""在第X列/行前/后插入"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Must complete Requirement Parsing→Scout→Plan before execution, and Verify after.
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须完成 需求解析→勘察→规划，执行后必须验证。

# Excel Safe Insert (Row & Column) / Excel 安全插入（行列通用）

## 第零步：需求解析

### 自动识别插入类型 / Auto-detect Insert Type

从用户原话中判断要插入**列**还是**行**：

| 用户说 | 判定 |
|--------|:--:|
| "插入列""加一列""新增列""左边""右边""E列后面" | → 列模式 |
| "插入行""加一行""新增行""上面""下面""第5行后面" | → 行模式 |

### 列模式解析

| 要素 | 常见表述 | 默认值 |
|------|---------|--------|
| **目标位置** | "第5列左边""E列右侧""申请日后面" | 必须明确 |
| **插入方向** | "左边""左侧""前面" → left；"右边""右侧""后面" → right | `left` |
| **表头命名** | "叫xxx" → 指定 | `"新列"` 或留空 |
| **填充内容** | "填xxx" → 值/公式 | 空 |

### 行模式解析

| 要素 | 常见表述 | 默认值 |
|------|---------|--------|
| **目标位置** | "第5行上面""第3行下面" | 必须明确 |
| **插入方向** | "上面""上方""前面" → above；"下面""下方""后面" → below | `above` |
| **填充内容** | "填xxx" → 值/公式 | 空（留白行） |

### 解析示例

| 用户说 | 提取 |
|--------|------|
| "在E列左边插入一列，叫'格式化日期'" | 列模式, E列, left, 表头='格式化日期' |
| "第5行下面加三行空行" | 行模式, 第5行, below, 3行, 空 |
| "申请日后面加一列" | 列模式, 申请日(勘察定位), right |

## 第一步：勘察

```python
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from openpyxl import load_workbook

FILE = '目标文件.xlsx'
size_mb = os.path.getsize(FILE) / 1024 / 1024
print(f'文件大小: {size_mb:.1f} MB')

wb = load_workbook(FILE)
ws = wb.active
print(f'工作表: {ws.title}, 行: {ws.max_row}, 列: {ws.max_column}')

# 展示表头（列模式需要）
print('\n=== 表头 ===')
for col_idx in range(1, ws.max_column + 1):
    h = ws.cell(row=1, column=col_idx).value
    if h:
        col_letter = chr(64 + col_idx) if col_idx <= 26 else f'col{col_idx}'
        print(f'  列{col_idx} [{col_letter}]: {h}')

# 如果用户用名称定位 → 匹配列号或行号
target_idx = None  # 最终的列号或行号

# 列模式：定位列号
if MODE == 'column':
    if isinstance(target_spec, str):  # 用户说的是列名
        for col_idx in range(1, ws.max_column + 1):
            if ws.cell(row=1, column=col_idx).value == target_spec:
                target_idx = col_idx
                print(f'\n定位: "{target_spec}" → 列{target_idx}')
                break
    else:
        target_idx = int(target_spec)  # 用户直接给列号

# 行模式：定位行号
elif MODE == 'row':
    target_idx = int(target_spec) if isinstance(target_spec, int) else int(target_spec)

# 双重扫描（检查附近是否有公式）
print('\n=== 公式检查 ===')
wb2 = load_workbook(FILE, data_only=True)
ws2 = wb2.active
if MODE == 'column':
    check_range = range(max(1, target_idx - 2), min(ws.max_column + 1, target_idx + 3))
else:
    check_range = range(1, ws.max_column + 1)  # 行模式检查整行

for col_idx in check_range:
    for row_idx in range(max(1, target_idx - 2), min(ws.max_row + 1, target_idx + 3)) if MODE == 'row' else range(2, min(6, ws.max_row + 1)):
        v_raw = ws.cell(row=row_idx, column=col_idx).value
        if v_raw and isinstance(v_raw, str) and v_raw.startswith('='):
            print(f'  ⚠️ 列{col_idx}行{row_idx}: 公式 = {v_raw[:50]}')
wb2.close()

print(f'\n准备执行: {MODE}模式, 位置={target_idx}, 方向={DIRECTION}')
```

## 第二步：规划

### 列模式
- 插入点：`DIRECTION == 'left'` → `insert_cols(target_col)`；`'right'` → `insert_cols(target_col + 1)`
- 多列插入：从右到左

### 行模式
- 插入点：`DIRECTION == 'above'` → `insert_rows(target_row)`；`'below'` → `insert_rows(target_row + 1)`
- 多行插入：从下到上（`sorted(target_rows, reverse=True)`）

## 第三步：执行

```python
import time
t0 = time.time()

# ===== 用户配置 =====
MODE = 'column'       # 'column' 或 'row'
TARGET_IDX = None     # 目标列号或行号
DIRECTION = 'left'    # column: left/right; row: above/below
NEW_HEADER = None     # 仅列模式有效，None=留空
FILL_VALUE = None     # None=留空
AMOUNT = 1            # 插入数量（默认1）
# ====================

wb = load_workbook(FILE)
ws = wb.active
total_rows = ws.max_row
total_cols = ws.max_column

from openpyxl.styles import Font

if MODE == 'column':
    # 列插入逻辑
    insert_at = TARGET_IDX if DIRECTION == 'left' else TARGET_IDX + 1

    for i in range(AMOUNT):
        ws.insert_cols(insert_at)
        new_col = insert_at

        # 写表头
        if NEW_HEADER:
            header_text = f'{NEW_HEADER}{i+1}' if AMOUNT > 1 else NEW_HEADER
            ws.cell(row=1, column=new_col).value = header_text
            ws.cell(row=1, column=new_col).font = Font(name='Arial', size=10, bold=True)

        # 填充内容
        if FILL_VALUE is not None:
            for row in range(2, total_rows + 1):
                ws.cell(row=row, column=new_col).value = FILL_VALUE
                if row % 50000 == 0:
                    print(f'  进度: {row}/{total_rows}')

        print(f'已插入列{new_col} (原列{TARGET_IDX}的{DIRECTION})')

elif MODE == 'row':
    # 行插入逻辑
    insert_at = TARGET_IDX if DIRECTION == 'above' else TARGET_IDX + 1

    for i in range(AMOUNT):
        ws.insert_rows(insert_at)
        new_row = insert_at

        # 填充内容
        if FILL_VALUE is not None:
            for col in range(1, total_cols + 1):
                ws.cell(row=new_row, column=col).value = FILL_VALUE

        print(f'已插入行{new_row} (原行{TARGET_IDX}的{DIRECTION})')

print(f'\n保存中...')
wb.save(FILE)
print(f'完成，耗时 {time.time()-t0:.1f}s')
```

## 第四步：验证

```python
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb.active

if MODE == 'column':
    new_col = TARGET_IDX if DIRECTION == 'left' else TARGET_IDX + 1
    # 验证表头
    if NEW_HEADER:
        h = ws.cell(row=1, column=new_col).value
        print(f'新列表头: "{h}" {"✓" if h == NEW_HEADER else "⚠️"}')
    # 验证总列数
    print(f'总列数: {ws.max_column} (原{ws.max_column - AMOUNT} + {AMOUNT})')
    # 抽查
    for row in [2, ws.max_row // 2, ws.max_row]:
        v = ws.cell(row=row, column=new_col).value
        print(f'  行{row}: {repr(v)[:30] if v else "(空)"}')

elif MODE == 'row':
    new_row = TARGET_IDX if DIRECTION == 'above' else TARGET_IDX + 1
    print(f'总行数: {ws.max_row} (原{ws.max_row - AMOUNT} + {AMOUNT})')
    # 抽查新行的几个列
    for col in [1, 2, min(3, ws.max_column)]:
        v = ws.cell(row=new_row, column=col).value
        print(f'  行{new_row}列{col}: {repr(v)[:30] if v else "(空)"}')

wb.close()
```

## 注意事项

1. **列插入多列**：从右到左处理
2. **行插入多行**：从下到上处理
3. **公式引用**：openpyxl 的 insert 会自动更新直接引用，但 INDIRECT/OFFSET 不会
4. **合并单元格**：插入位置与合并区域相交时，合并会自动扩展
5. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
