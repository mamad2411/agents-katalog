---
name: xlsx
description: "创建、读取、编辑电子表格文件（.xlsx/.xlsm/.csv/.tsv）。适用于任何需要生成或操作表格/电子表格的场景。不适用于 Word 文档、PDF、HTML 报告或不涉及表格文件的纯数据库操作。"
---

# xlsx

## Step 1（必做，最先执行）：目录变量与环境检查

```bash
# 技能目录（本 SKILL.md 所在目录）
export XLSX_SKILL_DIR="<本 SKILL.md 所在目录的绝对路径>"
# 工作区根目录：当前任务工作区或仓库根目录，不得等于技能目录
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$PWD}"

# 环境预检：解析工具位置；PATH 修正值以 PATH_FIX=<目录> 单行输出到 stdout，这里解析后拼接（不经 eval）
ENV_FIX="$(sh "$XLSX_SKILL_DIR/scripts/check_environment.sh")" && case "$ENV_FIX" in PATH_FIX=?*) PATH="${ENV_FIX#PATH_FIX=}:$PATH"; export PATH ;; esac

# 项目目录（本次任务的全部中间产物）：xlsx-<name>-<日期>-<uuid8>
export PROJECT_PATH="$(python3 "$XLSX_SKILL_DIR/scripts/project_manager.py" init <project_name> \
  --dir "$WORKSPACE_ROOT/.dumate" | sed -n 's/^Project created: //p')"
```

- 预检未输出「0 个失败」时停止任务，按脚本打印的安装命令装完再重跑；标为`[可选]`的可以继续，但需在最终回复中说明（缺 LibreOffice 时含公式文件验证返回 `partial`）。拼进 `PATH` 的修正值要在同一 shell 会话里保持有效，换会话就重跑预检。
- 脚本一律写成 `python3 "$XLSX_SKILL_DIR/scripts/xxx.py"`，不要用相对路径（当前工作目录不是技能目录）。
- 文件全部写在 `$PROJECT_PATH` 内：`sources/` 放源文件，`working/` 放可编辑副本，`helpers/` 放辅助脚本；下载资源、草稿、失败输出、验证报告和日志一律保留，只把最终交付文件复制到用户指定路径。
- 预检脚本按**当前 shell** 选，不看操作系统：bash / sh / zsh（含 Windows 上的 Git Bash、MSYS2、WSL）用 `check_environment.sh`；PowerShell 用 `$fix = & "$env:XLSX_SKILL_DIR\scripts\check_environment.ps1"`，当 `$fix` 以 `PATH_FIX=` 开头时执行 `$env:Path = $fix.Substring(9) + ';' + $env:Path`（不要用 Invoke-Expression），并把 `python3` 换成 `python`、`export X="Y"` 换成 `$env:X="Y"`。

## 必须遵守

