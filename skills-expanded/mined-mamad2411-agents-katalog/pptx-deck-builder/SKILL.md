---
name: pptx-deck-builder
description: >
  Build enterprise PowerPoint decks using the `pptx` and `excal` CLI tools.
  Use this skill whenever the user wants to create a PowerPoint presentation,
  generate slides from a template, build a deck with diagrams, or produce
  consulting-style slide content. Also triggers for requests involving
  .pptx files, slide decks, presentation generation, Excalidraw diagrams
  for slides, or McKinsey/consulting-style deliverables. If the user mentions
  "pptx", "excal", "slides", "deck", "presentation", or "PowerPoint" in the
  context of creating output, use this skill.
---

# pptx + excal Deck Builder

Build template-bound, validated PowerPoint decks with professional diagrams.
This skill combines two CLI tools (`pptx` for slide generation, `excal` for
diagrams) with consulting-grade presentation principles.

## When to read the reference files

- **`references/pptx-workflow.md`** — Read when you need the full `pptx` CLI
  command reference, manifest structure, placeholder details, deck spec format,
  error codes, or image-handling workarounds.
- **`references/excal-diagrams.md`** — Read when you need to create Excalidraw
  diagrams, render them to PNG, or understand the scene JSON format.
- **`references/mckinsey-style.md`** — Read when the user asks for
  consulting-style, executive, strategy, or McKinsey-style presentations. Also
  read when you need guidance on action titles, storyline structure, slide
  archetypes, or the Pyramid Principle.

---

## Core workflow

Every deck project follows this sequence. Do not skip steps.

### Step 0 — Think before building

Before touching any tool, resolve the presentation's purpose:

1. What decision or outcome is this deck driving?
2. What is the single governing thought or recommendation?
3. What are the 3-5 supporting arguments?
4. What evidence proves each argument?

If the user's request is vague, ask clarifying questions. A deck without a
clear purpose becomes a collection of slides instead of an argument.

For consulting-style decks, write a **ghost deck** first — a title-only
outline where each slide title states the takeaway (not the topic). The titles
alone should tell a coherent story. See `references/mckinsey-style.md`.

### Working from a YAML input file

When the user provides a YAML (or similar structured) file that already
contains slide content, treat it as the authoritative source. The file
typically defines `slides:` with per-slide fields such as `title`, `body`,
`notes`, `table`, `chart`, and `image`.

**Carry over every field.** Walk through each slide in the input and map
every field into the deck spec. The most common mistake is silently dropping
fields that do not map to a placeholder — especially `notes`. Always include:

- `title` and `body` → map to the layout's `title` and `content_1`
- `notes` → map to the slide-level `notes:` key in the deck spec
- `table` → map to a `{ kind: table, ... }` content block
- `chart` → map to a `{ kind: chart, ... }` content block
- `image` → map to a `{ kind: image, ... }` content block

**Do not summarize, rewrite, or omit content** unless the user explicitly
asks for editing. The goal is faithful conversion from the input format to
a template-bound deck spec, not reinterpretation.

**Checklist before building:** after writing the deck spec, verify that:

1. The number of slides matches the input.
2. Every `notes:` block from the input appears in the spec.
3. Every table, chart, and image from the input is present.
4. Source attributions are preserved.

### Step 1 — Initialize the manifest (one-time setup)

Check if a manifest package already exists. If not, initialize from the
template. Do not assume a PowerPoint template exists; ask the user for
the actual template path when it is not already present in the workspace:

```bash
pptx init <template.pptx> --out ./corp-template --format json
```

Then run the doctor to verify compatibility:

```bash
pptx doctor --manifest ./corp-template --format json
```

### Step 2 — Discover layouts and placeholders

List available layouts, then inspect placeholders for the ones you plan to use:

```bash
pptx layouts list --manifest ./corp-template --format json
pptx placeholders list <layout-id> --manifest ./corp-template --format json
```

Read-only commands can run in parallel for speed. Key information per
placeholder:

- `logical_name` — The key to use in your spec (e.g., `title`, `content_1`)
- `placeholder_type` — `title`, `body`, `object`, or `picture`
- `supported_content_types` — What it accepts (`text`, `markdown-text`,
  `image`, `table`, `chart`)
