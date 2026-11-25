---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides

Create animation-rich, Tailwind-styled HTML presentations that run entirely in the browser.

## Core Principles

1. **Single file, no build step** — One self-contained HTML file. Tailwind via CDN script, fonts via Google Fonts/Fontshare. No npm, no build tools.
2. **Tailwind for all styling** — Utility classes in markup. Raw CSS only in the three sanctioned blocks (see Styling Conventions).
3. **Show, don't tell** — Generate visual previews; users discover taste by seeing options, not describing them.
4. **Distinctive design** — No generic "AI slop." Every deck must feel custom-crafted.
5. **Progressive disclosure** — Read lightweight style indexes first; load a full `design.md` only after the user picks that template.
6. **Fixed 16:9 stage (NON-NEGOTIABLE)** — Slides are authored at 1920×1080 and the stage scales as a whole to the viewport; never reflow content per device.

## Styling Conventions (Tailwind)

Every deck and preview uses the same architecture:

- Load Tailwind in `<head>`: `<script src="https://cdn.tailwindcss.com"></script>`.
- Declare design tokens in an inline `tailwind.config` block — colors and fontFamily map to CSS variables or literal values (see [html-template.md](html-template.md)).
- Style everything with utilities in markup: layout, spacing, typography, color, borders, effects.
- Use arbitrary values for stage-pixel geometry: `left-[96px]`, `text-[168px]`, `tracking-[0.18em]`, `max-w-[1360px]`.
- Raw CSS lives in exactly three labeled `<style>` sections, nothing else:
  1. **Stage mechanics** — the full contents of [viewport-base.css](viewport-base.css), pasted verbatim.
  2. **Token definitions** — CSS variables (`--lp-*` for presets, theme vars for decks) that `tailwind.config` references.
  3. **Choreography** — `@keyframes` plus `.slide.active`-scoped animation triggers (state-dependent animation can't be pure utilities).
- Elements keep one short semantic class (`lp-title`, `reveal`) only as an animation/JS hook — all visual styling stays in utilities.
- Never build class names dynamically in JS (`bg-${color}` breaks the CDN JIT); toggle complete class strings.
- No spaces inside arbitrary values — use underscores: `shadow-[0_8px_32px_rgba(0,0,0,0.3)]`.
- Negate CSS functions with calc: `right-[calc(-1*clamp(28px,3.5vw,44px))]`; a leading `-` before a function is silently dropped.

## Design Aesthetics

You converge toward generic, "on distribution" outputs — the "AI slop" aesthetic. Actively resist it:

- **Typography:** pick beautiful, distinctive fonts; never Arial, Inter, Roboto, or system fonts.
- **Color:** commit to a cohesive palette via tokens; dominant colors with sharp accents beat timid, even distributions.
- **Motion:** prioritize CSS-only animation; one well-orchestrated staggered page load beats scattered micro-interactions.
- **Backgrounds:** build atmosphere with layered gradients, geometric patterns, or contextual effects — not flat default colors.

Avoid: purple-gradient-on-white clichés, predictable centered layouts, cookie-cutter card grids, and over-reused picks like Space Grotesk. Vary light/dark themes and aesthetics between generations.

## Fixed Stage Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every deck has a `.deck-viewport` wrapper filling the window and a `.deck-stage` fixed at 1920×1080.
- JS scales the whole stage uniformly (letterbox/pillarbox allowed); never re-layout content per device.
- No responsive breakpoints inside slides; author all measurements at the 1920×1080 design size.
- Slide switching uses `.active`/`.visible` via `visibility`/`opacity`/`pointer-events` from viewport-base.css — never `display: none`/`block`, which layout utilities like `flex` can override.
- `clamp()` is only for UI outside the stage or small fallback previews.
- Include `prefers-reduced-motion` support (shipped in viewport-base.css).

### Content Density Modes

Ask whether this is a reading deck or a speaking deck, then design around the answer:

| Density mode | Best for | Design behavior |
| --- | --- | --- |
| **Low density / speaker-led** | Talks, keynotes, live explanation | One idea per slide, large type, 1–3 bullets max, generous negative space, more slides |
| **High density / reading-first** | Reports, handouts, async review | Self-contained slides, structured grids/tables, 4–8 bullets or 4–6 cards, tight but intentional spacing |

Hard limits in both modes: no scrolling, no overflow, no overlapping panels, no uncomfortably small text. Split into more slides rather than shrinking content.

---

## Phase 0: Detect Mode

- **Mode A: New presentation** — go to Phase 1.
- **Mode B: PPT conversion** — go to Phase 4.
- **Mode C: Enhancement** — read the existing HTML, then follow the modification rules below.

### Mode C: Modification Rules

1. Before adding content, count existing elements against the density limits.
2. Adding images: fit inside the 1920×1080 canvas; if the slide is full, split into two slides.
3. Adding text: max 4–6 bullets per slide; split overflow into continuation slides.
4. After ANY modification verify: stage still 16:9, no text overflow, no panel overlap, screenshots correct at 1280×720 and one phone viewport.
5. Proactively split content that would overflow and inform the user — don't wait to be asked.

---

## Phase 1: Content Discovery (New Presentations)

Ask ALL questions together (use the native structured-question UI if available, else one numbered message):

1. **Purpose** — Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation.
2. **Length** — Short 5–10 / Medium 10–20 / Long 20+.
3. **Content** — All content ready / Rough notes / Topic only.
4. **Density** — "Low density / speaker-led" or "High density / reading-first" (see table above).

Do NOT ask about inline editing pre-draft; it's included by default unless the user asks for a locked/export-only file. If the user has content, ask them to share it. Remember the density choice — it drives slide count, type scale, and layout density.

### Step 1.2: Image Evaluation (if images provided)

1. Scan the folder for image files (.png, .jpg, .svg, .webp, …).
2. Inspect each with image understanding (fall back to filenames/metadata and ask only when needed).
3. Evaluate each: what it shows, USABLE or NOT (with reason), concept, dominant colors.
4. Co-design the outline around text AND images together (3 screenshots → 3 feature slides), not "plan then decorate."
5. Confirm outline: "Does this slide outline and image selection look right?" — Looks good / Adjust images / Adjust outline.
6. If a usable logo exists, embed it (base64) in each Phase 2 style preview.

---

## Phase 2: Style Discovery

Generate 3 distinct single-slide HTML previews (typography, color, animation, aesthetic) — never ask abstract style questions or offer a preset-name picker. If the user named a vibe or template, honor it; otherwise infer mood from occasion, audience, content, and stakes.

Read [STYLE_PRESETS.md](STYLE_PRESETS.md) and [bold-template-pack/selection-index.json](bold-template-pack/selection-index.json) first; do not read any `design.md` yet.

| Mood | Suggested presets |
| --- | --- |
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

**Preview mix:**

- Default trio: 1 safe preset from STYLE_PRESETS.md + at least 1 bold template + 1 wildcard.
- The wildcard is a second bold template or a self-generated custom design — whichever contrasts most usefully.
- Conservative/high-stakes deck: restrained safe preset, calm formal template, authoritative wildcard.
- Expressive deck: readable safe fallback, one strong template, one adventurous context-specific wildcard.
- Weak template matches? Use the wildcard as a custom design or a second safe preset — never force a template.

**Custom wildcard rules:**

- Obey Design Aesthetics: distinctive type, committed palette, recognizable layout system, one strong atmospheric device.
- Design for THIS deck's occasion, audience, mood, and density — authored, not merely stylish.
- Must imply a system that expands to section, content, quote, comparison, and closing slides.
- Same fixed-stage and authenticity rules as every preview; never render "custom"/"wildcard"/process labels on the slide.

**Bold template selection:**

- Match purpose/mood against `mood`, `tone`, `best_for`, `avoid_for`, `formality`, `density`, `scheme`; treat `best_for` as soft signal.
- Keep the three previews genuinely different from each other.
- After shortlisting, read only the candidates' `preview.md` (for title previews); full `design.md` waits for the final pick.

**Preview authenticity (NON-NEGOTIABLE):**

- Every preview must read as a real first slide of the user's deck, not a diagnostic card.
- Never render workflow text: "preview", "template", "preset", "Option A/B/C", file names, paths, or template/slug names.
- Never render requirement notes ("safe option", "audience: …") unless the user wants that exact phrase in the deck.
- Slide chrome must be real deck chrome: title, section, date, author, company, page number, genuine content.
- Before opening previews, inspect visible text and strip any internal metadata.

Save previews to `.frontend-slides/slide-previews/` (style-a.html, style-b.html, style-c.html) — each self-contained, one animated title slide — and open them automatically.

### Step 2.1: User Picks

Ask (header: "Style"): Style A: [Name] / Style B: [Name] / Style C: [Name] / Mix elements. If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Generate the full deck from Phase 1 content and the Phase 2 style. No images? CSS-generated visuals (gradients, shapes, patterns) are a first-class path.

Apply the density choice throughout:

- **Low density:** more slides, fewer ideas each; large headings, short phrases, section beats, quote slides.
- **High density:** self-contained slides; structured grids, tables, annotated diagrams, concise copy with strong hierarchy.
- Mixed needs: pick the closer mode (live persuasion → low; async circulation → high); split any slide that starts to overflow.

**If a bold template was chosen**, read that one template's full `design.md` (only that one) and treat it as the design recipe:

- Preserve its fonts, palette, decorative vocabulary, spacing rhythm, and component grammar.
- Generate as a fixed 1920×1080 stage regardless of the source template's original behavior.
- Translate any viewport-fluid values (vw/vh) in `design.md` into fixed 1920×1080 stage pixels — never keep live reflow rules.
- After generating, verify overflow AND panel overlap in rendered screenshots; `scrollHeight` checks alone miss visual overlap.

**If a custom wildcard was chosen**, its preview markup and config are the design recipe: expand the same system across the deck; never switch to a preset/template afterward.

**Layout presets are mandatory for covered slots** (opening, section, list, stats, chart, quote, comparison, timeline, image, video, closing):

- Read [layout-presets/README.md](layout-presets/README.md), pick a preset per slot, read that preset's `layout.md`.
- The preset fixes structure (geometry, hierarchy, limits, choreography); the design system supplies the skin via the `lp` token mapping.
- Substitute decoration only at documented skin points; if structure and decoration conflict, structure wins.
- Reusing one list/stats preset across slides is fine — vary content, not composition.
- Images are optional in every preset; each documents an Image variant with a `placehold.co` size, `object-cover` frame, and CSS fill fallback.
- Default every slide to a preset; go custom only when nothing fits, staying within fixed-stage and density rules.
- Comment each slide: `<!-- Slide 5: Market Growth — layout: stats/big-number (modified: added third stat) -->` (`layout: custom` when fully custom).

**Before generating, read:** [html-template.md](html-template.md) (architecture + JS), [viewport-base.css](viewport-base.css) (include verbatim), [animation-patterns.md](animation-patterns.md), [layout-presets/README.md](layout-presets/README.md).

**Output requirements:**

- Single self-contained HTML file: Tailwind CDN + config block, utilities in markup, the three sanctioned `<style>` sections only.
- Include the FULL viewport-base.css contents in the stage-mechanics block.
- Fonts from Fontshare or Google Fonts — never system fonts.
- Comment every major section: `<!-- === SECTION NAME === -->`.

---

## Phase 4: PPT Conversion

1. Extract: `python scripts/extract-pptx.py <input.pptx> <output_dir>` (needs `pip install python-pptx`).
2. Confirm extracted titles, content summaries, and image counts with the user.
3. Run Phase 2 for style discovery.
4. Generate HTML in the chosen style, preserving text, images (from assets/), slide order, and speaker notes as HTML comments.

---

## Phase 5: Delivery

1. Delete `.frontend-slides/slide-previews/` if present.
2. Open the file in the browser (`open [filename].html`).
3. Summarize for the user:
   - File location, style name, slide count.
   - Navigation: arrow keys, Space, swipe/tap if enabled.
   - Customization: token values in the `tailwind.config` block (colors/fonts), font `<link>` for typography, utility classes on any element.
   - Inline editing: hover top-left corner or press E, click any text, Ctrl+S to save.
   - Offer next steps: revisions, in-browser text edits, or export/share.

---

## Phase 6: Share & Export (Optional)

Ask: _"Would you like to share this presentation? I can deploy it to a live URL (works on any device) or export it as a PDF."_ Options: Deploy to URL / Export to PDF / Both / No thanks. If declined, stop.

### 6A: Deploy to a Live URL (Vercel)

1. Check CLI: `npx vercel --version`; if missing, install Node.js first (`brew install node` or nodejs.org).
2. Check login: `npx vercel whoami`; if not logged in, walk them through https://vercel.com/signup then `vercel login`, and wait for confirmation.
3. Deploy: `bash scripts/deploy.sh <path>` (accepts a folder with index.html or a single HTML file).
4. Share the URL; note it works on any device, redeploying updates the same URL, and teardown is at https://vercel.com/dashboard (free tier).

**Gotchas:**

- Local assets must travel with the HTML; the script bundles `src="..."` references but can miss CSS `background-image` paths — open the deployed URL and check every image.
- Many assets? Deploy the whole folder (`bash scripts/deploy.sh ./my-deck/`) — more reliable than a single file.
- Spaces in filenames become `%20`; if images break, rename with hyphens.

### 6B: Export to PDF

1. Run `bash scripts/export-pdf.sh <path-to-html> [output.pdf]` (PDF lands next to the HTML if no output given).
2. Explain: headless browser screenshots each slide at 1920×1080 and combines them; Playwright auto-installs if missing.
3. If Playwright fails: `npx playwright install chromium`; persistent failure is usually network/firewall.
4. Deliver: file location and size; note animations render as their final static state.

**Gotchas:**

- First run downloads Chromium (~150MB) — warn it may take 30–60s once.
- The script finds slides via `.slide`; externally-created HTML with other class names reports "0 slides found."
- Images must be relative paths (served over local HTTP); absolute filesystem paths won't load.
- PDF over 10MB? Offer `--compact` (renders at 1280×720, ~50–70% smaller).

---

## Supporting Files

| File | Purpose | When to read |
| --- | --- | --- |
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 12 curated visual presets: Tailwind token configs, fonts, signature elements | Phase 2 |
| [bold-template-pack/selection-index.json](bold-template-pack/selection-index.json) | Compact bold-template metadata for candidate selection | Phase 2 |
| [bold-template-pack/templates/*/preview.md](bold-template-pack/templates/) | Lightweight style cards for shortlisted title previews | Phase 2, after shortlisting |
| [bold-template-pack/templates/*/design.md](bold-template-pack/templates/) | Full design-system doc for the selected template only | Phase 3, after selection |
| [layout-presets/README.md](layout-presets/README.md) | Style-agnostic structural layouts + `lp` token contract | Phase 3 |
| [layout-presets/\*/\*/layout.md](layout-presets/) | Geometry, limits, choreography for the chosen preset | Phase 3 |
| [viewport-base.css](viewport-base.css) | Mandatory stage-mechanics CSS — paste verbatim into every deck | Phase 3 |
| [html-template.md](html-template.md) | HTML architecture, Tailwind config pattern, JS features | Phase 3 |
| [animation-patterns.md](animation-patterns.md) | Animation snippets (Tailwind + choreography CSS) by feeling | Phase 3 |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | PPT content extraction | Phase 4 |
| [scripts/deploy.sh](scripts/deploy.sh) | Vercel deployment | Phase 6 |
| [scripts/export-pdf.sh](scripts/export-pdf.sh) | PDF export | Phase 6 |
