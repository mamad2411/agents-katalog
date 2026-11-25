---
name: excel-date-to-text
description: |
  Scan all date columns in Excel and convert datetime values to user-specified text format (yyyymmdd, yyyy-mm-dd, yyyy/mm/dd, yyyy年mm月dd日, or any custom combination). Supports three output positions: insert new column on left, insert new column on right, or replace original column. New column headers can be customized, defaulting to "{original name}(text)".
  扫描 Excel 中所有日期列，将 datetime 转为用户指定的文本格式（yyyymmdd、yyyy-mm-dd、yyyy/mm/dd、yyyy年mm月dd日 等任意组合）。支持三种输出位置：左侧插入新列、右侧插入新列、替换原列。新列表头可自定义，未指定时默认"{原列名}(文本)"。
  Trigger keywords: "date to text" "yyyymmdd" "date format" "left of date column" "right of date column" "replace date column" "format date"
  触发词包括"日期转文本""yyyymmdd""日期格式""日期列左边/右边""替换日期列""格式化日期"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Must complete Requirement Parsing→Scout→Plan before execution, and Verify after.
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须完成 需求解析→勘察→规划，执行后必须验证。

# Excel Date Column to Custom Text / Excel 日期列转自定义文本

## 第零步：需求解析（先于勘察）

**核心原则：从用户原话中提取意图，只问没说的。用户已经明确的内容不要再问。**

### 解析三要素

从用户的请求中提取以下三项，缺失时才追问：

| 要素 | 常见表述 | 默认值 |
|------|---------|--------|
| **日期格式** | `yyyymmdd`、`yyyy-mm-dd`、`yyyy/mm/dd`、`yyyy年mm月dd日`、`yyyymd` 等 | `yyyymmdd` |
| **新列位置** | "左边插入""左侧加一列""右边""右侧" → left/right；"替换""覆盖原列""直接改" → replace | `left`（左侧插入） |
| **新列表头** | "叫xxx""命名为xxx""表头写xxx" → 使用指定名称；未提及 → 默认 `"{原列名}(文本)"` | `"{原列名}(文本)"` |

### 解析示例

| 用户说 | 提取结果 | 需要追问？ |
|--------|---------|:--:|
| "把日期列转成 yyyymmdd 放在左边" | format=yyyymmdd, pos=left, header=默认 | 否 |
| "日期改成 yyyy/mm/dd ，直接替换原数据" | format=yyyy/mm/dd, pos=replace, header=N/A | 否 |
| "在日期列右边加一列，叫'格式化日期'" | format=yyyymmdd(默认), pos=right, header='格式化日期' | 否 |
| "把日期处理一下" | 全缺 | **是**：追问格式、位置 |
| "日期列左边插入 yyyy-mm-dd 格式，命名为日期文本" | format=yyyy-mm-dd, pos=left, header='日期文本' | 否 |

### 追问模板（仅在信息不足时使用）

```
勘察完成，发现 N 个日期列：
  - 列X: "公开（公告）日"
  - 列Y: "申请日"
  ...

请确认以下三项（直接回复即可，已有默认值）：
1. 日期格式：默认 yyyymmdd（也可选 yyyy-mm-dd、yyyy/mm/dd、yyyy年mm月dd日 等）
2. 新列位置：默认左侧插入（也可选 右侧插入 / 替换原列）
3. 新列表头：默认 "{原列名}(文本)"（也可自定义）
```

## 日期格式说明

用户可通过自然语言描述想要的日期格式，常见映射：

| 用户说 | strftime 格式 | 示例输出 |
|--------|-------------|---------|
| yyyymmdd / 年月日紧凑 | `%Y%m%d` | `20260424` |
| yyyy-mm-dd / 带横线 | `%Y-%m-%d` | `2026-04-24` |
| yyyy/mm/dd / 斜线分隔 | `%Y/%m/%d` | `2026/04/24` |
| yyyy年mm月dd日 / 中文 | `%Y年%m月%d日` | `2026年04月24日` |
| yymmdd / 短年 | `%y%m%d` | `260424` |
| mmdd / 仅月日 | `%m%d` | `0424` |
| yyyymdd / 无补零月日 | 自定义函数 | `2026424` |
| yyyy/m/d / 斜线无补零 | 自定义函数 | `2026/4/24` |

