---
name: wps-data-viz
description: |
  数据看板一键生成。不用Power BI，在Excel里就能做出专业的数据仪表盘，
  KPI大数字卡片+趋势折线图+占比饼图+排名柱状图，一页展示所有关键数据。
  用于帮助用户制作数据仪表盘。当用户提到仪表盘、dashboard、数据看板时触发。
  Data dashboard generator in Excel with KPI cards and multiple charts.
license: MIT
user-invocable: true
argument-hint: '[数据/KPI描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 数据看板生成
  description_zh: 在Excel中生成数据仪表盘，包含KPI卡片、趋势图、占比图
  tags:
    - 仪表盘
    - 数据可视化
    - dashboard
    - 图表
    - WPS
  version: 1.0.1
  license: MIT
---

# 数据可视化仪表盘

数据 → KPI卡片 + 趋势图 + 占比图 → 一页式数据概览。

> 不用Power BI，Excel也能做出专业仪表盘。

## When to Use

- 制作数据概览/仪表盘
- 月度/季度数据一页展示
- KPI指标可视化
- 用户说"做个数据仪表盘""数据大屏"

## When NOT to Use

- 单个图表 → 使用 `wps-chart`
- 数据透视分析 → 使用 `wps-pivot`

## 仪表盘布局

```text
┌─────────┬─────────┬─────────┬─────────┐
│  KPI 1  │  KPI 2  │  KPI 3  │  KPI 4  │
│ 总收入  │ 订单数  │ 客单价  │ 转化率  │
│ ¥125万  │ 3,456  │ ¥362   │ 4.2%   │
│ ↑12.5%  │ ↑8.3%  │ ↓2.1%  │ ↑0.5%  │
├─────────┴─────────┼─────────┴─────────┤
│                    │                    │
│  收入趋势折线图    │  品类占比饼图      │
│  (12个月)          │                    │
│                    │                    │
├────────────────────┼────────────────────┤
│                    │                    │
│  TOP10产品柱状图   │  地区分布表格      │
│                    │                    │
└────────────────────┴────────────────────┘
```

## 工作流程

### Step 1: 确认仪表盘要素

- **KPI指标**：需要展示哪些关键数字
- **趋势图**：哪些数据看趋势
- **占比图**：哪些数据看构成
- **排名表**：哪些数据看排名
- **数据源**：数据在哪里

### Step 2: 生成仪表盘

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import os

def create_dashboard(kpis, charts_data, output_path=None):
    """
    kpis = [
        {'name': '总收入', 'value': '¥125万', 'change': '+12.5%', 'trend': 'up'},
        {'name': '订单数', 'value': '3,456', 'change': '+8.3%', 'trend': 'up'},
    ]
    charts_data = {
        'trend': {'labels': [...], 'values': [...]},
        'pie': {'labels': [...], 'values': [...]},
        'bar': {'labels': [...], 'values': [...]},
    }
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "数据仪表盘"
    ws.sheet_properties.tabColor = '2C3E50'

    # 隐藏网格线
    ws.sheet_view.showGridLines = False

    # KPI卡片
    kpi_colors = ['3498DB', '2ECC71', 'E74C3C', 'F39C12']
    for i, kpi in enumerate(kpis[:4]):
        col_start = i * 4 + 1
        ws.merge_cells(start_row=2, start_column=col_start,
                       end_row=2, end_column=col_start + 3)
        ws.merge_cells(start_row=3, start_column=col_start,
                       end_row=3, end_column=col_start + 3)
        ws.merge_cells(start_row=4, start_column=col_start,
                       end_row=4, end_column=col_start + 3)

        color = kpi_colors[i % len(kpi_colors)]
        fill = PatternFill('solid', fgColor=color)

        # 指标名
        cell = ws.cell(row=2, column=col_start, value=kpi['name'])
        cell.font = Font(name='微软雅黑', size=11, color='FFFFFF')
        cell.fill = fill
        cell.alignment = Alignment(horizontal='center')

        # 指标值
        cell = ws.cell(row=3, column=col_start, value=kpi['value'])
        cell.font = Font(name='微软雅黑', size=22, bold=True, color='FFFFFF')
        cell.fill = fill
        cell.alignment = Alignment(horizontal='center')

        # 变化
        arrow = '↑' if kpi.get('trend') == 'up' else '↓'
        cell = ws.cell(row=4, column=col_start,
                       value=f'{arrow} {kpi["change"]}')
        cell.font = Font(name='微软雅黑', size=10, color='FFFFFF')
        cell.fill = fill
        cell.alignment = Alignment(horizontal='center')

    # 数据区域（隐藏，供图表引用）
    data_start_row = 30
    if 'trend' in charts_data:
        td = charts_data['trend']
        for i, label in enumerate(td['labels']):
            ws.cell(row=data_start_row + i, column=1, value=label)
            ws.cell(row=data_start_row + i, column=2, value=td['values'][i])

        chart = LineChart()
        chart.title = "趋势"
        chart.width = 20
        chart.height = 12
        chart.style = 10
        data = Reference(ws, min_col=2, min_row=data_start_row,
                        max_row=data_start_row + len(td['labels']) - 1)
        cats = Reference(ws, min_col=1, min_row=data_start_row,
                        max_row=data_start_row + len(td['labels']) - 1)
        chart.add_data(data)
        chart.set_categories(cats)
        ws.add_chart(chart, 'A6')

    if 'pie' in charts_data:
        pd = charts_data['pie']
        for i, label in enumerate(pd['labels']):
            ws.cell(row=data_start_row + i, column=4, value=label)
            ws.cell(row=data_start_row + i, column=5, value=pd['values'][i])

        chart = PieChart()
        chart.title = "占比"
        chart.width = 14
        chart.height = 12
        data = Reference(ws, min_col=5, min_row=data_start_row,
                        max_row=data_start_row + len(pd['labels']) - 1)
        cats = Reference(ws, min_col=4, min_row=data_start_row,
                        max_row=data_start_row + len(pd['labels']) - 1)
        chart.add_data(data)
        chart.set_categories(cats)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showPercent = True
        ws.add_chart(chart, 'I6')

    if not output_path:
        output_path = '数据仪表盘.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成仪表盘Excel（一页展示）
2. KPI卡片 + 多图表组合
3. 说明如何更新数据（修改数据区域自动刷新图表）

## 示例

```bash
# 销售仪表盘
/wps-data-viz 做一个销售数据仪表盘，KPI包括收入、订单、客单价、转化率

# 从数据生成
/wps-data-viz 用sales_2025.xlsx做一个年度数据概览仪表盘

# 运营仪表盘
/wps-data-viz 做个运营数据看板：DAU、MAU、留存率、付费率
```
