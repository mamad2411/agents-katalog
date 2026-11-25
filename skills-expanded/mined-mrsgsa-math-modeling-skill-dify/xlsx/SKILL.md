---
name: xlsx
description: 读取、创建、修改和验证 XLSX，支持模板保留、公式重算和错误检查。
---

# Excel 工具

许可：专有；完整条款见 `LICENSE.txt`。

## 原则

- 输入表格只读，输出写入 `PROJECT_ROOT`。
- 普通结果汇总优先 CSV。
- 题目指定 XLSX、需保留公式、多工作表或模板结构时才使用 XLSX。
- 不覆盖题目原始附件和 Skill 文件。

## 读取与写入

```python
import pandas as pd

# 第一行就是数据时必须显式使用 header=None。
data = pd.read_excel("data/input.xlsx", sheet_name=0, header=None)
# 从题目数据合同、附件说明或独立原始计数填写；未知时保留 None 并先完成核验。
expected_rows = None
if expected_rows is None:
    raise ValueError("请先从当前题目建立 expected_rows，不能沿用其他题数值")
if len(data) != expected_rows:
    raise ValueError(f"行数异常: 实际 {len(data)}，预期 {expected_rows}")

def write_result_table(names, values, output_path):
    """names/values 必须来自真实运行结果，output_path 必须位于 PROJECT_ROOT。"""
    if len(names) != len(values):
        raise ValueError("方案名与目标值数量不一致")
    result = pd.DataFrame({"方案": names, "目标值": values})
    result.to_excel(output_path, index=False)
```

禁止依赖 `pandas.read_excel()` 默认的 `header=0` 猜测表头，否则第一行数据会被当成列名。未知表头结构或必须精确保留行时使用无隐式推断的读取工具：

```python
from scripts.read_rows import read_excel_rows

expected_rows = None  # 从当前题目合同填写
if expected_rows is None:
    raise ValueError("请先建立当前题目的预期行数")
rows = read_excel_rows(
    "data/input.xlsx",
    header=False,
    expected_rows=expected_rows,
)
# 与原始附件独立抽取的首末行哨兵核对，不能在 Skill 中硬编码某道题的数值。
expected_first_row = None
expected_last_row = None
if expected_first_row is None or expected_last_row is None:
    raise ValueError("请先记录当前附件的首末行哨兵")
if rows[0] != expected_first_row or rows[-1] != expected_last_row:
    raise ValueError("首行或末行哨兵与原始附件不一致")
```

读取后必须核对首行、末行、原始工作表有效行数和题目声明的记录数；行数不符时立即报错，不得静默继续建模。

使用模板时用 `openpyxl.load_workbook()` 打开，写入指定单元格后另存新文件。不要删除未知工作表、命名区域、公式或验证规则。

## 公式重算

`openpyxl` 不计算公式。修改含公式的工作簿后使用 LibreOffice 隔离重算：

```powershell
python scripts/recalc.py "<PROJECT_ROOT>/results/结果.xlsx" 60
```

工具会：

1. 使用唯一临时 LibreOffice 配置；
2. 把重算结果写入临时目录；
3. 检查常见 Excel 错误；
4. 仅在成功后原子替换目标文件；
5. 超时、失败或未生成输出时保留原文件。

DOCX 与 XLSX 共用的 OOXML/LibreOffice 基础代码位于 `../docx/scripts/office/`，本工具不再维护重复副本。

## 检查

- 公式引用和范围正确。
- 工作表名、列名、数据类型和单位正确。
- 已显式声明是否有表头，首行、末行和预期数据行数均已核对。
- 无 `#VALUE!`、`#DIV/0!`、`#REF!`、`#NAME?`、`#NULL!`、`#NUM!`、`#N/A`。
- 结果与代码终端输出和论文表格一致。
