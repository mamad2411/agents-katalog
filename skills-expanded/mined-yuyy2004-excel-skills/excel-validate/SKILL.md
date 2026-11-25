---
name: excel-validate
description: |
  Read-only scan of Excel files to check data quality — null rate, outliers, format consistency, duplicate values, etc. Outputs a quality issue report without modifying the original file.
  只读扫描 Excel 文件，检查数据质量——空值率、异常值、格式一致性、重复值等。输出质量问题报告，不修改原文件。
  Trigger keywords: "check data" "validate" "null values" "data quality" "any issues" "scan" "quality report"
  触发词包括"检查数据""校验""空值""数据质量""有没有问题""扫描""质量报告"。
---

> This skill is **read-only, no side effects**. Uses pandas for fast scanning, outputs an issue report.
> 本技能**只读不写**，安全无副作用。用 pandas 快速扫描，输出问题报告。

# Excel Data Validation / Excel 数据校验

## Check Items / 检查项目

| Check Item / 检查项 | What It Detects / 检测内容 | Severity / 严重程度 |
|------|------|:--:|
| Null Rate / 空值率 | NaN/None ratio per column / 每列 NaN/None 占比 | High >30%, Medium >10% / 高 >30%, 中 >10% |
| Uniqueness / 唯一值 | Unique value count per column (identifies all-same columns, ID columns) / 每列唯一值数量 | Info / 信息 |
| Type Consistency / 类型一致性 | Mixed number+text within same column / 同列混用数字+文本 | Medium / 中 |
| Outliers / 异常值 | Extreme values in numeric columns / 数值列的超大/超小值 | Low / 低 |
| Duplicate Rows / 重复行 | Count of fully duplicate rows / 完全重复的行数 | High / 高 |
| Formula Columns / 公式列 | Which columns are formula-calculated / 哪些列是公式计算 | Info / 信息 |

## Step 0: Requirement Parsing / 第零步：需求解析

| User Says / 用户说 | Check Scope / 检查范围 |
|--------|------|
| "Check data quality" / "检查数据质量" | All check items / 全部检查项 |
| "See which columns have nulls" / "看看哪些列有空值" | Null rate only / 只看空值率 |
| "Check for duplicates" / "检查有没有重复" | Duplicate rows only / 只看重复行 |
| "Any issues with this data?" / "这数据有没有问题" | All check items / 全部检查项 |

## Step 1: Scout + Check / 第一步：勘察+检查

