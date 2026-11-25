---
name: wps-pivot
description: |
  透视表傻瓜教程。透视表看不懂？不知道字段往哪拖？用最通俗的话教你：
  透视表就是"按X分组，算Y的汇总"。帮你选对字段，生成透视结果。
  用于帮助用户理解和创建透视表。当用户提到透视表、数据汇总、分组统计时触发。
  Pivot table guide - explains concepts in plain language and generates results.
license: MIT
user-invocable: true
argument-hint: '[数据描述/分析需求]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 透视表教程
  description_zh: 讲解透视表的用法，帮你理解字段拖放和数据汇总
  tags:
    - 透视表
    - 数据分析
    - 汇总
    - Excel
    - WPS
  version: 1.0.1
  license: MIT
---

# 数据透视表助手

用人话解释透视表 → 帮你拖对字段 → 生成结果。

> "透视表就是：按X分组，算Y的汇总。" 就这么简单。

## When to Use

- 需要按分类汇总数据
- 不知道透视表怎么用
- 需要交叉分析（如：各部门各月销售额）
- 用户说"帮我做透视表""按XX汇总"

## When NOT to Use

- 简单求和/计数 → 使用 `wps-formula`
- 图表可视化 → 使用 `wps-chart`

## 透视表一句话理解

```text
透视表 = 按【行标签】分组，计算【值字段】的【汇总方式】

例子：
  "按部门统计人数"
  → 行标签=部门，值=姓名，汇总=计数

  "各月份各产品的销售额合计"
  → 行标签=月份，列标签=产品，值=销售额，汇总=求和

  "每个销售员的平均单价"
  → 行标签=销售员，值=单价，汇总=平均值
```

## 字段拖放指南

```text
┌─────────────────────────────────────┐
│  你的数据有哪些列？                  │
│                                     │
│  分类列（文本）→ 拖到【行】或【列】  │
│    如：部门、月份、产品、地区        │
│                                     │
│  数值列（数字）→ 拖到【值】          │
│    如：金额、数量、分数              │
│                                     │
│  筛选列（可选）→ 拖到【筛选】        │
│    如：年份、状态                    │
└─────────────────────────────────────┘

常见搭配：
┌──────────────┬──────┬──────┬────────┐
│ 需求         │ 行   │ 列   │ 值     │
├──────────────┼──────┼──────┼────────┤
│ 各部门人数   │ 部门 │ -    │ 计数   │
│ 月度销售趋势 │ 月份 │ -    │ 求和   │
│ 部门×月份    │ 部门 │ 月份 │ 求和   │
│ 产品占比     │ 产品 │ -    │ 求和%  │
└──────────────┴──────┴──────┴────────┘
```

## 工作流程

### Step 1: 理解数据和需求

确认：
- 数据有哪些列
- 想按什么分组
- 想看什么数值（合计/平均/计数）
- 是否需要交叉分析

### Step 2: 用openpyxl生成透视结果

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from collections import defaultdict
import os

def create_pivot(data_path, row_field, value_field,
                 agg='sum', col_field=None, output_path=None):
    """生成透视表结果"""
    wb = load_workbook(data_path)
    ws = wb.active

    # 读取数据
    headers = [cell.value for cell in ws[1]]
    row_idx = headers.index(row_field)
    val_idx = headers.index(value_field)
    col_idx = headers.index(col_field) if col_field else None

    # 聚合
    if col_field:
        pivot = defaultdict(lambda: defaultdict(list))
        col_values = set()
        for row in ws.iter_rows(min_row=2, values_only=True):
            r_key = row[row_idx]
            c_key = row[col_idx]
            val = float(row[val_idx] or 0)
            pivot[r_key][c_key].append(val)
            col_values.add(c_key)
        col_values = sorted(col_values)
    else:
        pivot = defaultdict(list)
        for row in ws.iter_rows(min_row=2, values_only=True):
            r_key = row[row_idx]
            val = float(row[val_idx] or 0)
            pivot[r_key].append(val)

    # 聚合函数
    agg_funcs = {
        'sum': sum,
        'avg': lambda x: sum(x)/len(x) if x else 0,
        'count': len,
        'max': max,
        'min': min,
    }
    func = agg_funcs.get(agg, sum)

    # 写入结果
    wb_out = Workbook()
    ws_out = wb_out.active
    ws_out.title = "透视结果"

    header_fill = PatternFill('solid', fgColor='2C3E50')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')

    if col_field:
        # 交叉透视
        ws_out.cell(row=1, column=1, value=row_field).font = header_font
        ws_out.cell(row=1, column=1).fill = header_fill
        for ci, cv in enumerate(col_values, 2):
            ws_out.cell(row=1, column=ci, value=cv).font = header_font
            ws_out.cell(row=1, column=ci).fill = header_fill
        ws_out.cell(row=1, column=len(col_values)+2, value='合计').font = header_font
        ws_out.cell(row=1, column=len(col_values)+2).fill = header_fill

        for ri, (rk, cols) in enumerate(sorted(pivot.items()), 2):
            ws_out.cell(row=ri, column=1, value=rk)
            row_total = 0
            for ci, cv in enumerate(col_values, 2):
                val = func(cols.get(cv, [0]))
                ws_out.cell(row=ri, column=ci, value=round(val, 2))
                row_total += val
            ws_out.cell(row=ri, column=len(col_values)+2, value=round(row_total, 2))
    else:
        ws_out.cell(row=1, column=1, value=row_field).font = header_font
        ws_out.cell(row=1, column=1).fill = header_fill
        ws_out.cell(row=1, column=2, value=f'{value_field}({agg})').font = header_font
        ws_out.cell(row=1, column=2).fill = header_fill

        for ri, (rk, vals) in enumerate(sorted(pivot.items()), 2):
            ws_out.cell(row=ri, column=1, value=rk)
            ws_out.cell(row=ri, column=2, value=round(func(vals), 2))

    if not output_path:
        output_path = '透视结果.xlsx'
    wb_out.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 在WPS中创建透视表的步骤指引

```text
WPS中创建透视表（手动操作指引）：
1. 选中数据区域（含表头）
2. 菜单 → 插入 → 数据透视表
3. 选择放置位置（新工作表）
4. 在右侧面板拖放字段：
   - 行区域：拖入分类字段
   - 列区域：拖入交叉字段（可选）
   - 值区域：拖入数值字段
   - 筛选区域：拖入筛选字段（可选）
5. 点击值字段 → 值字段设置 → 选择汇总方式
```

### Step 4: 交付

1. 生成透视结果Excel
2. 或提供WPS内操作步骤指引
3. 说明如何修改汇总方式和筛选

## 示例

```bash
# 简单透视
/wps-pivot 按部门统计销售额合计，数据在sales.xlsx

# 交叉透视
/wps-pivot 各部门每个月的销售额是多少

# 不懂透视表
/wps-pivot 透视表是什么？我的数据有姓名、部门、月份、销售额，想看各部门汇总
```
