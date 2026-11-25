---
name: text-to-excel
description: 将结构化文本内容生成为Excel表格(.xlsx)的工具。支持解析用户提供的各种结构化文本（表格、列表、键值对、CSV、Markdown表格、JSON等），自动识别表头和数据行，生成格式规整的Excel文件。支持多sheet、合并单元格、样式设置、冻结窗格、自动筛选、条件格式、数据验证、图表生成等全部功能。当用户提到以下场景时触发：(1) 需要将文本/数据/内容转换为Excel/表格/xlsx文件 (2) 需要生成Excel表格 (3) 需要创建电子表格 (4) 提供了结构化数据并要求输出为Excel (5) 要求整理数据到表格中 (6) 需要把信息做成表格导出。关键词：Excel、表格、xlsx、电子表格、导出表格、生成表格、做成表格、转成表格、整理成表格。
---

# Text-to-Excel

将结构化文本转换为格式规整的Excel文件。

## Workflow

### Step 1: Parse User Input

Analyze user-provided structured text. Supported input formats:
- Markdown tables (`| col1 | col2 |`)
- Plaintext tables (tab/space-separated)
- CSV/TSV data
- Lists (bulleted, numbered)
- Key-value pairs
- JSON/dict-like structures
- Free-form text with identifiable tabular structure
- Descriptions of desired table content

Identify: headers, data rows, data types per column, and any special formatting requests.

### Step 2: Ask for Output Path

Ask the user for the save path. Suggest a reasonable default filename based on the content (e.g. `~/Desktop/sales_data.xlsx`).

### Step 3: Build JSON Config

Construct a JSON config object following the schema in [references/config_schema.md](references/config_schema.md).

Minimal example:
```json
{
  "sheets": [{
    "name": "Sheet1",
    "headers": ["Name", "Age", "City"],
    "data": [
      ["Alice", 30, "Beijing"],
      ["Bob", 25, "Shanghai"]
    ]
  }]
}
```

Full-featured example with styles, charts, and validation:
```json
{
  "sheets": [{
    "name": "Sales",
    "title_row": {"text": "Q1 Sales Report", "style": {"font": {"bold": true, "size": 16}}},
    "headers": ["Month", "Revenue", "Growth"],
    "data": [
      ["January", 50000, 0.12],
      ["February", 62000, 0.24],
      ["March", 58000, 0.16]
    ],
    "column_types": ["text", "currency_cny", "percent"],
    "freeze_pane": "A2",
    "auto_filter": true,
    "charts": [{
      "type": "bar",
      "title": "Monthly Revenue",
      "x_column": 1,
      "y_columns": [2],
      "position": "E2"
    }],
    "conditional_formats": [{
      "type": "color_scale",
      "range": "B2:B4"
    }]
  }]
}
```

### Step 4: Generate Excel

1. Write the JSON config to a temp file
2. Run: `python3 scripts/generate_excel.py <config.json> <output_path>`
3. Verify the file was created
4. Report success with the file path

## Style Defaults

The script applies professional defaults automatically:
- **Headers**: Blue background (#4472C4), white bold text, centered
- **Data rows**: Alternating gray/white bands, thin borders
- **Column widths**: Auto-calculated based on content length
- **Title row** (optional): Large bold text, merged across all columns

Override any default by specifying `header_style`, `data_style`, or per-cell styles in the config.

## Advanced Features

- **Multi-sheet**: Add multiple objects to the `sheets` array
- **Merge cells**: Use `merge_cells` with range strings or row/col objects
- **Freeze pane**: Set `freeze_pane` to e.g. `"A2"` to freeze header row
- **Auto-filter**: Set `auto_filter: true` to enable dropdown filters
- **Charts**: Bar, line, pie, area, scatter charts — see [references/config_schema.md](references/config_schema.md)
- **Data validation**: Dropdown lists, numeric ranges, date ranges, text length limits
- **Conditional formatting**: Cell-based rules, color scales, data bars
- **Number formats**: Predefined (`percent`, `currency_cny`, `currency_usd`, `date`) or custom Excel format strings
- **Print settings**: Orientation, paper size, fit-to-page

See full schema: [references/config_schema.md](references/config_schema.md)
