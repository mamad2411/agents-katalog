---
name: excel-replace
description: |
  Safely replace content in Excel — entire columns, rows, or condition-matched cells. Supports replacing with fixed values, Excel formulas, or Python transform functions.
  安全替换 Excel 中的内容——整列、整行、或指定条件的单元格。支持替换为固定值、Excel 公式、或 Python 转换函数。
  Trigger keywords: "replace column" "overwrite column" "entire column to" "replace row" "batch replace" "conditional replace" "cell replace" "clean" "change all to"
  触发词包括"替换列""覆盖列""整列改成""替换行""批量替换""条件替换""单元格替换""清洗""全部改为"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Must complete Requirement Parsing→Scout→Plan before execution, and Verify after. **Must confirm before overwriting.**
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须完成 需求解析→勘察→规划，执行后必须验证。**替换覆盖前必须确认。**

# Excel Safe Replace (Column/Row/Cell) / Excel 安全替换（列/行/单元格）

## 第零步：需求解析

### 自动识别替换范围 / Auto-detect Replace Scope

| 用户说 | 判定 |
|--------|:--:|
| "这列全改成""E列替换为""整列" | → 整列模式 |
| "这行全改成""第5行替换为""整行" | → 整行模式 |
| "把所有空值改成""xxxx的替换为""条件替换" | → 条件单元格模式 |
| "B5改成""这个单元格" | → 单单元格模式 |

### 解析要素

| 要素 | 说明 | 默认值 |
|------|------|--------|
| **范围** | 整列/整行/条件/单格 | 从用户话中判定 |
| **目标** | 列号/列名/行号/单元格坐标 | 必须明确 |
| **新内容** | 固定值 / `=`开头的公式 / 自定义转换 | 必须明确 |
| **条件** | （仅条件模式）"等于xx的""包含xx的""为空的" | 必须明确 |

### 解析示例

| 用户说 | 提取 |
|--------|------|
| "把E列全部替换成'已确认'" | 整列, E, 值='已确认' |
| "第3行整行清空" | 整行, 3, 值=None |
| "状态列里所有'待审'改成'已审'" | 条件, 状态列, 匹配='待审'→'已审' |
| "把空单元格全填上0" | 条件(全局), 匹配=None→0 |
| "B5改成'总计'" | 单格, B5, 值='总计' |
| "金额列换成公式 =C2*D2" | 整列, 金额列, 公式='=C2*D2' |

## 第一步：勘察

```python
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from openpyxl import load_workbook
from datetime import datetime

FILE = '目标文件.xlsx'
size_mb = os.path.getsize(FILE) / 1024 / 1024
print(f'文件大小: {size_mb:.1f} MB')

wb = load_workbook(FILE)
ws = wb.active
print(f'工作表: {ws.title}, 行: {ws.max_row}, 列: {ws.max_column}')

# 定位目标
target_col = None  # 整列模式
target_row = None  # 整行模式
target_cell = None # 单格模式

# 整列模式：定位列号
if SCOPE == 'column':
    if isinstance(target_spec, str):
        for col_idx in range(1, ws.max_column + 1):
            if ws.cell(row=1, column=col_idx).value == target_spec:
                target_col = col_idx
                break
    else:
        target_col = int(target_spec)

    print(f'\n目标列: 列{target_col} "{ws.cell(row=1, column=target_col).value}"')
    # 抽样展示
    for row in range(2, min(10, ws.max_row + 1)):
        v = ws.cell(row=row, column=target_col).value
        print(f'  行{row}: {repr(v)[:50]}')

# 条件模式：统计匹配数
if SCOPE == 'condition':
    match_count = 0
    for row in range(2, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            v = ws.cell(row=row, column=col).value
            if CONDITION(v):  # 用户定义的条件
                match_count += 1
    print(f'\n条件匹配: {match_count} 个单元格（共 {ws.max_row * ws.max_column} 个）')

# 双重扫描
print('\n=== 双重扫描 ===')
wb2 = load_workbook(FILE, data_only=True)
ws2 = wb2.active
# ... 对比 target 区域
wb2.close()
```

## 第二步：规划

| 模式 | 遍历方式 | 性能 |
|------|---------|------|
| 整列 (openpyxl) | `for row in range(2, max_row+1)` | ~0.5ms/格 |
| 整列 (XML, value/formula) | sheet XML 层 + 列号限定 + inline | 快 3-5x |
| 整行 | `for col in range(1, max_col+1)` | 很快 |
| 条件 | 嵌套循环 + 条件判断 | 取决于扫描范围 |
| 单格 | 直接赋值 | 瞬时 |

