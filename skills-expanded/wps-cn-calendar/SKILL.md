---
name: wps-cn-calendar
description: |
  日历排班值班表。生成带法定节假日和调休标注的月度/年度日历表，
  还能做三班倒/两班倒排班表和节假日值班安排，颜色区分不同班次一目了然。
  用于帮助用户生成日历和排班表。当用户提到日历、排班、值班、节假日时触发。
  Chinese calendar with holidays, shift scheduling, and duty rosters.
license: MIT
user-invocable: true
argument-hint: '[年月] [类型]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 日历排班表
  description_zh: 生成带法定节假日的月度日历，支持排班表和值班表
  tags:
    - 日历
    - 排班
    - 节假日
    - 值班
    - WPS
  version: 1.0.1
  license: MIT
---

# 中国日历/排班表生成器

生成含法定节假日+农历的日历表，以及排班/值班安排。

## When to Use

- 生成月度/年度日历
- 制作员工排班表
- 制作值班安排表
- 查看法定节假日安排
- 用户说"做个日历""排班表""值班安排"

## When NOT to Use

- 考勤统计 → 使用 `wps-attendance`
- 项目排期 → 使用 `wps-gantt`

## 功能模块

```text
[1] 月度日历 → 含农历、节假日标注
[2] 年度日历 → 12个月一览表
[3] 排班表 → 三班倒/两班倒/弹性
[4] 值班表 → 节假日/周末值班安排
```

## 工作流程

### Step 1: 确认需求

- **类型**：日历/排班/值班
- **时间范围**：哪年哪月
- **排班模式**（如需要）：几班倒、人员名单
- **特殊安排**（如需要）：谁请假、谁优先

### Step 2: 生成日历/排班表

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime, timedelta
import calendar
import os

# 2026年法定节假日（示例，需要每年更新）
HOLIDAYS_2026 = {
    '2026-01-01': '元旦',
    '2026-01-29': '除夕', '2026-01-30': '春节', '2026-01-31': '春节',
    '2026-02-01': '春节', '2026-02-02': '春节', '2026-02-03': '春节',
    '2026-02-04': '春节',
    '2026-04-05': '清明', '2026-04-06': '清明', '2026-04-07': '清明',
    '2026-05-01': '劳动节', '2026-05-02': '劳动节', '2026-05-03': '劳动节',
    '2026-05-04': '劳动节', '2026-05-05': '劳动节',
    '2026-05-31': '端午', '2026-06-01': '端午', '2026-06-02': '端午',
    '2026-10-01': '国庆', '2026-10-02': '国庆', '2026-10-03': '国庆',
    '2026-10-04': '国庆', '2026-10-05': '国庆', '2026-10-06': '国庆',
    '2026-10-07': '国庆',
}
# 调休上班日
WORKDAYS_2026 = {'2026-01-25', '2026-02-08', '2026-10-10'}


def create_monthly_calendar(year, month, output_path=None):
    """生成月度日历"""
    wb = Workbook()
    ws = wb.active
    ws.title = f"{year}年{month}月"

    # 样式
    header_fill = PatternFill('solid', fgColor='2C3E50')
    weekend_fill = PatternFill('solid', fgColor='FADBD8')
    holiday_fill = PatternFill('solid', fgColor='F5B7B1')
    today_fill = PatternFill('solid', fgColor='AED6F1')
    header_font = Font(name='微软雅黑', size=12, bold=True, color='FFFFFF')

    # 标题
    ws.merge_cells('A1:G1')
    ws['A1'] = f'{year}年{month}月'
    ws['A1'].font = Font(name='微软雅黑', size=18, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # 星期头
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    for col, wd in enumerate(weekdays, 1):
        cell = ws.cell(row=2, column=col, value=f'星期{wd}')
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        ws.column_dimensions[chr(64+col)].width = 14

    # 日期
    cal = calendar.Calendar(firstweekday=0)
    row = 3
    for week in cal.monthdatescalendar(year, month):
        for col, date in enumerate(week, 1):
            if date.month != month:
                continue
            date_str = date.strftime('%Y-%m-%d')
            cell = ws.cell(row=row, column=col)
            cell.value = date.day
            cell.font = Font(name='微软雅黑', size=14)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            ws.row_dimensions[row].height = 50

            # 节假日标注
            if date_str in HOLIDAYS_2026:
                cell.fill = holiday_fill
                note_cell = ws.cell(row=row, column=col)
                note_cell.value = f"{date.day}\n{HOLIDAYS_2026[date_str]}"
                note_cell.font = Font(name='微软雅黑', size=10)
                note_cell.alignment = Alignment(horizontal='center',
                                                 vertical='center',
                                                 wrap_text=True)
            elif date.weekday() >= 5 and date_str not in WORKDAYS_2026:
                cell.fill = weekend_fill

        row += 1

    if not output_path:
        output_path = f'{year}年{month}月日历.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)


def create_shift_schedule(year, month, staff_list, shift_pattern='三班倒',
                          output_path=None):
    """生成排班表"""
    wb = Workbook()
    ws = wb.active
    ws.title = f"{month}月排班"

    shifts = {
        '三班倒': ['早', '中', '晚', '休'],
        '两班倒': ['白', '夜', '休', '休'],
        '做五休二': ['班', '班', '班', '班', '班', '休', '休'],
    }
    pattern = shifts.get(shift_pattern, shifts['三班倒'])

    # 表头
    header_fill = PatternFill('solid', fgColor='2C3E50')
    header_font = Font(name='微软雅黑', size=9, bold=True, color='FFFFFF')
    shift_colors = {
        '早': PatternFill('solid', fgColor='AED6F1'),
        '白': PatternFill('solid', fgColor='AED6F1'),
        '班': PatternFill('solid', fgColor='AED6F1'),
        '中': PatternFill('solid', fgColor='F9E79F'),
        '晚': PatternFill('solid', fgColor='D7BDE2'),
        '夜': PatternFill('solid', fgColor='D7BDE2'),
        '休': PatternFill('solid', fgColor='ABEBC6'),
    }

    days_in_month = calendar.monthrange(year, month)[1]
    ws.cell(row=1, column=1, value='姓名').font = header_font
    ws.cell(row=1, column=1).fill = header_fill

    for d in range(1, days_in_month + 1):
        date = datetime(year, month, d)
        cell = ws.cell(row=1, column=d+1, value=f'{d}\n{["一","二","三","四","五","六","日"][date.weekday()]}')
        cell.font = Font(name='微软雅黑', size=8, color='FFFFFF')
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        ws.column_dimensions[chr(65+d) if d < 26 else 'A'].width = 4

    # 排班
    for i, name in enumerate(staff_list):
        ws.cell(row=i+2, column=1, value=name).font = Font(name='微软雅黑', size=10)
        for d in range(1, days_in_month + 1):
            shift_idx = (d - 1 + i) % len(pattern)
            shift = pattern[shift_idx]
            cell = ws.cell(row=i+2, column=d+1, value=shift)
            cell.alignment = Alignment(horizontal='center')
            cell.font = Font(name='微软雅黑', size=9)
            if shift in shift_colors:
                cell.fill = shift_colors[shift]

    if not output_path:
        output_path = f'{year}年{month}月排班表.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成日历/排班表Excel
2. 节假日用红色标注，周末用浅红色
3. 排班表用颜色区分不同班次

## 示例

```bash
# 月度日历
/wps-cn-calendar 生成2026年4月的日历

# 排班表
/wps-cn-calendar 4月排班表，三班倒，人员：张三李四王五赵六

# 值班表
/wps-cn-calendar 五一假期值班安排，6个人轮流
```
