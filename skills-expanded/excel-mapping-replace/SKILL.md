---
name: excel-mapping-replace
description: |
  Batch replace column values by mapping table. User provides mapping relationships (spoken in conversation / pasted list / mapping file), and the skill auto-matches and replaces corresponding values in the target column. Values not in the mapping table are preserved as-is.
  按映射表批量替换某列的值。用户提供映射关系（对话直说/粘贴列表/映射文件），技能自动匹配并替换目标列中对应的值。映射表中不存在的值保留原样。
  Trigger keywords: "mapping replace" "batch replace" "by lookup table" "convert codes" "corresponding replace"
  触发词包括"映射替换""批量替换""按对照表""换成代码""对应替换"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Mapping matching uses pandas, value replacement uses openpyxl (small files) or XML (large files).
> 本技能遵循 [[excel-safe-workflow]] 四步法。映射匹配用 pandas，值替换用 openpyxl（小文件）或 XML（大文件）。

# Excel Mapping Replace / Excel 映射替换

## 功能

给一张映射表，把目标列中匹配的值全部替换。

```
映射表:                          目标列替换前 → 替换后:
  中国 → CN                      中国 → CN
  日本 → JP                      中国 → CN
  美国 → US                      日本 → JP
  德国 → DE                      中国 → CN
  ...                            ...
```

**映射表中不存在的值保留原样，不会丢失数据。**

## 第零步：需求解析

| 要素 | 用户说 | 默认值 |
|------|--------|--------|
| **目标列** | "公开国别""状态列" | 必须明确 |
| **映射关系** | "中国→CN，日本→JP" / 粘贴列表 / 映射文件 | 必须明确 |
| **映射来源** | 对话口述 / 粘贴文本 / xlsx文件 | 对话口述 |

### 映射关系格式

```
# 对话直说（几个映射）
"中国换成CN，日本换成JP，美国换成US"

# 粘贴列表（几十个映射）
中国 → CN
日本 → JP
美国 → US
...

# 映射文件（几百个映射）
"用 国家代码表.xlsx 的 A列→B列 做映射"
```

## 第一步：勘察

```python
import pandas as pd

FILE = '目标文件.xlsx'
TARGET_COL = '列名'

df = pd.read_excel(FILE)
print(f'总行数: {len(df)}')

vc = df[TARGET_COL].value_counts()
print(f'唯一值: {len(vc)}')
for k, v in vc.head(20).items():
    print(f'  {k}: {v}')
```

## 第二步：规划

- 确认目标列和映射表
- 统计有多少行会受影响（映射表 ∩ 列中的值）
- 列出映射表中**不存在**的值（不会被改动）
- 确认无误后执行

## 第三步：执行

> ⚠️ **禁止在 sharedStrings 层做全局替换**。必须走 sheet 层 + 列号限定，只改目标列的 cell。

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import os, shutil, re, time

FILE = '目标文件.xlsx'
TARGET_COL = '列名'
MAPPING = {'旧值1': '新值1', '旧值2': '新值2', ...}

# ====== 3.1 勘察 ======
df = pd.read_excel(FILE)
col_idx = list(df.columns).index(TARGET_COL) + 1  # 列号（1-based）
col_letter = get_column_letter(col_idx)

# 统计影响
affected = {k: v for k, v in df[TARGET_COL].value_counts().items() if k in MAPPING}
unmatched = {k: v for k, v in df[TARGET_COL].value_counts().items() if k not in MAPPING}

print(f'目标列: {TARGET_COL} ({col_letter}), 将替换:')
for k, v in affected.items():
    print(f'  {k} → {MAPPING[k]}: {v} 行')
if unmatched:
    print(f'\n不在映射表中（保留原值）:')
    for k, v in unmatched.items():
        print(f'  {k}: {v} 行')

# ====== 3.2 执行 ======
USE_XML = os.path.getsize(FILE) > 10 * 1024 * 1024  # >10MB

