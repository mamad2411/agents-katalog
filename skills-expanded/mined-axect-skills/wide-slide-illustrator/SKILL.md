---
name: wide-slide-illustrator
description: >
  Compose image-generation prompts for wide 18:9 infographic slides that
  explain methodology, data pipelines, architectures, or research ideas. Support
  Friendly Whiteboard, Editorial Magazine, Engineering Blueprint, Swiss
  Minimalist, Dark Tech/Neon, and Scientific Poster styles, with English-only
  on-image text and style-specific hard negatives. Use when the user asks for
  slide illustrations, pipeline diagrams, paper hero figures, journal-style
  methodology figures, keynote backdrops, or prompts for ChatGPT Image,
  gpt-image, DALL-E, Sora, or Midjourney.
---

# Wide Slide Illustrator — Image Prompt Composer

Generate detailed prompts for raster image-generation models (ChatGPT Image 2.0,
DALL-E 3, gpt-image-1, Sora image, Midjourney) that produce wide cinematic
multi-panel infographic slides for research talks, blog posts, and reports.

Six reusable style variants are available; all share the same 5-panel 18:9
composition and the English-only-on-canvas guard rail, and differ only in
surface treatment.

| Style                          | Style block                                       | Worked example                                |
|--------------------------------|---------------------------------------------------|-----------------------------------------------|
| Friendly Whiteboard            | `references/friendly-whiteboard-style.md`         | `references/example-osprey-v021.md`           |
| Editorial Magazine             | `references/editorial-magazine-style.md`          | `references/example-osprey-editorial.md`      |
| Engineering Blueprint          | `references/engineering-blueprint-style.md`       | (none yet)                                    |
| Swiss Minimalist               | `references/swiss-minimalist-style.md`            | (none yet)                                    |
| Dark Tech / Neon               | `references/dark-tech-neon-style.md`              | (none yet)                                    |
| Scientific Poster (PRX/Nature) | `references/scientific-poster-style.md`           | (none yet)                                    |

- **Friendly Whiteboard** — warm whiteboard sketch, wavy strokes, stickers,
  sticky notes, chalk-style chunky arrows. Approved on 2026-04-27.
- **Editorial Magazine** — Quanta / NYT / The Atlantic feature-spread feel:
  cream paper, hairline rules, serif headline, status-badge / pull-quote /
  connection-line patterns. Approved on 2026-05-08 after a v1→v2 hardening
  pass.
- **Engineering Blueprint** — NASA / SpaceX / CAD blueprint feel: deep navy
  ground, cyan technical linework, monospace annotations, dimension lines and
  terminal nodes. Sub-patterns: DIMENSION-LINE / TERMINAL-NODE / STAGE-BOX.
  Drafted on 2026-05-08 (untested by user yet).
- **Swiss Minimalist (reframed)** — Müller-Brockmann / Vignelli typographic
  discipline applied to METHODOLOGY content: paper white, primary palette,
  single geometric sans, strict 12-column grid, hairline-rule dividers, but
  data plots / equations / parameter cards preserved inside panels.
  Sub-patterns: PROMINENT-NUMBER / PRIMARY-PLOT / GRID-CARD. Reframed on
  2026-05-08 after orthodox v1 stripped all methodology content
  ("예쁘긴 한데 아무 의미가 없는데?"). Orthodox title-poster mode is opt-in
  via the "Orthodox Müller-Brockmann" tone dial.
- **Dark Tech / Neon** — Linear / Anthropic / Cursor dark-mode product-page
  feel: charcoal ground, thin neon-accented strokes with subtle outer glow,
  monospace labels, "::" delimiters, NEON-CHIP containers. Sub-patterns:
  NEON-CHIP / GLOW-PATH / MONOSPACE-LABEL. Drafted on 2026-05-08 (untested by
  user yet).
- **Scientific Poster (PRX/Nature)** — published journal figure feel: white
  paper, black ink, viridis data ramp, serif body, panel labels (a)…(e),
  running FIG. N. caption, inward tick marks, no bottom ribbon. Sub-patterns:
  PANEL-LETTER / FIG-CAPTION / AXIS-LABEL. Drafted on 2026-05-08 (untested
  by user yet).

**Always include the explicit hard-negatives bullet** from the chosen style
block — without it, cues from other variants (wobbly curves, rubber-stamp
pass/reject, hand-lettered notes, chunky radiation arrows, infographic stage
names, neon glow on a journal figure, etc.) leak through. This was the v1→v2
lesson from the editorial variant.

If the user does not specify a style, ask once before composing.

## When to use

Trigger this skill when the user wants an **image-generator prompt** (not a
matplotlib/seaborn plot) for one of:

- A **methodology / pipeline / architecture** overview slide — for a lab
  meeting / seminar / workshop (friendly variant) OR a paper hero figure /
  blog post / report cover (editorial variant).
- A **data-generation flowchart** with multiple stages flowing left-to-right.
- A **"how X works"** explainer figure for a casual deck or a published
  article.

Do NOT use for:

- Publication figures with strict statistical content → use `scienceplot-py`.
- Real plots from data (matplotlib, seaborn, plotly) → write code directly.
- Slide *decks* (multi-slide presentations) → use `claude-typst-slides` or
  `frontend-slides`.

## How to compose a prompt

### Step 1 — Pick and read the style block

Decide which style applies — see the variant table above. Six variants:
Friendly Whiteboard, Editorial Magazine, Engineering Blueprint, Swiss
Minimalist, Dark Tech / Neon, Scientific Poster. If unclear, ask the user.
Then read the corresponding style file in full. The wording in those files is
what the user validated (or is the canonical draft for untested variants); do
not paraphrase.

Each non-Friendly variant defines named sub-patterns inside its style file.
Use them by name in the prompt whenever a panel would otherwise want
something the variant explicitly bans:

| Variant                | Sub-patterns to invoke by name                              |
|------------------------|--------------------------------------------------------------|
| Editorial Magazine     | STATUS-BADGE / PULL-QUOTE / CONNECTION-LINE                  |
| Engineering Blueprint  | DIMENSION-LINE / TERMINAL-NODE / STAGE-BOX                   |
| Swiss Minimalist       | PROMINENT-NUMBER / PRIMARY-PLOT / GRID-CARD                  |
| Dark Tech / Neon       | NEON-CHIP / GLOW-PATH / MONOSPACE-LABEL                      |
| Scientific Poster      | PANEL-LETTER / FIG-CAPTION / AXIS-LABEL                      |

### Step 2 — Gather task-specific content

Ask (or infer from context) the answers to:

1. **Title** (one short headline + optional subtitle).
2. **Number of panels** (default 5, range 3–6).
3. **Per-panel content**: what each panel illustrates, what equations / labels
   / icons should appear, in plain English.
4. **Aspect ratio** (default 18:9 cinematic wide; alternatives 16:9, 3:2, 4:3).
5. **Footer ribbon facts** (small chips with constants, seeds, scales, etc.) —
   optional but recommended.
6. **Domain-specific accuracy constraints**: math symbols, axis labels, exact
   parameter names. The skill must reproduce these verbatim.

If the user gave a research-log entry, code file, or paper section as source,
extract these facts from it directly — do NOT hallucinate.

### Step 3 — Assemble the prompt

The output prompt must contain, in order:

1. **One-paragraph framing** — adjust per chosen style:
   - Friendly: "A cinematic-wide {aspect} horizontal infographic illustrating
     {topic}, designed as a friendly conference-slide visual (NOT a stiff
     academic figure). All text in the image MUST be in English only."
   - Editorial: "A cinematic-wide {aspect} horizontal infographic illustrating
     {topic}, designed as a refined magazine-style spread — Quanta / NYT
     feature-article feel (NOT a friendly whiteboard sketch and NOT a stiff
     academic figure). The whole spread should look engraved / printed, not
     sketched. All text in the image MUST be in English only."
   - Engineering Blueprint: "A cinematic-wide {aspect} horizontal technical
     schematic illustrating {topic}, designed as an engineering blueprint
     sheet — NASA / SpaceX / CAD-precise feel. Deep navy ground, cyan
     linework, monospace annotations. NOT a friendly slide, NOT a magazine
     spread. All text in the image MUST be in English only."
   - Swiss Minimalist: "A cinematic-wide {aspect} horizontal explanatory
     poster illustrating {topic}, designed with Swiss design school
     typographic and grid discipline — Müller-Brockmann / Vignelli feel —
     applied to methodology content. Paper white, primary palette, single
     geometric sans typeface, strict 12-column grid, generous whitespace.
     Data plots, equations, and parameter cards stay inside the panels,
     styled in Swiss manner. NOT an orthodox title poster that strips
     content. NOT an infographic with decorations. All text in the image
     MUST be in English only."
   - Dark Tech / Neon: "A cinematic-wide {aspect} horizontal dark-mode
     product page illustrating {topic}, designed as a Linear / Anthropic /
     Cursor keynote slide — modern AI-lab feel. Charcoal ground, thin
     neon-accented linework with subtle glow, monospace labels. NOT a
     paper figure, NOT a sketch. All text in the image MUST be in English
     only."
   - Scientific Poster: "A cinematic-wide {aspect} horizontal journal
     figure illustrating {topic}, designed as a Phys Rev / Nature published
     figure — sober, precise, peer-reviewed feel. White paper, black ink,
     viridis data ramp, serif body, panel labels (a)…(e), running FIG. N.
     caption. NOT a slide, NOT an infographic. All text in the image MUST
     be in English only."
2. **`OVERALL LOOK:` block** — copy verbatim from the chosen style file
   (one of the six in the variant table). Always include the
   "Hard negatives" bullet.
3. **`TITLE BAR:` block** — headline + optional subtitle text.
4. **`PANEL N — "<short name>":`** blocks — one per panel, with concrete
   sub-bullets describing graphics, labels, equations, and tiny notes.
5. **`BOTTOM RIBBON:` block** — small chips with constants / metadata.
6. **`TYPOGRAPHY:`, `COMPOSITION:`, `MOOD:` closing blocks** — copy from the
   style reference.
