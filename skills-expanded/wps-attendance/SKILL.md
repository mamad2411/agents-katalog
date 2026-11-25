---
name: wps-attendance
description: |
  考勤打卡统计。把考勤机导出的打卡数据丢进来，自动统计每个人的
  迟到、早退、缺勤、加班时长，生成月度考勤汇总表，异常考勤自动标红。
  用于帮助HR处理考勤数据。当用户提到考勤、打卡、迟到、加班统计时触发。
  Attendance tracker - generates summary reports from clock-in records.
license: MIT
user-invocable: true
argument-hint: '[考勤数据/需求描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 考勤统计
  description_zh: 导入打卡记录，自动统计迟到早退缺勤加班，生成月度考勤汇总表
  tags:
    - 考勤
    - 打卡
    - HR
    - 加班
    - WPS
  version: 1.0.1
  license: MIT
---

# 考勤统计工具

打卡记录 → 考勤汇总 → 月度报表。HR每月必用。

## When to Use

- 处理考勤机导出的打卡数据
- 统计迟到、早退、缺勤、加班
- 生成月度考勤汇总表
- 用户说"帮我统计考勤""处理打卡记录"

## When NOT to Use

- 工资计算 → 使用 `wps-salary`
- 排班表制作 → 使用 `wps-schedule`

## 考勤规则配置

```text
标准班制（可自定义）：
  上班时间：09:00
  下班时间：18:00
  午休：12:00-13:00
  迟到容忍：10分钟（09:10前不算迟到）
  早退判定：17:30前离开
  加班起算：18:30之后
  缺勤判定：无打卡记录且无请假
```

## 工作流程

### Step 1: 读取打卡数据

支持常见考勤机导出格式：

```text
常见格式：
A列：工号/姓名
B列：日期
C列：打卡时间1（上班）
D列：打卡时间2（下班）
（或合并在一列，多次打卡用逗号分隔）
```

### Step 2: 考勤计算引擎

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime, timedelta
import os
import re

class AttendanceCalculator:
    """考勤计算器"""

    def __init__(self, config=None):
        default = {
            'work_start': '09:00',
            'work_end': '18:00',
            'late_tolerance': 10,  # 分钟
            'early_leave_before': '17:30',
            'overtime_after': '18:30',
            'lunch_start': '12:00',
            'lunch_end': '13:00',
        }
        self.config = {**default, **(config or {})}

    def _parse_time(self, t):
        if isinstance(t, datetime):
            return t
        if isinstance(t, str):
            for fmt in ['%H:%M:%S', '%H:%M', '%Y-%m-%d %H:%M:%S']:
                try:
                    return datetime.strptime(t.strip(), fmt)
                except ValueError:
                    continue
        return None

    def analyze_day(self, clock_in, clock_out, is_workday=True):
        """分析单日考勤"""
        result = {
            'status': '正常',
            'late_minutes': 0,
            'early_minutes': 0,
            'overtime_minutes': 0,
            'absent': False,
        }

        if not is_workday:
            if clock_in and clock_out:
                result['status'] = '加班'
                ci = self._parse_time(clock_in)
                co = self._parse_time(clock_out)
                if ci and co:
                    result['overtime_minutes'] = max(
                        int((co - ci).total_seconds() / 60) - 60, 0)
            return result

        if not clock_in and not clock_out:
            result['status'] = '缺勤'
            result['absent'] = True
            return result

        work_start = self._parse_time(self.config['work_start'])
        ci = self._parse_time(clock_in)
        if ci and work_start:
            diff = int((ci - work_start).total_seconds() / 60)
            if diff > self.config['late_tolerance']:
                result['late_minutes'] = diff
                result['status'] = '迟到'

        work_end = self._parse_time(self.config['work_end'])
        early_limit = self._parse_time(self.config['early_leave_before'])
        overtime_start = self._parse_time(self.config['overtime_after'])
        co = self._parse_time(clock_out)

        if co and early_limit:
            if co < early_limit:
                diff = int((early_limit - co).total_seconds() / 60)
                result['early_minutes'] = diff
                result['status'] = '早退' if result['status'] == '正常' \
                    else result['status'] + '+早退'

        if co and overtime_start:
            if co > overtime_start:
                result['overtime_minutes'] = int(
                    (co - overtime_start).total_seconds() / 60)

        return result


def generate_attendance_report(data_path, output_path, year_month, config=None):
    """生成月度考勤报表"""
    calc = AttendanceCalculator(config)
    wb_data = load_workbook(data_path)
    ws_data = wb_data.active

    wb_out = Workbook()
    ws = wb_out.active
    ws.title = f"考勤汇总{year_month}"

    # 表头
    headers = ['姓名', '部门', '应出勤', '实出勤', '迟到次数',
               '早退次数', '缺勤天数', '加班时长(h)', '备注']
    header_fill = PatternFill('solid', fgColor='4472C4')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')

    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    # 统计每人数据（示例逻辑）
    # ... 遍历打卡数据，调用calc.analyze_day() ...

    wb_out.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 生成汇总报表

```text
考勤月报模板：
┌────────────────────────────────────────────┐
│       XX公司 2026年3月 考勤汇总表          │
├────┬────┬────┬────┬────┬────┬────┬────┬───┤
│姓名│部门│应勤│实勤│迟到│早退│缺勤│加班│备注│
├────┼────┼────┼────┼────┼────┼────┼────┼───┤
│张三│技术│22  │21  │1   │0   │1   │8h  │病假│
│李四│销售│22  │22  │0   │0   │0   │12h │   │
│王五│行政│22  │20  │2   │1   │2   │0   │事假│
├────┴────┴────┴────┴────┴────┴────┴────┴───┤
│ 部门汇总 / 异常标记 / 审批签字栏           │
└────────────────────────────────────────────┘
```

### Step 4: 交付

1. 生成月度考勤汇总Excel（含格式和条件格式高亮异常）
2. 个人考勤明细表（可选）
3. 异常考勤提醒列表

## 考勤公式速查（WPS表格内直接用）

```text
# 判断迟到（C列为打卡时间）
=IF(C2>"09:10","迟到"&TEXT(C2-"09:00","h小时m分"),"正常")

# 计算加班时长（D列为下班打卡）
=IF(D2>"18:30",TEXT(D2-"18:30","h:mm"),"无")

# 统计迟到次数
=COUNTIF(E2:E32,"迟到*")

# 统计出勤天数
=COUNTA(C2:C32)-COUNTBLANK(C2:C32)
```

## 示例

```bash
# 处理打卡记录
/wps-attendance 帮我统计这个月的考勤，打卡数据在attendance_march.xlsx

# 生成报表
/wps-attendance 生成3月份考勤汇总表，标准班制9点到6点

# 加班统计
/wps-attendance 统计一下这个月每个人的加班时长
```
