---
name: vilsem-powerbi-visuals
description: Build, preview and add custom Power BI visuals with the vilsem MCP server (tools named mcp__vilsem__* or vilsem.*). Use when the user wants a custom, complex or "website-style" visual in a Power BI report (Sankey, calendar heatmap, KPI hero, leaderboard, radar, funnel, small multiples, any ECharts-style chart), wants to edit an existing vilsem visual, or asks why a vilsem visual looks wrong in Power BI Desktop. Covers PBIP/PBIR project prep, model discovery, data checks with DAX, spec authoring, preview/critique loops, committing to pages, and known vilsem workarounds.
---

# Building Power BI visuals with vilsem

Call `get_playbook` without arguments before authoring; request sections as needed. Clients supporting resources may instead read `vilsem://skill/powerbi-visuals`.

vilsem is the **custom-visual layer** for agentic Power BI authoring. It reads the model, runs read-only DAX, renders previews of a declarative ECharts-based spec, and writes **its own visuals** into PBIR pages.

It does **not** create pages, native visuals, slicers, bookmarks, filters or themes, and it never changes the semantic model. Do those yourself by editing the PBIR files (see `references/pbir-pages.md`) or with other tools, such as the Power BI Modeling MCP for model changes.

## Division of labour: vilsem draws, you do everything else

vilsem deliberately does one job: preview, validate and write its own visuals. Everything around that is **your** job as the agent. Don't stop and report "vilsem can't do X" when you can do X yourself:

| Need | Who does it |
|---|---|
| Find the project, the `.Report` folder and the Desktop port | You: file search, the Modeling MCP's `ListLocalInstances`, or `kind:"desktop"` |
| Read measure DAX, columns and relationships | You: the TMDL files, or the Modeling MCP |
| Check the data's grain, ranges and sanity | You: `run_dax` |
| Create pages | You: edit the PBIR files (`references/pbir-pages.md`) |
| Prototype measures for one visual | You: visual-scoped measures in the spec (preview only) |
| Persist measures for a committed / shared visual | You: add them to a model measures table in TMDL (with the user's OK), or the Modeling MCP |
| Fix the model itself | The Modeling MCP, **only if the user asks** |
| Work around vilsem limitations | You: patterns in `references/spec-cookbook.md` |
| Preview, validate, commit and update visuals | vilsem |

When you work around something, tell the user what you did and why, in one line.

## Ground rules

- **Preview before commit, always.** Never commit a spec you have not rendered against real data.
- **Check the data before designing.** Most broken visuals come from grain, blanks or measure semantics, not chart code.
- **Never silently replace a business measure.** If a model measure looks wrong (e.g. a rate above 100%), say so and explain what you used instead.
- **Ask the user before touching the model, once, up front.** Ask: "Will this report be published or shared (Service, Publish to web, other authors)?" If yes, committed visuals should bind **model measures**, not visual-scoped ones (see "Measures for shareable reports"). Visual-scoped measures remain fine for previews and for private prototypes. Asking about sharing does not itself authorize a model change; obtain the user's OK for those edits.
- **Keep the user's Desktop state safe.** After any file write, tell them to accept the reload prompt and not to save stale Desktop state over your changes.

## Workflow

### 1. Locate the project

- vilsem needs a **PBIP project** using enhanced PBIR. A `.pbix` must first be saved as PBIP in Desktop; vilsem cannot patch a PBIX.
- Pass the absolute path of the **`<Name>.Report` folder** (it contains `definition/pages/`), not the `.pbip` file.
- Recommend a test copy of the project for first experiments.

### 2. Connect

1. Try `connect_model` with `{"kind":"report","reportDir":...}`.
2. **Check `schemaOnly` in the result.** If it is `true`, previews and DAX will not work. Reconnect with `{"kind":"desktop","port":<port>}`. `{"kind":"desktop"}` auto-detects when only one model is open; with several open, the error lists each open session's **port and `.pbip` path**, so pick the right port from it (or use the Modeling MCP's `ListLocalInstances`).
   - If the error says the model **has no model loaded yet**, the report is still opening in Desktop (large models take a minute). Wait and retry; don't switch strategy.
