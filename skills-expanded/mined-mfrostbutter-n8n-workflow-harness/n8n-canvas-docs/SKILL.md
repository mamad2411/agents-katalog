---
name: n8n-canvas-docs
description: >-
  Document an n8n workflow canvas with zone sticky notes that frame the nodes:
  no overlaps, no truncated text, no orphan nodes. Use when adding, fixing, or
  reviewing sticky notes, zone labels, setup panels, or canvas groups
  (nodeGroups) on an n8n workflow, and before deploying a workflow through the
  canvas gate. Covers the zone-board pattern, the sizing math, the
  groups-vs-stickies routing decision, and ships a zone generator, a layout
  checker, and a headless screenshot loop.
---

# Documenting an n8n canvas with zone stickies

n8n has no canvas render API. Stickies placed "by eye" from code land wrong, and
the overlap or clipped text only shows when a human opens the editor. This skill
replaces guessing with three things: a **zone spec** you write, a **generator**
that sizes and tiles the stickies by rule, and a **checker** plus a **headless
screenshot loop** that prove the board before anyone looks at it.

The checker is also a deploy gate. See `n8n-instance-ops` for where it sits in
the deploy sequence.

## The pattern: a zone board

Every reference board that reads well does the same thing:

1. **Every node lives inside exactly one zone sticky.** A zone is a coloured
   sticky sitting behind one stage of the flow (Trigger, Validate, Store...).
   No node floats outside a zone; a floating trigger reads as unfinished.
2. **Each zone has a text band at the top, then the node row.** Title (`##`)
   plus a 2-4 line body that says what the stage does and why. The nodes start
   a clear gap below the last body line, never inside it.
3. **Zones tile in rows with one gutter.** 16 px between neighbours, tops and
   bottoms level within a row. Widths differ (content-driven), gutters do not.
4. **Long flows wrap to multiple rows.** Keep a row to <= 8 columns so the whole
   board reads in one screenshot; drop the next stage to a lower node `y` and the
   generator stacks it as a new row with a wider vertical gutter (a lane for the
   wrap connector). The checker fails a row that spans more than 8 columns.
5. **Doc panels sit in their own row above the flow**: a setup / how-it-works
   panel and, for shared templates, a credits panel. Same gutter, same height.
6. **Colour carries role**, body text carries detail. A reader decodes the board
   shape from colour alone (key below).
7. **Branches stay inside their zone**, dropped to a second node row under the
   main one. The zone grows down to hold them.
8. **A fan-out leads a row, it does not close one.** Put a Switch at the END of a
   row and all of its outputs wrap backwards across the zones above it, which is
   the ugliest thing a board can do. Start the next row with it instead: one
   connector wraps and the fan reads left to right.

Keep stage captions (a small sticky hung under a node) for the rare board where
a zone background would be too busy. Do not mix the two on the same nodes.

## Measurements (taken from rendered boards at default zoom)

| Thing | Value |
|---|---|
| Regular node footprint | 100 x 100 px, `position` = top-left; name label adds ~40 px below |
| Pill-rendered nodes | An AI Agent is ~224 x 96 and an output parser ~240 x 80, because the label sits *inside*. AI sub-nodes (model, memory, tool) are 80 x 80. `footprint()` in `layout_check.py` holds the table; both scripts use it |
| Branching nodes grow DOWN | A Switch draws one handle per output and gets taller: ~32 px per output plus one. A 5-output Switch is 192 px, not 100 |
| The caption is part of the node | The name, and the subtitle under it, render *below* the box and **twice as wide**, centred, ~40 px tall. It must fit inside the zone and must not touch the next node's caption. A pill has no caption: its name is inside the shape |
| Node pitch | **208 px minimum** between adjacent full-size nodes. A caption is 2x the node wide, so the old 176 puts neighbouring labels 16 px into each other and any long name or URL subtitle collides. 80 px sub-nodes are fine at 176 |
| Sticky text | ~9.5 px per char, 22 px per line; `##` title line ~40 px |
| Node-to-zone edge clearance | >= 32 px; 64 px looks right (HTTP nodes print their URL under the label, wider than the node) |
| Text band to node row | >= 40 px of air after the last body line; title-only zones need ~96 px above the node row |
| Bottom clearance | >= 64 px under the lowest node label |
| Minimum zone width | 304 px; narrower zones wrap a 2-line body into a 5-line column |
| Gutter (horizontal) | 16 px everywhere (between zones, between the panel row and the zone row) |
| Gutter (between rows) | >= 32 px, uniform; the generator uses 48 px so a wrap connector routes through open canvas |
| Max columns per row | 8; a wider flow wraps to another row |
| Grid | every sticky x, y, width, height a multiple of 16 |

