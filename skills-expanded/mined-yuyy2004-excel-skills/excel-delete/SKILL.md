---
name: excel-delete
description: |
  Safely delete rows or columns in Excel files. Auto-checks formula dependencies before deletion to prevent #REF! errors. Row deletion uses XML direct ops (10x faster), column deletion uses openpyxl. Supports by index, by name, and batch deletion.
  在 Excel 文件中安全删除行或列。删除前自动检查公式依赖，防止产生 #REF! 错误。行删除使用 XML 直接操作（快 10 倍），列删除使用 openpyxl。支持按序号、按名称、批量删除。
  Trigger keywords: "delete column" "remove column" "delete row" "remove row" "delete empty rows" "delete empty columns"
  触发词包括"删除列""去掉第X列""移除列""删除行""去掉第X行""移除行""删掉空行""删掉空列"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Must complete Requirement Parsing→Scout→Plan before execution, and Verify after. **Must check formula dependencies before deletion.**
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须完成 需求解析→勘察→规划，执行后必须验证。**删除前必须检查公式依赖。**

# Excel Safe Delete (Row & Column) / Excel 安全删除（行列通用）

## 核心原则

| 模式 | 引擎 | 原因 |
|------|------|------|
| **行删除** | XML 直接操作 | 快 10 倍，格式/公式无损 |
| **列删除** | openpyxl `delete_cols()` | 列删除需逐行移除 cell，XML 太复杂 |

## 第零步：需求解析

### 自动识别删除类型

| 用户说 | 判定 |
|--------|:--:|
| "删除列""去掉列""移除列""E列""第3列""空列" | → 列模式 |
| "删除行""去掉行""移除行""第5行""空行" | → 行模式 |

### 解析示例

| 用户说 | 提取 |
|--------|------|
| "把E列删掉" | 列模式, 目标=列E |
| "删除第5行到第10行" | 行模式, 目标=[5,6,7,8,9,10] |
| "清理所有空行" | 行模式, 自动扫描空行 |
| "删掉申请日那一列" | 列模式, 目标=申请日(勘察定位) |

## 第一步：勘察（含公式依赖检查）

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

# 展示结构
print('\n=== 表头 ===')
for col_idx in range(1, ws.max_column + 1):
    h = ws.cell(row=1, column=col_idx).value
    if h:
        col_letter = chr(64 + col_idx) if col_idx <= 26 else f'col{col_idx}'
        print(f'  列{col_idx} [{col_letter}]: {h}')

targets = []  # 列模式：列号列表；行模式：行号列表

# ⚠️ 关键：公式依赖检查
print('\n=== 公式依赖检查 ===')
wb2 = load_workbook(FILE, data_only=True)
ws2 = wb2.active

has_risk = False
if MODE == 'column':
    for col_idx in range(1, ws.max_column + 1):
        if col_idx in targets:
            continue
        for row_idx in range(1, min(50, ws.max_row + 1)):
            v_raw = ws.cell(row=row_idx, column=col_idx).value
            if v_raw and isinstance(v_raw, str) and v_raw.startswith('='):
                for tc in targets:
                    col_letter = chr(64 + tc) if tc <= 26 else ''
                    if col_letter and col_letter in v_raw:
                        print(f'  ⚠️ 列{col_idx}行{row_idx}引用被删列{col_letter}: {v_raw[:60]}')
                        has_risk = True
elif MODE == 'row':
    for col_idx in range(1, ws.max_column + 1):
        for row_idx in range(1, min(50, ws.max_row + 1)):
            if row_idx in targets:
                continue
            v_raw = ws.cell(row=row_idx, column=col_idx).value
            if v_raw and isinstance(v_raw, str) and v_raw.startswith('='):
                for tr in targets:
                    if str(tr) in v_raw:
                        print(f'  ⚠️ 列{col_idx}行{row_idx}引用被删行{tr}: {v_raw[:60]}')
                        has_risk = True

wb2.close()

if has_risk:
    print('\n⚠️ 发现公式依赖，删除后可能产生 #REF! 错误。')

print(f'\n准备删除 {len(targets)} 个{MODE}: {targets}')
```

## 第二步：规划

- **删除顺序**：列模式从右到左，行模式 XML 不需要排序（按集合判断）
- **风险评估**：有公式依赖 → 告知用户确认后再删
- **空行/空列扫描**：如需自动识别空行，逐行/列检查是否全为 None

## 第三步：执行

### 行模式 — XML 直接操作（默认）

```python
import zipfile, os, shutil, re, time
from lxml import etree

t0 = time.time()
FILE = '目标文件.xlsx'
ROW_SET = set(TARGETS)  # 要删除的行号集合

