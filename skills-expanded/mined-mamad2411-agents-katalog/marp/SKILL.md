---
name: marp
description: "Handle all Marp (Markdown) slide tasks: creating new decks, editing existing slides, theme creation, outline-to-slide conversion, and reading/summarizing. Trigger on: \"create slides\", \"fix slide 3\", \"create a theme\", \"convert this outline to slides\", \"what is this slide about\", \"make a presentation\", \"build a deck\", \"write a script\", \"export to PDF\", \"edit slide\", \"review slides\". For presentation structure planning and content strategy, use a presentation-planning skill as the entry point. For .pptx file operations, use a pptx skill."
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [topic or file path]
---

# marp

Skill for all Marp slide tasks: creation, editing, theme design, conversion, and reading.

## Quick Reference

|Task|Mode|Guide|
|-|-|-|
|Create new slides|A: Create|Mode A section below|
|Edit existing slides|B: Edit|Mode B section below|
|Create/edit themes|C: Theme|[theme-guide](references/theme-guide.md)|
|Convert outline → Marp|D: Convert|Mode D section below|
|Read/summarize slides|E: Read|Mode E section below|
|Marp syntax reference|All|[marp-conventions](references/marp-conventions.md)|
|Layout patterns|A/B/D|[layout-patterns](references/layout-patterns.md)|
|Design principles|All|[slide-design-principles](references/slide-design-principles.md)|
|Quality checklist|A/B/C/D|[qa-checklist](references/qa-checklist.md)|
|Script format|A|[script-format](references/script-format.md)|

***

## Design Ideas

**Don't create boring slides.** Every slide must be visually engaging.

### Pick colors for YOUR topic

Don't default to blue. Choose colors that match your topic using the Topic → Color mapping in [theme-guide](references/theme-guide.md).
Cooking → warm tones, technology → cobalt blue, environment → olive green.

### Every slide needs a visual element

Include an image, chart, icon, or background image. Text-only slides are forbidden.
**Code blocks count as visual elements** — syntax-highlighted code, `grid-2col` Before/After comparisons, and `vs-card` code comparisons serve as visual elements in code-heavy presentations.

### Vary your layouts

Switch layout patterns every 2-3 slides. Repeating the same structure (heading + bullets) creates visual boredom.
Combine multiple patterns from [layout-patterns](references/layout-patterns.md).

### Text alignment

- Body text: **left-aligned** (center-aligned body text is hard to read)
- Center alignment is only for h1 on title slides (`lead` class)

### NEVER

- NEVER create text-only slides without any visual element
- NEVER repeat the same layout for 3+ consecutive slides
- NEVER center-align body text or bullet lists
- NEVER use default blue palette without considering the topic's emotional tone
- NEVER put a decorative accent line directly under the slide title
- NEVER mention a library/package/API/tool without a link — all external references must include links by default
- NEVER use vague terms instead of precise terminology — use exact names + `<small>` annotations for explanation
- NEVER leave `bg` images without `brightness` specification (text becomes unreadable)
- NEVER use `![bg]` with SVG diagrams without `contain` — default `cover` crops text/data SVGs

***

## Mode A: Create (New Slides)

Triggered by "create slides", "prepare presentation", "write a script".
If structure planning (story arc, audience analysis, outline) is not done, recommend running a presentation-planning skill first.

### Workflow

1. **Confirm requirements**: Topic, audience, duration, slides/script/both
2. **Design planning**: Reference [slide-design-principles](references/slide-design-principles.md) and [layout-patterns](references/layout-patterns.md) to determine layout composition
3. **Generate**: Create slide files
4. **Quality check**: Verify per [qa-checklist](references/qa-checklist.md)
5. **Visual verification**: Generate PNGs and visually inspect. If SVGs are included, run SVG quality validation
6. **PDF/PPTX export**: Generate PDF and/or PPTX output

### File Structure

```
slides/<project-name>/
├── README.md           # Presentation overview
├── 01_opening.md       # Split by section
├── 02_<topic>.md
├── 0N_closing.md
├── themes/             # Custom theme (optional)
│   └── <theme-name>.css
└── pdfs/               # PDF output
```

### Frontmatter Template

```yaml
---
marp: true
theme: default          # or custom theme name
paginate: true
---
```

### Slide Separation

Use `***` (horizontal rule) to separate slides.
Per-slide directives:

```markdown
<!-- _class: lead -->
<!-- _backgroundColor: #1a0f05 -->
```

### Scripts

See [script-format](references/script-format.md) for detailed conventions.

|Range|Purpose|Style|
|-|-|-|
|01-09|MC flow (sequential)|Conversational|
|20s|Strategy/talking points|Bulleted|
|30s|Reference material (personal notes)|Memo format|
|90s|Appendix, afterword|Supplementary|
|99|Reference links, TODO|Management|

***

## Mode B: Edit (Partial Editing)

Triggered by "fix slide 3", "change the layout", "update the text".

### Workflow

1. **Identify target**: Confirm file path and slide number
2. **Read current state**: Read the target file, understand frontmatter, theme, and structure
3. **Edit**: Apply changes with the Edit tool. Be careful not to break existing styles/theme/structure
4. **Diff verification**: Follow "Mode B: Edit diff check" in [qa-checklist](references/qa-checklist.md) to verify changes and surrounding impact
5. **Visual verification**: Generate PNGs and verify
6. **Regenerate PDF/PPTX**: Regenerate output files after editing

### Guidelines

