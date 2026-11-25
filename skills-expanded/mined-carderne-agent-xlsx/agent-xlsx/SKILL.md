---
name: agent-xlsx
description: Read and edit .xlsx files from the command line with JSON in/out. Use whenever a task involves inspecting, creating, or modifying Excel spreadsheets.
---

# agent-xlsx

A small CLI for reading and editing `.xlsx` files. Every read prints JSON;
every write accepts JSON. Worksheets are selected with `-w/--worksheet`
(name or 0-based index; defaults to the first sheet).

## Availability

Check whether the binary is already on PATH:

```bash
command -v agent-xlsx
```

If not, install it. The installer detects the platform, fetches the latest
GitHub release, and drops the binary at the chosen path.

**If this skill is available as local files:**

```bash
./install.sh                      # installs to this skill's directory
./install.sh ~/.local/bin         # or to somewhere on PATH
```

**If not (e.g. SKILL.md was copy-pasted without the script):**

```bash
curl -fsSL https://raw.githubusercontent.com/carderne/agent-xlsx/main/install.sh \
    | bash -s -- ~/.local/bin
```

Supported platforms: Apple Silicon macOS, x86_64 Linux, x86_64 Windows.

## General Excel principles

### Use formulas, not hardcoded values
Always write Excel formulas instead of computing values yourself and
writing the result. The spreadsheet should recalculate when source data
changes.

```bash
# WRONG: computing in your head / in code and writing a literal
agent-xlsx edit book.xlsx B10 5000

# RIGHT: let Excel do the calculation
agent-xlsx edit book.xlsx B10 '"=SUM(B2:B9)"'
```

This applies to all calculations — totals, percentages, ratios, growth
rates, averages, etc. Place assumptions (growth rates, margins, multiples)
in their own cells and reference them in formulas.

### Zero formula errors
Deliver files with zero Excel errors (`#REF!`, `#DIV/0!`, `#VALUE!`,
`#N/A`, `#NAME?`). After writing formulas, read them back to verify
references are correct. Common pitfalls: division by zero, invalid cell
references, wrong cross-sheet reference syntax (`Sheet1!A1`).

### Preserve existing templates
When modifying an existing file, study and match its existing format,
style, and conventions. Existing template conventions always override
default guidelines.

### Financial model conventions
Unless the user or existing template says otherwise:

- **Color coding**: blue text = hardcoded inputs, black = formulas,
  green = cross-sheet links, red = external links, yellow bg = key
  assumptions.
- **Number formats**: currency `#,##0`, negatives in parentheses `(123)`,
  percentages `0.0%`, multiples `0.0x`, zeros as `"-"`, years as plain
  text (not `2,024`). Always state units in headers (`Revenue ($mm)`).
- **Documentation**: comment or annotate hardcoded values with their
  source (e.g. "Source: Company 10-K, FY2024, Page 45").

## Command reference

```
agent-xlsx create       <file>
agent-xlsx list-sheets  <file>
agent-xlsx read         <file> <range>            [-w …] [--raw] [--pretty]
agent-xlsx edit         <file> <range> <values>   [-w …] [-o OUT] [--no-formula]
agent-xlsx insert       <file> <json>             [-w …] [-o OUT] [--no-formula]
agent-xlsx style        <file> <range> [flags]    [-w …] [-o OUT]
agent-xlsx resize-cols  <file> <colrange> <w>     [-w …] [-o OUT] [--auto]
agent-xlsx resize-rows  <file> <rowrange> <h>     [-w …] [-o OUT]
```

## Ranges

Plain A1 notation, one syntax everywhere:

| Form     | Meaning                                  |
| -------- | ---------------------------------------- |
| `A1`     | single cell                              |
| `A1:C10` | rectangle                                |
| `B:B`    | whole column (trimmed to used rows)      |
| `3:3`    | whole row (trimmed to used columns)      |
| `B:D`    | columns B through D                      |
| `3:10`   | rows 3 through 10                        |

## Reading

`read` always prints JSON. Shape follows the range:

- single cell → scalar
- 1D range    → flat array
- 2D range    → array of row arrays
- empty cell  → `null`
- formula cell with no cached value → the formula string (`"=SUM(A1:A2)"`)

`--raw` returns `{"value", "type", "formula"?}` per cell so you can see the
type tag (`s`, `n`, `b`, …) and any formula without a second query.

```bash
agent-xlsx read book.xlsx A1                 # → "Hello"
agent-xlsx read book.xlsx A1:C1              # → ["Hello", 10, 20]
agent-xlsx read book.xlsx A1:C2              # → [["Hello",10,20],[1,2,3]]
agent-xlsx read book.xlsx B:B                # → whole column B
agent-xlsx read book.xlsx A1 --raw           # → {"value":"Hello","type":"s"}
```

## Writing

Two styles. Use whichever fits the shape of the data:

**`edit <range> <values>`** — positional. Values must match range dims:

```bash
agent-xlsx edit book.xlsx A1 42                         # scalar
agent-xlsx edit book.xlsx A1:C1 '[1,2,3]'               # 1D row
agent-xlsx edit book.xlsx A1:A3 '[1,2,3]'               # 1D col
agent-xlsx edit book.xlsx A1:B2 '[[1,2],[3,4]]'         # 2D rect
agent-xlsx edit book.xlsx A1:Z100 0                     # broadcast fill
agent-xlsx edit book.xlsx A3 '"=SUM(A1:A2)"'            # formula
```

Strings starting with `=` are treated as formulas. Pass `--no-formula` to
write them as literal strings.

**`insert <json>`** — parallel dict form, handy for sparse writes:

```bash
agent-xlsx insert book.xlsx \
    '{"A1":"name","B1":"age","A2":"Alice","B2":30}'
```

## Styling

```bash
agent-xlsx style book.xlsx A1:D1 \
    --bold --font Arial --font-size 14 \
    --color '#FF0000' --bg '#FFEEDD' \
    --align center --valign middle \
    --number-format '#,##0.00'
```

Only flags you pass are applied; the rest are left alone. `--no-bold`,
`--no-italic`, `--no-underline` turn attributes off.

## Sizing

```bash
agent-xlsx resize-cols book.xlsx B:D 18       # width in Excel units
agent-xlsx resize-cols book.xlsx A --auto     # auto-width
agent-xlsx resize-cols book.xlsx '*' 12       # every used column
agent-xlsx resize-rows book.xlsx 1:10 22      # row height in points
```

## Worksheets and output

- `-w/--worksheet <NAME|INDEX>` targets a specific sheet; defaults to index
  `0`.
- `-o/--output <PATH>` writes the result to a new file instead of mutating
  the original in place.

## Errors

Failures print a single JSON line to stderr and exit non-zero:

```json
{"error": "sheet 'Datz' not found", "kind": "sheet_not_found"}
```

`kind` values you can branch on: `io`, `xlsx`, `parse_range`, `bad_address`,
`parse_json`, `sheet_not_found`, `shape_mismatch`, `other`.

## What this tool does NOT do

- **Evaluate formulas.** Formulas are stored as text; there is no
  calculation engine. A freshly written `=SUM(...)` has no cached value
  until Excel/LibreOffice opens and recalculates the file. The same
  limitation applies to openpyxl and most pure-library xlsx tools.
- Add/remove/rename sheets, merge cells, borders, charts, images,
  comments, data validation, CSV import/export, password protection. Use
  a full library if you need these.