```python
import pandas as pd
import numpy as np
import os

FILE = 'target.xlsx' / FILE = '目标文件.xlsx'
size_mb = os.path.getsize(FILE) / 1024 / 1024

df = pd.read_excel(FILE)
total = len(df)
cols = len(df.columns)

print(f'{"="*60}')
print(f'Data Quality Report / 数据质量报告: {os.path.basename(FILE)}')
print(f'File Size: {size_mb:.1f}MB | Rows: {total} | Cols: {cols} / 文件大小: {size_mb:.1f}MB | 行数: {total} | 列数: {cols}')
print(f'{"="*60}')

# ====== 1. Null Check / 空值检查 ======
print(f'\n【Null Rate / 空值率】')
null_report = []
for col in df.columns:
    null_count = df[col].isna().sum()
    null_pct = null_count / total * 100
    if null_pct > 0:
        level = '🔴' if null_pct > 30 else ('🟡' if null_pct > 10 else '🟢')
        null_report.append((col, null_count, null_pct, level))

null_report.sort(key=lambda x: -x[2])
if null_report:
    for col, cnt, pct, level in null_report[:20]:
        print(f'  {level} {col}: {cnt} nulls / 空 ({pct:.1f}%)')
    if len(null_report) > 20:
        print(f'  ... {len(null_report)-20} more columns with nulls / 还有 {len(null_report)-20} 列有空值')
else:
    print(f'  ✅ No nulls / 无空值')

# ====== 2. Uniqueness / 唯一值 ======
print(f'\n【Uniqueness Analysis / 唯一值分析】')
for col in df.columns:
    n_unique = df[col].nunique()
    if n_unique <= 1:
        print(f'  ⚠️ {col}: unique={n_unique} (all same or no data / 全列相同或无数据)')
    elif n_unique == total:
        print(f'  📌 {col}: unique={n_unique} (likely ID column / 可能是ID列)')

# ====== 3. Type Consistency / 类型一致性 ======
print(f'\n【Type Consistency / 类型一致性】')
mixed_cols = []
for col in df.columns:
    types = df[col].dropna().apply(type).unique()
    if len(types) > 1:
        type_names = [t.__name__ for t in types]
        mixed_cols.append((col, type_names))
if mixed_cols:
    for col, types in mixed_cols[:10]:
        print(f'  ⚠️ {col}: mixed types / 混合类型 {types}')
else:
    print(f'  ✅ Types consistent / 类型一致')

# ====== 4. Outliers (numeric columns) / 异常值（数值列）======
print(f'\n【Numeric Outliers / 数值列异常值】')
num_cols = df.select_dtypes(include=[np.number]).columns
found_anomaly = False
for col in num_cols:
    vals = df[col].dropna()
    if len(vals) < 2: continue
    q1, q3 = vals.quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr == 0: continue
    outliers = vals[(vals < q1 - 3*iqr) | (vals > q3 + 3*iqr)]
    if len(outliers) > 0:
        print(f'  📊 {col}: {len(outliers)} extreme values / 个极端值 (min={vals.min()}, max={vals.max()})')
        found_anomaly = True
if not found_anomaly:
    print(f'  ✅ No obvious outliers / 未发现明显异常值')

# ====== 5. Fully Duplicate Rows / 完全重复行 ======
print(f'\n【Duplicate Rows / 重复行】')
dup_rows = df.duplicated().sum()
if dup_rows > 0:
    print(f'  🔴 {dup_rows} rows fully duplicate / 行完全重复 ({dup_rows/total*100:.1f}%)')
else:
    print(f'  ✅ No fully duplicate rows / 无完全重复行')

# ====== 6. Potential Issues / 可能的问题 ======
print(f'\n【Potential Issues / 可能的问题】')

# Check for obviously formula-result columns (e.g. "Unnamed") / 检查是否包含明显是公式结果的列
unnamed = [c for c in df.columns if 'Unnamed' in str(c)]
if unnamed:
    print(f'  ⚠️ {len(unnamed)} unnamed columns / 个未命名列 -> possible hidden header issues / 可能有隐藏的表头问题')

# Check all-null columns / 检查全空列
all_null = [c for c in df.columns if df[c].isna().all()]
if all_null:
    print(f'  🔴 {len(all_null)} all-null columns / 个全空列: {all_null}')

# Check columns that look like dates but are stored as text / 检查看起来像日期但是字符串的列
for col in df.select_dtypes(include=['object']).columns:
    sample = df[col].dropna().head(5)
    date_like = sample.astype(str).str.match(r'\d{4}[-/]\d{2}[-/]\d{2}').sum()
    if date_like >= 3:
        print(f'  💡 {col}: looks like date but stored as text / 看起来像日期但存储为文本, suggest using excel-date-to-text / 建议用 excel-date-to-text 处理')

print(f'\n{"="*60}')
print(f'Check complete / 检查完成')
```

## Step 2: Output / 第二步：输出

Only output the report, do not modify the file. If issues are found, inform the user of severity and suggested handling. / 只输出报告，不修改文件。如果发现问题，告知用户严重程度和建议的处理方式。

## Large File Optimization / 大文件优化

For large files (>10MB), `pd.read_excel()` is sufficient — pandas C engine reads at ~1s/MB. / 大文件（>10MB）用 `pd.read_excel()` 即可，pandas C 引擎读取速度约 1s/MB。

## Notes / 注意事项

1. **Read-only, no writes / 只读不写**：Absolutely no modification to original file / 完全不修改原文件
2. **Encoding / 编码**：On Windows, outputting Chinese may require `sys.stdout.reconfigure(encoding='utf-8')` / Windows 下输出中文可能需要
3. **Large file memory / 大文件内存**：330K rows × 48 cols ≈ 150MB memory, sufficient / 33 万行 × 48 列 ≈ 150MB 内存，够用
