---
name: financial-modeling-sheet
version: 1.1.1
description: >
  Apply house style to quantitative Excel workbooks through an Excel assistant
  add-in. Use to create, extend, audit, or restyle workbook layout, input/formula
  colors, named styles, navigation, dashboards, and Power Query output. Audit
  mode is read-only. Governs presentation and organization, not arithmetic or ETL.
---

# Financial modeling sheet: workbook house style

This skill governs how a quantitative workbook **looks and is organized**, not what it calculates. It answers one question at every cell: *what role does this play in the model, and how must that role be visible?*

A reader who has never opened the file should be able to tell, at a glance and without clicking a single cell, which numbers were typed, which were chosen, which were calculated, which came from an external engine, and which one is the answer.

Every sheet has the same skeleton: **rows 1–2 blank, the title on row 3, columns A and B empty, content anchored at column C.** That constant frame is what makes twenty sheets read as one workbook.

> Mode (CREATE / EXTEND / AUDIT / RESTYLE) -> palette profile -> semantic classification -> named styles -> navigation -> definition of done

It is domain-neutral. Financial models are the primary case, but the same architecture serves risk registers, research result sets, operations dashboards, statistical workbenches, and engineering calculation sheets.

---

## Prime directive: classify before you format

**Never apply one format to a whole used range.** Formatting is a claim about meaning. Applying a fill to a block you have not classified makes a false claim.

Three rules override everything else in this skill:

1. **Classify every cell or block by semantic role first** (`references/cell-classes.md`), then apply the matching named style. If you cannot name the role, do not color the cell.
2. **One palette profile per workbook, declared in Documentation, never mixed** (`references/palette-profiles.md`). The default is House Style. Mixing profiles makes the same fill mean two different things and destroys the reader's ability to audit at a glance.
3. **Preserve what is already coherent.** In EXTEND, AUDIT, and RESTYLE modes, formulas, cross-sheet references, charts, notes, named styles, column widths, hidden structures, and locally coherent formatting survive untouched unless the user explicitly asked for a full restyle. You are standardizing a workbook, not rebuilding it.

This skill does not verify arithmetic. Whether a number is *correct* is outside its scope; whether a reader can tell what that number **is** — typed, chosen, calculated, imported, decisive — is entirely inside it. When a request mixes the two, do the presentation work and say plainly which findings are formatting and which would need the math checked separately.

---

## Prime directive: lock the mode

Every request resolves to one of four modes. Identify it first and stay inside it.

| Mode | The user is saying | Primary output | Destructive? |
|---|---|---|---|
| **CREATE** | "build me a workbook for…" | a new workbook, fully styled from row 1 | no |
| **EXTEND** | "add a sheet / a module / a dashboard" | new blocks that match the existing house style | no |
| **AUDIT** | "check this workbook against the standard" | a conformance report, **no file changes** | no |
| **RESTYLE** | "standardize / clean up this workbook" | a changed workbook + a change log | **yes** |

AUDIT never writes. RESTYLE writes, so it needs an explicit go-ahead, a backup copy, and a change log listing every cell range touched. Do not drift from AUDIT into RESTYLE because the findings were obvious — report, then ask. The full mode contract, including the preservation list and the approval gates, is `references/mode-map.md`.

---

## When to use / when not

Use it to create a standardized quantitative workbook, add a conforming sheet to one, audit an existing workbook's structure and formatting, or normalize a legacy file that grew without a convention.

Skip it for: verifying the arithmetic itself, data cleaning and ETL, statistical method selection, presentation slides (`cobesy`), and diagrams (`drawio`). Skip it for a five-cell scratch calculation — the overhead is not worth it below roughly one screen of content.

---

## How to use this skill

