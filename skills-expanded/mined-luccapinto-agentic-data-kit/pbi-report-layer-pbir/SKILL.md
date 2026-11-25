---
name: pbi-report-layer-pbir
description: Edit the Power BI report layer as code — pages, visuals, filters, bookmarks and themes in the PBIR files of a PBIP project — with Power BI Desktop OPEN, using the edit → validate → save → status → reload → screenshot → review loop (Desktop Bridge via powerbi-report-author). Also covers the Desktop-closed path. Use for any request to add, move, restyle or fix a report page or visual.
---

# Skill: pbi-report-layer-pbir

The report layer (`<Name>.Report/`) is **PBIR**: one JSON file per page and per visual, each
with a public JSON schema. Power BI Desktop can stay **open** while you edit it: the
[Desktop Bridge](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-desktop-bridge-overview)
lets a tool reload the files from disk and take screenshots of the rendered pages.

Model objects (measures, columns, relationships) are NOT edited here — they go live through the
Modeling MCP (`pbi-semantic-layer-tmdl`). Create the measure first, then bind the visual to it.

## Tools
- `powerbi-report-author` — Microsoft's report CLI (`npm i -g @microsoft/powerbi-report-authoring-cli`,
  Node 20+). Validates PBIR, describes visual roles/formatting, and drives Desktop through
  `preview --host desktop`. It bundles the lower-level bridge CLI `powerbi-desktop`
  (`status`, `reload`, `screenshot`); always go through `powerbi-report-author preview`, which
  resolves the right Desktop window from the report folder. Details, errors and setup:
  [references/desktop-bridge.md](references/desktop-bridge.md).
