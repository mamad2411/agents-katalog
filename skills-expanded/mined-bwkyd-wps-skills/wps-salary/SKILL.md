---
name: wps-salary
description: |
  工资条计算。根据薪资数据计算五险一金和个人所得税，
  生成规范的工资条Excel，支持批量生成。
  用于帮助HR和财务处理薪资。当用户提到工资条、个税、五险一金时触发。
  Salary slip and tax calculator.
license: MIT
user-invocable: true
argument-hint: '[薪资数据/需求描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 工资条计算
  description_zh: 根据薪资计算五险一金和个税，生成规范的工资条
  tags:
    - 工资条
    - 薪资
    - 个税
    - 五险一金
    - WPS
  version: 1.0.2
  license: MIT
---

# 工资条/薪资表生成器

薪资数据 → 个税计算 → 规范工资条 → 批量生成。HR和财务的必备工具。

## When to Use

- 每月生成员工工资条
- 需要计算个税和五险一金
- 批量生成可打印的工资条
- 用户说"帮我做工资条""算个税"

## When NOT to Use

- 财务报表分析 → 使用 `wps-financial-report`
- 考勤统计 → 使用 `wps-attendance`

## 个税税率表（2024年累计预扣法）

```text
累计应纳税所得额          税率    速算扣除数
≤36,000                  3%      0
36,000-144,000           10%     2,520
144,000-300,000          20%     16,920
300,000-420,000          25%     31,920
420,000-660,000          30%     52,920
660,000-960,000          35%     85,920
>960,000                 45%     181,920

起征点：5,000元/月
专项扣除：五险一金个人部分
专项附加扣除：子女教育1000/月、继续教育400/月、
  大病医疗据实、住房贷款1000/月、住房租金800-1500/月、
  赡养老人2000/月（独生）
```

## 工作流程

### Step 1: 确认薪资结构

```text
标准工资条结构：
┌─────────────────────────────────────────┐
│          XX公司工资条 2026年3月          │
├─────────┬───────────┬──────────────────┤
│ 姓名    │ 张三       │ 部门：技术部     │
│ 工号    │ EMP001     │ 岗位：高级工程师 │
├─────────┴───────────┴──────────────────┤
│ 【应发项目】                            │
│ 基本工资    岗位工资    绩效奖金   加班费│
│ 8,000      4,000      2,000     500   │
│ 应发合计：14,500                        │
├────────────────────────────────────────┤
│ 【扣除项目】                            │
│ 养老8%  医疗2%  失业0.5%  公积金12%    │
│ 1,160   290    72.5      1,740       │
│ 个人所得税：145.88                      │
│ 扣除合计：3,408.38                      │
├────────────────────────────────────────┤
│ 实发工资：11,091.62                     │
└────────────────────────────────────────┘
```

### Step 2: 计算引擎

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from datetime import datetime
import os

class SalaryCalculator:
    """薪资计算器"""

    # 个税累进税率
    TAX_BRACKETS = [
        (36000, 0.03, 0),
        (144000, 0.10, 2520),
        (300000, 0.20, 16920),
        (420000, 0.25, 31920),
        (660000, 0.30, 52920),
        (960000, 0.35, 85920),
        (float('inf'), 0.45, 181920),
    ]

    # 五险一金比例（个人部分，各地不同，这是通用参考）
    INSURANCE_RATES = {
        '养老': 0.08,
        '医疗': 0.02,
        '失业': 0.005,
        '公积金': 0.12,
    }

    def __init__(self, base=5000, special_deduction=0):
        self.threshold = base  # 起征点
        self.special_deduction = special_deduction  # 专项附加扣除

    def calc_insurance(self, base_salary):
        """计算五险一金个人部分"""
        result = {}
        for name, rate in self.INSURANCE_RATES.items():
            result[name] = round(base_salary * rate, 2)
        result['合计'] = round(sum(result.values()), 2)
        return result

    def calc_tax(self, taxable_income_ytd, taxable_income_prev_ytd=0):
        """累计预扣法计算个税"""
        def _calc(income):
            for limit, rate, deduction in self.TAX_BRACKETS:
                if income <= limit:
                    return round(income * rate - deduction, 2)
            return 0

        tax_ytd = _calc(taxable_income_ytd)
        tax_prev = _calc(taxable_income_prev_ytd)
        return max(round(tax_ytd - tax_prev, 2), 0)

    def calc_monthly(self, gross, insurance_base, month, prev_taxable_ytd=0):
        """计算单月薪资"""
        insurance = self.calc_insurance(insurance_base)
        taxable = gross - insurance['合计'] - self.threshold - self.special_deduction
        taxable = max(taxable, 0)

        taxable_ytd = prev_taxable_ytd + taxable
        tax = self.calc_tax(taxable_ytd, prev_taxable_ytd)

        net = round(gross - insurance['合计'] - tax, 2)

        return {
            '应发合计': gross,
            '五险一金': insurance,
            '应纳税所得额': taxable,
            '个税': tax,
            '扣除合计': round(insurance['合计'] + tax, 2),
            '实发工资': net,
        }