1. **Lock the mode** (`references/mode-map.md`). CREATE, EXTEND, AUDIT, or RESTYLE. For EXTEND/AUDIT/RESTYLE, inspect first: sheet order, tab colors, view settings, used ranges, formulas, named styles, column widths, notes, charts, hidden sheets, and existing color conventions.
2. **Declare the palette profile** (`references/palette-profiles.md`). Default is House Style. If the workbook already follows the Audit Standard coherently, keep it and say so — do not convert a coherent workbook to the default profile without approval.
3. **Fix the architecture** (`references/workbook-architecture.md`). Sheet order, tab colors as a purpose code, gridlines and headings visible, no default freeze panes, **rows 1–2 blank and the title on row 3 on every sheet, columns A and B left empty, content anchored at column C**, method/source markers in a marker column to the right of each block.
4. **Build the shared inputs before anything downstream** (`references/sheet-standards.md`). They are the single source of truth — on their own sheet in a larger workbook, or as a block at the top of a task sheet in a small one. Every editable parameter lives there or in a clearly-marked scenario control, never buried in a formula.
5. **Classify and style each block** (`references/cell-classes.md`, `references/named-styles.md`). Nine semantic classes; apply the named style, not an ad-hoc fill. Where a named style exists in the workbook, reuse it rather than creating a parallel one.
6. **Apply typography, layout, and number formats** (`references/typography-and-layout.md`, `references/number-formats.md`). Arial for structure, Aptos Narrow for semantic styles. Leading minus for negatives, never red, never parentheses. Units in their own column.
7. **Normalize any Power Query output** (`references/power-query-data-sheets.md`). Its own `Data <n> <short id>` sheet at the end, loaded at `C6`, built-in table style stripped and replaced by the house header and body styles, a `PQ: <headline>` caption above the header row, column types set in the query — and everything downstream references it rather than copying it.
8. **Add charts only where a relationship is decision-useful** (`references/charts-and-tables.md`). XYScatter, XYScatterLines, or Line. No 3D. No decorative conditional formatting, no tables or pivots by default.
9. **Build navigation last** (`references/menu-and-navigation.md`). The menu is written *after* the tab order is final, and its order and swatches must match the actual tabs exactly.
10. **Run the checks** (`references/integrity-and-checks.md`). No `#REF!`, `#DIV/0!`, `#VALUE!`, or unexplained `#N/A`. Dashboard values link to source calculations. Every hyperlink resolves. No work-in-progress fills remain.
11. **Run the definition of done** (`references/audit-checklist.md`). The workbook is not deliverable until every line passes. In AUDIT mode this checklist *is* the deliverable.

This standard is applied **inside Excel**, through an assistant add-in (Claude for Excel, ChatGPT for Excel) driving the live workbook — not by generating a file offline. How to instruct the add-in, what units it reports, and the failure modes to watch for are in `references/implementation-excel-addin.md`.

---

## Capability map

- **A. Modes and the preservation contract**: what each mode may touch, approval gates, change logs: `references/mode-map.md`.
- **B. Palette profiles**: House Style vs Audit Standard, the fill-meaning conflict, the legacy house palette, the mapping table, the profile-neutral rules (green font for mixed cells, transient WIP fill): `references/palette-profiles.md`.
- **C. Semantic cell classes**: the nine roles from source data to recommended result, plus checks and warnings: `references/cell-classes.md`.
- **D. Named styles**: the exact style registry — `Header`, `SectionHeader`, `RowTitle`, `SourceData`, `Input`, `Constant`, `Output`, `Result`, `Recommended`, `Note`, `ExplanatoryText`, `Hlink`, `CheckPass`/`CheckWarn`/`CheckFail`: `references/named-styles.md`.
- **E. Workbook architecture**: sheet order, tab-color code, workbook view, the row-3 / column-C anchor, the no-merge rule: `references/workbook-architecture.md`.
- **F. Navigation**: menu geometry, swatches, hyperlink syntax and escaping, what to omit: `references/menu-and-navigation.md`.
- **G. Sheet standards**: dashboard, documentation, task sheets, shared inputs, engine, support calculations, data sheets: `references/sheet-standards.md`.
- **H. Typography and layout**: fonts, row heights, column widths, borders, alignment, wrapping: `references/typography-and-layout.md`.
- **I. Number formats**: format by measurement type, precision discipline, the negative-value convention, units: `references/number-formats.md`.
- **J. Power Query data sheets**: position and naming, replacing the built-in table style, the `PQ:` caption, type inference, refresh survival: `references/power-query-data-sheets.md`.
- **K. Charts and tables**: chart-type selection, chart styling, the tables/pivots/conditional-formatting policy: `references/charts-and-tables.md`.
- **L. Integrity and checks**: formula integrity, the check/warning block, legacy normalization: `references/integrity-and-checks.md`.
- **M. Delivery**: application workflow, definition of done, audit report format: `references/audit-checklist.md`.
- **N. Implementation**: how to drive Claude for Excel / ChatGPT for Excel against a live workbook: `references/implementation-excel-addin.md`.

---

## The style packet

Carry these fields across every phase and record them on the Documentation sheet.

| Packet field | Role |
|---|---|
| `M mode` | CREATE / EXTEND / AUDIT / RESTYLE |
| `P profile` | House Style (default) or Audit Standard — declared once, never mixed |
| `N naming` | the sheet-naming pattern for task sheets (numbered `Task 1…N`, or descriptive) — one pattern throughout |
| `T tab order` | the final sheet order; the menu is generated from this, not from memory |
| `S styles` | named styles present in the workbook, reused rather than duplicated |
| `C classes` | the semantic class assigned to each block, before any fill is applied |
| `U units` | unit and precision decision per row/table |
| `X external` | which blocks come from Python / an API / a solver / Power Query, and their marker-column labels |
| `D deltas` | in RESTYLE mode: every range changed, for the change log |

---

## Decision points