3. **Ports change every time Desktop reopens.** If calls fail with "A connection cannot be made", find the new port and reconnect. Old `connectionId`s are dead.

### 3. Understand the model cheaply

- **On large models, call `get_schema` with `profile:false` first.** It returns tables, columns, measures and their format strings in seconds without running any query. Then profile only what you need: `get_schema` with `tables:["Product","Date"]`.
- Default profiling stops after about 20 seconds; columns it didn't reach are marked `profileSkipped` and the result has `profileIncomplete`. Results are cached until `refresh:true`, so don't call it repeatedly.
- Prefer, in order:
  1. The TMDL files under `<Name>.SemanticModel/definition/tables/` (column names; `grep` for `column` / `measure`).
  2. The Modeling MCP: list measures, get specific measure DAX, and `GetStats` for table and measure counts.
  3. Targeted `run_dax` queries for the tables you actually need.
- **Read the DAX of every measure you plan to bind.** Look for:
  - `COALESCE(..., 0)` or `+ 0`: the measure returns 0 instead of BLANK, so a date axis will include every date in the calendar table.
  - Text measures (`FORMAT(...)`): they cannot be plotted. Recompute the number in a visual-scoped measure.
  - Ratios: never sum or average them in the visual. Evaluate them at the right grain in DAX.
  - Measures on DirectQuery or remote tables, which may be unreachable. Test with `run_dax` first. If a table's source can't be reached (e.g. "workspace not found"), every visual using it will fail. Find an equivalent local table, or tell the user.
  - **Snapshot columns** (active clients, inventory, balances): summing them across days or weeks inflates the number. Take the latest snapshot in context instead, e.g. `CALCULATE(<ratio>, LASTNONBLANK(DimDate[FullDate], CALCULATE(SUM(<snapshot col>))))`.

### 4. Probe the data with `run_dax` before designing

Check four things:
- **Range and grain:** min and max dates, the number of categories, and which fact table the measures come from.
- **Whether dimensions are shared.** If each fact table has its own `appttype` column, filter only within one fact table.
- **What each column actually means.** For example, a "lead-time bucket" may be stored against the booking-creation date, not the appointment date.
- **Sanity of rates.** Rates above 100% or below 0 point to a broken measure.

Wrap `SUMMARIZECOLUMNS` in `FILTER(..., [m] > 0)` when measures return 0, or you will get thousands of empty rows.

**Two traps worth checking on every measure you plot:**
- **The same value on every row** (e.g. `$6.4M` for every year) means the measure ignores that dimension (often an `ALL()` inside it). Don't plot it; pick another measure or tell the user.
- **Time-intelligence % measures** (`YoY %`, `MoM %`) often return **-100%** for empty or future periods. Guard with a visual-scoped measure: `IF(ISBLANK([Base]), BLANK(), [Base YoY %])`. Never silently drop the period without saying why.

