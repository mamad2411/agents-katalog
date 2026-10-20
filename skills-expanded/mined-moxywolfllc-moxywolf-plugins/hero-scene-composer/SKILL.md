---
name: hero-scene-composer
description: |
  This skill should be used when the Release Owner Gate (or any future workflow) needs to compose a labeled Excalidraw story scene as the hero image for a blog post. It is invoked by skills/release-owner-gate/SKILL.md STEP 2 after the writer approves a scene draft. It takes a structured `scene-outline.json` (produced by references/story-to-scene-extraction.md), the project's brand palette (from blog-project-instructions.md `## Hero image brand style` block), and produces a complete .excalidraw.md file at <BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md plus a PNG export at <piece>/04-diligence/og-hero.png. Heroes are always labeled, narrative, literal — never abstract AI cover art. The skill never calls an image-generation model.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# Hero Scene Composer

> Single source of truth for turning a `scene-outline.json` into a rendered Excalidraw hero scene. Invoked by `release-owner-gate` STEP 2 sub-step 5.

## Inputs

1. **Scene outline** at `<piece>/04-diligence/scene-outline.json` — schema and example in `references/story-to-scene-extraction.md`.
2. **Canvas template** at `${CLAUDE_PLUGIN_ROOT}/references/excalidraw-canvas-template.json` — the 1600×900 starter with title bar, two panels, bridge arrow, and slot anchor coordinates documented in its `_slots` block.
3. **Icon vocabulary** at `${CLAUDE_PLUGIN_ROOT}/references/excalidraw-icon-vocab.md` — registry of hand-drawn icon primitives.
4. **Brand palette** from `<BLOG_PROJECT_DIR>/blog-project-instructions.md`'s `## Hero image brand style` block (or the fallback default if the block is missing): `ground`, `accent`, `secondary`, plus the fixed `ink: #1A1A1A` and `muted: #6B7280`.
5. **Post slug** — derived from the staged draft's frontmatter or filename.

## Outputs

1. **Excalidraw source:** `<BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md` — Obsidian-Excalidraw plugin native format (parsed wrapper + uncompressed JSON block). Reusable in Obsidian for manual edits.
2. **PNG export:** `<piece>/04-diligence/og-hero.png` — 1600×900, sRGB, transparent background OFF (warm ground filled).
3. **AI-transparency artifact appendix:** appended to `<piece>/04-diligence/og-hero-prompt.md` recording the scene outline path, the brand block used, every icon name resolved (and any fallbacks), and the export method.

## Algorithm

### STEP 1 — Validate the outline

Read `scene-outline.json`. Reject and abort if:
- `title` is empty.
- `left_panel.icons` length is not 2–6.
- `right_panel.icons` length is not 2–6.
- Any `icons[].name` is not a registry key in `references/excalidraw-icon-vocab.md`.

On any reject, write the reason to `<piece>/04-diligence/og-hero-prompt.md` under `## Composer rejections` and stop. The release-owner-gate caller will surface the failure to the writer.

### STEP 2 — Load and stamp the canvas template

1. Read the canvas template JSON. Strip the leading underscore-prefixed metadata keys (`_README`, `_slots`, `_brand`) — they're documentation only and must not appear in the final file.
2. Apply the brand palette:
   - `appState.viewBackgroundColor` ← brand `ground`
   - `tpl-canvas-bg.backgroundColor` ← brand `ground`
   - Every element with `strokeColor: "#2C3E50"` in the template ← brand `accent`
   - Every element with `strokeColor: "#C9A66B"` in the template ← brand `secondary`
   - Every element with `strokeColor: "#1A1A1A"` in the template ← brand `ink` (or just keep `#1A1A1A`)
3. Substitute placeholders:
   - `{{TITLE}}` ← `outline.title`
   - `{{LEFT_PANEL_LABEL}}` ← `outline.left_panel.label`
   - `{{RIGHT_PANEL_LABEL}}` ← `outline.right_panel.label`
   - `{{BRIDGE_ARROW_LABEL}}` ← `outline.bridge_arrow_label`

### STEP 3 — Compose icons into the panel slots

For each panel (left then right):

