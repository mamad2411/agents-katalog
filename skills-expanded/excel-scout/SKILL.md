---
name: excel-scout
description: |
  Pre-operation reconnaissance — read-only scan of Excel files to locate columns relevant to user needs, output a structured scout report for user confirmation. Makes no modifications. When users describe complex Excel operation needs but haven't specified column numbers/names/current values, use this skill first to understand "what's in the file and which columns need to be operated on."
  操作前勘察——只读扫描 Excel 文件，定位用户需求涉及的列，输出结构化勘察报告供用户确认。不做任何修改。当用户提出复杂 Excel 操作需求但未明确指定列号/列名/当前值时，先调用此技能搞清楚"文件里有什么、哪些列要被操作"。
  Trigger keywords: "scout" "explore" "take a look" "check the file" "what columns" "find date columns" "inspect" "survey"
  触发词包括"先看看""勘察一下""确认一下列""看看文件结构""有哪些日期列""查一下""scout""探索""了解文件"。
---

> This skill is **read-only, no side effects**. Uses openpyxl read_only + pandas sampling for fast scanning. It is the prerequisite step for all other operation skills.
> 本技能**只读不写**，安全无副作用。用 openpyxl read_only + pandas 采样快速扫描，是其他所有操作技能的前置步骤。

# Excel Pre-Operation Scout / Excel 操作前勘察

## Purpose / 定位

This skill solves a high-frequency pain point: **users describe needs in business language ("convert dates to yyyymmdd", "change country codes to Chinese names"), but don't know which column corresponds to what or what the current values are.** Figure out the target columns before operating, to avoid modifying wrong columns.

本技能解决一个高频痛点：**用户描述需求时用的是业务语言（"把日期转成 yyyymmdd""国别代码改中文"），但不知道文件里哪一列对应、当前值是什么。** 在动手前先搞清楚目标列，避免改错列。

```
User Request (business language) / 用户需求（业务语言）
    │
    ▼
excel-scout: Scan file → Locate target columns → Show current values → Confirm operation scope
             扫描文件 → 定位目标列 → 展示当前值 → 确认操作范围
    │
    ▼
Other skills: Execute operations on confirmed target columns / 其他技能: 在已确认的目标列上执行操作
```

## Workflow / 工作流程

### 1. Receive Requirements / 接收需求

Extract the following from user requirements: / 从用户需求中提取以下信息：

| To Extract / 要提取的 | User Says / 用户说 | Example / 示例 |
|---------|--------|------|
| **File Path / 文件路径** | "test-files/xxx.xlsx" / "测试文件/xxx.xlsx" | Must be explicit / 必须明确 |
| **Operation Intent / 操作意图** | "dates to text" / "country codes to Chinese" / "renumber" / "日期转文本""国别改中文""序号重排" | One target column per intent / 每项一个目标列 |
| **Column Characteristics / 操作列特征** | Column name keywords / data type / position / 列名关键字 / 数据类型 / 位置 | Infer / 推断 |

### 2. Scan File / 扫描文件

```python
import os, sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from datetime import datetime
import pandas as pd

FILE = 'target.xlsx' / FILE = '目标文件.xlsx'
size_mb = os.path.getsize(FILE) / 1024 / 1024

# ====== A. Read headers (fast with read_only) / 读表头 ======
wb = load_workbook(FILE, read_only=True)
ws = wb.active

headers = {}
for cell in ws[1]:
    if cell.value:
        headers[cell.column] = str(cell.value).strip()

total_cols = len(headers)
print(f'File: {os.path.basename(FILE)} ({size_mb:.0f}MB) / 文件: {os.path.basename(FILE)} ({size_mb:.0f}MB)')
print(f'Columns: {total_cols} / 列数: {total_cols}')

# Print full header inventory / 打印完整表头清单
print(f'\n=== Header Inventory / 表头清单 ===')
for col_idx in sorted(headers.keys()):
    cl = get_column_letter(col_idx)
    print(f'  {cl}({col_idx}): {headers[col_idx]}')

wb.close()

# ====== B. data_only sample scan for date columns / data_only 采样扫描日期列 ======
wb2 = load_workbook(FILE, read_only=True, data_only=True)
ws2 = wb2.active

date_cols = {}
for row in ws2.iter_rows(min_row=2, max_row=min(500, ws2.max_row or 999999)):
    for cell in row:
        if isinstance(cell.value, datetime) and cell.column not in date_cols:
            date_cols[cell.column] = headers.get(cell.column, '?')

wb2.close()
if date_cols:
    print(f'\nFound {len(date_cols)} date columns / 发现 {len(date_cols)} 个日期列:')
    for c in sorted(date_cols):
        print(f'  {get_column_letter(c)}({c}): {date_cols[c]}')

# ====== C. pandas sample read (first N rows only) / pandas 采样读数据 ======
df_sample = pd.read_excel(FILE, nrows=5000)
print(f'\nTotal rows (sample cap): {len(df_sample)} / 总行数(采样上限): {len(df_sample)}')

# ====== D. Locate target columns per user requirements / 针对用户需求定位目标列 ======
# For each operation intent, match target columns and display current values
# 对每一项操作意图，匹配目标列并展示当前值

for intent in ['Dates→yyyymmdd / 日期→yyyymmdd', 'Country codes→Chinese / 国别代码→中文', 'Renumber / 序号重排']:
    # Match by keyword or data type / 按关键字或数据类型匹配
    # Show target column + current value samples / 展示目标列 + 当前值样本
    pass
```