def generate_salary_slips(data_path, output_path, year_month):
    """从Excel数据生成工资条"""
    wb_data = load_workbook(data_path)
    ws_data = wb_data.active

    wb_out = Workbook()
    ws = wb_out.active
    ws.title = f"工资条{year_month}"

    calc = SalaryCalculator()
    row = 1

    # 读取表头
    headers = [cell.value for cell in ws_data[1]]

    for data_row in ws_data.iter_rows(min_row=2, values_only=True):
        emp = dict(zip(headers, data_row))

        gross = float(emp.get('应发合计', 0) or 0)
        base = float(emp.get('社保基数', gross) or gross)
        result = calc.calc_monthly(gross, base, int(year_month[-2:]))

        # 写入工资条格式
        _write_slip(ws, row, emp, result, year_month)
        row += 8  # 每个工资条占7行 + 1行空行

    wb_out.save(output_path)
    return os.path.abspath(output_path)


def _write_slip(ws, start_row, emp, result, year_month):
    """写入单个工资条"""
    thin = Side(style='thin')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    header_fill = PatternFill('solid', fgColor='4472C4')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    body_font = Font(name='微软雅黑', size=10)

    r = start_row
    # 标题行
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    cell = ws.cell(row=r, column=1,
                   value=f"工资条 {year_month}  姓名：{emp.get('姓名','')}  "
                         f"部门：{emp.get('部门','')}")
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center')

    r += 1
    items = [
        ('基本工资', emp.get('基本工资', '')),
        ('岗位工资', emp.get('岗位工资', '')),
        ('绩效', emp.get('绩效', '')),
        ('应发合计', result['应发合计']),
        ('五险一金', result['五险一金']['合计']),
        ('个税', result['个税']),
        ('扣除合计', result['扣除合计']),
        ('实发工资', result['实发工资']),
    ]
    for col, (label, val) in enumerate(items, 1):
        ws.cell(row=r, column=col, value=label).font = Font(
            name='微软雅黑', size=9, bold=True)
        ws.cell(row=r, column=col).border = border
        ws.cell(row=r+1, column=col, value=val).font = body_font
        ws.cell(row=r+1, column=col).border = border
        ws.cell(row=r+1, column=col).number_format = '#,##0.00'
```

### Step 3: 交付

1. 生成工资条Excel文件（含格式）
2. 或生成可打印的工资条（每页N条，带裁切线）
3. 提供个税验证说明

## JSA宏：在WPS中直接生成工资条

```javascript
// JSA: 薪资表→工资条转换
function SalaryToSlips() {
    var ws = Application.ActiveSheet;
    var lastRow = ws.Cells(ws.Rows.Count, 1).End(-4162).Row;
    var lastCol = ws.Cells(1, ws.Columns.Count).End(-4159).Column;
    var newWs = Application.Sheets.Add();
    newWs.Name = "工资条";

    var outRow = 1;
    for (var i = 2; i <= lastRow; i++) {
        // 复制表头
        for (var j = 1; j <= lastCol; j++) {
            newWs.Cells(outRow, j).Value2 = ws.Cells(1, j).Value2;
            newWs.Cells(outRow, j).Font.Bold = true;
        }
        outRow++;
        // 复制数据
        for (var j = 1; j <= lastCol; j++) {
            newWs.Cells(outRow, j).Value2 = ws.Cells(i, j).Value2;
        }
        outRow++;
        outRow++; // 空行（便于裁切）
    }
    Application.alert("已生成 " + (lastRow - 1) + " 条工资条");
}
```

## 示例

```bash
# 生成工资条
/wps-salary 帮我把这个薪资表生成工资条格式，方便打印发给员工

# 计算个税
/wps-salary 月薪15000，社保基数12000，公积金12%，算一下到手多少

# 批量生成
/wps-salary 用salary_data.xlsx生成每个人独立的工资条
```