The 16 grid is not taste. n8n snaps sticky positions to 16 px on save, so an
8 px gutter becomes 4/20 the moment a human drags anything. Grid-aligned
dimensions keep the gutters even through an editor session. Snap every derived
coordinate with `round(v/16)*16`; nodes are already on the 16-grid.

## Colour key (n8n `color` 1-7)

- **Green (4)** human touchpoints: webhook/form intake, approval gates, the
  notify-a-person zone.
- **Red (3)** critical infrastructure or state: the store, the secret-bearing
  call, the one node that must not fail.
- **Blue (5)** logic and data transformation: validate, enrich, score, route.
- **Purple (6)** setup / overview panel; also domain accents, used sparingly.
- **Gray (7)** documentation panels: credits, conventions, runbook.
- **Gold (2)** outer frame when you need a frame around a frame. Rare. n8n has
  no true orange; gold is the closest.
- **Yellow (1)** n8n's default; avoid, it reads as "unfinished".

## Sticky node schema

```json
{
  "parameters": { "content": "## Title\n\nBody markdown.", "width": 400, "height": 608, "color": 5 },
  "type": "n8n-nodes-base.stickyNote", "typeVersion": 1,
  "position": [x, y], "id": "zone-02", "name": "zone-02"
}
```

`width` / `height` / `color` live in `parameters`, not top-level. Content is
markdown: `##` titles, bold, `code`, ordered lists all render. Emoji render.

## Canvas groups (nodeGroups, n8n 2.28+) vs stickies

n8n 2.28 added native **canvas groups**: a named container drawn around member
nodes that follows them when dragged.

- **Group** = structural zoning with no prose. Groups track their nodes, so they
  survive human rearranging; a background sticky does not move with the nodes it
  frames.
- **Sticky** = anything with content or a colour role. Body text, the colour key,
  title banners, setup and credits panels, stage captions. Groups carry only a
  name.

Routing: on 2.28+ prefer a **group** for bare zoning, and drop the background
sticky for that area (one zoning mechanism per area; group plus frame on the same
nodes is redundant). Keep the **zone sticky** when the zone needs a colour role or
body text, which on a documented board is almost always. Stickies layer fine
alongside groups for captions and doc panels.

Authoring goes through the `setNodeGroups` op of `n8n_update_partial_workflow`
(see `n8n-mcp-tools-expert` for the full shape). The behaviors that bite:

- It is a **full replacement**, like `replaceConnections`. Pass every group you
  want to keep; anything omitted is deleted. `nodeGroups: []` ungroups everything.
- Each group takes `nodeNames` **or** `nodeIds`, not both.
- Unmanaged edits are safe. Removing a grouped node prunes it from its group, and
  a group n8n can no longer accept is silently ungrouped; adjustments surface in
  `details.warnings`, so read them after edits to grouped workflows.
- `layout_check.py` only reads sticky nodes. It cannot see groups, so group
  membership is verified by reading back the workflow JSON, not by the checker.

## The workflow

1. **Lay the nodes out first.** One main row per stage at a single `y`, **208 px
   pitch** between adjacent nodes (see the caption row above), branches on a
   second row ~272 px lower.
   Leave 64 px of horizontal room between the last node of one stage and the
   first of the next, or let the generator shift zones to fit. Keep a row to
   <= 8 columns; drop the next stage to a lower `y` to wrap it.
2. **Write the zone spec** (`scripts/zone_layout.py` docstring has the schema):
   one entry per stage with title, 2-4 line body, colour, member node names;
   optional `panels` for setup and credits.
3. **Generate**: `python3 scripts/zone_layout.py workflow.json zones.json -o out.json`.
   It frames each zone around its members with the clearances above, levels
   each row, cascades the 16 px gutter (shifting member nodes along with their
   zone), stacks multiple rows with a uniform vertical gutter, and tiles the
   panel row above.
