---
name: animated-deck
description: >-
  Build a self-contained, animated HTML presentation deck — a single .html file that
  scales to any screen, navigates by keyboard/click/swipe, and animates content and
  SVG node-edge diagrams (graphs, pipelines, flows, blast-radius) as each slide is
  shown. Use this skill whenever the user wants a slide deck, presentation, talk,
  pitch, training slides, a "deck like the last one", an animated or futuristic
  presentation, or wants to turn a document/report into slides — especially when they
  want diagrams that draw themselves, a portable single file with no build step, or a
  PDF export of slides. Also use this when the user wants the deck to match a corporate or
  PowerPoint brand template (.pptx/.potx) — it can extract that template's colours, fonts,
  slide size and logo and build the deck on-brand, or strip an existing .pptx down to its
  blank layouts to fill with new content. It also builds consulting-grade "poster"
  one-pagers — numbered stage panels, icon cards, red/green problem-to-solution colouring,
  outcome chips, architecture pipelines — whenever the user wants dense, professional
  corporate or enterprise-workshop slides, or shows a reference slide to match. Prefer this
  over the React/Vite slide-deck skill when the user
  wants one portable file, hand-drawn animated diagrams, or zero tooling. Do NOT use
  for static documents, Word/PowerPoint files, or dashboards.
---

# Animated Deck

Build a **single-file HTML presentation** that looks handcrafted, animates on every
slide, and runs anywhere — no npm, no build, no server. One `.html` file the user can
double-click, present full-screen, and export to PDF.

The whole thing is one artifact: a fixed **1280×720 canvas** scaled with CSS `transform`
to fit any viewport, a tiny vanilla-JS engine for navigation, and CSS/SVG animations
gated on the active slide so they **replay every time** a slide is shown.

## When to reach for this

- "Make a deck / presentation / slides for X", "turn this report into slides", "a deck
  like the last one", "an animated/futuristic presentation", "slides with diagrams".
- The user wants **one portable file**, **animated diagrams** (graphs, call-flows,
  pipelines, before/after), or a **PDF** of slides.
- The user wants the deck to **match a PowerPoint brand template** — extract its theme with
  `scripts/pptx_theme.py` and build the HTML deck on the brand (see step 2).