# 1. 备份
BACKUP = FILE.replace('.xlsx', '_backup.xlsx')
if not os.path.exists(BACKUP):
    shutil.copy2(FILE, BACKUP)
    print(f'已备份: {BACKUP}')

# 2. 解压
TMP = FILE.replace('.xlsx', '_xml_tmp')
if os.path.exists(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)
with zipfile.ZipFile(FILE, 'r') as z:
    z.extractall(TMP)

# 3. 遍历所有 sheet XML，删除目标行
worksheets_dir = os.path.join(TMP, 'xl', 'worksheets')
for sf in sorted(os.listdir(worksheets_dir)):
    if not sf.endswith('.xml'):
        continue
    sp = os.path.join(worksheets_dir, sf)

    parser = etree.XMLParser(remove_blank_text=False, huge_tree=True)
    tree = etree.parse(sp, parser)
    root = tree.getroot()
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

    deleted = 0
    for row_elem in root.findall('.//s:row', ns):
        if int(row_elem.get('r')) in ROW_SET:
            row_elem.getparent().remove(row_elem)
            deleted += 1

    if deleted == 0:
        continue

    # 清理被删行相关的合并单元格
    for mc in root.findall('.//s:mergeCells/s:mergeCell', ns):
        m = re.match(r'[A-Z]+(\d+):[A-Z]+(\d+)', mc.get('ref', ''))
        if m and all(int(m.group(1)) <= r <= int(m.group(2)) for r in [int(m.group(1)), int(m.group(2))]):
            if all(r in ROW_SET for r in range(int(m.group(1)), int(m.group(2)) + 1)):
                mc.getparent().remove(mc)

    # 更新 dimension
    dim = root.find('.//s:dimension', ns)
    if dim is not None:
        remaining = sorted([int(re.get('r')) for re in root.findall('.//s:row', ns)])
        all_cols = []
        for re in root.findall('.//s:row', ns):
            for c in re.findall('s:c', ns):
                m = re.match(r'([A-Z]+)', c.get('r', ''))
                if m: all_cols.append(m.group(1))
        if remaining and all_cols:
            max_col = max(all_cols, key=lambda x: (len(x), x))
            dim.set('ref', f'A1:{max_col}{max(remaining)}')

    # 写回
    sheet_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    with open(sp, 'wb') as f:
        f.write(sheet_xml)
    print(f'  {sf}: 删除 {deleted} 行')

# 4. 重新打包
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for dirpath, _, filenames in os.walk(TMP):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            zout.write(full, os.path.relpath(full, TMP).replace('\\', '/'))

shutil.rmtree(TMP)
print(f'完成，耗时 {time.time()-t0:.1f}s')
```

### ⚠️ 删除后必须询问：是否压实行号 / Must Ask After Deletion: Compact Row Numbers?

XML 删除行后，行号不再连续，Excel 打开会显示空白行。删除完成后 **必须询问用户**：

> "删除完成。XML 删除后行号不连续，Excel 中会出现空白行。是否压实行号（重新连续编号）？"

用户确认后执行压实：

```python
# 压实行号：把剩余行重新连续编号，同时更新公式中的行引用
from compact_rows import compact_xlsx
# 或直接用内联版本（见下方）

import re
from lxml import etree

TMP2 = FILE.replace('.xlsx', '_compact_tmp')
os.makedirs(TMP2, exist_ok=True)
with zipfile.ZipFile(FILE, 'r') as z:
    z.extractall(TMP2)

worksheets_dir = os.path.join(TMP2, 'xl', 'worksheets')
parser = etree.XMLParser(remove_blank_text=False, huge_tree=True)