### 3. Output Scout Report / 输出勘察报告

Format as follows / 格式如下：

```
═══════════════════════════════════════════════
Scout Report / 勘察报告: ultimate-merge.xlsx / 终极合并.xlsx
═══════════════════════════════════════════════

File: 195MB | 47 cols | ~330K rows / 文件: 195MB | 47列 | 约33万行

=== Header Inventory / 表头清单 ===
  A(1): Seq / 序号
  B(2): Title (Chinese) / 标题 (中文)
  C(3): Abstract (Chinese) / 摘要 (中文)
  ...all listed / 全部列出...

=== Date Columns (datetime type) / 日期列 (datetime 类型) ===
  G(7): Publication Date / 公开（公告）日
  J(10): Application Date / 申请日
  AB(28): Estimated Expiry / 预估到期日
  AD(30): Grant Date / 授权公告日
  AP(42): First Publication Date / 首次公开日
  (5 date columns total / 共5个日期列)

=== Located by Requirements / 按需求定位 ===

Req 1: "Dates in-place→yyyymmdd" / 需求1: "日期原地→yyyymmdd"
  Target cols: G(7), J(10), AB(28), AD(30), AP(42)
  Current type: datetime
  Samples: G→2026-04-24, J→2025-12-30, AB→2045-12-30

Req 2: "Country code→Chinese name" / 需求2: "公开国别代码→中文"
  Target col: M(13) Publication Country / 公开国别
  Current unique values: CN(majority/多数), JP(minority/少数)
  Mapping direction: CN→China/中国, JP→Japan/日本

Req 3: "Re-sequence 1→N" / 需求3: "序号重排1→N"
  Target col: A(1) Seq / 序号
  Current state: Multi-segment concatenation / 多段拼接
  Conclusion: Need continuous numbering from scratch / 需要从头连续编号

═══════════════════════════════════════════════
Is the above correct? Please confirm before execution.
以上是否正确？请确认后开始执行。
```

### 4. User Confirmation / 用户确认

After user confirms, pass the confirmed results to subsequent operation skills. / 用户确认后，将确认结果传递给后续操作技能。

## Notes / 注意事项

1. **Read-only / 只读**：Absolutely no file modification / 完全不修改文件
2. **Large file optimization / 大文件优化**：Headers via openpyxl read_only (seconds-level), data values via pandas nrows sampling (avoid full load) / 表头用 openpyxl read_only（秒级），数据值用 pandas nrows 采样（避免加载全量）
3. **Dual-read comparison / 双读对比**：data_only=True sees values, default mode sees formulas; difference = formula column / data_only=True 看值，默认模式看公式，两者不同说明是公式列
4. **Mid-row sampling / 中间行采样**：Besides header and rows 2-10, also check middle and last rows to detect multi-segment concatenation / 除了表头和第2-10行，还要看中间和末尾行，才能发现多段拼接等问题
5. **Output IS the report / 输出即报告**：No need for user to say "output report" — scout results are themselves in report format / 不需要用户说"输出报告"，勘察结果本身就是报告格式
