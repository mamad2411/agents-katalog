---
name: spreadsheets
description: "Use this skill when a user requests to create, modify, analyze, visualize, or work with spreadsheet files (`.xlsx`, `.csv`, `.tsv`) with formulas, formatting, charts, tables, and data analysis. 处理表格：新建/编辑/分析/可视化 Excel 与 CSV。"
---

# Spreadsheets skill (Create • Edit • Analyze • Visualize)
Use this skill when you need to work with spreadsheets (.xlsx, .csv, .tsv) to do any of the following:
- Create or modify a workbook/sheet with proper formulas, cell/number formatting, and structured layout
- Read or analyze tabular data (filter, aggregate, pivot, compute metrics) directly in a sheet
- Visualize data with in-sheet charts/tables and sensible formatting
- Answer questions about an existing workbook's values, formulas, or structure

## Runtime & Tooling (READ FIRST)

All workbook authoring goes through **Python + openpyxl** in this skill's dedicated venv. Bootstrap once per session before any Python work:

```bash
# macOS / Linux — MUST use `source` (the script exports $SHEETS_PY back into your shell)
source ${SKILL_DIR}/bin/ensure-python.sh
"$SHEETS_PY" -c "import openpyxl; print(openpyxl.__version__)"
```

> **Windows**: run `${SKILL_DIR}\bin\ensure-python.cmd` instead; it prints `SHEETS_PY=<path>` on its last line — use that path for every subsequent Python command.

- The bootstrap builds a venv at `~/.spreadsheets-skill/venv` from the app-bundled Python 3.12 (or system python3 as fallback) and installs `openpyxl`, `Pillow`, `pandas`. First run downloads wheels (<1 min); later runs are instant.
- The skill directory may be read-only (packaged app). Never write into `${SKILL_DIR}`; never pip-install into the bundled runtime. All generated files go to the session working directory.
- Prefer ONE executable builder script (e.g. `build_workbook.py`) in the working directory and patch/rerun it, instead of piping many heredoc one-liners. Small read/inspect checks may be inline `-c` commands.
- Use the TodoWrite tool to plan complex multi-sheet workbook builds.

### Required reading before you start
- `API_QUICK_START.md`: REQUIRED — openpyxl quick reference (create/read/write, formatting, charts, tables, validation, conditional formatting) plus known gotchas. Read it entirely before your first build in a session.
- `style_guidelines.md`: REQUIRED for formatting requirements.
- `charts.md`: Read when creating or editing charts.

## ⚠️ openpyxl limitations that shape the workflow
1. **Formulas are NOT calculated by openpyxl.** Writing `=SUM(B2:B10)` stores the formula only; the computed value appears when the user opens the file in Excel/WPS. You cannot read a freshly written formula's result back.
   → Verify numbers by computing expected values in Python from the same inputs and comparing against what the formulas SHOULD produce (see Verification Rules).
2. **Never save a workbook opened with `data_only=True`.** That permanently strips all formulas, keeping only cached values. Open with `data_only=True` strictly for *reading* cached results of an existing file, in a separate load.
3. **`insert_rows`/`delete_rows` do not update formula references, chart ranges, or conditional-formatting ranges.** After structural edits, re-check and fix every formula/range that pointed at or beyond the edited area.
4. **No rendering.** openpyxl cannot screenshot a sheet. If LibreOffice (`soffice`) happens to be installed, you MAY convert to PDF for a visual check (see Verification Rules); otherwise rely on structural verification — do not claim visual verification you didn't perform.
5. Threaded comments are unsupported; use classic cell comments (`openpyxl.comments.Comment`).

## Final Response
- Include a short user-visible summary and standalone Markdown link(s) only to final `.xlsx` artifact(s), one per line: `[营收模型.xlsx](/absolute/path/to/营收模型.xlsx)`.
- Do not mention or link builder scripts, intermediates, or QA outputs unless requested.
- Communicate in the user's language (Chinese for this app's users) and plain words — no jargon dumps.

## Domain Requirements
You must read these domain rules when the request clearly relates to the domain, but do not load domain guidance for unrelated tasks unless asked:
- Finance and investment banking: `domain_guidance/financial_models.md`
- Corporate finance and FP&A: `domain_guidance/corporate_finance_fpa.md`
- Healthcare: `domain_guidance/healthcare.md`
- Marketing and advertising: `domain_guidance/marketing_advertising.md`
- Scientific research: `domain_guidance/scientific_research.md`

