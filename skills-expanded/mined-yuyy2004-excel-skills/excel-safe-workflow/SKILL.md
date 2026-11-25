---
name: excel-safe-workflow
description: |
  Excel safe editing five-step method (Backup→Scout→Plan→Execute→Verify). When users need to do structural editing on existing Excel files (insert columns, delete columns, modify data, format conversion, etc.), use this skill to ensure safe operations and avoid data corruption. Suitable for large files (>10MB or >10K rows) and complex spreadsheets with formulas. Other Excel operation skills reference this skill as their base workflow.
  Excel 安全编辑五步法（备份→勘察→规划→执行→验证）。当用户需要对现有 Excel 文件进行插入列、删除列、修改数据、格式转换等结构性编辑时，使用此技能确保操作安全、避免数据损坏。适用于大文件（>10MB 或 >1万行）和包含公式的复杂表格。其他 Excel 操作技能引用此技能作为基础流程。
---

# Excel Safe Editing Five-Step Method / Excel 安全编辑五步法

## 概述

编辑现有 Excel 文件（尤其是大文件或包含公式的文件）时，跳过勘察直接操作极易出错——不知道单元格里存的是值还是公式、insert 操作后公式引用错乱、处理完才发现数据对应不上。

此技能定义五步标准流程，所有 Excel 结构性编辑任务均应遵循。

## 第零步：备份（操作前必做） / Step Zero: Backup (Mandatory)

> 任何写操作都有不可逆风险。备份是第一道防线。

```python
import shutil
from datetime import datetime

FILE = '目标文件.xlsx'
BAK = FILE.replace('.xlsx', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
shutil.copy2(FILE, BAK)
print(f'已备份: {os.path.basename(BAK)}')
```

**规则**：
- 操作前必备份，备份名含时间戳，同目录存放
- 操作成功后，同文件历史备份仅保留最新 3 份
- 操作失误后：立即删除损坏文件 → 从备份恢复 → 重试

## 第一步：勘察 / Step 1: Scout

**目标**：彻底了解文件结构，不遗漏任何关键信息。

### 1.1 文件体量

```python
import os
size_mb = os.path.getsize('file.xlsx') / 1024 / 1024
print(f'文件大小: {size_mb:.1f} MB')
```

- 估算加载时间：~1s/MB（openpyxl 全量模式）
- 设定合理 timeout：至少 `文件大小_MB × 2 + 60` 秒

### 1.2 结构扫描

```python
from openpyxl import load_workbook

# 全量模式获取准确行列数
wb = load_workbook('file.xlsx')
ws = wb.active
print(f'工作表: {ws.title}, 行: {ws.max_row}, 列: {ws.max_column}')

# 读取所有表头（可能有合并单元格/多行表头）
for row_idx in range(1, 4):  # 前3行，覆盖多行表头
    for col_idx in range(1, ws.max_column + 1):
        v = ws.cell(row=row_idx, column=col_idx).value
        if v is not None:
            print(f'  行{row_idx} 列{col_idx}: {repr(v)[:60]}')
```

### 1.3 数据类型双重扫描（关键！） / Dual Data Type Scan (Critical!)

**这是最常见的翻车点。** 必须同时用两种模式读取，对比确认是值还是公式：

```python
# 模式A：默认模式 → 读到公式字符串
wb_raw = load_workbook('file.xlsx', read_only=True)
ws_raw = wb_raw.active

# 模式B：data_only → 读到计算结果
wb_data = load_workbook('file.xlsx', read_only=True, data_only=True)
ws_data = wb_data.active

# 对比目标列的2-6行
for col in target_columns:
    for row in range(2, 7):
        v_raw = ws_raw.cell(row=row, column=col).value
        v_data = ws_data.cell(row=row, column=col).value
        match = type(v_raw) == type(v_data)
        print(f'  列{col}行{row}: raw={type(v_raw).__name__}={repr(v_raw)[:30]}')
        print(f'         data_only={type(v_data).__name__}={repr(v_data)[:30]} {"✓" if match else "⚠️公式!"}')
```

| 加载模式 | 读到的是 | 适用场景 |
|----------|---------|---------|
| 默认（不带 data_only） | 公式字符串（如 `=TEXT(A1,"yyyymmdd")`） | 需要修改公式本身 |
| `data_only=True` | 计算结果（数值/日期/字符串） | 读取数据做分析转换 |

### 1.4 数据样本

检查前 5 行 + 中间若干行 + 末尾 5 行，确认数据格式一致。

## 第二步：规划 / Step 2: Plan

勘察完成后，回答以下问题再动手：

