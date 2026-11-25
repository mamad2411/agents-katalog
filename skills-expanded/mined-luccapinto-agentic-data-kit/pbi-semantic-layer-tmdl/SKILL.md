---
name: pbi-semantic-layer-tmdl
description: Change the Power BI semantic model — measures, columns, tables, relationships, RLS, DAX — with Power BI Desktop OPEN through the Power BI Modeling (Authoring) MCP server, saving to TMDL in a PBIP project; or by editing TMDL files with Desktop closed. Includes a semantic-model review checklist. Use for any request to add or fix a measure, DAX, relationship, table, column or model metadata.
---

# Skill: pbi-semantic-layer-tmdl

With Desktop open, the model lives in Desktop's memory (a local Analysis Services instance). Edit
it **there**, live, through the Power BI Modeling MCP server — then the user saves and Desktop
writes the TMDL into the PBIP. Editing the `.tmdl` files while Desktop is open does nothing
until a model reload and is overwritten by the next save.

## Default: Desktop open + Modeling MCP
Setup and the tool list: [references/modeling-mcp.md](references/modeling-mcp.md).
1. **Connect:** "Connect to '<file name>' in Power BI Desktop". Confirm with a read: list the
   tables and measures. If the MCP is not registered, stop and point the user to the setup —
   do not fall back to editing TMDL silently.
2. **Inspect through the MCP**, not the `.tmdl` files: while connected, the live model is the
   truth and disk may be stale.
3. **Change** in dependency order: tables/partitions → columns → relationships → measures.
   Check that every referenced table/column exists and that the name is not taken.
4. **Prove it:** run a DAX query through the MCP (`EVALUATE SUMMARIZECOLUMNS(..., "x", [New Measure])`
   or `EVALUATE { [New Measure] }`) and show the value. A measure that only "was created" is not done.
5. **Save:** ask the user to press Ctrl+S in Desktop. That writes the TMDL into
   `<Name>.SemanticModel/definition/` — the diff the team reviews and commits.
6. **Quality:** run `pbi-quality-rules` (BPA) after significant changes — on disk, so after step 5.
7. If a visual must use the new measure, continue in `pbi-report-layer-pbir`. Report reloads do
   not touch the model and are not needed for MCP changes.

## Alternative: Desktop closed (no MCP, older Desktop, CI)
Edit the TMDL files directly:
1. Make sure Desktop is **closed** — it overwrites disk on save.
2. Edit `.tmdl` files following the syntax below; run `pbi-quality-rules`.
3. Ask the user to open the `.pbip`: field list populates, no error banner, each new measure on a
   Card shows a value. On error, re-read the edited TMDL and fix the reference/syntax.

If Desktop must stay open and the MCP is unavailable, edit TMDL, then reload model + report with
`powerbi-report-author preview <folder> --host desktop --reload-with-model` after the same
unsaved-changes gate as `pbi-report-layer-pbir`. It reloads definitions only — the user must
refresh data for new/changed imported columns.

## `.SemanticModel` structure
```
<Name>.SemanticModel/
  definition.pbism          ← pointer (do not hand-edit)
  definition/
    database.tmdl           ← compatibilityLevel
    model.tmdl              ← model properties, `ref table` order, annotations
    tables/<Table>.tmdl     ← one table per file
    relationships.tmdl
    expressions.tmdl        ← shared M expressions / parameters
    roles.tmdl              ← RLS
    cultures/               ← translations
  .pbi/                     ← local cache/settings — never edit, keep out of git
```

## TMDL syntax
```tmdl
/// Order lines. Grain: one row per order line.
table Sales

	/// Sum of the order line amount.
	measure 'Total Sales' = SUM(Sales[Amount])
		formatString: #,##0.00
		displayFolder: Revenue

	measure 'Margin %' =
			DIVIDE([Total Sales] - [Total Cost], [Total Sales])
		formatString: 0.0%
		displayFolder: Revenue

	column Amount
		dataType: decimal
		summarizeBy: sum
		sourceColumn: Amount
```
```tmdl
relationship 5f0c2a4e-9b1d-4c3a-8e2f-1a6b7c8d9e01
	fromColumn: Sales.DateKey
	toColumn: Date.DateKey
```
- Indent with tabs; properties one level under their object.
- Descriptions are `///` lines directly above the object.
- Multi-line DAX: leave the `=` line empty and indent the expression two levels deeper than the
  object, or wrap it in a ```` ``` ```` block.
- Quote names with spaces or symbols: `'Margin %'`; double a quote inside: `'Customer''s'`.

## Review checklist (run it on any model you change or are asked to review)
- **Names** are business-friendly: no `tbl_`/`dim_` prefixes or `_id` columns visible to users.
- **Every measure** has a `formatString`, a `displayFolder` and a `///` description (what it
  means and its grain/filters in plain words).
- **Relationships** match reality: many-to-one from fact to dimension, single direction unless a
  documented reason exists; no ambiguous paths.
- **A real Date table** (marked as date table) drives time intelligence; auto date/time is off
  (`annotation __PBI_TimeIntelligenceEnabled = 0` in `model.tmdl`).
- **Technical keys hidden** (`isHidden` on `...ID`/`...Key` columns); explicit measures instead
  of implicit column aggregation for anything a report shows.
- **DAX:** `DIVIDE` instead of `/` + `IFERROR`; variables for repeated sub-expressions; no
  measure that just returns `BLANK()`.