> **XML 方案限制**：仅 `整列 + value/formula` 模式下可用。`transform`/`condition` 模式因需要运行 Python 逻辑判断，不走 XML。

## 第三步：执行

> ⚠️ **XML 方案必须在 sheet 层 + 列号限定**，不碰 sharedStrings。仅整列+值/公式模式下可用。

```python
import time, os, shutil
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# ===== 用户配置 =====
SCOPE = 'column'       # 'column' / 'row' / 'condition' / 'cell'
TARGET_COL = None      # 整列模式：列号（1-based）
TARGET_ROW = None      # 整行模式
TARGET_CELL = None     # 单格模式: (row, col)
REPLACE_MODE = 'value' # 'value' / 'formula' / 'condition' / 'transform'
NEW_VALUE = None       # value/formula 模式下的新值
# ====================

SIZE_MB = os.path.getsize(FILE) / 1024 / 1024
USE_XML = (SCOPE == 'column' and REPLACE_MODE in ('value', 'formula') and SIZE_MB > 10)

if USE_XML:
    # ====== XML 快速路径（整列 + value/formula，大文件）======
    print(f'\n替换中（XML sheet 层方案, {SIZE_MB:.0f}MB）...')
    import zipfile
    from lxml import etree

    t0 = time.time()
    col_letter = get_column_letter(TARGET_COL)

    TMP = FILE.replace('.xlsx', '_rep_tmp')
    if os.path.exists(TMP): shutil.rmtree(TMP)
    os.makedirs(TMP)
    with zipfile.ZipFile(FILE, 'r') as z:
        z.extractall(TMP)

    S_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    parser = etree.XMLParser(remove_blank_text=False, huge_tree=True)
    ns = {'s': S_NS}

    ws_dir = os.path.join(TMP, 'xl', 'worksheets')
    count = 0
    for sf in sorted(os.listdir(ws_dir)):
        if not sf.endswith('.xml'): continue
        sp = os.path.join(ws_dir, sf)
        tree = etree.parse(sp, parser)
        root = tree.getroot()

        for row_elem in root.findall('.//s:row', ns):
            if row_elem.get('r') == '1': continue  # 跳过表头
            for cell in row_elem.findall('s:c', ns):
                # 限定列号
                if not cell.get('r', '').startswith(col_letter):
                    continue

                # 改为 inline 字符串
                cell.set('t', 'inlineStr')
                for child in list(cell):
                    tag = child.tag.split('}')[-1]
                    if tag in ('v', 'f', 'is'): cell.remove(child)
                is_new = etree.SubElement(cell, '{'+S_NS+'}is')
                t_new = etree.SubElement(is_new, '{'+S_NS+'}t')
                t_new.text = str(NEW_VALUE) if NEW_VALUE is not None else ''
                count += 1

        sheet_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        with open(sp, 'wb') as f: f.write(sheet_xml)

    print(f'  替换 {count} 个单元格')

    # 打包
    with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
        for dirpath, _, filenames in os.walk(TMP):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                zout.write(full, os.path.relpath(full, TMP).replace('\\\\', '/'))
    shutil.rmtree(TMP)
    print(f'  耗时: {time.time()-t0:.0f}s')

else:
    # ====== openpyxl 方案（默认）======
    t0 = time.time()
    wb = load_workbook(FILE)
    ws = wb.active

    count = 0

    if SCOPE == 'column':
        # 整列替换
        print(f'替换列{TARGET_COL}...')
        for row in range(2, ws.max_row + 1):
            if REPLACE_MODE == 'value':
                ws.cell(row=row, column=TARGET_COL).value = NEW_VALUE
            elif REPLACE_MODE == 'formula':
                ws.cell(row=row, column=TARGET_COL).value = NEW_VALUE  # 以 = 开头
            elif REPLACE_MODE == 'transform':
                old = ws.cell(row=row, column=TARGET_COL).value
                ws.cell(row=row, column=TARGET_COL).value = transform(old)
            count += 1
            if row % 50000 == 0:
                print(f'  进度: {row}/{ws.max_row}')

    elif SCOPE == 'row':
        # 整行替换
        print(f'替换行{TARGET_ROW}...')
        for col in range(1, ws.max_column + 1):
            if REPLACE_MODE == 'value':
                ws.cell(row=TARGET_ROW, column=col).value = NEW_VALUE
            elif REPLACE_MODE == 'transform':
                old = ws.cell(row=TARGET_ROW, column=col).value
                ws.cell(row=TARGET_ROW, column=col).value = transform(old)
            count += 1

    elif SCOPE == 'condition':
        # 条件替换
        print(f'条件替换: {CONDITION_DESC}...')
        for row in range(1, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                val = ws.cell(row=row, column=col).value
                if condition_match(val):
                    if REPLACE_MODE == 'value':
                        ws.cell(row=row, column=col).value = NEW_VALUE
                    elif REPLACE_MODE == 'transform':
                        ws.cell(row=row, column=col).value = transform(val)
                    count += 1
            if row % 50000 == 0:
                print(f'  进度: {row}/{ws.max_row}')

    elif SCOPE == 'cell':
        # 单格替换
        row, col = TARGET_CELL
        ws.cell(row=row, column=col).value = NEW_VALUE
        count = 1
        print(f'替换 {chr(64+col)}{row} → {NEW_VALUE}')

    print(f'替换 {count} 个单元格')
    print(f'\n保存中...')
    wb.save(FILE)
    wb.close()
    print(f'完成，耗时 {time.time()-t0:.1f}s')
```