for sf in sorted(os.listdir(worksheets_dir)):
    if not sf.endswith('.xml'): continue
    sp = os.path.join(worksheets_dir, sf)
    tree = etree.parse(sp, parser)
    root = tree.getroot()
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

    # 收集行并构建 old→new 映射
    rows_info = sorted(
        [(int(re.get('r')), re) for re in root.findall('.//s:row', ns)],
        key=lambda x: x[0]
    )
    old_to_new = {}
    next_new = 1
    for old_r, _ in rows_info:
        old_to_new[old_r] = next_new
        next_new += 1

    # 检查是否需要压实
    if all(o == n for o, n in old_to_new.items()):
        continue

    formulas_updated = 0
    for old_r, row_elem in rows_info:
        new_r = old_to_new[old_r]
        if old_r == new_r:
            continue
        row_elem.set('r', str(new_r))
        for cell in row_elem.findall('s:c', ns):
            old_ref = cell.get('r', '')
            m = re.match(r'([A-Z]+)(\d+)', old_ref)
            if m:
                cell.set('r', f'{m.group(1)}{new_r}')
            f_elem = cell.find('s:f', ns)
            if f_elem is not None and f_elem.text:
                new_f = re.sub(r'([A-Z]+)(\d+)',
                    lambda m: f'{m.group(1)}{old_to_new[int(m.group(2))]}' if int(m.group(2)) in old_to_new else m.group(0),
                    f_elem.text)
                if new_f != f_elem.text:
                    f_elem.text = new_f
                    formulas_updated += 1

    # 更新合并单元格
    for mc in root.findall('.//s:mergeCells/s:mergeCell', ns):
        m = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', mc.get('ref', ''))
        if m and int(m.group(2)) in old_to_new and int(m.group(4)) in old_to_new:
            mc.set('ref', f'{m.group(1)}{old_to_new[int(m.group(2))]}:{m.group(3)}{old_to_new[int(m.group(4))]}')

    # 更新 dimension
    dim = root.find('.//s:dimension', ns)
    if dim is not None and rows_info:
        all_cols = []
        for _, re_elem in rows_info:
            for c in re_elem.findall('s:c', ns):
                m = re.match(r'([A-Z]+)', c.get('r', ''))
                if m: all_cols.append(m.group(1))
        if all_cols:
            max_col = max(all_cols, key=lambda x: (len(x), x))
            dim.set('ref', f'A1:{max_col}{max(old_to_new.values())}')

    sheet_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    with open(sp, 'wb') as f:
        f.write(sheet_xml)
    print(f'  {sf}: {sum(1 for o,n in old_to_new.items() if o!=n)} 行压实, {formulas_updated} 公式更新')

with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for dirpath, _, filenames in os.walk(TMP2):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            zout.write(full, os.path.relpath(full, TMP2).replace('\\', '/'))
shutil.rmtree(TMP2)
print('压实完成')
```

### 列模式 — openpyxl（保持不变）

```python
import time
t0 = time.time()

wb = load_workbook(FILE)
ws = wb.active

# 从右到左删除
for col_idx in sorted(TARGETS, reverse=True):
    header = ws.cell(row=1, column=col_idx).value
    print(f'删除列{col_idx} "{header}"')
    ws.delete_cols(col_idx)

wb.save(FILE)
print(f'完成，耗时 {time.time()-t0:.1f}s，剩余: {ws.max_row}行 × {ws.max_column}列')
```

## 第四步：验证

```python
wb = load_workbook(FILE, read_only=True, data_only=True)
ws = wb.active

print(f'当前: {ws.max_row}行 × {ws.max_column}列')

# 公式健康检查
print('\n=== 公式健康检查 ===')
ref_errors = 0
for row_idx in range(1, min(50, ws.max_row + 1)):
    for col_idx in range(1, ws.max_column + 1):
        v = ws.cell(row=row_idx, column=col_idx).value
        if v and isinstance(v, str) and '#REF!' in v:
            print(f'  ❌ 列{col_idx}行{row_idx}: {v}')
            ref_errors += 1
if ref_errors == 0:
    print('  ✅ 无 #REF! 错误')

# 验证被删行确实不存在
if MODE == 'row':
    for tr in TARGETS[:5]:  # 抽查前5个被删行
        v = ws.cell(row=tr, column=1).value
        print(f'  被删行{tr}: {v} (应为None表示已删除)')

wb.close()
```

## 特殊场景：自动扫描空行/空列

```python
# 扫描空行（所有列该行值均为 None）
empty_rows = []
for row_idx in range(2, ws.max_row + 1):
    all_empty = True
    for col_idx in range(1, ws.max_column + 1):
        if ws.cell(row=row_idx, column=col_idx).value is not None:
            all_empty = False
            break
    if all_empty:
        empty_rows.append(row_idx)

# 扫描空列（所有数据行该列值均为 None）
empty_cols = []
for col_idx in range(1, ws.max_column + 1):
    all_empty = True
    for row_idx in range(2, ws.max_row + 1):
        if ws.cell(row=row_idx, column=col_idx).value is not None:
            all_empty = False
            break
    if all_empty:
        empty_cols.append(col_idx)

print(f'空行: {empty_rows}, 空列: {empty_cols}')
```

## 注意事项

1. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——删除前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
2. **行删除用 XML**：不调用 `delete_rows()`，直接操作 sheet XML
3. **列删除用 openpyxl**：XML 列删除太复杂，保持原方案
4. **大文件需 lxml**：`pip install lxml`，配合 `huge_tree=True`
5. **间接引用**：INDIRECT、OFFSET 不会被自动检测到
6. **合并单元格**：XML 方案自动清理涉及被删行的合并定义