Instruction precedence is as follows: user request > reference/template > domain/formatting defaults

## Making edits on a spreadsheet or using an uploaded reference or template
- Before modifying: ALWAYS study and match the existing format, style and conventions. Load the workbook and inspect the relevant cells' values, formulas, number formats, fills, fonts, borders, merges, and column widths first (two loads: normal for formulas, `data_only=True` for cached values — save only the normal one).
- For visual fix requests, start with the smallest plausible local change. Do not apply sheet-wide autofit, wrapping, or restyling unless requested.
- Ensure existing formulas, layouts, structures, and patterns stay consistent. For example, if asked to add another column or row to a table and there is conditional formatting applied to the whole table, extend it to the new column or rows as well.
- Keep edits targeted unless a broader change is clearly necessary. Exception: dependencies — e.g. a chart based on a table's range must be updated when rows are added.
- Never overwrite formatting for spreadsheets with established formats, unless requested or to extend an added range.

## Importing or extracting data from screenshots or reference images
- When a reference image or screenshot is provided, use appropriate data formats (e.g. number/date formats) based on the workbook topic, audience and purpose instead of trying to recreate the rendered format with just text. Preserve numeric/date usability even when the screenshot shows locale-specific punctuation or currency symbols.
- Use formulas when appropriate and correct: For screenshot recreation, do not bulk-write numeric tables as all static values until you have separated any clearly formula-derived ranges; test adjacent numeric rows/columns for exact repeated relationships such as sums, differences, products, ratios, or constant multiples, then keep inputs hardcoded and write derived ranges as formulas.
- Match visible styling, but do not infer intentional formatting from ambiguous image artifacts such as zoom, antialiasing, or compression. Infer font weight only from relative contrast or clear semantics; if all visible text has the same apparent weight, use normal weight.

## Handling queries and questions
- The user may ask questions about the sheet instead of requesting an edit. Answer from the workbook's contents (values via `data_only=True`, formulas via a normal load) rather than making an edit the user didn't intend.

## Error Recovery
On first Python/openpyxl error:
1. Read the traceback.
2. Check `API_QUICK_START.md` gotchas; if it's an API-shape question, inspect the object with `help()`/`dir()` in a quick `-c` snippet.
3. Retry with a minimal patch to the builder script (not a full rewrite).
4. Continue from the existing builder + saved state.

Do not loop indefinitely on similar failures.

## Formula Rules
- Place assumptions and raw data in dedicated cells or clearly delineated input ranges, following the reference workbook's organization when one is provided.
- Derived values must be formulas (not hardcoded) and legible.
- Keep calculations formula driven, and prefer consistent formula patterns across a range where possible for readability. For example, formulas should be consistent across all projection periods.
- Use absolute/relative references correctly for fill/copy behavior.
- Use references instead of hardcoded or magic numbers inside formulas e.g. Use `=A5*(1+$A$6)` instead of `=A5*1.05`
- Formulas should be simple, legible and **easily auditable**. Use helper cells for intermediate values rather than performing complex calculations in a single cell. Users should be able to trace the model from inputs to outputs easily.
- No hardcoded numbers inside calculation areas unless explicitly allowed. Always ensure color formatting conventions are properly applied.
- For any complex formulas or important assumptions, add cell comments to explain.
- Always reference cells on other sheets as `='Sheet Name'!A1`, wrapping the sheet name in single quotes every time since quotes are required for any spaces or special characters.
- Stick to widely supported Excel functions. Dynamic-array functions (`FILTER`, `UNIQUE`, `SORT`, `SEQUENCE`, `XLOOKUP`) require recent Excel; prefer classic equivalents (`INDEX`/`MATCH`, `SUMIFS`, `IFERROR`) unless the user confirms a modern Excel.
- Avoid full-column references such as `A:A` or `Sheet!B:B` inside `COUNTIFS`, `SUMIFS`, `INDEX`, and lookups. Prefer bounded ranges sized to the table, e.g. `$A$6:$A$205`.