7. **English-only text guard rail**, repeated at the end:
   "IMPORTANT: every character on the canvas must be readable English. Render
   math with plain ASCII / Greek letters only (α β σ μ Σ are fine); no
   decorative non-Latin script anywhere."

### Step 4 — Deliver to the user

Present the final prompt inside a fenced code block so the user can copy-paste
it directly into the image generator. Below the prompt, add a short usage tip
section covering:

- **Aspect-ratio reality check**: gpt-image-1 supports 1024×1024, 1024×1536,
  1536×1024 — for true 18:9 generate at 1536×1024 and crop top/bottom, or use
  a service that allows custom dimensions (Midjourney `--ar 18:9`).
- **Text rendering caveat**: even with the English-only guard, expect 1–2
  retries; pick the cleanest output or composite text in post.
- **Tone dials**: each style file ends with a tone-dials table. Friendly can
  go calmer (drop stickers + chalk arrows) or more playful (add coffee-cup +
  sticky-note). Editorial can go more print-zine (paper grain + drop cap) or
  cleaner Bauhaus (drop foil-gold + serif headline → geometric sans).

## Worked examples

- **Friendly Whiteboard** — `references/example-osprey-v021.md`
- **Editorial Magazine** — `references/example-osprey-editorial.md`
- **Engineering Blueprint / Swiss Minimalist / Dark Tech / Scientific Poster** —
  no worked example yet. When generating one for the first time, follow the
  style block strictly, treat the OSPREY editorial example as the
  per-panel-content blueprint, and expect a v1→v2 hardening pass to refine
  the prompt the way the editorial variant needed.

Reuse the matching example 1-for-1 when the new task is also a multi-stage
data/methodology pipeline; only swap the per-panel content and the
bottom-ribbon / FIG-caption text.

## Style invariants (do not violate, regardless of variant)

- **English-only on canvas** — every label, equation, footer chip.
- **Default 18:9 cinematic wide** unless the user explicitly says otherwise.
- **Per-panel marker** (form depends on variant — circular badge / tabular
  "01" / "[01]" / huge "01" / neon chip / "(a)"). Always present, top-left.
- **No watermarks, no fake logos, no brand names**.
- **Always include the variant's "Hard negatives" bullet** in the prompt —
  without it, cues from neighboring variants leak through.

### Per-variant palette + identity reminders

- **Friendly Whiteboard** — teal #2EC4B6, coral #FF6B6B, mustard #FFB627,
  soft purple #7C5CFF, forest green #3FA34D, charcoal #2B2D42 text, off-white
  ground. Wavy strokes, stickers, sticky notes. Numbered circular badges.
- **Editorial Magazine** — deep navy #1A2E4F, ochre #C8932F, terracotta
  #B85A47, sage #6B8E5E, muted lilac #7C6BA1, warm charcoal #1B1B1B text,
  foil gold #B8902E accents, cream paper #FBF7F0. Precision vector linework,
  hairline rules + chevron dividers, serif headline. Tabular "01" markers
  with foil-gold underline. Sub-patterns: STATUS-BADGE / PULL-QUOTE /
  CONNECTION-LINE.
- **Engineering Blueprint** — navy ground #0A1F3D, grid #143257, cyan
  linework #6FE4FF, cream-white text #F4ECD8, amber #FFB000 critical, sage
  #B8D8BE OK, red-orange #FF6B5C reject. Monospace throughout, orthogonal
  bus-line dividers, "[01]" markers. Sub-patterns: DIMENSION-LINE /
  TERMINAL-NODE / STAGE-BOX.
- **Swiss Minimalist (reframed)** — paper white #F8F4EC, red #E63946,
  yellow #F4C95D, blue #1D3557, black #0B0B0B. At most 4 colors total,
  most panels use black + 1 accent. Single geometric sans typeface,
  hairline-rule dividers, prominent (~32–48pt) "01" markers (NOT 80pt
  hero numerals — that's the orthodox tone-dial mode). Methodology
  content (plots, equations, parameter cards) preserved inside panels.
  Sub-patterns: PROMINENT-NUMBER / PRIMARY-PLOT / GRID-CARD.
- **Dark Tech / Neon** — charcoal ground #0E1116, panel fill #15191F, cyan
  #00E5FF, magenta #FF3DAA, lime #C8FF3D, optional amber #FFB200, off-white
  text #E6EAF0, mid-grey #8892A6. NEON-CHIP rounded panels, glow-path
  connectors, monospace labels, "::" delimiter. Sub-patterns: NEON-CHIP /
  GLOW-PATH / MONOSPACE-LABEL.
- **Scientific Poster** — pure white #FFFFFF, black ink #000000, viridis
  data ramp #440154 → #FDE725, accent red #C1272D for emphasis only. Serif
  body, "(a)…(e)" panel labels, running FIG. N. caption below the panel
  row, inward tick marks, NO bottom ribbon. Sub-patterns: PANEL-LETTER /
  FIG-CAPTION / AXIS-LABEL.
