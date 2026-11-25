---
name: wps-financial-report
description: >
  财务三表生成。自动生成资产负债表、利润表、现金流量表的标准Excel格式，

  会计科目帮你列好，合计公式自动写好，还能算毛利率ROE等财务指标。

  用于帮助财务人员制作报表。当用户提到财务报表、资产负债表、利润表时触发。

  Financial statement generator with balance sheet, income statement, and
  ratios.
license: MIT
user-invocable: true
argument-hint: '[报表类型/财务数据]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 财务报表生成
  description_zh: 生成资产负债表、利润表、现金流量表的标准格式
  tags:
    - 财务报表
    - 资产负债表
    - 利润表
    - 会计
    - WPS
  version: 1.0.1
  license: MIT
---

# 财务报表生成器

财务数据 → 标准格式三表 → 自动勾稽校验 + 财务指标分析。

## When to Use

- 生成资产负债表/利润表/现金流量表
- 财务数据汇总和报表格式化
- 财务分析指标计算
- 用户说"做财务报表""资产负债表模板"

## When NOT to Use

- 预算编制 → 使用 `wps-budget`
- 工资核算 → 使用 `wps-salary`

## 财务三表

```text
[1] 资产负债表 → 资产=负债+所有者权益
[2] 利润表 → 收入-成本-费用=利润
[3] 现金流量表 → 经营+投资+筹资活动
```

## 工作流程

### Step 1: 确认报表需求

- 报表类型
- 报告期间（年度/季度/月度）
- 公司名称
- 数据来源

### Step 2: 生成报表

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side, numbers
from openpyxl.utils import get_column_letter
import os

def create_balance_sheet(company, period, data=None, output_path=None):
    """生成资产负债表"""
    wb = Workbook()
    ws = wb.active
    ws.title = "资产负债表"

    header_font = Font(name='宋体', size=12, bold=True)
    body_font = Font(name='宋体', size=10)
    money_fmt = '#,##0.00'
    thin = Side(style='thin')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # 标题
    ws.merge_cells('A1:F1')
    ws['A1'] = '资 产 负 债 表'
    ws['A1'].font = Font(name='黑体', size=16, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    ws.merge_cells('A2:F2')
    ws['A2'] = f'编制单位：{company}    {period}    单位：元'
    ws['A2'].font = Font(name='宋体', size=10)

    # 表头
    headers = [('资产', '行次', '期末余额', '负债和所有者权益', '行次', '期末余额')]
    for col, h in enumerate(headers[0], 1):
        cell = ws.cell(row=3, column=col, value=h)
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
        cell.border = border

    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 6
    ws.column_dimensions['C'].width = 16
    ws.column_dimensions['D'].width = 22
    ws.column_dimensions['E'].width = 6
    ws.column_dimensions['F'].width = 16

    # 资产科目
    assets = [
        ('流动资产：', '', '', '流动负债：', '', ''),
        ('  货币资金', '1', 0, '  短期借款', '31', 0),
        ('  应收账款', '2', 0, '  应付账款', '32', 0),
        ('  预付款项', '3', 0, '  预收款项', '33', 0),
        ('  存货', '4', 0, '  应付职工薪酬', '34', 0),
        ('  其他流动资产', '5', 0, '  应交税费', '35', 0),
        ('流动资产合计', '10', '=SUM(C5:C9)', '流动负债合计', '40', '=SUM(F5:F9)'),
        ('', '', '', '', '', ''),
        ('非流动资产：', '', '', '非流动负债：', '', ''),
        ('  固定资产', '11', 0, '  长期借款', '41', 0),
        ('  无形资产', '12', 0, '  长期应付款', '42', 0),
        ('非流动资产合计', '20', '=SUM(C14:C15)', '非流动负债合计', '50', '=SUM(F14:F15)'),
        ('', '', '', '负债合计', '51', '=F10+F16'),
        ('', '', '', '', '', ''),
        ('', '', '', '所有者权益：', '', ''),
        ('', '', '', '  实收资本', '52', 0),
        ('', '', '', '  资本公积', '53', 0),
        ('', '', '', '  盈余公积', '54', 0),
        ('', '', '', '  未分配利润', '55', 0),
        ('', '', '', '所有者权益合计', '60', '=SUM(F20:F23)'),
        ('资产总计', '30', '=C10+C16', '负债和所有者权益总计', '70', '=F17+F24'),
    ]

    for i, row_data in enumerate(assets):
        row = i + 4
        for col, val in enumerate(row_data, 1):
            cell = ws.cell(row=row, column=col, value=val)
            cell.font = body_font
            cell.border = border
            if col in [3, 6] and isinstance(val, (int, float)):
                cell.number_format = money_fmt

    if not output_path:
        output_path = f'{company}_资产负债表.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 财务分析指标

```text
盈利能力：
  毛利率 = (收入-成本)/收入 × 100%
  净利率 = 净利润/收入 × 100%
  ROE = 净利润/所有者权益 × 100%
  ROA = 净利润/总资产 × 100%

偿债能力：
  流动比率 = 流动资产/流动负债
  速动比率 = (流动资产-存货)/流动负债
  资产负债率 = 负债总额/资产总额 × 100%

运营能力：
  应收账款周转率 = 收入/平均应收账款
  存货周转率 = 成本/平均存货
  总资产周转率 = 收入/平均总资产
```

### Step 4: 交付

1. 生成标准格式财务报表Excel
2. 内置公式自动计算合计和勾稽
3. 可选：附加财务分析指标表

## 示例

```bash
# 资产负债表
/wps-financial-report 生成XX公司2025年度资产负债表模板

# 利润表
/wps-financial-report 做一份利润表，收入500万成本300万

# 财务分析
/wps-financial-report 根据这份财务数据计算财务指标
```