- `required` — Whether it must be filled
- `estimated_text_capacity` — Preferred normalized guidance for text-capable
  placeholders. Read `max_lines` first, then check `confidence`, `source`,
  and `font_size_pt`.
- `text_defaults` — Raw extracted placeholder hints such as suggested font
  size or explicit `max_lines` from the template text
- `left_emu`, `top_emu`, `width_emu`, `height_emu` — The actual geometry.
  Treat `width_emu` and `height_emu` as hard constraints for how much content
  the placeholder can realistically hold.

For slide drafting, prefer `estimated_text_capacity.max_lines` over parsing
`text_defaults.max_lines` directly. Treat it as guidance, not a hard rule:
stay at or below the line estimate when possible, and be more conservative
when `confidence` is `low`.

Respect placeholder size in every content decision:

- Text: do not write beyond the likely line budget for the box. If the message
  does not fit, tighten the wording or choose a layout with a larger text area.
- Images and diagrams: match the placeholder aspect ratio and expected visual
  density to the available width and height.
- Tables and charts: reduce rows, columns, labels, or series when the
  placeholder is small. Prefer a larger layout over forcing dense content into
  a small box.

Also inspect theme colors and assets if you need to match the visual identity:

```bash
pptx theme show --manifest ./corp-template --format json
pptx assets list --manifest ./corp-template --format json
```

### Step 3 — Create diagrams with excal (if needed)

When the deck needs diagrams, flowcharts, or visual explanations, create them
as Excalidraw scenes and render to PNG.

**Critical: match the placeholder aspect ratio.** Before designing a diagram,
check the target placeholder's dimensions in EMUs (from the placeholders
command). Calculate the aspect ratio and design the diagram to match.

For a picture placeholder that is 6642100 x 5514313 EMU (~1.2:1), design a
diagram roughly 540px wide x 450px tall. A mismatch causes cropping or
letterboxing.

```bash
# Create the .excalidraw file, then:
excal validate diagrams/my-diagram.excalidraw
excal render diagrams/my-diagram.excalidraw --outDir ./out/diagrams --png --scale 4 --no-background
```

Use `--no-background` for transparent backgrounds that blend with slide
backgrounds. Use `--scale 4` for crisp output — scale 2 looks blurry on
large slide placeholders because the pixel density is too low for the
physical size. Scale 4 ensures diagrams stay sharp even on high-DPI
displays and when projected.

**Match the template's visual identity.** Diagrams should feel like they belong
on the slide, not like foreign objects pasted in. Two things matter most:

1. **Use `fontFamily: 1`** (Excalidraw's hand-drawn style) for diagram text.
   This gives a clean whiteboard aesthetic that contrasts well with formal slide
   typography and looks intentional rather than mismatched.

2. **Pull colors from the template theme.** Run `pptx theme show --manifest
   ./corp-template --format json` and use the accent colors for fills and
   strokes. Common mapping:
   - Primary elements → accent1 (e.g., `#003778`)
   - Secondary elements → accent2 (e.g., `#4673C3`)
   - Tertiary/subtle → accent3 (e.g., `#87AAE1`)
   - Success/positive → `#087f5b` (green)
   - Labels/muted → `#868e96` (gray)

   Avoid arbitrary colors — diagrams that use theme colors integrate seamlessly
   with the slide's color palette.

**Keep elements away from frame edges.** Text and shapes positioned within
10px of the frame boundary may be clipped during PNG export. Use at least a
15px margin on all sides of the frame for safe rendering.

See `references/excal-diagrams.md` for the full Excalidraw scene format and
element types.

### Step 4 — Write the deck spec

Create a YAML file mapping layouts to content:

```yaml
manifest: ./corp-template
metadata:
  title: "Presentation Title"
  author: "Author Name"
slides:
  - layout: layout-id
    content:
      title: "Action title stating the takeaway"
      subtitle: "Optional context"
      content_1: |
        - Bullet point one
        - Bullet point two
      source: "Source: Data attribution"
    notes: |
      # Speaker notes

      - Open with the takeaway before reading the slide
      - Keep timing to under 90 seconds

  - layout: picture-layout-id
    content:
      title: "Slide title"
      picture:
        kind: image
        path: out/diagrams/my-diagram.png
      content_1: |
        Supporting text alongside the image
```

**Content value formats:**
- Plain string → treated as `text`
- Multi-line YAML block scalar with markdown-looking content (headings, lists,
  ordered items) → auto-detected as `markdown-text`
- `@notes.md` via `--set key=@notes.md` or `{ kind: "markdown-text", value:
  "..." }` → markdown parsed with headings, lists, inline emphasis, and light
  presentation-aware spacing
- Slide-level speaker notes → `notes: |` in the deck spec, or `pptx slide create --notes/--notes-file` for single-slide generation
- `{ kind: "image", path: "path/to/file.png" }` → image insertion
- `{ kind: "table", columns: [...], rows: [[...], ...] }` → table
- `{ kind: "chart", chart_type: "column_clustered", categories: [...], series: [{name: "...", values: [...]}] }` → chart

For markdown-heavy placeholders, prefer explicit `kind: markdown-text` when you
want unambiguous behavior. The current renderer preserves bold, italic, inline
code, bullets, nested bullets, ordered lists, and light block spacing, but it
does not attempt full document-layout fidelity.

**Section spacing in markdown content:** When a placeholder contains multiple
sections (e.g., bold heading + bullets, then another bold heading + bullets),
add a blank line between sections to create visual breathing room. Without it,
consecutive sections run together with minimal spacing.

### Step 5 — Build and validate

```bash
pptx deck build --manifest ./corp-template --spec deck.yaml --out ./out/deck.pptx --format json
pptx validate --manifest ./corp-template --deck ./out/deck.pptx --strict --format json
```

Always validate with `--strict`. Fix any issues and rebuild. If the output
file is locked (open in PowerPoint), write to a new filename.

Use `--dry-run` on build to preview without writing files.

---

## Image handling

### Image scaling — fit vs crop

Picture placeholders should already advertise `image` in
`supported_content_types`. Do not patch `manifest.yaml` unless inspection
output proves the template contract is actually wrong.

The current build behavior defaults to `image_fit: fit`, which preserves the
full image inside the placeholder. Use `image_fit: cover` when you explicitly
want crop-to-fill behavior.

```yaml
slides:
  - layout: picture-layout-id
    content:
      title: Workflow
      picture:
        kind: image
        path: out/diagrams/workflow.png
        image_fit: fit
```

---

## Slide writing principles

These apply to every deck, not just consulting-style ones.

### Action titles, not topic labels

Every slide title should state the takeaway — what the audience should
conclude — not just name the topic.

- Bad: "Market Overview"
- Good: "Nordic retail margins will remain under pressure through 2027"

### One slide, one message

If a slide has two insights, split it into two slides. The body must prove
the headline.

### Respect placeholder geometry

Never treat placeholder size as flexible. The template geometry is part of the
contract.

- If text exceeds the placeholder's likely capacity, shorten it or split it.
- If a table or chart needs more room, switch to a layout with a larger object
  placeholder.
- If a diagram becomes unreadable at the placeholder's size, simplify the
  diagram rather than shrinking text and shapes until they are illegible.

### Source attribution

Data-driven slides need source lines. Use the `source` placeholder when
available.

### Storyline coherence

A reader should be able to read only the slide titles, in order, and
understand the full argument.

For full consulting-style guidance including the Pyramid Principle, MECE
structuring, ghost decks, slide archetypes, and executive summary
construction, read `references/mckinsey-style.md`.

---

## Layout selection guide

Match content to the right layout:

| Content type | Suggested layout patterns |
|---|---|
| Opening / title (no image) | front-page-title-and-pattern layouts |
| Opening / title (with image) | front-page-title-and-picture layouts (see **Background image warning** below) |
| Agenda / TOC | agenda layouts (one item per line — see **Agenda formatting** below) |
| Section divider | breaker layouts |
| Single topic with bullets | title-and-content |
| Side-by-side comparison | two-contents |
| Topic with description header | title-description-and-content |
| Image with explanation | picture-right-text-and-box (or similar) |
| Minimal / custom | title-only or blank-with-logo |
| Closing | end-slide layouts |

When a template has numbered variants (e.g., `1-title-and-content`,
`2-title-description-and-content`), inspect the placeholders of each to
understand the differences. Numbered variants often differ in placeholder
arrangement, background color, or description fields.

### Background image warning — front-page-title-and-picture layouts

On `front-page-title-and-picture` layouts, the picture placeholder spans
the **full slide** and the title/subtitle render **on top of the image**.
This means:

- **Use abstract, low-detail images only** — blurred photos, gradients,
  subtle textures, or simple geometric shapes.
- **Never use information-dense diagrams** (with text labels, data, or
  fine details) as the background image. The title text will collide with
  diagram labels, making both unreadable.
- Reserve detailed diagrams for `picture-right-text-and-box` where the
  image sits **alongside** text, not beneath it.
- If you must use a diagram, design it as an ambient background: large
  shapes only, no text, muted/faded colors at low opacity.

### Agenda formatting

Agenda layouts expect **one item per line**, not a pipe-delimited string.
The layout may auto-number items. Do not add numbered prefixes yourself.

```yaml
# WRONG — renders as a single cramped line
content_1: "Foundations | Modern Patterns | Cloud-Native | Serverless"

# CORRECT — each item on its own line
content_1: |
  Foundations
  Modern Patterns
  Cloud-Native
  Serverless
  AI-Native
  What's Next
```

### Series 2 (white) vs Series 3 (sand) layouts

When a template offers both white-background (series 2) and sand-background
(series 3) variants of the same column layout:

| Visual intent | Use |
|---|---|
| Standard content slides | Series 2 (white background) |
| Highlighted or callout content | Series 3 (sand background) |
| Visual rhythm in long decks | Alternate between series 2 and 3 per section |

Do not mix white and sand variants within the same logical section — pick
one per section and stay consistent.

### Front-page variant differences

Front-page layouts with the same column count may differ in subtitle
placement. For example, variant 1 may place the subtitle **above** the
title while variant 2 places it **below**. Always inspect placeholders
(`top_emu` values) to understand the visual order before authoring content.

### End-slide positioning

End-slide layouts typically position the title left-of-center with the
right portion of the slide empty. Keep closing titles short (1-3 words
like "Thank you" or "Questions?") for visual balance.

---

## Quick reference — common commands

```bash
# One-time setup
pptx init <template.pptx> --out ./manifest-dir --format json
pptx doctor --manifest ./manifest-dir --format json

# Inspection (safe to parallelize)
pptx layouts list --manifest ./manifest-dir --format json
pptx placeholders list <layout-id> --manifest ./manifest-dir --format json
pptx theme show --manifest ./manifest-dir --format json
pptx assets list --manifest ./manifest-dir --format json

# Single slide (quick test)
pptx slide create --manifest ./manifest-dir --layout <id> --set title="Hello" --notes-file ./speaker-notes.md --out slide.pptx

# Full deck
pptx deck build --manifest ./manifest-dir --spec deck.yaml --out deck.pptx --format json
pptx validate --manifest ./manifest-dir --deck deck.pptx --strict --format json

# Diagrams
excal validate diagram.excalidraw
excal render diagram.excalidraw --outDir ./out --png --scale 4 --no-background

# Template versioning
pptx manifest diff ./v1-manifest ./v2-manifest --format json
```

---

## Error handling

All `pptx` commands return JSON envelopes with `ok`, `errors`, and exit codes:

| Exit code | Meaning |
|---|---|
| 0 | Success |
| 10 | Validation error (bad layout, missing placeholder, wrong content type) |
| 20 | Policy error |
| 40 | Conflict (output file exists / locked) |
| 50 | I/O error (file not found) |
| 90 | Internal error |

If output file is locked (exit code 40 or PermissionError), write to a
different filename — do not retry.

All `excal` errors also return JSON envelopes. Key codes: exit 10 for
invalid scene JSON, exit 20 for render failures, exit 50 for I/O errors.