**解析规则**：
- `yyyy` → 四位年份，`yy` → 两位年份
- `mm` → 补零两位月份，`m` → 不补零月份
- `dd` → 补零两位日期，`d` → 不补零日期
- 其他字符（`-`、`/`、`年`、`月`、`日`等）→ 原样保留

## 日期格式转换函数

```python
def build_format_fn(user_format):
    """根据用户描述的格式，返回一个 datetime → 文本 的转换函数。

    支持的模式（大小写不敏感）：
      yyyy → 四位年, yy → 两位年
      mm → 补零月, m → 不补零月
      dd → 补零日, d → 不补零日
      其他字符原样保留
    """
    import re

    fmt_lower = user_format.lower().strip()

    # 保护分隔符：将非模式字符标记出来
    # 替换顺序：先长后短，避免 yyyy 被误拆为 yy+yy
    replacements = [
        ('yyyy', '\x00'),   # 四位年占位
        ('yy', '\x01'),     # 两位年占位
        ('mm', '\x02'),     # 补零月占位
        ('dd', '\x03'),     # 补零日占位
        ('m', '\x04'),      # 不补零月占位
        ('d', '\x05'),      # 不补零日占位
    ]

    for pattern, placeholder in replacements:
        fmt_lower = fmt_lower.replace(pattern, placeholder)

    # 剩余字符是分隔符
    separators = fmt_lower

    # 重建格式序列
    format_seq = []
    i = 0
    tmp = fmt_lower
    while tmp:
        ch = tmp[0]
        if ch in '\x00\x01\x02\x03\x04\x05':
            format_seq.append(ch)
            tmp = tmp[1:]
        else:
            # 收集连续的分隔符
            sep = ''
            while tmp and tmp[0] not in '\x00\x01\x02\x03\x04\x05':
                sep += tmp[0]
                tmp = tmp[1:]
            format_seq.append(sep)

    def convert(dt):
        """将 datetime 转为目标格式文本"""
        parts = []
        for token in format_seq:
            if token == '\x00':   # yyyy
                parts.append(f'{dt.year:04d}')
            elif token == '\x01':  # yy
                parts.append(f'{dt.year % 100:02d}')
            elif token == '\x02':  # mm
                parts.append(f'{dt.month:02d}')
            elif token == '\x03':  # dd
                parts.append(f'{dt.day:02d}')
            elif token == '\x04':  # m (不补零)
                parts.append(str(dt.month))
            elif token == '\x05':  # d (不补零)
                parts.append(str(dt.day))
            else:                  # 分隔符
                parts.append(token)
        return ''.join(parts)

    return convert
```

## 完整执行脚本

以下脚本集成了勘察→规划→执行→验证四步。**使用前将 FORMAT 变量替换为用户指定的格式**。

### 第一步：勘察

```python
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from openpyxl import load_workbook
from datetime import datetime

FILE = '目标文件.xlsx'

# 1. 文件体量
size_mb = os.path.getsize(FILE) / 1024 / 1024
print(f'文件大小: {size_mb:.1f} MB')

# 2. 加载并扫描结构
wb = load_workbook(FILE)
ws = wb.active
print(f'工作表: {ws.title}, 行: {ws.max_row}, 列: {ws.max_column}')

# 3. 扫描所有列，在第2-10行找 datetime 值
print('\n=== 日期列扫描 ===')
date_cols = []
for col_idx in range(1, ws.max_column + 1):
    header = ws.cell(row=1, column=col_idx).value
    for row_idx in range(2, min(12, ws.max_row + 1)):
        if isinstance(ws.cell(row=row_idx, column=col_idx).value, datetime):
            date_cols.append({'col': col_idx, 'header': header})
            print(f'  ✅ 列{col_idx}: "{header}" — 日期列')
            break

# 4. 双重扫描确认非公式
print('\n=== data_only 对比（确认非公式）===')
wb2 = load_workbook(FILE, data_only=True)
ws2 = wb2.active
for dc in date_cols:
    v_raw = ws.cell(row=2, column=dc['col']).value
    v_data = ws2.cell(row=2, column=dc['col']).value
    same_type = type(v_raw) == type(v_data)
    print(f'  列{dc["col"]} "{dc["header"]}": raw={type(v_raw).__name__}, data_only={type(v_data).__name__} {"✓" if same_type else "⚠️ 公式!"}')
wb2.close()

print(f'\n共找到 {len(date_cols)} 个日期列')

# 5. 确认：展示给用户确认后再继续
for dc in date_cols:
    print(f'  列{dc["col"]}: {dc["header"]} → 将在左侧插入 "{dc["header"]}(文本)"')
print('\n请确认以上操作，确认后继续执行第二步...')
```

