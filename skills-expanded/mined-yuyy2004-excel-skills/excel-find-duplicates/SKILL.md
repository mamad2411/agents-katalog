---
name: excel-find-duplicates
description: |
  Read-only scan of Excel files to find duplicate rows by specified column(s), outputting duplicate row number lists. Does not modify the original file. Typically used in conjunction with excel-delete for safe, format-preserving deduplication.
  只读扫描 Excel 文件，按指定列查找重复行，输出重复行号列表。不修改原文件。通常配合 excel-delete 使用实现安全的格式无损去重。
  Trigger keywords: "find duplicates" "check duplicates" "scan duplicates" "duplicate rows" "what are the duplicates"
  触发词包括"查重""找重复""检查重复""重复行""有哪些重复"。
---

> This skill is read-only, no side effects. Follows [[excel-safe-workflow]] Scout→Analyze two-step approach.
> 本技能只读不写，安全无副作用。遵循 [[excel-safe-workflow]] 勘察→分析两步。

# Excel Find Duplicates (Read-only) / Excel 查重（只读）

## Function / 功能

1. Scan for duplicate rows by specified column(s) (or multi-column combination) / 按指定列（或多列联合）扫描重复行
2. Output duplicate statistics and row number list / 输出重复统计和行号列表
3. Results can be directly passed to [[excel-delete]] for deletion / 结果可直接传给 [[excel-delete]] 执行删除

## Step 0: Requirement Parsing / 第零步：需求解析

| Element / 要素 | Common Phrasing / 常见表述 | Default / 默认值 |
|------|---------|--------|
| **Key Column(s) / 关键列** | "By patent number" / "Column E" / "按专利号查""E列" | Must be explicit / 必须明确 |
| **Keep Strategy / 保留策略** | "Keep first" / "Keep latest" / "保留第一个""保留最新的" | Keep first occurrence / 保留首次出现 |
| **Output Format / 输出格式** | Directly return row number list / 直接返回行号列表 | Excel row numbers / Excel 行号 |

## Step 1: Scout (Read-only Scan) / 第一步：勘察（只读扫描）

```python
import pandas as pd

FILE = 'target.xlsx' / FILE = '目标文件.xlsx'
KEY_COL = 'Column Name / 列名'      # Key column name / 关键列名
KEEP = 'first'        # 'first'=keep first occurrence / 保留首次 / 'last'=keep last / 保留末次

# pandas efficient read (C engine, seconds-level) / pandas 高效读取（C引擎，秒级）
df = pd.read_excel(FILE)

total = len(df)
mask = df[KEY_COL].duplicated(keep=KEEP)
dup_indices = df.index[mask].tolist()
dup_excel_rows = [i + 2 for i in dup_indices]  # +2: pandas 0-index → Excel row number (row 1=header) / pandas 0-index → Excel行号（第1行=表头）

print(f'Total rows: {total} / 总行数: {total}')
print(f'Unique values: {total - len(dup_excel_rows)} / 唯一值: {total - len(dup_excel_rows)}')
print(f'Duplicate rows: {len(dup_excel_rows)} ({len(dup_excel_rows)/total*100:.1f}%) / 重复行: {len(dup_excel_rows)}')
print(f'Row range: {min(dup_excel_rows)} ~ {max(dup_excel_rows)}' if dup_excel_rows else 'No duplicates / 无重复')
```

### Multi-Column Joint Dedup / 多列联合查重

```python
KEY_COLS = ['Col1 / 列名1', 'Col2 / 列名2']  # Multi-column joint / 多列联合
mask = df.duplicated(subset=KEY_COLS, keep=KEEP)
```

## Step 2: Output Results / 第二步：输出结果

```python
if not dup_excel_rows:
    print('✅ No duplicates / 无重复数据')
else:
    print(f'\nDuplicate row number list (total {len(dup_excel_rows)} rows) / 重复行号列表（共{len(dup_excel_rows)}行）:')
    print(dup_excel_rows[:20])  # First 20 / 前20个
    if len(dup_excel_rows) > 20:
        print(f'... and {len(dup_excel_rows)-20} more rows / 还有{len(dup_excel_rows)-20}行')

    # Pass to excel-delete for use / 传递给 excel-delete 使用
    # Format: [row number list], sort descending then delete_rows one by one / 格式: [行号列表], 从大到小排序后逐个 delete_rows
```

## Working with excel-delete / 与 excel-delete 配合

Find-duplicates output directly feeds into delete input: / 查重输出直接作为删除输入：

```
excel-find-duplicates → [2, 5, 8, 3, 12, ...] → excel-delete delete bottom-to-top / 从下到上删除
```

Delete-side code / 删除侧代码：

```python
# Receive find-duplicates results / 接收查重结果
dup_rows = [2, 5, 8, 3, 12, ...]  # From excel-find-duplicates / 来自 excel-find-duplicates

# Delete bottom-to-top (critical! avoids row number shifting) / 从下到上删除（关键！避免行号偏移）
for row in sorted(dup_rows, reverse=True):
    ws.delete_rows(row)
```

## Notes / 注意事项

1. **Read-only / 只读**：Does not modify original file, safe to run / 不修改原文件，放心跑
2. **Row numbers are Excel row numbers / 行号是 Excel 行号**：Row 1 = header, Row 2 = first data row / 第1行=表头，第2行=第一条数据
3. **Large files / 大文件**：pandas reading 168MB/330K rows takes ~150s / pandas 读取 168MB/33万行约 150s
4. **Null values / 空值**：Multiple rows with None in the key column are treated as "duplicates", only the first is kept / 关键列为 None 的多个行会被视为"重复"，只保留第一个
