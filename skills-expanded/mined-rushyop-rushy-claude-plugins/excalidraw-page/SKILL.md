---
name: excalidraw-page
description: >
  Generate self-contained HTML pages in a fixed Excalidraw-style design system —
  warm paper background, ink text, hand-drawn Mermaid diagrams (rough/sketch look),
  wobbly sketch-border cards, marker highlights, hand-written headings, status pills,
  wireframe boxes, phase timelines, and a sticky section TOC. The design is locked;
  only the content changes. Use this whenever the user asks for a plan page, rewrite
  plan, architecture doc, design review, proposal, project recap, or any visual HTML
  explainer in a "sketch", "whiteboard", "hand-drawn", "excalidraw", or "x-cali"
  style — and whenever they say "like the CMD plan page" or "the usual plan design".
  Prefer it over ad-hoc styling any time a planning/architecture document needs to
  ship as a polished HTML page.
---

# Excalidraw Page

Produce documents that look hand-drawn on paper but behave like a polished web page:
interactive zoomable diagrams, sticky navigation, light/dark support, zero external
build steps. One file in, one file out.

## Workflow

1. **Copy the template.** Start every page from `assets/template.html` (next to this
   file). Copy it to the output location — `~/.agent/diagrams/<descriptive-name>.html`
   unless the user asks for a different path — and edit the copy. Never write the page
   from memory: the template *is* the design system, and retyping it drifts.
2. **Replace the content.** Everything inside `<div class="main">` is placeholder demo
   content. Replace it with the real document. Update the `<title>`, the `h1`, the
   `.subtitle`, and the TOC links. The blocks marked `DESIGN CORE` (the `<style>` block
   and both `<script>` blocks) stay byte-identical.
3. **Structure the sections.** Each section is a `.sec-head` with `id="s1"…"sN"` plus a
   `.sec-sub` intro line; the TOC (`nav.toc`, first child of `.wrap`) carries one link
   per section with matching `href="#sN"`. Fewer than 4 sections → delete the TOC
   entirely (it adds clutter below that).
4. **Compose from the catalog.** Build section bodies from the component catalog —
   sketch cards, tables with status pills, diagram shells, wireframes, phase timelines,
   collapsible trees, checklists. Read `references/components.md` for copy-paste markup
   of every component and its usage rules.
5. **Verify before delivering.** Open the page (needs network for fonts + the Mermaid
   CDN). Check: zero console errors, every diagram shell shows an SVG (a zoom label
   stuck on "Error: …" means a Mermaid syntax problem), no horizontal overflow at
   desktop width. If a browser tool is available, automate this check.
6. **Deliver.** Open the file in the user's browser (`open <path>` on macOS) and report
   the path.

## Design invariants — never change these

The whole point of this skill is that every page looks like it came from the same
sketchbook. Treat the following as fixed:

- **Fonts**: Gochi Hand (headings, labels, chips, wireframes, diagram text),
  DM Sans (body), Fira Code (mono). Loaded from Google Fonts in the template head.
- **Palette**: paper `--bg` + ink `--text` with the five Excalidraw accents
  (blue/red/green/orange/violet) and a yellow `--marker`. Light and dark are both
  defined; never hardcode colors that bypass the variables.
- **Sketch borders**: the wobbly look comes from asymmetric `border-radius` pairs on
  `.sk` / `.sk.alt` / `.mermaid-wrap` — don't straighten them, and alternate
  `.sk` / `.sk.alt` between neighboring cards so borders don't repeat.
- **Diagrams**: Mermaid 11 with `look: 'handDrawn'`, ELK layout, and a theme wired to
  the palette — already configured in the DESIGN CORE script. Flowchart,
  sequenceDiagram, gitGraph, and erDiagram all render pre-themed.
- **Dotted paper background**, staggered `fadeUp` entrances via `--i`, and
  `prefers-reduced-motion` respect.
- **Built-in theme toggle**: a fixed ☀/☾ button (top-right, bottom-right on mobile)
  overrides the system theme, persists to localStorage, and re-renders every Mermaid
  diagram in the new palette. It ships in the template — keep it, don't rebuild it.

## Content rules

- Accent by meaning, not decoration: green = good/in-scope/done, red = risk/out-of-scope,
  blue = neutral/structure, orange = new/changed, violet = agentic/AI. Apply via
  `data-a="…"` on cards and `.callout--…` / `.st-…` / `.tag--…` variants.
- Use `.tag` chips to mark process ownership (🤖 agent / ✋ human / ⚙ deterministic) and
  model names — put the legend near the top when tags are used.
- `.mk` marker highlights are for the handful of phrases the reader must remember —
  more than ~2 per section and they stop working.
- Long reference material (file trees, schemas, appendices) goes inside `<details>` so
  the page's hierarchy stays: overview and architecture dominate, reference collapses.
- Lead the page with a one-paragraph summary and stat `.chip`s — the first viewport
  should make the main idea obvious.

## Diagram authoring

Duplicate the whole `.diagram-shell` section per diagram; only the
`<script type="text/plain" class="diagram-source">` content changes. The init script
picks up every shell automatically — no per-diagram JS.

- Prefer `flowchart TD`; use `LR` only for short linear flows.
- Line breaks inside labels: `<br/>` in quoted labels — never `\n`.
- Emphasis colors inside a diagram: use the theme-aware palette tokens, never raw hex —
  `style NODE fill:@violet-fill,stroke:@violet,color:@ink`. Tokens (`@blue`, `@blue-fill`,
  `@red`, `@green`, `@orange`, `@violet`, their `-fill` pairs, and `@ink`) are substituted
  at render time for the active theme, so styled nodes stay readable when the user
  toggles light/dark. Raw hex would freeze a node in one theme's colors.
- 15+ elements → split into a small overview diagram plus detail cards instead of one
  giant graph.
- Don't define page-level CSS named `.node` — Mermaid owns that class internally.

## Pitfalls

- Grid/flex children need `min-width: 0` (already on `.main`, `.sk`, `.w-col`) — keep it
  when adding new grid content, or long code strings will blow the layout open.
- Wide tables must stay inside `.tbl-wrap` (it provides the scroll container).
- The page needs network access to render (fonts + Mermaid ESM from jsdelivr). If the
  user needs a fully offline page, say so and inline the dependencies on request —
  that's the one sanctioned deviation.
- Keep every non-ASCII glyph intentional: the tags use 🤖 ✋ ⚙ deliberately; stray
  characters in prose are a review smell.

## References

- `references/components.md` — the full component catalog: exact markup for hero,
  cards, tags, chips, tables, status pills, callouts, diagram shells (all four diagram
  types), wireframes, phase timeline, details/tree, checklist, footer, TOC rules.
  Read it before composing a page for the first time in a session.