- 创建新文件前阅读 `$XLSX_SKILL_DIR/references/design.md`；修改已有文件、或按用户提供的模板新建文件时，一律以原模板的格式和约定为准。
- 除非用户另有指示或原模板已有约定，交付物统一使用专业字体（如 Arial、Times New Roman），完整字体/配色/行高等风格以 `$XLSX_SKILL_DIR/references/design.md` 为准。
- **以模板为基准（存在模板时强制）**：当用户提供模板文件，或要求“依据模板/按模板格式/参照示例”生成时，必须先 `shutil.copy2(<模板>, "$PROJECT_PATH/working/output.xlsx")`，再在副本上就地追加或改写数据行；禁止用 `openpyxl.Workbook()` 新建工作簿后手工重建样式。确有必要新建时，逐单元格执行 `new_cell._style = copy(tpl_cell._style)`（`from copy import copy`），不得用 `Font(...)`/`PatternFill(...)`/`Border(...)` 按巡检结果重写样式——手工巡检必然漏项。
- 模板样式的继承范围必须覆盖：`font`（含 `name`、`sz`、`b`、`i`、**`color`**）、**`fill`**（`patternType`、`fgColor`）、**`border`** 四边、`alignment`（含 `wrap_text`）、`number_format`，以及 `column_dimensions[*].width`、`row_dimensions[*].height`、合并单元格、冻结窗格。新增数据行以模板最后一个数据行（示例行）为样式来源逐行继承；模板示例行属于真实数据时保留，否则由首条真实数据覆盖写入。
- 巡检模板时禁止只打印 `font.name/size/bold`：必须同时输出 `cell.font.color.rgb`、`cell.fill.patternType`、`cell.fill.fgColor.rgb`、`cell.border.{left,right,top,bottom}.style`。交付前逐单元格比对模板与产物的上述全部属性，任一项不一致即为交付错误，必须修复后重新比对。
- 对二维数据区使用同一份有序 schema 生成表头、数据行和 `validation.json`，禁止分别维护。空表头、重复/错序字段、表头外数据列均须修复，禁止自动猜测并移动数据。
- 学号、编号、邮编、代码、固定宽度或带前导零的内容属于文本。用 `column_rules` 声明 `type: text`，按需设置 `width`、`pattern`；读取、清洗、写入全程保持字符串并设置 `@` 格式。不得先转为数值再补零。
- 合计、比率、差值等可更新计算使用 Excel 公式，不在 Python 中硬编码结果。交付时不得含 `#REF!`、`#DIV/0!`、`#VALUE!`、`#N/A`、`#NAME?` 或循环引用。
- 每次创建或修改 `helpers/` 下的 Python 脚本后，先对该脚本的实际路径运行 `python3 -m py_compile <helper_script_path>`；语法检查通过后才能执行，失败时按报错文件和行号修复并重新检查。
- 动态创建或修改 `validation.json` 后，先对其实际路径运行 `python3 -m json.tool <validation_spec_path> >/dev/null`；解析失败时先修复配置，不进入工作簿生成或验证。

## Step 2（Step 1 完成后执行）：工作流

1. 在 `$PROJECT_PATH/sources/` 保留源文件，在 `$PROJECT_PATH/working/` 中创建可编辑副本。
2. 存在模板时，`$PROJECT_PATH/working/output.<xlsx|xlsm>` 必须是模板的 `shutil.copy2` 副本而非新建工作簿，后续写入全部在该副本上进行；无模板时才新建。用 pandas 分析数据，用 openpyxl 处理公式、格式、图表和图片；`.xlsm` 使用 `keep_vba=True`。
3. 从同一 schema 写入表头和数据，并在同目录生成 `validation.json`。
4. 保存后只运行一个验证命令：

```bash
python3 "$XLSX_SKILL_DIR/scripts/validate.py" \
  "$PROJECT_PATH/working/output.<xlsx|xlsm>" --work-dir "$PROJECT_PATH"
```

5. 根据总状态处理：
   - `success`：所有适用检查通过，可以交付。
   - `errors_found`：文件存在公式、结构或布局缺陷；修复后重跑。
   - `partial`：动态引擎缺失、超时或结果不确定；不能宣称完整通过，必要时在目标 Excel/LibreOffice 环境复核。
   - `error`：验证器或配置失败；先修复验证流程。
6. 仅在 `success`，或已明确披露并接受 `partial` 时，将最终文件从持久工作区复制到用户指定路径或当前工作区：

```python
import os
import shutil

working_file = os.path.join(os.environ["PROJECT_PATH"], "working", "output.xlsx")
final_path = os.path.join(os.environ["WORKSPACE_ROOT"], "output.xlsx")  # 或用户指定的绝对路径
shutil.copy2(working_file, final_path)
```

动态重算使用隔离副本和隔离的 LibreOffice 配置，保留全部输入、输出和配置产物，不覆盖源文件。静态公式、结构和布局检查不因动态重算失败而停止。
## Schema 与统一配置

`validation.json` 可同时声明表结构、文本保真规则、布局保护区和重算选项：

