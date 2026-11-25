---
name: design-spec-review
description: >
  Compare a Figma design against its source screen-spec (PPTX) and produce a designer-facing
  confirm/fix request report. Use for "design review", "check the mockup", "compare figma to the spec",
  "review the design against the screen spec", "design consistency check". Works self-contained from a
  Figma URL plus a screen-spec file — no special agents or infrastructure required. If the context is
  reviewing a Figma design that has a written screen spec, consider this skill even when "figma" is not named.
---

# Design Spec Review (screen spec ↔ Figma)

Review a Figma design **against the screen spec**, and write up confirm/fix requests for the designer. Needs only a **Figma URL** and a **screen-spec PPTX**; runs standalone.

## Inputs (ask the user for both)

1. **Figma URL** — link containing a `node-id`.
2. **Screen-spec file** — the PPTX to use as the baseline. The user points at "this file / this screen".
3. Output folder — where to write the report and screen PNGs. Default: a dated subfolder in a working directory you choose.

## ★Direction (never reverse it)

- Baseline = **the screen spec**. Subject under review = **the Figma design**. Output = **confirm/fix requests for the designer**.
- Do not send the spec's own internal flaws (e.g. ID mismatches inside the document) to the designer — that belongs to whoever owns the spec.
- When the design is correct and the spec is stale (design applied a fix the spec lacks), it is not a designer request — the spec should follow.
- If the design matches, say "match". No invented issues.

## Procedure

### 1. Fix the baseline

- The spec the user names is the baseline. If several versions exist, use the highest `vN.NN`. Do not read work-in-progress or temp copies.
- Open it, confirm the version, and state `Base: <file> (version)` in your first reply.
- Match by **screen name** (spec screen name ↔ Figma page/section name). Numbers may differ; match on names.

### 2. Export the design (Playwright)

Export the Figma screens as PNG. Browser is Playwright; a logged-in Figma session is required.

1. Open the Figma URL, wait for canvas load (~5s), select screens. For a whole page/section, focus the canvas and press `Ctrl+A`.
2. Right panel **Properties** tab → click **Export** (options expand) → scale **1x**, format **PNG**.
3. Click the **run button below the options** — its label is `<section> export` or `N layers export`, a long button (not the short "Export" toggle).
4. Record the download folder state, click, wait ~8s, confirm a new `.png`/`.zip` appeared (none = permission/selection issue).
5. Unzip if needed. **1x is recommended** (enough text, less crop work).

### 3. Crop per screen (so text is legible)

The export PNG is the full canvas width and too large to read whole. With an image tool:

1. Make an overview at ~1800px wide → see the screen layout.
2. Crop only the area where the screens sit; if a screen is tall, split top/bottom (each ≤1900px) → per-screen crops.

### 4. Diff

- Read the spec PPTX (read-only, no edits) and extract each screen's copy, labels, buttons, and screen list.
  - ⚠️ Recurse into **group shapes and table cells** (group `.shapes`, table `.table.rows[].cells[]`). Flat extraction drops nested copy and leads to "not in spec → design added it" false positives.
- Compare each spec screen to its design crop. Verdicts: `[match] / [missing in design] / [differs from design] / [design-only] / [unreadable]`.
- **Shared components**: popups, headers, common bottom sheets often live on a `Common` page in Figma and are not in a screen-section export — not "missing". Check the Common page before flagging.
- No verdict without evidence (spec page N + the quoted copy).

### 5. (Optional) Comment history — separate track

Comments are not in the export PNG. To review comment issues/resolution, open the Figma **Comments** tab via Playwright and extract all (virtualized list — scroll and accumulate). **Record only the author name as written** (do not infer role/affiliation). Separate report.

### 6. Report (for the designer)

Static HTML (system fonts, no external deps, no JS data-render). Open it in a browser.

- **Drop severity and internal IDs** → only `fix request` / `confirm request` badges. Say "confirm request", not "issue".
- Per screen: **spec name + version** + **Figma page │ frame name** + **spec page (`N`)**. End each screen with one "✓ correctly implemented" line.
- **No tool/author footer** — the recipient should be able to use it directly. Version and date only.
- Most-things-match is normal. Keep only the real questions.

## 7. Review/done ledger

Reviews repeat across screens and rounds, so track what was reviewed and whether each request was handled.

- Keep `review-ledger.json` in the output folder. One review = one record: `date`, `screen`, `spec_version`, `figma_url`, `report_path`, and `requests[]` where each request has `id`, `type` (fix/confirm), `text`, `status` (open/resolved), `resolved_date`.
- On re-review: read the prior record for that screen, decide whether each earlier request is resolved in the current design/spec, update to `resolved`, and append new ones.
- Put a "N of M prior requests resolved" line at the top of the report for progress tracking.
- The ledger carries across people and sessions as long as the folder exists.

## Never

- Use a design-tool MCP plugin (design = export PNG, comments = Playwright).
- Read a work-in-progress or older version as the baseline.
- Send the spec's internal flaws to the designer.
- Infer a comment author's role or affiliation.
