---
name: thinkcell
description: >-
  Generate, update, and automate think-cell charts and elements in PowerPoint and
  Excel. Use ANY time the user mentions think-cell, thinkcell, or .ppttc files, or
  asks to create/update PowerPoint charts following think-cell conventions
  (waterfall, Mekko, stacked column, Gantt, Harvey ball, scatter/bubble, etc.) —
  especially in consulting or finance contexts where charts must match a company
  template's fonts and colors. Also use when filling a PowerPoint template with
  Excel or JSON data, wiring VBA/C#/Python COM automation, or building slides that
  "look like the rest of the deck." If the user mentions PowerPoint + Excel +
  automation together, assume think-cell. Also triggers on French phrases
  "graphique en cascade", "histogramme empilé", "diagramme de Gantt", "Mekko",
  "feuille de données", "modèle PowerPoint", "remplir un modèle", "automatiser un
  rapport", "comme ailleurs dans la présentation", "respecter la charte graphique".
---

# think-cell automation

A skill for generating think-cell charts and elements correctly, in the right format, following a company template.

## Core principle: think-cell is template-driven

think-cell is **not** a charting library Claude can call directly. It is a PowerPoint COM add-in. To produce a think-cell chart programmatically, the workflow is always:

1. **A PowerPoint template exists** (`.pptx`) containing think-cell elements (chart, table, text field, Harvey ball, etc.) that each have a **name** assigned via the think-cell mini toolbar (`AddRangeData Name`).
2. **Data is supplied separately** — as JSON (`.ppttc` file) or as an Excel workbook range.
3. **think-cell merges them** when the `.ppttc` is opened, when `PresentationFromTemplate` runs, or when `UpdateBatch.Send()` runs.

This means the formatting (fonts, colors, layout, label positions, source line, page numbers) lives in the **template**, not in the code Claude writes. Claude's job is to (a) produce the correct data payload and (b) wire it to the correctly-named element. Everything else — house style — comes from the template, which is why charts produced this way automatically match the rest of the deck.

**Therefore, before doing anything, Claude must know:**
- Which template is being used (path to the `.pptx`)
- Which named elements are in it (and what kind: chart? text field? table?)
- For each chart element, its **datasheet layout** (default? `100%=` row? `Size` column for Mekko? etc.)

If any of these are unknown, ask the user, or — if a template file is available — inspect it before generating code.

## French ↔ English glossary (the user may speak either)

think-cell's UI exists in French. Recognise both labels — and when the user writes in French, respond in French and use the French chart/element names in explanations (but keep code identifiers — JSON keys, VBA function names — in English; those are fixed by the API).

| English | Français | Notes |
|---|---|---|
| Template (`.pptx`) | Modèle | "Le modèle de la boîte / du cabinet" = the corporate template. |
| Datasheet | Feuille de données | Per-chart Excel grid. |
| Datasheet layout | Mise en page de la feuille de données | Series row / category column / `100%=` row toggles. |
| Series / Category | Série / Catégorie | Row 1 = catégories; column 1 = séries (by default). |
| Stacked column | Histogramme empilé | Stacked-100% = "empilé 100 %". |
| Clustered column | Histogramme groupé | |
| Waterfall | Graphique en cascade | The `"e"` end-marker is called "fin" / "total" in the UI. |
| Mekko / marimekko | Mekko (also "marimekko") | The width row is the "ligne 100%=" or "ligne taille". |
| Pie / doughnut | Camembert / Anneau | |
| Scatter / bubble | Nuage de points / Bulles | |
| Gantt | Diagramme de Gantt | Anchor points = "points d'ancrage". |
| Harvey ball | Boule de Harvey | |
| Checkbox | Case à cocher | |
| Automation text field | Champ texte d'automatisation | The `<>` placeholder. |
| Source line / footer | Source / Pied de page | |
| Slide title | Titre de diapositive | |
| Excel data link | Lien de données Excel | |
| Style file | Fichier de style | The `.style` corporate-style file. |
| Mini toolbar | Mini-barre d'outils | Where `AddRangeData Name` lives. |
| House style / Brand compliance | Charte graphique | "Comme ailleurs dans la présentation" = matching house style. |

Common French request patterns and what they mean:
- "Fais un graphique en cascade avec ces chiffres" → waterfall via JSON automation (`.ppttc`).
- "Mets ce tableau dans le modèle de la boîte" → fill named element via JSON or `UpdateBatch`.
- "Comme ailleurs dans la présentation" / "Respecter la charte" → route through the corporate `.pptx` template; don't try to set fonts/colors from code (see `references/style-and-branding.md`).
- "La feuille de données doit avoir la ligne 100 %=" → enable the `100%=` row in the template's datasheet layout.

## Decision tree: which path to use