- Only change the specified slides — do not affect others
- If changing frontmatter or theme, warn the user about whole-deck impact first
- Reference [layout-patterns](references/layout-patterns.md) when changing layouts

***

## Mode C: Theme (Create/Edit Themes)

Triggered by "create a theme", "change the colors", "make it dark".

### Workflow

1. **Confirm requirements**: Purpose, color preferences, dark/light preference
2. **Palette design**: Reference [theme-guide](references/theme-guide.md), design palette using 60-30-10 rule
3. **Generate CSS**: Create theme file following the theme file structure
4. **Contrast verification**: Follow "Mode C: Theme contrast verification" in [qa-checklist](references/qa-checklist.md) to check WCAG AA compliance
5. **Preview**: Preview with Marp CLI server mode

### Theme File Location

```
slides/<project-name>/themes/<theme-name>.css
```

***

## Mode D: Convert (Outline → Marp)

Triggered by "convert this outline to slides", "turn this memo into a deck".

### Workflow

1. **Parse input**: Analyze source file structure (headings, bullets, paragraphs)
2. **Determine slide boundaries**: Split by heading level or content breaks
3. **Generate Marp**: Add frontmatter, split with `***`, apply directives
4. **Apply design**: Reference [layout-patterns](references/layout-patterns.md) and [slide-design-principles](references/slide-design-principles.md) for appropriate layouts
5. **Verify**: Run [qa-checklist](references/qa-checklist.md) quality checks

### Conversion Guidelines

- h1 → New slide title
- h2 → In-slide heading, or new slide boundary (depending on volume)
- Bullet lists → Keep as bullets (split if over 5-6 items)
- Long paragraphs → Extract key messages into bullets

### Handling Repetitive Structures

When converting N similar items (library introductions, feature comparisons), the same layout tends to repeat. Use these 4 strategies to add variety:

1. **Grouping**: Combine related items into a single slide (e.g., compare 2 of 5 plugins side by side)
2. **Layout rotation**: Apply different layout patterns to each item
3. **Restructuring**: Reorganize from per-item to per-aspect (e.g., "challenges → solutions → config" instead of "Plugin A → B → C")
4. **Detail gradient**: Cover 1-2 representative items in detail, summarize the rest in a table

***

## Mode E: Read (Summarize)

Triggered by "what is this slide about?", "summarize this deck".

### Workflow

1. **Read file**: Load the target Marp file(s)
2. **Analyze structure**: Count slides, identify sections, theme, layouts used
3. **Generate summary**: Output in the following format

### Output Format

```
## Overview
[1-2 sentence summary of the entire presentation]

## Structure
- Slide count: N slides
- Theme: [theme name]
- Sections:
  1. [Section name] (slides N-M)
  2. ...

## Key Messages
- [Key message 1]
- [Key message 2]
- ...
```

***

## Commands

```bash
# Preview with server mode
npx @marp-team/marp-cli -s slides/ --theme ./path/to/theme.css

# Watch single file
npx @marp-team/marp-cli -w <file>.md

# PDF export (single file)
npx @marp-team/marp-cli <file>.md --pdf --allow-local-files -o pdfs/<name>.pdf

# PPTX export
npx @marp-team/marp-cli <file>.md --pptx --allow-local-files -o <name>.pptx

# HTML export
npx @marp-team/marp-cli <file>.md --html

# PNG export (for visual review)
npx @marp-team/marp-cli <file>.md --images png --allow-local-files
```

## Multi-file Slides

When a presentation is split across multiple `NN_*.md` files, concatenate them before export:

```bash
# Concatenate and export (Unix)
cat 0*.md | npx @marp-team/marp-cli --stdin --pdf --allow-local-files -o pdfs/combined.pdf

# With custom theme
cat 0*.md | npx @marp-team/marp-cli --stdin --pdf --allow-local-files --theme ./themes/my-theme.css -o pdfs/combined.pdf
```

> [!NOTE]
> When concatenating, only the first file's frontmatter is used. Remove frontmatter from subsequent files, or use `---` only in the first file.

## Quality Checklist

→ [qa-checklist](references/qa-checklist.md)

## Self-Improvement

- **Feedback Capture**: Extract generalizable principles from visual verification and user feedback on layout issues
- **Checklist Evolution**: Add extracted principles to [qa-checklist](references/qa-checklist.md)
- **Triggers**: Layout breakage, contrast issues, new validation patterns

## Project Integration

This skill works standalone, but can be customized for your project.

### Validation Scripts (customize per project)

If your project has custom validation scripts (SVG validation, contrast checking, slide density analysis), specify them here. Example:

```bash
node scripts/marp-validate.js slides/<project>/ --png
node scripts/svg-validate.js slides/<project>/images/
```

If not defined, use Marp CLI's built-in export + manual visual review.

### Lint (customize per project)

If your project uses a Markdown linter for slide scripts, specify the command here. Slide content itself is typically excluded from linting due to Marp syntax constraints.

### Cross-Skill Integration

This skill can integrate with other skills in your project:

- **SVG quality review**: When slides include SVG diagrams, invoke an SVG review skill if available
- **Presentation planning**: Receive outlines from a presentation-planning skill
- **Research notes**: Use research note output as source material for slides
- **PPTX conversion**: Hand off to a PPTX skill when PowerPoint output is needed

## Dependencies

- `@marp-team/marp-cli` - Marp CLI for rendering, export, and preview
- Google Chrome or Chromium - Required by Marp CLI for PDF/PPTX/PNG export
