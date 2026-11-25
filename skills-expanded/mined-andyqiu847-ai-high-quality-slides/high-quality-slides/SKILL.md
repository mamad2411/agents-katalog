---
name: high-quality-slides
description: Use this skill when the user asks for a "high-quality" / "professional" / "Genspark-style" / "投资人级别" / "演示级" deck, or when they reference Genspark, Gamma, beautiful HTML slides, or pixel-perfect presentations. Trigger on requests like "做一份PPT", "生成幻灯片", "pitch deck", "做汇报", or when the user uploads research material (PDF/Excel/Word/notes/URL) and wants it turned into slides. Produces HTML decks (pixel-perfect, animation-capable, fully self-contained) and/or .pptx (editable). Do NOT trigger for plain Word docs or generic "summarize this" — only when a slide-shaped artifact is the deliverable.
---

# High-Quality Slides Skill

> Goal: replicate Genspark AI Slides' "feels designed, not templated" quality bar inside Claude. Optimized for the **decisive content + curated visual** philosophy, not the "wall of bullet points on a stock theme" pattern.

This skill is opinionated. Do not skip phases. Most low-quality AI decks fail at Phase 1–3 (no research, no narrative, no visual concept) and overinvest in Phase 4 (typography polish on garbage content). This skill inverts that.

---

## Operating principle

A great deck = `research × narrative × visual system × per-slide layout decisions`. If any one factor is zero, the deck is zero. The model's job is to be a **slide art director**, not a content shoveler.

Three rules that override everything else:

1. **One idea per slide.** If a slide has more than one assertion, split it.
2. **Visual relationship > text list.** Whenever bullet points appear, ask "can this be a 2×2, timeline, comparison table, stat strip, or diagram?" Default answer: yes.
3. **Pixel-perfect, viewport-locked.** Every slide fits in a fixed canvas (1920×1080 default). No overflow, no scroll-within-slide, no responsive text reflow.

---

## Five-phase workflow (mandatory order)

Modeled on Genspark's Guide Mode. Each phase has a **gate** — do not advance until the gate passes.

### Phase 1 — STRATEGY (audience & purpose)

Ask, or infer from context, then state back in one paragraph:

- Who is the audience? (board / customer / team / conference / academic)
- What is the single decision or action the audience should take after seeing this?
- What's the room? (live presentation, sent as PDF, embedded on web)
- Time budget for delivery? (drives slide count)
- Brand constraints? (logo, color, font, existing template)

**Gate:** if audience or call-to-action is unknown, ask the user with AskUserQuestion. Do not proceed.

### Phase 2 — SUBSTANCE (research & evidence)

Collect the raw material before designing anything. **Never invent statistics or quotes.**

Sources, in order of priority:
1. Files the user uploaded — read every one (Read tool, OCR via Python if needed).
2. URLs the user provided — fetch.
3. Connected MCP data (Slack, Asana, Drive, analytics).
4. WebSearch — only for facts the user couldn't supply, and only with citations.

Produce a `research-notes.md` scratchpad in the outputs folder with: claims, numbers, quotes, source URLs, image candidates (URLs or descriptions). This file is throwaway but you must produce it — it forces evidence discipline.

**Gate:** every assertion that will appear on a slide has a source in research-notes.md.

### Phase 3 — STRUCTURE (narrative & outline)

Choose a narrative arc that fits the goal. Default arcs:

| Arc | When to use | Slide skeleton |
|---|---|---|
| **Problem → Solution → Proof → Ask** | Pitch, sales, fundraising | Hook · Problem · Why now · Solution · How it works · Traction · Team · Ask |
| **Situation → Complication → Resolution** | Strategy memos, board updates | Where we are · What changed · What we propose · Plan · Risks |
| **Finding → Evidence → Implication** | Research, analytics reports | TL;DR · Method · Finding 1..N · So what · Next steps |
| **Before → After → Bridge** | Change management, launches | Today · The shift · What it enables · How we get there |
| **Chronological** | Quarterly review, retro | Timeline · Theme per period · Lessons · Forward look |

Output a numbered outline. **For each slide, write three things only:**
1. **Headline assertion** (≤ 12 words, declarative — "Revenue doubled in Q3", NOT "Q3 Revenue")
2. **The one supporting fact** (a number, a quote, a comparison)
3. **The intended visual** (chart type / diagram / photo / icon set / typographic)

**Gate:** user reviews the outline. Do NOT design slides before the headline list is approved. Use AskUserQuestion to confirm or ask for edits.

### Phase 4 — DESIGN SYSTEM (style & density)

Choose the visual system **once**, apply consistently. Do not "design each slide" — design the system, then instantiate slides from it.

Required design tokens (write to `design-tokens.css` as CSS custom properties):

```css
:root {
  /* Canvas */
  --slide-w: 1920px;
  --slide-h: 1080px;
  --safe-pad: 96px;        /* outer padding, ~5% of width */

  /* Type scale — pick ONE display font + ONE text font */
  --font-display: "Inter", system-ui, sans-serif;
  --font-text:    "Inter", system-ui, sans-serif;
  --fs-hero:      120px;   /* title slide */
  --fs-h1:        72px;    /* slide headline */
  --fs-h2:        44px;
  --fs-body:      28px;
  --fs-caption:   20px;
  --lh-tight:     1.1;
  --lh-body:      1.4;

  /* Color — pick ONE base + ONE accent. No more. */
  --bg:        #0B0B0C;
  --fg:        #F5F4F0;
  --muted:     #8C8A85;
  --accent:    #FF5A1F;
  --surface:   #17171A;
  --line:      rgba(255,255,255,.12);

  /* Grid */
  --col: 12;
  --gutter: 32px;
}
```