### 第二步：规划

勘察完成后确认：
- 日期列集合、列号、原始表头名
- 所有列为 datetime 硬值（非公式）
- 处理顺序：从右到左（列号降序）
- **left/right 模式** → 委托给 [[excel-insert]] 建列，本技能填充格式化日期
- **replace 模式** → 委托给 [[excel-replace]]，传入日期格式化函数

### 第三步：执行

**本技能只做日期专精的事：扫描 + 格式转换。列的插入/替换委托给通用技能。**

```python
# ===== 用户配置（从需求解析步骤获取）=====
FORMAT = 'yyyymmdd'        # 日期格式
POSITION = 'left'           # left / right / replace
HEADER_NAME = None          # None=自动"{原列名}(文本)"
# =========================================

fmt_fn = build_format_fn(FORMAT)
print(f'日期格式: {FORMAT} | 输出位置: {POSITION}')
print(f'共 {len(date_cols)} 个日期列: {[dc["header"] for dc in date_cols]}')

# 从右到左逐个处理
for dc in sorted(date_cols, key=lambda x: x['col'], reverse=True):
    name = dc['header']
    new_header = HEADER_NAME if HEADER_NAME else f'{name}(文本)'
    print(f'\n--- {name} ---')

    if POSITION in ('left', 'right'):
        # 委托 excel-insert：建列（空列）
        # 然后本技能：逐行填入格式化的日期文本
        pass  # 见下方具体实现

    elif POSITION == 'replace':
        # 委托 excel-replace：
        #   TARGET_COL=dc['col'], MODE='transform', transform=日期格式化
        pass  # 见下方具体实现
```

**left/right 模式实现**（本技能负责：建列 + 填格式化日期）：

```python
import time
t0 = time.time()

wb = load_workbook(FILE)
ws = wb.active
total_rows = ws.max_row

from openpyxl.styles import Font

for dc in sorted(date_cols, key=lambda x: x['col'], reverse=True):
    col = dc['col']
    name = dc['header']
    new_header = HEADER_NAME if HEADER_NAME else f'{name}(文本)'

    # --- 以下逻辑等同于 excel-insert ---
    if POSITION == 'left':
        ws.insert_cols(col)
        write_col, read_col = col, col + 1
    else:  # right
        ws.insert_cols(col + 1)
        write_col, read_col = col + 1, col

    ws.cell(row=1, column=write_col).value = new_header
    ws.cell(row=1, column=write_col).font = Font(name='Arial', size=10, bold=True)
    # --- 插入完成 ---

    # 本技能核心：逐行填入格式化的日期
    count = 0
    for row in range(2, total_rows + 1):
        dt = ws.cell(row=row, column=read_col).value
        if isinstance(dt, datetime):
            ws.cell(row=row, column=write_col).value = fmt_fn(dt)
            count += 1
        if row % 50000 == 0:
            print(f'  进度: {row}/{total_rows}')

    print(f'  {name} → {new_header}: 写入 {count} 行')

wb.save(FILE)
print(f'完成，耗时 {time.time()-t0:.1f}s')
```

**replace 模式实现**（本技能只定义转换逻辑，委托 excel-replace 执行）：

