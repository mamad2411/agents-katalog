---
name: excel-reader
description: Use when reading Excel files (.xlsx/.xlsm) to extract data. Triggers whenever user mentions Excel, xlsx, spreadsheets, or needs to extract/analyze tabular data. Outputs AI-friendly JSON with merge cell support and type inference.
---

# Excel Reader

读取 Excel 文件并输出结构化 JSON 格式，支持合并单元格、多 sheet、数据类型识别。

## 何时使用

- 需要读取 .xlsx 或 .xlsm 文件
- 需要提取 Excel 数据供 AI 分析
- 需要处理包含合并单元格的表格
- 需要读取特定 sheet 或全部 sheets

## 快速开始

```bash
# Bash/Linux/macOS
./scripts/excel-reader <excel_file> [sheet_name]

# PowerShell/Windows
./scripts/excel-reader.ps1 <excel_file> [sheet_name]
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `excel_file` | 是 | Excel 文件路径（.xlsx 或 .xlsm） |
| `sheet_name` | 否 | 指定读取的 sheet 名称，不指定则读取所有 |

## 输出格式

执行成功后，输出：
```
Success: <文件名>
Markdown: <缓存路径>/<文件名>.md
JSON: <缓存路径>/<文件名>.json
```

Markdown 文件包含格式化的表格，JSON 文件包含完整元数据（合并单元格信息、数据类型等）。

**缓存目录位置**：
- Linux: `~/.cache/excel-reader/` 或 `$XDG_CACHE_HOME/excel-reader/`
- macOS: `~/Library/Caches/excel-reader/`
- Windows: `%USERPROFILE%\.cache\excel-reader\`

**Markdown 示例**：
```markdown
# data.xlsx

## Sheet1

| 姓名 | 年龄 | 城市 |
| --- | --- | --- |
| 张三 | 25 | 北京 |
| 李四 | 30 | 上海 |
```

**JSON 结构**（包含完整元数据）：
```json
{
  "file": "/path/to/file.xlsx",
  "sheets": [
    {
      "name": "Sheet1",
      "data": [[...]],
      "dimensions": {"rows": 10, "columns": 5},
      "merged_cells": [...]
    }
  ]
}
```

## 功能特性

### 合并单元格支持

自动识别合并单元格：
- 左上角单元格包含实际值
- 其他合并区域单元格标记为 `type: "merged"` 且 `value: null`
- `merged_cells` 数组记录所有合并区域

### 数据类型识别

自动识别以下类型：
- `string` - 文本
- `number` - 数字（整数和浮点数）
- `boolean` - 布尔值
- `date` - 日期时间（转换为 ISO 8601 格式）
- `empty` - 空单元格
- `merged` - 合并区域的非主单元格

### 多 Sheet 支持

- 不指定 sheet_name 时读取所有 sheets
- 指定 sheet_name 时只读取指定 sheet
- Sheet 不存在时会列出可用的 sheet 名称

## 常见问题

### 文件不存在

```
Error: Excel file not found: /path/to/file.xlsx
```

检查文件路径是否正确。

### 不支持的格式

```
Error: Unsupported file format: .xls
```

只支持 `.xlsx` 和 `.xlsm` 格式，不支持旧版 `.xls`。

### Sheet 不存在

```
Error: Sheet 'Data' not found. Available sheets: Sheet1, Sheet2
```

使用列出的可用 sheet 名称。

## 依赖要求

- Python 3.12+
- openpyxl
- uv（用于依赖管理）

首次运行会自动初始化虚拟环境并安装依赖。

## 示例

```bash
# 读取所有 sheets
./scripts/excel-reader data.xlsx
# 输出:
# Success: data.xlsx
# Markdown: ~/.cache/excel-reader/data.md
# JSON: ~/.cache/excel-reader/data.json

# 读取指定 sheet
./scripts/excel-reader data.xlsx "销售数据"

# 查看生成的 Markdown
cat ~/.cache/excel-reader/data.md
```
