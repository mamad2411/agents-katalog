---
name: consulting-deck
description: Build consulting/think-tank quality slide decks with action titles, data exhibits and a rendered visual-QA loop. Use when the user asks for a deck, presentation, slides, board pack, or a "final slide" summarising a decision case. Produces a PDF, per-slide PNGs, and an editable PowerPoint.
allowed-tools:
  - Read
  - Create
  - Edit
  - Execute
  - Glob
  - Grep
version: 1.0.0
metadata:
  owner: keigo
---

# Consulting deck

Slides are authored as **HTML/CSS against a fixed component library**, rendered
with Chromium, reviewed visually by you, then exported. One source file yields
three artifacts: per-slide PNGs (for your own review), a print-fidelity PDF, and
an editable `.pptx`.

Do not reach for PptxGenJS, `python-pptx`, or a PowerPoint MCP. Those make you
compute absolute shape coordinates, which is where layout defects come from, and
they cannot be reviewed without a separate rendering step.

## Supporting files

| File | Read it when |
| --- | --- |
| `design-system.md` | Always, before writing the first slide. Slide grammar and the full CSS component reference. |
| `charts.md` | The deck needs any graph, chart, or data exhibit. |
| `case-mapping.md` | The deck summarises an AgentAdvisor case from `cases/<case-id>/`. |
| `assets/deck.css` | Never edit. Extend with a deck-local `<style>` override block instead. |
| `assets/template.html` | Copy as the starting skeleton. |

## Workflow

### 1. Establish the storyline before touching HTML

Write `<workdir>/outline.md` first, one line per slide, each line being the
**action title** you intend to use. If the titles read top to bottom as a
coherent argument, the deck works. If they read as a list of topics, restructure
before building. This step is not optional and it is where deck quality is won.

Standard consulting arc:

1. Title
2. Executive summary (the answer, stated first)
3. The question and why it matters now
4. Approach / what was assessed
5. Findings, one slide per finding, each with one exhibit
6. Alternatives and why they rank below the recommendation
7. Scenarios and quantified uncertainty
8. What would change the recommendation
9. Next actions with owners and dates
10. Appendix: evidence, method, sources

Confirm the outline with the user before building slides unless they asked for a
first draft to react to.

### 2. Set up the working directory

```bash
mkdir -p tmp/deck/charts
cp .factory/skills/consulting-deck/assets/template.html tmp/deck/slides.html
```

Everything lives under `tmp/deck/`. Do not write decks outside the current
working directory.

### 3. Generate charts before writing the slides that use them

Every number on a slide must come from executed code, never from prose
arithmetic. Read `charts.md`, write a script under `tmp/deck/`, and run it so
the PNGs exist in `tmp/deck/charts/` before you reference them. If the deck
summarises a case, the script reads that case's artifacts rather than numbers
you retyped.

### 4. Write the slides

Author `tmp/deck/slides.html` using only the classes in `design-system.md`.
Link the stylesheet with a relative path and reference charts as ordinary
`<img src="charts/....png">`; the build step inlines both.

Hard rules:

- Every content slide has an action title that is a full sentence making a claim.
- One message per slide, supported by at most one exhibit.
- Every slide showing data carries a `<p class="src">` source line.
- No `<script>`, no remote fonts, no remote images, no CDN links.

### 5. Build

```bash
python3 .factory/skills/consulting-deck/scripts/build_deck.py tmp/deck/slides.html
```

This inlines the CSS, base64-encodes the images, and writes:

- `tmp/<name>.preview.html` — for rendering and review
- `tmp/<name>.pptx.html` — the editable PowerPoint source

### 6. Render and run the visual QA loop

```bash
node .factory/skills/consulting-deck/scripts/render_deck.mjs tmp/deck.preview.html
```

Writes `tmp/deck-render/slide-01.png ...`, `tmp/deck.pdf`, and a
`tmp/deck-render/report.json`. Findings are split into `error` (overflow,
out-of-frame, clipped text) and `advice` (underfull slide, undersized type).
The command exits non-zero only on errors.

Then, and this is the part that produces a good-looking deck:

1. Read `report.json`. Fix every error. Judge each advisory on the merits, since
   a sparse appendix table is fine and a sparse argument slide is not. Rebuild.
2. **Read the slide PNGs as images.** Look at them. Check for text colliding
   with an exhibit, orphaned single words, uneven column baselines, a chart
   whose axis labels have shrunk to nothing, inconsistent left margins between
   slides, and a last slide that is half empty.
3. Fix, rebuild, re-render, look again. Two or three passes is normal.

Do not report the deck as finished before looking at the rendered images.
`report.json` catches geometry, not ugliness.

### 7. Deliver

Tell the user they have a PowerPoint and a PDF. Do not mention HTML, CSS, or the
build pipeline unless they ask. The `.pptx.html` file is picked up by Factory's
PowerPoint renderer, so the deck previews inline with a working download button.

## Success criteria

Before calling the deck done:

- [ ] Outline titles read as a connected argument
- [ ] `report.json` has zero errors and every advisory has been considered
- [ ] Every slide PNG has been visually inspected in this session
- [ ] Every number traces to a script under `tmp/deck/`
- [ ] Every data slide has a source line
- [ ] The PDF opens and page count matches slide count

## Presentation vs. reading deck

The default type scale is a **reading deck**: dense, ~28px titles, ~15px body,
meant to be sent and read without a presenter. If the user will present it from
a stage, add `class="deck--present"` to `<body>`, which scales type up and
reduces the content each slide can hold. Ask which one they need if it is not
obvious.