### Ensure formulas are correct
- Checklist: all cell references are correct, no off-by-one errors in ranges, edge cases (zero values, negative numbers, empty cells) are handled, no unintended circular references, every sheet referenced by a formula exists.

## Data Formatting Rules
- Store numbers, percentages, currency, and dates as typed spreadsheet values, not preformatted strings. Use text only for true identifiers such as ZIP codes, account IDs, SKUs, or labels.
- Use Excel-invariant number/date format codes, not locale-specific display strings. Examples include `#,##0`, `#,##0.0`, `0.0%`, `0.00%`, `"$"#,##0`, `"¥"#,##0.00`, `yyyy-mm-dd`, `mmm yyyy` but choose the format that best fits the data.
- Percentages: When not specified or no reference is provided, use 1 decimal for most internal/analytical cells, 0 decimals for user-facing/dashboard outputs, and 2 decimals where small differences in rates matter.
- Do not swap `.` and `,` in format codes to mimic locale separators; separators are controlled by the viewer's locale. Use `0.0%`, not `0,0%`, and `#,##0`, not `#.##0`.
- Choose the appropriate format for readability. Match precision to meaning: counts use `#,##0`; rates usually use `0.0%` or `0.00%`; currency uses whole units unless cents matter.

## Quality Guidelines
- Build correct, readable workbooks for the intended audience with clear structure, consistent formatting, reliable formulas, and useful outputs. Keep them as simple as practical.
- Set explicit column widths sized to content; cap oversized column widths and row heights.
- Make workbooks easy for another person to update, trace, and audit without the original author.

## Completion Criteria
Complete only when:
- Workbook content is populated and formulas are structurally sound (references resolve, ranges sized correctly).
- Python-side check values match what the key formulas should produce.
- `.xlsx` saved into the session working directory (or the user-specified location) with a descriptive filename.
- Structural verification passed (see below) — and, when a visual pass was possible, layout is organized, legible, nothing important clipped.

## Verification Rules
Before the final response, verify values/formulas and (when possible) visual quality.

1. **Structural read-back** — reload the saved file and check key ranges:
```python
from openpyxl import load_workbook
wb = load_workbook("output.xlsx")          # formulas view
for row in wb["Dashboard"]["A1:H20"]:
    for c in row:
        if c.value is not None:
            print(c.coordinate, repr(c.value), c.number_format)
```

2. **Reference audit** — every sheet name used in formulas exists; ranges match table sizes (no off-by-one at the last row); merged ranges and conditional-formatting/chart ranges still match after any structural edit.

3. **Numeric cross-check** — compute the expected results of key formulas in Python from the same input data (pandas/pure Python) and confirm the formula logic produces those numbers. This substitutes for recalculation, which openpyxl cannot do.

4. **Optional visual pass** — only if LibreOffice is available (`command -v soffice` or the macOS app path `/Applications/LibreOffice.app/Contents/MacOS/soffice`):
```bash
soffice --headless --convert-to pdf --outdir /tmp/sheet-preview output.xlsx
```
Then Read the PDF to check layout, clipping, and chart rendering. If soffice is absent, skip silently — do not install anything for this, and do not claim a visual check happened.

5. Keep verification compact: inspect key ranges, not entire sheets; avoid huge dumps.

6. Finalize immediately after successful save + verification. Do not export extra `.xlsx` variants unless asked.

## Citation Requirements
### Cite sources inside the spreadsheet
- Use plain-text URLs in spreadsheet cells.
- For financial models, cite model-input sources in cell comments.
- For researched row-wise data tables, include source URLs in a dedicated source column.

## Cell Comments
- Use classic cell comments: `ws["E2"].comment = Comment("Source: <website>", "Claude")`. Set the author to the user's display name if known from context, else `Claude`.

## Source, PDF, and Attachment Processing
- Keep source notes compact: record file name, section/table label, and enough context to audit the number. Do not paste large PDF excerpts into the workbook unless requested.
- The venv has `pandas` for tabular wrangling and `Pillow` for image checks. For PDF/DOCX extraction, add what you need to the venv on demand (`"$SHEETS_PY" -m pip install pypdf python-docx`) — never into the bundled runtime.
- Read CSV/TSV with pandas, clean/aggregate there, then write final data into the workbook with openpyxl (values or formulas per the Formula Rules).
