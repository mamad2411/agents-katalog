---
name: pptx-deck-creation
description: "Create editable, production-ready PPTX decks with narrative planning, explicit layout specs, asset guidance, and quality checks."
---

# PPTX Deck Creation

## Overview

Create an editable PowerPoint deck from a clear narrative, source evidence, and
explicit layout decisions. Keep the deck specification and its native
PowerPoint objects as the source of truth. Images may support a slide, but they
must not replace editable titles, labels, data, tables, or diagrams.

This skill embeds the design-profile catalog, reference-deck analysis guidance,
visual-asset decisions, OOXML safety rules, and final quality checks below. It
does not ship a general-purpose renderer or bundled runtime scripts.

## Scope Boundary

Use this skill as the primary workflow for creating a new, editable PPTX deck.
It owns the path from a deck brief through narrative planning, a
coordinate-explicit specification, task-specific PPTX generation, and final
quality assurance. Do not redirect a net-new deck to another skill merely
because the requested deliverable is a `.pptx` file.

Use `@pptx-official` when work starts with an existing PPTX and requires
package-level operations: raw OOXML editing, template duplication and text
replacement, speaker notes, comments, animations, or other structural changes
to that file. It may support a build when those operations are necessary, but
it is not the default workflow for a net-new deck authored here.

## When to Use This Skill

* Use when a user asks to create a new editable PowerPoint or PPTX deck
* Use as the default workflow when a new deck needs to be delivered as a `.pptx` file
* Use when a deck needs a narrative framework, a design direction, and final coordinates
* Use when analyzing a reference PPTX without copying its binary content
* Use when reviewing a generated PPTX for layout, package, or accessibility defects

## How It Works

### Step 1: Understand the requested deck

Collect the audience, decision or purpose, language, slide count, source
material, brand requirements, and delivery format. Ask the user to select a
narrative framework if they have not already done so. Do not select one on the
user's behalf.

Use one of these framework spines, or a user-defined alternative:

| Framework | Use case |
|---|---|
| `mckinsey` | Executive proposals and strategic recommendations |
| `scqa` | Situation, complication, question, answer narratives |
| `pyramid` | Main answer followed by supporting arguments |
| `mece` | Issue decomposition and workstream synthesis |
| `action-title` | Executive communications with conclusion-led titles |
| `assertion-evidence` | Technical or research presentations |
| `exec-summary-first` | Board and leadership briefings |
| `custom` | User-defined structure or organization playbook |

Record the resolved framework, its source, title rules, slide sequence, and
any approved assumptions in the deck summary.

### Step 2: Establish source and design context

Give each factual source a stable ID. Record a source reference for every
metric, chart value, quotation, and factual claim that appears in the deck.
Summarize source material into one message per slide rather than pasting long
documents into the specification.

For a reference presentation, inspect it read-only. Extract palette, font,
slide-size, template, layout-flow, and topic-sequence signals. Re-author target
slides with their own explicit coordinates. Do not copy, mutate, or use the
source PPTX as a template for generated content.

Select a documented design profile from the embedded Design Profile Catalog.
Use the user's named profile first. Use a reference deck when one is available.
Otherwise, use Fluent UI Design Token Guidance by default, use Primer
Primitives for GitHub-focused technical decks, and use a broader style catalog
only when the user requests multiple visual directions. Record the selected
profile, source URL, license, palette, typography, spacing, and signature
visual treatment in `summary.design_context`.

### Step 3: Plan the story and visual structure

Create one defensible message per slide. Use conclusion-led slide titles when
the selected framework calls for them. Keep the storyline mutually exclusive
and collectively exhaustive where appropriate. Include concrete numbers, dates,
owners, and sources only when supported by the evidence.

Every normal content slide needs a visible, style-derived structure such as an
accent band, card shell, divider, grid, diagram primitive, or image treatment.
Avoid plain title-and-bullets slides, default theme colors, and Calibri-only
output unless the user explicitly requests that treatment.

### Step 4: Author a coordinate-explicit specification

Create a JSON object with `summary` and `slides`. Every generated slide needs
an `id`, `title`, and complete `layout_tree`. Use final inch-based bounding
boxes, z-order, colors, font sizes, and grouping. Do not rely on a renderer to
make layout decisions.