- The user wants to **strip a PowerPoint deck to a blank template** ("remove the content,
  keep the template, I'll add my own") — run `scripts/pptx_chrome.py INPUT.pptx -o out.html`
  to strip per-slide content while keeping recurring chrome and each slide's background as
  blank branded slides, each with an empty `.content` layer to fill. General, any deck.
  Details in `references/pptx-template.md`.

If the user instead wants a React/Vite project, component library, or live data
dashboards, that's the other `slide-deck` skill — not this one. The animated **diagrams**
fit directed flows and small DAGs (≲15 boxes). Quantitative charts are out of scope (use a
plotting tool); dense / auto-laid-out graphs are handled by wrapping Graphviz, not by hand
(see `references/diagrams/graphviz.md`).

## Workflow

1. **Get the content.** If a source exists (a report, notes, a doc), read it and pull
   the spine: cover → **agenda** → problem → concept → examples → payoff → close. If not, ask
   for the topic and rough outline. Never invent facts — ground every number in something real
   and say so on a `meta`/caption line. **Every deck of more than ~4 slides needs an agenda
   (contents) slide right after the cover** that lists the sections to come; it orients the
   audience and is expected in any professional/presentation deck. For a proposal or pitch,
   make claims defensible — prefer neutral, verifiable phrasing over bold marketing
   assertions the user would have to defend.
2. **Theme & chrome — inherit a provided template; never reinvent it.** If the user supplies
   a template or an existing deck to match, its **cover page, header band and closing page
   are brand assets**: scrape them and build on them exactly — do not restyle them,
   approximate them, or ship placeholder branding (the ACME wordmark in
   `corporate-light.html` is a placeholder to replace, never a deliverable).
   - **`.pptx` / `.potx`** — extract palette, fonts, slide size and logo with
     `python3 scripts/pptx_theme.py BRAND.potx` (add `--light` for a light corporate brand),
     and where LibreOffice+UNO is installed strip the deck to blank branded layouts with
     `scripts/pptx_chrome.py`, reusing its cover/band/end backgrounds as-is. Without
     LibreOffice, still apply the extracted theme and logo and rebuild the band/cover/end to
     match a screenshot of the template's master — the reuse rule stands even when the
     tooling path does not. Details: `references/pptx-template.md`.
   - **`.html` deck or template** — run
     `python3 scripts/deck_chrome.py THEIRS.html -o starter.html` to scrape the chrome: it
     keeps the cover and end slides verbatim and blanks one body slide down to its header
     band plus an empty `.content` layer, emitting a 3-slide starter that already passes
     `check_template.js`. Author on that starter — copy the blank body slide once per
     content slide and retitle its band per slide. See `references/pptx-template.md`
     ("Scraping an HTML deck's chrome").
   With no template provided, pick by audience: for a **business / enterprise / consulting** audience — or any
   request for a "professional corporate" look or a dense one-pager — start from CORPORATE
   NAVY (`assets/templates/corporate-light.html`: light, semantic panel colours, icon library,
   poster components). For a technical/futuristic register default to the NEON CYBER preset
   in the template, or the TERMINAL AMBER alt. For anything else, see `references/themes.md`. Aim for a distinctive, cohesive
   look — the `frontend-design` skill's principles apply: a characterful display font paired
   with a refined body font (avoid Inter/Arial/system defaults), a dominant colour with
   sharp accents (not a timid even palette), atmosphere and texture over flat fills, and one
   orchestrated load animation. Avoid generic AI aesthetics.
3. **Copy a template.** If the user supplied a template, your starting file is the scraped
   starter from step 2 — not a stock template. Otherwise start from `assets/template.html` (the NEON base) — it contains the
   engine, both palettes, and one example of every slide type. Other ready templates live in
   **`assets/templates/`** (e.g. `amber.html`, the five-kinds dark theme, and
   `corporate-light.html`, the consulting-grade light theme with icon library and worked
   poster slides); the user can also
   drop their own `.html` template there. Pick one and copy it. Never hand-write the scaling/nav
   engine; it is solved — just edit the `:root` theme and the slides. **If you use a template
   from `assets/templates/` (especially a user-supplied one), verify it first:**
   `node scripts/check_template.js assets/templates/<name>.html` — it checks the template
   honours the contract (fixed canvas, shot.sh-seedable engine, reveal gating, reduced-motion,
   slide roles). Fix any FAIL before building on it. See `assets/templates/README.md`.
4. **Author the slides.** One idea per slide; respect the density limits below. For any
   diagram, first **choose its type from the content's shape** (see "Choosing the diagram
   type"), then read `references/diagrams/geometry.md` plus the matching family guide.
5. **Verify by rendering AND checking.** Run `node scripts/check_diagram.js deck.html` and
   fix every reported issue, then screenshot with `scripts/shot.sh` and look — geometry,
   tip-alignment and label-collision bugs are invisible in source.
6. **Export PDF** if asked: `scripts/export_pdf.sh deck.html`.
7. **Translate** if asked (or to hand off to a translator/comtor): externalise the text with
   `python3 scripts/i18n.py key deck.html -o deck.keyed.html --strings strings.en.json`, let
   the comtor translate the JSON values, then re-bake a new single-file deck with
   `python3 scripts/i18n.py apply deck.keyed.html strings.vi.json -o deck.vi.html`. Technical
   tokens and code are excluded automatically. Re-render afterwards — a longer translation can
   overflow a slide. For a non-technical translator, `scripts/i18n-editor.html` is a
   self-contained browser GUI (offline, no LLM): open a deck, edit each string in a table with
   live preview, click Apply to download the rebuilt deck. See `references/i18n.md`.

## The template is the contract

`assets/template.html` is a complete, working deck. It defines:

- the scaled `#canvas` and the `#stage` that centres it,
- `.slide` / `.slide.active` and the `.r` **reveal** system (staggered fade-in that
  replays on every visit because it is gated on `.active`),
- ready components: `.eyebrow`, `h1/h2`, `.lede`, `.grid3`/`.stat`, `.calc`, `table`,
  `.flow`, `.note2`, and the animated `svg.graph` block,
- the nav engine (keys, click-halves, swipe, dot strip, progress bar, counter),
- `prefers-reduced-motion` support.

Add slides by copying a `<section class="slide">…</section>` block. The counter and dots
auto-update from the number of slides — no bookkeeping.

### The five slide kinds, and the three roles

A deck is built from **five kinds of slide**, in this order:

1. **Cover** — opening slide: deck title + framing line. One per deck.
2. **Agenda** — the contents list, right after the cover (see the agenda rule in the
   workflow). One per deck, for any deck past ~4 slides.
3. **Divider** — introduces a section: a big section number + section title (and an optional
   one-line framing). Optional, but **all-or-nothing** — see below.
4. **Body** — a content slide (heading + diagram / table / cards / bullets). The bulk of the
   deck; repeat per idea.
5. **Closing** — the final slide: one statement + a close line. One per deck.

These five are *functional kinds*, not five attribute values. Each slide also carries one of
**three `data-role` values** that decide its chrome treatment:
- `data-role="cover"` — the **cover** (full-bleed: no header band, large title).
- `data-role="slide"` — everything in the middle: **agenda, dividers, and body** slides all
  use this (they carry the header band / chrome). A divider is just a `slide` styled as a
  section break.
- `data-role="end"` — the **closing** slide (full-bleed, like the cover).

So the role attribute is `cover → slide × (agenda + dividers + bodies) → end`, and the deck
*reads* as **cover → agenda → [divider · bodies…] × each section → closing**. Cover and end
are full-bleed; everything between carries the chrome.

**Section dividers are all-or-nothing, and must match the agenda.** A divider is a slide that
introduces a section (often the dark/full-bleed template variant with just a section number +
title). If you introduce one section with a divider, introduce **every** section that way —
one divider per agenda item, in the same order as the agenda. Using a divider for one section
and skipping it for the others reads as inconsistent and unfinished. So a divider deck flows
`cover → agenda → [divider · content…] × each section → end`, and the divider titles mirror
the agenda lines exactly. If you would rather keep the deck tight, use **no** dividers at all
(agenda → content slides → end) — just don't mix the two. When a deck is built from a
PowerPoint template (`scripts/pptx_chrome.py`), the script sets `data-role` automatically and
prints which rendered slide is the cover, which are the body slides, and which is the end —
keep those roles when you pour content in. **Reuse the template's real cover and end
backgrounds (the branded photo / closing visual) and overlay text on them — never invent a
flat-colour cover or end.** See `references/pptx-template.md` ("Building a real deck on the
extracted template").

## Content density (keep slides breathing)

Every slide must fit 1280×720 with margin. If it overflows, split it — never shrink to
cram. Rough ceilings per slide:

| Slide type | Maximum |
|---|---|
| Title | 1 headline + 1 subtitle + 1 context line |
| Stat cards | 1 heading + 3 cards (one idea each) |
| Text/bullets | 1 heading + 4–5 short bullets, or 2 short paragraphs |
| Diagram | 1 heading + 1 diagram + 1 caption |
| Table | 1 heading + ≤4 rows + 1 note |
| Calc/payoff | 1 heading + the 3-cell strip + optional lede |
| Close | 1 statement + 1 line |

Headlines are short (6–9 words). Body text is scarce; the diagram or the numbers carry
the slide. Left-align prose — never centre paragraphs (centre only single captions).

**The poster exception.** A consulting-style **poster slide** — the whole argument
(challenge → mechanism → outcomes) laid out spatially with numbered stage panels, icon
cards and outcome chips — deliberately exceeds this table. It has its own ceilings and
construction rules in `references/diagrams/poster.md`; use it when the audience will
*study* the slide (workshops, steering reviews, reference architectures), keep it to 1–3
posters per deck, and note the font floors below still apply unchanged.

**Centre content in the open area — but keep titles on a consistent line.** A slide whose
content is jammed to the top with a large empty band below it looks unbalanced. On a **plain
(no-band) slide**, centre the whole body (title + content) vertically — the base template's
`.slide` already does this with flexbox. On a slide built on a **PowerPoint template with a
header band**, do *not* centre the whole block: pin the **title** at a fixed top just below
the band so it lands on the same line on every slide (centring each slide independently floats
the title to a different height — the most common "looks inconsistent" complaint), and centre
only the **content** in the area below the title (a `flex:1; justify-content:center` wrapper
under the pinned title). Pinning the title outside that wrapper also stops a tall table from
pushing the title up into the band. Either way, content sits centred in its open area, never
jammed to the top. The full banded-slide layout grid — section tag in the band, pinned title,
centred content, agenda-matched numbering — is in `references/pptx-template.md`.

### Minimum font sizes (readability floor)

The canvas is a fixed 1280×720 shown on a projector or shared screen, so text must stay
legible from the back of a room. **Never set any text below 14px**, and prefer these floors —
if content does not fit at these sizes, it is too dense: split the slide, do not shrink past
them.

| Role | Minimum | Comfortable |
|---|---|---|
| Headline (`h1`/`h2`) | 32px | 40–74px |
| Body / bullets / lede | 18px | 19–22px |
| Captions, notes, table cells, `meta` | 15px | 15–17px |
| Diagram node labels (`svg.graph` text) | 16px | 16–18px |
| Diagram sub-labels / edge captions | 14px | 14–16px |

14px is the hard floor for *anything*, including SVG sub-labels and edge captions.
`scripts/check_diagram.js` fails a diagram with a `FONT` issue if any `<text>` drops below
14px. The instinct to shrink a label to fit a small box is the wrong fix — enlarge the box,
shorten the text, drop a secondary sub-label, or move the detail to a caption instead. A
crowded diagram that only fits below 14px is a sign the diagram has too many annotations:
prune it rather than shrink it.

## Writing the content

- **One idea per slide.** If a slide has two arguments, it is two slides.
- **Show, don't tell** — prefer a diagram, a before/after, or a number to a paragraph.
- **Ground every claim.** Real numbers, real file names, real commands. Put the source on
  a `meta` or caption line so the audience trusts it.
- **Write in a professional register — always.** This is a presentation, not a chat
  transcript. No contractions in body text, no emoji, no decorative markers (`▶ ✓ ✕ →`)
  inside prose, no slang or jokey asides. Prefer declarative sentences and precise nouns
  ("Mitigation: route through rtk", not "→ just wrap it with rtk"). Title-case headings.
  When the source material is casual, translate it up into formal prose rather than
  echoing its tone — the register should not depend on how the request was phrased.
- Keep **code, identifiers, file paths, and domain terms verbatim** — do not translate or
  prettify them, even in a translated deck (translate prose, keep technical tokens).

## Animated diagrams — pick a family guide

Animated SVG node-edge diagrams are the deck's differentiator; invest here. This master
file owns deck **structure and language**; the diagram detail is split into focused guides
so only what you need loads. **Always start with the universal rules, then read the one
family guide that matches what you are drawing:**

- **`references/diagrams/geometry.md`** — mechanics (pop-in nodes, self-drawing edges,
  replay-on-activation) and the universal box/connector/fan/label rules. Read this for
  *every* diagram.

### Choosing the diagram type

The right diagram is decided by **the shape of the relationship in the content, not by the
word the user used** — people say "show this" far more often than "draw a funnel". Read the
content, name what kind of thing it is, and pick the row that matches. This is the step to
get right: a pipeline drawn as a table, or proportions drawn as boxes, reads as wrong no
matter how clean the geometry.

| If the content is essentially… | Draw a | Guide |
|---|---|---|
| ordered steps that transform input into output (A then B then C) | pipeline / dataflow | `flow.md` |
| many components with grouping and cross-links | architecture (nested groups) | `flow.md` |
| a process that repeats with no end | cycle / loop | `flow.md` |
| parallel tracks owned by different actors | swimlanes | `flow.md` |
| who calls / asks whom, a request and its response | call-flow / interaction | `interaction.md` |
| one source reaching many targets, or many feeding one | fan-out / fan-in (bus) | `interaction.md` |
| an ordered exchange between a few actors over time | sequence (lifelines) | `interaction.md` |
| two situations contrasted, or the reach of one change | before/after · blast-radius | `concept.md` |
| a set of states and the transitions between them | state machine | `concept.md` |
| containment or parent→child hierarchy | tree | `concept.md` |
| a chain of yes/no tests leading to outcomes | decision tree | `concept.md` |
| items classified on two independent axes | 2×2 matrix | `concept.md` |
| a quantity shrinking through stages | funnel | `concept.md` |
| events, phases, or milestones along a date axis | timeline / roadmap | `timeline.md` |
| parts of one whole that sum to 100% | pie / donut | `composition.md` |
| ranked tiers where size encodes effort or volume | pyramid | `composition.md` |
| one centre with independent members around it | radial (hub-and-spoke) | `composition.md` |
| several items compared across the same attributes | comparison table | `composition.md` |
| the whole argument on one slide — challenge → mechanism → outcomes, a dense corporate one-pager | poster (stage panels + icon cards + chips) | `poster.md` |
| a reference architecture of stage columns with sub-processes, a core, and consumers | poster architecture pipeline | `poster.md` |
| a dense / many-to-many mesh, or any graph needing auto-layout (>~15 nodes) | wrap Graphviz | `graphviz.md` |

When two rows seem to fit, keep the one that surfaces the relationship that matters: if the
content has a clear direction of flow it is a flow diagram; if it is discrete options judged
on shared criteria it is a table; if it is quantitative shares of a whole it is composition.
If nothing fits a diagram (it is just prose or a single number), use a stat-card or text
slide instead — do not force a diagram. And mixing types across a deck is good: a strong
deck often opens with a flow, compares with a table, and lands a proportion on a pie.

The full animation catalogue (traversal highlight, flow-dot, multi-stage reveals,
dim-the-rest focus) is in `references/animation-cookbook.md`.

**Verify diagrams with the checker — never by eye.** Geometry, tip-alignment and
label-collision bugs do not show in the HTML source:

```bash
node scripts/check_diagram.js deck.html   # flags PADDING / VCENTER / OVERLAP / TIP / LABEL
scripts/shot.sh deck.html <n>             # render slide n to a PNG and look at it
```

Iterate until the diagram slide reports `OK` and the PNG looks right.

Diagrams suit a hand-curated **directed flow / DAG of roughly 15 boxes or fewer**. They are
the wrong tool for quantitative charts (bar/line/scatter — there is no charting engine here;
use a real plotting tool). For a **dense / many-to-many mesh or any graph that needs
automatic layout**, do not hand-place it and do not reimplement layout: simplify it first
(aggregate, subgraph, or split), and if the whole graph must appear, wrap Graphviz with
`scripts/graphviz_embed.py` — it themes, fits and legibility-checks the result. See
`references/diagrams/graphviz.md`.

## Verify before delivering

Geometry and overflow bugs do not show in the HTML source. Render the actual slides:

```bash
scripts/shot.sh deck.html 3        # screenshot slide 3 (1-indexed)
scripts/shot.sh deck.html 1 16     # screenshot a range
```

It uses headless Chrome with `--force-prefers-reduced-motion` so every reveal is shown at
its final state instantly (animated captures are flaky under headless virtual-time — a
slide can come out blank even though it is fine in a real browser). Look at the PNGs, fix
endpoints/overlaps/overflow, re-shoot.

## Export to PDF

```bash
scripts/export_pdf.sh deck.html              # → deck.pdf, one slide per landscape page
```

It builds a print variant (all slides stacked, each a 1280×720 page) and renders it with
headless Chrome. The deck stays interactive; the PDF is a static handout. Details and the
print-CSS override are in `scripts/export_pdf.sh`.

## Common mistakes

- Hand-writing the scaling/nav engine instead of starting from the template. Don't.
- Rebuilding a provided template's cover, band or closing from scratch — or delivering the
  ACME placeholder wordmark — instead of scraping the chrome with `deck_chrome.py` /
  `pptx_chrome.py`. Inherited chrome is the whole point of being given a template.
- Building a dense poster slide as one giant SVG instead of HTML panels with embedded
  clusters — layout belongs to HTML; see `references/diagrams/poster.md`.
- Using the dark NEON default for a business/corporate audience — pick the theme by
  audience (workflow step 2); enterprise decks read best on CORPORATE NAVY light.
- Animating on load rather than on `.active` — the replay-on-revisit effect is the point.
- Forgetting `transform-box:fill-box` on a custom node → it flies in from the corner.
- Edge endpoints eyeballed instead of computed onto the border.
- Cramming a slide past 1280×720 — split it.
- Centring body paragraphs. Centre only single captions/notes.
- Casual tone, emoji, or `→`/`✓`/`✕` markers in prose — keep the register professional.
- Diagram geometry/label slips (floating tips, edges hidden in a wrapper, captions on a
  line, uneven padding) — these all live in `references/diagrams/geometry.md`; obey it and
  let `scripts/check_diagram.js` catch what the eye misses.
- Claiming the deck works without rendering it. Run the checker and screenshot first.