| User situation | Path to use | Reference |
|---|---|---|
| Wants to generate a presentation from data (no manual PowerPoint editing) | **JSON automation** (`.ppttc`) | `references/json-automation.md` |
| Wants charts that auto-refresh from a live Excel workbook | **Excel data links** (set up once in template) + `PresentationFromTemplate` for batch refresh | `references/excel-automation.md` |
| Wants to update specific named elements in an existing template from Excel ranges, possibly without pre-existing links | **`UpdateBatch`** API (VBA / C# / Python via win32com) | `references/excel-automation.md` |
| Wants Claude to write VBA / C# / Python that drives think-cell at runtime | **COM API** (`thinkcell.addin`) | `references/excel-automation.md` |
| Doesn't have a template yet, just wants a one-off chart | Create a `.ppttc` referencing a **minimal default template** (see `assets/templates/`), or guide the user to set one up | `references/templates-and-naming.md` |
| Working in Claude Cowork with PowerPoint open on a Windows machine | Use COM API via Python (`win32com.client`) — most flexible. think-cell add-in must be loaded. | `references/excel-automation.md` |

**Default recommendation:** If unsure, use **JSON automation (`.ppttc`)**. It's the cleanest path, requires no COM setup, works without Claude having to script Office, and produces a `.pptx` the user can immediately edit. The Excel COM path is for recurring report-refresh workflows.

## Required reading before generating output

Before generating any think-cell artifact (`.ppttc`, VBA macro, C# code, Python COM script, template instructions), Claude **must** read the relevant reference file(s):

- **Always** read `references/json-automation.md` if producing a `.ppttc` file. Get the exact cell types right (`string`, `number`, `date`, `percentage`, `fill`, `null`); date format is `YYYY-MM-DD`; percentages are bare numbers without `%`; decimal separator is always `.`; the first cell of row 1 is always `null` (or anything — it's discarded).
- **Always** read `references/chart-datasheets.md` for the specific chart type being produced, to know which rows mean categories vs. series vs. 100%= totals vs. Mekko widths vs. Gantt anchor dates.
- **Always** read `references/excel-automation.md` if generating VBA, C#, or Python COM code. Get the `Transposed` argument right — it differs per element type.
- Read `references/templates-and-naming.md` if the user needs help structuring or inspecting a template. When a `.pptx` template is uploaded, **run `scripts/inspect_template.py` on it first** — it lists slides, shapes, and any think-cell custom XML found, and gives you a name-candidate list to confirm with the user.
- Read `references/style-and-branding.md` if the user asks about matching company colors/fonts, datasheet fill colors, or style files.

Reading the reference is mandatory, not optional. The schema details (especially Mekko's `Size` column, scatter/bubble's dimension layout, and Gantt's anchor-date convention) are easy to get wrong from memory.

## The naming contract

Every think-cell element in the template that Claude wants to fill must have an `AddRangeData Name` (or `AddRangeImage Name` for table images) assigned via the mini toolbar in PowerPoint. **Names are case-insensitive** and must be unique within the template. If two elements share a name, think-cell fills them with the same data.

When proposing names to the user, use a clear convention:
- `SlideTitle`, `Chapter1Title` — for automation text fields holding titles
- `RevenueChart`, `MarginByRegion` — for charts
- `KPITable`, `PnLTable` — for tables
- `Source` — for the source footnote text field (if templated)

If the user hasn't set names yet, the first deliverable is a checklist of what to name in the template (see `references/templates-and-naming.md`).

## When generating `.ppttc` files

1. Read `references/json-automation.md` first.
2. Read `references/chart-datasheets.md` for the chart types involved.
3. Use the helper at `scripts/build_ppttc.py` to construct the JSON — it gets cell types right by construction.
4. Validate with `scripts/validate_ppttc.py` before presenting the file to the user.
5. Save the output as `something.ppttc` (NOT `.json`) so think-cell's file association picks it up on double-click. The file content is JSON; only the extension differs.
6. Tell the user the file pairs with a specific template (state which `.pptx`) and what each named element receives.

## When generating VBA / C# / Python COM code

1. Read `references/excel-automation.md` first.
2. Always show the user the prerequisites: think-cell installed, COM add-in `thinkcell.addin` loaded, PowerPoint Object Library referenced (VBA) or interop assemblies added (C#).
3. Default to `UpdateBatch` (modern API) over `UpdateChart` (deprecated).
4. Get `Transposed` right — re-check the table in the reference. The default for most charts is rows=series, columns=categories, so if the Excel layout puts series in columns, set `Transposed = True`.
5. Wrap COM objects with explicit close / quit / release to avoid orphaned Office processes (especially for Python `win32com`).

## When the user's request is vague

Ask clarifying questions in this priority order:
1. **Which template / which style?** (path to `.pptx`, or "no template yet")
2. **What chart type(s)?** (waterfall, stacked column, Mekko, Gantt, …)
3. **Where is the data?** (inline in the request, Excel file, JSON, database)
4. **Refresh cadence?** (one-off → JSON automation; recurring report → Excel automation)

If the user provides data inline and doesn't mention a template, proceed with JSON automation against a minimal default template and call this out explicitly: "I'll generate a `.ppttc` that targets a default template — for this to render in your house style, point it at your corporate template instead by changing the `template` field."

## Adapting to the company template (the "elsewhere in the template" requirement)

The skill cannot read minds about house style. It can, however:
- **Preserve** house style automatically by routing data through the template (since fonts/colors live there).
- **Inspect** an uploaded `.pptx` template to enumerate named elements, chart types, and datasheet layouts before generating data — do this whenever a template is provided.
- **Match Excel formatting** to chart features via the "Use Datasheet Fill" option (see `references/style-and-branding.md`) so that per-cell fill colors flow into the chart.

If the user uploads a template, the first step is always: open it, list its named elements with their types and datasheet layouts, and confirm with the user before generating data.

## Output conventions

- `.ppttc` files: pretty-printed JSON, 2-space indent, trailing newline.
- VBA: `Option Explicit` at top, explicit `Dim` declarations, comment the prerequisites block at top.
- C#: full `using` block, `Main()` that opens/closes Office cleanly.
- Python (`win32com`): wrap in `try/finally` with explicit `Quit()` calls, and use `pythoncom.CoInitialize()` if running outside the main thread.

## What this skill does NOT do

- It does not install think-cell. The user must have a licensed installation.
- It does not work without an `AddRangeData Name` on each target element — naming is a manual step in the template.
- It does not work on macOS for the COM/Excel automation path (Windows only). JSON automation works on macOS provided think-cell for Mac is installed.
- It does not modify the visual style of a chart programmatically beyond per-cell datasheet fill colors. Style changes belong in the template or in a think-cell style file (`.style`).
