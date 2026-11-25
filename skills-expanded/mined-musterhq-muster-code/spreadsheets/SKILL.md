---
name: spreadsheets
description: Create, edit and review Excel workbooks (.xlsx) with Muster. Use whenever the person asks for a spreadsheet, budget, model, tracker, table of data as .xlsx, or to change an existing workbook. Writes live formulas with exceljs and native, editable charts, keeps existing formatting when editing, renders the sheets to page images with office_render and fixes them until they read well.
metadata:
  short-description: Excel workbooks (.xlsx) with live formulas and a render check
---

# Spreadsheets (.xlsx)

Use this skill for any Excel workbook: new ones, edits to an existing .xlsx, and reviews. For a quick table in the
reply, or a .csv the person asked for, you do not need a workbook.

## Tools

- `muster_office` `office_setup`: call it once per chat before the first script. It answers with the command that
  runs a script (`<node> script.mjs`); with it `import ExcelJS from 'exceljs'` works from any folder. Do not
  `npm install` anything into the person's project.
- `muster_office` `office_render`: renders the workbook to page images (each sheet as it would print) and shows you
  the first pages. The first render may download LibreOffice; wait for it.
- Library: `exceljs` reads and writes .xlsx, including styles, number formats, formulas, merged cells, data
  validation, conditional formatting and pictures.

`example.mjs` next to this file is a tested starting point (two sheets, formulas across sheets, number formats, a
frozen header, a total row, a native chart, a picture, print setup). Copy it into the working folder and change it.

## The loop

1. Plan the sheets: inputs, calculations, summary. Decide which cells are inputs and which are formulas.
2. Write a script in the working folder that builds the workbook. Keep the data at the top of the script.
3. Run it with the command from `office_setup`.
4. Call `office_render` and look at every page: headers, widths, number formats, totals.
5. Read the workbook back with exceljs and check that every formula cell still has its formula (see below).
6. Fix, run and render again until the checks pass. Reply with the path and what each sheet holds.

## Formulas stay formulas

- Write calculations as formulas, never as numbers you computed in the script: `{ formula: 'SUM(B2:B13)' }` (no
  leading `=`). Totals, ratios, lookups and cross-sheet references (`Sales!D5`) are all formulas.
- Set `workbook.calcProperties = { fullCalcOnLoad: true }` so Excel and LibreOffice recalculate everything when the
  file opens. Add `result` to a formula cell only when you know the exact value.
- Use only functions Excel has. Absolute references (`$D$14`) for fixed cells; check ranges cover every data row.
- Check after writing:

```js
const check = new ExcelJS.Workbook();
await check.xlsx.readFile('out.xlsx');
check.eachSheet(sheet => sheet.eachRow(row => row.eachCell(cell => {
  if (cell.formula || cell.sharedFormula) console.log(sheet.name, cell.address, '=', cell.formula ?? cell.sharedFormula);
})));
```

- The render shows the recalculated values: `#REF!`, `#NAME?`, `#DIV/0!` or `#VALUE!` on a page image is a bug to fix.

## Quality checks (on the page images)

- Column widths fit their content (no `####`, no cut-off headers); long text wraps (`alignment: { wrapText: true }`).
- Numbers use the right format: money `"$"#,##0.00`, counts `#,##0`, percents `0.0%`, dates `yyyy-mm-dd` or the
  person's locale. Numbers are stored as numbers, not text.
- The header row stands out and is frozen (`views: [{ state: 'frozen', ySplit: 1 }]`); totals are visibly separate.
- Each sheet prints to a sensible width: `pageSetup: { orientation, fitToPage: true, fitToWidth: 1, fitToHeight: 0 }`.
- Sheet names are short and say what they hold.

## Charts

Make charts native and editable with Muster's chart writer, `muster-xlsx-charts` (importable once `office_setup` ran,
like exceljs). It adds real Excel chart parts to a file exceljs saved; every series points at a sheet range, so the
chart follows the cells in Excel, LibreOffice and Numbers. Never put a picture of a chart in a workbook.

```js
import { addCharts } from 'muster-xlsx-charts';
await workbook.xlsx.writeFile('out.xlsx');            // the last exceljs save: saving with exceljs again drops charts
await addCharts('out.xlsx', [{
  type: 'column', sheet: 'Summary', title: 'Revenue by month', position: { from: 'A5', width: 480, height: 280 },
  series: [{ name: 'Sales!$D$1', categories: 'Sales!$A$2:$A$13', values: 'Sales!$D$2:$D$13' }],
  xAxisTitle: 'Month', yAxisTitle: 'Revenue', numberFormat: '"$"#,##0',
}]);
```

- `type`: `column`, `bar`, `line`, `area` (each with `stacked: true` or `'percent'`), `pie` (one series), `doughnut`,
  `scatter` (series are `{ name, x, y }` ranges).
- Ranges are absolute and name their sheet; quote names with spaces: `'Q1 Spend'!$A$2:$A$9`. `name` is a header cell
  or plain text.
- Options: `sheet` (where the chart goes; default the sheet of the first series), `position` (`from` cell plus
  `width`/`height` in pixels, or `from` and `to` cells; default to the right of the data), `legend` (`right`, `left`,
  `top`, `bottom` or `false`), `dataLabels`, `numberFormat` (value axis), `xNumberFormat` (scatter), series `color`.
- Look at the render: every chart should show its bars, lines or slices, readable titles and no overlap with cells.

## Editing an existing workbook

Load it with exceljs, change only the cells you need, and save to a new file unless the person asked to overwrite
theirs. exceljs keeps cell styles, number formats, merged cells, column widths and formulas it read. It does not keep
charts, pivot tables, slicers or macros. If you made the workbook, run the script again (it adds its charts after the
last save) or call `addCharts` again after saving. If it is someone else's and has any (look for `xl/charts/`,
`xl/pivotTables/` or `vbaProject.bin` inside the file with `jszip`), say so and ask before saving over it, or change
cell values directly in the sheet XML with `jszip`: their charts read the edited cells.

```js
const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile('budget.xlsx');
const sheet = workbook.getWorksheet('Budget');
sheet.getCell('C7').value = 4200;                     // an input
sheet.getCell('C20').value = { formula: 'SUM(C2:C19)' };
workbook.calcProperties = { fullCalcOnLoad: true };
await workbook.xlsx.writeFile('budget-updated.xlsx');
```

Render the original and the new file and compare them before you reply.

## Reading a workbook

Load it with exceljs and print the used range of each sheet (`sheet.actualRowCount`, `row.values`); for a formula
cell, `cell.formula` is the formula and `cell.result` the value saved with it. Render it to see how it looks.
