---
name: wps-schedule
description: |
  课程表/日程表。快速生成格式漂亮的课程表、周工作计划、会议日程表，
  按时间×日期的矩阵布局，不同类别自动用不同颜色区分。
  用于帮助用户制作时间安排表。当用户提到课程表、日程表、时间安排、周计划时触发。
  Schedule/timetable generator - class schedules, weekly plans, event agendas.
license: MIT
user-invocable: true
argument-hint: '[日程类型/内容]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 课程表/日程表
  description_zh: 生成课程表、周工作计划表、会议日程安排表
  tags:
    - 日程
    - 课程表
    - 时间表
    - 计划
    - WPS
  version: 1.0.1
  license: MIT
---

# 日程/时间表生成器

快速生成格式化的课程表、周计划、活动日程。

## When to Use

- 制作课程表
- 周/月工作计划表
- 会议/活动日程安排
- 用户说"做个课程表""周计划表"

## When NOT to Use

- 排班值班 → 使用 `wps-cn-calendar`
- 项目甘特图 → 使用 `wps-gantt`

## 模板类型

```text
[1] 课程表 → 周一~周五 × 时间段
[2] 周计划 → 周一~周日 × 时间
[3] 会议日程 → 时间 × 议程
[4] 活动安排 → 多日活动详细时间表
```

## 工作流程

### Step 1: 确认日程信息

- 类型（课程表/周计划/会议日程）
- 时间范围和时间段划分
- 内容项

### Step 2: 生成时间表

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import os

def create_timetable(schedule_type, data, output_path=None):
    """生成时间表"""
    wb = Workbook()
    ws = wb.active

    header_fill = PatternFill('solid', fgColor='2C3E50')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    body_font = Font(name='微软雅黑', size=10)
    thin = Side(style='thin')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # 分类颜色
    colors = {
        '语文': 'FADBD8', '数学': 'AED6F1', '英语': 'A9DFBF',
        '物理': 'F9E79F', '化学': 'D7BDE2', '体育': 'ABEBC6',
        '会议': 'AED6F1', '工作': 'A9DFBF', '学习': 'F9E79F',
    }

    if schedule_type == '课程表':
        ws.title = "课程表"
        days = ['时间', '周一', '周二', '周三', '周四', '周五']
        time_slots = data.get('time_slots', [
            '08:00-08:45', '08:55-09:40', '10:00-10:45', '10:55-11:40',
            '14:00-14:45', '14:55-15:40', '16:00-16:45',
        ])

        # 标题
        ws.merge_cells(start_row=1, start_column=1,
                       end_row=1, end_column=len(days))
        ws['A1'] = data.get('title', '课程表')
        ws['A1'].font = Font(name='微软雅黑', size=18, bold=True)
        ws['A1'].alignment = Alignment(horizontal='center')

        # 表头
        for col, day in enumerate(days, 1):
            cell = ws.cell(row=2, column=col, value=day)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = border

        ws.column_dimensions['A'].width = 15
        for col in range(2, len(days) + 1):
            ws.column_dimensions[chr(64 + col)].width = 14

        # 时间段和课程
        courses = data.get('courses', {})
        for row, time_slot in enumerate(time_slots, 3):
            ws.cell(row=row, column=1, value=time_slot).font = body_font
            ws.cell(row=row, column=1).alignment = Alignment(horizontal='center')
            ws.cell(row=row, column=1).border = border
            ws.row_dimensions[row].height = 35

            for col in range(2, len(days) + 1):
                cell = ws.cell(row=row, column=col)
                key = f'{days[col-1]}_{row-3}'
                course = courses.get(key, '')
                cell.value = course
                cell.font = body_font
                cell.alignment = Alignment(horizontal='center',
                                           vertical='center')
                cell.border = border
                # 颜色
                for subject, color in colors.items():
                    if subject in str(course):
                        cell.fill = PatternFill('solid', fgColor=color)
                        break

            # 午休分隔
            if row == 6:
                r = row + 1
                ws.merge_cells(start_row=r, start_column=1,
                               end_row=r, end_column=len(days))
                ws.cell(row=r, column=1, value='午  休').font = Font(
                    name='微软雅黑', size=12, bold=True, color='888888')
                ws.cell(row=r, column=1).alignment = Alignment(
                    horizontal='center')

    if not output_path:
        output_path = f'{schedule_type}.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成格式化时间表Excel
2. 颜色区分不同类别
3. 可直接打印

## 示例

```bash
# 课程表
/wps-schedule 帮我做个课程表，周一到周五，每天7节课

# 周计划
/wps-schedule 做一个下周的工作计划表

# 会议日程
/wps-schedule 明天全天会议的日程安排表
```
