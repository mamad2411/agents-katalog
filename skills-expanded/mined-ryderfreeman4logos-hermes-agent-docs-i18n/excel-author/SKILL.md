---
name: excel-author
description: Build auditable financial workbooks headless via openpyxl.
version: 1.0.0
author: Anthropic (adapted by Nous Research)
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [excel, openpyxl, finance, spreadsheet, modeling]
    related_skills: [xlsx, pptx-author, dcf-model, comps-analysis, lbo-model, 3-statement-model]
---

# excel-author

使用 `openpyxl` 在磁盘上生成 .xlsx 文件。请遵循以下银行级规范，以确保模型具备可审计性、灵活性，并能让除开发者之外的其他人进行审查。

该技能基于 Anthropic 在 [anthropics/financial-services](https://github.com/anthropics/financial-services) 仓库中发布的 `xlsx-author` 和 `audit-xls` 技能优化而来。原版本中的 MCP / Office-JS / Cowork 相关分支已被移除——本技能假定在无界面 Python 环境下运行。

## 输出规范

- 将文件写入 `./out/<名称>.xlsx`。如果 `./out/` 目录不存在，则需先创建该目录。
- 在最终回复中返回相对路径，以便后续工具能够获取文件。
- 每个文件仅包含一个逻辑模型。除非有明确要求，否则不得向现有工作簿中追加内容。

## 设置步骤

```bash
pip install "openpyxl>=3.0"
```

## 核心规范（不可更改）

### 蓝色/黑色/绿色单元格颜色
- **蓝色**（`Font(color="0000FF")`）——人工输入的固定值。包括收入驱动因素、加权平均资本成本参数、终端增长率以及市场数据。
- **黑色**（默认值）——公式。所有衍生单元格均为实时 Excel 公式。
- **绿色**（`Font(color="006100")`）——指向其他工作表或外部文件的链接。

这样一来，审核人员只需浏览表格，即可立即区分哪些是假设值，哪些是计算结果。

### 必须使用公式而非固定值
所有计算单元格都必须为公式字符串，绝不能是将 Python 计算出的数值直接粘贴作为内容。

```python
# WRONG — silent bug waiting to happen
ws["D20"] = revenue_prior_year * (1 + growth)

# CORRECT — flexes when the user changes the assumption
ws["D20"] = "=D19*(1+$B$8)"
```

唯一允许硬编码的数值包括：
1. 原始历史数据（实际营收、报告中的EBITDA等）；
2. 用户可自行调整的假设参数（增长率、WACC数值、终端增长率）；
3. 当前市场数据（股价、债务余额）——需在对应单元格中注明数据来源及日期。

如果发现自己正在用Python计算数值并直接写入结果，请立即停止。

### 用于跨工作表引用的命名范围
对于需要从其他工作表、演示文稿或备忘录中引用的任何数据，都应使用命名范围。

```python
from openpyxl.workbook.defined_name import DefinedName
wb.defined_names["WACC"] = DefinedName("WACC", attr_text="Inputs!$C$8")
# then elsewhere:
calc["D30"] = "=D29/WACC"
```

### 余额校验标签页
该标签页包含一个 `Checks` 标签页，用于整合所有相关数据并显示 TRUE/FALSE 结果：
- 资产负债表平衡性（资产 = 负债 + 所有者权益）
- 现金流与资产负债表中各期现金变动的匹配情况
- 各组成部分之和与合并后的总计是否一致
- 计算范围内不存在非法硬编码

示例：
```python
checks = wb.create_sheet("Checks")
checks["A2"] = "BS balances"
checks["B2"] = "=IS!D20-IS!D21-IS!D22"
checks["C2"] = "=ABS(B2)<0.01"  # TRUE/FALSE
```

### 对每个硬编码输入添加单元格注释
请在创建单元格时立即添加注释，切勿延后操作。

```python
from openpyxl.comments import Comment
ws["C2"] = 1_250_000_000
ws["C2"].font = Font(color="0000FF")
ws["C2"].comment = Comment("Source: 10-K FY2024, p.47, revenue line", "analyst")
```

格式：`来源：[系统/文档]，[日期]，[参考编号]，[如有相关网址则填写]。`

绝不可延迟标注来源。也严禁使用“TODO: 添加来源”这样的表述。

## 典型财务模型框架

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
from pathlib import Path

BLUE = Font(color="0000FF")
BLACK = Font(color="000000")
GREEN = Font(color="006100")
BOLD = Font(bold=True)
HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(color="FFFFFF", bold=True)

wb = Workbook()

# --- Inputs tab ---
inp = wb.active
inp.title = "Inputs"
inp["A1"] = "MARKET DATA & KEY INPUTS"
inp["A1"].font = HEADER_FONT
inp["A1"].fill = HEADER_FILL
inp.merge_cells("A1:C1")

inp["B3"] = "Revenue FY2024"
inp["C3"] = 1_250_000_000
inp["C3"].font = BLUE
inp["C3"].comment = Comment("Source: 10-K FY2024 p.47", "model")

inp["B4"] = "Growth Rate"
inp["C4"] = 0.12
inp["C4"].font = BLUE

# --- Calc tab ---
calc = wb.create_sheet("DCF")
calc["B2"] = "Projected Revenue"
calc["C2"] = "=Inputs!C3*(1+Inputs!C4)"   # formula, black

# --- Checks tab ---
chk = wb.create_sheet("Checks")
chk["A2"] = "BS balances"
chk["B2"] = "=ABS(BS!D20-BS!D21-BS!D22)<0.01"

Path("./out").mkdir(exist_ok=True)
wb.save("./out/model.xlsx")
```

## 合并单元格的章节标题设置

openpyxl 的特殊要求：在合并单元格时，需先设置左上角单元格的值，再单独为整个合并区域设置样式。

```python
ws["A7"] = "CASH FLOW PROJECTION"
ws["A7"].font = HEADER_FONT
ws.merge_cells("A7:H7")
for col in range(1, 9):  # A..H
    ws.cell(row=7, column=col).fill = HEADER_FILL
```

## 敏感性分析表

应通过循环结构构建表格，而非为每个单元格硬编码公式。相关规则如下：

- **行数/列数为奇数**（如5×5或7×7）——这样可以确保存在真正的中心单元格。
- **中心单元格即为基准情况**。中间行/列的数值必须与模型实际的加权平均资本成本及永续增长率一致，这样中心的计算结果才会对应基准情况下的预期股价。这是用于验证计算正确性的关键步骤。
- 用中蓝色填充色（`"BDD7EE"`）并加粗来标出中心单元格。
- 每个单元格都需填入完整的重新计算公式——绝不能使用近似值。

```python
# 5x5 WACC (rows) x terminal growth (cols) sensitivity
wacc_axis = [0.08, 0.085, 0.09, 0.095, 0.10]        # center row = base 9.0%
term_axis = [0.02, 0.025, 0.03, 0.035, 0.04]        # center col = base 3.0%

start_row = 40
ws.cell(row=start_row, column=1).value = "Implied Share Price ($)"
ws.cell(row=start_row, column=1).font = BOLD

for j, g in enumerate(term_axis):
    ws.cell(row=start_row+1, column=2+j).value = g
    ws.cell(row=start_row+1, column=2+j).font = BLUE

for i, w in enumerate(wacc_axis):
    r = start_row + 2 + i
    ws.cell(row=r, column=1).value = w
    ws.cell(row=r, column=1).font = BLUE
    for j, g in enumerate(term_axis):
        c = 2 + j
        # Full DCF recalc formula (simplified for illustration).
        # In a real model this references the full projection block.
        ws.cell(row=r, column=c).value = (
            f"=SUMPRODUCT(FCF_range,1/(1+{w})^year_offset) + "
            f"FCF_terminal*(1+{g})/({w}-{g})/(1+{w})^terminal_year"
        )

# Highlight center cell (base case)
center = ws.cell(row=start_row+2+len(wacc_axis)//2,
                 column=2+len(term_axis)//2)
center.fill = PatternFill("solid", fgColor="BDD7EE")
center.font = BOLD
```

## 交付前的重新计算

openpyxl仅会写入公式字符串，而不会实际计算这些公式。Excel在文件被打开时会自动重新计算，但后续的处理程序（如自动检查脚本、持续集成系统）需要的是已计算完成的数值。

因此，建议在交付前运行LibreOffice或执行专门的重新计算步骤：

```bash
# LibreOffice headless recalc
libreoffice --headless --calc --convert-to xlsx ./out/model.xlsx --outdir ./out/
```

或者可以使用 Python 重算辅助工具（详见该技能中的 `scripts/recalc.py` 文件）。

## 模型结构规划

在编写任何公式之前，请遵循以下步骤：
1. 先确定所有章节的行位置
2. 写入所有的表头和标签
3. 添加所有的章节分隔符及空行
4. 最后再根据已确定的行位置编写公式

这样做可以避免“公式链断裂”问题——即在公式写完后插入表头行会导致后续的所有引用出错。

## 与用户逐步验证结果

对于大型模型（DCF、三表模型、LBO模型），在继续下一步之前，请暂停并向用户展示中间结果。在生成下游敏感性分析表之前发现 margin 假设有误，往往能节省数小时的调试时间。

具体的检查点安排如下：
- 完成“输入数据”部分后 → 显示原始输入数据，并在继续推演前获得用户确认
- 完成收入预测后 → 确认营收总额及增长趋势
- 完成自由现金流计算后 → 确认整个时间表的正确性
- 计算完加权平均资本成本后 → 确认输入参数无误
- 完成估值后 → 确认股权价值转换逻辑正确
- 所有步骤确认无误后，再生成敏感性分析表

## 何时不应使用此技能

- 用户正在使用支持 Office MCP 的实时 Excel 会话——建议让他们直接操作自己的实时工作簿。
- 仅需导出纯表格数据且不包含公式的情况——使用 `csv` 格式或 `pandas.to_excel` 函数更为简单。
- 需要高度交互功能的仪表板或图表——应选用专业的商业智能工具。

## 来源说明

本文所采用的规范（蓝色/黑色/绿色标识、优先使用公式而非硬编码、命名范围、敏感性分析规则等）借鉴自 Anthropic 的 Claude for Financial Services 插件套件，采用 Apache-2.0 许可协议。原始代码地址：https://github.com/anthropics/financial-services/tree/main/plugins/vertical-plugins/financial-analysis/skills/xlsx-author
