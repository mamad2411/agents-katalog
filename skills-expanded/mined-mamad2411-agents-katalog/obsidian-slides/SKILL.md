---
name: obsidian-slides
description: Convert markdown slide drafts to polished Obsidian Slides Extended presentations with Databricks branding. Use when user asks to create slides, improve slides, or convert a draft to reveal.js format. Triggers on "obsidian slides", "slides extended", "reveal.js slides", "presentation from markdown".
---

# Obsidian Slides Extended — Databricks Theme

Convert any plain markdown slide draft into a visually polished reveal.js presentation using the Obsidian Slides Extended plugin with Databricks corporate branding.

## Prerequisites

- [Obsidian](https://obsidian.md) installed
- [Slides Extended](https://github.com/ebullient/obsidian-slides-extended) community plugin enabled
- Font Awesome icon support (bundled with Slides Extended)

## Workflow

### Step 1 — Read Input

Read the input file the user specifies. Look for `---` separators that delimit slides.

### Step 2 — Analyze Slide Structure

For each slide delimited by `---`, classify its type:

| Type | Signals |
|------|---------|
| **title-slide** | First slide, contains project name, subtitle, author |
| **section-divider** | Short heading + optional subtitle, introduces a new section |
| **bullet-content** | Heading + bullet list |
| **card-grid** | Multiple items that benefit from card layout (features, pain points, options) |
| **split-layout** | Two distinct content areas (e.g., left description + right screenshot) |
| **table-slide** | Contains a markdown table |
| **mermaid-diagram** | Contains a ```mermaid code block |
| **callout-quote** | Contains a blockquote or emphasized single statement |
| **checklist** | Contains checkboxes or status items |
| **timeline** | Sequential steps or phases (e.g., "Phase 1 → Phase 2 → ...") |

### Step 3 — Apply Transformations

For each slide, apply the appropriate layout pattern from `resources/slide-patterns.md`.

**Frontmatter** — Add at the top of the output file:
```yaml
---
theme: white
transition: fade
transitionSpeed: fast
width: 1280
height: 720
margin: 0.04
center: false
controls: true
progress: true
slideNumber: true
css:
  - slides-css/databricks.css
---
```

**Per-slide transformations:**

1. **Background** — Add `<!-- slide bg="#1B3139" -->` for dark slides (title, section dividers, callouts) or `<!-- slide bg="#F5F3F0" class="db-light" -->` for content slides.

2. **Layout** — Convert bullet lists to `<split>` or `<grid>` card layouts where there are 2-4 parallel items. Use `<split even gap="2">` for two-column layouts and `<split wrap="N" gap="1">` for N-card grids.

3. **Cards** — Wrap feature groups, pain points, and options in `<div class="db-card">` blocks with appropriate icons.

4. **Icons** — Add Font Awesome icons using `:fas_icon_name:` syntax where appropriate (features, categories, steps).

5. **Fragments** — Add `class="fragment"` on card-heavy slides to reveal items sequentially.

6. **Tables** — Wrap tables in `<div class="db-table">` and replace status text with styled tags:
   - Ready → `<span class="db-tag-ready">Ready</span>`
   - Working → `<span class="db-tag-working">Working</span>`
   - Planned → `<span class="db-tag-planned">Planned</span>`
   - — → `<span class="db-tag-none">—</span>`

7. **Mermaid** — Keep mermaid code blocks as-is (the plugin renders them natively). Use `flowchart` syntax (not `sequenceDiagram`) to avoid syntax-highlighting interference.

8. **Callouts** — Use `<div class="db-callout">` for large centered quotes on dark backgrounds.

9. **Images in split layouts** — When placing images in a `<split>` column:
   - **Single image**: max-height 400px (`<!-- element style="max-height:400px" -->`)
   - **Two stacked images**: max-height **220px each** so combined height fits within the 720px slide height
   - **Never exceed 240px per image** when stacking multiple images in one column
   - The CSS enforces `max-height:240px` on `.reveal split img` as a safety net
   - Always add `<!-- element style="max-height:Npx" -->` to every image in a split layout

### Step 4 — Ensure CSS Exists

Check for a `slides-css/databricks.css` file relative to the output path. If it doesn't exist, create it using the full CSS from `resources/databricks.css`.

### Step 5 — Write Output

Write the output to the user-specified path, or to `{input_stem}_slides.md` if no path given.

### Step 6 — Report

Tell the user:
- Total slide count
- Layout types used (list which patterns were applied)
- How to preview: Open in Obsidian → Command Palette → "Slides Extended: Show Slide Preview"

## Design Principles

- **Dark/light alternation**: Section dividers and titles use dark bg (`#1B3139`), content slides use light bg (`#F5F3F0`)
- **Cards over bullets**: When 2-4 items exist at the same level, prefer card grid over plain bullets
- **Progressive reveal**: Use fragments on slides with multiple cards or steps
- **Minimal text**: Keep bullet points short; move detail to speaker notes if needed
- **Consistent spacing**: Use `<grid>` for all multi-element layouts, keep padding consistent
- **Image overflow prevention**: Slide height is 720px. When stacking images, total height must stay under ~500px (accounting for margins, headings). Use max-height 220px per image when stacking two. The CSS provides `@media print` overflow protection but inline heights are the primary safeguard.

## CSS Specificity Notes

These are hard-won lessons from production use:

- `.has-dark-background` must override ALL text elements (p, li, strong, em, span, div, td, th, blockquote, a) to `color: #fff`
- `.has-light-background` must NOT override `div`, `span`, or `th` — doing so breaks component colors (`.db-flow-step`, `.db-key`, `.db-table th`)
- Use `overflow: visible` for screen display but `overflow: hidden` in `@media print` to prevent slide bleed during PDF export
- `sequenceDiagram` mermaid blocks get broken by syntax highlighting — use `flowchart` format instead

## Examples

### Example: Create slides from a plain draft
User says: "Convert this markdown into obsidian slides"
Result: Reads the file, classifies each slide, applies Databricks-branded layouts, creates CSS if needed, writes polished output.

### Example: Fix slide rendering issues
User says: "The text is invisible on my dark slides"
Result: Checks CSS for `.has-dark-background` rules, ensures all text elements are overridden to white, fixes specificity conflicts.

## Resources

- `resources/plugin-syntax.md` — Complete syntax reference for Obsidian Slides Extended
- `resources/databricks-theme.md` — Brand tokens and CSS class definitions
- `resources/slide-patterns.md` — Copy-paste layout pattern cookbook
- `resources/databricks.css` — Full CSS theme file ready to copy into any vault
