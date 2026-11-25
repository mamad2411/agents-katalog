---
name: moda-deck-pptx
description: >-
  Import a .pptx into Moda as an editable canvas, then fix it. For "clean up
  this PowerPoint" or any .pptx in hand. CLI lane; the connector routes to the
  app.
argument-hint: "[path to the .pptx] [what to fix] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-deck-pptx

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Sizes and defaults

| Thing | Value | Notes |
|---|---|---|
| Import | `moda canvas import-pptx [file.pptx]` | FREE, un-billed, async — the verb polls to completion |
| Result | one canvas, one page per slide | slide size is preserved from the file |
| Round trip | `moda export … --format pptx` | native shapes and text layers, not screenshots |
| Data law | every source string and number survives verbatim | a cleanup that loses data is a failure |

Import takes a local path or a durable `file_…` ref. Nothing is generated and
nothing is charged; the import is the cheapest useful thing you can do with a
deck someone hands you.

## Recipe — import, then fix

1. `moda canvas import-pptx [deck.pptx]` — free, async, polls itself to completion (`--no-wait` returns a job id; re-poll with `moda canvas import-pptx --job [JOB_ID]`). Send the canvas link the MOMENT it exists.
2. `moda canvas read [CANVAS_REF] --summary` — the page index and what landed on each slide.
3. `moda canvas screenshot [CANVAS_REF] --page [IDS]` in ≤3-page batches, worst slides first. Judge with your own eyes; list the fixes before making any.
4. Fix smallest-change-first, one slide at a time: `moda canvas edit [CANVAS_REF] --file fix.js` for targeted property changes (references/edit-code.md); `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID] --mode replace --revision [REV]` to rebuild a slide outright (grammar: references/markup.md); `moda canvas delete-items [CANVAS_REF] [NODE_IDS]` for cruft. Data preservation is non-negotiable — restate every source string and number verbatim.
5. Re-theming to the team's kit? `moda canvas brand [CANVAS_REF] [KIT]` records the kit; the tokens still have to be authored into the slides (kit creation itself is moda-brand's job).
6. `moda canvas screenshot [CANVAS_REF]` again and compare against your fix list.
7. Deliver the live link; export back only on a format word or an accepted offer: `moda export [CANVAS_REF] --format pptx -o [deck]-clean.pptx`.
8. **Read the export warnings** — `pptx_shape_rasterized` (an image baked in rather than editable) and `pptx_content_dropped` (an element missing entirely) name exactly what did not survive. Repair or disclose; never hand over a silently degraded deck.

## Examples

- "clean up this PowerPoint" → import, screenshot the worst slides, fix, export.
- "put our brand on this deck" → import, bind the kit, re-author the tokens.
- "what's actually in this deck?" → import + `read --summary`; no edits unasked.
- "fix slide 7's chart" → import, then the targeted-edit step on that page only.
- "build a NEW deck from this content" → moda-deck owns authoring from scratch.

## Errors

Any typed error → load moda-core and read its recovery reference.
An import that fails or returns an empty canvas is a file problem, not a retry
problem: say what happened, then `moda ask "<question>"` with the task error.

## Make it recurring

The cleaned deck is the team's canonical starting point — flag it with
`moda canvas template [CANVAS_REF]` via moda-templates, so the next deck starts
there instead of from another crufty .pptx.

See also: moda-deck — authoring a deck from a brief, doc, or notes ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/deck-design.md | judging and rebuilding an imported slide |
| references/edit-code.md | before any targeted fix program |
| references/export.md | the pptx round trip and its warnings |