**Check comparisons in total and within each group.** If an overall rate and the per-category rates point in opposite directions (Simpson's paradox), show both and say so. For example, one booking method had the lower no-show rate overall but the higher rate within the largest appointment type.

### 5. Pick the design

- Call `list_templates` (no arguments) for a compact list: id, name, description and slots. Use `search:"sankey"` to filter, and `id:"<id>"` to get one complete template with its `exampleSpec`. Avoid `full:true`: it returns every template in full (about 550K characters).
- Start from the closest shipped template and adapt it. For custom layouts, see `references/spec-cookbook.md`.
- **Limits:** at most 6 dimensions and 6 measures per visual. Power BI sends at most about 2,000 rows to the visual. Aggregate or limit with visual-scoped measures.

### 6. Author the spec

- Envelope: `{"version":1,"type":"custom","config":{"cardStyle":"plain"},"measures":{...},"template":{meta, slots, params, transforms, template}}`. Use `meta.formatVersion: 2`.
- **Slots fill in declaration order** from the bindings: dimensions first in the order bound, then measures in the order bound.
- Tokens must be the **entire string value**:
  - Slot data: `$slot.<name>.values`, `.categories`, `.pairs`, `.pairsSwapped`, `.dateRange`.
  - Slot summaries: `.last`, `.sum`, `.max`, and the `*Label` variants.
  - Theme: `$theme.palette.<i>`, `$theme.textPrimary`, `$theme.textMuted`, `$theme.gridStroke`, `$theme.background`, `$theme.font`.
  - Transform results: `$calc.<as>.*`.
- **Visual-scoped measures**, which keep the model untouched:
  - Shape: `"measures":{"name":{"expression":"DAX","format":"0.0%"}}`.
  - Names must not collide with model measures or columns.
  - Bind them with `{"table":"<an existing table>","name":"name"}`. Every scoped binding uses the first measure binding's table.
  - Use them for windows (return BLANK outside a date range), top-N (`IF([rank] <= 15, ...)`), constants broadcast to every row, and numeric copies of text measures.
- Formatting:
  - **Show large values in compact units by default with `{value:compact}`** ($9.9B, 14.6K, 950): it scales K/M/B/T and keeps only the bound measure's currency symbol, so **no scaled visual-scoped measure is needed** (that keeps the visual Publish-to-web safe). Use it on labels and value axes (`axisLabel.formatterTemplate`). It needs renderer 4.45+; `commit_visual` refuses older registered renderers with an upgrade message.
  - Use `formatterTemplate` with `{value}`, `{value:compact}`, `{value:thousands}`, `{value:percent}`, `{value:date}`, `{name}`, `{label}`, `{d}`.
  - **Tuple data** (`.pairs`, `.pairsSwapped`, points) holds `[value, category]`: plain `{value}` prints the **last** element (the category). Use `{value.0:percent}` / `{value.0:compact}` to pick the number.
  - If a unit is already in the measure format (e.g. `$0.0"M"`), don't add it again in the formatter: `$14.6MM` in a preview means the unit was applied twice.
  - Functions and JavaScript strings are rejected.

### 7. Validate, preview and iterate

- Run `validate_spec` (it needs `connectionId` when the spec declares measures), then `preview_visual` with the visual's real `width` and `height`, `reportDir`, and enough `maxRows`.
- **Look at the PNG.** The critique catches truncation, contrast and missing formats.
  - Contrast warnings for white text on dark fills are usually false positives.
  - `all-zero` warnings usually mean a grain or filter problem.
- Iterate until the numbers in the image match your DAX probes.

- **Iterate cheaply:** use `preview_variants` (one spec) while iterating, `preview_visual` only when you need the option JSON, and the no-op `update_visual` dry run to view committed visuals.
- **Reconcile before committing:** check the preview's numbers against a `run_dax` total. For example, the top-N bars plus the excluded remainder should equal the grand total; say so in the report-back.
- **Test one filtered state** for layouts that depend on index or rank (Sankey node lists, grids), so an empty slot doesn't break the visual.

### 8. Make sure the page exists

`commit_visual` only adds to **existing** pages. If the user wants a new page, create it in the PBIR files first (`references/pbir-pages.md`). Use the page's internal `name` (the folder id), not its display name, as `pageName`.

### 9. Commit

**Relay the tool's `nextStep` verbatim; don't infer the reload step yourself.**

If the user doesn't give a size, choose one from `list_pages` that keeps all text readable and avoids overlap. Don't default to small tiles. If a size is fixed, scale fonts, label density and margins to it (e.g. `fontSize` from `viewportWidth`, hide secondary labels), and re-check the critique's text-bounds and overlap findings before committing.

- Call `commit_visual` with the page, a unique `visualName`, the layout (page pixels; 16px margins on a 1280×720 page gives x=16, y=16, w=1248, h=688), the spec and the bindings.
- **Tell the user how to see the change in Desktop.** The step depends on whether this is the report's first vilsem visual:

  | Situation | What the user sees | What the user must do |
  |---|---|---|
  | **First vilsem visual in this report** (`commit_visual` returns `rendererRegistered: true`) | The visual fails to render: *"To see this custom visual, add it to this report first: semanticaRenderer…"* | **Close the report without saving and reopen the `.pbip`.** The renderer is registered in `report.json`, which Desktop only reads when it opens the project. |
  | **New pages added** | Desktop shows an external-changes prompt, or the page is missing | Try **apply / reload external changes** first; close without saving and reopen if the page is still missing. |
  | **Model measures added or changed** (TMDL edits) | Nothing changes after "apply external changes" | **Close without saving and reopen.** External-change reload covers report files, not the semantic model. |
  | **Every later commit or update** (`rendererRegistered: false`) | Desktop shows a prompt about external changes to the project files | Click **apply / reload external changes** in that prompt. No restart needed. |

  - In all cases: **don't save in Desktop before reloading or reopening**, or Desktop overwrites the new files with its stale state.
  - Alternative for the first time only: import `<install>/node_modules/@vilsem/core/assets/renderer.pbiviz` (Visualizations pane → ⋯ → Import a visual from a file), save, then commit.
  - Tell the user this **up front** with the first commit, so they don't think the visual is broken.

### 9a. Measures for shareable reports

Visual-scoped measures (`spec.measures`) are committed as `NativeMeasure` projections, which Power BI stores as report-level extensions. That has two consequences:

- The **Build pane shows no fields** for those visuals.
- **Publish to web fails** on every such visual with `PowerBIAnonymousExtensionSchemaException`. The signed-in Service still works, so this is easy to miss.

So use `spec.measures` as a **preview scratchpad**, and commit model measures. Do it at commit time so there is no rework later:

**Use the bundled script instead of writing your own.** Requires **Python 3.9+** (stdlib only); if Python is unavailable, follow the manual steps below. The target measures table must already exist; create it in Desktop and save before external edits. Save any existing Desktop work before running the script. `scripts/promote-measures.py` does steps 2–3 for every Vilsem visual in a report that still has visual-scoped measures. Ask the user before running it with `--apply`, because it changes the model files:

Run these commands from the installed `vilsem-powerbi-visuals` skill folder, or use the script's absolute path. The npm package also contains it under `skills/vilsem-powerbi-visuals/scripts/`.

    python scripts/promote-measures.py "<Name>.Report"                          # dry run: shows the plan, writes nothing
    python scripts/promote-measures.py "<Name>.Report" --table "<Measures table>" --apply

It backs up every file it changes, tags created measures `annotation VilsemOwned = true`, refuses name collisions with non-Vilsem measures, and is idempotent. Afterwards: close Desktop without saving, reopen, run `validate_visuals`.

**Migrating an existing report** works the same way: run the script on it. (What it does: for each Vilsem `visual.json`, parse the `primitiveSpec` literal, take `spec.measures`, write them to TMDL as described below, then for each projection with `field.NativeMeasure` replace `field` with `{"Measure":{"Expression":{"SourceRef":{"Entity":"<Measures table>"}},"Property":"<name>"}}`, set `queryRef` to `"<Measures table>.<name>"` and `nativeQueryRef` to `"<name>"`, and drop `measures` from the spec.)

**Manual equivalent (when Python is unavailable):**

1. **Design and preview** with `spec.measures` as usual. Nothing is persisted.
2. **When the visual is final**, write each measure into a measures table in the model's TMDL (e.g. `<Model>.SemanticModel/definition/tables/<Measures table>.tmdl`):
   - `measure '<name>' = <DAX>` (use a ```` ``` ```` block for multi-line DAX)
   - `formatString: "<format>"` (escape `"` as `""`)
   - `displayFolder: "Vilsem\<page display name>"`
   - a new `lineageTag: <uuid>`
   - optional `/// Vilsem measure used by visual '<visualName>'` description
   - Names must be unique across the model. Insert the measures before the table's first `column`/`partition`.
3. **Commit the visual bound to the model measures**: bindings `{"table":"<Measures table>","name":"<name>"}`, and remove `measures` from the spec.
4. **Batch:** model changes need Desktop to **close (without saving) and reopen**, so promote a batch of visuals and reopen once, not per visual.
5. **Report back:** list the measures you added and their folder.

If the model must not be changed (user says no), commit with `spec.measures` and tell the user up front: *"These visuals use visual-scoped measures: the Build pane won't list their fields and Publish to web won't render them. Promote them to model measures before publishing."*

**Unloaded-measure verification is pending.** The order above is not yet verified for a new model measure written to TMDL while Desktop is still running its old model. On a test copy, check `validate_spec`, `commit_visual` and `validate_visuals` before reopening (see `docs/qa/model-measures-and-install.md`). If a tool rejects the unknown measure, use **write TMDL -> close without saving/reopen -> rediscover the port and reconnect -> preview -> commit**, batching promotions before one reopen. Re-preview model-bound specs after reconnecting; do not treat a scratchpad preview as proof that persisted bindings work.

### 10. Edit later

Use `update_visual`:
1. Send an RFC 6902 patch with `dryRun:true` and review the before/after PNGs.
2. Send the same patch with `dryRun:false` and the returned `etag`.

Paths look like `/template/template/series/-`. Don't re-commit under the same name; it is refused.

### 11. Report back

Tell the user:
- Which page or pages changed, and what to do in Desktop (reload, or close and reopen).
- The key numbers the visual shows, so they can cross-check them.
- Any substitutions you made: measures you replaced, windows you applied, data you excluded.
- What is not verified: host interactions such as cross-filtering, and scoped measures inside Desktop.

## Working with the user

- **Don't run long exploration silently.** Full-model profiling or reading hundreds of templates can take minutes; users will interrupt. Do a fast, targeted look, then **propose 3–4 concrete visual ideas** with the fields they'd use, and let the user pick.
- For multi-visual requests, give a one-line update as each visual is previewed and committed.
- Show the key numbers from each preview, so the user can sanity-check them against what they know.
- When you change the design for data reasons (e.g. a "funnel" whose stages aren't sequential, or a measure above 100%), say what you changed and why before you commit.

## Environment and setup gotchas (Windows)

- **npm in PowerShell:** use `npm.cmd`, which avoids execution-policy errors. The warning `install-scripts … vilsem-mcp (prepare: npm run build)` is harmless for the release tarball, because `dist/` is prebuilt. Check that `node_modules/vilsem-mcp/dist/index.js` exists.
- **`claude` CLI not on PATH** (common with the VS Code extension): the extension bundles it at `%USERPROFILE%\.vscode\extensions\anthropic.claude-code-*\resources\native-binary\claude.exe`. Use that to run `claude mcp add --scope user …`.
  If no bundled binary exists either, add the server to `%USERPROFILE%\.claude.json` under a top-level `"mcpServers"` key, or a project `.mcp.json`:
  `{"mcpServers":{"vilsem":{"type":"stdio","command":"node","args":["C:/Users/<you>/vilsem-mcp/node_modules/vilsem-mcp/dist/index.js"]}}}`
  Edit by parsing the JSON, setting `mcpServers.vilsem` and writing it back, after backing up the file. Never splice strings. Close Claude Code first so it does not overwrite the file.
- **New MCP servers need a client restart** (VS Code: Developer: Reload Window) before their tools appear.
- **Python printing model data on Windows:** set `PYTHONIOENCODING=utf-8`, because template metadata contains emoji and the default code page will crash.
- **The Power BI Modeling MCP can drop its connection,** especially after Desktop restarts. Reconnect with `ListLocalInstances` → `Connect`. If the server itself is down, fall back to the TMDL files and `run_dax`.

## Known vilsem issues and workarounds

Applies to renderer 4.45 / core 0.8.2.

| Symptom | Cause | Workaround |
|---|---|---|
| Publish to web shows an error on every Vilsem visual (`PowerBIAnonymousExtensionSchemaException`) | Visual-scoped measures are report extensions, unsupported in anonymous embed | Promote to model measures and rebind (section 9a), republish |
| Build pane shows no fields when a Vilsem visual is selected | Same: `NativeMeasure` projections | Same fix |
| First vilsem visual shows "To see this custom visual, add it to this report first" | Renderer registration in `report.json` isn't live-reloaded | Close the report without saving and reopen it (one time per report). After that, applying the external-changes prompt is enough. |
| Report on an older renderer, or `commit_visual` says the visual requires a newer renderer | Reports keep the renderer they registered; installing a new MCP does not change them. `{value:compact}` needs 4.45; the HTML-measure security fix needs 4.44 | Tell the user once: import the bundled renderer.pbiviz (Home > More visuals > From my files, accept Update, save, close and reopen). Never edit the GUID or replace registered resources yourself. Until then, avoid `{value:compact}` in that report. |
| Visual looks blurry in Desktop with an older renderer | Reports retain their registered renderer | Upgrade to renderer 4.43 or later (import the bundled renderer.pbiviz, save, close and reopen). Canvas accounts for page zoom; use `config.renderer:"svg"` or Appearance > Render mode for text-heavy layouts. Canvas-only trail/blend effects fall back with a warning. |
| KPI shows `0.04` instead of `4.2%` | `lastLabel`, `sumLabel` and `deltaPctLabel` ignore the measure format | Draw the number as a hidden gauge's `detail` with `formatterTemplate:"{value:percent}"` (see the cookbook), or show it in a formatted data or axis label |
| Previews have no data after connecting by `reportDir` | Silent fallback to `schemaOnly` | Reconnect with `kind:"desktop"` and the port |
| "Connection cannot be made" | Desktop was reopened and its port changed | List the instances and reconnect |
| `get_schema` is slow on a large model | Column profiling (about 110 s on 10M rows before 0.9.2) | `profile:false` first, then `tables:[...]`; default profiling stops after about 20 s |
| Years/months render in the wrong order in races, timelines and custom series | Rows arrive in **query order**; plain `dimension` slots aren't sorted chronologically | Bind the year/month field to a slot with `"kind":"time"`. For text periods ("Q1-2017", "Sep 2025") bind a numeric sort column (e.g. `YearMonthNumber`, `MonthNumber`) and supply labels separately. |
| Two items drawn on top of each other in rank-based layouts | `RANKX` ties caused by floating-point noise in the value | Wrap **both** the expression and the explicit value argument in `ROUND(…, 0)`: `RANKX(ALLSELECTED(T[c]), ROUND(CALCULATE(…),0), ROUND(CALCULATE(…),0))` |
| A rank meant to be global restarts within each category | The category is still in filter context inside `RANKX` | Remove it inside the ranked table, e.g. `CALCULATETABLE(VALUES(Product[Sub]), REMOVEFILTERS(Product[Sub], Product[Category]))` |
| A literal string such as `"$1,834M"` disappears or errors | Strings **starting with `$`** are parsed as tokens | Don't author `$`-prefixed literals. Put the number in a slot and format it (`formatterTemplate`, or the hidden-gauge pattern in the cookbook). |
| Preview is fine but the visual **hangs Desktop** | Heavy per-row DAX, e.g. `AVERAGEX`/`STDEVX` over all dates evaluated for every row | Keep DAX to one cheap value per row; compute statistics with `stat`/`calculate` transforms instead. |
| Preview or query fails after about 30 s | Set-heavy DAX (`INTERSECT`/`EXCEPT` over large customer sets) across several measures | Keep at most 2–3 such measures per visual. Derive the rest with transforms (e.g. `window` `lag`) instead of more DAX. |
| Bar-race labels are nearly invisible on a dark background | `axisLabel` colour set on the base `yAxis` is overridden per timeline frame | Set `yAxis.axisLabel.color` inside the **per-frame** options (`options[].yAxis`). Check the critique's contrast numbers. |
| `fontStyle` in an expression text style is refused | Not an allowed style property in the expression language | Use `fontWeight`/`fontSize`/`fill` only. |
| A `graphic` outline rectangle is cut off in Desktop | Container clipping differs from the preview | Avoid outline rects at the edges; use filled panels with an inset, or the card style. |
| A comparison chart shows flat, near-identical bars | The data has no variance for that KPI (**synthetic or sample datasets** (e.g. Contoso) often have near-identical margin %, AOV, units/order and discount across groups) | Probe variance with `run_dax` **before** designing comparisons. Pick KPIs that move (growth, orders per customer, sales per customer, share). |
| Labels show a doubled unit (`$14.6MM`) | The value was scaled in DAX with a unit in its format string, and the formatter added the unit again | Apply the unit in one place only. |

## References

- `references/data-art-recipes.md`: eight model-neutral data-art recipes; fetch `get_playbook` section `art`, then `art:<slug>`. These are examples, not shipped templates.
- `references/pbir-pages.md`: creating pages, the PBIR layout and Desktop reload rules.
- `references/spec-cookbook.md`: proven layout patterns, each verified against a real model: KPI hero, formatted KPI numbers, sorted leaderboard, calendar heatmap, Sankey, funnel with donut, radar with company baseline, butterfly bars, date-window and top-N measures.
