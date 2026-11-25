---
name: wps-chart
description: |
  数据图表一键生成。不知道数据该用什么图表？告诉我你的数据和目的，
  自动推荐最佳图表类型并生成，柱状图折线图饼图散点图都支持，还帮你调配色。
  用于帮助用户制作数据可视化图表。当用户提到图表、柱状图、折线图、饼图时触发。
  Chart generator - recommends best chart type and creates professional charts.
license: MIT
user-invocable: true
argument-hint: '[数据描述/图表需求]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 数据图表生成
  description_zh: 根据数据生成柱状图、折线图、饼图等常用图表
  tags:
    - 图表
    - 可视化
    - 柱状图
    - 折线图
    - WPS
  version: 1.0.1
  license: MIT
---

# WPS图表生成与美化

数据 → 选对图表 → 专业呈现。三步搞定数据可视化。

## When to Use

- 需要把数据做成图表
- 不知道该用什么类型的图表
- 图表做出来不好看需要美化
- 用户说"帮我做个图表""数据可视化"

## When NOT to Use

- 复杂数据分析仪表盘 → 使用 `wps-data-viz`
- PPT中的图表 → 使用 `wps-ppt-gen`

## 图表选择指南

```text
你的数据要表达什么？

├─ 比较大小 → 柱状图（≤12项）/ 条形图（项目名长）
│  └─ 多组对比 → 簇状柱形图
│  └─ 占比对比 → 堆积柱形图
│
├─ 趋势变化 → 折线图（时间序列）
│  └─ 多条线 → 建议≤5条，否则太乱
│  └─ 面积强调 → 面积图
│
├─ 占比构成 → 饼图（≤6项）/ 环形图
│  └─ >6项 → 改用条形图排序
│  └─ 多层级 → 旭日图
│
├─ 分布关系 → 散点图 / 气泡图
│
├─ 地理数据 → 地图图表
│
└─ 多维对比 → 雷达图（≤8维度）
```

## 工作流程

### Step 1: 分析数据特征

- 数据量（行/列数）
- 数据类型（时间序列？分类？连续？）
- 表达目的（对比？趋势？占比？关系？）

### Step 2: 推荐图表类型 + 生成方案

**方案A：openpyxl生成Excel内嵌图表**

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter

def create_chart(ws, chart_type, data_range, title, categories_col=1):
    """创建图表"""
    chart_map = {
        'bar': BarChart,
        'line': LineChart,
        'pie': PieChart,
    }

    chart = chart_map.get(chart_type, BarChart)()
    chart.title = title
    chart.width = 18
    chart.height = 12

    max_row = ws.max_row
    max_col = ws.max_column

    # 数据系列
    data = Reference(ws, min_col=categories_col + 1,
                     min_row=1, max_col=max_col, max_row=max_row)
    cats = Reference(ws, min_col=categories_col,
                     min_row=2, max_row=max_row)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)

    # 美化
    chart.style = 10
    if chart_type == 'bar':
        chart.y_axis.title = "数值"
        chart.x_axis.title = "类别"
    elif chart_type == 'pie':
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showPercent = True

    return chart

# 使用示例
wb = Workbook()
ws = wb.active
# ... 填入数据 ...
chart = create_chart(ws, 'bar', None, '2025年销售数据')
ws.add_chart(chart, 'E2')
wb.save('chart_output.xlsx')
```

**方案B：JSA操作WPS原生图表**

```javascript
// JSA: 创建柱状图
function CreateBarChart() {
    var ws = Application.ActiveSheet;
    var dataRange = ws.UsedRange;

    var chart = ws.ChartObjects.Add(
        dataRange.Left + dataRange.Width + 20, // 放在数据右侧
        dataRange.Top,
        450, 300
    ).Chart;

    chart.ChartType = 51; // xlColumnClustered
    chart.SetSourceData(dataRange);
    chart.HasTitle = true;
    chart.ChartTitle.Text = "数据图表";

    // 美化配色
    var colors = [0xD35400, 0x2ECC71, 0x3498DB, 0xF39C12, 0x9B59B6];
    for (var i = 1; i <= chart.SeriesCollection().Count; i++) {
        if (i <= colors.length) {
            chart.SeriesCollection(i).Format.Fill.ForeColor.RGB = colors[i-1];
        }
    }

    // 添加数据标签
    chart.SeriesCollection(1).HasDataLabels = true;
    chart.SeriesCollection(1).DataLabels().Position = 0; // xlLabelPositionOutsideEnd
}
```

### Step 3: 图表美化规范

```text
配色方案（专业商务）：
  主色：#2C3E50（深蓝灰）
  强调：#E74C3C（红）#3498DB（蓝）#2ECC71（绿）#F39C12（橙）
  背景：#FFFFFF 或 #F8F9FA

字体：
  标题：14pt 微软雅黑 加粗
  轴标签：10pt 微软雅黑
  数据标签：9pt

布局：
  ✅ 有标题、有单位
  ✅ Y轴从0开始（柱状图）
  ✅ 图例放右侧或底部
  ✅ 网格线浅灰色或隐藏
  ❌ 不要3D效果
  ❌ 不要太多颜色（≤5色）
  ❌ 饼图不超过6块
```

### Step 4: 交付

1. 生成含图表的 .xlsx 文件
2. 或提供JSA宏代码让用户在WPS中运行
3. 说明如何调整（修改数据范围、切换图表类型）

## 常用图表类型编号（JSA ChartType）

| 图表类型 | ChartType值 | 说明 |
|---------|------------|------|
| 簇状柱形图 | 51 | xlColumnClustered |
| 堆积柱形图 | 52 | xlColumnStacked |
| 折线图 | 4 | xlLine |
| 带标记折线图 | 65 | xlLineMarkers |
| 饼图 | 5 | xlPie |
| 环形图 | -4120 | xlDoughnut |
| 条形图 | 57 | xlBarClustered |
| 面积图 | 1 | xlArea |
| 散点图 | -4169 | xlXYScatter |
| 雷达图 | -4151 | xlRadar |

## 示例

```bash
# 自动选图表
/wps-chart 我有12个月的销售额数据，想看趋势

# 指定类型
/wps-chart 把部门人数做成饼图

# 美化已有图表
/wps-chart 我的柱状图太丑了，帮我美化一下
```