Pick a **style preset** from `layouts.md` (see attached). Presets encode color + type + grid + motion, e.g. `bold-signal`, `swiss-modern`, `editorial-serif`, `dark-botanical`, `neon-cyber`, `notebook-tabs`. If the user can't articulate a preference, **generate 3 preset previews** (single hero slide for each) and let them pick — this is the "show, don't tell" trick that makes the user feel ownership of the design.

Density rules (override per-slide judgement only with reason):
- Title ≤ 12 words. Body ≤ 30 words OR ≤ 5 list items.
- One hero element per slide (chart OR quote OR photo OR diagram — not all four).
- Whitespace ≥ 30% of canvas.

**Gate:** preset chosen, tokens written, single sample slide approved before mass generation.

### Phase 5 — BUILD (generate slides)

Generate slides as **HTML**, one `<section class="slide">` per page, single self-contained file, inline CSS/JS, viewport-locked. Use the patterns in `html-template.md`.

For each slide in the outline:

1. Choose a **layout pattern** from `layouts.md` based on the intended visual: `cover`, `headline-only`, `three-stat-strip`, `quote-hero`, `two-column-compare`, `timeline`, `process-flow`, `2x2-matrix`, `chart-focus`, `image-with-caption`, `data-table-clean`, `kpi-grid`, `section-divider`, `closing-cta`.
2. Drop in the headline + supporting fact + visual.
3. Render the visual:
   - **Charts** → inline SVG (preferred) or Chart.js / D3 from CDN. Real data only. Strip chartjunk: no gridlines unless necessary, no 3D, no default rainbow palettes — use the accent color + neutrals.
   - **Diagrams** → hand-built SVG or HTML/CSS boxes with the design tokens. Avoid mermaid for hero diagrams (looks generic); use it only for technical flow appendices.
   - **Icons** → Lucide via CDN, OR inline SVG. Consistent stroke width across the deck.
   - **Photos** → only if the user provided them, or via clearly-licensed source. Apply a duotone or grayscale-with-accent treatment so stock images don't break the system. If no real photo, **prefer a typographic/abstract treatment over a generic AI image.**
   - **Smart visualization** (Genspark's edge): match content semantics to visual form. Code → terminal mockup. Comparison → side-by-side cards. Process → arrowed steps. Numbers → big number + tiny label. Quote → oversized punctuation. This is the single biggest quality lever.

Then run the **self-check** before delivery:
- [ ] Every slide has exactly one headline assertion (declarative, ≤ 12 words).
- [ ] No two slides use the exact same layout in a row (unless intentional sequence).
- [ ] All numbers/quotes trace to research-notes.md.
- [ ] No text overflows the safe area at 1920×1080.
- [ ] Color usage: ≤ 1 accent color, used sparingly (< 20% of pixels).
- [ ] No emoji unless the brief is informal.
- [ ] Final slide has a clear CTA / next step (matches Phase 1 audience action).

If a check fails, **fix the slide, do not ship**.

### Optional: pptx export

If the user needs an editable `.pptx`:
1. First produce the HTML deck (it's the design source of truth).
2. Then call the `pptx` skill, passing the outline + design tokens + per-slide layout choices as the construction plan. The HTML serves as the visual reference.
3. Note in the handoff: complex SVG diagrams may need to be rasterized for pptx compatibility — call this out to the user.

---

## Anti-patterns (these are what makes AI decks look like AI decks)

Refuse these by default. If the user insists, comply but note the trade-off.

- Purple-to-blue gradients on white. Generic.
- Stock photos of diverse people pointing at laptops.
- 7+ bullet points per slide.
- "Title Case Every Word" headlines that don't make an assertion.
- Decorative AI-generated images that don't carry information.
- Same icon pack used for unrelated concepts.
- Default Chart.js color palette.
- Footer with date + page number + company name + tagline (pick one).
- "Thank You / Questions?" closing slide — replace with a real CTA.

---

## Files in this skill

| File | When loaded | Purpose |
|---|---|---|
| `SKILL.md` | Always | Workflow, gates, anti-patterns |
| `layouts.md` | Phase 4–5 | 14 layout patterns + 12 style presets with code |
| `html-template.md` | Phase 5 | Canvas HTML scaffold, navigation, print/export |
| `scripts/extract_uploads.py` | Phase 2 | Pull text+images from pdf/docx/pptx uploads |

Load files on demand. Do not preload everything into context.

---

## Quick reference — what the agent actually does, step by step

```
1. Parse the brief → identify audience, action, format, slide count, brand.
2. If anything in (1) is unknown → AskUserQuestion. Do not start.
3. Read all attached files + fetch URLs → write research-notes.md with sources.
4. Propose narrative arc + numbered outline (headline + fact + visual per slide).
   → AskUserQuestion to confirm outline. Iterate until approved.
5. Propose 2–3 style preset previews → user picks one.
6. Write design-tokens.css. Build sample slide. Confirm with user.
7. Generate full HTML deck, one layout-pattern per slide based on visual intent.
8. Run the self-check list. Fix anything that fails.
9. Save deck.html + research-notes.md + design-tokens.css to outputs folder.
10. (Optional) Export to .pptx via the pptx skill, using the HTML as the spec.
11. Hand back computer:// links. Offer one round of revisions.
```

Last note: the user does not care about your process. They care about getting a deck that looks like a designer made it. The phases exist to force that outcome — keep them, but communicate progress in plain language, not jargon.
