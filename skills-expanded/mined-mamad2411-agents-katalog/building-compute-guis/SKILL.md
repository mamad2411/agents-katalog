---
name: building-compute-guis
description: Use when the user wants a calculator, form, what-if slider explorer, or dataset analyzer — a render_gui COMPUTE-mode page where their numbers run locally and never reach the model
---

# Building Compute GUIs

Typical flow, two tool calls total: load the `render_gui` schema via
ToolSearch → write the spec → call the tool once. The tool description IS
the full grammar (components, expressions, formats) — trust it; this skill
only adds page design. A success reply means done: do not read the output
back or re-render.

You ship the *formulas*; the user runs their *real numbers* locally. Design
the page so every value the user cares about updates live as they type.

## Shape of a compute page

1. **Inputs** — scalars (`slider`, `input`, `select`, `toggle`) for a
   calculator; a `table` when the data is rows. Seed `rows` with 2–3 example
   rows the user will replace; label the table with a privacy cue
   ("paste from your spreadsheet — data never leaves this page").
2. **Answers** — computed `text` for scalars (`{"expr": "sum(col(rows,'amount'))",
   "label": "Total"}`), a `plot` for series. Answers re-render on every edit.
   Label plot axes with `xLabel`/`yLabel` on the plot node — supported, no
   need to verify; fields outside the grammar come back as tool warnings.
3. **Layout** — group inputs and answers into top-level stacks; each becomes
   a panel card. Put the primary answer where the eye lands.

```json
[
  { "bind": "rows", "columns": ["month", "amount"], "label": "Your expenses — data never leaves this page",
    "rows": [ { "month": "Jan", "amount": 1240 }, { "month": "Feb", "amount": 980 } ] },
  { "children": [
    { "type": "text", "expr": "sum(col(rows,'amount'))", "label": "Total" },
    { "type": "text", "expr": "avg(col(rows,'amount'))", "label": "Monthly average" }
  ] },
  { "series": [{ "y": "col(rows,'amount')", "label": "spend" }], "x": "labels(rows,'month')", "kind": "bar", "title": "Spend by month" }
]
```

## Rules the schema doesn't spell out

- Declare a control (or `table`) before anything that reads its key;
  unset keys show `—` in computed text rather than erroring.
- Table paste: multi-line or tab-delimited clipboard text replaces all rows;
  a single-line paste (even with commas) is a plain cell edit.
- Expression-language edge cases (operator list, data helpers, array-aware
  min/max): [references/expressions.md](references/expressions.md).
- Without MCP registered, render from the CLI:
  `node ${CLAUDE_PLUGIN_ROOT}/scripts/render-spec.js gui spec.json out.html`

## Runtime constraints (load-bearing facts — trust these, don't re-derive)

- **Money:** computed text prints up to 12 significant digits
  (`1234.56789012`) by default. Use `money(x)` for a `"$"`-prefixed 2-decimal
  string (`money(100/3)` → `"$33.33"`), or `fixed(x, n)` for n decimals — both
  return strings, for `text{expr}` display only, never for `plot`/`chart`/
  aggregates.
- **Missing table cells:** `col(rows,'name')` maps a blank or whitespace-only
  cell to `NaN`, same as non-numeric junk — `sum`/`avg` skip it rather than
  treating it as 0.
- **Per-row column math:** give the `table` node a `derived` array —
  `"derived": [{"name": "profit", "expr": "revenue-cost"}]` — to compute a
  read-only column per row (editable column names are the expr's variables).
  It appears after the editable columns, recomputes live, and is reachable by
  aggregates (`sum(profit)`). Arithmetic still does not broadcast over
  columns at page level — for "total revenue" derive
  `{"name": "total", "expr": "revenue*qty"}` and use `sum(total)`, never
  `sum(revenue)*sum(qty)` (and never `sum(revenue*qty)`, which validates but
  renders `—`).
- **Width budget:** the page is 960px wide and `dir:"row"` stacks never
  wrap. A slider row is ~300px (label + 160px track + 68px number box), so
  three control-bearing panels per row is the practical max; when in doubt
  keep the default vertical stacking.
- **Unset inputs:** computed text renders `—` until every dependency has a
  value.
- **Hand-off:** say how you verified the file opens (double-click /
  `file://`, or a dev server) so the user knows the tested path.
