---
name: lark-sheets-ops
version: "1.0"
description: Read and write Lark Sheets (电子表格) through the bot's NyxID-brokered sheets APIs — find a spreadsheet and its sheet ids, read a cell range, append rows to the bottom, and overwrite a range. Handles the range format (sheetId!A1:D10) and the valueRange wrapper, extracts the spreadsheet_token from a share URL, and doubles as the sheets-scope probe — on a scope 403 it reports the exact missing permission. Lark Sheets here is the spreadsheet product, distinct from Lark Base / Bitable — use the Base skill for Bitable tables.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - sheets
    - spreadsheet
---

# Lark Sheets Ops

Use for "把这些数据追加到那张表 / 读一下这个表格 / 把第二列改成 X" against a **Lark Sheets**
spreadsheet. (For a **Base / Bitable** table — records, fields, views — use the Base skill instead;
they are different products with different APIs.)

**You (the agent) run the flow yourself** via NyxID-brokered access `nyxid_proxy`
`{slug:"api-lark-bot", path:"/open-apis/sheets/...", method:...}`. NyxID injects the bot's
`tenant_access_token` server-side — never ask for a token. Paths start at `/open-apis/...`.

## Two footguns

1. **`spreadsheet_token`** is the id in the share URL after `/sheets/` (e.g.
   `https://…/sheets/shtcnXXXX` → token `shtcnXXXX`). Read it from the URL the user pasted; never invent it.
2. **Range = `{sheet_id}!A1:D10`** and every read/write wraps values in a `valueRange` object. A range
   without the `sheet_id!` prefix, or values not wrapped in `valueRange`, is the usual 400.

## How to run it

1. **Resolve the sheet ids (and scope probe).** `GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query`
   lists every sheet with its `sheet_id` and `title`. On 403/scope error, report it verbatim, say the
   tenant app needs sheets scopes (e.g. `sheets:spreadsheet`), and stop. Pick the `sheet_id` for the
   tab the user means (default the first tab if there is only one).

2. **Read a range.** `GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}!A1:D50`
   → `data.valueRange.values` is a row-major 2D array. Render it as a compact table and say which range
   you read.

3. **Append rows to the bottom.**
   `POST /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append?insertDataOption=INSERT_ROWS`
   body `{"valueRange":{"range":"{sheet_id}!A1:C1","values":[["a","b","c"],["d","e","f"]]}}`. The
   `range` only anchors the columns/sheet; appended rows go after the existing data. Echo the rows and
   confirm before writing.

4. **Overwrite a specific range.**
   `PUT /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values`
   body `{"valueRange":{"range":"{sheet_id}!A2:C3","values":[[...],[...]]}}`. This **replaces** the
   cells in that exact range — echo the range and the new values and get an explicit confirm first,
   because it overwrites existing content.

## Failure semantics

- Scope 403 / `99991xxx` → verbatim error + the missing sheets scope; never retry blindly.
- 400 on read/write → almost always a bad `range` (missing `sheet_id!` prefix) or values not wrapped
  in `valueRange`; fix the shape and retry once.

## Guardrails

- Append is additive and low-risk; **overwrite (PUT) replaces cells** — always echo the target range
  and values and get an explicit confirm before a PUT.
- Never invent a `spreadsheet_token` or `sheet_id` — read the token from the URL and the sheet_id from
  step 1.
- Only use real returned data; never ask the user for tokens — NyxID handles all credentials.