if USE_XML:
    # ====== XML 方案：sheet 层 + 列号限定 + inline 写入 ======
    print('\n替换中（XML sheet 层方案）...')
    import zipfile
    from lxml import etree

    t0 = time.time()
    TMP = FILE.replace('.xlsx', '_mp_tmp')
    if os.path.exists(TMP): shutil.rmtree(TMP)
    os.makedirs(TMP)
    with zipfile.ZipFile(FILE, 'r') as z:
        z.extractall(TMP)

    S_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    parser = etree.XMLParser(remove_blank_text=False, huge_tree=True)
    ns = {'s': S_NS}

    # 读 sharedStrings 建立 si→text 映射（只读，用于解析 t="s" 的 cell）
    ss_path = os.path.join(TMP, 'xl', 'sharedStrings.xml')
    si_lookup = {}
    if os.path.exists(ss_path):
        ss_tree = etree.parse(ss_path, parser)
        for idx, si_elem in enumerate(ss_tree.findall('.//s:si', ns)):
            t_elem = si_elem.find('s:t', ns)
            si_lookup[idx] = t_elem.text if t_elem is not None else ''

    # 处理 sheet XML — 只在目标列上改值
    ws_dir = os.path.join(TMP, 'xl', 'worksheets')
    replaced = 0
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

                # 获取当前文本值
                cell_type = cell.get('t', '')
                val = None
                if cell_type == 's':
                    v_elem = cell.find('s:v', ns)
                    if v_elem is not None and v_elem.text:
                        val = si_lookup.get(int(v_elem.text), '')
                else:
                    is_elem = cell.find('s:is', ns)
                    if is_elem is not None:
                        t_elem = is_elem.find('s:t', ns)
                        val = t_elem.text if t_elem is not None else ''

                if val is None or val not in MAPPING:
                    continue

                # 改为 inline 字符串（不创建新的 sharedString 引用）
                new_val = MAPPING[val]
                cell.set('t', 'inlineStr')
                for child in list(cell):
                    tag = child.tag.split('}')[-1]
                    if tag in ('v', 'f', 'is'): cell.remove(child)
                is_new = etree.SubElement(cell, '{'+S_NS+'}is')
                t_new = etree.SubElement(is_new, '{'+S_NS+'}t')
                t_new.text = new_val
                replaced += 1

        sheet_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        with open(sp, 'wb') as f: f.write(sheet_xml)

    print(f'  替换 {replaced} 个单元格')

    # 打包
    with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
        for dirpath, _, filenames in os.walk(TMP):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                zout.write(full, os.path.relpath(full, TMP).replace('\\\\', '/'))
    shutil.rmtree(TMP)
    print(f'  耗时: {time.time()-t0:.0f}s')

else:
    # ====== openpyxl 方案（小文件，简单可靠）======
    print('\n替换中（openpyxl 方案）...')

    # 备份
    bak = FILE.replace('.xlsx', '_backup.xlsx')
    if not os.path.exists(bak):
        shutil.copy2(FILE, bak)

    t0 = time.time()
    wb = load_workbook(FILE)
    ws = wb.active

    replaced = 0
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=col_idx)
        if cell.value in MAPPING:
            cell.value = MAPPING[cell.value]
            replaced += 1
        if row % 50000 == 0:
            print(f'  进度: {row}/{ws.max_row}')

    wb.save(FILE)
    wb.close()
    print(f'  替换: {replaced} 个, 耗时: {time.time()-t0:.1f}s')
```

## 第四步：验证

```python
df2 = pd.read_excel(FILE)
print(f'\n替换后 [{TARGET_COL}] 分布:')
for k, v in df2[TARGET_COL].value_counts().items():
    marker = ' ← 新' if k in MAPPING.values() else ''
    print(f'  {k}: {v}{marker}')

# 确认未映射值没被修改
for old_val in unmatched:
    still_there = (df2[TARGET_COL] == old_val).sum()
    if still_there != unmatched[old_val]:
        print(f'  ❌ {old_val}: 预期{unmatched[old_val]}行, 实际{still_there}行')
```

## 从映射文件读取

```python
# 从另一个 xlsx/csv 读取映射表
map_df = pd.read_excel('映射文件.xlsx')
MAPPING = dict(zip(map_df.iloc[:, 0], map_df.iloc[:, 1]))
# 或从 csv
# map_df = pd.read_csv('映射文件.csv')
# MAPPING = dict(zip(map_df['中文'], map_df['代码']))
```

## 注意事项

1. **映射表不匹配的值不动**：只替换映射表中存在的值，其余原样保留
2. **精确匹配**：不是包含匹配。`中国` 只匹配 `中国`，不匹配 `中国北京`
3. **⚠️ XML 方案只在目标列上改值**：通过列号限定 `cell.get('r').startswith(col_letter)`，不会误伤其他列。**禁止**在 sharedStrings 层做全局替换
4. **改值后写 inline string**：替换后的值写为 `<is><t>` 内联字符串，不产生新的 sharedString 引用
5. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
6. **文件被占用**：如果目标文件正在 Excel 中打开，会保存失败。提示用户关闭后重试
7. **大小写敏感**：`China` ≠ `china`，如需不敏感需预处理