- **Which palette profile?** New workbook, or the user wants the semantic 9-class scheme -> House Style (the corporate-finance blue/yellow convention). Existing workbook already coherently using orange-input/gray-formula -> Audit Standard, keep it. Existing workbook on the old gray-source/orange-control house scheme -> the legacy house palette; match it, do not convert without approval. Never mix. (`references/palette-profiles.md`.)
- **Blue or yellow for this cell?** Is it data the world supplied, filled once — a historical actual, an opening balance, an observed or imported value, a value surfaced from the shared inputs -> blue `SourceData`. Is it an assumption or driver the user tunes to run a scenario -> yellow `Input`. Is it a constant fixed by the task or methodology -> gold `Constant`. A cross-sheet formula that *surfaces* an input into a parameter block is still blue — it is consumed there, not edited; role beats mechanism. (`references/cell-classes.md`.)
- **Output or Result?** Any calculated value a reader consumes -> light-gray `Output`. The value the decision turns on -> navy `Result`, white bold. The option actually chosen -> pale-green recommendation. If everything is navy, nothing is. (`references/cell-classes.md`.)
- **Freeze panes?** Default no. Add only when a sheet is long or wide enough that the header scrolls out of sight during normal reading. (`references/workbook-architecture.md`.)
- **A chart or a table?** Does the relationship between two metrics carry the message -> chart. Does the reader need the exact figures -> table. Decoration -> neither. (`references/charts-and-tables.md`.)
- **Table or formatted range?** Formatted range by default. Formal Excel table only when filtering, structured references, or aggregation genuinely require it — and for Power Query output, which necessarily lands as a table. (`references/charts-and-tables.md`.)
- **Where does this loaded data go?** Any Power Query output gets its own `Data <n> <short id>` sheet at the end of the workbook, is referenced rather than copied, and never edited in place — a refresh silently overwrites the edit. (`references/power-query-data-sheets.md`.)
- **Can this be delivered?** Only if every line of the definition of done passes and no WIP fill survives. (`references/audit-checklist.md`.)

---

## Cross-skill handoffs

| Sibling skill | Direction | Phase | What flows |
|---|---|---|---|
| `reflect` | out | AUDIT | an ambiguous restyle request -> a resolved prompt before touching a live workbook |
| `premortem` | out | 10 | a finished decision workbook -> "how could this mislead a reader" failure modes |
| `cobesy` | out | delivery | a standardized workbook -> the rollout plan that gets the convention adopted |
| `drawio` | out | 3 | sheet architecture and data-flow between modules -> a workbook map diagram |
| `intana-viz` | out | AUDIT | conformance findings -> a structured-analytic view of where the model misleads |
| `humanizer` (external) | out | any | the written audit narrative -> de-AI'd prose ([github.com/blader/humanizer](https://github.com/blader/humanizer)) |

---

## Files

References (normative rules):

- `references/mode-map.md`: the four modes, preservation contract, approval gates, change log format.
- `references/palette-profiles.md`: House Style vs Audit Standard, the fill-meaning conflict, the legacy house palette, mapping table, profile-neutral rules.
- `references/cell-classes.md`: the nine semantic classes plus checks and warnings, with classification tests.
- `references/named-styles.md`: exact specification of every named style — fill, font, color, border, alignment.
- `references/workbook-architecture.md`: sheet order, tab colors, workbook view, starting positions, no-merge rule.
- `references/menu-and-navigation.md`: menu geometry and structure, swatches, hyperlink syntax and escaping.
- `references/sheet-standards.md`: dashboard, documentation, task sheets, shared inputs, engine, support calculations, data sheets.
- `references/typography-and-layout.md`: fonts, row heights, column widths, borders, alignment, wrapping.
- `references/number-formats.md`: formats by measurement type, precision, units, the negative-value convention.
- `references/power-query-data-sheets.md`: Power Query output — position, naming, table-style replacement, the `PQ:` caption, data types, refresh survival.
- `references/charts-and-tables.md`: chart selection and styling; tables, pivots, and conditional-formatting policy.
- `references/integrity-and-checks.md`: formula integrity, check/warning blocks, legacy normalization.
- `references/audit-checklist.md`: application workflow, definition of done, audit report format.
- `references/implementation-excel-addin.md`: driving an Excel add-in to apply all of the above, and the failure modes to check for.

Assets (fill-in build specs):

- `assets/menu-sheet-spec.md`: the menu sheet, cell by cell.
- `assets/dashboard-spec.md`: dashboard layout with key results, notes, and linked outputs.
- `assets/input-block-spec.md`: the single-source-of-truth input block, as a sheet or as a block.
- `assets/documentation-sheet-spec.md`: methodology, dependencies, sources, limitations, instructions.
- `assets/task-sheet-spec.md`: the repeatable six-block task sheet.
- `assets/data-sheet-spec.md`: the Power Query data sheet, cell by cell.
- `assets/audit-report-template.md`: the AUDIT-mode conformance report.
