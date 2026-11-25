---
name: excel-split
description: |
  Split a large table into multiple files by a specified column (one file per unique value). Uses pandas grouping + iterparse streaming fan-out (single XML parse, multi-output), with format fully preserved. Supports limiting split count (Top N + Others).
  按指定列将一个大表拆分成多个文件（每个值一个文件）。用 pandas 分组 + iterparse 流式分流（一次解析XML，多路输出），格式完整保留。支持限制拆分数量（Top N + 其他）。
  Trigger keywords: "split" "separate" "split by" "split into files" "break apart by"
  触发词包括"拆分""拆开""按xx分开""分表""拆成多个文件"。
---

> This skill follows [[excel-safe-workflow]] four-step method. Grouping uses pandas, fan-out uses lxml iterparse single-scan multi-output.
> 本技能遵循 [[excel-safe-workflow]] 四步法。分组用 pandas，分流用 lxml iterparse 一次扫描多路输出。

# Excel Split / Excel 拆分

## 功能

把一张大表按某列的值拆成 N 个独立文件。

```
总表 (33万行)
  │
  │ 按"申请人"拆分 Top 10
  │
  ├── 上海诺基亚贝尔.xlsx    (1859行)
  ├── 上海泰康网络.xlsx      (1301行)
  ├── ... (8个)
  └── 其他.xlsx              (283145行)
```

## 第零步：需求解析

| 要素 | 用户说 | 默认值 |
|------|--------|--------|
| **拆分列** | "按申请人拆""按年份分" | 必须明确 |
| **Top N** | "前10个""最多的20个" | 20 |
| **输出目录** | "放到 split 文件夹" | `{原文件名}_split_{列名}/` |

## 第一步：勘察

```python
import pandas as pd

FILE = '目标文件.xlsx'
SPLIT_COL = '列名'

df = pd.read_excel(FILE)
counts = df[SPLIT_COL].value_counts()
print(f'总行数: {len(df)}, 唯一值: {len(counts)}')
print(f'Top 10:')
for k, v in counts.head(10).items():
    print(f'  {k}: {v} 行')
```

## 第二步：规划

- **Top N 限制**：唯一值太多时（>50），只拆 Top N，其余合并为"其他"
- **先压实**：如果文件之前做过去重/筛选（有行号空隙），先压实再拆分，否则 pandas 扫描行数会偏高
- **输出目录**：`{原文件名}_split/`
- **文件命名**：`{拆分值}.xlsx`（自动清理非法字符）

## 第三步：执行

核心思路：**一次 iterparse 流式解析 XML，按行分流到各输出缓冲区**，避免重复解析。

