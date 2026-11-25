---
name: rgaa-tables
description: "Audit a web page for RGAA v4.1.2 Theme 5 – Tables accessibility compliance. Checks that complex data tables have summaries, layout tables linearize correctly, data tables have proper titles and headers, and header-cell associations are correct. Use this skill when someone asks to check table accessibility, verify RGAA Theme 5, audit data tables, or check table markup on a website."
---

# RGAA Tables Accessibility Audit (Theme 5)

Audits a web page against the 8 criteria of RGAA v4.1.2 Theme 5: Tables.

## Audit procedure

### Step 1: Gather table data

```javascript
(() => {
  const tables = [];
  document.querySelectorAll('table').forEach((table, i) => {
    const ths = Array.from(table.querySelectorAll('th')).map(th => ({
      text: th.textContent.trim().substring(0, 50),
      scope: th.getAttribute('scope'),
      id: th.getAttribute('id'),
      headers: th.getAttribute('headers')
    }));
    const tds = Array.from(table.querySelectorAll('td')).map(td => ({
      headers: td.getAttribute('headers'),
      hasContent: !!td.textContent.trim()
    }));
    const caption = table.querySelector('caption');

    tables.push({
      index: i,
      role: table.getAttribute('role'),
      ariaLabel: table.getAttribute('aria-label'),
      ariaLabelledby: table.getAttribute('aria-labelledby'),
      ariaDescribedby: table.getAttribute('aria-describedby'),
      summary: table.getAttribute('summary'),
      hasCaption: !!caption,
      captionText: caption?.textContent.trim().substring(0, 100),
      rowCount: table.rows.length,
      colCount: table.rows[0]?.cells.length || 0,
      headerCount: ths.length,
      headers: ths.slice(0, 20),
      sampleCells: tds.slice(0, 10),
      isLayoutTable: table.getAttribute('role') === 'presentation' || table.getAttribute('role') === 'none',
      hasTheadTbodyTfoot: !!(table.querySelector('thead') || table.querySelector('tbody') || table.querySelector('tfoot'))
    });
  });
  return JSON.stringify(tables, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 5.1** – Complex data tables have a summary.
A complex table (multiple header levels, spanning cells) must have a summary explaining its structure, via `aria-describedby` pointing to a description or a `<caption>` containing both title and summary.

**Criterion 5.2** – Summary of complex data tables is relevant.
The summary must help the user understand the table's organization.

**Criterion 5.3** – Layout tables linearize correctly.
Tables with `role="presentation"` or `role="none"` must make sense when read linearly (left to right, top to bottom). They must NOT use `<th>`, `<caption>`, `<thead>`, `<tfoot>`, `<colgroup>`, or `scope`/`headers` attributes.

**Criterion 5.4** – Data table titles are correctly associated.
Title must use `<caption>` directly inside the `<table>`, or `aria-label`, or `aria-labelledby`.

**Criterion 5.5** – Data table titles are relevant.
Titles must describe the table's content or purpose.

**Criterion 5.6** – Column and row headers use `<th>`.
Every header cell must use `<th>`, not styled `<td>`.

**Criterion 5.7** – Header-cell association uses appropriate technique.
- Simple tables: `<th scope="col">` or `<th scope="row">`
- Complex tables: `headers` attribute on `<td>` referencing `id` values on `<th>` elements

**Criterion 5.8** – Layout tables must not use data table elements.
Tables with `role="presentation"` must not contain: `<caption>`, `<th>`, `<thead>`, `<tfoot>`, `<colgroup>`, `scope` attribute, or `headers` attribute.

### Step 3: Generate report

Classify each table as data table, complex data table, or layout table. Then apply the relevant criteria.