Include this production metadata before building:

```json
{
  "summary": {
    "layout_policy": {
      "safe_margin": 0.5,
      "content_bottom": 6.7,
      "footer_top": 6.85,
      "minimum_gap": 0.12
    },
    "accessibility": {
      "language": "en-US",
      "presentation_title": "Deck title"
    }
  }
}
```

Keep content inside the safe margin and above the footer rail. Use native
`text`, `shape`, `line`, `table`, and `image` objects. Add alt text to
meaningful images and a reading order for each production slide. Use images as
supporting visuals only; recreate essential labels, legend entries, process
steps, and data values as editable objects.

Use the following object constraints:

* Keep content text at 9 pt or larger; prefer 10 to 12 pt for body copy
* Keep every child object inside its parent group bounding box
* Keep table column widths equal to the table width and split dense tables across slides
* Keep normal content objects within slide bounds; only decorative full-bleed elements may cross an edge
* Keep images behind overlapping text and preserve their aspect ratio
* Store `source_ref` with source ID, locator, claim type, and verification status for sourced claims

### Step 5: Create the PPTX deck when requested

Own net-new PPTX creation in this workflow. When a PPTX file is required,
create a small task-specific builder with the user's approved environment. Start
slides from a blank layout and create native objects from the final bounding
boxes. Enable word wrap, disable automatic text resizing, set text insets and
alignment explicitly, and reject zero or negative bounding boxes for non-line
objects before building. Validate lines by requiring two distinct endpoints;
horizontal and vertical lines may have a zero-height or zero-width bounding
box.

Save the authored specification, PPTX, build manifest, audit records, and
source manifest together. Do not add a large shared renderer or copy source
presentation content. Use `@pptx-official` only when the requested result also
requires an existing-file or OOXML workflow.

### Step 6: Validate and repair

Apply the embedded Manual Audit Checklist before and after building. Check
collisions, text capacity, font sizes, safe margins, group containment, table
fit, object bounds, design context, and native editability. Reopen the PPTX to
verify slide count, package structure, hidden slides, actual geometry,
language, image alt text, reading order, and table headers.

Inspect rendered previews when a compatible renderer is available. Check
clipping, font fallback, contrast, image crops, and visual hierarchy. Repair
the specification or the task-specific builder, rebuild, and repeat the audit
until all deterministic failures are resolved. Report any remaining exception
with the slide ID, object ID, reason, owner, and review date.

## Reference-Deck Analysis

The skill provides a read-only analysis contract, not packaged code. For a
specific task, use `python-pptx` and the Office Open XML package to inspect a
presentation. Use OOXML package inspection when `python-pptx` cannot expose
theme, master, layout, relationship, notes, comments, animation, media, or
non-modeled formatting evidence. Resolve the package relationship graph;
never infer slide order from filenames or copy source package parts. Produce
only the context needed for the task:

* Compact prompt context with slide count, styles, brands, template, and layout
* Full extraction with `layout_tree`, summary metrics, and render-aware elements
* Folder-level diagnostics with one result per deck and a manifest
* Style-master analysis with colors, fonts, layout usage, and flow patterns

Use the embedded Reference-Deck Analysis Recipes and Patterns as static
implementation guidance. Use the embedded OOXML Parsing Reference for the
package-part map, relationship resolution, namespaces, and secure parsing
requirements. Keep all extraction read-only.

## Visual Assets

Use the embedded Visual Asset Guidelines when an icon, image, SVG, or
user-managed infographic is needed. Confirm image licensing before placing it.
Record asset provenance, local path, and alt text. Never ask users to provide
secrets in chat, and never use a placeholder when acquisition fails.

When a provider, output path, or other required setting is missing, ask for the
non-secret information before generating an infographic. If no configured
provider is available, omit the asset and continue with editable native slide
objects.

Before any external generation call, disclose the provider and model, what
prompt or source material will leave the machine, the likely cost, and the
output path. Obtain explicit confirmation unless the user already authorized
that exact operation. Never overwrite an existing output or manifest without
separate explicit confirmation.

## Examples

### Example 1: Executive recommendation deck

