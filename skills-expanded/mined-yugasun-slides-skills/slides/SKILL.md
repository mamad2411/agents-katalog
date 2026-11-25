---
name: slides
description: Generate high-quality HTML slide presentations with beautiful templates. Make sure to use this skill whenever the user mentions slides, presentation, PPT, deck, keynote, 演示文稿, or 幻灯片 — even if they don't explicitly ask for HTML or templates. This skill handles both polished multi-template workflows and fast self-contained themes. Use it for any request involving creating, building, or generating a presentation regardless of how the request is phrased.
license: MIT
author: yugasun
homepage: https://github.com/yugasun/slides-skills
version: 1.0.0
config:
  outputRoot: "~/slides"   # default output directory; override via --slides-root or user request
  previewOpen: true         # auto-open preview in browser after generation
---

# Interactive HTML Slide Generator

## Output Directory

Generated decks are saved under `~/slides/<deck-name>/` by default. Before generating, the skill:

1. Expands `~` to the user's home directory
2. Creates the output directory if it doesn't exist (`mkdir -p`)
3. Creates `slides/<deck-name>/previews/` for Workflow A preview files
4. Creates `slides/<deck-name>/` for the final deck

**Custom root directory**: If the user specifies a path (e.g., "save it to `~/my-decks`" or "output to `/tmp/slides`"), use that instead of the default. Respect the user's intent — don't override a explicitly requested path.

**Directory initialization example**:
```bash
mkdir -p ~/slides/my-deck/previews
mkdir -p ~/slides/my-deck/previews
```

---

## Two Workflows

This skill supports **two workflows**:

- **Workflow A — Beautiful HTML Templates** (recommended): 32 professionally-designed templates. Best for polished, visually distinctive decks. Asks about occasion and mood, presents 3 candidates, builds from real template HTML/CSS/JS.
- **Workflow B — Built-in CSS Themes**: 4 CSS themes (Cyberpunk, Corporate, Minimal, Nature). Fast, self-contained single-file output, no external dependencies.

**Default to Workflow A** unless the user explicitly asks for a specific theme or wants a minimal/lightweight output.

---

## Workflow A — Beautiful HTML Templates (Recommended)

### Step 1 — Clarify Taste

Ask the user two questions before picking any template:

> "Two quick questions before I pick a template:
> 1. **What's the occasion?** (e.g. product launch, research talk, brand manifesto, classroom, team review, etc.)
> 2. **What mood / vibe do you want?** (e.g. confident & editorial, warm & playful, dark & moody, quiet & literary, etc.)"

Wait for the user's answer. Do not skip this — the user's stated taste reveals what no inferred brief can.

### Step 2 — Read index.json and Shortlist 3 Candidates

Read `skills/ppt/beautiful-html-templates/index.json`. Match the user's stated **occasion + mood** against each template's `mood`, `tone`, `formality`, `density`, and `scheme` fields.

