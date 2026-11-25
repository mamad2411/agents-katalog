---
name: slidify
description: >-
  End-to-end PowerPoint generator. Use whenever the user wants to create, edit, or export a .pptx
  (or convert to PDF), add watermarks/logos/footers, apply brand templates, build a deck from any
  content, generate charts/diagrams, fetch stock images, or add animations/transitions. Always use
  this skill rather than writing pptxgenjs/python-pptx from memory. Triggers on: 'make a
  presentation', 'create slides', 'generate pptx', 'export to pdf', 'add watermark', 'apply
  template', 'add chart', '/slidify', or any .pptx request.
domain: process
composable: true
yields_to: [craft]
---

# Slidify

You generate production-quality PowerPoint presentations using a two-layer architecture:
1. **Slide Spec (JSON)** — you write and edit this; humans can read and tweak it
2. **Code Layer (JS)** — generated from the spec; you run it

This separation makes the pipeline AI-friendly: editing means editing JSON, not wrestling with pptxgenjs internals.

---

## Core Philosophy: Images Over Text

**1 image > 2 slides of text.** Visuals are processed 60,000x faster than text. Every slide with more than 4 bullet points is a candidate for an image replacement.

Before writing any slide, ask: **"Can this be a chart, diagram, or image instead of text?"**

| If the content is... | Replace with... |
|---------------------|----------------|
| 5+ bullet points with data | Bar chart or comparison visual |
| A process with 3+ steps | Flowchart diagram |
| A timeline of events | Timeline visual |
| Statistics/numbers | Stat callout cards with big numbers |
| Before/after comparison | Side-by-side visual |
| Overlapping concepts | Venn diagram |
| Feature list | Icon grid |
| Trend over time | Line chart |
| Part-of-whole data | Pie/donut chart |
| Hero/intro slide | Searched stock image |

Use `scripts/gen_images.py` to generate charts from data. Use `scripts/fetch_images.py`
to find stock images from the web. See `references/images.md` for the full catalog.

---

## When to Use

- User asks to create, edit, or export a presentation
- User mentions slides, deck, pptx, PowerPoint, or PDF export
- User wants watermarks, logos, brand colors, or footers on slides
- User provides content (paper, report, outline) and wants it as slides
- User wants charts, diagrams, or data visualizations in slides
- User wants stock images or illustrations fetched from the web
- User says "/slidify"

---

## Workflow

### Step 1 — Resolve Template

Does the user have a template requirement (university logo, company brand, conference theme)?

**Yes** → Read `references/templates.md`, pick or create a template config in `assets/templates/`.
**No** → Use `default` template (clean white, no watermark).

Templates live as JSON in `assets/templates/`. The generator reads them at runtime.

### Step 2 — Write Slide Spec

Read `references/slide-spec.md` for the full schema.

Write `slides.json`:
```json
{
  "meta": {
    "title": "My Presentation",
    "author": "Your Name",
    "template": "default",
    "output": "output.pptx"
  },
  "slides": [
    { "type": "title", "title": "...", "subtitle": "..." },
    { "type": "content", "title": "...", "layout": "bullets", "items": ["..."], "notes": "Speaker notes here" }
  ]
}
```

The spec is the **single source of truth**. All edits go here, never in generated code.

### Step 2b — Generate Speaker Notes (MANDATORY)

**Every slide MUST have a `notes` field.** Speaker notes appear in the PPTX notes panel below each slide and are essential for presenting — they serve as the presenter's script.

When writing `slides.json`, add `"notes"` to every slide object. Generate notes automatically based on the slide content:

**What good speaker notes contain:**

| Element | Example |
|---------|---------|
| **Opening line** | "Today I'll walk you through our approach to..." |
| **Key talking points** | Expand on each bullet/visual — what to say, not just what's on screen |
| **Emphasis cues** | "Make sure to pause on this stat — it's the core finding" |
| **Transitions** | "This leads us directly into the results section..." |
| **Context for visuals** | "The chart shows a 4x improvement — let me explain why..." |
| **Q&A prep** | "If asked about limitations, mention the dataset size constraint" |

**Notes format — keep them scannable for a presenter:**

```json
{
  "type": "content",
  "title": "Key Results",
  "layout": "stats",
  "stats": [
    { "value": "4x", "label": "Token efficiency" },
    { "value": "~2x", "label": "Perplexity gain" }
  ],
  "notes": "OPEN: Let's look at the numbers that matter.\n- 4x token efficiency: this is vs Phi-4 on Hindi — the core contribution.\n- ~2x perplexity: TokenAdapt halves the gap to English-quality models.\nEMPHASIS: Pause on the 4x stat — it's the headline.\nTRANSITION: Now let me show you how we got here..."
}
```

**Slide-type-specific notes:**

| Slide Type | Notes Should Include |
|------------|---------------------|
| `title` | Welcome line, self-intro prompt, topic framing |
| `content` (bullets) | Expand each bullet into 1-2 spoken sentences |
| `content` (stats) | Explain what each number means and why it matters |
| `content` (chart) | Describe the chart trend, highlight key comparisons |
| `content` (cards) | Walk through each card with a real-world example |
| `content` (timeline) | Narrate the story arc across the timeline |
| `section` | Preview what's coming in this section |
| `image-full` | Describe what the audience should notice in the image |
| `closing` | Wrap-up statement, invite questions, share contact info |

