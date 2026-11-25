---
name: wps-budget
description: |
  预算表一键生成。部门年度预算、项目预算、活动经费预算，选个模板填数字就行，
  小计合计公式自动写好，还有预算vs实际对比和执行率自动计算。
  用于帮助财务和行政制作预算表。当用户提到预算、费用表、经费时触发。
  Budget spreadsheet generator with formulas and variance analysis.
license: MIT
user-invocable: true
argument-hint: '[预算类型/需求描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 预算表生成
  description_zh: 生成部门预算、项目预算、活动经费表格，含预算公式和汇总
  tags:
    - 预算
    - 费用
    - 财务
    - Excel
    - WPS
  version: 1.0.1
  license: MIT
---

# 预算表/费用表生成器

选类型 → 填数据 → 自动公式 → 预算表搞定。

## When to Use

- 制作年度/季度/月度预算表
- 项目预算编制
- 活动经费预算
- 预算执行情况分析
- 用户说"帮我做预算表""编制费用预算"

## When NOT to Use

- 工资核算 → 使用 `wps-salary`
- 财务报表 → 使用 `wps-financial-report`

## 预算模板类型

```text
[1] 部门年度预算 → 人力/办公/差旅/培训等分项
[2] 项目预算 → 人工/材料/设备/外包/管理费
[3] 活动预算 → 场地/餐饮/物料/交通/宣传
[4] 家庭预算 → 收入/固定支出/可变支出/储蓄
[5] 营销预算 → 线上/线下/品牌/效果/公关
```

## 工作流程

### Step 1: 确认预算要素

- **预算类型**：部门/项目/活动
- **时间范围**：年度/季度/月度
- **预算分类**：需要哪些费用项
- **是否需要对比**：预算vs实际

### Step 2: 生成预算表

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side, numbers
from openpyxl.utils import get_column_letter
import os

def create_budget(budget_type, items, output_path=None):
    """生成预算表"""
    wb = Workbook()
    ws = wb.active
    ws.title = "预算表"

    # 样式
    header_fill = PatternFill('solid', fgColor='2C3E50')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    cat_fill = PatternFill('solid', fgColor='ECF0F1')
    cat_font = Font(name='微软雅黑', size=11, bold=True)
    body_font = Font(name='微软雅黑', size=10)
    money_fmt = '#,##0.00'
    pct_fmt = '0.0%'
    thin = Side(style='thin')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # 标题
    ws.merge_cells('A1:G1')
    ws['A1'] = f"{'部门' if budget_type=='dept' else '项目'}预算表"
    ws['A1'].font = Font(name='微软雅黑', size=16, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # 表头
    headers = ['序号', '费用类别', '费用项目', '预算金额',
               '实际金额', '差异', '执行率']
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        cell.border = border

    # 列宽
    widths = [6, 14, 20, 14, 14, 14, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # 填入数据
    row = 4
    seq = 1
    for category, sub_items in items.items():
        # 分类行
        ws.merge_cells(start_row=row, start_column=2,
                       end_row=row, end_column=3)
        ws.cell(row=row, column=1, value='').border = border
        cat_cell = ws.cell(row=row, column=2, value=category)
        cat_cell.font = cat_font
        cat_cell.fill = cat_fill
        cat_cell.border = border
        # 分类小计公式
        start = row + 1
        end = row + len(sub_items)
        for c in [4, 5]:
            cell = ws.cell(row=row, column=c)
            cell.value = f'=SUM({get_column_letter(c)}{start}:{get_column_letter(c)}{end})'
            cell.number_format = money_fmt
            cell.font = cat_font
            cell.fill = cat_fill
            cell.border = border
        # 差异和执行率
        ws.cell(row=row, column=6,
                value=f'=D{row}-E{row}').number_format = money_fmt
        ws.cell(row=row, column=6).fill = cat_fill
        ws.cell(row=row, column=6).border = border
        ws.cell(row=row, column=7,
                value=f'=IF(D{row}=0,"",E{row}/D{row})').number_format = pct_fmt
        ws.cell(row=row, column=7).fill = cat_fill
        ws.cell(row=row, column=7).border = border
        row += 1

        for item_name, amount in sub_items.items():
            ws.cell(row=row, column=1, value=seq).border = border
            ws.cell(row=row, column=1).font = body_font
            ws.cell(row=row, column=3, value=item_name).border = border
            ws.cell(row=row, column=3).font = body_font
            ws.cell(row=row, column=4, value=amount).border = border
            ws.cell(row=row, column=4).number_format = money_fmt
            ws.cell(row=row, column=5, value=0).border = border
            ws.cell(row=row, column=5).number_format = money_fmt
            ws.cell(row=row, column=6,
                    value=f'=D{row}-E{row}').number_format = money_fmt
            ws.cell(row=row, column=6).border = border
            ws.cell(row=row, column=7,
                    value=f'=IF(D{row}=0,"",E{row}/D{row})').number_format = pct_fmt
            ws.cell(row=row, column=7).border = border
            seq += 1
            row += 1

    # 合计行
    ws.merge_cells(start_row=row, start_column=1,
                   end_row=row, end_column=3)
    total_cell = ws.cell(row=row, column=1, value='合计')
    total_cell.font = Font(name='微软雅黑', size=12, bold=True)
    total_cell.alignment = Alignment(horizontal='center')
    total_cell.fill = PatternFill('solid', fgColor='3498DB')
    total_cell.font = Font(name='微软雅黑', size=12, bold=True, color='FFFFFF')

    for c in [4, 5, 6]:
        cell = ws.cell(row=row, column=c)
        cell.value = f'=SUMPRODUCT(({get_column_letter(c)}4:{get_column_letter(c)}{row-1})*(A4:A{row-1}<>""))'
        cell.number_format = money_fmt
        cell.font = Font(name='微软雅黑', bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor='3498DB')
        cell.border = border

    if not output_path:
        output_path = '预算表.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 内置费用分类参考

```text
部门年度预算常见项：
├─ 人力成本：工资、社保、奖金、培训
├─ 办公费用：房租、水电、物业、办公用品
├─ 差旅费用：交通、住宿、餐饮补贴
├─ 营销费用：广告、活动、礼品
├─ IT费用：软件、硬件、云服务
└─ 其他：招待费、杂费、预备金(5%)
```

### Step 4: 交付

1. 生成含公式的预算Excel文件
2. 预算vs实际列预留（填入实际数据自动算差异）
3. 执行率自动计算和条件格式标记

## 示例

```bash
# 部门预算
/wps-budget 帮我做技术部2026年年度预算表

# 项目预算
/wps-budget 新产品开发项目预算，包含人工、设备、测试费用

# 活动预算
/wps-budget 公司年会预算表，200人规模
```