```json
{
  "tables": [
    {
      "name": "records",
      "sheet": "Data",
      "header_row": 1,
      "data_start_row": 2,
      "start_column": "A",
      "expected_headers": ["ID", "Name", "Score"],
      "column_rules": {
        "ID": {"type": "text", "width": 6, "pattern": "\\d{6}"},
        "Score": {"type": "text", "width": 2, "pattern": "\\d{2}"}
      }
    }
  ],
  "gap_columns": 1,
  "gap_rows": 2,
  "sheets": [
    {"sheet": "Data", "protected_ranges": ["A1:C20"]}
  ],
  "formula_validation": {"engine": "auto", "timeout_seconds": 90}
}
```

生成数据时：

- `expected_headers` 是唯一字段顺序；数据行按该列表取值，未知字段立即报错。
- `column_rules` 的文本值必须是 Python `str`；写入后将对应单元格 `number_format` 设为 `"@"`。仅给数值设置 `@` 不会恢复前导零。
- `width` 检查字符数，`pattern` 使用完整正则匹配。正常业务空值允许存在。
- `text_type_mismatch`、`fixed_width_mismatch`、`pattern_mismatch` 均为交付错误。
- pandas 读取 Excel/CSV 时为文本字段指定 `dtype="string"`，不要读取成数值后再修补。

使用 `python3 "$XLSX_SKILL_DIR/scripts/validate.py" --print-example-spec` 查看完整配置示例。

## 修改已有文件

始终编辑工作区中的持久副本：

```python
import os
import shutil
from openpyxl import load_workbook

working_file = os.path.join(os.environ["PROJECT_PATH"], "working", "input.xlsx")
shutil.copy2(src, working_file)
wb = load_workbook(
    working_file,
    keep_vba=working_file.lower().endswith(".xlsm"),
)
# 按原模板修改，并同步更新受影响区域的 schema
wb.save(working_file)
```

不要用 `data_only=True` 打开后再保存，否则公式会被替换为缓存值。

## 图表与图片

图表和图片是浮动对象，不会挤开单元格。使用 `TwoCellAnchor` 绑定起止单元格并预留空列/空行；不要只传入 `"E5"` 等起点锚点。

`max_column/max_row` 为 1 基，`AnchorMarker.col/row` 为 0 基。数据右侧起点应为 `last_col + GAP_COLS`：

```python
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, TwoCellAnchor

last_col = sheet.max_column
GAP_COLS, GAP_ROWS = 2, 2
DRAWING_W, DRAWING_H = 8, 15
start_col0 = last_col + GAP_COLS

def place(drawing, index, kind):
    top0 = index * (DRAWING_H + GAP_ROWS)
    drawing.anchor = TwoCellAnchor(
        _from=AnchorMarker(col=start_col0, row=top0),
        to=AnchorMarker(col=start_col0 + DRAWING_W, row=top0 + DRAWING_H),
    )
    (sheet.add_chart if kind == "chart" else sheet.add_image)(drawing)
```

在 `protected_ranges` 中声明不可覆盖的内容区域。图表应位于报告有效画布内并沿连续阅读路径排列，不得推到远端空白列；缺失值不得按 0 绘制，系列名称不得保留默认文本。统一验证会检查图表/图片相互重叠及覆盖内容，并兼容 `TwoCellAnchor`、`OneCellAnchor`、`AbsoluteAnchor` 和字符串锚点。

数据标签默认关闭；需要时仅显示数值，避免同时显示系列名、类别名和值。密集图表优先不加标签或仅标关键点。

## 财务模型

仅在构建财务模型时应用，原模板或用户要求优先：

- 年份按文本显示；货币表头注明单位；百分比用 `0.0%`；倍数用 `0.0x`；负数用括号；零值可用数字格式显示为 `-`。
- 假设值放在独立单元格，公式引用假设而非硬编码常数；预测期公式保持一致，并测试零值、负数和循环引用。
- 硬编码数据添加来源批注：`来源: [系统/文档], [日期], [具体参考], [URL（如有）]`。

## 资源

- `$XLSX_SKILL_DIR/references/design.md`：新工作簿的商务设计规范。
- `$XLSX_SKILL_DIR/scripts/project_manager.py`：初始化、检查和验证持久项目工作区。
- `$XLSX_SKILL_DIR/scripts/validate.py`：唯一对外验证入口。

