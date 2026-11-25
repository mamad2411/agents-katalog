---
name: create-slides
description: Create or revise a branded Slidev presentation with OfficeKit. Use for pitch decks, talks, lectures, workshops, demos, kickoffs, internal reviews, slides, PDF export, or PowerPoint.
compatibility: Requires an OfficeKit workspace created by setup-office-kit, Node.js 22+, npm, Python 3.10+, and uv.
metadata:
  author: OfficeKit
  version: "0.2.0"
---

# Create OfficeKit slides

Work in `.office-kit/`. If absent, use `setup-office-kit` first. Author in the
main agent. Research claims directly with host-provided tools when necessary;
write verified sources to `projects/<slug>/reports/research.md`.

## Boundary

Edit only:

- `projects/<slug>/slides.md`
- `projects/<slug>/styles/brand.css`
- `projects/<slug>/components/`, `layouts/`, and `public/` when needed
- the project plan and reports

Never inspect or edit `node_modules`, `package-lock.json`, or Vite internals.
Never run Slidev directly. The OfficeKit Python script owns installation,
preview, audit, stop, and export.

## Pass

From `.office-kit/`, scaffold and immediately start a verified preview:

```bash
uv run python scripts/presentation/deck.py new <slug> --title "…" \
  [--brand <id>]
uv run python scripts/presentation/deck.py dev <slug>
```

Tell the user the URL only after `dev` prints it. If preview health later
fails, run `deck.py stop <slug>` then `deck.py dev <slug>`; do not investigate
dependencies.

While preview runs, write a short `plan/PLAN.md`: purpose, audience,
constraints, brand ID, slide sequence, visual intent, accessibility, assets,
delivery request, and acceptance criteria. No plan approval gate.

Use only built-in layout names carried by the template, including `cover`,
`default`, `center`, `section`, `statement`, `two-cols`,
`two-cols-header`, `fact`, `quote`, `image-right`, and `end`. Every slide
declares a real layout. Reorder, duplicate, or remove the scaffold vocabulary
slides as the narrative demands.

Prefer the template's authored `ok-*` classes (`ok-hero`, `ok-bands`,
`ok-flow`, `ok-outcome`, `ok-icon-line`, and related classes). Use bundled
Lucide components such as:

```html
<lucide-eye class="ok-icon" />
```

Content slides should not be only a heading and bullets; use a meaningful
diagram, comparison, number, image, flow, or icon structure. Never hardcode
brand colors, fonts, or logo paths. Preserve user assets under `public/`.

For evidence, reach for the template's figure vocabulary before another icon
card: `ok-figure` (image plus `figcaption`), `ok-shot` (framed screenshot),
`ok-split` / `ok-split-1-1` / `ok-split-2-3` (figure beside copy), `ok-table`
on a table, `ok-code` for a literal excerpt, and the bundled `<OkBars>`
component for a grouped bar chart drawn from literal numbers (series colours
`.ok-s0`…`.ok-s3` map to primary, accent, secondary, muted). Put images under
`public/`, reference them as `/name.ext`, and give every `<img>` a non-empty
`alt`; prefer a local file to a remote URL.

Component contracts the audit checks: `ok-flow` holds exactly three
`ok-step` children with `ok-flow-join` between them; each `ok-band` has at
most two element children (the mark, then one wrapper holding `h3` + `p`);
`ok-hero-num` holds text, not an element.

Build in logical groups while the live preview updates, recording progress in
`reports/build.md`. Then run:

```bash
uv run python scripts/presentation/deck.py audit <slug>
```

Audit must exit 0. While the preview runs, audit also renders every slide
at the canvas size, fails on content that extends past the slide or an image
that did not load, and writes one PNG per slide to `reports/render/`
(`--render` starts a preview if needed, `--no-render` skips the pass,
`--dark` adds a dark-scheme pass). Look at those PNGs; a static pass cannot
judge a visual medium. Review narrative, overflow, readability,
accessibility, brand fidelity, visual variety, speaker flow, and acceptance
criteria; fix findings and write `reports/review.md`.

Export only when requested:

```bash
uv run python scripts/presentation/deck.py export <slug> \
  [--format pdf|pptx|png|html]
```

`html` writes `dist/slides.html`: one self-contained file with a built-in
player (present mode with click steps, a browse mode that stacks slides for
reading and commenting, overview, `#n` slide links, fullscreen) and no Slidev
server. Use it when the deck must be shared as a link, opened from disk, or
published to a store that takes a single HTML body. Keep click-driven
content to `v-click`/`v-clicks`/`v-after`, because `v-if`/`v-switch` export in
their final state. Read the warnings it prints.

Record delivered paths in `reports/delivery.md`. A preview or stale `dist/`
file is not a delivery.