1. **目标列**：列号、英文代码、中文名各是什么？
2. **数据类型**：值是 datetime？float？还是公式？如果用默认模式读，`int()` 会不会炸？
3. **公式列**：文件中有哪些列包含公式？insert/delete 会不会打乱引用？
4. **多列操作**：如果涉及多列插入/删除，从右到左处理避免索引错乱
5. **耗时估算**：加载 ~1s/MB，逐格写入 ~0.5ms/格

## 第三步：执行 / Step 3: Execute

### 3.1 加载

```python
wb = load_workbook('file.xlsx')  # 不带 data_only，才能保存
ws = wb.active
```

### 3.2 多列操作顺序

**从右到左（列号从大到小）**，避免前面插入导致后续列号偏移：

```python
target_cols = [6, 8, 25, 26, 36]  # 原始列号
for col in sorted(target_cols, reverse=True):
    ws.insert_cols(col)
    # ... 操作 ...
```

### 3.3 进度输出

大文件必须输出进度，否则用户不知道是否卡死：

```python
for row in range(start_row, total_rows + 1):
    # ... 单元格操作 ...
    if row % 50000 == 0:
        print(f'进度: {row}/{total_rows} ({row/total_rows*100:.1f}%)')
```

### 3.4 保存

```python
wb.save('file.xlsx')
```

### 3.5 清理 / Cleanup

```python
# 清理旧备份（保留最新3个）
import os, re
backup_dir = os.path.dirname(FILE)
base = os.path.basename(FILE).replace('.xlsx', '')
backups = sorted([
    f for f in os.listdir(backup_dir)
    if f.startswith(base + '_backup_') and f.endswith('.xlsx')
], reverse=True)
for old_bak in backups[3:]:
    os.remove(os.path.join(backup_dir, old_bak))

# 清理临时解压目录
import shutil
for tmp_dir in [d for d in os.listdir(backup_dir) if d.endswith('_tmp') or d.endswith('_proc')]:
    full = os.path.join(backup_dir, tmp_dir)
    if os.path.isdir(full):
        shutil.rmtree(full)
```

### 3.6 失误恢复 / Failure Recovery

```python
# 如果操作失败，删损坏文件 + 从备份恢复
try:
    # ... 执行操作 ...
except Exception as e:
    print(f'❌ 操作失败: {e}')
    if os.path.exists(FILE):
        os.remove(FILE)           # 删除损坏产物
    shutil.copy2(BAK, FILE)       # 从备份恢复
    print(f'已从备份恢复')
    raise
```

## 第四步：验证 / Step 4: Verify

### 4.1 表头验证

确认新插入/修改的列头正确，相邻列未受影响。

### 4.2 数据抽样

必须覆盖：**前 5 行 + 中间 2 处 + 末 2 行**。

```python
wb = load_workbook('file.xlsx', read_only=True, data_only=True)
ws = wb.active
check_rows = [2, 3, 4, 5, 6, ws.max_row // 2, ws.max_row // 2 + 100, ws.max_row - 1, ws.max_row]
for row in check_rows:
    # 验证目标列数据
    ...
```

### 4.3 验证清单 / Verification Checklist

- [ ] 新列/修改列的位置正确
- [ ] 数据格式正确（如 yyyymmdd 文本）
- [ ] 相邻列未被意外修改
- [ ] 公式列引用未错乱（如果有公式）
- [ ] 无遗漏行（空值行确认是源数据为空而非写入遗漏）
- [ ] 备份文件已保留（操作成功则保留最新 3 份）
- [ ] 损坏/临时文件已清理

## 常见踩坑经验 / Common Pitfalls

| 坑 | 原因 | 预防 |
|----|------|------|
| 把公式当值读 | 没用 data_only 双重扫描 | 勘察阶段必须双读 |
| insert_cols 后列号全乱 | 从左到右操作 | 从右到左 |
| 循环引用 | insert 后公式中的列引用未自动更新 | 勘察时标记所有公式列 |
| 大文件加载超时 | 没预估文件大小 | 先 getsize，设足 timeout |
| 不小心覆盖原文件 | 没备份 | **第零步必须备份** |
| 损坏文件残留 | 操作失败后没删损坏产物 | **失误即删 + 从备份恢复** |
| 临时文件堆积 | 解压目录/tmp 没清理 | **finally 块必须 rmtree** |
| 备份文件过多 | 每次都留备份不清理 | **保留最新 3 份，其余自动删** |

## 供其他技能引用

其他 Excel 操作技能在 SKILL.md 开头声明：

```markdown
> 本技能遵循 [[excel-safe-workflow]] 四步法。执行前必须完成勘察→规划，执行后必须验证。
```

然后直接引用此技能中的代码模板，不需要重复描述四步法细节。