```python
import pandas as pd, zipfile, os, shutil, re, time
from lxml import etree
from collections import defaultdict

S_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

FILE = '目标文件.xlsx'
SPLIT_COL = '列名'
TOP_N = 20
OUTPUT_DIR = FILE.replace('.xlsx', f'_split_{SPLIT_COL}')

# ====== 3.1 pandas 分组 ======
print(f'[1/4] pandas 分组...')
df = pd.read_excel(FILE).dropna(how='all')  # 去掉空行（如有间隙）
total = len(df)
counts = df[SPLIT_COL].value_counts()
top_keys = set(counts.head(TOP_N).index.tolist()) if len(counts) > TOP_N else set(counts.index)

row_to_file = {}
file_sizes = defaultdict(int)
for key in top_keys:
    safe = str(key).replace('/', '_').replace('\\', '_').replace(':', '_')[:80]
    indices = df.index[df[SPLIT_COL] == key].tolist()
    for i in indices:
        row_to_file[i + 2] = f'{safe}.xlsx'
    file_sizes[f'{safe}.xlsx'] = len(indices)

other = df.index[~df[SPLIT_COL].isin(top_keys)].tolist()
if other:
    for i in other:
        row_to_file[i + 2] = '其他.xlsx'
    file_sizes['其他.xlsx'] = len(other)

print(f'  将生成 {len(file_sizes)} 个文件')

# ====== 3.2 解压 ======
print(f'[2/4] 解压...')
TMP = FILE.replace('.xlsx', '_split_tmp')
if os.path.exists(TMP): shutil.rmtree(TMP)
os.makedirs(TMP)
with zipfile.ZipFile(FILE, 'r') as z:
    z.extractall(TMP)

worksheets_dir = os.path.join(TMP, 'xl', 'worksheets')
orig_sheet = None
for sf in sorted(os.listdir(worksheets_dir)):
    if sf.endswith('.xml') and sf.startswith('sheet'):
        orig_sheet = os.path.join(worksheets_dir, sf)
        break

# ====== 3.3 iterparse 流式分流 ======
print(f'[3/4] 流式分流...')
row_xml = defaultdict(list)
header_xml = []

tag = f'{{{S_NS}}}row'
for event, elem in etree.iterparse(orig_sheet, tag=tag):
    r = int(elem.get('r'))
    row_str = etree.tostring(elem, encoding='unicode')

    if r == 1:  # 表头行
        header_xml.append(row_str)
    elif r in row_to_file:
        row_xml[row_to_file[r]].append(row_str)

    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]

# ====== 3.4 生成输出文件 ======
print(f'[4/4] 生成输出文件...')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 构建 sheet XML 模板（<sheetData> 前后的结构）
tree_orig = etree.parse(orig_sheet, etree.XMLParser(huge_tree=True))
full_xml = etree.tostring(tree_orig.getroot(), encoding='unicode')
sd_start = full_xml.find('<sheetData')
sd_end = full_xml.find('</sheetData>')
prefix = full_xml[:sd_start]
suffix = full_xml[sd_end + len('</sheetData>'):]

for idx, (fname, rows) in enumerate(sorted(row_xml.items(), key=lambda x: -len(x[1]))):
    fpath = os.path.join(OUTPUT_DIR, fname)
    all_rows = ''.join(header_xml) + ''.join(rows)
    new_xml = f'{prefix}<sheetData>{all_rows}</sheetData>{suffix}'

    with open(orig_sheet, 'w', encoding='utf-8') as f:
        f.write(new_xml)

    with zipfile.ZipFile(fpath, 'w', zipfile.ZIP_DEFLATED) as zout:
        for dirpath, _, filenames in os.walk(TMP):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                zout.write(full, os.path.relpath(full, TMP).replace('\\', '/'))

shutil.rmtree(TMP)
print(f'完成，输出: {OUTPUT_DIR}/')
```

## 第四步：验证

```python
import pandas as pd, os

total_out = 0
for f in os.listdir(OUTPUT_DIR):
    if not f.endswith('.xlsx'): continue
    fp = os.path.join(OUTPUT_DIR, f)
    df = pd.read_excel(fp).dropna(how='all')
    total_out += len(df)

    if f != '其他.xlsx':
        key = f.replace('.xlsx', '')
        bad = df[df[SPLIT_COL] != key].shape[0]
        if bad: print(f'  ❌ {f}: {bad} 行错配')

print(f'输出总行: {total_out} (期望 {total})')
```

## 性能

| 文件 | 行数 | 输出文件数 | pandas扫描 | iterparse分流 | 生成打包 | 总耗时 |
|------|------|:--:|------|------|------|------|
| 测试文件 | 914 | 6 | 1s | 0s | 0s | 1s |
| 主文件 | 29万 | 11 | 82s | 51s | 258s | ~6.5min |

> 生成打包阶段耗时较长是因为每个输出文件都包含完整的 sharedStrings.xml（273MB），11 个文件约 3GB 压缩量。迭代次数越多，此阶段越慢。

## 注意事项

1. **拆分前先压实**：如果文件做过去重/筛选有行号空隙，先用 [[excel-delete]] 中的压实功能
2. **共享字符串膨胀**：每个输出文件继承完整的 sharedStrings，N 个文件 = N × 原始大小
3. **大文件建议限制 Top N**：默认 Top 20，避免生成数百个文件
4. **iterparse 内存友好**：一次只保有一个 row 元素，33万行约占用 100-200MB 内存
5. **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——拆分前自动备份原文件（时间戳命名），成功后保留最新3份
