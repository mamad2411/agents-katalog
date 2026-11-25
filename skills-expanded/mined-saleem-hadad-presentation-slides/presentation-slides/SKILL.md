---
name: presentation-slides
description: Create HTML presentations in a warm, playful visual style with marker highlights, dashed borders, and hand-drawn feel. Supports 5 languages including Arabic RTL. Use when the user asks to create slides, a presentation, a deck, or webinar visuals.
---

# Presentation Slides

Create zero-dependency HTML presentations in a warm, hand-crafted design language. Supports English, Arabic (RTL), French, Spanish, and German.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Multi-Language** — Ask the user which language. Adapt font, direction, and navigation accordingly.
3. **Warm Aesthetic** — Warm, playful, hand-crafted feel. Never generic, never corporate, never dark.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides. Content overflows? Split into multiple slides.
5. **One Idea Per Slide** — Big text, few words. Each slide is a talking point, not a wall of text.

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|----------------|
| Title slide | 1 heading + 1 subtitle + optional stat row |
| Statement slide | 1 tag + 1 heading + 1 body paragraph |
| Comparison slide | 1 heading + 2 column cards (max 6 items each) |
| Evidence slide | 1 tag + 1 heading + 1 body + 1 commit log (max 5 entries) |
| Question slide | 1 heading only (with decorative question marks) |
| Chart slide | 1 heading + 1 bar chart + 1 caption line |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode B modification rules below.**

### Mode B: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

---

## Phase 1: Content Discovery

**Ask ALL questions in a single AskUserQuestion call** so the user fills everything out at once:

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Webinar-Talk / Teaching-Tutorial / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Language** (header: "Language"):
What language? Options: English / Arabic (RTL) / French / Spanish / German

**Question 4 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

If user has content, ask them to share it.

**There is no style discovery phase. The style is always this design system. There is no style choice.**

---

## Phase 2: Generate Presentation

Generate the full presentation using content from Phase 1 and the design system defined in this file.

**Before generating, read these supporting files:**

- [html-template.md](html-template.md) — HTML architecture, JS features, and slide structure
- [viewport-base.css](viewport-base.css) — Mandatory responsive CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference

**Key requirements:**

- Single self-contained HTML file, all CSS/JS inline
- Set `lang` and `dir` attributes based on language choice (see [html-template.md](html-template.md))
- Include the FULL contents of viewport-base.css in the `<style>` block
- Use the language-appropriate Google Font (see [html-template.md](html-template.md))
- Rotate slide backgrounds — never two adjacent slides with the same color
- Use marker highlights on 1–2 key words per slide, not more
- Add wavy SVG decorations on ~30% of slides
- Add question mark decorations on thought-provoking slides
- Mobile responsive with single-column fallback for grids

---

## Phase 3: Delivery

1. **Open** — Use `open [filename].html` to launch in browser
2. **Summarize** — Tell the user:
   - File location and slide count
   - Navigation controls (direction-aware based on language)
   - How to customize: CSS variables in `:root` for colors, font link for typography

---

## Phase 4: Share & Export (Optional)

After delivery, ask the user: "Would you like to share this presentation? I can deploy it to a live URL or export it as a PDF."

Options: Deploy to URL / Export to PDF / Both / No thanks

If the user declines, stop here.

### Deploy to URL (Vercel)

Run `bash scripts/deploy.sh <path-to-html>`. See the script for full instructions on Vercel setup.

### Export to PDF

Run `bash scripts/export-pdf.sh <path-to-html> [output.pdf]`. The script captures each slide as a screenshot and combines them into a PDF. Note: animations are not preserved — the PDF is a static snapshot.

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [viewport-base.css](viewport-base.css) | Mandatory responsive CSS — copy into every presentation | Phase 2 (generation) |
| [html-template.md](html-template.md) | HTML structure, JS features, language config | Phase 2 (generation) |
| [animation-patterns.md](animation-patterns.md) | CSS animation snippets and patterns | Phase 2 (generation) |
| [scripts/deploy.sh](scripts/deploy.sh) | Deploy slides to Vercel for sharing | Phase 4 (sharing) |
| [scripts/export-pdf.sh](scripts/export-pdf.sh) | Export slides to PDF | Phase 4 (export) |
