---
name: fina-xlsx-author
version: 1.0.0
description: Produces a clean, auditable Excel financial workbook built from scratch with a standard tab architecture, color conventions, named ranges, consistent row formulas, no hardcodes, and a dedicated checks tab.
author: matrixx0070
tags: [finance, excel, spreadsheet, modeling, workbook, formatting, audit-ready]
capabilities: []
---

# Author an Auditable Excel Workbook

## When to use
Use this when you are building a financial workbook from a blank file and want it to be legible, maintainable, and audit-ready: a clear tab structure, banker-standard formatting, named ranges, one consistent formula across each row, and a checks tab that proves the model ties. This is the structural discipline layer, not the content of any particular model.

**Not for:** cleaning raw inputs before they enter the workbook (use fina-clean-data-xls), constructing the linked income statement, balance sheet, and cash flow logic (use fina-3-statement-model), valuation mechanics (use fina-dcf-model or fina-comps-analysis), reviewing a finished third-party file (use fina-audit-xls), or presenting results (use fina-pptx-author).

## Method
1. **Lay out the tab architecture first.** Create tabs in flow order: `Cover`, `Assumptions`, `Model`, `Outputs`, `Checks`. Data flows left to right; nothing downstream feeds back upstream. Order tabs so a reader can walk them like a document.
2. **Isolate every input on the assumptions tab.** All drivers live in one place, formatted as inputs, each labeled with its unit and source. Decision point: if a number could ever change or be argued about, it is an assumption and belongs on `Assumptions`, not buried in a formula on `Model`.
3. **Apply the color convention to every cell.** Blue for hardcoded inputs, black for formulas/calculations, green for links pulling from another tab, and a distinct color for links to other workbooks. A reader must be able to tell input from calculation from link at a glance.
4. **Name the ranges that matter.** Give stable, readable names to key drivers and anchors (`tax_rate`, `wacc`, `rev_growth`) so formulas read as prose and cannot silently point at the wrong cell when rows move.
5. **Write one formula across each row.** The formula in the first period column must copy cleanly across every following period with no manual edits. Decision point: if you feel the urge to hand-edit one cell in the middle of a row, stop and add a switch, flag row, or `CHOOSE`/`IF` driver instead, because a broken row pattern is the most common source of silent model errors.
6. **Ban hardcodes inside formulas.** No magic numbers mixed into calculations. A constant used in a formula must reference a labeled input cell or named range.
7. **Build the checks tab.** Add explicit tie-outs (balance sheet balances, cash flow ties to the balance sheet cash line, sources = uses, sum-of-parts = total) that each return TRUE/OK or FALSE, plus a single master flag that is OK only when every check passes.
8. **Set up outputs and printing.** On `Outputs`, present the summary and any charts; set print areas, headers/footers, and freeze panes so the deliverable is clean on screen and on paper.

## Example
You are starting a small operating model. You create `Assumptions` with `rev_growth` = 8% (blue, named), `gross_margin` = 60% (blue, named), and a period header row. On `Model`, revenue period 1 is `=Assumptions!base_rev` and each later period is `=prev_period*(1+rev_growth)` copied cleanly across; COGS is `=revenue*(1-gross_margin)`. Nothing on `Model` is blue except nothing at all, because every input lives on `Assumptions`. On `Checks`, `chk_gp = gross_profit - (revenue - cogs)` must equal 0, and `master_ok = AND(all checks = TRUE)`. On `Outputs`, a summary table links (green) to `Model` totals and a chart reads from it. Print area set, top rows frozen. A reviewer can trace any number blue to black to green in seconds.

## Pitfalls
- **Hardcodes in formulas.** A number typed inside a calculation (`=A1*1.21`) is invisible and un-flexable. Move every constant to a labeled input and reference it.
- **Broken row consistency.** One hand-edited cell in an otherwise uniform row is nearly impossible to spot and silently wrong. Keep one formula copyable across the whole row; encode exceptions as flag rows.
- **Inputs scattered across the model.** Drivers buried among calculations cannot be found or sensitized. Centralize them all on `Assumptions`.
- **No color discipline.** If inputs, formulas, and links all look the same, no one can audit the file. Apply blue/black/green consistently to every cell.
- **Missing checks tab.** Without explicit tie-outs a model can be confidently wrong. Every workbook needs a checks tab with a single master flag.
- **Volatile and fragile references.** Overusing `OFFSET`/`INDIRECT` or hardcoded cell addresses breaks when rows shift. Prefer `INDEX`/`MATCH` or `XLOOKUP` and named ranges.
- **Circular references left on.** An unintended circularity (often via interest-on-average-debt) silently zeroes or errors. Resolve deliberately with a documented iterative switch, never by accident.

## Output format
```
Workbook: <name>.xlsx
  Cover        title, author, date, version, purpose, tab index
  Assumptions  all inputs (blue), labeled, unit + source per driver, named ranges
  Model        calculations (black) and cross-tab links (green), one formula per row
  Outputs      summary tables + charts (links to Model), print area set
  Checks       tie-out rows returning TRUE/FALSE + one master_ok flag

Cell color legend:
  blue  = input/hardcode    black = formula    green = link to another tab
```

## Reference

### Color conventions
| Color | Meaning | Example |
|-------|---------|---------|
| Blue | Hardcoded input / assumption | `rev_growth = 8%` |
| Black | Formula / calculation | `=revenue*(1-gross_margin)` |
| Green | Link to another tab | `=Assumptions!wacc` |
| Red / other | Link to another workbook, or warning | `=[other.xlsx]Sheet!A1` |

### Tab architecture
| Tab | Purpose | Contains |
|-----|---------|----------|
| Cover | Orientation | title, version, date, purpose, tab index |
| Assumptions | Single source of inputs | all drivers, units, sources, named ranges |
| Model | Engine | linked calculations, one formula per row |
| Outputs | Deliverable | summary tables, charts, print setup |
| Checks | Integrity | tie-outs + master OK flag |

### Formula hygiene rules
| Rule | Why |
|------|-----|
| No constants inside formulas | keeps inputs findable and flexable |
| One formula copyable across each row | prevents silent per-cell errors |
| Reference named ranges for key drivers | readable and move-safe |
| No feedback from downstream to upstream tabs | preserves clean left-to-right flow |
| Wrap risky lookups in error handling | avoids `#N/A` cascades |
| Resolve circularity deliberately | avoids accidental iterative loops |

### Useful functions
| Function | Use |
|----------|-----|
| `INDEX`/`MATCH` | robust two-way lookup that survives inserted rows/columns |
| `XLOOKUP` | modern single-function lookup with built-in default |
| `SUMIFS` | conditional aggregation by account/period |
| `IFERROR` | trap `#N/A`/`#DIV/0!` and return a clean value |
| `CHOOSE` | scenario switch (base/bull/bear) driven by one selector |
| `SUMPRODUCT` | weighted sums and array-style checks |

### Checks-row conventions
- Each check returns a boolean or a difference that should be 0 (for example `bs_balance = assets - (liabilities + equity)`).
- Cash tie: cash flow ending cash equals balance sheet cash.
- Sources = uses; sum-of-parts = reported total.
- One `master_ok = AND(all checks)` cell, colored so a failure is obvious at a glance.

### Structure checklist
- Tabs in flow order; cover tab present with version and index.
- Every input on `Assumptions`, blue, labeled with unit and source.
- Color convention applied to every cell.
- Named ranges for all key drivers.
- One formula per row, copyable end to end, no hardcodes.
- Checks tab with tie-outs and a master flag reading OK.
- Print areas, headers/footers, and freeze panes set on delivered tabs.