- `scripts/validate_pbir.py` (in this skill's folder) — runs `powerbi-report-author validate`, or
  a structural check when the CLI is missing. It looks on PATH, in `$PBIR_AUTHOR_CLI`, and on
  Windows in `%APPDATA%\npm`. If the output says "structural fallback", schemas were NOT
  checked: say so in your report.
- `pbi-visual-reviewer` agent — independent screenshot review.

## The loop (Desktop open)
`<folder>` = the project folder or the `.pbip` path; `<shots>` = an absolute folder OUTSIDE the
PBIP (e.g. `%TEMP%\pbir-review\<Name>`), so screenshots never land in git.

1. **Read before writing.** `powerbi-report-author preview-pages <folder>` and
   `preview-visuals <folder>` list pages and visuals with their file paths. For a new or changed
   visual, `powerbi-report-author catalog describe <visualType>` gives the exact role names
   (e.g. `cardVisual` uses `Data`, `clusteredColumnChart` uses `Category` + `Y`);
   `formatting describe-object <visualType> <object>` gives property names. Do not guess them.
2. **Edit** the PBIR JSON (anatomy below). One logical batch at a time.
3. **Validate:** `python3 <skill>/scripts/validate_pbir.py <folder>`. Fix every error before
   going on; read the warnings.
4. **Save gate.** Ask the user to save in Desktop (Ctrl+S) if they changed anything by hand,
   then check: `powerbi-report-author preview <folder> --host desktop --status`.
   Continue only when `data.details.hasUnsavedChanges` is exactly `false`.
5. **Reload:** `powerbi-report-author preview <folder> --host desktop --reload`.
6. **Screenshot every affected page:**
   `powerbi-report-author preview <folder> --host desktop --screenshot "<shots>" --all-pages`
   (or `--screenshot "<shots>\<page>.png" --page <pageId>`). A screenshot does not reload; always
   reload first.
7. **Review:** hand the PNG paths, the user's request/spec and the `.Report` path — and nothing
   about your reasoning — to the `pbi-visual-reviewer` agent. In tools without subagents
   (Cursor, Antigravity), run its checklist in a fresh chat with only those inputs.
8. REJECTED → fix the listed files and repeat from step 3. APPROVED → report the result and let
   the user save/commit.

### Pitfalls (each one has lost real work)
- **Reload discards whatever Desktop has not saved.** That is why step 4 exists. If status says
  `true`, `null`, or fails, stop and ask the user to save; never reload "just to see".
- **A Desktop save can drop `"$schema"`** from the `.pbip` and `definition.pbir` (seen once on
  Desktop 2.159). `validate` then fails with `PBIR_JSON_FILE_NO_SCHEMA` on files you did not edit. Put
  the line back as the first key, copied from git history (`git diff` shows the removed line);
  do not "fix" anything else in those files.
- **Reload covers the report only.** `--reload` does not re-read model files. Model changes go
  through the Modeling MCP, which updates Desktop live. Use `--reload-with-model` only when TMDL
  was edited on disk (Desktop-closed habits) — and it still does not refresh data.
- **An edited theme may not show after reload.** Desktop caches themes by file name. When you
  change a custom theme, rename its JSON (e.g. `Brand-3f9a1c.json` → `Brand-7b2e04.json`) and
  update both references in `report.json` (`themeCollection.customTheme.name` and the
  `resourcePackages` item `name`/`path`), then validate and reload.
- A page added on disk is unknown to the open window until a reload; a screenshot of it fails
  with `RENDER_FAILED`.
- Two Desktop windows with the same report → `HOST_UNAVAILABLE`. Ask the user to close one;
  never close Desktop yourself.

## Alternative: Desktop closed
Use it when there is no Bridge (Desktop older than the Bridge release, the setting
*File > Options > Security > Desktop Bridge* is off, or the machine is not Windows) and in CI.
1. Make sure Desktop is **closed** — an open Desktop overwrites the files on its next save.
2. Edit the PBIR, run `validate_pbir.py` (in CI: `--format json`, fail on exit code 1).
3. Ask the user to open the `.pbip` and check the pages; no screenshots, so ask for one or for
   a description, and run the reviewer checklist on what you get.

## `.Report` structure (PBIR)
```
<Name>.Report/
  definition.pbir                        ← model binding (byPath ../<Name>.SemanticModel)
  definition/
    version.json
    report.json                          ← themeCollection, resourcePackages, settings
    pages/
      pages.json                         ← pageOrder + activePageName
      <pageId>/
        page.json                        ← name (= folder), displayName, width, height
        visuals/<visualId>/visual.json   ← one visual per file; name = folder
  StaticResources/
    RegisteredResources/                 ← custom themes and images you add
    SharedResources/BaseThemes/          ← Microsoft base themes — never edit
```
PBIR-Legacy (a single `report.json` at the `.Report` root) cannot be edited this way: ask the
user to save the report in PBIR format first.

## Visual anatomy (`visual.json`)
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
  "name": "7b2d4f6a8c0e1a3b5d02",
  "position": { "x": 40, "y": 240, "z": 2000, "width": 760, "height": 420, "tabOrder": 2000 },
  "visual": {
    "visualType": "clusteredColumnChart",
    "query": { "queryState": {
      "Category": { "projections": [ { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "Product" } }, "Property": "Category" } }, "queryRef": "Product.Category", "nativeQueryRef": "Category", "active": true } ] },
      "Y":        { "projections": [ { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Sales" } }, "Property": "Total Sales" } }, "queryRef": "Sales.Total Sales", "nativeQueryRef": "Total Sales" } ] }
    } },
    "visualContainerObjects": { "title": [ { "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "text": { "expr": { "Literal": { "Value": "'Sales by category'" } } } } } ] }
  }
}
```
- New page/visual: fresh 20-hex-char `name`, folder with the same name; add new pages to
  `pages.json` `pageOrder`.
- Position is in pixels from the page's top-left; keep `x + width ≤ page width` and
  `y + height ≤ page height`. Align edges to a shared grid (e.g. multiples of 8) and keep equal gaps.
- Literal encoding: text `'quoted'`, numbers `12D`, booleans `true`. When unsure,
  `powerbi-report-author expr encode --kind <type> <value>`.
- Avoid visuals Microsoft is retiring (Q&A, Bing Map, filled map).

## Themes
Create custom themes under `StaticResources/RegisteredResources/`, register them in
`report.json` (`themeCollection.customTheme` + a `resourcePackages` item of type
`RegisteredResources`), define ≥ 8 `dataColors`, and standardize fonts with the wildcard
`visualStyles` (`"*": { "*": { ... } }`). Rename the file on every edit (pitfall above).

## Before large changes
Ask the user to commit the PBIP first so every agent edit is a reviewable diff.
