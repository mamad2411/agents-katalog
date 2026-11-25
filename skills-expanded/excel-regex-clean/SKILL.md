---
name: excel-regex-clean
description: |
  Use regular expressions to clean Excel column content — extract, delete, or replace matched portions. Supports three modes: extract (capture matched content), remove (delete matched content), replace (substitute matched content). XML fast path for large files (4x faster).
  用正则表达式清理 Excel 某列的内容——提取、删除或替换匹配的部分。支持三种模式：extract（提取匹配内容）、remove（删除匹配内容）、replace（替换匹配内容）。大文件走 XML 快速路径（快 4x）。
  Trigger keywords: "regex" "clean" "extract" "remove numbers" "keep only" "clean up"
  触发词包括"正则""清理""提取""删除xxx部分""去掉数字""只保留""清洗"。
---

> This skill follows [[excel-safe-workflow]]. Regex processing uses Python `re` module. Large files (>10MB) use XML direct ops on sheet XML (4x faster), small files use openpyxl.
> 本技能遵循 [[excel-safe-workflow]]。正则处理用 Python `re` 模块。大文件（>10MB）用 XML 直接操作 sheet XML（快 4 倍），小文件用 openpyxl。

# Excel Regex Clean / Excel 正则清理

## Three Modes / 三种模式

| 模式 | 用户说 | 正则怎么写 | 效果 |
|------|--------|-----------|------|
| **extract** | "只保留括号里的""提取中文部分" | 用捕获组 `()` 圈出要保留的 | `1.1 (新一代)` → `新一代` |
| **remove** | "删掉所有数字和点""去掉空格" | 匹配要删除的部分 | `1.1 新一代` → `新一代` |
| **replace** | "把空格换成下划线""把CN改成中国" | 匹配→替换 | `新一代 产业` → `新一代_产业` |

## 第零步：需求解析

| 用户说 | 解析 |
|--------|------|
| "删掉新兴产业列的数字、点和括号，只留中文" | extract模式, 提取括号内中文 |
| "把申请日里的横线去掉" | remove模式, 删掉 `-` |
| "把空格全部换成下划线" | replace模式, ` ` → `_` |
| "去掉所有数字" | remove模式, `\d+` |
| "只保留英文字母" | extract模式, `[A-Za-z]+` |

### 常用正则速查 / Common Regex Quick Reference

| 要匹配 | 正则 |
|--------|------|
| 数字 | `\d+` |
| 英文点 | `\.` |
| 括号及内容 | `\([^)]*\)` |
| 括号里的内容（提取用） | `\((.+)\)` |
| 中文 | `[一-龥]+` |
| 空格 | `\s+` |
| 英文字母 | `[A-Za-z]+` |

## 第一步：勘察

```python
import pandas as pd, re

FILE = '目标文件.xlsx'
TARGET_COL = '列名'

df = pd.read_excel(FILE)
vc = df[TARGET_COL].value_counts()
print(f'列 [{TARGET_COL}] 唯一值: {len(vc)}')

# 展示前20行 + 变换预览
MODE = 'extract'       # extract / remove / replace
PATTERN = r'\((.+)\)'  # 正则
REPLACE = ''           # replace 模式时的替换文本

print('\n变换预览:')
count = 0
for idx, val in df[TARGET_COL].items():
    if pd.notna(val) and count < 20:
        old = str(val)
        if MODE == 'extract':
            m = re.search(PATTERN, old)
            new = m.group(1) if m else old
        elif MODE == 'remove':
            new = re.sub(PATTERN, '', old)
        else:  # replace
            new = re.sub(PATTERN, REPLACE, old)

        if new != old:
            print(f'  {old[:60]}  →  {new[:60]}')
            count += 1
```

## 第二步：规划

- 确认模式和正则，预览无误后执行
- 正则不会的让用户直接描述需求，自动推断

## 第三步：执行

> ⚠️ **XML 方案必须在 sheet 层 + 列号限定**，不碰 sharedStrings。

