---
name: xlsx
description: Create, read, edit Excel .xlsx workbooks and CSVs.
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [excel, spreadsheet, xlsx, csv, openpyxl, productivity]
    category: productivity
    related_skills: [docx, pdf, powerpoint]
---

# Xlsx 技能

该技能可使用 Python 和 openpyxl 处理 Excel .xlsx 格式的工作簿：创建包含公式与图表的多工作表格式化工作簿，查看或导出现有文件内容，编辑单元格及其结构，以及实现与 CSV 格式之间的相互转换。所有辅助脚本均为基于 argparse 的命令行工具，它们会以 JSON 格式输出结果，并采用显式的 UTF-8 输入输出方式。

## 适用场景

- **创建 .xlsx 报告**：支持多工作表、数字格式设置、样式应用、合并单元格、冻结窗格、自动筛选、条件格式、图表展示、数据验证下拉列表、原生 Excel 表格、定义名称、超链接、单元格备注以及工作表保护功能。
- **读取工作簿**：可查看工作表清单，将数据导出为 JSON 或 CSV 格式，区分公式计算结果与缓存值，同时显示备注、定义名称及表格信息。
- **编辑现有文件**：可设置单元格内容、追加行、插入/删除行或列（通过 `xlsx_restructure.py` 脚本实现基于引用关系的操作），还可复制/重命名工作表、表格、定义名称、备注及保护设置。
- **通过 LibreOffice 在后台重新计算公式**（使用 `xlsx_recalc.py` 脚本）。
- **支持带类型推断功能的 CSV 格式互操作，以及非 UTF-8 编码的处理**。
- **不支持旧的 .xls 二进制格式**（需先使用 LibreOffice 进行转换：`soffice --headless --convert-to xlsx old.xls`）。

## 前提条件

- 安装了 Python 3.10 及以上版本，并已安装 `openpyxl` 库（可通过 `pip install openpyxl` 安装）。除此之外无需其他第三方软件，所有功能均基于标准库实现。
- 可选：如需在后台重新计算公式或转换文件格式，可安装 LibreOffice（命令为 `soffice`）。

## 运行方式

请从该技能对应的 `scripts/` 目录中使用 `terminal` 工具来运行各类辅助脚本（所有脚本均支持 `--help` 参数）。

```bash
python scripts/xlsx_create.py spec.json report.xlsx   # build from JSON spec
python scripts/xlsx_read.py report.xlsx --sheets      # inventory
python scripts/xlsx_read.py report.xlsx --json --sheet Data
python scripts/xlsx_read.py report.xlsx --formulas
python scripts/xlsx_edit.py report.xlsx --sheet Data --set B2=42 --recalc
python scripts/xlsx_restructure.py report.xlsx --sheet Data --insert-rows 3:2
python scripts/xlsx_recalc.py report.xlsx
python scripts/csv_to_xlsx.py data.csv out.xlsx --encoding utf-8
python scripts/xlsx_to_csv.py report.xlsx out.csv --sheet Data
```

使用 `write_file` 函数编写 JSON 规范文件，或通过 `read_file` 函数、亦或是直接从标准输出中查看脚本生成的 JSON 结果。

## 快速参考