Pick **three templates** whose tones genuinely fit and are *different enough* from each other (e.g., don't pick three editorial templates — pick one editorial, one warmer alternative, and one wildcard).

### Step 3 — Build Title-Slide Previews of Each Candidate

For each of the 3 candidates:

1. Read `skills/ppt/beautiful-html-templates/templates/<slug>/template.html`
2. Extract **the first slide only** (the cover/title slide)
3. Replace placeholder content with **the user's actual topic/title/subtitle/author/date**
4. Save as `~/slides/<deck-name>/previews/01-<slug>.html`
5. Initialize `~/slides/<deck-name>/` for later use

Open each preview with `open <path>` (macOS) and send the user a message:

> "Three options to compare:
> 1. **<Template A>** — <one-line tone description>
>    `~/slides/<deck-name>/previews/01-template-a.html`
> 2. **<Template B>** — <one-line tone description>
>    `~/slides/<deck-name>/previews/02-template-b.html`
> 3. **<Template C>** — <one-line tone description>
>    `~/slides/<deck-name>/previews/03-template-c.html`
>
> Which one feels right?"

Wait for the user to pick.

### Step 4 — Build the Full Deck

Once the user picks:

1. Read `skills/ppt/beautiful-html-templates/templates/<slug>/template.html` in full
2. Adapt every slide per the rules in [AGENTS.md](./beautiful-html-templates/AGENTS.md) §3 — preserve the design system, replace placeholder content
3. Add/remove/split slides to match the user's content outline
4. **If a layout is missing**, design it using the template's fonts, color palette, decorative vocabulary, and spacing rhythm — see [AGENTS.md](./beautiful-html-templates/AGENTS.md) §5
5. Ensure the navigation (keyboard/click) works correctly
6. Save the final deck as `~/slides/<deck-name>/index.html`

### Step 5 — Open and Deliver

Open the final deck with `open <path>`. Send:

> "Done. Your deck is at `~/slides/<deck-name>/index.html` — opened in your browser."

---

## Workflow B — Built-in CSS Themes (Fallback)

Use this when the user wants a specific theme or a self-contained minimal output.

### Theme Selection

| Theme | Style | When to Use |
|---|---|---|
| **Cyberpunk** | Dark, neon, futuristic | Default — tech, gaming, innovation |
| **Corporate** | Light, professional, blue/slate | Business, formal reports |
| **Minimal** | Black & white, Swiss style | Academic, stark, editorial |
| **Nature** | Cream/green, elegant serif | Warm, organic, literary |

**Default to Cyberpunk** if no theme is specified.

### Assembly Process

1. **Read reference files**: the selected CSS theme + `templates/template.html` + `templates/scripts.js` + `templates/layouts.md`
2. **Load Template**: Start with `template.html`
3. **Inject CSS**: Replace `/* CSS_INJECTION_POINT */` with the selected theme CSS
4. **Inject JS**: Replace `/* JS_INJECTION_POINT */` with `scripts.js`, then replace `[TOTAL_SLIDES_COUNT]` with the actual number
5. **Generate Slides**: Create HTML using patterns from `layouts.md`
6. **Inject Slides**: Replace `<!-- SLIDES_INJECTION_POINT -->`
7. **Save**: `~/slides/<deck-name>/index.html`

---

## Overflow Prevention (Workflow B)

Slides are fixed **1280×720px**. Overflow is hidden and will clip content silently.

| Element | Max | If Exceeded |
|---|---|---|
| Bullets | **5** | Split into 2 slides |
| Cards | **3** | Use `.compact` or split |
| Code lines | **10** | Use `.scrollable` on content-area |
| Card body | 2 lines | Shorten |

**Rules**:
- Max 5 bullets per slide, each max 1-2 lines
- Max 3 cards per grid slide
- Never stack bullets + cards + code on the same slide
- Use `.compact` class to reduce font sizes and spacing
- Prefer splitting over cramming

---

## Template Index Summary

| Slug | Name | Mood | Scheme |
|---|---|---|---|
| 8-bit-orbit | 8-Bit Orbit | retro-tech, playful, cyberpunk | dark |
| biennale-yellow | Biennale Yellow | editorial, atmospheric, warm | light |
| block-frame | BlockFrame | neobrutalist, pastel-neon | mixed |
| blue-professional | Blue Professional | clean, modern, professional | light |
| bold-poster | Bold Poster | editorial, massive display | light |
| broadside | Broadside | dark editorial, orange accent | dark |
| capsule | Capsule | modular, pastel-pop | light |
| cartesian | Cartesian | quiet, warm, classical | light |
| cobalt-grid | Cobalt Grid | electric, graph-paper | dark |
| coral | Coral | cream/coral, oversized display | dark |
| creative-mode | Creative Mode | confident, multi-color | light |
| daisy-days | Daisy Days | cheerful, pastel, hand-drawn | light |
| editorial-tri-tone | Editorial Tri-Tone | dusty pink, mustard, burgundy | light |
| grove | Grove | forest-green, classical serif | dark |
| long-table | Long Table | cream/rust, supper-club | light |
| mat | Mat | dark sage, mid-century modern | dark |
| monochrome | Monochrome | ivory, all-black, literary | light |
| neo-grid-bold | Neo-Grid Bold | neo-brutalist, neon yellow | light |
| peoples-platform | People's Platform | activist, bold colors | light |
| pin-and-paper | Pin & Paper | yellow paper, handwritten | light |
| pink-script | Pink Script | hot pink, late-night luxury | dark |
| playful | Playful | sun-warm, indie launch | light |
| raw-grid | Raw Grid | neo-brutalist, thick borders | light |
| retro-windows | Retro Windows | Windows 95, pixel nostalgia | light |
| retro-zine | Retro Zine | riso-printed, beige/green | light |
| sakura-chroma | Sakura Chroma | vintage Japanese cassette | light |
| scatterbrain | Scatterbrain | post-it, pastel handwriting | light |
| signal | Signal | navy, bone, muted-gold | dark |
| soft-editorial | Soft Editorial | serif, warm paper, sage/blush | light |
| stencil-tablet | Stencil & Tablet | stencil-cut, earth palette | light |
| studio | Studio | black canvas, electric yellow | dark |
| vellum | Vellum | navy, yellow italic serif | dark |

Full details in `beautiful-html-templates/index.json`.
