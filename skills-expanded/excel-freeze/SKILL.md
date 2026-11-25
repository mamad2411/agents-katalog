---
name: excel-freeze
description: |
  Freeze or unfreeze Excel worksheet panes. Supports freeze top row, freeze first column, freeze top row + first column, freeze at specified position.
  冻结或取消冻结 Excel 工作表窗格，支持冻结首行、冻结首列、冻结首行+首列、冻结指定位置。
  Trigger keywords: "freeze" "freeze header" "lock top row" "freeze first column" "unfreeze"
  触发词包括"冻结""固定表头""锁定首行""首列不动""取消冻结""冻住"。
---

> This skill follows [[excel-safe-workflow]] four-step method (lightweight: Scout→Execute→Verify).
> 本技能遵循 [[excel-safe-workflow]] 四步法（轻量版：勘察→执行→验证）。

# Excel Freeze Panes / Excel 冻结窗格

## 功能

冻结后，被冻结的行/列在滚动时始终可见。纯 Excel 视图效果，不影响数据。

## 第零步：需求解析

| 用户说 | 冻结位置 | freeze_panes 值 |
|--------|---------|:--:|
| "冻结首行""表头不动""标题行固定" | 仅首行 | `A2` |
| "冻结首列""第一列不动""序号锁定" | 仅首列 | `B1` |
| "冻结首行和首列""表头和序号都不动" | 首行+首列 | `B2` |
| "冻结前3行" | 指定行 | `A4` |
| "取消冻结""解冻""不冻了" | 取消 | `None` |

## 第一步：勘察

```python
from openpyxl import load_workbook

wb = load_workbook('目标文件.xlsx')
ws = wb.active
current = ws.freeze_panes
print(f'当前冻结: {current if current else "无"}')
print(f'工作表: {ws.max_row}行 x {ws.max_column}列')

# 展示表头供确认
for col_idx in range(1, min(6, ws.max_column + 1)):
    h = ws.cell(row=1, column=col_idx).value
    print(f'  表头列{col_idx}: {h}')
```

## 第二步：执行

```python
from openpyxl import load_workbook

# ===== 用户配置 =====
FREEZE = 'A2'  # None=取消 / 'A2'=首行 / 'B1'=首列 / 'B2'=首行+首列 / 'A4'=前三行
# ====================

wb = load_workbook('目标文件.xlsx')
ws = wb.active
ws.freeze_panes = FREEZE
wb.save('目标文件.xlsx')

desc = {
    None: '已取消冻结',
    'A2': '已冻结首行',
    'B1': '已冻结首列',
    'B2': '已冻结首行+首列',
}
print(desc.get(FREEZE, f'已冻结: {FREEZE}'))
```

## 第三步：验证

```python
wb = load_workbook('目标文件.xlsx', read_only=True)
ws = wb.active
print(f'冻结状态: {ws.freeze_panes}')
wb.close()
```

## 注意事项

- **仅影响活动工作表**：如有多个 sheet，需逐个设置
- **合并单元格**：冻结线穿过合并单元格时，合并会被拆分
- **Excel 打开才可见**：openpyxl 只是写入属性，效果需在 Excel 中查看
- **操作前必备份**：遵循 [[excel-safe-workflow]] 第零步——操作前自动备份（时间戳命名）