4. **Check**: `python3 scripts/layout_check.py out.json` must print `RESULT: ok`.
   Errors: sticky overlap, truncation, **header collision** (a node in the text
   band), **orphan node** (outside every zone), node or caption clipped by a zone
   edge, **caption collision** (two labels overlapping), row tops/bottoms not
   level, gutters uneven, **row overflow** (a row wider than 8 columns), **row
   gutters uneven or too tight** to route a wrap connector.
   Warnings: off-grid, tight clearance, nested stickies. `--strict` promotes
   off-grid and tight-clearance to errors.
5. **Push** with `PUT /api/v1/workflows/{id}` (body: `name, nodes, connections,
   settings` only) to keep the id and webhook paths. A fresh `POST` mints a new
   id and can collide on a webhook path. Ordering and read-back verification are
   `n8n-instance-ops`.
6. **Screenshot and look.** The checker is construction-time; the render is the
   truth. `scripts/shoot.js` (playwright-core + a local Chromium) logs in with
   an injected session cookie, opens each workflow, presses `1` (zoom to fit),
   and saves a PNG. Read the PNG. Fix, regenerate, re-shoot until it reads
   cleanly. Two or three loops is normal.

Orphan checks only run once the workflow has at least one zone, so a
caption-style board is not penalised for having no zones at all.

## Screenshot loop details

- **Never type a password into a tool call.** Log in once with `curl -c`
  against `/rest/login` (or `/rest/owner/setup` on a fresh instance), keep the
  `n8n-auth` cookie in a file, and have the script read the file and call
  `context.addCookies`. The cookie never enters the transcript.
- A **throwaway container** is the right render target:
  `podman run -d -p 5690:5678 -e N8N_SECURE_COOKIE=false docker.n8n.io/n8nio/n8n`.
  Import the workflow via the public API with credentials stripped (the canvas
  does not need them), shoot, iterate, then push the final JSON to the real
  instance. If you only have the live instance, shoot there; the editor is
  read-only until you save.
- If a shared Playwright MCP browser says "already in use", do not fight it;
  `npm i playwright-core` in a scratch dir and point `executablePath` at any
  installed Chromium (`~/.cache/ms-playwright/` on Linux/macOS,
  `~/AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe` on Windows).
- 1920x1080 viewport, `deviceScaleFactor: 1`, `networkidle` plus 2.5 s settle,
  `Escape` to dismiss callouts, click the canvas, then `1`.

## Gotchas

- **Default pitch is too tight.** n8n drops new nodes ~220 px apart on the
  canvas but the JSON often carries 144-176. That is fine for the icons and
  wrong for the labels: captions are twice the node wide, so they run into each
  other long before the nodes do, and it only shows once a name or a URL
  subtitle is long. Use 208.
- **Height is the usual failure.** The estimator is conservative but real fonts
  vary; empty space at the bottom of a zone is harmless, clipped text is not.
  Truncation clips silently with a fade, so err large.
- **Wide bodies in narrow zones.** If a zone is one node wide, keep the body to
  one sentence or accept a taller band; the generator grows the band, not the
  zone width beyond the minimum.
- **Orphan triggers.** Manual Trigger and Schedule Trigger often end up left of
  the first zone. Put every trigger in the intake zone.
- **Not every node is 100 px wide.** Some render as a labelled pill whose width
  tracks the node NAME, so a long name overhangs the zone while a flat 100 px
  model says the board is fine. `footprint()` carries what has been measured;
  a type that is not in it falls back to 100 x 100. When the screenshot shows a
  node crossing a zone edge that the checker passed, measure the real width in
  the browser and add the type:

  ```js
  // in the n8n editor console, canvas units
  const z = 0.851;  // read the .vue-flow transform's matrix scale
  [...document.querySelectorAll('.vue-flow__node')]
    .map(e => [e.innerText.split('\n')[0], Math.round(e.getBoundingClientRect().width / z)]);
  ```
- **Row overflow.** A single row past 8 columns will not read in one screenshot
  and the checker fails it. Wrap the flow: drop later stages to a lower node
  `y` and the generator stacks them as a new row.
- **`PUT`, do not re-`POST`** when fixing an existing workflow, to keep its id
  and webhook/form path (a form-path collision blocks activation with a 409).
- **Publish model (2.3x+).** A public-API `PUT` publishes the new version
  immediately; the internal `/rest` `PATCH` the UI uses writes a draft. After
  pushing, confirm `activeVersionId == versionId` on a `GET`, or click Publish
  in the editor.
- **Reference:** the `figma-design-build` skill covers FigJam and Figma canvases
  (a different tool with its own screenshot loop); this skill is n8n-specific.