| Task | Command |
|---|---|
| Create workbook from spec | `xlsx_create.py spec.json out.xlsx` |
| Sheet names + dimensions | `xlsx_read.py f.xlsx --sheets` |
| Dump sheet as JSON | `xlsx_read.py f.xlsx --json --sheet S` |
| Dump sheet as CSV | `xlsx_read.py f.xlsx --csv --out d.csv` |
| List formulas + cached values | `xlsx_read.py f.xlsx --formulas` |
| Set a cell / formula | `xlsx_edit.py f.xlsx --set "A1==SUM(B:B)"` |
| Append a row | `xlsx_edit.py f.xlsx --append '[1,"x",true]'` |
| Insert 2 rows, refs NOT shifted | `xlsx_edit.py f.xlsx --insert-rows 3:2` |
| Insert 2 rows, refs shifted | `xlsx_restructure.py f.xlsx --insert-rows 3:2` |
| Delete a column, refs shifted | `xlsx_restructure.py f.xlsx --delete-cols B` |
| Create a native table | `xlsx_edit.py f.xlsx --add-table Sales:A1:C9` |
| Append inside a table | `--table-append 'Sales=["West",5]'` |
| List tables | `xlsx_edit.py f.xlsx --list-tables` |
| Defined names | `--define-name "Rates='Data'!$B$2:$B$9"` / `--delete-name Rates` / `xlsx_read.py f.xlsx --names` |
| Hyperlink | `--hyperlink "A1=https://example.com|Docs"` |
| Cell note | `--note "B2=Check this|Reviewer"`; read via `xlsx_read.py f.xlsx --notes` |
| Protect sheet (see Pitfalls) | `--protect your-password --unlock B2:B9` |
| Recalculate via LibreOffice | `xlsx_recalc.py f.xlsx` |
| Copy / rename sheet | `--copy-sheet Src:New --rename-sheet Old:New` |
| Force recalc on open | `xlsx_edit.py f.xlsx --recalc` |
| CSV -> styled xlsx | `csv_to_xlsx.py in.csv out.xlsx` |
| xlsx -> CSV | `xlsx_to_csv.py f.xlsx out.csv --encoding utf-8` |

## 操作步骤

1. **创建**：编写 JSON 规范文件（其结构可在 `xlsx_create.py --help` 及其文档字符串中查看）。每张工作表支持以下功能：`rows`（标量值或带样式的单元格对象）、稀疏的 `cells` 覆盖设置、`column_widths`、`row_heights`、`merges`、`freeze_panes`、`autofilter`、`conditional_formats`（包含 cell_is 规则与颜色映射表）、`charts`（基于单元格区域的柱状图/折线图/饼图）、`validations`（列表下拉验证）、`tables`（带有样式名称的 Excel 原生表格）以及 `protection`。在工作簿级别，`defined_names` 用于将名称映射为引用。单元格对象还支持 `hyperlink` 和 `note` 属性。数值类型：JSON 格式的数字/布尔值可直接传递；日期则需使用 `{"value": "2026-01-31", "type": "date"}` 的格式。数字格式遵循 Excel 格式字符串规则：货币格式为 `"$#,##0.00"`，百分比格式为 `"0.0%"`，日期格式为 `"yyyy-mm-dd"`。

2. **公式设置**：可在规范文件中通过 `"formula": "SUM(B2:B9)"` 的形式进行设置，或在编辑器中使用 `--set "C1==SUM(A:A)"` 命令。在编写公式时，可添加 `"full_calc_on_load": true`（用于规范文件）或 `--recalc`（用于编辑器）；这样即可设置工作簿的 `fullCalcOnLoad` 标志，促使 Excel/LibreOffice 在打开文件时重新计算所有内容。需注意，openpyxl 本身永远不会执行公式计算。
3. **读取**：使用 `--sheets` 可获取工作表信息（名称、尺寸、合并区域、图表数量、表格、保护设置以及定义名称）；使用 `--json`/`--csv` 可读取数据；使用 `--formulas` 可将每条公式字符串与其缓存结果对应起来；使用 `--notes` 可查看单元格注释；使用 `--names` 可获取定义名称。只有当文件是由真正的电子表格应用程序最后保存的，才会存在缓存结果；而由 openpyxl 直接生成的文件则在此处返回 `null` 值。若需无界面地计算结果，可运行 `xlsx_recalc.py file.xlsx`（该工具基于 LibreOffice，若未安装 soffice，则会输出 `{"recalculated": false, ...}` 并以代码 0 结束执行），之后再使用 `--data-only` 参数重新加载数据。

4. **编辑**：`xlsx_edit.py` 会先执行重命名/复制操作，接着进行行/列结构调整，最后处理 `--set`/`--append` 指令。除非指定了 `--out` 参数，否则它会在原文件上进行直接编辑——若需要保留原始文件，请先对其进行复制。