A user asks for a 10-slide leadership deck based on a project brief. Confirm
the audience, choose `exec-summary-first`, summarize the brief into one claim
per slide, and create coordinate-explicit content cards with a documented
Fluent UI design context. Add source references for each brief-derived metric,
then build and audit the requested PPTX.

### Example 2: Reference-deck-informed proposal

A user supplies a prior PPTX and asks for a new proposal in a similar visual
language. Extract only the existing deck's palette, typography, layout rhythm,
and template usage. Use those signals to design a new outline and native layout
tree. Do not duplicate slides, copy the deck's binary parts, or present the
reference deck as the new deliverable.

## Best Practices

* Keep the business framework and source lineage visible in the deck summary
* Make each slide title convey the slide's conclusion or narrative role
* Use source evidence for charts and dashboard-like exhibits
* Build meaningful content from native editable PowerPoint objects
* Add a deliberate visual structure to every normal content slide
* Rebuild and inspect previews after repairing layout or text issues

## Limitations

* This skill does not replace a user-provided brand guide, legal asset review, or expert accessibility review
* It does not include a general renderer, a bundled extraction module, or credentials for external providers
* It does not own raw OOXML editing, template duplication, or other mutations of an existing PPTX package
* Stop and ask for clarification when the audience, source evidence, brand requirements, or required output path is missing

## Security and Safety Notes

* Keep reference-deck analysis read-only and never overwrite the source deck
* Request confirmation before any task-specific build or repair overwrites an existing output file
* Use user-managed providers only and keep credentials outside chat and skill content
* Omit unlicensed or license-ambiguous visual assets instead of substituting placeholders

## Common Pitfalls

### Problem: A slide has more copy than its bounding box can hold

Shorten the copy, enlarge the bounding box, or split the content across slides.
Do not solve the issue by reducing meaningful content below 9 pt.

### Problem: The deck resembles an unstyled default PowerPoint file

Select and record a design profile, then add explicit background, typography,
accent, card, divider, or grid primitives to the layout tree.

### Problem: A reference deck is used as a source file for the output

Treat the reference deck as read-only context. Re-author the target deck with
its own slide specification and native editable content.

## Related Skills

* `@pptx-official` - Use for existing PPTX, OOXML, and template-mutation workflows, not default net-new deck creation
* `@python-pptx-generator` - Use for focused Python PPTX generation patterns

## Embedded Reference Guide

This guide contains the essential material formerly kept in `references/`, so
this file is self-contained for upload. It is instructional material only: do
not treat the examples as a packaged module, ship them as scripts, or copy a
reference presentation's package content into a new deck.

### Design Profile Catalog

Select and lock one profile before authoring the layout tree. Record its ID,
source URL, license, palette, typography, spacing, and signature treatment in
`summary.design_context`. Convert every selected signal to explicit native
PowerPoint primitives; never use scraped images, screenshots, or logos as a
substitute for a design system.