```python
import re, os, shutil, time
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# ===== 用户配置 =====
FILE = '目标文件.xlsx'
TARGET_COL = '列名'
MODE = 'extract'       # extract / remove / replace
PATTERN = r'\((.+)\)'  # 正则
REPLACE = ''           # replace 模式时使用
# ====================

df = pd.read_excel(FILE)
col_idx = list(df.columns).index(TARGET_COL) + 1
col_letter = get_column_letter(col_idx)

# 副本（不修改原文件）
OUT = FILE.replace('.xlsx', '_cleaned.xlsx')
shutil.copy2(FILE, OUT)

SIZE_MB = os.path.getsize(FILE) / 1024 / 1024
USE_XML = SIZE_MB > 10  # >10MB 走 XML 快速路径

# ====== 正则处理函数 ======
def apply_regex(val):
    old = str(val) if val is not None else ''
    if MODE == 'extract':
        m = re.search(PATTERN, old)
        new = m.group(1) if m else old
    elif MODE == 'remove':
        new = re.sub(PATTERN, '', old)
    else:  # replace
        new = re.sub(PATTERN, REPLACE, old)
    return new, new != old

# ====== XML 快速路径 ======
if USE_XML:
    print(f'\n替换中（XML sheet 层方案, {SIZE_MB:.0f}MB）...')
    import zipfile
    from lxml import etree

    t0 = time.time()
    TMP = OUT.replace('.xlsx', '_rgx_tmp')
    if os.path.exists(TMP): shutil.rmtree(TMP)
    os.makedirs(TMP)
    with zipfile.ZipFile(OUT, 'r') as z:
        z.extractall(TMP)

    S_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    parser = etree.XMLParser(remove_blank_text=False, huge_tree=True)
    ns = {'s': S_NS}

    # 读 sharedStrings 建立 si→text 映射（只读）
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
                    else:
                        v_elem = cell.find('s:v', ns)
                        val = str(v_elem.text) if v_elem is not None and v_elem.text else ''

                if val is None:
                    continue

                new, changed = apply_regex(val)
                if not changed:
                    continue

                # 改为 inline 字符串
                cell.set('t', 'inlineStr')
                for child in list(cell):
                    tag = child.tag.split('}')[-1]
                    if tag in ('v', 'f', 'is'): cell.remove(child)
                is_new = etree.SubElement(cell, '{'+S_NS+'}is')
                t_new = etree.SubElement(is_new, '{'+S_NS+'}t')
                t_new.text = new
                replaced += 1

        sheet_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        with open(sp, 'wb') as f: f.write(sheet_xml)

    print(f'  替换 {replaced} 个单元格')

    # 打包
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
        for dirpath, _, filenames in os.walk(TMP):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                zout.write(full, os.path.relpath(full, TMP).replace('\\\\', '/'))
    shutil.rmtree(TMP)
    print(f'  耗时: {time.time()-t0:.0f}s')

# ====== openpyxl 方案（小文件）======
else:
    print(f'\n替换中（openpyxl 方案, {SIZE_MB:.0f}MB）...')
    t0 = time.time()
    wb = load_workbook(OUT)
    ws = wb.active

    replaced = 0
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=col_idx)
        new, changed = apply_regex(cell.value)
        if changed:
            cell.value = new
            replaced += 1
        if row % 50000 == 0:
            print(f'  进度: {row}/{ws.max_row}')

    wb.save(OUT)
    wb.close()
    print(f'  替换: {replaced} 个, 耗时: {time.time()-t0:.1f}s')

print(f'输出: {OUT}')
```

## 第四步：验证

```python
df2 = pd.read_excel(OUT)
print(f'\n处理后 [{TARGET_COL}] 分布:')
for k, v in df2[TARGET_COL].value_counts().items():
    print(f'  {k}: {v}')
```

## 注意事项

1. **副本操作**：自动生成 `_cleaned.xlsx`，不修改原文件
2. **正则只处理目标列**：XML 方案通过列号限定，openpyxl 方案只遍历目标列，不影响其他列
3. **匹配不到保留原值**：extract 模式中正则不匹配的保留原样
4. **改值后写 inline string**（XML 方案）：替换后的值写为 `<is><t>` 内联字符串，不产生新的 sharedString 引用
5. **大文件自动走 XML**：>10MB 或 >5万行自动使用 XML sheet 层方案，速度快 4 倍
6. **正则需转义**：`.` `(` `)` `\` 等特殊字符前加 `\`
7. **建议先预览**：看到变换效果后再执行
8. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名），成功后保留最新3份，失误后立即删除损坏文件并从备份恢复