### Step 3 — Generate PPTX

```bash
node scripts/gen_pptx.js slides.json
# → output.pptx
```

The generator reads `slides.json` + the template config and produces a `.pptx`.

### Step 3b — Generate Images (Optional but Recommended)

If the slide spec has an `"images"` block, generate charts and fetch stock images:

```bash
# Generate charts/diagrams from data
python scripts/gen_images.py images-config.json assets/generated/

# Fetch stock images from the web
python scripts/fetch_images.py fetch-config.json assets/fetched/
```

Then reference the generated images in the slide spec:

```json
{
  "type": "content",
  "title": "Results",
  "layout": "image-right",
  "image": { "path": "assets/generated/perf_chart.png" },
  "notes": "The chart shows our 4x improvement..."
}
```

**When to generate images:**

| Slide Content | Generate | Type |
|--------------|----------|------|
| Data comparisons | Yes | `bar` or `grouped_bar` |
| Statistics | Yes | `stat_callout` |
| Process/workflow | Yes | `flowchart` |
| Timeline | Yes | `timeline` |
| Trends | Yes | `line` |
| Hero/intro | Fetch | Stock image via `fetch_images.py` |

See `references/images.md` for all chart types and options.

### Step 3c — Add Animations (Optional)

If the user wants animations or transitions, add an `"animations"` block to `slides.json`
(see `references/slide-spec.md` for full schema). Then post-process:

```bash
node scripts/add_animations.js output.pptx animations.json output-animated.pptx
```

See `references/animations.md` for the full effect catalog.

### Step 4 — Export (Optional)

```bash
bash scripts/export.sh output.pptx pdf    # → PDF
bash scripts/export.sh output.pptx all    # → PDF + PPT + images
```

### Step 5 — QA

```bash
# Text content check
python scripts/extract_text.py output.pptx

# Visual check — convert to images
bash scripts/export.sh output.pptx images
```

Fix issues in `slides.json` → re-run generator → re-check. Never edit generated code directly.

---

## Slide Types Quick Reference

| Type | Use For | Key Fields |
|------|---------|------------|
| `title` | Opening slide | `title`, `subtitle`, `presenter`, `affiliation`, `date` |
| `content` | General slides | `title`, `layout`, `items`/`stats`/`cards`/`steps`/`chart` |
| `section` | Section dividers | `title`, `subtitle` |
| `image-full` | Full-bleed image | `path`, `caption` |
| `closing` | Final slide | `title`, `contact`, `links` |

Content layouts: `bullets`, `two-column`, `image-right`, `image-left`, `cards`, `stats`, `timeline`, `chart`, `blank`

---

## Critical Rules

| Rule | Why |
|------|-----|
| No `#` in hex colors | `"FF0000"` not `"#FF0000"` — corrupts the file |
| No unicode bullets | Use `bullet: true`, never the `•` character |
| No 8-char hex opacity | Use `opacity: 0.15` field, never `"00000020"` |
| No reused option objects | Use factory `() => ({...})` for shadows/styles |
| No placeholder text in output | Grep for "TODO", "lorem", "XXX" before shipping |
| Watermark on EVERY slide | Template applier loops all slides, not just first |
| Edit spec only | Never modify generated `.js` — edit `slides.json` and regenerate |
| Speaker notes on EVERY slide | Every slide object must have a `notes` field — presenter's script |

---

## Editing an Existing Deck

1. Edit `slides.json` — change content, reorder, add/remove slides
2. Change template? Update `meta.template` → all slides update automatically
3. Re-run generator — full regeneration from spec (idempotent)

---

## File Map

| Need | Read |
|------|------|
| Slide spec format | `references/slide-spec.md` |
| Template system | `references/templates.md` |
| pptxgenjs API cheatsheet | `references/pptxgenjs-cheatsheet.md` |
| Images & charts | `references/images.md` |
| Animations & transitions | `references/animations.md` |
| Export options | `references/export.md` |
| Ready-made templates | `assets/templates/*.json` |

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: [craft]
```

Slidify owns **process** — the workflow for generating PowerPoint presentations from structured specs. It controls the slide spec format, generation pipeline, and export steps.

### When Slidify Leads

- Any request to create, edit, or export a `.pptx` file
- Any request involving slide decks, presentations, or PowerPoint
- Template creation or modification for presentations

### When Slidify Defers

| Other Skill's Domain | What Slidify Does |
|---------------------|-------------------|
| **Craft** (e.g. painter) | Slidify handles structure and content. Visual design decisions (color palettes, layout aesthetics, typography choices) defer to craft skills. |
| **Content** (e.g. researcher, documenter) | Slidify handles slide structure. The actual content substance comes from content skills. |
| **Voice** (e.g. blogger) | Slidify handles slide layout. Tone and wording of slide text defers to voice skills. |

### Conflict Signal

> `⚠️ Process conflict: visual design request overlaps with craft domain. Slidify handles slide structure; craft skill handles aesthetic decisions. Which approach?`