1. **Pick the grid** based on icon count using the table in `excalidraw-icon-vocab.md` "Grid placement rules". Special case: if this panel has exactly 5 icons AND the panel label or `arrow_label` contains "layer" / "tape" / "stack", use the `1×5 vertical` pattern (stacked plates).

2. **For each icon:**
   - Look up its JSON snippet in the icon registry.
   - Generate a fresh integer base `B = 200_000 + 1000 * panel_index + 100 * icon_index` for `id` / `seed` / `version` / `versionNonce` numbering.
   - For each element in the snippet:
     - Set `id` to `<icon-name>-<element-tag>-<B + element-index>`.
     - Set `seed`, `version`, `versionNonce` to `B + element-index`.
     - Resolve `fill` strings (`"secondary"`, `"accent"`, `"ground"`) to brand hex codes; assign to `backgroundColor`. Drop the `fill` key from the final element.
     - Translate coordinates: `x ← anchor.x + cell_offset.x + element.x`, same for `y`.
     - Add required fields not in the snippet (defaults): `angle: 0`, `strokeStyle: "solid"`, `roughness: 1`, `opacity: 100`, `groupIds: ["<icon-name>-<panel>-<icon-index>"]`, `frameId: null`, `isDeleted: false`, `boundElements: null`, `updated: 1`, `link: null`, `locked: false`. For arrows add `startBinding: null`, `endBinding: null`, `lastCommittedPoint: null`, `startArrowhead: null`, `endArrowhead: "arrow"`, `points`.
   - Append all translated elements to the canvas `elements` array.

3. **Append the icon's text label** below the icon's 140×140 bounding box:
   - `x = anchor.x + cell_offset.x + 0` (label spans icon width)
   - `y = anchor.y + cell_offset.y + 148` (8px below the 140px icon)
   - `width = 140`, `height = 24`
   - `fontSize = 18`, `fontFamily = 1`, `textAlign = "center"`
   - `text = icon.label` (from outline)
   - `strokeColor = brand.ink`

### STEP 4 — Render the chart (if present)

If `outline.chart.present === true`, drop a chart group into the `chart_anchor` slot.

- **`bars3`:** 3 vertical bars, leftmost shortest, rightmost tallest. Heights = 30/60/100 of slot. Fill = brand `secondary`. Below each bar, a centered text label from `outline.chart.values[i]` (fontSize 14).
- **`count_of`:** Large text "X / Y" centered in slot. `X` is `outline.chart.values[0]`, `Y` is `outline.chart.values[1]`. fontSize 48 for X (color = accent), 24 for "/" and Y (color = muted).
- **`contrast_pair`:** Two bars side by side, same height. Labels = `outline.chart.values[0]` and `outline.chart.values[1]`. The left bar fills with `muted`, the right bar with `secondary` — visualizes "before / after" or "wrong / right".

Always append the chart caption as a text element directly below the chart slot (fontSize 14, italic-effective via `fontFamily: 1`, color = `muted`, textAlign = "center"). Text = `outline.chart.caption`.

### STEP 5 — Render callouts

For each callout in `outline.callouts` (max 2):

1. Pick the anchor based on `callout.anchor` (`left_panel` → `callout_left_anchor`, `right_panel` → `callout_right_anchor`).
2. Draw a small rounded rectangle (the callout box):
   - Stroke = brand `secondary`, fill = `transparent`, `roundness: {type: 3}`, `roughness: 1`, `strokeWidth: 2`.
3. Inside, drop a text element with `callout.text`. Wrap to box width; the composer is responsible for line-breaking at word boundaries (`fontSize 16`, `fontFamily 1`, color = `ink`).

If both callouts target the same panel, stack them vertically with a 12px gap. If the chart is present, callouts shrink in width per the slot definitions.

### STEP 6 — Final integer-uniqueness pass

Walk every element in the final `elements` array. Ensure `id`, `seed`, `version`, `versionNonce` are unique integers (id may be a string, but the integer part must be unique). If duplicates are detected, increment by 1 until unique.

### STEP 7 — Wrap and write the .excalidraw.md file

Wrap the final canvas JSON in the Obsidian-Excalidraw plugin format defined in `plugins/excalidraw-vault/skills/excalidraw-vault-core/SKILL.md`. Required structure:

```
---
excalidraw-plugin: parsed
tags: [excalidraw]
---

==⚠ Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements

%%
## Drawing
```json
<the canvas JSON, uncompressed, pretty-printed with 2-space indent>
```
%%
```

Write to `<BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md`. Use `Write` (not `Edit`) — this is always a fresh file per scene.

### STEP 8 — Export PNG

Call the headless export script:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/excalidraw-to-png.mjs \
  --input "<BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md" \
  --output "<piece>/04-diligence/og-hero.png" \
  --width 1600 --height 900
```

If the script exits non-zero (commonly: `node` not installed, or the `@excalidraw/excalidraw` package not yet installed), fall back gracefully:

1. Skip the PNG export.
2. Write `<piece>/04-diligence/og-hero-export-instructions.md` with:
   - The path to the `.excalidraw.md` source.
   - One-line instruction: *"Open the source in Obsidian, switch to Excalidraw view, then File → Export Image → PNG at 1600×900. Save to `<piece>/04-diligence/og-hero.png`."*
   - A note that the gate will block on a missing PNG, so this is required before signing.
3. Surface the fallback to the release-owner-gate caller (which surfaces to the writer).

The plugin **never** calls an AI image generator. This is intentional and permanent.

### STEP 9 — Write the AI-transparency artifact

Append (or create) `<piece>/04-diligence/og-hero-prompt.md`:

```markdown
# Hero Scene — Generation Record

**Style:** excalidraw-story (labeled Excalidraw scene composed from post artifacts)
**Source file:** <BLOG_PROJECT_DIR>/drafts/blog-media/<slug>.excalidraw.md
**PNG output:** <piece>/04-diligence/og-hero.png
**Export method:** headless `@excalidraw/excalidraw` via scripts/excalidraw-to-png.mjs
  (or: "by hand in Obsidian Excalidraw view" if the script fallback was used)

## Brand palette used
- ground: <hex>
- accent: <hex>
- secondary: <hex>
- ink: <hex>
- muted: <hex>

## Scene outline
<verbatim copy of scene-outline.json>

## Icons resolved
- Left panel: <icon-name> (label "<label>"), <icon-name> (label "<label>"), ...
- Right panel: <icon-name> (label "<label>"), ...

## Composer warnings
<none, or list of fallback substitutions if any icon name was missing from the registry>

## What this is not
This scene was not generated by any image model. It is a deterministic composition
from the post's H1, H2s, named concrete nouns, and a structured icon vocabulary.
The same outline + the same registry + the same brand palette will always produce
the same scene.
```

## Idempotency

Running the composer twice on the same outline + brand palette must produce a byte-equivalent `.excalidraw.md` (ignoring `updated` timestamps if any) and a byte-equivalent PNG. Seeds and IDs are derived deterministically from panel and icon indices, so no randomness leaks in.

## Failure modes

| Cause | Behavior |
|---|---|
| `scene-outline.json` missing or invalid | Abort with reason logged to og-hero-prompt.md; do not call back into release-owner-gate other than to surface the rejection. |
| Icon name missing from registry | Substitute `notebook`, log the substitution under "Composer warnings", continue. |
| `excalidraw-to-png.mjs` missing or fails | Skip PNG, write export-instructions.md, surface to caller. The gate will block until the writer drops the PNG manually. |
| Brand palette missing from project marker | Use the fallback default (warm off-white / deep navy / muted gold / `#1A1A1A` / `#6B7280`). Log under "Composer warnings". |

## Why this design

The hero used to be generated by an image model from an abstract prompt. The writer rejected that output ("we need to change the graphic to be something that relates to the story"). This skill replaces that path with a **deterministic, story-grounded, vocabulary-driven** composition:

- Every hero looks like an editorial infographic, not abstract cover art.
- Every hero is derived from the post's actual H1, H2s, and named entities — never invented.
- Every hero is editable in Obsidian after generation — the `.excalidraw.md` source is the canonical artifact.
- Every hero is reproducible — same inputs, same output, byte-for-byte.
- No image model is ever called for heroes. The plugin enforces this via the absence of an image-gen call site.