| Profile ID | Design context | Use when | Key rule |
|---|---|---|---|
| `fluent-ui-design-tokens` | [Fluent UI Design Token Guidance](https://github.com/microsoft/fluentui/blob/master/docs/architecture/design-tokens.md), MIT, Microsoft | Microsoft, M365, Teams, Power Platform, or enterprise decks; the default | Use token roles for color, spacing, radius, font, line height, stroke, shadow, duration, and easing rather than arbitrary values. Available themes include `webLightTheme`, `webDarkTheme`, `teamsLightTheme`, `teamsDarkTheme`, and `teamsHighContrastTheme`. |
| `getdesign-md-design-systems` | [getdesign.md](https://getdesign.md/), independent VoltAgent analyses; license varies by entry | The user explicitly asks to echo a real product or brand's public aesthetic | This is inspiration only, not an official or affiliated brand resource. Extract observable colors, type scale, components, foundations, and motifs; do not redistribute proprietary assets. |
| `corazzon-pptx-design-styles` | [corazzon/pptx-design-styles](https://github.com/corazzon/pptx-design-styles), MIT, TodayCode/contributors | Several visual directions or a pre-defined modern style are needed | Choose one style and lock its palette, fonts, layout rules, signature elements, and avoid list. Never accidentally combine style families. |
| `primer-primitives` | [Primer Primitives](https://github.com/primer/primitives), MIT, GitHub | GitHub-style developer-product, engineering, and token-driven UI decks | Use Primer's color, spacing (`xxs`–`xl`), typography, motion, and z-index roles. Typical colors include `#ffffff`, `#1f2328`, `#F6F8FA`, `#0969da`, `#1a7f37`, and `#cf222e`. |

The corazzon catalog includes Glassmorphism, Neo-Brutalism, Bento Grid, Dark
Academia, Gradient Mesh, Claymorphism, Swiss International, Aurora Neon Glow,
Retro Y2K, Nordic Minimalism, Typographic Bold, Duotone Color Split,
Monochrome Minimal, Cyberpunk Outline, Editorial Magazine, Pastel Soft UI,
Dark Neon Miami, Hand-crafted Organic, Isometric 3D Flat, Vaporwave, Art Deco
Luxe, Brutalist Newspaper, Stained Glass Mosaic, Liquid Blob Morphing,
Memphis Pop Pattern, Dark Forest Nature, Architectural Blueprint, Maximalist
Collage, SciFi Holographic Data, and Risograph Print. Its families are
modern-ui, editorial, retro, technical, luxury, organic, and experimental.

For `getdesign-md-design-systems`, resolve a brand's slug at
`https://getdesign.md/design-md`, then fetch
`https://getdesign.md/{slug}/design-md`. A slug can include a TLD, for example
`linear.app`. Map colors to a deck palette (`Primary`/`Accent` for emphasis,
`Ink`/`Muted` for text, `Canvas`/`Canvas Alt` for backgrounds, and `Hairline`
for rules); map display/body scales to title/body roles; and map its 8px-style
spacing, radius, elevation, component, and signature rules to layout-tree
objects. Record the entry URL and the independent-analysis disclaimer. If it
cannot be fetched or has no matching slug, use a bundled profile and record
the fallback.

### Manual Audit Checklist

Audit the spec before building and reopen the PPTX for the post-build checks.
All 15 checks pass before delivery, unless every exception records a slide ID,
object ID, reason, owner, and review date. Repair the spec, rebuild, and
re-audit for every failure.

| # | Check | Pass condition and repair direction |
|---:|---|---|
| 1 | Content collisions | No two `classification: "content"` bboxes overlap. They overlap when `A.x < B.x + B.w AND B.x < A.x + A.w` and `A.y < B.y + B.h AND B.y < A.y + A.h`; move, resize, reduce density, or split the slide. |
| 2 | Text overflow | Estimate Latin characters per line as `(w × 72) / (font_size × 0.5)` and lines as `(h × 72) / (font_size × 1.2)`. Halve characters per line for CJK/full-width content and remove about 0.1 in from each side for text on a card. Treat this as a preview-confirmed warning; shorten, enlarge, or split content rather than shrinking it. |
| 3 | Font minimum | Every content object is at least 9 pt. Increase type and split material if needed. |
| 4 | Design context | `summary.design_context` contains `profile_id`, source URL, and license. Do not deliver default-theme, Calibri-only, all-white, title-and-bullets output. |
| 5 | Per-slide visual design | Each non-header, visible content slide has a style-derived accent, card, grid, rule, motif, image treatment, or background pattern. |
| 6 | Narrative and count | The count is within ±2 of the requested count; sequence follows the selected framework. For action-title frameworks, a title-only “ghost deck” tells the story. |
| 7 | Hidden slides | Hidden slides are last unless specified otherwise, and the saved PPTX has `p:sldId show="0"` at the intended presentation entries. |
| 8 | Asset layering | Images/SVGs sit below overlapping text, keep their aspect ratio, and never carry all meaningful labels, metrics, data, or process steps. Put captions beside, not over, images. |
| 9 | Bounds and safe margins | Every content object is within the slide and the default 0.5 in safe edge; only full-bleed `layout_design` objects may cross an edge. |
| 10 | Containment | Child objects/groups fit their parent bbox; text on a shape fits its inset inner area. Resize or split overflowing content. |
| 11 | Table fit | Columns sum to the table width; wrapped cell text fits row heights; target about 8–10 body rows at 10–11 pt. Rebalance, raise rows, or split and repeat the header. |
| 12 | Native editability | Titles, labels, metrics, tables, charts, and process steps are native editable objects. A raster/SVG may only support the message. |
| 13 | Post-build artifact | Reopen the file to check actual geometry, safe margin/footer rail, hidden state, document language, unique accessible titles, image alt text, reading order, table headers, and rendered clipping, font fallback, contrast, crop, and hierarchy. Record renderer and results. |
| 14 | Metadata and lineage | `summary.layout_policy` identifies safe margin, `content_bottom`, `footer_top`, and minimum gap; content remains above the footer. `summary.accessibility` names language and presentation title. Every sourced claim has a `source_ref` with ID, locator, claim type, and verification status found in the source manifest. The build manifest records builder, input spec, output, slide count, time, and warnings. |
| 15 | Positive geometry | Each non-line object has positive width and height. A line has distinct endpoints (`x1 != x2` or `y1 != y2`); horizontal/vertical lines may have a zero bbox dimension. Correct invalid geometry before rebuilding. |

### OOXML Parsing and Read-Only Reference Analysis

A `.pptx` is an Open Packaging Conventions ZIP archive. Treat any source deck
as untrusted and read-only: reject path traversal, symlinks, oversized ZIP
members, and archive bombs; use a secure XML parser with DTDs, external entity
expansion, and network access disabled; preserve `xml:space="preserve"`; and
never overwrite the source or blindly copy its XML, media, fonts, images, or
embeddings.

| Analysis need | Package evidence |
|---|---|
| Presentation order | `ppt/presentation.xml` and `ppt/_rels/presentation.xml.rels` |
| Slide shapes/text | Slide parts resolved from presentation relationships, often `ppt/slides/slideN.xml` |
| Layout, notes, images, charts | The owning slide's relationship part, often `ppt/slides/_rels/slideN.xml.rels` |
| Template geometry | `ppt/slideLayouts/` and `ppt/slideMasters/` |
| Colors and fonts | Theme parts resolved from presentation/master relationships, often `ppt/theme/` |
| Notes/comments | `ppt/notesSlides/` and `ppt/comments/` |
| Media/embeddings | `ppt/media/` and `ppt/embeddings/` |

Start at `ppt/presentation.xml`, resolve its slide-ID list through the
presentation relationship part, then resolve each further target relative to
the owning source part—not by hard-coded filenames and not relative to the
`.rels` file. Retain each relationship ID, type, resolved target, missing
target, unreadable XML error, and raw-element ordering as render evidence.
Use PresentationML namespace
`http://schemas.openxmlformats.org/presentationml/2006/main`, DrawingML
`http://schemas.openxmlformats.org/drawingml/2006/main`, Office relationships
`http://schemas.openxmlformats.org/officeDocument/2006/relationships`, and
package relationships
`http://schemas.openxmlformats.org/package/2006/relationships`.

For an extraction, retain slide number, resolved target, concatenated text,
shape counts, notes, relationship types, and OOXML-only markers such as
animations, comments, transitions, unsupported shapes, and non-modeled
formatting. Retain theme colors and fonts as scheme/system tokens whenever an
RGB value cannot be reliably resolved. Record the input path, inspected parts,
relationship failures, and unreadable XML in an analysis manifest.

#### Analysis Contracts

Implement these contracts on demand with task-local `python-pptx`, `zipfile`,
and secure XML parsing. Do not create a reusable extraction module under this
skill.

1. **Prompt context:** return `slide_count`, `slide_size`, `styles`, `brands`,
   `template`, `layout`, and per-slide title/text snippets with shape counts.
2. **Full extraction:** return complexity `summary`,
   `slides[*].layout_tree` (groups and objects), `ooxml_elements`, resolved
   relationships, OOXML-only markers, and parsing exceptions. A root group
   covers the full slide; recurse nested groups; classify leaves as `text`,
   `table`, `image`, `chart`, `connector`, or `shape` and capture `content`
   plus `style`.
3. **Folder batch:** write one `.pptx-spec.json` per deck and a
   `manifest.json` for the outputs.
4. **Style master:** return palette/accent frequency, font and size
   distribution, master/layout usage, and region/flow patterns.
5. **Reference template catalog:** list source slides by **zero-based** index
   with `layout_role`, visual description, usable regions, placeholder roles,
   visual structures, and content-fit constraints. Use it only to select
   inspiration; re-author every target slide independently.

For a style master, read slide size, extract theme tokens from
`ppt/theme/theme1.xml`, recurse all slide/group shapes, and rank counters with
`most_common`. Normalize colors to `#RRGGBB` or `theme:<token>`; treat colors
with channel spread $\leq 18$ as neutrals so accents rank higher. Bucket bbox
centers into top/middle/bottom × left/center/right and infer row, column, or
grid flow from their spread. Convert EMUs to inches with $\text{EMU}/914400$.
Use guarded attribute access for optional fill, line, color, image, table, and
chart properties because `python-pptx` can raise for valid real-world decks.

For each leaf object, preserve rich text runs (font size, bold, italic, color,
hyperlink, alignment, and level); table rows/columns, dimensions, banding, and
merged-cell spans; image alt text, crop, and a saved local path or base64
blob; chart type/title/categories/series; and connector endpoints, flips, and
arrow heads/tails. Resolve embedded image relationship attributes ending in
`}embed`; count `ppt/media/` and `ppt/embeddings/`; resolve notes-slide
relationships and join `<a:t>` nodes for speaker notes. Flag a missing image
blob rather than inventing one.

### Visual Asset Guidance

Use a placed asset only with a local path, `content.alt`, bbox, z-index,
classification, and provenance (`source`, `license`, `provider`, `model`).
Never hotlink remote files into a deck. Never request secrets in chat or a
dialog; use a preconfigured environment, `.env`, or `az login`. On failure,
write a failure manifest and omit the asset—do not substitute a placeholder.

- **Icons:** The public Iconify search endpoint is
  `https://api.iconify.design/search?query=<q>&limit=<n>` and its SVG endpoint
  is `https://api.iconify.design/<prefix>/<name>.svg?color=%23<hex>`. Use
  simple, single-color icons matching the accent, verify each icon-set license,
  save the SVG locally, and use it only as a cue.
- **Web images:** Prefer an available web/image-search capability. When a
  direct image URL is approved, download it to a local assets folder, record
  its source and license, and reference that path. Confirm rights before use.
- **Vectors:** Use true clean SVGs only. Do not wrap or trace a raster simply
  to call it editable. Recreate essential visual text/data with native
  PowerPoint objects and keep non-compliant art only as support or hidden
  reference.
- **Generated infographics:** Use only a user-managed OpenAI or Azure OpenAI
  provider. Before any billable or third-party request, disclose provider and
  model, all user/source material leaving the machine, likely cost, and output
  path; obtain explicit confirmation for that exact call. Separately confirm
  overwriting any existing image or manifest. Save a manifest with provider,
  model/deployment, output path, status, and any error. Generated art supports
  the message only; its labels, metrics, and steps must be recreated natively.
- **NotebookLM bridge:** NotebookLM has no public generation API. If the user
  configured a NotebookLM/MCP bridge, call it with `source_refs` and a prompt,
  save its result locally, and apply the same confirmation, overwrite,
  provenance, and failure-manifest rules. Otherwise, use an approved managed
  infographic provider or omit the asset.

#### Illustrative Read-Only Analysis Patterns

Use these snippets only in task-local code. They are short patterns, not a
library to package or import from the skill.

```python
from collections import Counter

EMU_PER_INCH = 914400
DRAWING_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

def _inches(value: int) -> float:
  return round(int(value or 0) / EMU_PER_INCH, 4)

def _iter_shapes(shapes):
  for shape in shapes:
    yield shape
    if hasattr(shape, "shapes"):
      yield from _iter_shapes(shape.shapes)

def analyze(presentation) -> dict:
  colors: Counter[str] = Counter()
  fonts: Counter[str] = Counter()
  for slide in presentation.slides:
    for shape in _iter_shapes(slide.shapes):
      colors.update(_shape_colors(shape).values())
      fonts.update(_text_styles(shape)["fonts"])
  return {
    "colors": [{"value": value, "count": count}
           for value, count in colors.most_common(10)],
    "fonts": [{"value": value, "count": count}
          for value, count in fonts.most_common(10)],
  }
```

```python
def _bbox(shape) -> dict:
  return {
    "x": _inches(getattr(shape, "left", 0)),
    "y": _inches(getattr(shape, "top", 0)),
    "width": _inches(getattr(shape, "width", 0)),
    "height": _inches(getattr(shape, "height", 0)),
  }

def _kind(shape, shape_type: str) -> str:
  if getattr(shape, "has_table", False):
    return "table"
  if getattr(shape, "has_chart", False):
    return "chart"
  if "picture" in shape_type or getattr(shape, "image", None):
    return "image"
  if getattr(shape, "has_text_frame", False) and shape.text.strip():
    return "text"
  return "shape"

def _safe_attr(value, name):
  if value is None:
    return None
  try:
    return getattr(value, name)
  except (AttributeError, TypeError, ValueError):
    return None
```

#### Illustrative Asset-Acquisition Patterns

Use these snippets in a temporary task-local file or terminal context only.
They save usable source assets locally but do not replace the provenance,
licensing, confirmation, overwrite, or failure-manifest requirements above.

```python
import json
import urllib.parse
import urllib.request
from pathlib import Path

def icon_search(query, limit=8, prefix=None, color=None, out_dir="assets/icons"):
  url = "https://api.iconify.design/search?query=" + urllib.parse.quote(query)
  url += f"&limit={limit}"
  if prefix:
    url += f"&prefix={urllib.parse.quote(prefix)}"
  data = json.load(urllib.request.urlopen(url, timeout=15))
  Path(out_dir).mkdir(parents=True, exist_ok=True)
  results = []
  for icon_id in data.get("icons", []):
    icon_prefix, name = icon_id.split(":", 1)
    svg_url = f"https://api.iconify.design/{icon_prefix}/{name}.svg"
    if color:
      svg_url += f"?color=%23{color}"
    svg_path = Path(out_dir) / f"{icon_prefix}_{name}.svg"
    svg_path.write_bytes(urllib.request.urlopen(svg_url, timeout=15).read())
    results.append({"id": icon_id, "svg_path": str(svg_path),
            "license": "per-set (see iconify.design)"})
  return {"query": query, "results": results}

def download_image(url, out_path="assets/images/img1.jpg"):
  output = Path(out_path)
  output.parent.mkdir(parents=True, exist_ok=True)
  request = urllib.request.Request(url, headers={"User-Agent": "pptx-builder/1.0"})
  output.write_bytes(urllib.request.urlopen(request, timeout=20).read())
  return {"url": url, "local_path": str(output)}
```

```python
import base64
import json
import os
from pathlib import Path
from openai import OpenAI, AzureOpenAI  # supplied by the user's environment

def text_to_infographic(prompt, output_path, provider="openai",
            model_or_deployment="gpt-image-1", size="1024x1024",
            confirmed=False, allow_overwrite=False):
  output = Path(output_path)
  manifest_path = output.with_suffix(".manifest.json")
  existing = [path for path in (output, manifest_path) if path.exists()]
  if existing and not allow_overwrite:
    raise FileExistsError(f"Refusing to overwrite existing paths: {existing}")
  manifest_path.parent.mkdir(parents=True, exist_ok=True)
  manifest = {"provider": provider, "model_or_deployment": model_or_deployment,
        "output_path": output_path}
  if not confirmed:
    manifest.update(status="cancelled", error="External generation was not confirmed")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
  try:
    if provider == "azure-openai":
      client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
      )
    else:
      client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.images.generate(model=model_or_deployment, prompt=prompt, size=size)
    output.write_bytes(base64.b64decode(result.data[0].b64_json))
    manifest["status"] = "ok"
  except Exception as exc:
    manifest.update(status="error", error=str(exc))
  manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
  return manifest
```

Collect a missing provider, prompt, model/deployment, size, or output path as
non-secret input. Set `confirmed=True` only after the exact external request is
authorized, and set `allow_overwrite=True` only after separate approval to
replace every existing output or manifest path.