## 第四步：验证

```python
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb.active

if SCOPE == 'column':
    # 抽查整列
    print(f'=== 列{TARGET_COL}替换后抽样 ===')
    for row in [2, 3, 4, ws.max_row // 2, ws.max_row - 2, ws.max_row]:
        v = ws.cell(row=row, column=TARGET_COL).value
        print(f'  行{row}: {repr(v)[:40] if v else "(空)"}')

    # 全部校验
    if REPLACE_MODE == 'value':
        ok = all(
            ws.cell(row=row, column=TARGET_COL).value == NEW_VALUE
            for row in range(2, ws.max_row + 1)
        )
        print(f'{"✅ 全部一致" if ok else "❌ 存在不一致"}')

elif SCOPE == 'condition':
    # 验证不再有匹配旧条件的单元格
    remaining = 0
    for row in range(1, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            if old_condition(ws.cell(row=row, column=col).value):
                remaining += 1
    print(f'剩余匹配旧条件的单元格: {remaining} {"✅" if remaining == 0 else "⚠️"}')

wb.close()
```

## 注意事项

1. **大文件整列替换自动走 XML**：>10MB 的整列 value/formula 替换使用 sheet 层 XML 快速路径，快 3-5x
2. **XML 方案限定列号**：通过 `cell.get('r').startswith(col_letter)` 限定，不会误伤其他列
3. **XML 方案写 inline string**：替换后的值写为 `<is><t>` 内联字符串，不产生新的 sharedString 引用
4. **transform 和 condition 模式走 openpyxl**：需要 Python 逻辑判断（自定义函数），XML 无法替代
5. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复

## 常见场景速查 / Common Scenarios Quick Reference

### 整列填充固定值 / Entire Column Fill Fixed Value
```python
SCOPE = 'column'; TARGET_COL = 5
REPLACE_MODE = 'value'; NEW_VALUE = '已确认'
```

### 整列填充公式 / Entire Column Fill Formula
```python
SCOPE = 'column'; TARGET_COL = 7
REPLACE_MODE = 'formula'; NEW_VALUE = '=C2*D2'
```

### 条件替换（空值→0）/ Conditional Replace (Null→0)
```python
SCOPE = 'condition'
def condition_match(val):
    return val is None or (isinstance(val, str) and val.strip() == '')
REPLACE_MODE = 'value'; NEW_VALUE = 0
```

### 条件替换（特定值→新值）/ Conditional Replace (Specific→New)
```python
SCOPE = 'condition'
def condition_match(val):
    return val == '待审'
REPLACE_MODE = 'value'; NEW_VALUE = '已审'
```

### 整行清空 / Entire Row Clear
```python
SCOPE = 'row'; TARGET_ROW = 5
REPLACE_MODE = 'value'; NEW_VALUE = None
```

### 单格修改 / Single Cell Edit
```python
SCOPE = 'cell'; TARGET_CELL = (5, 2)  # B5
REPLACE_MODE = 'value'; NEW_VALUE = '总计'
```