```python
# replace 模式：定义日期格式化函数，交给 excel-replace 执行
from datetime import datetime

def date_transform(val):
    """日期→文本转换函数，供 excel-replace 调用"""
    if isinstance(val, datetime):
        return fmt_fn(val)
    return val  # 非日期值保持不变

import time
t0 = time.time()
wb = load_workbook(FILE)
ws = wb.active
total_rows = ws.max_row

for dc in sorted(date_cols, key=lambda x: x['col'], reverse=True):
    col = dc['col']
    name = dc['header']
    new_header = HEADER_NAME if HEADER_NAME else f'{name}(文本)'
    print(f'\n替换 "{name}" → "{new_header}"')

    # 改表头（如果需要）
    if new_header != name:
        ws.cell(row=1, column=col).value = new_header

    # 逐行替换
    count = 0
    for row in range(2, total_rows + 1):
        val = ws.cell(row=row, column=col).value
        if isinstance(val, datetime):
            ws.cell(row=row, column=col).value = fmt_fn(val)
            count += 1
        if row % 50000 == 0:
            print(f'  进度: {row}/{total_rows}')

    print(f'  替换 {count} 行')

wb.save(FILE)
print(f'完成，耗时 {time.time()-t0:.1f}s')
```

### 第四步：验证

验证逻辑取决于位置模式，与 [[excel-insert]] 或 [[excel-replace]] 的验证对齐。

```python
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb.active
fmt_fn = build_format_fn(FORMAT)

check_rows = [2, 3, 4, ws.max_row // 2, ws.max_row - 2, ws.max_row]

for dc in date_cols:
    new_header = HEADER_NAME if HEADER_NAME else f'{dc["header"]}(文本)'

    if POSITION == 'replace':
        # 替换模式：验证列值变为文本格式
        col = dc['col']
        actual_header = ws.cell(row=1, column=col).value
        ok = True
        for row in check_rows:
            v = ws.cell(row=row, column=col).value
            if v and isinstance(v, str) and len(v) >= 6:
                print(f'  列{col}行{row}: ✓ "{v}"')
            elif v is None:
                print(f'  列{col}行{row}: ✓ (空)')
            else:
                print(f'  列{col}行{row}: ⚠️ {v}')
                ok = False
        print(f'  [{new_header}] 表头: "{actual_header}" {"✓" if actual_header == new_header else "⚠️"}')
        print(f'  {"✅" if ok else "❌"}')

    else:
        # left/right 模式：找文本列位置，对比源日期列
        text_col = None
        for col_idx in range(1, ws.max_column + 1):
            if ws.cell(row=1, column=col_idx).value == new_header:
                text_col = col_idx
                break

        if text_col is None:
            print(f'  ❌ 未找到文本列 "{new_header}"')
            continue

        # 日期列在文本列右侧(left)或左侧(right)
        date_col = text_col + 1 if POSITION == 'left' else text_col - 1

        ok = True
        for row in check_rows:
            v_text = ws.cell(row=row, column=text_col).value
            v_date = ws.cell(row=row, column=date_col).value
            if v_date and hasattr(v_date, 'strftime'):
                expected = fmt_fn(v_date)
                ok = ok and (v_text == expected)
        print(f'  [{new_header}] ← [{dc["header"]}] {"✅" if ok else "❌"}')

wb.close()
```

## 注意事项

1. **必须从右到左处理**：多个日期列时按列号降序处理，每次 insert 后源数据自动移到 col+1 位置
2. **空值处理**：datetime 为空（如"授权公告日"仅已授权专利有值）时，文本列保持空白，这是正确行为
3. **文件大小**：大文件（>100MB）加载和保存各需几分钟，中断前确认 timeout 足够
4. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
5. **⚠️ 禁止用 XML 数字范围猜测日期**：Excel 的 `<v>` 元素可能是日期序列号（如 46154=2026-05-15），也可能是普通数字（金额、编号等）。**不要**用 `20000 < serial < 100000` 这种范围判断——金额和编号会落在同一范围，导致数据被错误转为日期文本。日期转换**必须**通过 `isinstance(val, datetime)`（openpyxl）或 `pd.api.types.is_datetime64_any_dtype()`（pandas）来判断列类型。
6. **如需加速大规模日期转换**：先通过 pandas 采样确认列类型是日期，然后在 XML 层**只在已确认的日期列上**做数字→文本转换