5. **重构**：对于包含公式、合并区域、表格或筛选器的工表，应使用 `xlsx_restructure.py` 而非 `xlsx_edit.py`。该工具会重写所有工作表中的公式引用（包括绝对引用 `$`、范围引用以及跨工作表引用），同时调整合并区域、自动筛选、冻结窗格、数据验证与条件格式应用区域、表格引用、定义名称以及行/列尺寸，随后会生成一份包含 `not_shifted` 列表的 JSON 报告。相关规则与限制详见 `references/restructuring.md` 文件。
6. **CSV格式互操作**：`csv_to_xlsx.py`能够自动识别每单元格中的整数、浮点数、布尔值及ISO日期格式，并对表头行进行格式设置；而`xlsx_to_csv.py`则会将ISO日期格式写入文件，空单元格则显示为空字符串。这两款工具均默认使用UTF-8编码，同时也支持通过`--encoding`参数指定其他编码方式（例如，使用`utf-8-sig`可生成适合Excel识别的BOM标记，使用`cp1252`则适用于旧版Windows系统的导出）。

## 转换为PDF格式

LibreOffice可在后台模式下完成转换（同样适用于单工作表的CSV导出）：

```bash
soffice --headless --convert-to pdf report.xlsx --outdir out/
soffice --headless --convert-to csv report.xlsx --outdir out/  # 1st sheet only
```

只有第一个工作表会被导入 CSV 文件；对于其他工作表，请使用 `xlsx_to_csv.py --sheet NAME` 命令。如果系统中没有安装 `soffice`，则需要先安装 LibreOffice，或者将文件直接交给用户进行手动转换。

## 常见问题

- **openpyxl 无法计算公式**。只有通过 `load_workbook(path, data_only=True)` 才能获取公式结果，且前提是该文件之前已由 Excel/LibreOffice 保存过。否则将会返回 `None`。
- **`xlsx_edit.py` 的插入/删除操作不会调整引用位置**（这是 openpyxl 的原生行为）。建议使用 `xlsx_restructure.py`，它具备此功能——但即便如此，也无法移动图表锚点、图片或条件格式规则公式；相关说明可参见其 JSON 报告中的 `not_shifted` 列表以及 `references/restructuring.md` 文件。
- **工作表保护并非真正的安全措施**。`--protect` 选项仅设置标准的 xlsx 工作表保护哈希值，作用仅仅是向正常运行的应用程序发出“请勿编辑此文件”的提示而已。任何人都可以通过修改 ZIP 文件中的 XML 内容或在 LibreOffice 中取消保护来解除该限制。切勿依赖它来保障数据的保密性或完整性，因为它并不具备加密功能。
- **使用 `data_only=True` 后再保存会隐式丢弃所有公式**（系统会用缓存值替代公式）。除非有意如此，否则请勿保存以该模式加载的工作簿。
- **加载文件时会丢失图表/图片**：由于 openpyxl 不支持图表的往返处理，因此在对包含图表的工作簿进行编辑并保存后，图表将会被删除。建议在编辑完成后重新添加图表，或避免重新保存带有图表的文件。
- **CSV区域设置陷阱**：务必明确指定编码格式（脚本本身已会处理此操作），同时需注意欧洲地区的CSV文件通常使用`;`作为分隔符且小数点用逗号表示——此时应使用`--delimiter ';'`选项，并确保像`"12,5"`这样的字符串仍被识别为字符串。
- **日期即时间戳**：Excel会将日期存储为序列号，而openpyxl则返回`datetime`/`date`类型对象。此处导出的数据会以ISO格式的字符串呈现。
- 工作表名称长度不得超过31个字符，且不能包含`[ ] : * ? / \`等特殊字符。

## 验证方法

- 创建文件后，运行`xlsx_read.py out.xlsx --sheets`命令，检查工作表名称、尺寸、合并单元格范围以及图表数量是否与预期一致。
- 使用`--json`选项导出数据，并与原始数据值进行对比。
- 进行修改后，重新导出被修改的区域；如果使用了公式，需确认`--formulas`选项能正确列出这些公式，且已执行了`--recalc`命令。
- 使用`xlsx_restructure.py`处理文件后，先读取其生成的JSON报告，再分别运行`--formulas`和`--sheets`命令，确保引用和单元格范围均位于预期位置。
- 如需进行全面的可视化检查，可在LibreOffice中打开文件：执行`soffice --headless --convert-to pdf out.xlsx`，然后查看生成的PDF文件。
