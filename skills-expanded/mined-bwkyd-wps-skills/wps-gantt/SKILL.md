---
name: wps-gantt
description: |
  项目甘特图。输入任务名称、开始结束日期，自动在Excel里画出甘特图，
  用颜色显示进度，不用买Project也能做漂亮的项目排期表。
  用于帮助用户制作项目甘特图。当用户提到甘特图、项目排期、时间线时触发。
  Gantt chart generator in Excel - no Project software needed.
license: MIT
user-invocable: true
argument-hint: '[项目任务列表/需求]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 甘特图生成
  description_zh: 根据任务列表在Excel中生成甘特图，用于项目进度管理
  tags:
    - 甘特图
    - 项目管理
    - 排期
    - Excel
    - WPS
  version: 1.0.1
  license: MIT
---

# 甘特图生成器

任务列表 → Excel甘特图。不用Project也能做项目排期。

## When to Use

- 制作项目计划/排期表
- 需要可视化的时间线
- 项目进度跟踪
- 用户说"做个甘特图""项目排期表"

## When NOT to Use

- 复杂项目管理 → 建议使用专业工具
- 普通表格 → 使用 `wps-docx-writer`

## 工作流程

### Step 1: 确认任务信息

每个任务需要：
- 任务名称
- 开始日期
- 结束日期（或工期天数）
- 负责人（可选）
- 进度百分比（可选）

### Step 2: 生成甘特图

```python
from openpyxl import Workbook
from openpyxl.styles import (Font, Alignment, PatternFill,
                              Border, Side, numbers)
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta
import os

def create_gantt(tasks, output_path=None):
    """
    tasks = [
        {'name': '需求分析', 'start': '2026-04-01', 'end': '2026-04-07',
         'owner': '张三', 'progress': 100},
        {'name': '系统设计', 'start': '2026-04-08', 'end': '2026-04-14',
         'owner': '李四', 'progress': 60},
        ...
    ]
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "项目甘特图"

    # 计算日期范围
    all_dates = []
    for t in tasks:
        all_dates.append(datetime.strptime(t['start'], '%Y-%m-%d'))
        all_dates.append(datetime.strptime(t['end'], '%Y-%m-%d'))
    min_date = min(all_dates)
    max_date = max(all_dates)
    total_days = (max_date - min_date).days + 1

    # 样式
    header_fill = PatternFill('solid', fgColor='2C3E50')
    header_font = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF')
    bar_fill = PatternFill('solid', fgColor='3498DB')
    done_fill = PatternFill('solid', fgColor='2ECC71')
    milestone_fill = PatternFill('solid', fgColor='E74C3C')
    today_fill = PatternFill('solid', fgColor='F39C12')
    thin = Side(style='thin', color='D5D8DC')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # 左侧列标题
    left_headers = ['序号', '任务名称', '负责人', '开始', '结束', '进度']
    for col, h in enumerate(left_headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    # 列宽
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 8
    ws.column_dimensions['D'].width = 11
    ws.column_dimensions['E'].width = 11
    ws.column_dimensions['F'].width = 7

    # 日期列标题（每天一列或按周）
    date_start_col = len(left_headers) + 1
    use_weekly = total_days > 60

    if use_weekly:
        # 按周显示
        week_start = min_date - timedelta(days=min_date.weekday())
        col = date_start_col
        while week_start <= max_date:
            cell = ws.cell(row=1, column=col,
                          value=week_start.strftime('%m/%d'))
            cell.font = Font(name='微软雅黑', size=8, color='FFFFFF')
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
            ws.column_dimensions[get_column_letter(col)].width = 5
            week_start += timedelta(days=7)
            col += 1
    else:
        for d in range(total_days):
            date = min_date + timedelta(days=d)
            col = date_start_col + d
            cell = ws.cell(row=1, column=col, value=date.strftime('%m/%d'))
            cell.font = Font(name='微软雅黑', size=7, color='FFFFFF')
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', text_rotation=90)
            ws.column_dimensions[get_column_letter(col)].width = 3.5

    # 任务行
    body_font = Font(name='微软雅黑', size=10)
    for row_idx, task in enumerate(tasks, 2):
        ws.cell(row=row_idx, column=1, value=row_idx-1).font = body_font
        ws.cell(row=row_idx, column=2, value=task['name']).font = body_font
        ws.cell(row=row_idx, column=3,
                value=task.get('owner', '')).font = body_font
        ws.cell(row=row_idx, column=4, value=task['start']).font = body_font
        ws.cell(row=row_idx, column=5, value=task['end']).font = body_font
        progress = task.get('progress', 0)
        ws.cell(row=row_idx, column=6,
                value=f'{progress}%').font = body_font

        # 画甘特条
        start = datetime.strptime(task['start'], '%Y-%m-%d')
        end = datetime.strptime(task['end'], '%Y-%m-%d')

        if use_weekly:
            week_start = min_date - timedelta(days=min_date.weekday())
            s_col = date_start_col + (start - week_start).days // 7
            e_col = date_start_col + (end - week_start).days // 7
        else:
            s_col = date_start_col + (start - min_date).days
            e_col = date_start_col + (end - min_date).days

        for c in range(s_col, e_col + 1):
            cell = ws.cell(row=row_idx, column=c)
            if progress == 100:
                cell.fill = done_fill
            else:
                cell.fill = bar_fill
            cell.border = border

    ws.row_dimensions[1].height = 30
    ws.freeze_panes = 'G2'  # 冻结左侧列和标题行

    if not output_path:
        output_path = '项目甘特图.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成甘特图Excel文件
2. 冻结窗格方便查看
3. 颜色说明（蓝=进行中，绿=已完成，红=里程碑）

## 示例

```bash
# 生成甘特图
/wps-gantt 帮我做个项目甘特图，需求分析2周→设计1周→开发4周→测试2周→上线

# 从数据生成
/wps-gantt 用tasks.xlsx里的任务列表生成甘特图

# 更新进度
/wps-gantt 更新项目甘特图的进度
```
